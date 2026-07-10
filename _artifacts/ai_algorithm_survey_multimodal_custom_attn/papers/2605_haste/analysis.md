# HASTE 精读：把稀疏 mask 的“控制面”从每步重算变成按 head 自适应复用

## 来源与图示索引

- 论文：*HASTE: Training-Free Video Diffusion Acceleration via Head-Wise Adaptive Sparse Attention*，PDF 共 25 页。本分析以本地 `paper.pdf` 为一手证据；本次未获得可审计的官方代码。
- 推荐嵌入图：**Fig. 2（PDF p. 5）**，不同 prompt/layer/head 的相邻去噪步 mask IoU；**Fig. 4（p. 7）**，在线 TMR 与离线 EBC 的总体数据流；**Fig. 5 + Algorithm 1（p. 9）**，低成本 drift 判据和缓存控制流；**Table 4/5（p. 15）**，两个组件及复用阈值的消融。
- 证据边界：论文明确说两项机制不改变底层 top-p 稀疏 attention pipeline 或 sparse kernel（p. 12-13），因此本文不能把它误写成新的 Triton/FlashAttention kernel。

## 解决的问题

训练后的视频 DiT 在每个 denoising step、每层、每个 head 上重新预测 top-p sparse mask。即使随后 QK/softmax/AV 已能跳过块，**mask 预测本身仍是控制面开销**，并会被几十个去噪步放大。HASTE 的观察是：

1. 相邻 step 的 mask 稳定性不是全局一致的，而是随 prompt、layer、head 变化（Fig. 2，p. 5）。固定“每 k 步刷新一次”的策略会让稳定 head 重算、又让不稳定 head 复用过期 mask。
2. 同一个 top-p 阈值在不同 head 上诱导的实际 sparsity 与模型误差不同（Fig. 3，p. 6），因此共享阈值不是同等质量预算下的最优分配。

它不是改变多模态 token 的可见性语义，而是面向视频生成中**动态 block mask 的生成与调度**。目标是在不训练、不改预训练权重、不改既有 XAttention/SVG2 稀疏 kernel 的前提下，同时降低在线 planner 成本并改善同一全局 sparsity 下的质量。

## 符号与核心机制

| 符号 | 含义 | 论文位置 |
|---|---|---|
| \(Q_t^{(h)},K_t^{(h)}\in\mathbb{R}^{N\times D}\) | step \(t\)、head \(h\) 的 query/key；\(N\) 是 token 数，\(D\) 是 head dim | p. 7, Sec. 4.2 |
| \(M_t^{(h)}\) | head 的稀疏 attention mask；观测阶段以累积概率质量达到 0.95 的二值 token mask 定义 | p. 4-5, Eq. (1) |
| \(S_t\subseteq\mathcal B\) | 底层 top-p pipeline 在 block 集合 \(\mathcal B\) 中实际保留的 blocks | p. 8, Eq. (3) |
| \(\bar Q_t^{(h)},\bar K_t^{(h)}\) | 按 token 维 mean-pool 后的 Q/K，作为轻量缓存 | p. 8, Eq. (5) |
| \(\delta\) | TMR 的 drift 阈值；小于阈值则复用 anchor mask | p. 8-9 |
| \(\tau_{l,h}\) | EBC 为 layer/head 离线选出的 top-p 阈值 | p. 9-12 |
| \(S_{l,h,k},E_{l,h,k}\) | 候选阈值 \(\tau_k\) 的已测实际 sparsity 与输出误差 | p. 10, Eq. (7) |

### 1. 在线 Temporal Mask Reuse (TMR)

对每个 head 维护最近一次刷新时刻 \(t_a\)、cached mask \(M_{t_a}^{(h)}\)、以及 \(\bar Q_{t_a}^{(h)},\bar K_{t_a}^{(h)}\)。当前 step \(t_b\) 先从刚产生的 Q/K 求均值，再计算：

\[
d_{t_a\to t_b}^{(h)}=
\lVert \bar Q_{t_a}^{(h)}-\bar Q_{t_b}^{(h)}\rVert_1+
\lVert \bar K_{t_a}^{(h)}-\bar K_{t_b}^{(h)}\rVert_1.
\]

若 \(d\leq\delta\)，直接把 anchor 的 block mask 交给底层 sparse attention；否则调用原有 `PredictMask`、更新 anchor 和缓存（Algorithm 1，p. 9）。论文先给出全 token drift 对 changed-block ratio 的上界 \(R_{t_a\to t_b}^{(h)}\le C\tilde d_{t_a\to t_b}^{(h)}\)，再用 mean-pooled 版本作为工程替代（p. 8, Eq. (2)-(5)）。

关键不是缓存一个 \(N\times N\) dense mask：HASTE 讨论的是底层 pipeline 的**block 保留集合**。它报告，在 Wan2.1-1.3B、480P、CFG 条件下，缓存完整 token Q/K 约需 11.2 GB，而缓存 pooled Q/K 约 0.35 MB（\(L=30,H=12,D=128,N=32{,}760\)，FP16；p. 8）。这说明长序列的可扩展点是小状态 + 既有 block metadata，而不是重传 dense boolean/bias mask。

为避免 per-head 选择造成过多 launch/startup，论文还有 layer-level gate：刷新 head 比例低于下阈值则整层复用，高于上阈值则整层刷新，中间才保留 head-wise 决策（p. 8）。这属于 scheduler/控制面优化，不改变单个 selected block 内的数学 attention。

### 2. 离线 Error-guided Budgeted Calibration (EBC)

EBC 把“所有 head 用同一 \(\tau\)”改为一个离散预算分配问题。它在 prompt pool 和分段采样的 timestep 上，为每个 \((l,h)\) 测量多个 \(\tau_k\) 的 \((S_{l,h,k},E_{l,h,k})\)，选择每个 head 一个候选点，同时满足平均 sparsity 下界（p. 10, Eq. (6)-(7)）。离线流程是：

`dense inference/cache dense velocity -> 单独稀疏一个 head + 候选阈值 -> 计算稀疏输出相对 dense velocity 的误差与实际 sparsity -> ILP 选表 -> 在线查表`。

误差不是仅用 attention-output MSE，而是 denoising velocity 误差的四个 3D-FFT 频带加权和（p. 11-12, Eq. (9)-(11)）。Table 1（p. 12）显示相同相对扰动下 LL 频带破坏最大，因而校准时以输出质量的 proxy 取代“尽量多跳过 block”的单一目标。论文实际以 4 个时间区间、每个 head 三个阈值 \(\{0.85,0.90,0.95\}\) 测量，权重为 \((1.0,0.5,0.01,0.01)\)（p. 13）。

## Mask、metadata 与 kernel 数据流

```text
当前 Q/K
  -> per-head mean pool + cached pooled Q/K 的 L1 判定
  -> [reuse] cached selected block metadata
     [refresh] existing XAttention/SVG2 的 block scoring + top-p selection
  -> existing block-sparse QK / online softmax / AV kernel
  -> O

离线：prompt/timestep 采样 -> dense velocity reference -> per-head candidate table -> ILP -> {tau[l,h]}
```

| 问题 | 可由论文确认的答案 | 不能从论文确认的部分 |
|---|---|---|
| mask 语义/粒度 | 线上 top-p 是以 **block** 为单位的 retain/skip；TMR 复用的是 head 的上次 sparse mask | 具体 block size、`CSR/COO/BlockMask` 字段、是否带 per-row ragged 长度均未给出 |
| mask 在哪生成 | TMR 判定在线；EBC 的阈值表离线生成；真正 `PredictMask` 复用既有 pipeline | `PredictMask` 是 GPU kernel、GPU 上的 planner，还是 host 预处理未披露 |
| kernel 如何收到 mask | 论文称底层 sparse kernel 未改，因此 HASTE 只减少其输入 metadata 的刷新频率 | 没有 API、Triton/CUDA 代码或 kernel trace，不能断言 CSR/bitset/dense bias |
| 长序列内存 | pooled Q/K 状态显著小于全 token Q/K；不需要为 TMR 新建 \(N^2\) dense mask | cached block-index 的精确大小、host-device transfer/是否 pinned memory 均未报告 |

工程上最合理的解释是：mask metadata 应长期驻留 device，refresh 时仅更新 selected-block descriptor；但这是**根据 block-sparse 系统惯例作的推断，不是论文已公开实现**。尤其不能把“0.35 MB pooled state”误读成完整 mask 的空间成本。

## 实验、归因与证据矩阵

| 技术主张 | 直接证据 | 结论强度 |
|---|---|---|
| mask 演化具 head 异质性 | Fig. 2（p. 5）热图/曲线 | 直接观察，但不是跨所有模型的统计证明 |
| pooled drift 可作为复用 proxy | Fig. 5（p. 9）与 mask IoU 呈负相关；算法给出显式 gate | 有机制和实证，阈值泛化仍待验证 |
| TMR 主要减少在线开销 | Table 4（p. 15）：baseline 1.30x，+TMR 1.49x；EBC-only 仍 1.30x | 受该 backbone/设置支持 |
| EBC 主要改善同预算质量 | Table 4：VBench 75.89% -> 76.28%，speedup 不变 | 受该校准池和指标支持 |
| 两者组合有更好折中 | Table 2/4（p. 14-15），Wan2.1-1.3B XAttention 从 150s/1.30x 到 131s/1.49x，VBench 75.89% 到 76.51% | 论文报告，未复现 |

阈值不能无限放宽。Table 5（p. 15）中 \(\delta=100\) 的复用率 96.53%，但 sparsity 降到 61.62%，速度反而仅 1.34x 且质量变差；这说明过期 mask 不只是质量风险，也会破坏“预测的 sparsity”与“实际跳过的计算”之间的对应关系。

## 实现核验、局限与启示

- **代码核验：未完成。** 当前 artifacts 未包含 HASTE 官方仓库；所有 kernel/metadata 结论只能停留在论文语义层，不能把它归入 Triton、FlexAttention 或 FlashInfer 的具体实现。
- **ILP placement 未披露。** 这是一次性离线校准，可能在 CPU 运行，也可能使用任意求解器；论文没有写，不能据此主张“host 生成 mask 后 H2D”。
- **质量归因有近似。** EBC 使用单 head 稀疏化与一阶可加 surrogate；多 head 同时稀疏时的互作只在最终实验中间接覆盖，并未逐项隔离。
- **多模态范围。** HASTE 的验证是 text-to-video / image-conditioned Wan 视频生成，而非统一理解-生成模型；其核心可迁移性在于“去噪步重复的动态 mask 控制面”，不等价于 AR LLM prefill 的一次性 mask planner。
- **对 kernel 设计的启示。** 若 sparse kernel 支持稳定 block descriptor，优先让 TMR 只缓存/更新 descriptor，Q/K drift 在 GPU 上融合或紧邻 projection 完成；不要预生成并上传完整 \(N\times N\) mask。是否把 head-wise 元数据合并为 layer-level launch，应由实际 descriptor 分歧率和 kernel batchability 决定。
