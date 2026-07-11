# VMoBA 精读：动态 block 选择不是自定义 kernel，而是 selector + varlen FlashAttention

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：`../assets/papers/vmoba/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

> 资料状态：已核对 arXiv PDF（13 页）与官方 `KlingAIResearch/VMoBA` snapshot，commit `48aaccd4f14c5adb7db961058bfbb2113e392003`。它是 2025 年 arXiv work，代码为单文件参考实现；论文的完整 Video DiT 训练配置、训练入口和精确 runtime profile 未在该仓库提供，因此实现层结论必须区分“论文机制”和“reference kernel path”。

## 0. 资料、图示与符号

| 用途 | 一手来源 | 关键阅读点 |
|---|---|---|
| 三阶段机制 | PDF Fig. 2（p.4） | partition -> gate/select -> selected block attention |
| 视频局部性证据 | PDF Fig. 3（p.4） | 不同层表现为 temporal / spatial / 3D neighbor |
| 主实验与消融 | PDF Table 1--3、Fig. 6--7 | 区分 FLOPs 降低和真实 latency；检查 selector 消融 |
| 实际 kernel 路径 | `src/vmoba.py:339-727` | gate tensor、`nonzero`、packing、FlashAttention varlen、LSE merge |

![论文 Fig. 2：VMoBA 三级流水线（PDF 第 4 页，后续应裁出图及完整 caption）](../assets/papers/vmoba/fig2_vmoba_pipeline_caption.png)

图 1 中蓝色的 selected block 是针对 query-head/block pair 的选择结果；它不表示一个常驻的 token-token sparse mask。

| 符号 | 含义 | 作用域 | 证据 |
|---|---|---|---|
| $s$ | sequence token 数 | 一个 video sample | PDF §3.1 |
| $d$ | hidden/head dimension（论文复杂度中省略 head） | attention | PDF §3.1 |
| $s_b$ | 一个 key block 的 token 数 | block | PDF §3.1 |
| $N_b$ | key block 数，约 $s/s_b$ | layer | PDF §3.1 |
| $B$ | 对 block 内 K 求均值得到的 block representation | layer/head | PDF Eq. (1)--(2) |
| $S_i=q_i B_i^\top$ | head $i$ 的 query-to-block similarity | $[s,N_b]$ | PDF Eq. (3) |
| $M_i$ / `gate_mask` | 被选 query-block 对 | 每 layer/step | PDF Eq. (3)--(4)；`vmoba.py` |
| $\tau$ | 累积 similarity threshold | head/selection | PDF Eq. (4) |

## 1. 问题、算法与 mask 语义

### 1.1 为什么普通 MoBA 不适合 video DiT

论文将先前 MoBA 的 1D flatten block 切分视为问题：相邻的时间、空间和时空 token 在 flatten 后可能被拆到不同块，导致 block mean 不再代表实际局部性；同时固定 top-$k$ 给每个 query 分配同样 budget，忽略不同 head/query 的相似度集中度。作者的实证动机是 Fig. 3：full-attention DiT 的不同层分别偏向 1D temporal、2D spatial、3D spatio-temporal 邻域。

VMoBA 因而由三部分组成：

1. **Layer-wise recurrent partition**：按层号循环应用 temporal (1D)、spatial (2D)、spatio-temporal (3D) 切分。对 $K\in\mathbb R^{T\times H\times W}$ 重排为 $K'$，再计算每个块均值 $B=\operatorname{mean}(K')$（PDF Eq. 1--2）。这是一种静态、geometry-driven grouping，不是数据驱动 routing。
2. **Global block selection**：对每个 head 计算 $S_i=q_iB_i^\top$，从该 head 的所有 query-block pair 统一挑高分 pair，而不是每个 query 都用固定 block 数：
   $$M_i=\operatorname{TopkMask}(q_iB_i^\top,k).$$
3. **Threshold-based selection**：将 score 排序并选择最小 $k$，使累计归一化 similarity 达阈值 $\tau$：
   $$k=\min\left\{k'\mid\sum_{j=1}^{k'}\operatorname{Sorted}(\hat S_j)\ge\tau\right\}.$$

最终每个 query 只和其选中 block 的原始 K/V 做 attention。这里的“mask”是一个**动态产生的 query-to-block gate**；真正的 KV 可见性粒度由 block 决定。

### 1.2 复杂度和质量取舍

论文给出的主要 work 可分为 selector 与 selected attention：

$$
O(sdN_b)=O\left(\frac{s^2d}{s_b}\right),\qquad
O(sk_{\mathrm{avg}}s_bd),
$$

合计为

$$
O\left(sd\left(\frac{s}{s_b}+k_{\mathrm{avg}}s_b\right)\right).
$$

因此 block 太小会让 selector 的 $s^2/s_b$ 项变大，block 太大则让 selected K/V attention 粗糙且 $k_{\mathrm{avg}}s_b$ 增大。它不是像 LVSA 一样将每 query 的 frame budget 固定为常数；当 head score 分布稀疏度不同，$k_{\mathrm{avg}}$ 会随数据和 $\tau$ 变化。

## 2. 实现分解：没有传入 sparse mask 的 FlashAttention

### 2.1 脚本侧的 selector 与中间表示

官方实现 `moba_attn_varlen` 中，`kv=torch.stack((k,v))` 后按 `cu_seqlens` 和 `moba_chunk_size` 切 chunk（`vmoba.py:529-573`）。每个 chunk 的 K 均值形成 `key_gate_weight[C,H,D]`，与 `q[S,H,D]` 相乘得到

$$
\texttt{gate}\in\mathbb R^{C\times H\times S}.
$$

这不是 $S\times S$ token attention matrix，但仍是一个**dense selector score tensor**，内存约为 $C\times H\times S$（fp32，因为代码把 K/Q 转为 `.float()`，`:587-595`）。`topk` 或 `_select_threshold_*` 产生同形状 bool `gate_mask`（`:600-663`），随后 `nonzero` 把 true 条目压缩成索引（`:674-727`）。

因此回答“mask 是预生成还是 kernel 在线生成”时，VMoBA 的正确分类是：

| 位置 | 做什么 | 表达 |
|---|---|---|
| 模型脚本/GPU tensor op | block mean、dense gate、sort/top-k/threshold | $[C,H,S]$ score/bool，短暂存在 device 上 |
| packing | 按 selected pair gather Q、block K/V，生成 `moba_cu_seqlen_q/kv` 与 scatter indices | index list + varlen offsets |
| FlashAttention | 对每一条 packed varlen segment 做标准 non-causal attention | **没有**通用 `attn_mask` 参数，也没有 CSR blockmask |
| merge | 通过 LSE 的 stable reduction 合并 self branch 和 selected-block branch | `moba_q_sh_indices` + LSE |

它不会把 $[S,S]$ 完整 mask 传给 FlashAttention；稀疏性在 **gather/pack 后的序列边界**中表达。代价是 selector 和 packing 成为控制面瓶颈。

### 2.2 FlashAttention 为什么要有两个 branch

`MixedAttention.forward` 先对原始 chunk 做 self-attention，再对选中 block 的 packed Q/K/V 调用 `_flash_attn_varlen_forward`（`vmoba.py:339-424`）。二者分别产生 LSE，再以 max/LSE reduction 做等价 softmax 归一化合并，避免简单相加导致概率质量错误。backward 对两 branch 分别调用 `_flash_attn_varlen_backward`（`:431-525`）。

这意味着 VMoBA 的加速不是一个“支持 arbitrary sparse mask 的 FlashAttention kernel”：FlashAttention 各 call 都是合法的 dense varlen attention；稀疏结构由上游重排和下游 LSE merge 实现。对 kernel 开发者，这是较容易落地、但会牺牲 gather locality、sort、index launch 与小 segment occupancy 的路线。

代码中 `process_moba_input` / `process_moba_output`（`:730-780`）承担 1-2-3D partition 对数据 layout 的转换；release README 也明确这是单文件 reference implementation。固定 commit 可追溯链接：[`vmoba.py`](https://github.com/KlingAIResearch/VMoBA/blob/48aaccd4f14c5adb7db961058bfbb2113e392003/src/vmoba.py)。

### 2.3 一个必须记录的复现差异

论文文字强调 per-head global selection，而实现公开了 `query_head`、`block`、`overall`、`head_global` 多种 threshold mode。函数默认 `threshold_type='query_head'`（`vmoba.py:529-539`），而 paper-level global definition 更接近 `head_global`/`overall` 的语义；本地 snapshot 未包含论文实验训练脚本来锁定实际配置。故不能仅根据默认代码宣称它精确复现论文的 global selector。复现时必须记录 `select_mode`、`threshold_type`、`simsum_threshold`、chunk size、layout cycle 与 random seed。

## 3. 实验证据、系统风险与可复现实验

| 技术点 | 论文支撑 | 控制是否直接 | 判断 |
|---|---|---|---|
| 1-2-3D recurrent partition | Table 3a、Fig. 3 | 有去除各 partition 的消融 | 支持其相对单一切分的必要性，仍受训练预算限制 |
| global + threshold selection | Table 3b--3c、Fig. 4--5 | 有选择规则/阈值消融 | 对质量有直接证据；不同长度下 selector cost 未完全隔离 |
| FLOPs 与 latency | Table 1、README 55K-token benchmark | 有端到端对比 | 论文也承认短 sequence 加速有限；FLOPs 不等于 latency |
| training-free 可迁移 | Table 1 | 在特定预训练模型上测试 | 不等于所有 DiT 或所有 resolution 都稳定 |

论文主张在长序列上比 full attention/MoBA 更平衡质量与效率；但它同时在 §4 和补充材料承认短序列时当前 FlashAttention-based 实现可能比 full attention 慢。根因正是 selector 的 `topk/sort/nonzero`、K/V gather、varlen segment 及 LSE merge：它们的算术量不大，却可能 memory-bound、产生不连续 HBM 访问并降低 tensor-core tile 利用率。

### 建议的复现实验

1. 用同一 Q/K/V 测 `gate_mask` 后的 varlen + LSE merge 与基准 naive selected-block attention，先验证数值等价和 gradient。
2. 固定 $s$，扫描 $s_b$、$\tau$ 和 selection mode，分别计时 `gate`、sort/threshold、gather/pack、FA kernel、merge；只报总 latency 会掩盖 selector 成本。
3. 用 33K、46K、55K+ token 分层报告：理论 FLOPs、peak memory、kernel time、effective HBM bandwidth 和 end-to-end time。
4. 对照论文 selector 语义，明确每个 run 使用的是 `head_global` 还是 default `query_head`，否则“global selection”是不可审计的标签。

**一句话总结**：VMoBA 的创新在于视频几何感知的 block 切分和动态预算分配，但其稀疏 mask 不是交给 kernel 的 CSR/DSL，而是在 GPU 脚本侧算出 $[C,H,S]$ gate 后 lowering 为 varlen packed calls；它降低了 token-token attention work，也把性能成败转移给 selector、packing 与 memory locality。
