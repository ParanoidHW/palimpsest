---
tags:
  - survey
  - collection/parallel-partitioning
  - domain/ai-infra
  - topic/system-design
document_type: survey
domain: parallelism
canonical: true
---

# 并行策略选型：从瓶颈、工作负载与拓扑出发

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 方法体系：[并行切分方法体系](parallel-partitioning-taxonomy.md)
> - 成本模型：[通信原语与成本模型](../topics/communication-primitives-and-cost-model.md)
> - 设备网格：[多轴组合与设备网格](../topics/composition-and-device-mesh.md)

选型不要从“行业通常用什么”开始，而要从单卡/当前集群的首要约束开始。每次只引入能直接切掉该约束的轴，再用 profile 验证它是否把瓶颈转移到了可接受的位置。

## 1. 决策表

| 首要瓶颈 | 第一候选 | 需要验证 | 失败信号 |
|---|---|---|---|
| batch 可扩、模型可单卡 | DP | global batch 与收敛 | sample efficiency 下降 |
| optimizer/gradient/parameter OOM | ZeRO/FSDP | gather/reduce overlap、peak buffer | 通信或碎片仍 OOM |
| 单层权重/GEMM OOM | TP | hidden/head divisibility、NVLink | small GEMM、all-reduce 主导 |
| 总层数/activation OOM | PP | stage balance、\(M/K\) | bubble/最慢 stage |
| MoE expert 参数 OOM | EP | routing balance、all-to-all fabric | hot experts、token drop |
| attention activation OOM | Ulysses/Ring/CP | heads、block、mask、topology | all-to-all 拥塞/causal imbalance |
| CFG 双分支 latency | CFGP | 分支成本、combine tensor | branch idle、状态复制 |
| projection/layout 反复 reshard | custom shard | 相邻 operator contract | 新增更大 redistribution |

## 2. Dense LLM 训练

典型路径：

1. DP 扩吞吐；
2. ZeRO/FSDP 切状态；
3. 单层 OOM 时加 TP；
4. 模型很深或 activation 高时加 PP；
5. 长序列再加 CP/SP。

拓扑建议：

- TP 放节点内；
- PP 沿节点边界；
- DP/ZeRO 跨节点；
- CP 高频通信尽量放快速域。

要测：

- per-rank peak memory，而非平均；
- GEMM shape 与 MFU；
- 每层 collective exposed time；
- PP bubble 和 max-stage time；
- communicator contention。

## 3. MoE 训练

新增 EP 后，模型参数增长不再等于每 token FLOPs 增长，但 token routing 成为动态数据重排。

优先检查：

- top-k、capacity factor、drop policy；
- 每 expert token count 的 P50/P99/max；
- dispatch/combine bytes 与 exposed time；
- EP 与 TP/CP 的 group nesting；
- all-to-all 是否跨 oversubscribed links。

[GShard](../papers/gshard.md)适合建立基础语义；[DeepSeek-V4](../../../02_model_systems/llm_foundations/papers/deepseek-v4.md#84-带宽互联与高效利用)提供 wave-based EP 等更定制的调度案例。

## 4. 长上下文

先区分瓶颈：

- 只是 LN/MLP activation 复制：轻量 sequence parallel；
- attention 需要全局 context：Ulysses/Ring/CP；
- KV cache 为主：需要单独设计 prefill/decode layout；
- causal/sparse mask 不均：workload-aware placement。

选择 Ulysses：

- heads 足够；
- all-to-all fabric 强；
- 希望复用标准 attention kernel。

选择 Ring：

- sequence 极长；
- 邻接链路强；
- block 足够大；
- 可以处理 causal imbalance。

## 5. 图像/视频生成

视频 DiT 同时有长 sequence、3D mask、CFG 双分支和 denoising-step 调度：

- Ulysses/Ring/CP 解决 token/context；
- CFGP 沿 conditional/unconditional branch；
- sparse CP 根据 block workload 重新分配；
- pipeline/timestep parallel 可能改变 cache 和同步边界。

参考 canonical 案例：

- [SwiftFusion](../../../02_model_systems/multimodal_generation/papers/swiftfusion.md)：Ulysses/Ring/Torus 与 topology-aware overlap；
- [Cosmos 3](../../../02_model_systems/multimodal_generation/papers/cosmos-3.md)：Ulysses、HSDP、CFGP、cache/compile；
- [DSV](../../kernel/custom_attn/papers/dsv.md)：hybrid sparse CP；
- [MAGI-1](../../../02_model_systems/multimodal_generation/papers/magi-1.md)：异构 mask 与 workload dispatch。

## 6. Serving

训练最优 mesh 不一定适合 serving：

- prefill compute-heavy，decode memory/bandwidth-heavy；
- DP 可能变成 request parallel；
- TP 降单请求 latency 但增加通信；
- PP 增 pipeline latency，需连续 batching；
- CP 需要 KV owner、cache migration 和 fault handling；
- speculative/CFG branches 可能适合 branch parallel。

应分别记录 TTFT、TPOT、tokens/s、KV cache peak、request tail latency，而不是沿用 training MFU。

## 7. 组合配置审查

每个候选配置写成：

| Axis | Degree | Physical scope | Placement | Collective | Peak buffer | Critical overlap |
|---|---:|---|---|---|---|---|
| DP |  |  |  |  |  |  |
| TP |  |  |  |  |  |  |
| PP |  |  |  |  |  |  |
| EP |  |  |  |  |  |  |
| CP/SP |  |  |  |  |  |  |

然后执行以下反证：

1. 如果去掉该轴，是否真的 OOM 或变慢？
2. collective-off/overlap-off 能否隔离收益？
3. max-rank workload 是否远大于平均？
4. 设备数增加时是固定工作量还是 weak scaling？
5. batch、模型、精度、checkpoint、kernel 是否同时变化？

只有控制变量明确，才能把收益归因给某个切分设计。
