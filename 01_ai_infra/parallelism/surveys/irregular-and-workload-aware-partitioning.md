---
tags:
  - survey
  - collection/parallel-partitioning
  - domain/ai-infra
  - topic/custom-sharding
document_type: survey
domain: parallelism
canonical: true
---

# 不规则与 workload-aware 切分

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 基础坐标：[并行切分坐标系](../topics/parallel-coordinate-system.md)
> - 方法总览：[并行切分方法体系](parallel-partitioning-taxonomy.md)
> - 跨域采用：[Evidence](../evidence/parallel-partitioning-cross-domain-adoption.md)

规则切分假设 tensor axis 可均匀分片、每个 shard 工作量相近、局部结果用固定 collective 合并。不规则切分则由 operator 代数、动态 sparsity、条件分支、mask 或拓扑驱动，目标通常是移动 collective、减少 redistribution 或均衡 max-rank work。

## 1. Operator-specific sharding

### `o_proj` / grouped projection

[DeepSeek-V4 grouped output projection](../../../02_model_systems/llm_foundations/papers/deepseek-v4.md#43-模型系统架构)展示了结构分解与设备切分的交叉：

- attention heads/group 先形成局部表示；
- output projection 的输入/输出 volume 不同；
- 选择 row/column/group shard 会把 collective 放在不同边界；
- 最优策略取决于下游 residual/layout，而不是单个 GEMM。

设计方法：

1. 写出 projection 前后 shape；
2. 标记哪一侧是 `Shard`、`Replicate` 或 `Partial`；
3. 比较在输入侧 gather、输出侧 reduce 或跨更多 elementwise op 延迟 gather；
4. 把 collective 放到 tensor 更小、可融合或可 overlap 的一侧。

## 2. CFG Parallel

Classifier-Free Guidance 同时执行 conditional/unconditional branches：

$$
\epsilon_{\mathrm{guided}}
=\epsilon_{\mathrm{uncond}}
+w(\epsilon_{\mathrm{cond}}-\epsilon_{\mathrm{uncond}}).
$$

CFGP 沿 branch 切分：

- rank/group A 计算 conditional；
- rank/group B 计算 unconditional；
- guidance combine 前交换输出或必要状态。

它适合两分支算力接近、combine tensor 明确、模型/缓存复制可接受的场景。主要开销：

- 两组参数/KV/cache 的驻留；
- 分支时长不均导致 idle；
- 每 denoising step 的交换；
- 与 batch/sequence parallel 的 communicator 冲突。

[Cosmos 3](../../../02_model_systems/multimodal_generation/papers/cosmos-3.md#8-infrastructure-分析)已有 Ulysses、HSDP、CFG parallel 与 cache/compile 的组合证据；本领域不复制其资产。

## 3. Sparse / causal workload

规则 `Shard(S)` 只均分 token 数，不保证均分有效 attention blocks。

### Causal

早期 Q blocks 只需少量历史 K，后期 Q blocks 需要更多 K，形成三角工作量。Ring 中即使跳过上三角 compute，通信 step 仍同步推进。

### Dynamic sparsity

视频 attention 的有效 KV 会随 layer、head、timestep 和输入变化。平均 sparsity 相同的两个 shards 也可能有完全不同的 block distribution。

[DSV](../../kernel/custom_attn/papers/dsv.md#4-研究方法)联合搜索 head-wise/sequence-wise CP、头分配和节点布局；评价目标应是：

$$
\min \max_r \left(T_{\mathrm{compute},r}+T_{\mathrm{comm},r}\right),
$$

而不是只最小化平均 FLOPs。

### Heterogeneous masks

[MAGI-1](../../../02_model_systems/multimodal_generation/papers/magi-1.md#6-magiattention-与-infrastructure)中的 MagiAttention根据 mask/workload dispatch，并按需组成 communication group。此类 runtime 需要 mask metadata、work queue 与动态 group management。

## 4. Topology-aware scheduling

[SwiftFusion](../../../02_model_systems/multimodal_generation/papers/swiftfusion.md#7-基础设施带宽与异构性)把 Ulysses、Ring/Torus 与节点内外拓扑结合，说明“更少字节”不等于“更少 exposed time”：

- 节点内适合细粒度 ring/TP；
- 跨节点适合粗粒度 all-to-all 或分层交换；
- collective 可拆成通信-计算可重叠阶段；
- rank placement 与调度时序同样属于切分设计。

## 5. Stateful / recurrent CP

[Kimi K3 KDA Context Parallelism](../../../02_model_systems/llm_foundations/papers/kimi-k3.md#61-flashkda-与-kcp)提示另一类边界：局部状态不是简单相加。需要记录：

- local transition；
- prefix state；
- state composition 是否结合；
- 顺序是否可交换；
- backward 如何传播。

若组合运算只满足结合律而不满足交换律，可以 tree-scan/prefix-scan；若连结合律也不满足，就需要更强的顺序约束。

## 6. 编译器/runtime 所需抽象

不规则切分至少需要：

- uneven shard；
- operator-specific sharding rule；
- `Partial` 与自定义 reduce semantics；
- dynamic shape/mask metadata；
- topology-aware cost；
- buffer lifetime；
- load-balance objective；
- correctness oracle。

GShard 的 annotation propagation 是基础，但动态 workload 还需要 runtime decision。

## 7. 证据要求

定制切分必须给出：

1. baseline 的具体失败场景；
2. global/local layout；
3. communication before/after；
4. max-rank workload；
5. memory peak；
6. matched ablation；
7. 不适用的 mask、shape、topology 或 branch；
8. correctness/equivalence test。

如果只展示 full-system speedup，应把收益标成组合证据，不单归因给某个 custom collective。
