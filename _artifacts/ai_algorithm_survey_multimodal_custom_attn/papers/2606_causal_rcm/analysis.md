# Causal-rCM 精读：把 Teacher-Forcing mask 做成可 JVP 的结构化 Attention

> 资料状态：已核对 arXiv PDF（32 页）与官方 `NVlabs/rcm` 快照，commit `ed3cb14dd936f92cdc9f9381af7369991509b41f`。本文件的图示来自论文 PDF 渲染页；后续成品应裁出完整图和 caption，而不是把图重新绘制为结论图。论文为 2026 年 technical report/ICLR 2026 仓库标注，未检索到公开 OpenReview 评审，以下性能结论按作者报告对待。

## 0. 资料、图示与术语

| 用途 | 一手来源 | 阅读时应看什么 |
|---|---|---|
| 因果训练语义 | `paper.pdf` §2.3、§3.1，PDF p.6 的 Fig. 3 | TF/DF/SF 三条训练轨迹，以及 TF 的 clean/noisy block mask |
| 方法阶段 | PDF p.7 的 Fig. 4 | “先 TF-CM、后 SF-DMD”的分阶段关系，不要误读为单一 loss |
| 自定义 attention/JVP | PDF §B，`extracted_text/page_15.txt`；`rcm/utils/flash_attention_jvp_triton.py` | primal 与 tangent 必须走同一可见性规则 |
| mask lowering | `rcm/utils/blockmask.py`、`rcm/utils/magimask.py` | `BlockMask` 和 range-CSR，而非 `[L,L]` bool tensor |

![论文 Fig. 3：TF/DF/SF 的训练与 KV-cache 关系（PDF 第 6 页，后续应裁图）](figures/page_png/page_06.png)

图 1 的关键信息是：TF 把 clean context 和 noisy target 放入同一次 packed forward；SF 则真的按 chunk rollout 并维护 KV cache。因此两者不能仅靠“改变 loss”互相替代。

| 符号 | 含义 | 作用域 | 证据 |
|---|---|---|---|
| $x_0^i, x_t^i$ | 第 $i$ 个 video block 的 clean latent、时刻 $t$ 的 noisy latent | block | PDF §2.3、§3.1 |
| $v_{\theta}$, $v_{\mathrm{teacher}}$ | 学生/teacher 的 flow velocity 或 denoiser 所诱导的速度 | token/block | PDF §2、§3.1.2 |
| $M_{\mathrm{TF}}$ | packed `[clean, noisy]` 的 teacher-forcing attention 可见性 | Q-K block 对 | PDF §3.1.1；代码 `blockmask.py:258-312` |
| $\operatorname{JVP}$ | 预测沿 teacher ODE 轨迹的 Jacobian-vector product | 单层/全网 | PDF §3.1.2、§B |
| `BlockPattern` | frame-to-block 切分（首块、后续 chunk、每帧 token 数） | metadata | `blockmask.py:71-143` |

术语边界：这里的 **TF mask** 是训练时 attention graph，不是 diffusion loss mask；**SF** 是用自身生成历史作为 context 的 rollout 训练；**JVP** 是计算连续时间一致性目标的导数传播，不是为常规 attention 额外加的一次推理。

## 1. 要解决的问题与核心机制

### 1.1 逻辑链

AR video diffusion 让每个 frame/chunk 只依赖历史，因而可使用 KV cache 做 streaming；但稳定的 offline TF 会在真实 clean history 上训练，推理时却面对自己的生成历史，产生 exposure bias。反过来，SF/DMD 直接对 rollout 分布优化，但训练较不稳定。Causal-rCM 的主张是将二者**分阶段**组合：

$$
\text{causal teacher / initialization}
\rightarrow \text{TF-CM（offline, forward-divergence）}
\rightarrow \text{SF-DMD（on-policy, reverse-divergence）}.
$$

关键不是一个普通 causal lower triangle，而是对每个 block 的可见性精确约束：设 clean half 和 noisy half 都有 $n$ 个 block，noisy block $i$ 只能读取 clean 的严格历史 block $<i$ 与自身 noisy block $i$。对应的规则可概括为

$$
M_{\mathrm{TF}}(q,k)=
\begin{cases}
k\le q,&q,k\in\mathrm{clean},\\
k<i,&q\in\mathrm{noisy}_i,\;k\in\mathrm{clean},\\
k\in\mathrm{noisy}_i,&q\in\mathrm{noisy}_i,\\
0,&\text{otherwise}.
\end{cases}
$$

这里的 $\le$ 是 **block-causal**（块内可双向），并非 token 级 strict causal；是否启用 local window/sink block 是额外的实现配置。论文 Fig. 3 直观展示了 TF 中 clean/noisy 的非三角形网格，以及 SF 的 cache append/read-only 执行。

### 1.2 为什么需要 JVP-aware custom attention

连续时间 CM 需要沿 teacher trajectory 的切向量。抽象地，若网络输出为 $f_\theta(x,t)$，则

$$
\mathrm{JVP}\big(f_\theta,(x,t),(\dot x,1)\big)
=\partial_x f_\theta(x,t)\dot x+\partial_t f_\theta(x,t).
$$

TF-CM 中 clean half 的 tangent 为零，noisy half 才随 teacher velocity 演化（PDF §3.1.2）。因此 primal attention 和 tangent attention 必须共享 $M_{\mathrm{TF}}$；先跑 dense/causal attention 再对输出置零会混入本不该存在的 KV 信息，数学上不等价。

论文报告相对 discrete-time distillation 有“10x faster convergence”的总体训练结论（摘要、PDF p.1）。这应归因于连续时间目标、JVP 实现、teacher/student recipe 与训练配方的组合，**不是**单独 kernel 的 10x 加速。

## 2. Mask 如何进入 kernel：从规则到 BlockMask / range-CSR

### 2.1 三层表示，而不是 dense mask

| 层级 | 具体表示 | 在哪里生成 | 作用 |
|---|---|---|---|
| 模型语义 | `AttnMaskSpec(mode="teacher_forcing", pattern, clean_blocks, local_attn_blocks, sink_blocks)` | Python metadata | 说明 clean/noisy、chunk 边界和局部窗口 |
| FlexAttention lowering | `mask_mod(b,h,q_idx,kv_idx)` -> PyTorch `BlockMask` | GPU 上 `create_block_mask`，以 128-token block 缓存 | 编译为可跳过 tile 的 block 元数据 |
| Magi/JVP lowering | `q_ranges[R,2]` + `k_ranges[R,2]` -> `MagiMask{q_unique,k_flat,qk_map,tasks}` | range 构造后 merge/CSR group | 给 Triton JVP kernel 枚举允许的矩形切片 |

`blockmask.py:270-309` 直接把上述四分支翻译为 predicate；`:316-333` 以 `(spec,Q_pad,KV_pad,device,BLOCK_SIZE)` 为 key 缓存 `BlockMask`。普通 Flex path 会按 block 对齐 padding（默认 `mask_block_size=128`，`:368-389`），但不会创建 $L\times L$ bool/bias tensor。

JVP 路径更能回答“custom mask 到底在哪里表达”：`magimask.py:10-124` 先将每一段允许区域表达为 query/key 的半开区间，例如 noisy block $i$ 输出两类 rectangle：`[noisy_i]×[clean_<i]` 和 `[noisy_i]×[noisy_i]`。随后 `merge_k_ranges` 合并重叠 key range，`prepare_magi_csr_and_tasks` 形成 query-range 到 key-range 的 CSR（`:126-285`）。Triton kernel 的每个 query tile 只迭代这些 range（`flash_attention_jvp_triton.py:255-406`），而不是扫描全长 KV 并逐元素判断一个 bool mask。

### 2.2 代码到 kernel 的精确链路

1. `BlockPattern` 将 `frame_tokens`、首 chunk、后续 chunk 转成 block 边界（`blockmask.py:71-143`）。
2. `AttnMaskSpec` 固化 training/inference mode（`blockmask.py:145-170`）。
3. Flex backend：`_make_mask_fn` -> `create_block_mask` -> `torch.compile(flex_attention)`；可选后端为 PyTorch Inductor Triton 或 FA4/CuTe（`blockmask.py:12-29`、`:316-389`）。
4. Magi/JVP backend：`make_magi_ranges_full` -> `MagiMask` CSR/task list -> `_attn_fwd` custom range kernel；Triton forward 同时维护 output、logsumexp 与 tangent output（`flash_attention_jvp_triton.py:95-229,255-406`）。
5. backward 仍调用 FlashAttention-2 接口；源码明确 `MagiMask` 的 backward 未支持（`:460-505`），这是复现实验必须验证的边界，不能把它描述成全训练路径均为单一 Triton kernel。

官方代码固定 commit 的可追溯链接：[`blockmask.py`](https://github.com/NVlabs/rcm/blob/ed3cb14dd936f92cdc9f9381af7369991509b41f/rcm/utils/blockmask.py)、[`magimask.py`](https://github.com/NVlabs/rcm/blob/ed3cb14dd936f92cdc9f9381af7369991509b41f/rcm/utils/magimask.py)、[`flash_attention_jvp_triton.py`](https://github.com/NVlabs/rcm/blob/ed3cb14dd936f92cdc9f9381af7369991509b41f/rcm/utils/flash_attention_jvp_triton.py)。

### 2.3 长序列与系统含义

若将 $B$ 个 frame/chunk、每块 $P$ token 的规则 materialize 为 token mask，存储为 bool 也有 $O((BP)^2)$ bytes，若为 fp16 bias 则是两倍；本实现只传 `BlockPattern`、少量 scalar、block/range CSR。对规则稀疏的元数据上界约为 $O(B)$ 个 q-range 加允许 k-range，实际取决于 local window/sink 的分段数。

它也**不是 CPU 直接喂给 GPU kernel 读取**：Flex `BlockMask` 和 Magi range tensors 都由 device-side attention runtime 消费；host 只负责构建/cache Python metadata。若每 step 的 chunk 数、window 或 cache offset 改变，BlockMask/CSR 缓存 key 会失配并重新构建。长上下文的主要剩余瓶颈是 KV cache、本地块 padding、Ulysses CP 的 all-to-all，以及不规则 mask 引起的 tile 利用率，而不是 dense mask 显存。

| 技术声称 | 直接证据 | 证据强度 | 应如何解读 |
|---|---|---|---|
| TF mask 精确模拟 clean-history training | Fig. 3、PDF §3.1.1、`blockmask.py:270-309` | 机制 + 代码直接 | 支持，但不等价于已经消除 rollout gap |
| TF-CM + SF-DMD 互补 | Fig. 4、主结果/阶段描述 | 端到端为主 | 分阶段收益没有完全独立的 component 方差分解 |
| JVP 可在 custom mask 下运行 | PDF §B、`magimask.py`、Triton range loop | 代码直接 | 支持 forward/JVP 语义；Magi backward 未支持需复核训练配置 |
| 10x convergence | 摘要/主实验 | 端到端、混杂 | 不可归因给 mask kernel 单独贡献 |

## 3. 复现价值、局限与对 kernel 设计的启发

- **适用价值**：当 mask 可被少量单调 block range 描述（causal、window、sink、`[clean,noisy]` 的矩形并集）时，优先保留规则并 lower 成 `BlockMask` 或 range-CSR。它比预生成 dense bias 更容易与 fused attention、JVP、FSDP2 和 Ulysses CP 组合。
- **实现代价**：Triton JVP 把 `Q/K/V` 的 tangent 一起带入 kernel，寄存器、HBM reads 与 autotune 复杂度都高于常规 FlashAttention；也要求 FlashAttention 版本、CUDA、MagiAttention/FA4 可用性与 compile cache 同时正确。
- **未验证处**：论文代码 snapshot 未给出针对“Flex BlockMask vs Magi range-CSR vs two-pass KV cache”的等预算 microbenchmark；也没有将 TF-CM、SF-DMD、cache layout、JVP kernel 的贡献完全隔离。当前结论是实现机制核验，不是通用吞吐定律。
- **复现最小闭环**：先用 `blockmask.py` 的 `visualize_attn_mask_spec` 对小 block 验证 TF 图样；再用 `flash_attention_jvp_triton.py` 的 reference JVP test 对比 dense masked attention；最后才接入 Wan2.1 的 packed training。这样能把“mask 错”与“连续时间 loss 不稳定”分离。

**一句话总结**：Causal-rCM 的新意不是任意稀疏 attention，而是把 TF 的非三角 block 可见性同时下沉到 fused primal/JVP attention；对 kernel 工程最有价值的经验是用规则或 range-CSR 表达 mask，避免让 $L^2$ tensor 成为训练图的一部分。
