# LVSA 精读：训练外推时的窗口 + 轮转锚点，以及 CPU 生成的 Block-CSR

> 资料状态：已核对 arXiv PDF（10 页）与官方 `JiusiServe/LongVideoSparseAttention` 快照，commit `1ebcc92e13d353cbc685eb8bf435e47dd5dfa062`。这是训练免费（training-free）的 inference/serving 方法，不应与通过重新训练学习 sparse pattern 的 VMoBA 混为一谈。未发现公开 OpenReview 评审；性能和质量数字为论文在其提示词集、模型、GPU 与采样设置下的报告。

## 0. 资料、配图与符号

| 用途 | 一手来源 | 关键阅读点 |
|---|---|---|
| pattern 本身 | PDF §2.1，Fig. 1（PDF p.3） | basic window 预算浪费的原因，expanded window 如何保持每帧固定 budget |
| 长序列结果 | PDF Table 1 / Fig. 4（PDF p.6） | 将算法收益与 FlashInfer runtime 收益分开看 |
| CSR / host-device 边界 | `lvsa/sparse_attention.py:398-747` | `fi_indptr/fi_indices` 在 CPU；FlashInfer plan 拥有自己的 device-side copy |
| serving 集成 | `docs/VLLM_OMNI_INTEGRATION.md` | metadata 每个 denoising step 更新，runtime 不读取 host dense mask |

![论文 Fig. 1：LVSA basic/expanded sparse mask（PDF 第 3 页，后续应裁出图及完整 caption）](figures/page_png/page_03.png)

图 1 展示的是 frame-grid mask，不是 token-grid 的 dense materialization。每个彩色格会扩展为该 frame 内所有 patch token 的 block-pair。

| 符号 | 含义 | 作用域 | 证据 |
|---|---|---|---|
| $T$ | latent frame 总数 | request | PDF §2 |
| $P$ | 每 latent frame 的 patch token 数 | model geometry | PDF §2；`LVSAMetadata.build` |
| $W$ | local window 半宽 | per request | PDF Fig. 1、代码 `expanded_window_bounds` |
| $G$ | 首帧/周期 keyframe 组成的 global anchor set | 每 denoising step | PDF §2；代码 `compute_global_indices` |
| $\mathcal A(t)$ | query frame $t$ 可见 frame 集合 | 每 query frame | PDF §2 |
| $C$ | 目标 attended-frame budget | 每 query frame | PDF §2、Fig. 1 |
| `fi_indptr`, `fi_indices` | FlashInfer block-CSR row pointer/column index | host planner metadata | `sparse_attention.py:437-445,662-747` |

## 1. 论文解决什么问题，以及 sparse pattern 为什么能改善外推

视频 DiT 在超过训练时长后，full temporal self-attention 同时面对两个问题：$T^2$ 时间/显存增长，以及所有远距离 frame 一视同仁带来的时序退化（论文将其描述为 frozen/looping output）。LVSA 不改变权重，也不根据 QK 值在线学习 token router；它为每个 query frame $t$ 规定

$$
\mathcal A(t)=G\cup W(t), \qquad |\mathcal A(t)|\approx C,
$$

其中 $G$ 包含起始参考帧和周期 keyframe，$W(t)$ 是局部 temporal window。若局部窗口与 $G$ 重叠，naive pattern 实际可见帧数会小于 $C$；expanded window 会向外延伸，补足非全局帧。这一点正是 Fig. 1 左右两图的区别，而不是“增加了更多 global frame”。

keyframe grid 会随 diffusion step 平移。它让一个长视频中的不同 frame 在多步去噪中轮流充当 global anchor，避免固定锚点长期偏置。这个现象是算法设计；FlashInfer 与 SDPA 两个 backend 应给相同 pattern 的近似数值输出，因而不应把质量变化归给 FlashInfer。

若 $P$ 为每帧 token 数，则 dense attention 的主项约为

$$
O(T^2P^2d),
$$

而固定 budget 的 LVSA 每个 query token 最多看 $CP$ 个 key token，主项约为

$$
O(TCP^2d).
$$

这解释了为什么 $T$ 增长时收益加大，但不保证短序列一定更快：metadata、gather、compact-KV copy、kernel plan 的固定开销可能超过省掉的 QK work。

## 2. 从 mask 规则到 runtime：SDPA、Triton metadata、FlashInfer CSR

### 2.1 同一模式的三种执行表达

| 执行路径 | mask 表达 | kernel 实际收到什么 | 是否构造 $[L,L]$ mask |
|---|---|---|---|
| SDPA fallback | Python `local_frames` + `window_ctx`，按 frame gather | 每帧一个小的 `Q_chunk` 对 `K_global + K_window` 的 dense SDPA | 否 |
| indexed/Triton 相关路径 | `global_frame_mask[T]`、`window_bounds[T,2]`、`attended_indices[T_{local},C]` | 小型索引/边界 tensors，供 indexed gather 或 kernel | 否 |
| FlashInfer | block CSR `indptr[MB+1]`、`indices[nnz]` + compact KV layout | pre-planned `BlockSparseAttentionWrapper` 与 `[B,compact_N,H,D]` 的 K/V | 否 |

`LVSAMetadata.build` 是规则到 metadata 的唯一入口：先在 host 侧按 $(T,P,W,G,rank,world)$ 计算每个 local query frame 的可见 frames，再生成三类 backend 所需索引（`sparse_attention.py:451-596`）。这说明 LVSA 是**离线/step-level pattern planner**，不是 kernel 内根据 QK score 做 selection。

FlashInfer 格式的生成尤其清楚：`_build_flashinfer_csr` 对每个 query block 收集 visible frame，压缩为 `compact_frames`，然后构造

$$
\texttt{indptr}[i+1]-\texttt{indptr}[i]
= \#\{\text{visible KV blocks of Q block }i\},
$$

`indices` 列出压缩 KV block 的编号（`sparse_attention.py:662-747`）。`global_copies` / `local_copies` 则描述怎样把 global anchors 与本 rank local K/V 填进紧凑 buffer。这是 sparse 的真正存储格式：**block CSR + compact K/V**，不是 COO token pair，也不是 full attention bias。

### 2.2 “CPU 生成后给 kernel”到底是什么意思

本实现给出非常直接的反例，说明“不在 kernel online 生成”并不等于“把完整 mask 从 CPU 拷到 GPU”：

- `fi_indptr`、`fi_indices` 创建为 `int32` CPU tensor；
- `LVSAMetadata.ensure_device` 有意不把它们 `to(device)`，注释说明它们被 host-side mask builder 与 FlashInfer planning pass 消费（`sparse_attention.py:598-607`）；
- FlashInfer plan 在 runtime 内部准备自己的 device/NPU copy，之后 `lvsa_flashinfer` 只执行 `fi_wrapper.run(q,k_compact,v_compact)`（`:792-822`）。

因此，attention inner loop 不会跨 PCIe/CPU RAM 逐格读取 mask。host 传输的是 $O(MB+nnz)$ 个 `int32` 的结构化 metadata，device 上的主要 payload 是 compact K/V；相比 $O((TP)^2)$ 的 dense mask，规模和传输都可控。若 pattern 每一 denoise step 因轮转 keyframe 变化，则 planner 重建/传输会进入 step latency，长序列才更容易摊薄这项成本。

### 2.3 kernel / 硬件边界

- `lvsa_sdpa` 对每个 frame 拼接 `k_global` 和 local pieces，调用 SDPA/FlashAttention dispatch（`sparse_attention.py:755-810`）。它可跑 CUDA、Ascend NPU、CPU，但仍有多次小调用与 concat 的开销。
- `lvsa_flashinfer` 是 CUDA-only 的 single planned block-sparse run（`:813-851`）；论文 headline 中的 LVSA-FI 应理解为“同一 algorithm pattern + 更合适的 block-sparse runtime”。
- GQA 不会预先把 KV 重复到 query head 数，代码把 `enable_gqa` 交给 backend（`:770-807`）；这是一个实在的 KV bandwidth/VRAM 节省。
- 多 GPU 情况下，pattern 是 sequence/frame grid；`LVSAMetadata` 带 `rank/world`、local frame range。Ulysses 可在 all-to-all 后使用完整 grid；Ring-SP 若永远看不到完整 K/V，则文档要求 fallback dense/不启用该路径，不能假设 CSR 自动解决分布式可见性问题。

固定 commit 代码：[`sparse_attention.py`](https://github.com/JiusiServe/LongVideoSparseAttention/blob/1ebcc92e13d353cbc685eb8bf435e47dd5dfa062/lvsa/sparse_attention.py)、[`architecture.md`](https://github.com/JiusiServe/LongVideoSparseAttention/blob/1ebcc92e13d353cbc685eb8bf435e47dd5dfa062/docs/architecture.md)、[`vLLM-Omni integration`](https://github.com/JiusiServe/LongVideoSparseAttention/blob/1ebcc92e13d353cbc685eb8bf435e47dd5dfa062/docs/VLLM_OMNI_INTEGRATION.md)。

## 3. 证据、结果与落地边界

PDF Table 1（p.6）在单张 80GB GPU、五条长 prompt 的设定下报告：Wan 2.1 1.3B 在 481 frames/6x horizon 时，dense `50.8 min`、LVSA-FI `16.0 min`，为 `3.17x`；Wan 2.1 14B 同点为 `237.9 min` 对 `79.8 min`，为 `2.98x`。HunyuanVideo 1.5 在 257 frames/2x 时 dense OOM，而 LVSA-FI 为 `54.9 min`；论文给出的峰值显存约 `60.4 GB`，dense 在 80GB 卡上无法完成。

| 论文声称 | 支撑证据 | 证据强度 | 正确归因 |
|---|---|---|---|
| length extrapolation 更快 | Table 1 / Fig. 4，多个 horizon | 直接 runtime 对比 | 由 $TC$ sparsity 加 runtime 共同决定 |
| extended horizon 质量较好 | Table 2、Fig. 5 | 定性 + 指标 | pattern 的 rotating anchors/window 是候选原因；kernel 不改变数学 mask |
| LVSA-FI 优于 LVSA-SDPA | Table 1，同 mask backend 比较 | 直接 runtime 对比 | FlashInfer/compact CSR runtime 效果 |
| training horizon 保持品质 | Table 2 | 有限样本实测 | 不等于所有模型/提示词的 exact equivalence |

需要保留的限制：

1. 实验提示词数量小，且 long-video quality 指标对“静止但一致”的偏好存在争议，作者也讨论 VBench-Long 与 VQeval 的分歧；不能把单一 benchmark 当成内容质量的充分证据。
2. global/window pattern 是静态几何规则，不能对语义突变、镜头切换或跨模态事件做数据依赖选择；大 $W$、过密 anchors 会迅速吞掉 sparsity。
3. CSR planner、compact-buffer copy 和不连续 KV 访问可降低 tensor-core/HBM 利用率。短长度、低稀疏度或频繁改 geometry 时，dense FA 可能更快。
4. “CPU metadata”路线需要 cache：相同 geometry/step pattern 应复用 plan；若请求级 pattern 任意变化，host planning 与 H2D metadata latency 需纳入端到端 benchmark。

**一句话总结**：LVSA 不是向 kernel 传一张稀疏 token mask，而是用固定的 `global anchors + expanded local window` 规则在 CPU 构造 frame-block CSR，再将紧凑 K/V 与经 planner 编译的 CSR 交给 FlashInfer；这是一条可扩展到长序列 serving 的“host plan、device execute”路径。
