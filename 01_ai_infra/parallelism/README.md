# 并行切分（Parallel Partitioning）

本领域研究如何把模型、数据、状态与执行过程映射到多设备系统。核心问题不是记住 DP、TP、EP、PP、SP、CP 或 CFGP 的缩写，而是持续回答四个问题：

1. 切分对象是什么；
2. 每个 rank 实际持有什么；
3. 为恢复全局语义需要什么通信；
4. 在目标 workload 与硬件拓扑下，这个切分是否值得。

当前版本已完成统一坐标、成本模型、方法体系、选型指南、不规则切分、六篇 canonical Paper、Figure inventory 和跨域采用索引；方法体系另提供 11 张由 TikZ 排版的高分辨率 PNG，其中普通 DP 与 ZeRO-1/2/3 分别使用独立 workflow 显式展示 forward、backward、optimizer、dtype、state ownership 和 collective dataflow，其余图统一展示 rank-local layout、恢复语义、通信、状态/激活内存、计算量与推理差异。后续以增量补充 pipeline schedule 实现演进、自动切分编译器和 serving 并行为主。

## 阅读路径

1. [并行切分方法体系](surveys/parallel-partitioning-taxonomy.md)：DP/ZeRO/TP/PP/EP/SP/CP 的统一总览。
2. [并行切分坐标系](topics/parallel-coordinate-system.md)：切分对象、placement 与 device mesh。
3. [通信原语与成本模型](topics/communication-primitives-and-cost-model.md)：collective、bubble、overlap、topology 与 peak buffer。
4. [并行策略选型](surveys/parallel-strategy-selection.md)：按 Dense LLM、MoE、长上下文、视频生成和 serving 选择。
5. [不规则与 workload-aware 切分](surveys/irregular-and-workload-aware-partitioning.md)：`o_proj`、CFGP、稀疏/causal CP 和 stateful CP。
6. [并行切分知识领域规划](surveys/parallel-partitioning-domain-plan.md)：领域组织、视觉语言和建设边界。

## 文档索引

### Surveys

- [并行切分方法体系](surveys/parallel-partitioning-taxonomy.md)
- [并行策略选型](surveys/parallel-strategy-selection.md)
- [不规则与 workload-aware 切分](surveys/irregular-and-workload-aware-partitioning.md)
- [并行切分知识领域规划](surveys/parallel-partitioning-domain-plan.md)

### Topics

- [并行切分坐标系](topics/parallel-coordinate-system.md)
- [通信原语与成本模型](topics/communication-primitives-and-cost-model.md)
- [序列与上下文并行](topics/sequence-and-context-parallelism.md)
- [多轴组合与设备网格](topics/composition-and-device-mesh.md)

### Papers

- [Megatron-LM](papers/megatron-lm.md)：tensor parallel
- [GPipe](papers/gpipe.md)：pipeline parallel
- [ZeRO](papers/zero.md)：data-parallel state sharding
- [GShard](papers/gshard.md)：expert parallel 与 sharding annotation
- [DeepSpeed Ulysses](papers/deepspeed-ulysses.md)：all-to-all sequence parallel
- [Ring Attention](papers/ring-attention.md)：ring sequence/context parallel

### Evidence

- [选篇与影响力证据](evidence/parallel-partitioning-selection.md)
- [方法与系统索引](evidence/parallel-partitioning-method-system-index.md)
- [跨领域采用](evidence/parallel-partitioning-cross-domain-adoption.md)
- [主张—证据矩阵](evidence/parallel-partitioning-claim-matrix.md)
- [Figure inventory](evidence/figure-inventory.md)

## 领域边界

本领域纳入：

- 数据、请求、参数、activation、expert、layer、token/context、graph branch 与训练状态的切分；
- collective、P2P、layout transform、同步、pipeline bubble、负载不均和通信重叠；
- 训练与推理的并行组合，以及 topology-aware device mesh；
- 架构语义、稀疏 workload、算子代数结构或执行调度驱动的定制切分。

本领域不重复拥有具体模型或论文。DeepSeek-V4、Kimi K3、SwiftFusion、Cosmos 3、MAGI-1、Causal-rCM、DSV、LVSA 等分析继续由原领域拥有；本领域只建立并行视角的跨域链接和综合判断。

## 资产说明

- `assets/surveys/parallel-partitioning-taxonomy/`：方法体系 Survey 独占的 11 张 `2400×1350` TikZ 排版 PNG 教学整理图，覆盖普通 DP、ZeRO-1/2/3、TP、PP、EP、Megatron SP、Ulysses、Ring/CP 与 CFGP；这些图是 analysis-derived 解释资产，不是原论文证据。
- `assets/surveys/parallel-partitioning-domain-plan/`：领域规划 Survey 的生成图。
- `assets/topics/parallel-coordinate-system/`：`$imagegen` 生成并经人工纠错的坐标系教学图。
- `assets/papers/<slug>/`：六篇 canonical Paper 的 QA-passed 原论文 Figure/Table。
- 跨域 Paper 资产仍归原领域 owner，本领域只链接。
- 生成图只用于解释与导航，不能代替论文机制或实验依据。
