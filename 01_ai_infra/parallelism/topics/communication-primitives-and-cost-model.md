---
tags:
  - topic
  - collection/parallel-partitioning
  - domain/ai-infra
  - topic/collective-communication
document_type: topic
domain: parallelism
canonical: true
---

# 通信原语与成本模型

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 坐标系：[并行切分坐标系](parallel-coordinate-system.md)
> - 选型指南：[并行策略选型](../surveys/parallel-strategy-selection.md)
> - Claim 矩阵：[Evidence](../evidence/parallel-partitioning-claim-matrix.md)

并行方案的通信成本不能只用“总字节数”描述。实际 exposed time 同时由启动延迟、每 rank 字节、同步 step、拓扑、并发 collective、buffer peak 和 overlap 条件决定。

## 1. \(\alpha\)-\(\beta\) 基线

\[
T_{\mathrm{comm}}
\approx \alpha\,s(p)+\beta\,V(m,p)+T_{\mathrm{contention}}.
\]

- \(\alpha\)：一次通信 step 的启动/同步成本；
- \(s(p)\)：算法 step 数；
- \(\beta\)：每字节时间；
- \(V(m,p)\)：每 rank 的有效收发字节；
- `contention`：多个并行轴、NIC、NVLink 或 PCIe 共享资源产生的额外等待。

小消息主要受 \(\alpha\) 支配；大消息主要受带宽和拥塞支配。同样的 \(V\) 经由 all-to-all 与 ring P2P，性能可以完全不同。

## 2. Primitive 与语义

| Primitive | 输出语义 | 常见并行轴 | 典型风险 |
|---|---|---|---|
| all-reduce | 每 rank 得到全局 sum | DP gradient、TP partial output | 强同步、跨层高频 |
| reduce-scatter | 全局 sum 后每 rank 保留 shard | ZeRO/FSDP、sequence-parallel output | 下游必须能消费 shard |
| all-gather | 每 rank 拼出完整 tensor | ZeRO parameter、部分 SP/TP 边界 | 峰值 buffer 与瞬时带宽 |
| all-to-all | 每 rank 向每个 rank 发送不同 slice | EP、Ulysses | 小包、radix、oversubscription |
| broadcast | 一对多复制 | PP 参数/控制、初始化 | root 热点 |
| send/recv | 邻接 rank 交换 | PP、Ring | pipeline stall、邻接映射 |

all-reduce 常被实现为 reduce-scatter + all-gather；因此算法名和 runtime primitive 需要分层记录。

## 3. 代表性成本

### TP

以边界 activation \(n\approx bSH\) elements、dtype \(q\) bytes、ring all-reduce 为例，一层训练中四次 all-reduce 的 analysis-derived 每卡传输近似：

\[
C_{\mathrm{TP,layer}}
\approx 8\frac{p-1}{p}\,bSHq.
\]

TP degree 增大时计算按约 \(1/p\) 缩小，但通信系数趋近常数；这解释了强扩展末端的效率下降。[Megatron-LM](../papers/megatron-lm.md#43-fg-的-forwardbackward-collective-精确位置)给出准确 collective 边界。

### PP

均衡 stage 的名义 bubble：

\[
\beta_{\mathrm{pipe}}\approx\frac{K-1}{M+K-1}.
\]

这不是完整性能模型。最慢 stage、activation P2P、重计算、kernel shape 与调度策略会改变实际值。[GPipe](../papers/gpipe.md#43-关键公式)的 Table 2 支持 \(M/K\) 越大吞吐越好，但 batch size 可能调整。

### ZeRO/FSDP

ZeRO 的核心结论是：Stage 1/2 可在与经典 DP 同量级通信下减少状态冗余；Stage 3 通过 parameter all-gather/release 改变通信时序。实践还需加入：

- live parameter window；
- prefetch distance；
- bucket size；
- gather buffer 和 fragmentation；
- CPU/NVMe offload。

因此“平均每卡状态内存”不是“峰值显存”。

### EP

EP 的 dispatch/combine bytes 与 routed tokens、hidden size、top-k 和 dtype 成正比，但 exposed time 由 max-rank token count 决定。平均负载均匀仍可能有尾部热点。[GShard](../papers/gshard.md#42-专家并行与通信的准确位置)的 Figure 8 显示 all-to-all 随 expert scale 成为系统压力。

### Ulysses

论文级每链路元素量：

\[
V_{\mathrm{link}}\approx\frac{4SH}{P},
\]

来自 Q/K/V 与 attention output 的两次 all-to-all。该式不含 latency、反向、拓扑拥塞和 uneven heads；见 [Ulysses](../papers/deepspeed-ulysses.md#44-关键公式)。

### Ring Attention

通信被 block compute 覆盖的理想条件：

\[
c\ge \frac{F}{B}.
\]

其中 \(F\) 是设备 FLOP/s，\(B\) 是邻居链路 bytes/s，\(c\) 是 block length。causal skip 会减少某些 ranks 的 compute，破坏 overlap 窗口；见 [Ring Attention](../papers/ring-attention.md#43-关键公式)。

## 4. Overlap 不是免费

声称“通信被隐藏”时必须说明：

- overlap 的 compute kernel 是什么；
- 通信和计算是否使用独立 streams/engines；
- buffer 是否双缓冲；
- 最短可覆盖消息或 block 大小；
- critical path 是否仍有尾部 collective；
- causal/sparse/uneven workload 是否让各 rank 的 overlap window 不同。

如果没有 overlap-off 消融或 timeline，证据应标为 theory/indirect，而不是直接系统归因。

## 5. 拓扑

- TP/CP：高频低延迟，优先节点内 NVLink/NVSwitch。
- PP：邻接 P2P，通常更能容忍跨节点；activation 大时例外。
- DP/ZeRO：大消息，可层级化 reduce-scatter/all-gather。
- EP/Ulysses：all-to-all 对 fat-tree radix 和 oversubscription 最敏感。
- Ring：logical neighbor 必须映射到物理高速路径。

多轴组合时还要检查 NCCL communicator、NIC rail、rank ordering 和同时在途的 collective 是否争用。
