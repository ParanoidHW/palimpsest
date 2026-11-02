---
tags:
  - topic/speculative-decoding-training
  - collection/speculative-decoding
  - domain/model-systems
document_type: topic
domain: model-systems
collection: speculative-decoding
review_status: planning
canonical: true
---

# DeepSpec online_train 后续算法与实验规划

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[投机推理方法时间演进调研](../surveys/evolution.md)
> - 相关 Paper：[DSpark](../papers/dspark.md)、[DFlash](../papers/dflash.md)、[DeLS-Spec](../papers/dels-spec.md)、[DPara](../papers/dpara.md)、[DLoop](../papers/dloop.md)、[D-Loop](../papers/d-loop.md)、[DRelay](../papers/drelay.md)
> - 相关 Topic：[Speculator 训练的数据生命周期与框架策略](speculator-training-data-lifecycle.md)、[RL 期间的 drafter 联合适配](rl-drafter-cotraining.md)

## 0. 规划状态与基线口径

本文是面向 DeepSpec-npu `online_train` 分支的算法和实验规划，不是论文精读，也不是已执行的实验报告。本文基于仓库 `online_train` 分支提交 `2b730e8c7142f7f516c4c5a4b476f765e95de1` 和已有投机推理 Survey/Paper 形成。

用户提供的当前 baseline 口径为：

- 训练数据：约 40 万条样本；
- global batch size：32；
- 训练轮数：3 个 epoch 以上；
- draft 结构：`block_size=5`，3 层 drafter；
- target 条件特征：第 `[40, 41, 42]` 层 hidden states；
- 当前接受长度：约 `2.7`。

仓库内的 `scripts/train/train_online_8card_tcp.sh` 是默认启动示例，仍写有 5 万 prompt、global batch 512 和 3 epoch；它不能作为本次 2.7 baseline 的实验口径。后续每个实验必须把实际样本数、global batch、epoch、有效 optimizer step、target checkpoint、tokenizer、chat template、数据生成版本和 producer commit 写入实验记录。

## 1. 先锁定“2.7”到底是什么

这是 P0 阶段，所有后续实验都依赖它。仓库当前同时维护两种接受长度：

1. **greedy 连续接受长度**：逐位置比较 draft 与 target 的 top-1 token，在第一个不匹配处截断，再加 target bonus token。实现见 `deepspec/modeling/dspark/loss.py:84-109`。
2. **rejection-sampling 概率期望接受长度**：先计算

   $$
   a_i=1-\frac{1}{2}\lVert p_{draft,i}-p_{target,i}\rVert_1,
   $$

   再计算前缀连乘并求和，最后加 1。实现见 `deepspec/modeling/dspark/loss.py:113-137` 和 `:45-62`；公式和指标定义见仓库 `docs/configuration.md:216-241`。

如果 2.7 来自 greedy 指标，就应优化真实连续 prefix；如果来自 probabilistic 指标，就不能直接把它当成线上 token 命中长度。两个指标必须同时报告：`greedy_accept_length`、`rejection_accept_length`、`accept_rate@0..4`、每轮实际 target forward 次数和端到端 tokens/s。

此外，建议新增以下诊断指标：

| 指标 | 为什么必须有 | 解释 |
|---|---|---|
| `accept_rate@position` | 定位是首位错还是后位退化 | 首位低优先改条件特征/数据；后位低优先改块内条件化与训练目标 |
| first-rejection position | 直接对应连续 prefix | 比平均接受长度更容易定位失败位置 |
| confidence calibration | 当前 confidence head 的目标是概率接受率，不是实际二值结果 | 需要 ECE、Brier、分桶可靠性曲线 |
| draft entropy / target entropy | 区分模型不确定性和条件失配 | 支撑动态 block、难例采样和拒绝反馈 |
| valid block ratio | 排除 padding、无效 anchor、短样本造成的假改善 | 当前 `eval_mask` 和 `block_keep_mask` 会改变有效分母 |
| draft/verify/transfer latency | 接受长度不是 wall-clock speedup | online_train 还包含 producer、Mooncake 和 host/device transfer |

## 2. 当前实现的可利用点与瓶颈

### 2.1 已有结构

DeepSeek-V4 recipe 在 `config/dspark/dspark_deepseek_v4_flash.py:45-77` 固定了 `block_size=5`、`num_draft_layers=3`、`target_layer_ids=[40,41,42]`、`markov_rank=256`、confidence head，以及 CE/L1/tau 损失。drafter 的第一层把三层 target feature 拼接后投影，见 `deepspec/modeling/dspark/deepseek_v4/modeling.py:1127-1167`；最后一层再经过 DeepSeek-V4 的 HC head folding、Markov bias 和 confidence head，见 `:1169-1194`、`:1250-1283`。

训练前向从有效 loss token 中随机采样 anchor，构造一个 anchor 加五个 mask 位置的 block；同一 block 内的 draft 位置并行计算，见 `deepspec/modeling/dspark/common.py:194-258`、`:327-360` 和 `deepspec/modeling/dspark/deepseek_v4/modeling.py:1556-1667`。这说明当前主要矛盾不是“还没有 block draft”，而是：

- 5 个位置的条件信息是否足以支撑连续 prefix；
- 训练目标是否和线上实际接受规则一致；
- 随机 anchor 是否覆盖了高价值的 first-rejection 场景；
- 在线 producer 返回的 target features 是否和训练样本、target 版本严格一致。

### 2.2 训练目标的限制

当前 loss 是加权 CE、概率分布 L1、可选 tau loss 和 confidence BCE 的线性组合，见 `deepspec/modeling/dspark/loss.py:346-378`、`:381-473`。DeepSeek-V4 配置默认 `ce_loss_alpha=0.1`、`l1_loss_alpha=0.9`、`tau_loss_alpha=0.05`、`confidence_head_alpha=1.0`。

这套目标有三个需要先实证的假设：

1. **L1 分布距离是接受率的足够代理。** 它与拒绝采样概率有关，但不直接优化“第一个错误前的连续 prefix”。
2. **位置指数衰减适合 5 个位置。** `loss_decay_gamma=4.0` 在 `loss.py:30-42` 对后位逐渐降权，但后位错误可能由前位条件失配引起，简单降权未必正确。
3. **confidence BCE 目标和线上决策一致。** 当前目标是连续的 `accept_rate_3d`，而线上 gate 通常根据预测 confidence 决定是否继续或截断；两者之间需要校准，而不是只看 BCE 下降。

### 2.3 在线训练的额外变量

`online_mooncake` 路径把完整 token 序列发给 producer，读取 target hidden states 和 final hidden states，并验证 token IDs、shape、dtype 和 finite values；见 `deepspec/data/online_feature_dataset.py:35-44`、`:64-86`、`:137-255`。异步路径使用有界 `/dev/shm` slab、lease、release 和 backpressure，见 `deepspec/data/async_feature_cache.py:44-87`、`:157-180`。

因此必须记录并控制：

- target model / producer 服务版本；
- `online_vllm_layer_ids` 与训练使用的 `[40,41,42]` 的映射；
- response 生成策略、temperature、thinking/non-thinking 比例；
- sample 是否跨 epoch 重复读取同一 target feature；
- producer 延迟、跳过 batch 数、Mooncake cache 命中和 transfer bytes。

已有 Topic 已说明 hidden-state 在线提取不等于 response 在线生成：[Speculator 训练的数据生命周期与框架策略](speculator-training-data-lifecycle.md#4-在线特征提取的数据流)。本项目若要提高 acceptance，首先要保证 response 和 hidden-state 的 target 版本一致。

## 3. 实验原则与统一协议

### 3.1 固定项

除非实验明确改变该项，以下保持不变：

- target checkpoint、tokenizer、chat template；
- 40 万样本训练集、固定 held-out 验证集；
- global batch size 32、相同有效 optimizer steps；
- `block_size=5`、3 层 drafter、target feature `[40,41,42]`；
- optimizer、precision、NPU 数量和通信设置；
- 训练后使用同一推理 evaluator、同一 prompt 顺序、同一随机种子集合。

### 3.2 统一报告

每个实验至少报告：

| 类别 | 指标 |
|---|---|
| 训练 | total steps、tokens、wall-clock、最终/最佳 checkpoint、CE/L1/tau/confidence loss |
| 接受 | greedy length、probabilistic length、每位置接受率、first rejection 分布 |
| 质量 | target 分布一致性、GSM8K/Math/代码任务准确率或 pass rate；lossless 路线不应只报 acceptance |
| 系统 | drafter latency、target verify latency、producer latency、Mooncake transfer、端到端 tokens/s |
| 稳定性 | 3 个随机种子或至少 2 个复跑、训练曲线方差、NaN/skip batch、梯度范数 |

成功标准建议分两级：

- **算法成功**：greedy accepted length 相对 2.7 提高至少 `+0.2`，且质量不下降；
- **系统成功**：端到端 tokens/s 提高至少 `5%`，并且新增训练/推理开销不超过收益。

只提高 probabilistic length、但 greedy length 和 wall-clock 不变，不应标为成功。

## 4. 实验矩阵

### P0：指标、数据与在线一致性

| ID | 实验 | 改动 | 主要假设 | 为什么优先 | 支撑来源 | Go/No-go |
|---|---|---|---|---|---|---|
| P0-1 | 双接受长度基线 | 不改模型；同时记录 greedy/probabilistic、位置接受率、first rejection | 当前 2.7 可能混用了两种口径 | 仓库明确区分两种指标，默认 best checkpoint 还是 greedy 指标 | `loss.py:65-109`；`docs/configuration.md:216-241` | 若两者差距大于 0.3，后续先按 greedy 重新定 baseline |
| P0-2 | target 版本闭环 | 为每条数据记录 target hash、producer commit、tokenizer/chat template、layer schema | online feature stale 或 schema mismatch 会伪装成训练失败 | Mooncake 路径已验证 token/shape/dtype，但没有证明 target 版本被完整记录 | `online_feature_dataset.py:64-86`、`:201-223` | 发现混版则废弃该 run，不比较算法 |
| P0-3 | 在线 vs 固定 feature | 同一批 1--2 万样本先保存 feature，再用相同 seed 做 online/static 对照 | online transfer 或 producer 时序不应改变模型收敛 | 区分算法问题和 online pipeline 问题 | `base_trainer.py:761-803`；`async_feature_cache.py:157-180` | acceptance 差异超过 0.1 或 loss 曲线明显漂移，先修 pipeline |
| P0-4 | 难例分层 | 按 response 长度、thinking/non-thinking、first rejection 位置和 entropy 分桶 | 2.7 可能由数据构成决定，而不是模型容量 | DFlash/DSpark 研究都强调 accepted prefix 与位置条件；长 CoT 还需单独看 | [DFlash](../papers/dflash.md#5-关键结论与技术-claim-证据矩阵)；[DSpark](../papers/dspark.md#5-关键结论与技术主张证据矩阵) | 若某一桶低于 1.5，后续增加该桶采样比例 |

### P1：低风险训练目标与采样

| ID | 实验 | 推荐设置 | 目标 | 设计理由与来源 | 预期判读 |
|---|---|---|---|---|---|
| P1-1 | tau/L1/CE 权重 | 固定结构，测试 baseline、`L1:CE=0.7:0.3`、`0.5:0.5`；tau `0/0.02/0.05/0.1` | 判断分布拟合和 prefix 目标的平衡 | 当前 L1=0.9 可能压低 token CE；tau 直接使用前缀连乘，比单 token L1 更接近接受长度 | 若 tau 增大 greedy 不升而 probabilistic 升，说明目标错位 |
| P1-2 | 位置权重 | `gamma=None/2/4/8`；增加前两位加权 control | 找到首位与后位的最优权衡 | `loss_decay_gamma` 当前只按位置衰减；DRelay 说明早期位置对连续 prefix 边际价值更高 | 首位提升优先于后位平均 loss 下降 |
| P1-3 | confidence 校准 | 只训练 confidence head：BCE vs Brier/Huber；报告 ECE、Brier、prefix calibration | 让 gate 的决策概率可信 | 当前 confidence target 是连续 `accept_rate_3d`，线上却使用 threshold；代码见 `loss.py:256-298` 和 `draft_ops.py:97-131` | 同等 acceptance 下减少无效 stage/verify 才算收益 |
| P1-4 | Markov 头容量 | vanilla rank `128/256/512`；再测 gated head | 判断块内 token 依赖是否是瓶颈 | 当前 vanilla head 只把前 token embedding 投影成 vocab bias；`markov_head.py:8-90`；gated 头提供 hidden-conditioned gate | rank 增长若只提升训练 loss、不提升后位 acceptance，停止扩容 |
| P1-5 | RNN/半自回归头 | 只作为对照，不作为首选 | 测试显式块内递归状态的上限 | RNN head 已有实现，但训练 teacher-forced、推理逐步采样，存在 exposure bias；`markov_head.py` 的 RNN 实现 | 若 acceptance 提升但 draft latency 超过 5%，不进入生产 |
| P1-6 | anchor 采样 | uniform 对照；按 first-rejection/entropy/位置重要性重采样 | 让训练集中在真正影响 prefix 的 anchor | 当前 `sample_anchor_positions` 对有效位置随机排序；`common.py:194-258` | 先只改采样概率，不改 loss，便于归因 |

### P2：直接吸收 DFlash/DSpark 后续路线

| ID | 实验 | 实现范围 | 目标假设 | 参考来源 | 成功标准与风险 |
|---|---|---|---|---|---|
| P2-1 | rejected-suffix state reuse | 在验证数据生产端保存首个拒绝后的 target hidden states；训练一个小 residual/gate 注入下一 block | ReTrace/ReAnchor 表明拒绝后状态仍包含可复用轨迹信息 | [ReTrace](https://arxiv.org/abs/2608.29748)；10 月谱系中的 ReAnchor；Survey 的 rejected-trajectory 小节 | 先做 training-only offline replay；若 feature/transfer 成本超过 5%，不接 online 主链 |
| P2-2 | DCOCO/全局候选修复 | 每个 block 保留 top-k candidate，增加轻量相邻位置 compatibility selector | DFlash 的 per-position marginal 组合不一致，是后位 rejection 来源之一 | 10 月候选 DCOCO，及 [DRelay](../papers/drelay.md) 的 global reader + repair loss | 需要同时报告 selector latency、显存和 candidate coverage；没有正确候选时不能修复 |
| P2-3 | DSpark confidence scheduler | 复用 confidence head 做动态 block/stage 预算；保持 target verifier 不变 | 固定 block=5 对不同样本不适配；confidence 可决定是否继续便宜 drafting | [DSpark](../papers/dspark.md)；[LibraSpec](../papers/libraspec.md) | 若平均 acceptance 提升但 target call 未降，说明 gate 只改善指标未改善系统 |
| P2-4 | block size sweep | `3/5/7`，只改推理和训练形状，重新训练 | 2.7 可能受 block 长度与接受概率乘积限制 | DFlash/HyperDFlash 证明更长 block 不一定更快；[HyperDFlash](../papers/hyperdflash.md#8-infra-需求分析) | 以 speedup Pareto 选点，不按 accepted length 单指标选 7 |
| P2-5 | looped drafting | 在当前 5-token block 上累积 2 个 stage 后一次验证 | 减少全接受轮的 target verification | [DLoop](../papers/dloop.md)、[D-Loop](../papers/d-loop.md) | 这是 serving/状态机改动，放在 P2 后半；需先证明线上 graph/cache 可承载 |

### P3：数据与在线训练策略

| ID | 实验 | 做法 | 为什么值得做 | 主要风险 |
|---|---|---|---|---|
| P3-1 | on-policy response 重生成 | 固定 40 万 prompt，比较旧 response、当前 target 重生成 response、混合 1:1 | drafter 目标必须和实际 target 输出分布一致；Topic 已区分 response 与 hidden-state 生命周期 | 生成成本高；必须锁 target/sampling 版本 |
| P3-2 | rejection-focused replay | 用当前 checkpoint 在训练集上跑 verifier，过采样首个拒绝位置前后窗口 | 直接增加模型最缺的错误边界样本 | 可能过拟合某个 checkpoint 或任务桶 |
| P3-3 | length/entropy curriculum | 前期短样本和低 entropy，后期加入长 thinking、高 entropy、代码样本 | 先学稳定首位，再学长尾后缀 | curriculum 顺序可能只改变收敛速度，需等 step 对齐比较 |
| P3-4 | online freshness window | 当前 target snapshot 每 N 个 step 更新 producer；限制 feature 最大年龄 | 避免在线 producer 与训练 target/response 版本错位 | producer reload 和 cache invalidation 会增加系统停顿 |
| P3-5 | asynchronous pipeline ablation | sync、async、不同 `window/concurrency/slots` | 区分算法收益和 transfer/backpressure 造成的训练噪声 | async 只改变吞吐时不能宣称提高 acceptance |

## 5. 推荐执行顺序

### 第一阶段：一周内完成的诊断

1. 固定 40 万数据、GBS 32、实际 epoch 和有效 step，重跑 baseline。
2. 输出 greedy/probabilistic 双接受长度、position acceptance、first rejection 和 confidence calibration。
3. 做 online/static feature 对照，确认 target 版本和 feature schema 没有混用。
4. 对数据按 thinking、长度、entropy 和 first rejection 分桶。

### 第二阶段：低风险收益搜索

1. 先做 P1-1（loss 权重）和 P1-2（位置权重）的低成本矩阵。
2. 再做 P1-3（confidence calibration）和 P1-6（anchor sampling）。
3. 只有当这些实验不能把 greedy length 推到约 `2.9` 以上，才做 Markov/gated/RNN 结构比较。

### 第三阶段：结构增量

推荐顺序是：

1. DSpark confidence scheduler / dynamic block；
2. rejected-suffix state reuse；
3. DCOCO/DRelay 风格候选修复；
4. DLoop looped drafting。

原因是前两项可以保持现有 target verifier 和 5-token block 合同，后两项会增加 candidate storage、selector 或 serving 状态机复杂度。DLoop 的论文证据显示减少 target verification 可能带来更好的 wall-clock，但它不能直接替代 drafter 训练优化。

## 6. 需要避免的错误结论

- 不能把 probabilistic `accept_length` 的提升直接写成线上 greedy accepted tokens 提升。
- 不能只看 accepted length；DFlash、HyperDFlash 和 DPara 都说明 draft cost、verify cost、padding、graph bucket 与缓存传输会改变真实 speedup。
- 不能把 confidence BCE 下降当成 confidence scheduler 有效；必须看 calibration、target calls 和端到端延迟。
- 不能把 online producer 的吞吐提升当成模型算法提升；应拆分 producer、Mooncake、训练前向和 verifier latency。
- 不能把 10 月论文的 baseline 比较当成已经继承 DFlash/DSpark；直接继承关系已在 [2026-10 谱系清单](../evidence/2026-10-dflash-lineage-scan.md)中区分。

## 7. 当前建议的首批最小矩阵

如果算力只能支持 8--12 个 run，优先执行以下组合：

| Run | 配置 | 目的 |
|---|---|---|
| B0 | 当前 baseline，完整双指标 | 锁定 2.7 口径 |
| B1 | L1/CE `0.7/0.3`，tau `0.05` | 减少过度分布拟合 |
| B2 | L1/CE `0.5/0.5`，tau `0.1` | 强化 prefix 目标 |
| B3 | gamma `2` | 强化前两位 |
| B4 | gamma `8` | 保留后位监督 |
| B5 | gated Markov rank 256 | 测试 hidden-conditioned block dependency |
| B6 | vanilla rank 512 | 测试容量上限 |
| B7 | rejection-focused anchor sampling | 测试难例覆盖 |
| B8 | confidence calibration loss | 测试 gate 可靠性 |
| B9 | fixed feature vs online feature | 排除 pipeline confounder |
| B10 | block size 3 | 接受率/成本 Pareto |
| B11 | block size 7 | 接受率/成本 Pareto |

每个 run 先以相同训练 token 数比较；如果 B1--B8 中任何一个达到 greedy `+0.2` 且 wall-clock 不恶化，再把该方向与 P2-1 rejected-state reuse 组合。不要同时改变 loss、block size、Markov 结构和数据分布，否则无法判断收益来源。

## 8. 证据边界与未审计状态

- DeepSpec-npu 的代码事实来自 GitCode `online_train` 分支提交 `2b730e8c7142f7f516c4c5a4b476f765e95de1`；代码仓库不是本知识库的 canonical Paper。
- 当前 2.7、40 万样本、GBS 32、3 个以上 epoch 来自项目方提供的实际运行口径；仓库默认脚本参数已明确排除为本 baseline。
- DFlash、DSpark、DeLS-Spec、DPara、DLoop、D-Loop、DRelay、LibraSpec 等算法依据链接到已有 canonical Paper；ReTrace、ReAnchor、DCOCO、TreeSpark 等 10 月候选只用于方向识别，不在本文展开其论文分析。
- 本文是规划交付：**review validation、publisher validation、promotion-plan validation 和正式资产 Git-tracked 审计按用户要求暂未执行**。因此本文不应被表述为已通过发布门禁的最终验收件。
