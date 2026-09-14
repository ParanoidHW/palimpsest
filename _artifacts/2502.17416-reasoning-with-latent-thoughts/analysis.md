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

> 资料状态：依据 arXiv `2502.17416v1`（2025-02-24）官方 PDF 与 LaTeX 源码归档；未找到开源实现。Figure/Table 均从 PDF 页面紧裁剪，保留完整 caption。OpenReview forum `din0lGfZFd` 在 2026-09-14 访问返回 403，评审内容不可核验。

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[LLM Foundations README](../../02_model_systems/llm_foundations/README.md)
> - 上位汇总：[Linear Attention Transformer 演化](../surveys/linear-attention-transformer-evolution.md)
> - 证据资产：`../assets/papers/reasoning-with-latent-thoughts/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

## 修订信息

- 当前文档版本：`1.0.1`
- 当前修订 ID：`rev-2026-09-15-render-qa`
- 当前修订时间：`2026-09-15T00:05:00+08:00`
- 替代版本：`rev-2026-09-14-initial / 1.0.0 / bfbdb1712c272da9bc2a105de77db5898a5571190e15078b0cc9be0aaace1c6e`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 变更摘要 | 原因 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|
| rev-2026-09-14-initial | 1.0.0 | 2026-09-14 | Codex | initial | none | 新建 standalone Paper | 用户任务 | arXiv v1 PDF/source；验证脚本 | none |
| rev-2026-09-15-render-qa | 1.0.1 | 2026-09-15T00:05:00+08:00 | Codex | evidence-update | rev-2026-09-14-initial / 1.0.0 / bfbdb1712c272da9bc2a105de77db5898a5571190e15078b0cc9be0aaace1c6e | 补 Pandoc 3.8 + Chromium 渲染 QA | 解除渲染门禁 | canonical Paper；review checklist | Pandoc 自包含 HTML、6 images、49 MathML nodes、1440×1200 screenshot | none |

## 0. 资料与配图索引

- 论文：`_artifacts/2502.17416-reasoning-with-latent-thoughts/paper.pdf`（正式文档不引用该路径）
- 源码：`_artifacts/2502.17416-reasoning-with-latent-thoughts/source.tar`
- 版本：arXiv `2502.17416v1`，Submitted 2024-10-01，公布 2025-02-24；ICLR 2025 conference paper。
- OpenReview：forum `din0lGfZFd`，访问状态见 `openreview_reviews.md`。
- 图表完整记录：`_artifacts/2502.17416-reasoning-with-latent-thoughts/figure_inventory.md`。
- AI 生成分析示意图：不适用。原 Figure 1 已展示输入、共享块、循环次数、等参数/等 FLOPs 基线和 middle looping，满足算法总览要求。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| looped Transformer（循环 Transformer） | 同一个 $k$ 层参数块在输入上重复执行 $L$ 次 | looping | 不是新增 $kL$ 组独立权重 | §2、Fig.1 |
| effective depth（有效深度） | 实际执行的层数 $D=kL$ | depth | 不等于参数量 | §3.4 Eq.(2) |
| iso-param | 与循环模型有相同独立参数量的 $k$ 层一次模型 | parameter-matched | 不保证相同 FLOPs | Fig.1、Table 3 |
| iso-FLOP | 与循环模型执行深度/FLOPs 相同的 $kL$ 层非循环模型 | compute-matched | 参数量约为循环模型 $L$ 倍 | Fig.1、Table 3 |
| latent thoughts（潜在思维） | 循环内部并行更新的隐藏表示，不显式输出 token | hidden intermediate states | 不等于可读的 CoT 文本 | §3.4、Fig.4、Theorem 5.4 |
| CoT（chain of thought，思维链） | 每一步生成一个显式中间 token 再继续推理 | scratchpad | 本文只证明可模拟，不证明训练时自动出现可读思维 | §3.4、§5.4 |
| reasoning primitives（推理原语） | 只测上下文推理、尽量排除记忆的合成任务 | — | 不代表全部真实推理 | Table 3 |
| middle looping（中部循环） | 首尾层独立，仅循环中间层 | — | 不同于整网循环 | §3.3、Fig.1 |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/索引 | 单位/取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|
| $f$ | $k$ 层 Transformer 函数 | 作者定义 | 一个共享块 | — | §2 | 非单层函数 |
| $k$ | 块内层数 | 超参数 | 模型结构 | 正整数 | §2 | 与循环次数混淆 |
| $L$ | 循环次数 | 超参数 | 推理/训练执行 | 正整数 | §2、Def.5.2 | 理论中也表示层数，按上下文区分 |
| $D$ | 有效深度，$D=kL$ | 派生量 | 缩放实验 | 层数 | §3.4 | 不表示参数量 |
| $operatorname{Avg}_G$ | 任务组 $G$ 的平均准确率 | 指标 | Table 3 | 百分比 | Eq.(1) | 不是单任务分数 |
| $alpha,eta$ | 缩放式斜率与截距 | 拟合参数 | Eq.(2) | — | §3.4 | $eta$ 不是训练写入率 |
| $lambda_{m reg}$ | 循环正则强度 | 超参数 | Eq.(4) | 非负标量 | §4 | 越大越接近共享权重 |
| $R_G(k)$ | 参数组 $G$ 在相邻块对应层之间的余弦相似度平均 | 损失项 | Eq.(3) | — | §4 | 论文把相似度直接加到损失，符号方向需结合实现理解 |
| $p$ | p-hop 任务的跳数 | 难度参数 | Table 1 | 正整数 | §2.1 | 不是概率 |

## 1. 论文基本信息

- 标题：*Reasoning with Latent Thoughts: On the Power of Looped Transformers*
- 署名类型：个人作者；作者顺序为 Nikunj Saunshi、Nishanth Dikkala、Zhiyuan Li、Sanjiv Kumar、Sashank J. Reddi。
- 第一作者及机构：Nikunj Saunshi，Google Research；role basis 为 `first listed; no equal-contribution marker`，证据为 `PDF title page`。共同一作：未标示。
- 通讯作者：未标示；邮箱仅列作者组邮箱，不能据此推断通讯作者。
- 其余作者机构：Google Research；Zhiyuan Li 另属 Toyota Technological Institute at Chicago（标记 2）。全局证据为 `PDF title page author and affiliation markers`。
- venue：ICLR 2025；论文页明确写 “Published as a conference paper at ICLR 2025”。
- 研究领域：语言模型结构、深度与推理归因。
- 核心问题：在参数预算有限时，能否通过共享权重的循环执行获得推理所需的有效深度？
- 研究目标：比较循环模型与等参数/等 FLOPs 非循环模型，并检查语言模型、理论表达力及正则化迁移。
- 约束：循环块结构固定；语言模型实验约 1B/1.5B 参数、250B Pile tokens；推理任务只覆盖选定 benchmark。

## 2. 研究动机与问题—方案闭环

### 2.1 出发点与背景痛点

作者明确指出：既有 scaling law 常把参数量视为主要因素，但组合推理需要多步变换，深度可能比参数数量更关键。若每增加一步深度都复制一套权重，参数和存储随深度增长；循环 Transformer 让同一块函数反复作用，从而把“可执行深度”与“独立参数量”分离。本文的重建是：问题不是深度不够，而是扩大深度的成本被默认绑定到参数量。

### 2.2 现有方案为何不够

| 现有做法 | 可观察失败 | 具体场景 | 根因/忽略变量 | 为什么简单修补不够 | 证据 |
|---|---|---|---|---|---|
| 只增加独立层 | 小模型在多步组合任务上迅速掉点 | 本文加法实验中，2 层模型对 32 个三位数仅 38.8%，而 2 层循环 6 次为 99.5%；1 层一次几乎为 0%，循环 12 次达 99.6% | 需要重复算法步骤，参数量不是唯一瓶颈 | 单纯扩大宽度或参数会增加容量，却没有证明能以同样执行深度学习迭代算法 | Table 1 |
| 以参数量/困惑度作为唯一质量代理 | 循环模型困惑度更差，却在推理任务接近或超过 24 层基线 | Table 3 中 $(12\otimes2)$ 困惑度 7.90 高于 24 层基线 7.40，但数学题平均 34.3 高于 29.3 | 预训练损失偏向记忆/词预测，忽略上下文组合 | 降低困惑度不能区分“记住答案”和“从上下文推导” | Table 3、Fig.2 |
| 直接把 CoT 当作唯一增加推理时间的办法 | 显式 CoT 每次只新增一个可见 token，序列更长且带解码开销 | Figure 4 左图是每轮新增一个思维 token；循环模型可在隐藏状态中并行更新多个位置 | 中间计算可隐藏且并行，不必都写入文本 | 本文只给理论模拟，尚未证明实际训练的循环模型会产生可解释潜在思维 | Fig.4、Theorem 5.4 |

### 2.3 论文计划解决的问题与成功标准

研究问题是：在相同有效深度/FLOPs 下，$k$ 层块循环 $L$ 次是否能匹配 $kL$ 层独立模型；在相同参数量下，循环是否优于 $k$ 层一次模型。成功标准包括：合成推理准确率接近等 FLOPs 基线；1B 语言模型中推理任务的 `% Gap` 高于记忆任务；准确率随 $D$ 近似按 $log D$ 增长；正则化能保留推理增益且不明显损失困惑度。论文不声称覆盖多模态、常识推理、实际服务延迟或训练稳定性的全谱系。

### 2.4 核心方案如何解决并优化问题

一个样本先进入 $k$ 层块，块输出再作为同一块下一轮输入，执行 $L$ 次；因此参数只保留一份，执行层数为 $kL$。训练时模型直接做输入到输出映射，不使用 CoT（加法/p-hop/i-GSM），语言模型使用因果下一 token 目标。另有 middle looping 保留首尾独立层，以及余弦相似度正则化，使普通 24 层模型的相邻 $k$ 层块趋向共享。

| 原始问题 | 方案 | 改变的变量 | 预期优化 | 判断 |
|---|---|---|---|---|
| 深度与参数绑定 | $(k\otimes L)$ 权重共享循环 | 独立参数从 $kL$ 降为 $k$，执行深度保持 $kL$ | 参数/显存下降，组合推理保持 | 合成任务直接支持；真实推理部分支持 |
| 首尾层角色可能不同 | middle looping | 只共享中间块 | 保留输入编码和输出解码自由度 | Table 3 显示困惑度和总体改进更均匀，仍是单次实验 |
| 普通模型没有循环归纳偏置 | Eq.(3)-(4) 余弦正则 | 相邻块权重相似度上升 | 保留参数自由度并注入推理偏置 | Table 4/Fig.5 支持，归因仍非方差分解 |

### 2.5 完整因果链与证据闭环

组合推理需要多步计算（作者陈述）→ 独立加深同时增加参数（结构事实）→ 循环共享把有效深度与参数分离（方法）→ 迭代算法可在短描述下重复执行（Theorem 5.1–5.3）→ 加法、p-hop、i-GSM 准确率接近等 FLOPs 基线（Table 1/2）→ Pile 预训练后推理任务的 `% Gap` 高、记忆任务接近参数效应（Table 3、Fig.2）→ 深度缩放近似 $log D$（Fig.3）→ 正则化复现方向且困惑度近似不变（Table 4）。直接验证的是合成任务、固定规模语言模型和理论构造；“潜在思维是实际收益根因”“适用于更广泛推理”仍属间接或未验证结论。

## 3. 核心贡献与创新点

1. 提出以 $(k\otimes L)$ 统一比较共享参数循环、等参数和等 FLOPs 基线（Fig.1）。
2. 在加法、p-hop、i-GSM 上显示少参数循环模型接近等 FLOPs 深模型（Table 1/2）。
3. 在 1B 级语言模型上发现推理/记忆分化及有效深度缩放（Table 3、Fig.3）。
4. 给出循环模型模拟群合成、p-hop 和 CoT 的理论构造（Theorem 5.1–5.4）。
5. 提出循环启发正则化，在近似不变困惑度下改善数学题和推理原语（Eq.(3)-(4)、Table 4）。

## 4. 研究方法

### 4.1 方法总览

![Figure 1：循环架构与三类基线](../../02_model_systems/llm_foundations/assets/papers/reasoning-with-latent-thoughts/fig1-looping-architecture-caption.png)

过程审计副本（同一裁剪，原分辨率 QA 通过）：![Figure 1 audit crop](figures/fig1-looping-architecture-caption.png)

图 1 紧邻展示：$(k\otimes1)$ 是等参数浅层基线；$(kL\otimes1)$ 是等有效深度/FLOPs 但约多 $L$ 倍独立参数的基线；$(k\otimes L)$ 反复使用同一块；middle looping 仅循环中段。训练边界是标准 Transformer/因果语言模型目标，推理边界是固定 $L$ 次执行，论文没有报告自适应提前停止或线上延迟。

### 4.2 组件级设计动机与具体问题映射

**权重共享循环。** 作者明确用它解决“深度增加会复制参数”的约束：同一函数迭代提供计算步骤，Table 1/2 与 Theorem 5.1–5.3 分别从实验和表达力支持该设计；代价是循环间必须顺序执行，且共享权重降低容量。

**Middle looping。** 作者沿用首尾层可能承担特殊角色的动机，只共享中段而保留输入/输出边界层。Table 3 的单一对照显示困惑度和任务改进较均匀，但缺少位置和块长度的系统消融，因此只是部分支持。

**循环启发余弦正则。** 作者希望普通深模型保留独立参数改善困惑度，同时让相邻块方向接近以获得循环偏置。Table 4 与 Figure 5 支持相似度和结果方向，但没有排除一般优化正则效应。

| 设计项 | why 状态 | 具体问题 | 因果机制 | 验证证据 | 判断 |
|---|---|---|---|---|---|
| 权重共享循环 | author-stated | 深度重要但参数昂贵 | 同一函数迭代，增加计算步骤而不复制权重 | Table 1/2、Theorem 5.1–5.3 | 直接支持 |
| middle looping | author-stated + inferred | 首尾层可能承担特殊编码/解码角色 | 只共享中段，保留边界层自由度 | Table 3 一组对照 | 部分支持 |
| `% Gap` | author-stated | 困惑度不能公平比较不同参数预算 | 将循环结果放在等参数与等 FLOPs 两端归一化 | Eq.(1)、Table 3 | 指标合理，但分母小/可超 100% |
| latent thoughts | inferred from theory | CoT 显式 token 有序列开销 | 隐状态多位置并行更新，理论上模拟多步 CoT | Fig.4、Theorem 5.4 | 理论支持，实践未验证 |
| 余弦正则 | author-stated | 普通模型缺少循环归纳偏置 | 让相邻块参数方向接近但保留各块幅度 | Fig.5、Table 4 | 直接支持方向，独立贡献未完全隔离 |

### 4.3 关键公式

$$
(k\otimes L)=f^{(L)}=\underbrace{f\circ f\circ\cdots\circ f}_{L\ \text{次}},\qquad D=kL.
$$

**这条公式在算什么？** 定义循环模型及其有效深度。

**怎么读？** 一份 $k$ 层函数重复 $L$ 次，执行上像 $kL$ 层。

**输入与输出。** 输入序列经 $f$ 反复变换，输出最终隐藏状态/词分布。

**变量在这里各做什么？** $k$ 控制独立参数块深度，$L$ 控制重复次数，$D$ 是执行层数。

**直觉。** 增大 $L$ 提高计算步数而不按比例增加参数。

**边界。** 共享参数不意味着中间状态完全等价于独立层；表达能力和优化轨迹可能不同。

**小例子。** $(4\otimes6)$ 与 $(24\otimes1)$ 都执行 24 层，但前者只有约 1/6 的独立块参数。

$$
\%\,Gap_G=\frac{\operatorname{Avg}_G(k\otimes24/k)-\operatorname{Avg}_G(k\otimes1)}{\operatorname{Avg}_G(24\otimes1)-\operatorname{Avg}_G(k\otimes1)}.
$$

**这条公式在算什么？** 计算循环模型填补等参数与 24 层基线差距的比例。

**怎么读？** 分子是循环相对浅层增加的分数，分母是深层相对浅层的全部增量。

**输入与输出。** 输入任务组平均准确率，输出百分比。

**变量在这里各做什么？** $G$ 是任务组；三项 Avg 分别对应循环、浅层和 24 层基线。

**直觉。** 0% 表示循环没有超出浅层，100% 表示追平深层；超过 100% 表示超过深层。

**边界。** 分母接近零会放大数值；指标不是因果效应或成本收益比。

**小例子。** Table 3 的数学题 $k=12$：$(34.3-26.7)/(29.3-26.7)=2.92$，即 292%，与表中四舍五入的 282% 略有差异，说明报告值/底层均值存在舍入或任务平均细节差异，不能过度解读小数点。

$$
\operatorname{Acc}=\alpha\log(D)+\beta.
$$

**这条公式在算什么？** 拟合准确率随有效深度的缩放趋势。

**怎么读？** 深度增加带来收益，但每增加同样比例的深度，收益按对数递减。

**输入与输出。** 输入 $D$，输出预测准确率。

**变量在这里各做什么？** $alpha$ 表示深度敏感度，$eta$ 是截距。

**直觉。** $D$ 从 4 增至 8 的收益可能大于 24 增至 48 的收益。

**边界。** 这是有限实验点上的线性拟合，不是跨规模定律；Figure 3 没有给置信区间。

**小例子。** 推理原语拟合中作者报告 $alpha_{loop}/\alpha_{base}=1.19$，表示循环加深斜率约为独立加层的 1.19 倍。

$$
R_G(k)=\frac{1}{L-k}\sum_{i=0}^{L/k-2}\sum_{j=0}^{k-1}\operatorname{Cosine}\!\left(\theta_G^{(ik+j)},\theta_G^{((i+1)k+j)}\right),
\quad
\mathcal L=\mathcal L_{xent}+\lambda_{reg}|\mathcal G|^{-1}\sum_{G\in\mathcal G}R_G(k).
$$

**这条公式在算什么？** 第一项衡量相邻块对应层的权重方向相似度，第二项把它加入交叉熵目标。

**怎么读？** 提高 $lambda_{reg}$ 会让相邻块更像，从而趋近循环模型。

**输入与输出。** 输入各层参数、块大小 $k$ 和正则强度，输出训练损失。

**变量在这里各做什么？** $G$ 是参数组（如 Attn-Q、FFN-W1）；$	heta_G^{(l)}$ 是第 $l$ 层该组权重；$mathcal G$ 是全部参数组。

**直觉。** $lambda=0$ 是普通训练；较大 $lambda$ 压缩块间差异。

**边界。** 论文正文将相似度写入加法损失，实际最小化方向需依实现约定理解；作者报告 $lambda=10$ 时相似度约 0.98，但未提供完整代码。

**小例子。** 24 层模型用 $k=4$、$lambda=10$，Table 4 数学题平均从 29.3 升至 36.4，困惑度从 7.40 变为 7.38。

### 4.4 训练/实验/部署设计

- 合成任务：加法为 3 位数、操作数 $n\in\{2,4,8,16,32\}$；p-hop 字母表大小 4、序列长 256、$p\in\{16,32\}$；i-GSM 是深度 4 的符号 DAG、模 7。均直接训练输入到答案，不用 CoT；3 个随机种子取最佳平均准确率（Appendix A.1）。
- 语言模型：Pile 250B tokens；24 层、约 1.5B 参数（正文称 1B 级），2048 hidden、5120 FFN、32 heads，序列长 1280、batch 512、400k steps；浅层/循环仅改变层数。
- 评估：困惑度、closed-book QA（主要记忆）、open-book QA（上下文推理）、数学题、reasoning primitives，共 19 个任务；多数下游为 5-shot。
- 公平性：循环与等 FLOPs 基线执行深度相同；参数量不同是研究变量。未报告 wall-clock、GPU 型号、吞吐、能耗、显存峰值或自适应循环策略。

## 5. 关键结论

### 5.1 主结果

![Table 1：加法与 p-hop](../../02_model_systems/llm_foundations/assets/papers/reasoning-with-latent-thoughts/table1-addition-phop-caption.png)

Table 1 显示：加法中 $(1\otimes12)$ 在 32 个操作数上 99.6%，而 $(1\otimes1)$ 为 0.0%；$(2\otimes6)$ 为 99.5%，对应浅层 $(2\otimes1)$ 38.8%。p-hop 的 $(1\otimes6)$ 在 $p=32$ 达 99.5%，而一次模型为 49.0%。这直接支持“这些合成任务更需要深度而非独立参数”。

![Table 3：语言模型主结果](../../02_model_systems/llm_foundations/assets/papers/reasoning-with-latent-thoughts/table3-language-model-results-caption.png)

Table 3 的 24 层基线困惑度 7.40、数学题 29.3、推理原语 47.5。$(12\otimes2)$ 只有约一半独立参数，困惑度 7.90，却数学题 34.3、推理原语 51.2；$(4\otimes6)$ 数学题 24.8、推理原语 56.9。循环模型对 closed-book QA 的 `% Gap` 约 37–58%，对 open-book 约 56–94%，对数学题最高 282%，说明推理/记忆分化，但 `% Gap` 超过 100% 也表明它不是“恢复比例”的严格上界。

### 5.2 消融和机制证据

![Figure 3：有效深度缩放](../../02_model_systems/llm_foundations/assets/papers/reasoning-with-latent-thoughts/fig3-effective-depth-scaling-caption.png)

Figure 3 对 $(4\otimes L)$ 与 $(4L\otimes1)$ 都拟合 $log D$；推理原语循环斜率比独立加层高 1.19 倍。图支持“更多循环仍有收益且边际递减”，但只有少数深度点、无误差条，不能证明普适 scaling law。

![Table 4：循环启发正则化](../../02_model_systems/llm_foundations/assets/papers/reasoning-with-latent-thoughts/table4-regularization-results-caption.png)

Table 4 中 $k=4,\lambda=10$ 的数学题 36.4、推理原语 57.2，困惑度 7.38；baseline 分别为 29.3、47.5、7.40。Fig.5 的相似度约 0.98 验证参数确实趋同。可是不同 $k$、$lambda$ 与训练轨迹没有完整网格，不能将收益归因到“共享结构”而排除优化正则本身。

| 技术点 | 对照 | 证据强度 | 尚缺最小实验 |
|---|---|---|---|
| 循环深度 | 等参数/等 FLOPs | 直接受控（合成任务）；语言模型任务组有混杂 | 固定参数、训练步数和实际 FLOPs 的多种随机种子报告 |
| middle looping | $(12\otimes2)$ | 单一结构对照，部分支持 | 首尾层位置、循环块长度的系统消融 |
| latent thoughts | CoT 理论模拟 | 理论构造，非实测机制 | 记录隐藏状态、与显式 CoT 的同 FLOPs 实验 |
| 正则化 | baseline、多个 $k$ | 结果和相似度直接支持方向 | $lambda$ 网格、等优化噪声、参数组移除消融 |

### 5.3 是否验证了假设

- “合成算法任务主要需要深度”：Table 1/2 和 Theorem 5.1–5.3 支持，范围限于模运算、p-hop、符号 i-GSM。
- “语言模型循环偏向推理”：Table 3、Fig.2/7 在任务组平均层面支持；困惑度与下游评价存在指标不一致，机制仍未识别。
- “收益随有效深度对数增长”：Fig.3 的拟合支持描述性趋势，不足以外推到更大模型或不同数据。
- “循环可模拟 CoT”：Theorem 5.4 是存在性证明，要求固定输入长度、dummy tokens、额外维度和 mask；不等于实际训练模型自然学会 CoT。

### 5.4 收益来源归因

循环的直接收益首先体现在组合推理准确率和 reasoning primitives；closed-book/困惑度收益较小甚至为负。数学题的 282% `% Gap` 是基于表格的近似归因，不是正式方差分解。论文没有 runtime kernel、显存或吞吐测量，因此不能把参数节省直接表述为服务成本下降。

## 6. 理论分析与 CoT 边界

Theorem 5.1 证明有限群合成可由 1 层循环 $\lceil\log_2 n\rceil$ 次完成；Corollary 5.3 给出 p-hop 用 1 层、$\lfloor\log_2p\rfloor+2$ 次循环。Theorem 5.2 将最多 $R$ 个不同层的 Transformer 模拟为带额外 embedding/MLP 宽度的 1 层循环。Theorem 5.4 通过 mask、位置右移和 token 编解码，让循环模型在理论上模拟 $m$ 步 CoT。它们共同说明“迭代结构可以压缩描述”，但复杂度转移到隐藏维度、精度、dummy token 和构造性权重；不是无条件的参数、内存或延迟优势。

![Figure 4：CoT 与潜在思维](../../02_model_systems/llm_foundations/assets/papers/reasoning-with-latent-thoughts/fig4-cot-latent-thoughts-caption.png)

图 4 左侧将 CoT 画成每轮生成一个可见 token，右侧画出循环模型并行产生多个 latent thoughts。该图是概念和定理的桥接，不是隐藏状态可解释性实验证据。

## 7. Related Work 对比

| 类别 | 方法核心 | 优点 | 局限 | 与本文关系 |
|---|---|---|---|---|
| Universal Transformer / ALBERT | 循环或跨层共享 | 参数效率、可重复计算 | 主要关注监督或困惑度 | 本文把问题转向推理任务 |
| CoT / scratchpad | 显式生成中间 token | 可解释、可扩展推理步数 | 序列变长、解码成本 | 本文将其抽象为循环，并提出潜在思维 |
| MidAS/stacking | 训练中逐步复制层 | 改善训练和推理偏置 | 最终参数仍增长 | middle looping 与其层复制联系 |
| looped programmable computers | 迭代层模拟算法/Turing machine | 理论表达力强 | 与真实 LM 指标距离较远 | 本文加入 1B LM 和推理/记忆实验 |

## 8. 基础设施、部署与归因边界

循环推理在算术上保持相同每层算子，但重复访问同一权重可能有缓存收益，也可能因循环间同步增加调度开销；论文没有 kernel 或硬件测量，不能断言吞吐更高。训练需跨 $L$ 次反向传播，激活保存和梯度稳定性未报告。middle looping 可能更适合实际模型，因为首尾层独立，但这只是 Table 3 的一次对照。若用于推理时扩展，循环次数 $L$ 是显式计算预算；论文没有自适应停止、批处理或 KV-cache 设计。

## 9. 局限、解读问题与待验证清单

1. “推理”由四类任务组代理，是否覆盖常识、多模态、长程规划未知。
2. 1B 语言模型只在 Pile、固定训练预算下测试；规模、数据和优化器的交互未拆分。
3. 循环与非循环模型的实际 wall-clock、能耗、显存和服务吞吐缺失。
4. 正则化公式的符号方向依实现约定；源码归档未包含可运行训练代码。
5. OpenReview 评审不可访问，无法交叉核对作者回复或审稿人指出的反例。
6. 理论是存在性/构造性结果，不能直接解释实验模型内部是否真的形成 latent thoughts。

## 10. 结论

这篇论文最可靠的结论是：在若干算法化推理任务上，循环共享权重可以用少得多的独立参数提供接近等 FLOPs 深模型的有效深度；在 1B 级语言模型上，循环模型相对更偏向上下文推理而非记忆，且简单的块间相似度正则化能部分迁移这一偏置。较弱的结论是“循环等同于显式 CoT”或“循环普遍降低部署成本”：前者目前主要是理论模拟，后者缺少系统实测。后续工作应以同参数/同 FLOPs/同 wall-clock 的受控实验、跨规模任务、隐藏状态机制分析和真实硬件基准验证因果链。
