---
tags:
  - topic
  - collection/parallel-partitioning
  - domain/ai-infra
  - topic/device-mesh
document_type: topic
domain: parallelism
canonical: true
---

# 多轴组合与设备网格

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 坐标系：[并行切分坐标系](parallel-coordinate-system.md)
> - 成本模型：[通信原语与成本模型](communication-primitives-and-cost-model.md)
> - 选型指南：[并行策略选型](../surveys/parallel-strategy-selection.md)

混合并行不是把若干 degree 相乘就结束。每个轴都会改变 tensor layout、communicator、buffer lifetime 和 kernel shape；组合的难点是减少轴与轴之间的 redistribution 和网络争用。

## 1. Device mesh

例如 64 GPUs 可以组织为：

\[
8_{\mathrm{DP}}\times 4_{\mathrm{TP}}\times 2_{\mathrm{PP}}.
\]

这只是逻辑 shape。物理 placement 还需决定：

- 4-way TP 是否位于同一 NVLink island；
- PP 邻接 stages 是否跨节点；
- DP all-reduce 是否使用独立 NIC rail；
- rank ordering 是否让 logical neighbors 对应真实高速链路。

## 2. 推荐的约束驱动组合顺序

1. 模型可单卡且 batch 可扩：DP。
2. DP state OOM：ZeRO/FSDP。
3. 单层或 GEMM OOM：TP。
4. 总层数/activation OOM：PP。
5. MoE expert 容量：EP。
6. sequence/attention OOM：SP/CP。
7. 最后搜索 degree、micro-batches、bucket 和 topology placement。

这个顺序不是绝对算法，而是减少搜索空间。每加一个轴，都应重新测量 peak memory、critical-path communication 和 min-rank/max-rank work。

## 3. 组合冲突

| 冲突 | 原因 | 诊断 |
|---|---|---|
| TP × Ulysses | 两者都可能切 head/hidden | 记录 attention 前后 exact placement |
| EP × Ulysses | 两者都使用 all-to-all | 检查 fabric contention 与 communicator overlap |
| PP × ZeRO-3 | stage compute 前参数 gather | 看 prefetch 是否进入 bubble/critical path |
| CP × causal mask | sequence shard 工作量不均 | 比较 max-rank compute，不只平均 FLOPs |
| DP × 大 global batch | 系统可扩但优化语义变化 | 监控 sample efficiency 和收敛 |
| CFGP × cache | 分支切分可能复制 KV/参数 | 明确 combine 和 cache owner |

## 4. Layout contract

每个 stage/operator 应声明：

```text
input placements
local computation
output placements
required redistribution
temporary buffers
backward/inference inverse
```

如果相邻两个 operator 的 placement 不一致，compiler/runtime 必须插入 reshard。定制优化通常来自：

- 改变某个 projection 的切分，使输出直接匹配下游；
- 把 concat/sum 放到更小 tensor 的一侧；
- 合并连续 collective；
- 延迟 gather，保持 shard 穿过更多 elementwise operators；
- 根据 topology 把一个全局 collective 分层。

## 5. 自动化的边界

[GShard](../papers/gshard.md#45-自动-sharding-的准确边界)展示的是 annotation propagation + SPMD lowering，而不是无约束搜索。现代 DTensor/device mesh 进一步把 placement 变成框架 API，但完整自动化仍需准确预测：

- kernel efficiency 随 local shape 的变化；
- collective contention；
- buffer peak 和 fragmentation；
- dynamic/uneven shard；
- sparse/causal workload；
- retry、checkpoint 和 fault domain。

因此 cost model 的可信度往往比搜索算法本身更关键。

## 6. 实践记录表

| Mesh axis | Degree | Physical scope | Tensor/state placement | Collective | Peak buffer | Overlap target |
|---|---:|---|---|---|---|---|
| DP |  |  |  |  |  |  |
| TP |  |  |  |  |  |  |
| PP |  |  |  |  |  |  |
| EP |  |  |  |  |  |  |
| CP/SP |  |  |  |  |  |  |

只有这张表与 profile 对得上，混合并行配置才算被解释，而不是只被跑通。
