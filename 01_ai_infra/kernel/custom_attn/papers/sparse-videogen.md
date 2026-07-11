# Sparse VideoGen 精读：按视频时空先验选择结构化 mask，并把非连续时间访问重排成 block-sparse kernel 可吃的布局

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：`../assets/papers/sparse-videogen/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

## 来源与图示索引

- 论文：*Sparse VideoGen: Accelerating Video Diffusion Transformers with Spatial-Temporal Sparsity*，本地 `paper.pdf` 共 17 页。当前 artifacts 未包含官方代码，以下 kernel/API 表述仅来自论文与伪码。
- 推荐嵌入图：**Fig. 3（PDF p. 3）** 是 spatial head / temporal head 的 attention map 与视频 token 含义；**Fig. 4（p. 4）** 是在线 profile 选择 mask；**Fig. 5 + Algorithm 1（p. 5）** 是 layout transform 和 sampled-row classification；**Fig. 8（p. 8）** 说明重排前后为什么性能不同。

## 解决的问题

视频 DiT 的 full 3D attention 同时承载两种不同的关系：同帧/邻帧的空间一致性，以及同一空间位置跨帧的时间一致性。SVG 发现它们常由不同 attention head 主导：

- **Spatial head**：主要关注同帧及邻近帧的连续 token，attention map 为 frame-size 对齐的 block-wise 布局。
- **Temporal head**：主要关注不同帧中相同空间位置的 token，原始 frame-major token 顺序下呈间隔为每帧 token 数 \(L\) 的 slash/stride 访问。

难点不只是找对稀疏 pattern：head 的类别随 prompt 和 denoising step 改变；而 temporal head 的 stride 访问不连续，若原样喂给 Tensor Core，理论 sparsity 不会转换为实际加速。SVG 因此把算法拆成 **online classification + layout transformation + 专用稀疏 kernel**，是视频生成中“mask 语义、metadata、内存布局和 kernel”同时设计的典型样本。

## 符号与成本模型

| 符号 | 含义 | 论文位置 |
|---|---|---|
| \(H,L,N\) | hidden dim、每帧 token 数、总帧数 | PDF p. 5, Sec. 3.3 |
| \(c_s\) | spatial head 看的邻近帧数 | p. 5 |
| \(c_t\) | temporal head 看的跨帧 token 数 | p. 5 |
| \(Q,K,V,O\) | attention 输入/输出，伪码形状 `[B,H,S,D]` | p. 5, Algorithm 1 |
| \(Q_p\) / \(Q_i\) | online profile 抽样的 query rows | Fig. 4 / Algorithm 1 |

full 3D attention 的主计算量写为 \(4L^2N^2H\)。若 spatial head 每个 token 仅看 \(c_s\) 个邻帧，主项约为 \(4L^2Hc_sN\)；若 temporal head 每 token 仅看 \(c_t\) 个时间关联 token，约为 \(4N^2Hc_tL\)（p. 5）。这不是任意 unstructured top-k，而是依据视频的二维时空 token 排列定义的规则可计算 mask。

## 核心算法

### 1. 两个 mask family

Fig. 3（p. 3）给出语义：

- `mask_spatial` 选择同一帧和邻近 \(c_s\) 帧的空间 blocks；block 大小与每帧 token 数相关。
- `mask_temporal` 选择跨帧的相同空间位置，即原布局里 stride 为 \(L\) 的 token；论文还说明 text prompt 和首帧对两类 head 都保留，因为它们具有显著 attention 分数（p. 4-5）。

这些不是完整 \(S\times S\) dense mask 必须存在的唯一表达。Algorithm 1 为便于说明写出 `gen_spatial_mask()` / `gen_temporal_mask()`，但后续系统章节强调最终以 block sparse attention 和 layout transform 落地；论文没有公开其确切 descriptor schema（CSR、block list、bitmask 等）。

### 2. sampled-row online profiling

直接为每个 head 计算 full attention 再与两个 sparse 输出比 MSE，分类正确但没有加速。SVG 只采样 \(t\) 个 query row：

```python
indices = sample_indices(S, t)
Q_i = Q[:, :, indices, :]
O_full = mask_attention(Q_i, K, V, None)
O_spatial = mask_attention(Q_i, K, V, mask_spatial)
O_temporal = mask_attention(Q_i, K, V, mask_temporal)
best_mask_config = (MSE_spatial < MSE_temporal)
```

该 decision 为每个 head、每个 denoising step 选择 MSE 更小的模式（Fig. 4，p. 4；Algorithm 1，p. 5）。注意 `O_full` 仍需计算，但仅针对抽样 query rows，而不是全部 \(S\) rows。Table 3（p. 8）显示 1% profile 在 CogVideoX-v1.5-I2V 上取得 PSNR 31.118，接近 100% oracle 的 31.324；这验证的是分类 proxy 的质量，不是 free-of-cost 的 mask 生成。

### 3. temporal layout transform

Temporal head 的“同空间位置跨帧”在普通顺序中相隔 \(L\)，不能高效组成 Tensor Core 所需的连续 tile。论文将 token-major tensor transpose 成 frame-major layout，使跨帧时间 group 连续，再以 block-sparse attention 计算；该变换在数学上保持等价（PDF p. 6, Sec. 4.2；Fig. 5 p. 5）。

这一步的意义是：mask 语义没有变，**物理 layout 变了**。无变换的 sparse computation 虽跳过 pair，仍可能有 gather/scatter 和 non-coalesced load；变换后，selected temporal groups 可按 dense block 读取。Fig. 8（p. 8）报告在给定 sparsity 下，transform 路径比原始 sparse 实现额外约 1.7x，接近理论速度线。

## Kernel、metadata 与 host-device 数据流

```text
Q/K/V on GPU
  -> (Triton fused) sampled-Q full/spatial/temporal profile
  -> per-head {spatial | temporal} choice
  -> [temporal only] layout transform kernel
  -> block-sparse QK + online softmax + AV (FlashInfer-based path)
  -> inverse/layout-aware output
```

论文列出的系统实现（PDF p. 6, Sec. 4.3）应严格分层理解：

| 子问题 | 论文报告的实现 | 不应过度推断的内容 |
|---|---|---|
| profile + layout transform | Triton fused kernels | 没有 source/IR，无法核验是否一个 kernel、是否有 persistent cache |
| QK-norm / RoPE | 自定义 CUDA sub-warp reduction，面向 head dim 64 的并行不足 | 不是 sparse mask kernel；Table 2 的收益不能归因于 mask |
| sparse attention | FlashInfer 后的 block-sparse attention kernel；另称定制 kernel 支持 FP8 + block sparse | 未说明 block list 的精确内存格式、tile size、FlashInfer API / workspace |
| full mask 存储 | 论文以规则化 spatial/temporal pattern + profile 分类运行，没有要求为每个 pair 保留 dense bias | 具体 mask 是 kernel predicate、device block metadata，还是预建 tensor，未明说 |
| host CPU 参与 | 未报告 host 生成/读取 mask；性能实验在 GPU 上 | 不能主张 CPU side streaming 或 pinned-H2D metadata pipeline |

从文章的系统形态可得一个受限的工程推论：spatial/temporal 两类 mask 的大部分规则可由 token 坐标、帧数与 profile label 在线计算，实际需要存储的更可能是 per-head choice 和少量边界/布局参数，而不是 \(S^2\) mask。但这应标注为**结构性推断**，因为论文没有提供源代码来确认 metadata 的 device placement。

## 实验归因与证据矩阵

| 主张 | 直接证据 | 限制 |
|---|---|---|
| 两个模式能维持视频质量 | Fig. 3/4（p. 3-4）机制；Table 1（p. 6）CogVideoX T2V 的 SVG PSNR 29.989、2.28x | PSNR 主要相对 dense output，非人工偏好；不同模型 pattern 仍须 profile |
| online profile 足够小 | Table 3（p. 8）1% vs 100% profile | 仅 CogVideoX-v1.5-I2V 子集 |
| layout transform 是实际加速关键 | Fig. 5（p. 5）+ Fig. 8（p. 8）单 kernel 比较 | 具体 benchmark shape/稀疏率影响很大 |
| end-to-end 加速来自多组件 | Fig. 7（p. 7）HunyuanVideo：sparse attention 1.81x，FP8 后总 2.33x；Table 1 | 不应把 2.33x 全归因于 sparse attention |
| FP8 可叠加 | Table 1：HunyuanVideo 2.33x，PSNR 29.452 vs 29.546 | CogVideoX head dim 64 时作者明确说 FP8 不带来 on-GPU 加速（p. 7） |

## 局限与多模态落地启示

- **两模式假设可能不够。** 论文按 spatial/temporal 二分类；复杂 camera motion、对象交互、音频/文本/图像混合 token 可能出现第三类或跨模态 pattern。它没有给出 open-set fallback（例如 dense 或 generic block sparse）的质量策略。
- **profile 成本重复于每步。** 1% 仍需三次 sampled attention；长视频收益大时可摊销，但短序列、少 step 或大量小 batch 时控制面会占比更高。
- **从论文无法确认 metadata 格式。** `mask_spatial`/`mask_temporal` 在伪码中像 mask tensor，但 kernel 章节只说 block sparse/FlashInfer；不能声称使用 CSR、FlexAttention BlockMask 或完整 device mask。
- **没有可审计源代码。** 不能复现 H100/CUDA 12.4、FP8 格式、FlashInfer 版本、layout inverse 成本或 kernel occupancy；论文的“dedicated CUDA kernels”应与可复查实现区分。
- **对自定义 attention 的启示。** 对视频类规则可见性，优先使用坐标规则 + 小型在线分类器产生 mode，必要时转置/重排让 selected blocks 连续；不要先生成高维 dense mask 再交给通用 attention。真正无法用固定几何表达的模式，才需要 MInference/FlexAttention 类动态 index 或 selector。
