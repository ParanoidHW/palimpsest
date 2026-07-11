# FrameDiT 精读：不是 sparse mask，而是把时序全连接压缩到帧级矩阵 attention

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：`../assets/papers/framedit/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

## 来源、代码与图示索引

- 论文：*FrameDiT: Diffusion Transformer with Matrix Attention for Efficient Video Generation*，本地 `paper.pdf` 共 16 页。
- 代码：`code/FrameDiT`，remote `https://github.com/minhkhoale/FrameDiT.git`，本地 commit `359bd123bf077ffd197d3e059422f4bf309bc050`。
- 推荐嵌入图：**Fig. 1（PDF p. 2）** 比较 local / global / hybrid block；**Fig. 3（p. 5）** 是时长从 16 到 128 帧的 FVD、FLOPs、latency、memory 缩放；**Fig. 4（p. 8）** 是参数规模-质量-计算量关系。Fig. 2（p. 4）只是定性视频帧对比，不应用作 kernel 机制图。

## 核心问题与路线定位

视频 DiT 常在两个极端之间选择：

- **Local Factorized temporal attention**：每个空间位置只跨帧看“同一坐标”的 token，计算约为 \(O(T^2N+TN^2)\)，但物体发生位移时，同一对象不再落在同一空间位置，跨帧关联需由多层间接传递。
- **Full 3D attention**：所有时空 token 两两连接，能建模大运动，但时空长度为 \(TN\) 时 attention 主项为 \(O(T^2N^2)\)，长视频/高分辨率不可承受。

FrameDiT 选择第三条路：**不是从 \(TN\times TN\) dense mask 中挖稀疏块，也不训练 selector；而是先把每帧 \(N\) 个 token 映射为低行数的矩阵表示，再只在 \(T\) 帧之间做 dense attention。** 因而它是本调研中很重要的“非典型 attention”反例：减少复杂度的关键是改变 representation/layout，而不是向 kernel 传一个 custom sparse mask。

## 符号与算法

| 符号 | 含义 | 证据 |
|---|---|---|
| \(z^t\in\mathbb{R}^{N\times D}\) | 第 \(t\) 帧的 token-by-channel 矩阵 | PDF p. 3, Sec. 3.1 |
| \(T,N,D\) | 帧数、每帧 token 数、特征维度 | 同上 |
| \(q^t,k^t\in\mathbb{R}^{N_{qk}\times D_{qk}}\) | 被 MatrixLinear 压缩后的帧级 Q/K 矩阵 | p. 3, Eq. (6) |
| \(v^t\in\mathbb{R}^{N_v\times D_v}\) | 帧级 V 矩阵 | p. 3, Eq. (6) |
| \(S\in\mathbb{R}^{T\times T}\) | 所有帧对的相似度矩阵 | p. 3, Eq. (7)-(8) |

对每帧，先进行双侧线性变换：

\[
q^t=U_q^\top z^tW_q+B_q,\quad
k^t=U_k^\top z^tW_k+B_k,\quad
v^t=U_v^\top z^tW_v+B_v.
\]

其中 \(U\) 把 token 行从 \(N\) 合成为 \(N_{qk}\) 或 \(N_v\)，\(W\) 再投影特征列。帧间 score 取矩阵 Frobenius 内积：

\[
S^{t,t'}=\frac{\langle q^t,k^{t'}\rangle_F}{\sqrt{N_{qk}D_{qk}}},\qquad
u=\operatorname{Softmax}(S)v.
\]

因此每个帧对依然允许全连接，但连接对象已经是压缩后的帧表示；softmax 的有效 sequence axis 是 \(T\)，不是 \(TN\)。论文给出 Global 版本复杂度 \(O(TN^2+T^2N_{qk})\)，Hybrid 版本为 \(O(TN^2+T^2N+T^2N_{qk})\)（PDF p. 4）。

- **FrameDiT-G**：用 Matrix Attention 取代 local temporal block，隔离验证全局帧关系。
- **FrameDiT-H**：保留 local temporal branch 获取细粒度运动，和 global Matrix branch 并行后 concat + MLP 融合（p. 4, Eq. (10)）。论文还报告 softmax gate 容易饱和，故改用 concat；移除 local branch 会得到类似独立图片的帧序列（p. 5）。

## 实际实现与 kernel 数据流核验

代码比论文更明确地说明了它不是 custom sparse mask 路线：

```text
x: [B, T, N, D]
  -> MatrixLinear(U^T x W) 产生 Q/K/V
  -> 重排为 [B, num_row_heads*num_col_heads, T, compressed_frame_dim]
  -> dense SDP / FlashAttention 沿 T 帧维计算
  -> 重排回 [B, T, N, D]
  -> (Hybrid) 与 local temporal attention 输出 concat -> Linear
```

具体证据：

- `models/framedit_h_t2v.py:141-228` 的 `MatrixAttentionProcessor.__call__` 先调用三次 `MatrixLinear`，再把矩阵分块/heads 重排为以 `T` 为 sequence length 的 Q/K/V。
- `:184-205` 在 `attention_mode == 'flash'` 时调用 `torch.nn.functional.scaled_dot_product_attention(query, key, value)`；`flash_v2` 分支调用 `flash_attn_func(..., causal=False)`。二者都是**紧凑、连续的 dense QKV 输入**，没有 sparse index 参数。
- `:329-470` 的 `FusedMatrixAttention` 明确把 local branch 与 global branch 分开，并在 `concat` 模式用 `torch.cat` + `nn.Linear` 融合。
- `MatrixAttentionProcessor` 虽接收 `attention_mask` 形参，但没有将它传给 SDP 或用于 score；因此 Matrix Attention 的公开实现是 all-to-all、non-causal 帧 attention，而非 predicate/block-mask attention。

现有 Latte 路径中的 `models/latte_t2v.py:761-779` 会把 2D `attention_mask` 转为 `(1-mask)*-10000` 的 additive bias 并扩展维度。这只是底座/交叉 attention 的 **dense/broadcast bias** 兼容逻辑，不能当作 FrameDiT 对长视频稀疏 mask 的证据。特别地，它既没有 block list，也没有跳过 QK tile；放到 \(N\times N\) pair mask 上仍会有 dense 内存和计算问题。

| 问题 | FrameDiT 的答案 |
|---|---|
| custom mask 如何表达？ | 核心 Matrix Attention **没有 custom mask**；所有帧彼此可见，`causal=False`。|
| 是稀疏表达还是 online kernel predicate？ | 两者都不是。它用 learned matrix projection 缩短有效 temporal sequence，随后跑 dense kernel。|
| 长序列如何给 kernel？ | 给 `[B, heads, T, compressed_frame_dim]` 的连续 QKV，而不是给 host 生成的 \(TN\times TN\) mask。|
| CPU/host 是否生成 metadata？ | 论文与代码中没有 selector/index/mask metadata，故没有这条数据路径。|

## 结果与证据矩阵

| 主张 | 证据 | 判读 |
|---|---|---|
| 帧级压缩可随帧数扩展 | Fig. 3（p. 5）比较 16-128 帧的 FLOPs、latency、peak memory | 直接趋势证据；图中不是固定硬件微基准 |
| Hybrid 比纯 global 更适合视频一致性 | p. 5 的“移除 local 会像独立帧”消融描述；Table 2/3（p. 7-8） | 有架构比较，但文本中的独立帧结论偏定性 |
| \(N_{qk}\) 是质量-计算 knob | Table 5（p. 8）：\(N_{qk}\) 增大时 FVD/FVMD 改善、GFLOPs 小幅增加 | 直接消融，局限于 Taichi 128x128 |
| T2V 质量增益 | Table 3（p. 8）：FrameDiT-H 总分 79.12，Latte 77.29 | 训练数据/新增 314M 模块等仍是混杂因素；论文说明原 Latte 参数冻结有助于归因 |

## 局限与对 custom-attn 设计的启示

- **不是通用稀疏 attention 的实现例。** 将它放入调研的价值在于说明：当多模态结构允许将大量 token 先聚合为状态/帧对象时，压缩 representation 往往比表达一个不规则 mask 更易获得 FlashAttention 级吞吐。
- **空间 attention 仍可能主导。** 论文复杂度中 \(TN^2\) 没有消失，只有全 3D 项被避免；超高分辨率时这个分支仍是主要成本（PDF p. 4）。
- **全帧 dense attention仍有 \(T^2\) 项。** 视频足够长时，\(T^2N_{qk}\) 会再次成为瓶颈，可能需要和 block/local memory/paged KV 结合；论文没有提出这种扩展。
- **数据类型、Flash kernel 细节未报告。** 代码提供 SDP/FlashAttention 路径，但没有论文级 kernel benchmark、tile 配置或 bandwidth utilization；不能把架构 FLOPs 下降直接等价为某一 kernel 的实测吞吐提升。
- **对落地的建议。** 对具有自然 group（frame、image region、audio chunk、memory slot）的统一多模态模型，先评估“group-level dense attention + 组内局部路径”是否足够；只有 group 数仍很大或可见性真正不规则时，再进入 BlockMask/CSR/predicate kernel 的设计空间。
