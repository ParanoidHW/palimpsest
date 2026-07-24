# OmniFit：受阻证据交付

## 修订信息

- 当前文档版本：`1.1.0`
- 当前修订 ID：`rev-omnifit-openreview-refresh`
- 交付状态：`blocked`

| Revision ID | Version | Revised at | Revised by | Type | Supersedes | Summary | Reason | Affected locations | Evidence | Conclusion impact |
|---|---|---|---|---|---|---|---|---|---|---|
| `rev-omnifit-initial` | 1.0.0 | 2026-07-17T00:00:00+08:00 | `review_omnifit` | initial | 无 | 建立 blocked 交付并记录恢复边界 | 精确论文资料不可用 | `analysis.md`; `figure_inventory.md`; `review_checklist.md` | prior manifest history | material |
| `rev-omnifit-openreview-refresh` | 1.1.0 | 2026-07-24T23:30:00+08:00 | `omnifit_refresh` | evidence-update | `rev-omnifit-initial` 1.0.0 / manifest `c1e005ec54ecc31b02783bc72ffc11a46f944f80d3a6173071d7d4da5ffc61e7` | 解析精确 OpenReview/ICML 身份并记录新的获取证据，但 PDF/source/reviews 仍受阻 | 用精确官方记录替换未解析身份；受硬停止指令约束，不再重试 | `analysis.md`; `openreview_reviews.md`; `figure_inventory.md`; `review_checklist.md`; `agent_handoff.md`; `deliverable_manifest.json` | material |

## 0. 来源与视觉清单

| 来源 | 本地证据 | 结果 |
|---|---|---|
| OpenReview forum | `https://openreview.net/forum?id=8RY20mLzup` | 浏览器挑战页；身份 URL 已确定，正文/评审不可读 |
| OpenReview PDF | `https://openreview.net/pdf?id=8RY20mLzup` | `curl -L --fail --retry 3` 返回 HTTP 403；无本地 PDF |
| OpenReview API v2 | `https://api2.openreview.net/notes?forum=8RY20mLzup&limit=1000` | HTTP 403；无 note/review JSON |
| ICML Downloads 2026 | `retrieval/icml-downloads.html` | 精确标题指向 poster `65962` |
| ICML official poster | `retrieval/icml-poster.html` | 标题、八位作者、摘要、2026 Spotlight 关联 `84897`；无 PDF/source/code 链接 |
| public metadata mirror | `retrieval/papers-cool.html` | 精确 OpenReview ID、作者、摘要、`ICML.2026 - Spotlight`；仅元数据，不替代论文 |

视觉计数为零。由于精确 PDF/source 均未获得，无法跨全文搜索 caption/关键词、渲染页面或裁剪 Figure/Table；因此既无机制视觉，也无结果/消融/系统视觉，且不生成空白 contact sheet。替代证据仅为官方 ICML 摘要和公开元数据，不能验证正文方法图、表格数字或硬件设置。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 别名/来源 | 本文可核验含义 | 范围 | 来源 | 歧义/限制 |
|---|---|---|---|---|---|
| OmniFit | author-defined method name | 标题与摘要中的 training-free token-compression framework | omnimodal LLM inference | ICML poster abstract; OpenReview ID metadata | 算法细节未由 PDF 核验；不得与 arXiv:2604.21575 混淆 |
| LAHP | Layer-Adaptive Heterogeneity Profiling | 摘要称其按层冗余与模态偏好动态分配计算预算 | profiling stage | ICML poster abstract | 具体统计量、采样方式、预算公式与 profiling 开销未知 |
| ARTS | Alignment-Rectified Token Selection | 摘要称其选取与跨模态线索语义对齐的 token | inference token selection | ICML poster abstract | alignment score、候选集合与保留规则未知 |
| profiling–execution decoupling | 摘要表述 | 将 interaction profiling 与 inference execution 分离 | system workflow | ICML poster abstract | 是否离线、每模型/每任务/每样本运行以及摊销成本未知 |

### 0.1.2 符号表

符号不适用：本次没有可读 PDF/source，且本报告没有引入需要当作论文公式证据的分析符号。摘要中的百分比与倍数是 claim 数字，不足以重建作者公式。

## 1. 论文基本信息

- 精确标题：*OmniFit: Bridging Modalities via Layer-Adaptive Token Compression for Omnimodal Large Language Models*
- OpenReview forum ID：`8RY20mLzup`
- 官方 ICML 页面：poster `65962`，关联 Spotlight presentation `84897`
- 作者：Zining Wang, Zhihang Yuan, Yingjie Zhai, Wenshuo Li, Han Shu, Ruihao Gong, Jinyang Guo, Xianglong Liu
- venue/status：ICML 2026 Spotlight（由 ICML official poster relation 与公开 OpenReview metadata 一致支持）
- affiliations：未从当前可访问的官方页面获得，不能猜测
- final revision、decision note、public reviews、rebuttal：OpenReview challenge/403 阻断，未核验
- 明确排除：arXiv:2604.21575 不是本次替代来源，未被用作证据

核心问题按摘要是：连续视频、音频与文本造成长 token 序列和高计算成本，而既有压缩常依赖单一模态先验或统一保留率，忽略层间异质性和跨模态对齐。

## 2. 核心贡献与创新点

下列仅是“摘要声明”，不是已由全文实验验证的结论：

1. training-free OmniFit 框架，将 profiling 与 execution 解耦。
2. LAHP：按层冗余及模态偏好分配 token/计算预算。
3. ARTS：以跨模态对齐信号修正 token 选择。
4. 摘要声明在 3 个模型系列、10 个 benchmark 上，以 20% token 保留 98% 性能，并达到最高 2.31× end-to-end speedup 与 2.5× VRAM saving。

## 3. 研究方法

### 3.1 问题到方案的逻辑链

长流式多模态序列 → attention/activation 成本随 token 数增大 → 固定或模态偏置压缩无法适配层间差异 → LAHP 给出层/模态预算，ARTS 用跨模态线索选 token → 预期减少后续层 token，同时降低语义损失。最后一步是摘要层因果主张；无全文公式、消融或代码可验证。

### 3.2 设计动机与具体问题映射

| 设计项 | why 状态 | 原文证据 | 针对问题 | 可能因果机制 | 替代方案/权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|---|
| profiling–execution decoupling | author-stated | ICML poster abstract | 在线推理中反复 profiling 可能增加开销 | 预先/独立测量后复用预算，降低 execution 热路径成本 | 在线样本自适应更灵活但有额外延迟 | none | unverified |
| LAHP | author-stated | ICML poster abstract | uniform retention 忽略层间冗余和模态偏好 | 把预算集中到更敏感层/模态，压缩更冗余部分 | 固定层级比例简单可复现；动态分配增加 profiling 与泛化风险 | none | unverified |
| ARTS | author-stated | ICML poster abstract | 仅靠单模态重要性可能删除跨模态关键 token | alignment cue 提高语义相关 token 的保留概率 | attention-only、similarity/diversity selection 成本更低但可能偏置 | none | unverified |
| training-free insertion | author-stated | ICML poster abstract | 训练/微调增加部署成本 | 在推理路径中选择 token，复用原模型权重 | 无训练易部署，但压缩策略可能缺少任务适配 | none | unverified |

### 3.3 模型/系统架构

无法核验。没有机制图、层插入位置、KV-cache 行为、prefill/decode 边界或压缩后 position handling 的可读证据。

### 3.4 关键公式

无法核验：PDF/source 不可读，因此不重建 LAHP budget、ARTS alignment score 或 token retention 公式。

### 3.5 训练/实验/部署设计

摘要只说明 training-free、3 model series、10 benchmarks。数据集名称、prompt/template、输入长度、token ratio 定义、baseline 预算、公平性、精度聚合方式、硬件、batch size、dtype、warmup 和 latency 测量均未知。

## 4. 关键结论

### 4.1 主结果

| 摘要 claim | 可访问证据 | 所需匹配证据 | 状态 |
|---|---|---|---|
| 20% token 保留 98% model performance | ICML poster abstract | 主表、指标聚合、模型/benchmark 明细、baseline 与 ratio 定义 | blocked |
| up to 2.31× end-to-end inference speedup | ICML poster abstract | latency table、硬件、batch、输入/输出长度、warmup、测量范围 | blocked |
| up to 2.5× VRAM saving | ICML poster abstract | peak/allocated VRAM 定义、模型、dtype、batch、输入长度、缓存设置 | blocked |

这些数字是摘要原文 claim，不能被当作已复核的实验事实。

### 4.2 技术点证据矩阵

| 技术点 | 声称收益 | 对应实验/消融 | 控制性 | 证据强度 | 结论 |
|---|---|---|---|---|---|
| LAHP layer/modality budget | 更好性能-效率权衡 | 不可访问 | unknown | none | unverified |
| ARTS cross-modal selection | 保留跨模态语义 token | 不可访问 | unknown | none | unverified |
| profiling/execution separation | 降低在线开销 | 不可访问 | unknown | none | unverified |
| full OmniFit | 20% tokens / 98% performance | abstract only | confounded | summary claim only | unverified |
| runtime/memory | 2.31× / 2.5× | abstract only | unknown | none | unverified |

### 4.3 假设验证与收益归因

没有可读消融、替换 baseline、敏感性图或系统表，不能区分 LAHP、ARTS、压缩比例、kernel/runtime 与模型/任务差异的贡献。最低复现实验应包含：固定同一 token ratio 的 uniform 与 LAHP；固定 LAHP 的 ARTS 替换；profiling 成本计入/摊销；相同硬件、dtype、batch 和序列长度的 end-to-end latency/VRAM。

## 5. Related Work 对比

摘要只给出两个相关类别：依赖 modality-centric priors 的方法与 uniform retention 方法。无法访问 bibliography 和具体 baseline，故不能审计比较公平性或建立论文级 related-work 对照。

## 6. OpenReview 公开评审 × 论文内容交叉核验

- OpenReview：`https://openreview.net/forum?id=8RY20mLzup`
- 访问日期：2026-07-24
- decision/meta-review/reviews/rebuttal：HTTP 403 / browser challenge，均未读取

| 来源 | 观点/问题 | 对应 claim | 证据 | 状态 | 判断 |
|---|---|---|---|---|---|
| public forum record | 无可读 review note | 全文方法与实验 | `openreview_reviews.md` 记录 403/challenge | unclear | 不能声称 reviewer 支持、反对或 rebuttal 已解决任何问题 |

## 7. Infra 需求分析

仅能做范围判断，不能给出已验证数值。token compression 理论上减少后续层 attention/MLP activation 和 KV-cache 流量；实际收益取决于压缩发生层、保留 token 的 gather/scatter、动态 shape、kernel fusion、cache layout 与 scheduler。硬件型号、dtype（fp32/fp16/bf16/fp8/int8 等）、有效带宽、峰值利用率、CPU/GPU/NPU 分工、互联与自定义算子均未报告在可访问摘要中，因此 2.31×/2.5× 不能归因到算法或系统优化。

## 8. 开源代码对照

官方 ICML poster 与可访问作者 publication 页面未给出 OmniFit code link；任务包也标为 unknown。未获得官方仓库、commit、checkpoint 或 config，因此所有实现行为（profiling pipeline、budget schedule、alignment score、token gather、KV cache、serving）均为 unavailable，不能由摘要推断。

## 9. 优点与局限

摘要呈现的优点是把 layer heterogeneity 与 cross-modal alignment 同时纳入 training-free compression。核心局限是本交付没有精确 PDF/source/reviews/code，无法验证任何公式、表格、硬件或消融；因此只能确认身份与摘要声明，不能把性能和系统数字提升为 survey established evidence。

## 10. 研究启发

可复现时应把“profiling 学到的预算是否跨样本/任务/输入长度泛化”作为首要问题，并拆分 algorithm-only token quality、profiling amortization 与 runtime kernel 效果。

## 11. 解读问题/待验证清单

1. LAHP 的冗余和模态偏好如何定义，预算约束与层间更新公式是什么？
2. ARTS alignment score 使用哪些 query/key/token，在哪一层计算，复杂度是多少？
3. profiling 是否离线、每模型、每 benchmark 或每样本执行？
4. 20% token 与 98% performance 的聚合口径、方差和最差任务是什么？
5. 2.31× 和 2.5× 分别在哪个模型、硬件、dtype、batch、输入长度与 runtime 上测量？
6. LAHP、ARTS 与 profiling separation 是否有独立 matched ablation？
7. 官方代码、commit、config 与 checkpoint 是否发布？
8. decision、review 与 rebuttal 是否对 novelty、公平 baseline、profiling 成本或系统测量提出未解决问题？

## 12. 一句话总结

本次已把 OmniFit 精确定位为 OpenReview `8RY20mLzup`、ICML 2026 Spotlight poster `65962`，但精确 PDF/source/review/code 均未取得；20%/98%/2.31×/2.5× 只能作为未复核摘要声明，交付必须保持 blocked。
