---
tags:
  - topic
  - collection/parallel-partitioning
  - domain/ai-infra
  - topic/long-context
document_type: topic
domain: parallelism
canonical: true
---

# 序列与上下文并行：Ulysses、Ring 与 CP

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 方法总览：[并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md)
> - Ulysses：[Paper](../papers/deepspeed-ulysses.md)
> - Ring Attention：[Paper](../papers/ring-attention.md)
> - 不规则 CP：[Survey](../surveys/irregular-and-workload-aware-partitioning.md)

SP/CP 的术语并不统一。本 Topic 以 attention 内的数据所有权为主线：每个 rank 持哪些 Q/K/V、全局 softmax 如何恢复、attention 前后 layout 是否变化。

## 1. 三类数据流

### Megatron-style Sequence Parallel

非 attention 的 LayerNorm/dropout 等 activation 沿 sequence 切分，减少复制 activation；进入需要 TP layout 的算子时执行 reduce-scatter/all-gather。它常是 TP 的补充，不等于长上下文 attention 本身。

### Ulysses

逻辑 layout：

\[
[b,S/P,A,d_h]
\xrightarrow{\mathrm{all\text{-}to\text{-}all}}
[b,S,A/P,d_h].
\]

每 rank 在 attention 内看完整 sequence、只计算部分 heads；attention 后做逆 all-to-all。优点是 local attention kernel 保持标准接口，缺点是依赖 all-to-all fabric 和 head partition。

论文均匀路径要求 \(A\bmod P=0\)。当前有限官方实现有 uneven-head 分支，但引入不均匀负载和 overlap 限制，不能回填为论文实验结论。

### Ring Attention

每 rank 固定 local \(Q_i\)，K/V blocks 在 logical ring 中移动。online softmax 维护 running max、denominator 和 weighted numerator，使分块合并仍是精确 attention：

\[
\begin{aligned}
m_j &= \max(m_{j-1},\max z_j),\\
\ell_j &= e^{m_{j-1}-m_j}\ell_{j-1}+\sum_k e^{z_{j,k}-m_j},\\
o_j &= e^{m_{j-1}-m_j}o_{j-1}+\sum_k e^{z_{j,k}-m_j}V_{j,k}.
\end{aligned}
\]

优点是单卡工作集随 local block 而非 global sequence 增长；缺点是 \(p-1\) 个 ring steps、block-size overlap 条件和 causal imbalance。

## 2. 对照

| 维度 | Ulysses | Ring Attention |
|---|---|---|
| Q ownership | attention 前后随 layout 转换 | local Q 固定 |
| KV ownership | all-to-all 后每 rank 得完整 sequence 的 head slice | KV blocks 环传 |
| communication | 两次 all-to-all | neighbor P2P |
| local operator | full-sequence attention on local heads | blockwise attention + online softmax |
| 主要约束 | head divisibility、all-to-all fabric | block size、ring mapping、causal load |
| 输出 layout | 回到 sequence shard | 留在 Q owner |

## 3. Causal 与稀疏 workload

规则 sequence shard 假设各 rank 工作量近似相同，但 causal mask 形成三角工作量：

- 早期 Q block 只看少量历史 K；
- 后期 Q block 看几乎全部 K；
- 某些 ring steps 只有通信没有足够 compute 覆盖；
- 同步推进时快 rank 等待慢 rank。

稀疏视频 attention 还会因 head、layer、timestep 和 mask pattern 变化而更不规则。[DSV](../../kernel/custom_attn/papers/dsv.md#4-研究方法)联合搜索 head/sequence CP 与头分配；[MAGI-1](../../../02_model_systems/multimodal_generation/papers/magi-1.md#6-magiattention-与-infrastructure)按异构 mask 调度 workload 和 communication group。

## 4. 组合边界

- 与 DP/ZeRO：参数状态可独立分片，但 DP×SP group 的 gather/reduce 时序需明确。
- 与 TP：Ulysses 和 TP 都可能切 heads/hidden，必须避免同一轴重复切或产生额外 transpose。
- 与 PP：sequence shard 可跨 stage 保持，但 stage boundary activation layout 必须一致。
- 与 EP：MoE token all-to-all 与 Ulysses all-to-all 可能争用同一 fabric。
- 与 cache：训练 activation、prefill KV 和 decode KV 的 layout 不同；[Causal-rCM](../../../02_model_systems/multimodal_generation/papers/causal-rcm.md#8-infra-需求分析)提供 Ulysses layout 与 CP cache 的案例。

## 5. 选择

优先 Ulysses：

- heads 足够多且可均匀切；
- all-to-all fabric 强；
- 希望复用标准 attention kernel；
- sequence/head transpose 可与上下游 layout 对齐。

优先 Ring：

- sequence 极长；
- 邻接高速链路稳定；
- block compute 足以隐藏 P2P；
- 能处理 causal/sparse imbalance 或采用更均衡的 token placement。

如果只是 LayerNorm/MLP activation 复制过多，而 attention 并未 OOM，先考虑轻量 sequence parallel，不必直接引入完整 CP。
