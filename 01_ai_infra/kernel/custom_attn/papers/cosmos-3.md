# Cosmos 3 精读：把非典型双流 Mask 分解为两次标准 varlen Attention

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：`../../../../02_model_systems/multimodal_generation/assets/papers/cosmos-3/`
> - 相关文档：[Cosmos 3 完整精读](../../../../02_model_systems/multimodal_generation/papers/cosmos-3.md)，[Figure inventory](../evidence/figure-inventory.md)

> 资料状态：本 survey folder 未保留 Cosmos 3 PDF/官方源码 snapshot；本分析基于知识库中已完成的一手材料索引 [`Cosmos3.md`](../../../../02_model_systems/multimodal_generation/papers/cosmos-3.md)（记录 arXiv `2606.02800`、LaTeX source 与 `NVIDIA/cosmos-framework` commit `3a5314b7dd3c3abb84df71627ecb10ef8423dbdd`）。因此本文能核验该本地精读记录中的 source/code line reference，但本轮没有重新执行 Cosmos code。最终交付应将 PDF 原图和源码 snapshot 一并归档，以消除该证据边界。

## 0. 资料、图示与关键名词

![Cosmos 3 two-way flat attention（知识库基于论文/实现整理的机制图）](../../../../02_model_systems/multimodal_generation/assets/papers/cosmos-3/two-way-attention-infra.png)

上图最重要的不是模型画成两座塔，而是可见性方向：Reasoner/AR query 只读本 sample 的 AR 历史；Generator/diffusion query 可读同 sample 的 AR + Generator tokens；AR 不会读回 noisy diffusion tokens。

| 术语/符号 | 本文含义 | 不应误读为 | 证据 |
|---|---|---|---|
| $R_i$ | 第 $i$ 个 sample 的 reasoner/AR subsequence（text、理解 vision 等） | 所有样本共享一段 global prompt | 本地精读 §Q4、`transformer.py:74` 索引 |
| $G_i$ | 第 $i$ 个 sample 的 generator/diffusion subsequence（vision/audio/action latent） | 只能看自身 generator token | 同上 |
| MoT | 每层 reasoner/generator 有独立 norm/attention projection/MLP 路径 | token-MoE 的动态 expert router | 本地精读 §Q4 |
| two-way flat attention | 两次 variable-length attention call 的 implementation lowering | 一个 dense `[L,L]` custom attention bias | 本地精读 infrastructure §3 |
| `cu_seqlens` | packed varlen segment offset | token-token mask | `two_way_attention_infra.png` / code 索引 |

另一个建议在最终报告嵌入的论文源图是 [`mot_architecture.png`](../../../../02_model_systems/multimodal_generation/assets/papers/cosmos-3/mot-architecture.png)：它解释参数路径分离；本图解释 attention 可见性与 kernel lowering。两图不能互相替代。

## 1. 统一多模态模型究竟要解决什么冲突

Cosmos 3 将语言/视觉理解和 image/video/audio/action 的 diffusion generation 放进同一 backbone。直接把所有 token 用一个 causal 或 full-attention mask 处理会遇到相反约束：

- Reasoning/understanding 需要严格 AR causal history，防止未来或 noisy generation target 污染语言表示；
- diffusion generator 需要在同一 sample 内双向读取文本、条件视觉、其他 noisy latents，才能进行条件去噪与时空一致性；
- 如果两部分共用同一层参数，训练目标和数值分布也会互相干扰。

MoT 通过两个参数路径处理前两项冲突，再用非对称 attention 处理第三项。对 packed batch

$$
[R_0,G_0,R_1,G_1,\ldots,R_n,G_n],
$$

第 $i$ 个 sample 的 attention 可以写成

$$
O_{R_i}=\operatorname{CausalAttn}(Q_{R_i},K_{R_i},V_{R_i}),
$$

$$
O_{G_i}=\operatorname{FullAttn}\big(Q_{G_i},[K_{R_i};K_{G_i}],[V_{R_i};V_{G_i}]\big).
$$

第二式的 “full” 只在本 sample segment 内成立，**不包含** $R_j,G_j\;(j\ne i)$。这正是文本中“diffusion subsequence interacts with AR subsequence”最容易被误读的地方：信息方向是 $R\rightarrow G$ 的条件读取，而不是 $R\leftrightarrow G$ 双向读。

## 2. Mask 到 kernel 的 lowering：拆解优于通用 Flex mask

### 2.1 表达方式

| 语义需求 | 低层调用 | mask 表达 | dense mask 是否存在 |
|---|---|---|---|
| AR/Reasoner causal | `varlen SDPA(Q_R,K_R,V_R, causal=True)` | `cu_seqlens_R` + `causal=True` | 否 |
| Generator full-attend 同 sample $[R_i,G_i]$ | `varlen SDPA(Q_G,K_{[R;G]},V_{[R;G]}, causal=False)` | 两套 Q/KV `cu_seqlens` | 否 |
| 跨 sample 隔离 | varlen segment boundary | offsets 保证不同 sample 不在同一 attention segment | 否 |

常见的表达是一次 FlexAttention `mask_mod`，对每个 $(q,k)$ 判断 “同 sample 且按 token mode 可读”。Cosmos 3 的关键工程选择是**不让 kernel 反复解释这个一般 predicate**：模型层先按 semantic route 拆 sequence，再发两条普通、强优化的 causal/full varlen call。对于由少数矩形块构成、可分解的 mask，这通常有更好的 tile regularity，也避免 BlockMask compilation 和 block padding。

本地 source audit 指向：

- `sequence_packing.py:77,127`：根据 `attn_modes` 建立 causal/full indices 与 offsets；
- `sequence_packing.py:1295`：pack text/vision/action/sound，并维护 full-attention segment；
- `transformer.py:74-118`：`CosmosAttnProcessor3_0` 分别执行 causal 和 full path；
- `transformer.py:333-578`：`PackedAttentionMoT` 的 generator 独立 Q/K/V/out projection 与 MoT decoder layer。

固定 commit 链接（需在最终归档时下载 snapshot 再次校验）：[`transformer.py`](https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py)、[`sequence_packing.py`](https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py)。

### 2.2 对“稀疏 mask/CPU host”的具体回答

Cosmos 3 的 two-way flat attention **不是稀疏 attention**：每个 $G_i$ 仍对 $[R_i,G_i]$ 做 dense full attention；它节省的是通用 arbitrary-mask 路径中的无效跨段/padding-equivalent work。metadata 是每段的 begin/end offset，空间为 $O(n_{\mathrm{segments}})$，远小于 $O(L^2)$。

现有材料没有给出“CPU 生成 offsets 后 GPU kernel 从 host 读取”的证据。更严谨的表述是：kernel 接收的是标准 varlen lengths/offsets，具体由 packing runtime 在何处创建和迁移需以归档源码/trace 验证；不能把 LVSA 的 host-side CSR planner 套用到 Cosmos。由于 offsets 极小，即使由 host 构造并 H2D，传输也不是核心瓶颈；真正的数据量仍在 Q/K/V 及跨 CP 的 all-to-all。

### 2.3 backend 与分布式含义

本地论文审计记录：H100/H200 走 FlashAttention-3，GB200/Blackwell 走 NATTEN/CUTLASS 路径；相对 FlexAttention baseline，Cosmos3-Nano 端到端训练 throughput 报告 `+22%`。这个百分比是 attention lowering、packing、编译和整训练栈的合成效果，不能直接解读为某一个 kernel 的 microbenchmark。

长 context 训练使用 HSDP + Ulysses CP：sequence-shard 在 attention 前交换为 head-shard，attention 后再交换回来。two-way split 要与每个 sample 的 `cu_seqlens` 保持一致；否则 causal/full 两 branch 的 segment 边界和 mRoPE position 会错位。对于系统设计，正确的优先级是：**先保证 semantic segmentation 正确，再做 varlen packing，再选择 FA3/NATTEN backend**。

## 3. 证据边界、局限与实现启发

| 技术声称 | 支撑来源 | 证据强度 | 结论 |
|---|---|---|---|
| AR 不被 diffusion token 反向污染 | 模型段落、`CosmosAttnProcessor3_0` 索引、two-way 图 | 机制/代码索引 | 支持；需要 source snapshot 重验具体版本 |
| Generator 可读 AR + Generator | 同上 | 机制/代码索引 | 支持；相互作用为单向 $R\rightarrow G$ |
| two-way flat 比 FlexAttention 高 22% throughput | infrastructure section/source index | 端到端结果 | 支持总体收益，不可分配到单 kernel |
| Hopper/Blackwell backend 分工 | infrastructure section/source index | 配置/实现声明 | 需在可运行环境复验版本与 hardware guard |

局限与可迁移性：

1. $G_i$ 内仍是 dense full attention，随 video/audio/action token 数增长仍有平方瓶颈；它解决的是**结构化异质 mask 的 lowering**，并不是长视频稀疏化方案。
2. MoT 有两套 pathway 参数；attention 计算减少不代表模型容量、optimizer state、activation 都降低。
3. 该方案依赖 mask 能被分解为少数、无交叉依赖的 sequence groups。窗口、全局 anchor、动态 top-k 或任意 pairwise routing 则无法只靠两次 varlen call 表达，应转向 BlockMask/CSR/runtime planner。
4. 当前 survey artifacts 缺少 Cosmos PDF/source-code copy，图片与关键实现索引来自本地深读，交付前必须补齐 source artifact 与 commit-level recheck。

**一句话总结**：Cosmos 3 为统一多模态模型提出的不是“稀疏 mask”，而是一种可分解的非对称可见性：在模型脚本侧把 reasoner/generator 按语义拆开，用两次标准 causal/full varlen attention 代替一张任意 mask，从而把正确性和 kernel 效率同时做成可审计的 sequence packing 问题。
