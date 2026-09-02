---
tags:
  - paper
  - collection/speculative-decoding
  - domain/model-systems
  - status/deep-review
  - topic/moe-speculative-decoding
  - method/commitment-weighted-expert-selection
---

# AcceptMoE 精读分析

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Evolution](../surveys/evolution.md)
> - 证据资产：`../assets/papers/acceptmoe/`
> - 相关文档：[Figure inventory](../evidence/acceptmoe-figure-inventory.md)

> 资料状态：已核验 arXiv `2608.02989v1` PDF、TeX 源码和 10 页文本；图表由源码中的 vector PDF 转为 PNG。未发现公开代码仓库或 OpenReview 评审记录，因此实现与评审结论只按论文证据表述。

## 修订信息

- 当前文档版本：`1.1.0`
- 当前修订 ID：`rev-acceptmoe-visual-completeness-20260901`
- 当前修订时间：`2026-09-01T21:10:00+08:00`
- 替代版本：`rev-acceptmoe-initial-20260901` / `1.0.0`

| 修订 ID | 文档版本 | 时间 | 类型 | 替代修订 | 变更摘要 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|
| `rev-acceptmoe-initial-20260901` | `1.0.0` | `2026-09-01T12:00:00+08:00` | `initial` | 无 | 建立单篇因果闭环、公式卡、图表证据、基础设施分析和发布链路 | arXiv v1 PDF/TeX；结构与语义校验 | none |
| `rev-acceptmoe-visual-completeness-20260901` | `1.1.0` | `2026-09-01T21:10:00+08:00` | `evidence-update` | `rev-acceptmoe-initial-20260901` / `1.0.0` | 将 Figure 2–5 嵌入正文并固化示意图完整性要求 | 用户反馈；Figure inventory；发布器校验 | minor |
| `rev-acceptmoe-zh-method-flow-20260902` | `1.2.0` | `2026-09-02T10:00:00+08:00` | `content-update` | `rev-acceptmoe-visual-completeness-20260901` / `1.1.0` | 将 4.1 的系统黑话改为中文解释，保留必要专名与数学术语 | 用户反馈；readability audit | minor |

## 0. 资料与配图索引

- 论文：`arXiv:2608.02989v1`，arXiv `2608.02989v1`。
- 源码/LaTeX：`arXiv source archive`，归档为 `source.tar.gz`。
- 开源代码：未找到；实现状态为“不可核验”，不据 README 推断。
- OpenReview：未找到；公开评审、决定和作者回复不适用。
- 提取文本：`PDF/TeX extraction`。
- 原始图：Figure 1（算法总览）、Figure 2（驻留感知剪枝）、Figure 3（全驻留吞吐）、Figure 4（offload 吞吐）、Figure 5（消融）；正式 PNG 位于 `../assets/papers/acceptmoe/`，完整 bbox/caption/QA 见 [figure_inventory](../evidence/acceptmoe-figure-inventory.md)。
- AI 生成分析图：不需要；原始 Figure 1 已显示输入、阶段、输出和推理边界。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 不等于/易混项 | 来源 |
|---|---|---|---|
| MoE | 混合专家目标模型；每个 token 只路由到 top-k 专家 | 不等于所有专家同时计算 | §1, §3 |
| verification block（验证块） | 一次目标模型前向中并行验证的候选树节点集合 | 不等于最终接受的前缀 | Eq. 1 前 |
| commitment probability（提交概率） | 某候选位置的节点最终落在已接受输出前缀上的边际概率 | 不等于条件接受率 | §3.2 |
| eligible expert set（允许专家集合） | 验证块中路由器可以选择的专家集合 | 不等于自然路由得到的专家并集 | Eq. 2 |
| effective rank（有效秩） | 需求分布熵的指数，用于自动决定集合大小 | 不等于参数量或固定预算 | Eq. 5 |
| residency-aware pruning（驻留感知剪枝） | 根据 GPU 专家缓存的当前驻留状态删除低需求专家 | 不等于预测自然路由后预取 | §3.4 |
| rerouting budget（重路由预算） | 允许剪枝额外改派的 token 数量上限 | 不等于传输字节预算 | Eq. 6 |
| Standard SD（标准投机解码） | EAGLE-3 候选树加目标模型原始 top-k 路由 | 不等于普通自回归解码 | §4 |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/单位 | 来源 |
|---|---|---|---|---|
| $E,k$ | 专家总数、每个 token 路由的专家数 | author-defined | 每层/数量 | §3.1 |
| $\mathcal V,K_t$ | 验证块、token 的自然 top-k 专家集合 | author-defined | 验证块/token | Eqs. 1–2 |
| $\mathcal V,T,t,d_t$ | 验证块、块中 token 数、token 索引、候选位置 | author-defined | 验证块/token | §3.1 |
| $z_t,r_t,K_t$ | 路由器分数、softmax 概率、自然 top-k 集合 | author-defined | token/专家 | Eqs. 1–2 |
| $S,A,R$ | 允许集合、根节点锚点集合、非锚点专家 | author-defined | 每层/验证块 | §3.1–3.3 |
| $\widehat p_d,N_d,\beta,\alpha_t$ | 位置提交概率估计、该位置节点数、权重指数、token 重要性 | author-defined | 位置/token | Eq. 3 |
| $u_e,q_e,n_{er}$ | 专家需求分数、归一化需求、有效秩得到的数量 | author-defined | 专家 | Eqs. 4–5 |
| $\mathcal H,C,D,v_e,a(S),X$ | 驻留集合、未驻留集合、删除集合、自然分配数、位移预算、GPU 槽位数 | author-defined | 每层/运行时 | §3.4, Eq. 6 |

## 0.2 算法总览

![AcceptMoE Figure 1](../assets/papers/acceptmoe/algo1.png)

> 图注：原论文 Figure 1，展示 demand computation、self-sizing eligible set 和 constrained dispatch；原始 caption 及 bbox 见 `../evidence/acceptmoe-figure-inventory.md`。

## 1. 论文基本信息

- 标题：AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding
- arXiv：2608.02989v1，2026；10 页，5 个 figure。
- 作者（按顺序）：Shuang Liang；Hao (Mark) Chen；Zhiwen Mo；Qianzhou Wang；Guoyu Li；Lingxiao Ma；Wayne Luk。
- 第一作者：Shuang Liang（first listed author），机构 1 Imperial College London。
- 通讯作者：论文标题页以邮箱 `shuang.liang@imperial.ac.uk` 标示 Shuang Liang（title-page contact email）；机构 1 Imperial College London。
- 其余作者机构（去重）：Imperial College London；Tile-AI。
- 机构证据：PDF 标题页的上标 1/2 与 affiliations 行；未推断未标注身份。
- 角色证据短语：first listed author；title-page contact email；PDF title block, affiliation 1；PDF title block email and affiliation 1；paper.pdf first page title block and affiliations。
- 研究领域：MoE 推理、speculative decoding、专家 offloading。
- 核心问题：树验证中的专家 union 和 offload 传输成本不随 token 数同步下降。
- 关键约束：验证块固定后才选专家；约束路由会改变 target 分布；batch size=1、单卡评测。

## 2. 研究动机与问题—方案闭环

自回归模型每生成一个 token 都需要一次完整的目标模型计算。投机解码用 EAGLE-3 先提出候选树，再一次验证多个节点；但混合专家目标模型的成本由“所有节点自然 top-k 专家的并集”决定。被拒绝分支仍会触发专家权重访问。作者引用的 Qwen3-30B-A3B 例子显示，EVICT 可减少 74.7% 的验证 token，却只减少 32.5% 的已激活专家，说明减少节点不是减少专家访存的充分条件（Introduction）。

第二个痛点是固定专家预算：MoE-Spec 必须预先给每层预算 $B$，而论文的五组预算试验表明最佳 $B$ 随模型和任务变化。第三个痛点是专家卸载：同样大小的集合，如果成员不在 GPU 缓存中，仍会产生主机到显存的权重传输。AcceptMoE 的目标是把“预计会提交的节点需求”和“当前缓存驻留状态”纳入验证阶段的专家选择。

### 2.1 现有方案为何不够

具体场景：根节点和兄弟节点选择不同专家，最终只接受一条路径但 union 仍很大。简单修补失败：只减少节点不保证路由集中。

| 旧做法 | 可观察失败 | 具体场景 | 根因 | 为什么简单修补不够 | 证据 |
|---|---|---|---|---|---|
| 原始路由 | 拒绝分支也加载专家，专家并集很大 | 本文构造说明例：根节点和 63 个兄弟节点各选不同专家；最终只接受一条路径，但一次验证仍触碰几十个专家 | token 数与专家并集是不同成本量 | 只减少候选节点可能仍保留分散路由；需要改变验证阶段的允许集合或预取策略 | §1；引用 EVICT 数据 |
| 固定 B 的 MoE-Spec | B 跨任务不稳 | GPT-OSS HumanEval 的最佳 B=25；把它用于 Qwen3-Coder 同任务比该模型最佳固定 B 低 9.1 个百分点 | 需求分布随模型/任务/块变化 | 调一个全局 B 保护最坏任务会浪费其他任务的计算 | Fig. 5b，§5.3 |
| 原始路由加预取 | 缓存未命中仍造成传输等待 | §5.2 中标准投机解码有 65%–78% 的墙钟时间在等待专家加载 | 成本取决于未驻留成员而非集合大小 | 预测路由只改变加载时序，不减少被请求的专家并集 | Fig. 5a,c,d |

### 2.2 目标与成功标准

目标：为每个层和验证块构造足够小、又能覆盖关键提交路径的专家集合，并在专家卸载时适配显存缓存。成功标准是准确率接近标准投机解码，同时提高每秒生成 token 数、降低每个输出 token 的传输字节和专家加载等待占比。明确不保证保持目标模型分布：公式 2 的掩码会改变路由器分布。

### 2.3 方案如何改变变量

| 问题 | 设计 | 改变的变量/行为 | 预期指标 | 判断 |
|---|---|---|---|---|
| 分支需求被等权计数 | $\widehat p_d^\beta$ commitment weighting | token utility 权重 $\alpha_t$ | 更高准确率/相同 accepted length | 直接 matched-budget 支持 |
| budget 需人工给定 | effective rank | $|S|$ 随 block demand 熵变化 | 免 sweep，平均损失小 | 部分支持 |
| nonresident 专家拖慢 offload | residency pruning | $S\to S'$，减少 nonresident eligibility | H2D、cache hit、吞吐 | 直接消融支持；准确率代价存在 |

因果链是：MoE 树验证产生分散 expert union -> 拒绝分支造成无效访存 -> 用提交概率重加权 router demand 并约束 $S$ -> 限制执行专家数；offload 再用 cache 状态剪枝 -> 减少 fetch stall。准确率和吞吐测量支持这条链，但“约束路由本身不会伤害更广泛任务分布”没有被验证。

## 3. 核心贡献与创新点

1. commitment-weighted demand：在 matched $B_0$ 下，AcceptMoE-fix 比 MoE-Spec 平均高 2.45 个百分点（Table 1）。
2. self-sizing：用需求熵的 effective rank 自动定大小；五个 sweep 点平均比最佳测量固定 B 低 0.97 个百分点，最坏低 1.83。
3. residency-aware pruning：相对关闭 pruning，流量下降 38.6%–48.6%，平均准确率变化 -0.27 个百分点。

## 4. 研究方法

### 4.1 方法流程

EAGLE-3 先生成一棵最多 5 步、64 个节点的候选 token 树。随后，对每个 MoE 层（混合专家层），目标模型的路由器输出每个专家的分数（logit）；AcceptMoE 用“该节点最终会被提交的概率”给这些分数加权。它先保留根节点按原始规则选出的 top-k 专家作为锚点，再按加权需求从高到低排序，并用需求分布的有效秩自动决定还要保留多少个非锚点专家。验证时，每个 token 只能在这个允许集合 $S$ 中选择 top-k 专家。

在专家权重不能全部放入显存的场景，AcceptMoE 还会读取当前的 LRU（最近最少使用）显存缓存。它按加权需求从低到高检查不在缓存中的专家，在不超过额外重路由预算且不低于 $k$ 个专家的条件下删除尽可能长的前缀，得到最终集合 $S'$。这里的“重路由”是指原本会发送给被删除专家的 token 改派给保留专家；被保留但仍不在显存中的专家，第一次收到 token 时仍需从主机内存加载。

![AcceptMoE Figure 2](../assets/papers/acceptmoe/algo2.png)

> 图注：原论文 Figure 2，展示驻留感知剪枝如何按需求排序删除未驻留专家，并通过重路由更新 GPU 中可容纳的专家槽位。

### 4.2 关键公式与解释卡

$$U_{\mathrm{nat}}(\mathcal V)=\bigcup_{t\in\mathcal V}K_t$$

**这条公式在算什么？** 计算专家 union：一次验证会触碰多少个不同专家。

**怎么读？** 把块内每个 token 的自然 top-k 集合取并集。

**输入与输出。** 输入是 token 集合和每 token 的 $K_t$；输出是专家集合。

**变量在这里各做什么？** $\mathcal V$ 是验证节点，$K_t$ 是 token 的自然专家集合。

**直觉。** 分支越多且路由越分散，专家并集越大。

**边界。** 这是原始路由的逻辑专家并集，不等于实际分波执行、缓存未命中次数或主机到显存的传输字节。

**小例子。** 4 个 token、每个选择 2 个且彼此无重叠时，专家并集为 8；最终只接受 1 条路径也不会自动把并集变成 2。

$$\widetilde K_t(S)=\mathrm{TopK}_k(z_t+M_S)$$

**这条公式在算什么？** 在允许集合 $S$ 内重新分配 token 的专家。

**怎么读？** 把不在 $S$ 中的专家分数设为 $-\infty$，再选择分数最高的 $k$ 个专家。

**输入与输出。** 输入是路由器分数 $z_t$ 和允许集合 $S$；输出是受限的 top-k 专家集合。

**变量在这里各做什么？** $M_S$ 在 S 内为 0，外部为 $-\infty$；$k$ 是路由数量。

**直觉。** $S$ 越小，专家计算和访存上限越低，但被迫重路由的 token 越多。

**边界。** 这会改变目标模型路由分布，因此不是保持分布不变的优化；只有 $S=[E]$ 时才恢复标准投机解码。

**小例子。** 若自然 top-2 是 {E1,E7} 而 S={E1,E2}，E7 会被 E2 替代，输出分布可能改变。

$$\alpha_t=\widehat p_{d_t}^{\,\beta}N_{d_t}^{-1/2},\qquad u_e=\sum_t\alpha_t r_{t,e}\mathbf1[e\in K_t]$$

**这条公式在算什么？** 估计专家 e 对“最终可能提交”的需求。

**怎么读？** router 概率乘位置提交概率，再对块内 token 求和。

**输入与输出。** 输入是离线 $\widehat p_d$、层宽 $N_d$、router 概率；输出是每专家 utility $u_e$。

**变量在这里各做什么？** $\beta=0.5$ 控制 commitment 强度；$N_d^{-1/2}$ 抑制宽树层级；指示函数只计自然 top-k 内专家。

**直觉。** 越可能被提交的位置权重越大；兄弟分支越多，每个节点的分摊权重越小。

**边界。** $\widehat p_d$ 来自训练追踪记录，并在评估前固定；它是边际概率，不是条件接受率。

**小例子。** 位置 1 的 $\widehat p=.8$、位置 4 为 .2，$\beta=.5$ 时权重因子分别约 .894 和 .447，早期位置约为后期两倍。

$$n_{\mathrm{er}}=\left\lceil\exp\left(-\sum_{e\in R}q_e\log q_e\right)\right\rceil$$

**这条公式在算什么？** 把剩余需求的分散程度转换为要保留的非锚点专家数。

**怎么读？** 需求集中时接近 1，均匀分布在 m 个专家时接近 m。

**输入与输出。** 输入归一化需求 $q_e$；输出整数 $n_{er}$。

**变量在这里各做什么？** $R$ 是非 anchor 专家；$q_e=u_e^+/Z$；$Z$ 是正 utility 总和。

**直觉。** 熵高意味着需要更宽集合覆盖需求，熵低意味着可缩小集合。

**边界。** 需满足 $|S|\ge k$；全零 utility 时只保留满足最小大小的专家。

**小例子。** 若 q=(0.9,0.1)，effective rank=$e^{0.325}\approx1.38$，向上取整为 2；均匀 q=(.5,.5) 时为 2。

$$m^\star=\max\{m:\sum_{j=1}^{m}v_{\pi(j)}\le a(S),\ |S|-m\ge k\},\quad D^\star=\{\pi(1),...,\pi(m^\star)\}$$

**这条公式在算什么？** 在不超过 rerouting budget 且不低于 k 个专家的条件下，最多删除多少 nonresident 专家。

**怎么读？** 按需求分数从低到高删除，直到下一次删除会超出预算或破坏最小集合。

**输入与输出。** 输入自然 assignment 数 $v_e$、预算 $a(S)$、排序 $\pi$；输出删除集合 $D^\star$。

**变量在这里各做什么？** $X$ 只限制 GPU 槽位；$\mathcal H$ 是 resident set；$C=S\setminus\mathcal H$ 是可剪枝候选。

**直觉。** 需求低且不在缓存中的专家最适合删除，可以减少加载和缓存驱逐。

**边界。** 被保留但未驻留的专家仍会按需加载；显存槽位不足时仍可能分波执行。

**小例子。** 若预算允许移动 3 个 assignments，候选专家 assignment 数为 (1,2,4)，只能删前两个。

### 4.3 组件级设计动机矩阵

| 设计项 | 论文是否说明原因 | 目标问题 | 因果机制 | 替代/权衡 | 验证 |
|---|---|---|---|---|---|
| commitment weight（提交概率加权） | 论文明确说明（§3.2） | 被拒绝的兄弟分支等权污染 | 让更可能提交的位置主导专家需求 | 直接累加路由概率更简单但会高估分支需求 | 同预算消融，直接证据 |
| root anchor（根节点锚点） | 论文明确说明（§3.3） | 保证必提交根节点覆盖 | 固定加入根节点原始 top-k 专家 | 不加锚点可能更小但会伤害首 token | 未单独消融，部分支持 |
| effective rank（有效秩） | 论文明确说明（§3.3） | 去掉人工指定专家数 | 用需求熵映射集合大小 | 固定数量可调到更高点但需要逐任务试验 | 五组预算试验，部分支持 |
| residency pruning（驻留感知剪枝） | 论文明确说明（§3.4） | 未驻留专家造成加载等待 | 根据缓存状态限制允许集合 | 预测原始路由并预取可保持分布，但不能缩小专家并集 | 流量/缓存/吞吐消融，直接证据 |
| rerouting budget（重路由预算） | 论文明确说明（§3.4） | 防止过度改变路由 | 约束额外 token 改派数量 | 按字节计价更精确但需要运行时成本模型 | 未做单独敏感性，部分支持 |

## 5. 关键结论与技术 claim 证据矩阵

| 技术点 | 论文声称 | 证据 | 对照是否充分 | 判断 |
|---|---|---|---|---|
| 提交概率加权需求 | 同预算下平均比 MoE-Spec 高 2.45 个百分点 | Table 1，平均接受长度近似不变 | 只改变专家成员选择 | 直接支持 |
| 自适应集合大小 | 平均比最佳测量固定点低 0.97 个百分点 | Figure 5b，5 组 | 只是有限预算试验，不是全空间最优 | 部分支持 |
| 受限路由 | 提高速度 | Figure 3/4、Table 1 | 同时包含集合限制与 SGLang 执行 | 多项改动同时发生，但趋势一致 |
| 驻留感知剪枝 | 传输量下降 38.6%–48.6%，吞吐提高 4.6%–15.1% | Figure 5c–d、§5.3 | 同一选择器开关剪枝 | 直接支持 |
| 准确率边界 | 12 对平均低 0.27 个百分点 | Table 1 | 只看任务分数，未测 KL 或长尾质量 | 直接但范围窄 |

### 5.1 主结果

12 个模型—任务组合（Qwen3-Instruct/Coder、GPT-OSS-120B × GSM8K/MATH500/HumanEval/MBPP）中，AcceptMoE 平均准确率 90.63%，标准投机解码 90.90%，相差 -0.27 个百分点；最大单对下降 1.22 个百分点。全专家驻留于 RTX PRO 6000 Blackwell、SGLang 0.5.12.post1、单请求下平均吞吐为 1.290 倍，范围 1.217–1.339 倍，平均接受长度均约 4.39，因此收益主要来自专家计算和访存减少，而不是接受长度增加。RTX 5090、每层 48 个显存槽位的专家卸载下平均为 2.06 倍；每个输出 token 的主机到显存传输量下降 73.6%–77.1%，缓存命中率提高 10.8–14.2 个百分点（Table 2）。

![AcceptMoE Figure 3](../assets/papers/acceptmoe/hbm_throughput.png)

> 图注：原论文 Figure 3，全专家驻留于 GPU 时的端到端吞吐；测试硬件为 RTX PRO 6000 Blackwell。

![AcceptMoE Figure 4](../assets/papers/acceptmoe/offload_throughput.png)

> 图注：原论文 Figure 4，物理专家 offloading 下的端到端吞吐；测试硬件为 RTX 5090、每层 48 个 expert slots。

### 5.2 归因边界

直接证据支持“集合限制减少 union/传输”与“commitment weighting 优于等预算 MoE-Spec”。但吞吐还受 SGLang kernel、CUDA Graph（全驻留开、offload 关）、模型路由 fan-out、BF16 vs packed MXFP4 影响；论文没有跨 backend 或 batch sweep，因此不能把 1.290×/2.06× 外推为通用系统收益。约束 router 改变 target 分布，论文只测准确率，未报告 KL、perplexity、router load balance、长尾任务或安全拒答。

![AcceptMoE Figure 5](../assets/papers/acceptmoe/ablations.png)

> 图注：原论文 Figure 5，包含 fetch-wait、固定预算准确率 sweep、expert-weight traffic 和 cache hit 的消融与机制结果。

## 6. 相关工作比较

| 家族 | 机制 | 优点 | 局限/与本文差异 |
|---|---|---|---|
| EAGLE-3/Standard SD | draft tree + natural target routing | 分布保持 | MoE union 和 offload traffic 高 |
| EVICT/EcoSpec | draft-side 节点筛选、保留 natural routing | lossless 语义 | 不直接改变 verifier expert union |
| MoE-Spec | verifier-side 固定 B、router mass | 简单可部署 | budget 外部给定、位置等权 |
| SP-MoE/MoESpeQ | 预测 natural route + prefetch | 保持路由分布 | 预测/预取不能压缩 union |
| AcceptMoE | commitment-weighted、self-sizing、cache-aware eligibility | 不需 learned predictor 或固定 B | 近似 target 分布，batch=1 证据有限 |

## 7. 基础设施与部署分析

- 计算：每层路由器分数已经由验证器产生，选择器额外计算量约为 $O(TE)$ 的排序和熵计算；主要收益来自减少专家前馈网络的执行。
- 显存：专家卸载使用每层 $X=48$ 个 GPU 显存槽位，非专家权重、候选模型和 KV 缓存常驻显存；GPT-OSS 峰值占用 28.60 GiB/32 GB。
- 带宽：有效的主机到显存带宽应按 `传输字节 / 运行时间` 计算；论文只报告 MiB/token，未报告秒级带宽和 PCIe 利用率，因此无法判断是否带宽饱和。驻留感知剪枝将 Qwen 的传输量降至 633/464 MiB/token、GPT-OSS 降至 298 MiB/token。
- 数据类型：Qwen 专家权重使用 BF16；GPT-OSS 使用打包的 MXFP4，字节数不能直接跨模型比较。
- 运行时：全驻留测试启用 CUDA Graph、关闭调度重叠；专家卸载测试关闭二者以支持即时执行的槽位缓存。结论依赖 SGLang 0.5.12.post1 和单请求调度。
- 异构执行：GPU 执行非专家部分和已驻留专家，CPU 固定页主机内存保存被卸载专家，首次使用时按需传输；未评估 NPU、NVLink/RDMA 或多卡通信。

## 8. 代码、复现与证据缺口

未发现作者公开 Git 仓库、提交版本、模型配置或运行脚本；因此算法实现细节（掩码后端、LRU 更新、分波调度、计数器定义）只能按 TeX 描述。复现至少需要三种目标模型权重、EAGLE-3 候选模型、SGLang 版本、CUDA/驱动、20/50 条输入提示列表和固定页内存卸载实现。公开评审不可得，不能判断审稿人是否质疑分布变化或预算选择。

## 9. 局限、研究启发与待验证问题

1. AcceptMoE 通过改变 verifier 路由换取系统收益，因此不是严格 lossless SD；应补充 token-level KL、perplexity、最坏任务和长尾领域评测。
2. self-sizing 仅与有限五点 budget sweep 比较，不能证明 effective rank 是全局最优；应做更多 entropy/β/最小集合敏感性。
3. 所有端到端结果 batch=1、单卡、固定 256 token；应测试 batch、并发、不同 cache 容量和多卡互联。
4. residency pruning 的 rerouting budget 以 assignment 数近似传输成本；BF16/MXFP4 权重大小和 cache eviction 代价未进入目标函数。
5. 一个保持 natural route 的对照（只用 commitment 做 prefetch/cache）可分离“算法收益”和“改分布风险”。

总体判断：论文对 MoE speculative verification 的成本分解很有用，commitment-weighted utility 和 cache-conditioned eligibility 有直接实验支持；但准确率只用任务分数近似分布保真，代码缺失且部署范围窄，因此结论应限定为“单卡 batch=1 serving 的有效近似优化”，而不是普适无损加速。
