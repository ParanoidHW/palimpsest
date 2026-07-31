# 并行切分（Parallel Partitioning）

本领域研究如何把模型、数据、状态与执行过程映射到多设备系统。核心问题不是记住 DP、TP、EP、PP、SP、CP 或 CFGP 的缩写，而是持续回答四个问题：

1. 切分对象是什么；
2. 每个 rank 实际持有什么；
3. 为恢复全局语义需要什么通信；
4. 在目标 workload 与硬件拓扑下，这个切分是否值得。

当前处于领域建设规划阶段。首版规划已经确定统一分析坐标、文档职责、视觉语言、跨域复用边界和后续实施顺序；基础 Topic、方法 Survey、Evidence 与新增 Paper 将在评审规划后逐步建立。

## 阅读路径

1. [并行切分知识领域规划](surveys/parallel-partitioning-domain-plan.md)：先看领域边界、统一分析框架、计划文档树、呈现方式和实施顺序。
2. 后续从 `tensor-and-state-coordinate-system` 建立 $B/S/H/D/E/L/G$ 坐标，再进入 DP/TP/EP/PP 与 attention SP/CP。
3. 需要做系统选型时，进入计划中的 `parallel-strategy-selection`，按 Dense LLM、MoE、长上下文、图像/视频生成和在线 serving 查找。
4. 遇到不能沿规则 tensor axis 均分的工作负载时，进入计划中的 `irregular-and-workload-aware-partitioning`。

## 文档索引

- Survey：[并行切分知识领域规划](surveys/parallel-partitioning-domain-plan.md)
- Topic：待规划评审后创建
- Paper：当前不新建；优先跨域复用已有 canonical Paper
- Evidence：待后续检索、选篇和 adoption 核验时创建

## 领域边界

本领域纳入：

- 数据、请求、参数、activation、expert、layer、token/context、graph branch 与训练状态的切分；
- collective、P2P、layout transform、同步、pipeline bubble、负载不均和通信重叠；
- 训练与推理的并行组合，以及 topology-aware device mesh；
- 架构语义、稀疏 workload、算子代数结构或执行调度驱动的定制切分。

本领域不重复拥有具体模型或论文。DeepSeek-V4、Kimi K3、SwiftFusion、Cosmos 3、MAGI-1、Causal-rCM、DSV、LVSA 等分析继续由原领域拥有；本领域只建立并行视角的跨域链接和综合判断。

## 资产说明

- `assets/surveys/parallel-partitioning-domain-plan/`：领域规划 Survey 自有的生成图或整理图。
- 后续引用的原论文 Figure/Table 仍归对应 canonical Paper，不在本领域复制。
- 生成图只用于解释与导航，不能代替论文机制或实验依据。
