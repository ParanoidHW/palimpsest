# 多模态稀疏 Attention 与定制 Mask Kernel 调研

> 检索快照：2026-07-10。范围：多模态理解、视频/图像生成、统一/世界模型；主硬件为 NVIDIA CUDA。论文原文、源码与检索证据包位于 [`_artifacts/ai_algorithm_survey_multimodal_custom_attn`](../../../_artifacts/ai_algorithm_survey_multimodal_custom_attn/)。

## 结论先行

1. **mask 已从模型脚本中的逻辑条件，变成运行时接口。** 可扩展实现不传完整 `[B,H,Lq,Lk]` mask，而是传可分解的流边界、block schedule、CSR、page table 或 selector 输出。
2. **“稀疏 mask”不等于“稀疏 kernel”。** Dense bool/bias mask 即使数学上为零，也通常仍触发 dense tile 的 QK/softmax/AV。必须让 kernel 知道可跳过哪些 tile，或者把 token/块先 compact 为 varlen segment。
3. **三条工程主线正在收敛。**
   - 规则型：`BlockMask`/kernel predicate，适合 causal、窗口、anchor、双流可见性。
   - 索引型：CSR/indptr/indices 或 paged block table，适合结构化 block sparse 与长视频。
   - 打包型：selector 后 gather QKV，交给 FlashAttention varlen，适合 learned/dynamic routing。
4. **CPU 可以生成 sparse metadata，但不应生成 dense mask。** LVSA 的官方代码明确将 CSR 留在 CPU，交给 FlashInfer planning pass；复杂度从 `O(Lq*Lk)` 降为 `O(nnz_blocks + n_rows)`。CPU 仍可能是 planner 瓶颈，需缓存、异步 pin-memory copy 或将动态 selector 放 GPU。
5. **统一模型的优先优化不是通用 mask。** Cosmos 3 把 reasoner causal 与 generator full attention lowering 为两次 variable-length 调用，比 FlexAttention baseline 快 22%（本地论文材料）；只有不可矩形分解的 window/anchor/router 才值得进入 block-sparse kernel。

## 1. 为什么完整 mask 不可取

对 `Lq=Lk=L` 的 bool mask，单头/单样本至少需要 `L^2` bytes；如果是 fp16 additive bias 则为 `2L^2` bytes，尚未包含 `[B,H]` 广播。`L=64K` 时：

$$
64K^2 \times 1\ \text{byte}=4\ \text{GiB},\qquad
64K^2 \times 2\ \text{bytes}=8\ \text{GiB}.
$$

FlashAttention 只避免 materialize attention **scores**，不自动让任意 dense mask 的无效 tile 消失。若 kernel 仍遍历所有 `(q_tile,k_tile)`，计算仍为 `O(L^2d)`；因此完整 mask 放 device 既占内存，也不能保证省 FLOPs。

## 2. 2026 前沿与谱系

| 类别               | 代表工作                          | mask/attention 非典型性                                                          | kernel/运行时证据                                                                         | 关键启示                                 |
| ---------------- | ----------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------ |
| 流式世界模型           | Causal-rCM (2026)             | `[clean,noisy]` teacher-forcing special causal mask；block 内双向、block 间 causal | `BlockPattern`/`AttnMaskSpec`、Flex `BlockMask`、custom FlashAttention-2 JVP Triton 路径 | mask 与 JVP、KV cache、CP 必须共同设计        |
| 动态视频稀疏           | HASTE (2026)                  | per-head budget 与 denoising-step mask reuse                                  | PDF 证据；官方代码未核验                                                                       | 先降低 mask planner 频率                  |
| 长视频生成            | LVSA (2026)                   | local window + rotating global anchors                                       | CPU CSR -> FlashInfer plan -> block sparse run                                       | 可跳过未列 tile，避免 dense mask             |
| 架构替代             | FrameDiT (2026)               | frame-level matrix attention                                                 | 开源实现仍有 dense-bias 框架路径                                                               | 不要把所有问题强行写成 sparse mask              |
| token selector   | Token Sparse Attention (2026) | 每 head interleaved token selection                                           | compact QKV 后复用已有 kernel                                                             | selector 与 kernel 可解耦                |
| 统一模型             | Cosmos 3 (2026)               | reasoner causal + generator full 的双流语义                                       | two-way flat attention；Hopper FA3、GB200 NATTEN/CUTLASS                               | 先分解成少量高效 varlen call                 |
| learned router   | VMoBA (2025)                  | query/block gate、threshold/top-k                                             | dense gate -> `nonzero`/pack -> FlashAttention varlen                                | routing 控制面可能成为瓶颈                    |
| training-free 视频 | Sparse VideoGen (2025)        | spatial/temporal head pattern                                                | 论文称 Triton + FlashInfer 原型                                                           | pattern dispatch 需要专用 tile traversal |
| 长上下文桥接           | MInference (2024)             | per-head dynamic A/vertical/block pattern                                    | PIT/Triton/FlashAttention kernels                                                    | kernel-aware pattern search 是核心      |

### 2.1 多模态 mask 的语义形态

多模态模型的关键不是普通 lower-triangular causal，而是下列组合：

```text
reasoner/text/history:        causal self-attention
video/audio/action tokens:    local bidirectional time-space window
current diffusion chunk:      bidirectional within chunk
past chunks:                  block-causal read
global/keyframe/reference:    sparse anchor read
noisy generation -> reasoner: forbidden or read-only boundary
```

其逻辑可看成多个条件的合取：`visible(q,k) = stream_rule AND time_window OR global_anchor OR same_chunk`。如果这些条件在 tile/block 粒度可计算，应传规则或 block metadata；不应先展开为 token-pair matrix。

## 3. Kernel 实现与 mask 表达对比

| 路径 | 模型侧表达 | kernel 看到的对象 | 是否 materialize dense mask | 适用与边界 |
|---|---|---|---|---|
| FlashAttention causal/varlen | `causal`、`cu_seqlens` | 连续序列边界 | 否 | 最快；只能表达少数标准结构 |
| FlexAttention | `score_mod` / `mask_mod` + `BlockMask` | 可计算 predicate + 可跳过 block | 不必；错误使用仍可能退化 | 适合规则复杂、原型到生产的 lowering |
| 定制 Triton/FlashAttention 衍生 | block schedule/offset/metadata | kernel 内 tile predicate 和索引 | 否 | Causal-rCM 的 JVP 类需求；维护成本高 |
| FlashInfer block sparse | CSR `indptr,indices`、page/block metadata | block traversal plan | 否 | LVSA、paged/KV serving；需要 plan 与 layout 对齐 |
| gather + FlashAttention varlen | selector/gate、indices、segment lengths | 已 compact 的 Q/K/V | 不传 pair mask | VMoBA/Token Sparse；gather/scatter 与排序有成本 |
| SDPA/Diffusers bias | bool / additive `[Lq,Lk]` 或广播 bias | dense score bias | 常常是 | correctness fallback；不适合长序列 sparse |

### 3.1 Causal-rCM：在线规则与结构化 metadata

官方代码的 `BlockPattern` 按 frame token 数和 chunk 划分 block，`AttnMaskSpec` 只携带 `mode`、block schedule、sliding-window、sink 和 query offset。`FlexOrSdpaLocalAttention` 注释明确：非 full 模式使用 FlexAttention + `BlockMask`，默认对齐 128 token block。JVP 路径必须使用同一 mask，因此该例证明 custom mask 不只是 forward 的 score bias，而是 autograd/JVP operator contract 的一部分。

### 3.2 LVSA：CSR 与 host/device 边界的直接答案

`ring_block_frame_csr()` 生成 `int32 indptr` 与 `int32 indices`；其注释明确 FlashInfer `BlockSparseAttentionWrapper` 会跳过未列 frame blocks，且“不构建 dense `[Sq,Sk]` mask”。更关键的是 `ensure_device()` 明确不移动 `fi_indptr/fi_indices`：它们供 host-side `build_bsa_mask_compact` 和 FlashInfer planning pass 消费。这里 CPU 传递的是 block 邻接表，不是完整 mask；执行期由 planner 生成适合 device 的内部副本/计划。

### 3.3 VMoBA：脚本侧 selector，但不传 token-pair mask

`src/vmoba.py` 中 gate 在模型侧以 bool tensor 暂存，通过 top-k/threshold 得到 `gate_mask`，再以 `nonzero` 收集索引、pack Q/KV、调用 FlashAttention varlen。它的稀疏表征是“选中的 token/块列表 + segment length”，不是 `Lq*Lk`。这适合 learned routing；但 `sort/topk/nonzero/gather/scatter` 都在 GPU 控制面上，低稀疏度或短序列可能慢于 dense FA。

## 4. 长序列怎样把 mask 给 kernel

推荐按动态性选择：

| 场景 | 推荐表征 | 生成位置 | 传入 kernel 的内容 |
|---|---|---|---|
| causal、固定窗口、固定跨模态块 | 参数化规则/BlockMask | GPU kernel 或一次 block compile | offsets、block size、window、stream id |
| 静态时空 anchor | CSR/CSC block adjacency | CPU 初始化或 GPU 初始化后缓存 | `indptr,indices`、tile/page layout |
| 每请求变化的 page/KV 选择 | page table + selected block ids | GPU selector；必要时 CPU scheduler | page IDs、lengths、indptr，不传 dense mask |
| learned top-k router | selected indices + packed varlen QKV | GPU | gather index、`cu_seqlens`、compact tensor |
| 每 denoising step 小变化 | cached metadata + delta/refresh flag | GPU | 上一步 pattern 与少量更新 |

**CPU 方案可行，但边界明确：** CPU 很适合静态几何 mask、请求级 planner 和 FlashInfer 的 plan preparation；metadata 应为 pinned `int32` CSR/page table，异步 H2D 与 QKV prefetch overlap。CPU 不适合逐 step、逐 head、逐 token 的动态 top-k：PCIe/NVLink 往返、Python 循环和同步会抵消稀疏收益。HASTE 的 temporal reuse 正是在减少这种 refresh 次数。

## 5. 面向 kernel 设计的推荐接口

```text
MaskSpec
  kind: split_stream | block_causal | window_anchor | csr_blocks | selected_segments
  geometry: seq/frame/modal offsets, block size, page size
  dynamic: static | per-request | per-step | per-layer-head
  storage: CPU-pinned metadata | GPU metadata | kernel predicate

plan(spec, layout, device) -> Plan
run(q, k, v, Plan) -> o
```

1. 先做 **lowering**：可将 mask 切成少数 full/causal rectangles 时，拆分为 varlen FlashAttention 调用。
2. 不可分解但结构化时，用 CSR/page table；让 kernel scheduler 遍历 `nnz_blocks`，不是所有 tile。
3. selector 驱动时，先 benchmark control-plane time：`T = T_select + T_pack + T_attn + T_unpack`，而不是只报 attention FLOPs。
4. 以 `O(nnz_blocks)` metadata、KV locality、head/layer load balance、denoising-step reuse 为硬约束；对跨模态 anchor 保留质量 guard（identity、motion、audio/action sync）。

## 6. 评测清单

| 指标 | 必要记录 |
|---|---|
| 语义正确性 | 每种 stream/window/anchor 边界的 dense reference 对比；JVP/backward 一致性 |
| 控制面 | metadata 生成、H2D、plan、top-k/sort、pack/unpack 时间 |
| kernel | attention 时间、有效带宽 `bytes/time`、tile occupancy、稀疏度与 speedup 曲线 |
| 内存 | dense mask 假设值、CSR/page/indices、QKV/KV cache、临时 gather buffer |
| 质量 | 视频 motion/identity/loop，音画/动作同步；理解模型的跨模态检索/定位 |
| serving | TTFT、TPOT、batch 变化、cache reuse、长短请求混合和 fallback 触发率 |

## 证据与限制

- 已核验源码：Causal-rCM、LVSA、VMoBA、FrameDiT；commit 与行级路径在中间产物各 `analysis.md`。
- 已核验 PDF：九篇核心工作；HASTE、Token Sparse Attention、Sparse VideoGen 的 kernel 具体数据结构因未取得官方实现而标为未核验。
- “2026 最新”是 2026-07-10 的公开检索快照；一般 Web 搜索工具响应解码失败，已用 arXiv API/PDF 和 GitHub API/官方仓库补足一手证据。
- 论文性能不可跨硬件、序列长度、视频模型与质量指标直接横比；本报告不将论文级加速全归因给 kernel。
