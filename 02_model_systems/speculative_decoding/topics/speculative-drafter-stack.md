# 投机草稿模型：从训推对齐到在线训练的技术思考

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[Evolution](../surveys/evolution.md)
> - 相关文档：[DeepSpec online_train 后续算法与实验规划](deepspec-online-train-followup-planning.md)
> - 训练 Recipes：[现有工作：投机模型训练 Recipes](speculative-training-recipes.md)
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

“训推一致性”不是一个单一指标，而是多个层面分别对齐。每个层面都有自己的责任人、检查方法和失败表现；把它们混成一个 cosine 相似度，容易把输入问题误判成模型问题。

### 3.1 模型层：前向实现与权重转换

训练侧和推理侧首先要计算同一个目标模型。需要核对算子实现、归一化顺序、位置编码、并行切分、dtype，以及 checkpoint 到推理权重的命名和排列。对同一输入逐层比较 hidden state 和最终 logits，记录余弦相似度、最大相对误差和首个显著偏差位置；`>0.999` 只能作为当前项目的起始门槛，不能直接推导接受长度。

### 3.2 采样层：策略与 temperature

训练期间生成 proposal、离线评估和线上 decode 必须明确使用哪一种采样策略。temperature、top-k/top-p、随机种子、停止条件和 bonus token 规则只要有一项不同，草稿遇到的 token 分布就会改变。应分别记录 greedy、采样 rollout 和目标验证后的接受长度，不能把 probabilistic acceptance 当作线上 greedy 收益。

### 3.3 输入层：chat template、QA regen 与 hidden state 提取

输入形式决定模型看到的 prefix。需要对齐 tokenizer、BOS/EOS、system/user/assistant 标记、thinking 开关和 chat template，并逐条比较服务端与本地 `input_ids` 的首个差异位置。QA regen 应使用与线上相同的目标模型和模板；hidden state 提取还要对齐层号、截断位置、padding、dtype 和 feature schema。否则 feature 看似来自同一目标模型，实际上对应的是另一条上下文。

### 3.4 Infra 层：确定性计算与 batch 一致性

相同输入不一定产生相同结果。需要检查 deterministic kernel、通信归约顺序、TP/EP 分组、batch padding、动态 batching、长度桶和并发请求的调度方式。先用固定 batch 和单请求建立基线，再逐步加入真实并发；如果只在大 batch 下出现差异，应优先排查归约、padding 和调度，而不是修改 loss。

### 3.5 评估层：teacher-forcing 只是训练期验证口径

teacher-forcing 是把数据集中的真实前缀喂给模型，用来计算训练期间的验证 loss 或概率长度。它不是一种模型对齐维度，也不能代替推理实测：真实推理中 prefix 会由草稿模型生成，并经过接受或拒绝后继续前进。训练期间可以保留 teacher-forcing 观察收敛，但必须并行做 sampled-prefix 或真实 rollout 评估，至少报告 greedy 接受长度、首个拒绝位置、目标调用次数和端到端时延。否则训练曲线无法回答“这次更新是否真的改善线上候选”。

### 3.6 统一的对齐记录

每次实验保存 `target hash`、producer commit、tokenizer/chat template、采样配置、layer schema、dtype、batch 形状和随机种子。对同一 prompt 同时记录前向误差、模板差异、teacher-forcing 概率长度、greedy 长度、真实 rollout 接受长度、首个拒绝位置和最终 logits。若离线与线上接受长度差异超过约 `0.3`，先定位上述五个维度，再讨论模型结构。

因果关系是：模型层决定“算的是不是同一个模型”，采样层决定“走的是不是同一分布”，输入层决定“看的是不是同一 prefix”，infra 层决定“同一输入是否稳定复现”，评估层决定“训练曲线能不能预测线上表现”。只有这些层面分别闭环，接受长度变化才有资格归因于草稿训练。

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
