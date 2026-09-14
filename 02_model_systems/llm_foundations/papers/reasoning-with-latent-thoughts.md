---
tags:
  - paper
  - collection/llm-foundations
  - domain/model-systems
  - status/deep-review
  - topic/reasoning
  - method/looped-transformer
---

# Reasoning with Latent Thoughts: On the Power of Looped Transformers 精读分析

> 本文为 arXiv `2502.17416v1`（ICLR 2025）canonical Paper。PDF/LaTeX 来源、逐图 bbox 与审计记录保存在任务过程区；正式正文只引用本目录下 Git 跟踪资产。

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[LLM Foundations README](../README.md)
> - 上位汇总：[Linear Attention Transformer 演化](../surveys/linear-attention-transformer-evolution.md)
> - 证据资产：`../assets/papers/reasoning-with-latent-thoughts/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

## 修订信息

- 当前文档版本：`1.0.0`；当前修订 ID：`rev-2026-09-14-initial`
- 当前修订时间：`2026-09-14T18:00:00+08:00`；替代版本：`none`

## 论文信息与证据边界

Nikunj Saunshi、Nishanth Dikkala、Zhiyuan Li、Sanjiv Kumar、Sashank J. Reddi；Google Research，Zhiyuan Li 另属 Toyota Technological Institute at Chicago。论文发表于 ICLR 2025。研究问题是：在参数预算有限时，能否通过共享权重的循环执行获得推理所需的有效深度？

OpenReview forum `din0lGfZFd` 在 2026-09-14 官方 API 返回 403，公开评审、meta-review、rebuttal 和 decision 不可独立核验；本文不据此推断审稿意见。论文没有开源训练代码，也没有报告 GPU、wall-clock、能耗、显存峰值或服务吞吐。

## 术语与符号

- **循环 Transformer**：同一个 $k$ 层参数块重复执行 $L$ 次；不是复制 $kL$ 组独立权重。
- **有效深度** $D=kL$：实际执行的层数，不等于参数量。
- **等参数基线** $(k\otimes1)$：与循环模型有相同独立参数量的一次模型。
- **等 FLOPs 基线** $(kL\otimes1)$：深度/FLOPs 相同但独立参数约多 $L$ 倍的模型。
- **潜在思维**：循环内部并行更新的隐藏表示，不等于可读的思维链文本。
- **思维链（CoT）**：每步生成显式中间 token 的推理；本文证明可模拟，不证明实际训练模型自然生成可解释思维。

符号：$f$ 为 $k$ 层共享块；$L$ 为循环次数；$D$ 为有效深度；$G$ 为任务组或参数组（依公式）；$\lambda_{reg}$ 为正则强度；$p$ 为 p-hop 跳数；$\alpha,\beta$ 为深度缩放拟合参数。

## 研究动机与问题—方案闭环

组合推理需要多步变换，但传统加深模型同时复制参数。作者因此把“执行深度”和“独立参数量”分开：循环模型重复同一个块，保留计算步骤而减少参数。本文构造的失败场景是：在 Table 1 的加法任务中，2 层一次模型对 32 个操作数只有 38.8%，2 层循环 6 次为 99.5%；仅增加宽度并不能证明能实现同样的迭代算法。

论文用三类任务检验该主张：3 位数 n-ary addition、p-hop induction、符号 i-GSM；随后在 Pile 上训练约 1B/1.5B 参数的因果语言模型，对比困惑度、closed-book QA（偏记忆）、open-book QA、数学题和 reasoning primitives。成功标准是循环模型接近等 FLOPs 深模型、相对提升推理任务 `% Gap`、准确率随 $D$ 近似按对数增长，并可用正则化迁移该偏置。

核心因果链为：多步推理需求 → 独立加深参数昂贵 → $(k\otimes L)$ 共享块重复 → 合成任务准确率接近等 FLOPs 基线（Table 1/2）→ 语言模型推理任务 `% Gap` 高于记忆任务（Table 3）→ 深度缩放近似 $\log D$（Figure 3）→ 块间余弦正则化改善推理且困惑度近似不变（Table 4）。直接支持限于这些任务和规模；“潜在思维是实测收益根因”和“普遍降低部署成本”仍未验证。

## 方法与公式

![Figure 1：循环架构与基线](../assets/papers/reasoning-with-latent-thoughts/fig1-looping-architecture-caption.png)

一个样本依次经过 $k$ 层块，块输出作为同一块下一轮输入，执行 $L$ 次；训练直接做输入到输出映射，不使用 CoT。middle looping 只循环中间层，首尾层保持独立。

$$
(k\otimes L)=f^{(L)}=f\circ\cdots\circ f,\qquad D=kL.
$$

**解释卡。** 这定义共享块循环及有效深度：输入经同一函数 $L$ 次变换，$k$ 控制独立参数块深度，$L$ 控制重复次数。增大 $L$ 提高计算步骤但不按比例增加参数；$(4\otimes6)$ 与 $(24\otimes1)$ 都执行 24 层，但前者约只有一份 4 层参数。共享参数不保证等价于独立层，优化轨迹仍不同。

$$
\%\,Gap_G=\frac{\operatorname{Avg}_G(k\otimes24/k)-\operatorname{Avg}_G(k\otimes1)}{\operatorname{Avg}_G(24\otimes1)-\operatorname{Avg}_G(k\otimes1)}.
$$

**解释卡。** `% Gap` 衡量循环模型填补浅层到 24 层基线差距的比例；分子是循环增益，分母是深层全部增量。0% 表示没有超出浅层，100% 表示追平，超过 100% 表示超过深层。分母小会放大结果，它不是因果效应或严格上界。

$$
\operatorname{Acc}=\alpha\log(D)+\beta.
$$

**解释卡。** 这是有限深度点上的描述性拟合：深度增加仍有收益但边际递减；$\alpha$ 是深度敏感度，$\beta$ 是截距。Figure 3 报告 reasoning primitives 的 $\alpha_{loop}/\alpha_{base}=1.19$，但无置信区间，不能外推为普适 scaling law。

$$
R_G(k)=\frac{1}{L-k}\sum_{i=0}^{L/k-2}\sum_{j=0}^{k-1}\operatorname{Cosine}(\theta_G^{(ik+j)},\theta_G^{((i+1)k+j)}),\quad
\mathcal L=\mathcal L_{xent}+\lambda_{reg}|\mathcal G|^{-1}\sum_{G\in\mathcal G}R_G(k).
$$

**解释卡。** $R_G$ 比较相邻块对应层的参数方向，$\mathcal L$ 将所有参数组平均相似度加入交叉熵目标；$\lambda_{reg}=0$ 是普通训练，增大它使模型趋向循环。论文报告 $k=4,\lambda=10$ 时块间相似度约 0.98；正文未提供可运行代码，损失符号的最小化方向需结合实现约定理解。

## 实验与主结果

![Table 1：加法与 p-hop](../assets/papers/reasoning-with-latent-thoughts/table1-addition-phop-caption.png)

加法中 $(1\otimes12)$ 在 32 个操作数上 99.6%，一次 1 层为 0.0%；p-hop 的 $(1\otimes6)$ 在 $p=32$ 达 99.5%，一次模型为 49.0%。这支持算法化任务更需要深度而非独立参数。

![Table 3：语言模型结果](../assets/papers/reasoning-with-latent-thoughts/table3-language-model-results-caption.png)

24 层基线困惑度 7.40、数学题 29.3、推理原语 47.5；$(12\otimes2)$ 困惑度 7.90，却数学题 34.3、推理原语 51.2，只有约一半独立参数。循环模型对 open-book QA 的 `% Gap`（56–94%）和数学题（最高 282%）明显高于困惑度/closed-book，说明推理与记忆受不同归纳偏置影响；超过 100% 的 `% Gap` 也说明该指标不是恢复比例上界。

![Figure 3：有效深度缩放](../assets/papers/reasoning-with-latent-thoughts/fig3-effective-depth-scaling-caption.png)

Figure 3 显示 $(4\otimes L)$ 与 $(4L\otimes1)$ 的任务准确率随 $D$ 增加，均可用 $\log D$ 粗略拟合；收益递减，推理原语的循环斜率更高。实验点少且无误差条，结论限于该设置。

![Table 4：循环启发正则化](../assets/papers/reasoning-with-latent-thoughts/table4-regularization-results-caption.png)

$k=4,\lambda=10$ 时数学题从 baseline 的 29.3 升至 36.4，推理原语从 47.5 升至 57.2，困惑度由 7.40 变为 7.38。结果与 Figure 5 的参数相似度检查支持“注入循环偏置”，但缺少完整 $k,\lambda$ 网格和独立优化对照，不能做严格组件归因。

## 理论、CoT 与局限

Theorem 5.1 证明有限群合成可由 1 层循环 $\lceil\log_2 n\rceil$ 次完成；Corollary 5.3 给出 p-hop 用 $\lfloor\log_2p\rfloor+2$ 次循环；Theorem 5.2 将有限个不同层的 Transformer 模拟为循环块；Theorem 5.4 在固定输入长度、dummy tokens、额外维度和 mask 条件下模拟多步 CoT。它们是存在性/构造性结果，复杂度转移到隐藏维度、精度和控制 mask，并不证明实验模型真实形成可解释潜在思维。

![Figure 4：CoT 与潜在思维](../assets/papers/reasoning-with-latent-thoughts/fig4-cot-latent-thoughts-caption.png)

局限包括：推理任务覆盖有限；规模只到 1B 级；没有真实硬件成本数据；正则化收益未做充分拆分；OpenReview 评审不可访问；未验证多模态、常识、长程规划或自适应循环。最稳妥的结论是：循环共享能在若干算法化任务中以较少独立参数提供有效深度，并在固定规模语言模型上偏向上下文推理；“等同 CoT”与“普遍更快/更省服务成本”仍是待验证假设。
