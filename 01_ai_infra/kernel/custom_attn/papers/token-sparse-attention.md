# Token Sparse Attention 精读：把任意 token mask 转换为连续 QKV 的 gather/attention/scatter 管线

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：`../assets/papers/token-sparse-attention/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

## 来源与图示索引

- 论文：*Token Sparse Attention: Efficient Long-Context Inference with Interleaved Token Selection*，本地 `paper.pdf` 共 16 页；本次 artifacts 未包含官方实现，kernel 细节仅以论文为准。
- 推荐嵌入图：**Fig. 3（PDF p. 3）** 是最关键的 `compress -> attention -> scatter/residual` 示意；**Algorithm 1（p. 4）** 给出 budget 和 per-head index 的求法；**Fig. 6（p. 7）** 把 selector/indexing、QKV compression、output decompression 的时延单列；**Table 10/11（p. 14-15）** 给出 A100/A6000 的 prefill 端到端数据。

## 解决的问题

长上下文 prefill 中，token eviction 虽然能减少后续计算，却把未选 token 从 hidden-state 流中永久移除。论文认为这与两个事实冲突：重要 token 随 layer 迁移（Fig. 2a，p. 2），且同层不同 head 需要不同 token 集（Fig. 2b）。

Token Sparse Attention 的解法是**每个 attention layer、每个 head 都从完整序列重新选 token，但只在紧凑子序列上计算一次 attention**。选不到的 token 本层没有 attention 增量，仍经 residual 留在完整序列中，因此下一层可以再次被选中。这是“interleaved”的含义，不能误读为 KV eviction 或永久 prompt compression。

## 符号与方法

| 符号 | 含义 | 论文位置 |
|---|---|---|
| \(L,L'\) | 原序列长度、某 head 选后的长度，\(L'\ll L\) | p. 2-3 |
| \(Q,K,V\) | 原始 QKV；按 head 选择后为 \(\hat Q,\hat K,\hat V\) | Fig. 3, p. 3 |
| \(S_h\) | head \(h\) 的保留 token index set | p. 3-4, Algorithm 1 |
| \(\hat A\) | 用少数 recent queries 对全部 keys 算出的轻量 attention proxy | p. 4, Algorithm 1 |
| \(s_h[t]\) | token \(t\) 对 head \(h\) 的 importance score | p. 4 |
| \(\tau\) | 由低重要度尾部累计质量确定的动态 token coverage / pruning budget | p. 4 |
| \(R_\ell\) | Inter-Layer Representation Drift，用于筛出可稀疏 layer | p. 4, Eq. (1) |

### 1. 选择与压缩

先用最近一小段 queries 近似 score：

\[
\hat A=\operatorname{softmax}\left(Q[-\text{last\_q}:]K^\top/\sqrt d\right),\qquad
s_h=\operatorname{pooling}\big(\operatorname{sum}_{\text{vertical}}(\hat A)\big).
\]

这一步的 score 计算由论文所称的 fused Triton kernel 完成，以减少中间 memory I/O（p. 4）。跨 head 聚合并归一化后，从**低**重要度开始找累计质量达到 \(\tau\) 的最小删除集合，得到 \(k_{keep}=L-k_{sparse}\)；再对每个 head 独立取 `TopK(s_h, k_keep)`（Algorithm 1）。换言之：layer 级 budget 决定“留多少”，head 级 score 决定“留谁”。

对第 \(h\) 个 head，按照 \(S_h\) gather 原始 Q/K/V 的行，构成连续的 \(\hat Q_h,\hat K_h,\hat V_h\in\mathbb R^{L'\times d}\)。随后在紧凑张量上运行原本的 dense FlashAttention 或任一 structured sparse kernel。其 attention 主项从 \(O(L^2d)\) 缩为 \(O(L'^2d)\)，且不会要求 kernel 支持任意的 token-pair predicate。

### 2. 解压与 residual 语义

计算结果 \(\hat O_h\) 用 \(S_h\) scatter 到 zero-initialized 的 \(O_h\in\mathbb R^{L\times d}\)，未选位置保留 0；然后与 residual 相加（PDF p. 3, Fig. 3）。这有两个不能混淆的后果：

- 本层 attention 增量对未选 token 为零，等价于对这些 query/output 使用硬选择；但 hidden state 本身没有从模型中删除。
- 每层都复原 \(L\)，所以后层能重新选择此前跳过的 token，代价是每层都需重新做 score、TopK、gather/scatter。

它不是仅剪 K/V。论文明确选择 Q、K、V 都压缩，并把输出恢复到完整长度；因此这一方案适用于 prefill，不自动解决 autoregressive decode 的 full KV-cache bandwidth 问题。

### 3. 哪些 layer 允许做 token sparsity

为避免全层启用造成显著质量下降，论文定义：

\[
R_\ell=\mathbb E_t\left[\frac{\|h_{\ell+1,t}-h_{\ell,t}\|_2}{\|h_{\ell,t}\|_2+\epsilon}\right],
\]

只对 normalized drift rank \(\hat R_\ell\le\delta\) 的 layer 启用（p. 4-5, Eq. (1)-(2)）。实验使用 \(\delta=0.5\)，该选择对每个模型只预处理一次；这与每个请求/每层在线计算的 \(S_h\) 是不同阶段，不能把 layer selection 说成 per-request mask planner。

## Kernel、mask 与长序列数据流

```text
full Q/K/V [B,H,L,d]
  -> recent-Q x full-K proxy score (Triton fused, paper claim)
  -> aggregate budget + TopK indices S_h [B,H,L']
  -> per-head gather to contiguous Qhat/Khat/Vhat [B,H,L',d]
  -> unchanged FlashAttention / block-sparse kernel
  -> scatter Ohat into zero [B,H,L,d] + residual
```

| 用户关心的问题 | 论文可确认的答案 |
|---|---|
| mask 如何表达？ | 核心表达是 per-head **一维 index set \(S_h\)**，不是 materialized \(L\times L\) boolean/bias mask；最终语义由 gather 与 scatter 实现。|
| sparse 表示在哪里使用？ | 上游是 token index / TopK；下游 QKV 是连续 dense 张量。若再叠加 FlexPrefill/MInference，后者才另有 block mask/structured index。|
| kernel 内 online 生成吗？ | score 计算被称为 Triton fused kernel；TopK/index/gather/scatter 的具体 kernel、是否融合、是否有 host 参与均未公开。|
| 长序列是否放完整 mask 到 device？ | 不需要。常驻的主要 metadata 是 \(S_h\)，规模约 \(O(HL')\) 个 integer，而 dense pair mask 是 \(O(HL^2)\)。|
| CPU 生成后读取吗？ | 论文没有这种路径；因为 selector 要读当前 Q/K，合理实现应在 device 上，但这只是实现推断，非公开代码证据。|

一个重要的工程约束是：节省并非免费。Fig. 6b（p. 7）将 scoring/indexing、QKV compression、output decompression 计为额外开销，且论文报告在 128K、各 coverage 下它们合计小于总 attention latency 的 11%。这只证明该实验实现可用，不表示任意 batch、head dim、ragged \(L'\) 都能保持相同占比。

## 实验与技术主张证据矩阵

| 主张 | 直接证据 | 结论强度/限制 |
|---|---|---|
| 跨 layer/head 动态选择优于永久 eviction | Fig. 2（p. 2）、Table 5（p. 8）同等约 1.5x 下 RULER 平均 86.84 vs FastKV 85.64 / GemFilter 85.12 | 有对照；任务限于 LLM prefill |
| 动态 coverage 优于固定 sparsity | Table 4（p. 8）：约 54.44% sparsity 时 dynamic 87.02 vs fixed 86.91；高 sparsity 处差距更大 | 受该 budget 对齐方式影响 |
| 与其他 kernel/结构化稀疏可组合 | Table 1（p. 5）FlexPrefill 2.44x -> 2.76x，平均 RULER 均 87.27；Table 12（p. 15）也含 Seer/X-Attention | 论文层面说明“无需改底层 kernel”，无源码审计 |
| 真正 prefill 加速只在长上下文显著 | A100 Table 10（p. 14）：8K 0.68s -> 0.70s，128K 31.04s -> 24.35s | 清楚显示短序列 planner/gather 可能反而减速 |
| 不加速 decode | Appendix A.4（p. 14）：所有方法 decode 使用 full KV + dense attention，TPOT 相同 | 明确范围边界 |

## 实现边界、局限与多模态迁移

- **没有官方代码可审计。** 论文声称 Triton scorer 和与 FlashAttention 的集成，但没有给出 Triton tile、`TopK` kernel、gather/scatter layout、dtype 或 stream placement；不能把它定性为完整的 fused Triton solution。
- **per-head ragged 长度是隐含难点。** 方法先得到每层统一的 \(k_{keep}\)，使各 head 在该层相同长度，这有利于 batch kernel；若扩展到真正 per-head 可变 \(L'_h\)，需 varlen/cu_seqlens 或 padding，论文未研究。
- **压缩的是 attention 的 Q/K/V，不是多模态 token routing 的完整答案。** 用于视频/图像-文本统一模型时，必须防止把图像全局 token、文本 instruction、特殊锚点误判为低重要度；论文的 LLM prefill 实验没有验证跨模态保留约束。
- **最适合作为 kernel 边界的例子。** 对任意、动态、token-granularity mask，优先在模型侧/selector 侧产出 index，然后将 QKV compact 到连续布局后调用成熟 FlashAttention；硬把每个任意 token predicate 塞入 block-sparse kernel，通常会损失 tile 利用率并使 metadata 复杂化。
