---
tags:
  - evidence
  - collection/parallel-partitioning
  - domain/ai-infra
document_type: evidence
domain: parallelism
canonical: true
---

# 跨领域采用与定制切分索引

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 上位 Survey：[不规则与 workload-aware 切分](../surveys/irregular-and-workload-aware-partitioning.md)
> - 所有链接指向原领域 canonical Paper；本 Evidence 不复制其资产。

| Canonical owner | 并行采用/定制点 | 本领域解读 |
|---|---|---|
| [DeepSeek-V4](../../../02_model_systems/llm_foundations/papers/deepseek-v4.md) | grouped output projection、wave EP、确定性边界 | operator-specific shard 与 EP 调度 |
| [Kimi K3](../../../02_model_systems/llm_foundations/papers/kimi-k3.md) | KDA CP、PP/VP/EP | stateful CP 与非交换状态组合 |
| [SwiftFusion](../../../02_model_systems/multimodal_generation/papers/swiftfusion.md) | Ulysses、Ring、Torus、topology-aware scheduling | 逻辑切分与物理拓扑联合 |
| [Cosmos 3](../../../02_model_systems/multimodal_generation/papers/cosmos-3.md) | Ulysses、HSDP、CFGP、cache/compile | 视频生成多轴组合 |
| [Causal-rCM](../../../02_model_systems/multimodal_generation/papers/causal-rcm.md) | Ulysses layout、CP cache、custom mask | sequence layout 与 cache owner |
| [MAGI-1](../../../02_model_systems/multimodal_generation/papers/magi-1.md) | Ulysses、MagiAttention、长视频 runtime | heterogeneous mask workload dispatch |
| [DSV](../../kernel/custom_attn/papers/dsv.md) | hybrid sparse CP、workload balancing | 稀疏模式驱动的 head/sequence placement |
| [LVSA](../../kernel/custom_attn/papers/lvsa.md) | Ulysses/ring/TP adoption | video sparse attention 与基础并行组合 |

## 1. 采用关系

这些记录不是八篇新 Paper 的计数，而是八个已有 canonical owners 的跨域 adoption 关系。任何图表继续归原 Paper owner。

## 2. 共同模式

### 移动 collective

`o_proj`、grouped projection 或 fused operator 通过改变输入/输出 placement，把 collective 从大 tensor 一侧移到小 tensor 一侧。

### 改变调度

wave EP、Torus/Ring overlap、denoising-step pipeline 主要改变执行时序和拓扑映射，不一定改变数学 shard axis。

### 动态负载

稀疏 attention、causal mask、模态 mask 和 CFG branches 会让相同 shard size 对应不同 compute。目标应从平均 workload 改为 max-rank critical path。

### 状态组合

KDA/recurrent CP 的 local state 需要有序组合；不能默认 all-reduce。

## 3. 后续核验

每条 adoption 后续应补：

- exact config/key/code path；
- upstream commit；
- native/optional/third-party 分类；
- target hardware/topology；
- measured benefit 与 matched baseline；
- 是否只是概念提及。
