---
tags:
  - survey
  - collection/parallel-partitioning
  - domain/ai-infra
  - topic/distributed-training
document_type: survey
domain: parallelism
canonical: true
---

# 并行切分方法体系：DP、TP、PP、EP、SP、CP 与状态切分

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 领域规划：[并行切分知识领域规划](parallel-partitioning-domain-plan.md)
> - 统一坐标：[并行切分坐标系](../topics/parallel-coordinate-system.md)
> - 选型指南：[并行策略选型](parallel-strategy-selection.md)
> - 非规则切分：[不规则与 workload-aware 切分](irregular-and-workload-aware-partitioning.md)
> - 选篇证据：[Evidence](../evidence/parallel-partitioning-selection.md)

## 1. 总原则

并行切分的统一定义是：把全局 tensor、训练状态或执行图映射到 device mesh，使每个 rank 执行局部工作，再通过 collective/P2P 恢复与单设备程序一致的语义。

阅读任何方法时固定回答：

1. 切了什么；
2. 每个 rank 持什么；
3. 怎么恢复全局语义；
4. 节省了什么；
5. 新增了什么通信、bubble、buffer 或 imbalance；
6. 适合什么 workload 和 topology；
7. 与其他轴组合时是否发生 layout 冲突。

## 2. 方法总表

| 方法 | 切分对象 | 局部状态 | 恢复语义 | 主要收益 | 主要新增成本 |
|---|---|---|---|---|---|
| DP | batch/request | 完整模型 + 局部样本 | gradient all-reduce | 吞吐扩展、简单 | 状态复制、global batch |
| ZeRO/FSDP | optimizer/gradient/parameter | 局部 state shard | gather + reduce-scatter | 消除 DP 状态冗余 | 参数通信、峰值 buffer |
| TP | hidden/head/vocab | 局部权重/activation shard | sum/concat/reduce-scatter | 单层容量、GEMM 并行 | 高频 activation collective |
| PP | layers/stages | 连续层 + micro-batches | stage send/recv | 总模型容量 | bubble、stage imbalance |
| EP | experts + routed tokens | local experts | all-to-all dispatch/combine | MoE 容量 | 路由通信、热点 |
| Sequence Parallel | sequence activation | 非 attention activation shard | gather/reduce-scatter | activation memory | 与 TP layout 协调 |
| Ulysses-SP | sequence ↔ heads | full sequence + local heads | 两次 all-to-all | 长序列 attention | head/fabric 约束 |
| Ring-SP/CP | sequence/KV block | local Q + rotating KV | online softmax + ring | 工作集随 local block | 多 step、causal imbalance |
| CFGP | conditional branch | branch-local execution | guidance combine | 多分支并发 | 状态复制、分支不均 |

## 3. DP 与状态切分

经典 DP 让每个 rank 持完整模型，batch shard 后独立 forward/backward，再合并 gradient。它的计算效率高，但参数、梯度和 optimizer states 全部复制。

[ZeRO](../papers/zero.md)把这三类状态按顺序分片：

- Stage 1：optimizer states；
- Stage 2：再分 gradients；
- Stage 3：再分 parameters。

Stage 3 只在 layer 使用参数时 gather。论文的平均状态公式建立了容量上界，但实际峰值还取决于 prefetch、bucket、live window 和 allocator。

适用：state memory 是首要瓶颈、模型单层仍可执行。
反证：parameter gather 进入 critical path，或瞬时 buffer 仍 OOM。

## 4. TP

[Megatron-LM](../papers/megatron-lm.md)的经典配对：

- 第一 GEMM column parallel，切输出特征；
- GeLU 或 attention heads 本地执行；
- 第二 GEMM row parallel，切输入特征；
- 出口归约部分和。

关键代数原因：

\[
\operatorname{GeLU}(X_1A_1+X_2A_2)
\neq
\operatorname{GeLU}(X_1A_1)+\operatorname{GeLU}(X_2A_2).
\]

如果先按输入维切第一 GEMM，就必须在非线性前归约；column→row 配对把同步移到更少的边界。

适用：单层权重/GEMM 超单卡、节点内互联强。
反证：local GEMM 太小、all-reduce 比例上升、head/hidden 不可合理分片。

## 5. PP

[GPipe](../papers/gpipe.md)先把连续 layers 分 stages，再把 mini-batch 分 micro-batches。仅切 layers 仍然串行；micro-batch 才让不同 stage 同时工作。

均衡理想 bubble：

\[
\beta\approx\frac{K-1}{M+K-1}.
\]

重计算减少 stage 内 activation 保存，但增加 forward compute。GPipe 在 mini-batch 末同步更新，所有 micro-batches 使用同一参数版本。

适用：模型深、单层可放入一设备、可构造均衡 stages。
反证：最慢 stage、bubble 或 activation P2P 主导。

## 6. EP

[GShard](../papers/gshard.md)普通 Transformer layers 复制，MoE experts 分片。token 根据 router 分数 all-to-all 到 expert owner，计算后逆路由 combine。

capacity、random second-choice 和 auxiliary loss分别处理：

- 单 expert overflow；
- token 被丢弃；
- router 长期集中少数 experts。

适用：MoE 参数容量是主约束且 fabric 能承受 all-to-all。
反证：max-rank token count、dispatch/combine 或 capacity drop 主导。

## 7. SP 与 CP

### Ulysses

[Ulysses](../papers/deepspeed-ulysses.md)把 \([b,S/P,A,d]\) 转为 \([b,S,A/P,d]\)，attention 后再转回。它保留标准 attention kernel，但需要 all-to-all 和可分 heads。

### Ring

[Ring Attention](../papers/ring-attention.md)固定 local Q，KV 走 logical ring。online softmax 保证精确性。它依赖 block compute 覆盖邻接通信；causal mask 会产生三角负载。

完整对照见 [序列与上下文并行](../topics/sequence-and-context-parallelism.md)。

## 8. 通信与开销对照

| 方法 | 通信频率 | 消息形态 | latency 敏感 | bandwidth 敏感 | 其他关键开销 |
|---|---|---|---|---|---|
| DP | step/bucket | 大 gradient | 中 | 高 | global batch |
| ZeRO-3 | layer/bucket | parameter + gradient | 高 | 高 | gather buffer |
| TP | 每层多次 | activation | 高 | 高 | small GEMM |
| PP | stage boundary | activation/gradient | 中 | 中高 | bubble |
| EP | MoE layer 两次 | routed tokens | 高 | 高 | imbalance |
| Ulysses | attention 前后 | QKV/output all-to-all | 高 | 高 | head divisibility |
| Ring | 每 block step | neighbor KV | 高 | 中高 | block/causal balance |

## 9. 组合

推荐从约束驱动逐步增加轴：

DP → ZeRO/FSDP → TP → PP → EP → CP/SP。

这不是固定顺序，而是避免一次同时搜索所有 degrees。组合细节见 [多轴组合与设备网格](../topics/composition-and-device-mesh.md)。

## 10. 证据边界

- 六篇 Paper 均通过 schema/semantic validation 和原图 QA。
- Megatron-LM 是 accepted；其余因代码或 OpenReview 可访问性为 accepted-with-limitations。
- full-system scaling 不能自动归因到单个 parallel primitive。
- 当前框架 API 与论文版本分开记录；采用证据见 [方法与系统索引](../evidence/parallel-partitioning-method-system-index.md)。
