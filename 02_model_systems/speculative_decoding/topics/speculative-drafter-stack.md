# 投机草稿模型：从训推对齐到在线训练的技术思考

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[Evolution](../surveys/evolution.md)
> - 相关文档：[DeepSpec online_train 后续算法与实验规划](deepspec-online-train-followup-planning.md)
> - 全景补充件：[技术栈与思考全景 HTML](../supplements/speculative-drafter-stack.html)

## 1. 先把问题说清楚

投机推理的基本分工很简单：较小的草稿模型先提出一段候选 token，较大的目标模型再一次性检查并接受其中的正确前缀。真正困难的地方不在“能不能训练一个小模型”，而在于 **训练时优化的接受率，能否在真实推理框架中兑现为更少的目标模型调用和更高的 tokens/s**。

因此，这个主题应当被看作一条闭环，而不是一张组件清单：

```text
目标模型与输入协议
  -> 训练特征与监督轨迹
  -> 草稿模型训练目标
  -> 候选生成与验证调度
  -> 推理框架中的缓存/通信/批处理
  -> 真实接受长度与端到端时延
  -> 反哺数据、损失和结构选择
```

如果链条中任何一环不一致，单点指标都会误导。例如 teacher-forcing（训练时把真实前缀喂给模型）通常比真实 rollout（模型自己采样前缀）容易；若只看前者，接受长度可能虚高。类似地，离线 feature 与线上 target 版本、聊天模板或采样温度不一致时，loss 下降也不能说明算法有效。

## 2. 术语与指标

| 术语 | 本文含义 | 不应混淆 |
| --- | --- | --- |
| 目标模型（target） | 最终决定输出、负责验证候选的大模型 | 草稿模型；二者权重和算力职责不同 |
| 草稿模型（drafter） | 低成本提出候选 token 的模型或头 | 只会降低候选生成成本，不自动提高最终质量 |
| 接受长度 | 一轮验证中目标模型连续接受的 token 数 | 单 token 接受率、概率长度、线上吞吐 |
| 真实 rollout | 草稿模型按推理配置逐步生成候选，再交给目标模型验证 | teacher-forcing 或只用数据集真值的评估 |
| feature | 目标模型产生并供草稿训练使用的 hidden state、logit 等中间量 | 训练文本本身；feature 必须带版本和形状信息 |
| regen | 用目标模型重新生成训练 response | 不能把 regen 的收益与数据来源、温度变化混为一谈 |
| prefix | 当前已经确定的上下文，包括被接受的候选 | 不是“数据集中的正确前缀”的同义词 |

## 3. 第一门槛：训推一致性

### 3.1 对齐的不是数据集，而是目标模型的行为

草稿模型要逼近的是目标模型在具体推理协议下的分布。协议至少包括：模型前向实现、权重转换、tokenizer 与 chat template、BOS/EOS 处理、采样温度、top-k/top-p、停止条件、批处理形状，以及拒绝后如何更新 prefix 和 KV cache。只要其中一项不同，草稿看到的 hidden state 就不再是线上会看到的状态。

建议把“对齐”拆成三个可验收层级：

1. **数值对齐**：同一输入、同一权重和同一 dtype 下，训练侧与推理侧的关键 hidden state、logit 做逐点比较；目标是先达到项目约定的余弦相似度门槛（当前讨论以 `>0.999` 为起点），同时报告最大相对误差，而不是只报一个平均值。
2. **语义对齐**：两侧使用同一 tokenizer、chat template、采样和停止规则。不同业务场景若确实需要不同协议，应先判断能否通过显式条件输入或少量校准覆盖；直接为每种 harness（推理驱动程序）训练一套模型会迅速失去维护性。
3. **轨迹对齐**：训练验证阶段必须使用 sampled-prefix。也就是说，草稿已经生成的 token 被接受或拒绝后，下一步状态要按线上规则更新；不能持续喂数据集真值，否则会掩盖草稿自身造成的状态偏移。

### 3.2 可证伪的对齐检查

每次实验都应保存 `target hash`、producer commit、tokenizer/chat template、layer schema、dtype 和随机种子。对同一 prompt 同时记录：teacher-forced 概率长度、greedy 长度、真实 rollout 接受长度、首个拒绝位置及最终 logits。若离线与线上接受长度差异超过约 `0.3`，先修评估口径或 prefix 覆盖，再讨论模型结构。

这一步的因果逻辑是：只有输入、目标前向和轨迹都相同，接受长度的变化才可能归因于草稿训练；否则“算法收益”与 pipeline 错位无法区分。

## 4. 技术栈的六层结构

### 4.1 模型与算子层：先保证可运行，再谈结构创新

当前可选结构包括 DFlash、DSpark、DPara、DLite，以及带 hidden-conditioned gate 的 Markov 头、RNN/半自回归头等。它们分别改变块内条件化、候选并行度、验证窗口或头部容量。选择顺序应是：固定一个能在目标框架运行的 baseline，验证前向和权重转换；只改变一个结构变量；同时测接受长度、草稿耗时、目标调用次数、显存和端到端 tokens/s；只有真实 rollout 中成立的结构收益才进入异步传输和动态验证优化。

“容量更大”不等于“系统更快”：一个更复杂的草稿头若增加 5% 草稿延迟，却只增加很少的接受 token，整体收益可能为负。

### 4.2 训练数据与监督轨迹层

数据来源至少分为 ground-truth response、target regen response 和混合数据。regen 可以让监督更贴近目标模型，但代价是额外目标模型生成；不能用一次混合实验同时推断“数据来源、温度和长度覆盖”的主效应。

建议先核对约 40 万样本的来源比例，检查 chat template 与本地 `input_ids` 的首个差异位置，再按 response 长度、thinking/non-thinking、entropy 和 first rejection 分桶。只有入口一致，才比较长序列覆盖或更昂贵的 regen。

更进一步的方向是 draft-induced supervision：让草稿自己生成 proposal，在其诱导的状态或首个拒绝位置请求目标监督。这比普通 teacher-forcing 更接近线上问题，但会增加 feature 生成与缓存成本，应作为独立实验。

### 4.3 损失与决策层

训练目标至少有三种不同含义：token 分布拟合、连续 prefix 的接受倾向、以及 confidence head 对“是否值得继续 drafting”的校准。可先固定结构比较 L1/CE 权重和 prefix 权重，再独立评估 confidence 的 BCE、Brier 或 Huber 损失，并报告 ECE/Brier、target calls 和端到端延迟。

若 confidence loss 下降但 target calls 不降，说明模型学会了一个数值目标，却没有改善调度决策。若 probabilistic acceptance 上升而 greedy acceptance 不变，则应怀疑温度或评估口径。

### 4.4 Feature 生产与传输层

目标模型的 hidden-state feature 可以离线落盘，也可以由 producer 在线生成。存储量大致随 `层数 × batch × 序列长度 × hidden size × dtype 字节数` 线性增长，因此不能默认“全部缓存”是最优方案。

工程上可采用共享存储或 Mooncake 等 feature 服务，训练侧异步申请并与训练 step 重叠。TCP 更灵活但 CPU 拷贝和带宽压力更明显；RDMA 降低传输开销，却不能修复版本错配。重点指标是 host wait、H2D、缓存命中、feature 年龄、backpressure，以及这些因素是否改变模型更新顺序。

必须做 online feature 与 fixed feature 的同 seed 对照。若两者 loss 或 acceptance 曲线漂移，先查 target 版本、schema、lease、缓存失效和 producer 时序，再归因于算法。

### 4.5 推理验证与调度层

验证策略可以从固定 block、动态 block、树状验证扩展到 looped drafting（多轮 drafting 后合并一次验证）和候选修复。每个方向都要回答：减少了多少目标模型调用，新增了多少草稿计算、候选存储、KV cache 操作和调度复杂度？

动态 verify 只有在 confidence 校准可靠时才值得启用；DLoop/D-Loop 属于 serving 状态机改造，不能当作单纯训练技巧。验证器仍需保持 lossless contract，任何“近似接受”都必须单独标注为有界例外并报告质量风险。

### 4.6 框架与交付层

目标是让同一套草稿模型能在 DeepInfer、Recipes-Infer、vLLM/vLLM-Ascend、SGLang 等推理栈中运行，并与 DeepSpec、TorchSpec、Speculators 等训练栈衔接。交付物应包括模型代码、权重转换工具、训推 parity skill、feature producer/consumer 接口、Mooncake 接入、评测 harness 和最小复现实验脚本。

框架适配不能只停留在“模型能加载”。至少要验证前向结果、权重命名、batch padding、TP/EP 通信、异步 feature 生命周期、拒绝后状态更新和 checkpoint round-trip。模型支持矩阵应按目标模型版本、草稿结构、训练框架、推理框架和 dtype 展开。

## 5. 训练、prefill 与 decode 的边界

- **训练**：关注 forward/backward 的 sampled-prefix、梯度累积、feature 生产时序、optimizer 状态和异步缓存是否可复现。训练吞吐提升不能直接写成接受率提升。
- **Prefill**：整段 prompt 进入目标模型并建立 KV cache；需要检查 batch 形状、模板、prefix 截断和 feature 生成位置。prefill 的一次性吞吐不能替代 decode 的逐步时延。
- **Decode**：通常每轮只有一个或少量 token，需要读取并追加 KV cache，配合动态 batching 和频繁验证。真正的系统指标是端到端延迟、target calls、草稿耗时、padding、缓存传输和 tokens/s。

## 6. 实验决策树：先排除错因，再扩大搜索

### P0：不通过就不比较算法

1. 重跑固定 baseline，锁定数据量、有效 step、GBS 和双指标。
2. 补齐 hidden state、最终 logits、checkpoint round-trip、边界 shape 和 DeepSpec/vLLM parity。
3. 做 teacher-forced、greedy、真实 rollout 三种接受长度对照。
4. 做 online/static feature 对照，并记录版本与 schema。
5. 按长度、entropy、thinking 和首个拒绝位置分桶。

### P1：低风险搜索

依次尝试 L1/CE 与 prefix 权重、前两位位置加权、confidence 校准、anchor 重采样、温度和 block size。每次只改一个变量，指标同时包含 greedy acceptance、target calls、draft/verify latency 和 wall-clock。

### P2：轨迹、结构与调度

当 P0/P1 不能解释 baseline 或不能将 greedy 接受长度提高约 `0.2` 时，再尝试 draft-induced supervision、rejected-suffix state reuse、DSpark confidence scheduler、DCOCO/DRelay 风格候选修复和 DLoop looped drafting。推荐先做保持 verifier 合同不变的训练方向，再做 serving 状态机改造。

### P3：数据与在线系统

最后比较 ground-truth/target regen、长序列覆盖、同步/异步传输、freshness window、rejection-focused replay 和 curriculum。P3 的收益必须拆成模型指标、producer 吞吐、训练等待和线上时延，不能把缓存吞吐当成模型进步。

## 7. 当前最小可行矩阵

| 批次 | 实验 | 目的 | 通过条件 |
| --- | --- | --- | --- |
| B0 | 当前 baseline，完整双指标 | 锁定口径 | 结果可复现，版本闭环完整 |
| B9 | fixed feature vs online feature | 排除 pipeline 混淆 | loss/acceptance 无显著漂移 |
| B12 | 离线 vs 真实 rollout | 量化评估偏差 | 差异可解释且被记录 |
| B15 | chat template/token parity | 排除入口错位 | 首个差异位置符合预期 |
| B1-B4 | L1/CE、prefix、位置权重 | 搜索训练目标 | greedy 与 wall-clock 同向改善 |
| B5-B8 | Markov/gated 容量、anchor、confidence | 搜索结构和决策 | acceptance 提升且 target calls 不恶化 |
| B10-B11 | block size 3/7 | 找 Pareto 点 | 不按 accepted length 单指标选型 |
| B13-B14 | regen 与长序列 | 判断数据主效应 | 生成成本和收益可比较 |
| B16 | Draft-OPD offline replay | 验证 draft-induced supervision | 真实 rollout 改善且不破坏 lossless target |

## 8. 尚未闭合的论证链

以下问题应明确留作讨论，而不是用结论填空：

1. `>0.999` 的前向余弦相似度是否足以预测接受长度？需要结合最终 logits、相对误差和首个拒绝位置建立经验边界。
2. 不同采样场景是否能通过条件化一个草稿模型覆盖，还是必须维护多个专用模型？需要按场景差异和校准成本实验。
3. regen 的收益来自目标分布更接近、温度变化，还是 response 长度变化？需要固定另外两项做因子实验。
4. 在线 feature 的新鲜度、缓存传输和训练随机性如何共同影响收敛？需要记录 feature age 与 step-level host wait。
5. acceptance 提升在何种 draft/verify 成本比下才转化为端到端收益？需要以 Pareto 曲线而非单一 accepted length 做决策。

## 9. 证据边界与下一步

本文是基于现有 Topic、canonical speculative decoding 论文和项目训练规划的工程综合，不把约 `2.7` acceptance、约 `40 万`样本、GBS 32 或余弦相似度约 `0.999` 写成已完成、可外推的实验结论。它们是当前项目口径，必须在 P0 中复核。DFlash、DSpark、DPara、DLoop、D-Loop、DRelay、LibraSpec 等算法细节应回到对应 Paper；本文只使用它们来组织决策顺序。

建议下一轮先补齐 B0/B9/B12/B15，并把每次运行的配置、source commit、feature 版本、评估轨迹和 wall-clock 放入同一实验记录。只有当这四项闭环后，才值得讨论是否扩大结构、数据或 serving 状态机。
