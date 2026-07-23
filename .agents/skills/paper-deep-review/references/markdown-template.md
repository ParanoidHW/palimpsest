# Markdown Paper Review Template

Use this template for Chinese paper-review deliverables. Adapt headings when the user gives a stricter format, but preserve the evidence discipline.

```markdown
# <Paper Title> 精读分析

> 资料状态：说明 PDF/LaTeX/source/code 是否存在；说明图片来自原始素材还是 PDF 截图裁剪。

## 修订信息

- 当前文档版本：`<semver, e.g. 1.0.0>`
- 当前修订 ID：`<rev-...>`
- 当前修订时间：`<ISO 8601 datetime>`
- 替代版本：`<previous version/revision/manifest sha256 or none for initial>`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `<rev-id>` | `<version>` | `<datetime>` | `<agent task/name or human role>` | `<initial/migration/migration-resolution/content-update/evidence-update/correction/format-only/mixed>` | `<tracked revision+version+hash / legacy hash / unresolved recovery record / none>` | `<issue-id + attempts / recovered legacy manifest / none>` | `<what changed>` | `<why>` | `<analysis.md#section; artifact paths>` | `<user request/source/validation evidence>` | `<none/minor/material>` |

全新交付记录 `initial`。接入旧交付时记录 `migration`：旧 manifest hash 可得时使用 `legacy-manifest`，允许旧版本/修订 ID 未知；若 hash 也无法恢复，记录稳定 `issue_id`、`unresolved` 和恢复尝试，并将交付标为 blocked。恢复后追加 `migration-resolution`，它既指向前一 blocked manifest，也把同一 issue ID 绑定到恢复出的 legacy manifest；不要改写原 unresolved 记录。此后继续只追加记录；冻结后的任何内容变化都必须递增版本、生成新的修订 ID、精确指向前一 manifest SHA-256，并重新计算交付 hash。

## 0. 资料与配图索引

- 论文：`<path>`
- 源码/LaTeX：`<path or unavailable>`
- 开源代码：`<repo url>`, commit `<hash>`
- OpenReview：`<url or unavailable>`；公开评审/decision/rebuttal：`<path or unavailable>`
- 提取文本：`<path>`
- 图表：列出 Figure/Table 与本地图片路径；标明截图是否包含完整 caption，边距是否已经裁成窄边界。
- AI 生成分析示意图：`<figures/generated/algorithm-analysis.png or unavailable>`

## 0.1 术语与符号解释

将术语与符号集中在本节，不要把定义散落在方法、实验和 Infra 各节。所有条目均给出论文或代码来源，并显式说明同名异义、符号复用或论文表述不一致之处。

### 0.1.1 术语表

解释论文中特定含义的术语，尤其是容易误读的训练数据、模型角色、mask、budget、benchmark 设定。

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| `<term>` | `<definition in this paper>` | `<aliases or none>` | `<what it is not>` | `<Section/Table/Code>` |

### 0.1.2 符号表

每篇论文的符号可能不同，先澄清再解释公式。覆盖核心公式、指标、表格和系统量。

| 符号 | 含义 | 性质 | 作用域/索引 | 单位/取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|
| `<symbol>` | `<meaning>` | `<author-defined/code-defined/analysis-derived>` | `<global/per-layer/per-token/per-request>` | `<unit/range>` | `<Eq./Section/Table/analysis derivation>` | `<ambiguity>` |

仅当论文、代码和本分析中的推导公式都没有需要解释的数学/系统符号时，明确写“符号不适用”；不要虚构符号条目。

## 0.2 AI 生成算法分析示意图

如果 `$openrouter-icu-image` 可用且已成功生成图片，在这里插入。该图只能作为分析辅助，不替代论文原图、表格或实验数据。

![AI-generated algorithm analysis diagram](figures/generated/algorithm-analysis.png)

> 图注：AI 生成的扁平化算法分析示意图，基于本文 Markdown 分析生成，用于概括方法机制、证据链、技术点消融支撑、关键局限和 infra 影响；不代表论文原始图表。

## 1. 论文基本信息

- 研究领域：
- 核心问题：
- 研究目标：
- 关键约束/假设：

## 2. 核心贡献与创新点

列出 3-5 个贡献。每个贡献说明：
- 解决什么问题
- 与已有方法的差异
- 证据来源：Section/Figure/Table

## 3. 研究方法

### 3.1 问题到方案的逻辑链

用简洁链条说明：问题 -> 约束 -> 方法设计 -> 预期收益。

### 3.2 设计动机与具体问题映射

不要只写“采用了什么模块/损失/数据/推理策略”。逐项回答论文是否解释了为什么这样设计、要解决哪个具体失败模式或瓶颈、设计通过什么因果机制起作用，以及实验是否真的验证了这条解释。

| 设计项 | 论文是否明确说明 why | 原文证据 | 针对的具体问题/失败模式 | 可能起作用的因果机制 | 替代方案/权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|---|
| `<component/objective/data/inference/kernel>` | `<author-stated / inferred / not-stated>` | `<Section/Equation/Figure/Appendix/none>` | `<specific bottleneck, ambiguity, constraint, baseline weakness>` | `<why this design could address that problem>` | `<alternative and trade-off>` | `<ablation/control/theory/code/none>` | `<supported/partially supported/plausible/unverified>` |

当论文没有明确给出设计动机时，写 `not-stated`；如果根据公式、图、实验或代码推断，写 `inferred` 并说明推断依据。不要把推断改写成作者原意。

### 3.3 模型/系统架构

嵌入关键示意图。

### 3.4 关键公式

使用 LaTeX：

$$
<formula>
$$

解释公式中的变量、单位、系统含义。
公式中的每个变量都必须能在“0.1.2 符号表”中找到；如果论文复用了符号或符号含义不一致，在这里显式说明。

### 3.5 训练/实验/部署设计

说明数据、baseline、公平性设置、指标、实现假设。
对训练数据构造、teacher/student、target/draft、生成温度、prompt/chat template、过滤规则等信息做事实-缺口分离：论文明确报告什么，代码/配置确认什么，仍未知什么。

## 4. 关键结论

### 4.1 主结果

嵌入主表/主图，说明：
- 指标是什么
- 数字来自哪里
- 结论如何由数据推出

### 4.2 消融和机制证据

按 Figure/Table 解释，避免只复述 caption。

先把论文声称的技术点逐一列出来，再判断是否有消融实验或受控证据支撑其收益。不要把“完整方法优于 baseline”直接等同于“每个技术点都有效”。

| 论文声称的技术点 | 声称收益/效果 | 对应实验/消融 | 对照是否受控 | 指标变化 | 证据强度 | 结论 |
|---|---|---|---|---|---|---|
| `<component/objective/data/inference/kernel>` | `<claimed benefit>` | `<Table/Figure/Appendix/none>` | `<matched/confounded/unknown>` | `<delta>` | `<direct ablation / replacement baseline / sensitivity / mechanism visualization / theory / code-only / none>` | `<supported/partially supported/unverified/correlation-only>` |

对没有消融的核心技术点，说明缺少什么最小实验，例如移除该模块、替换为常规模块、固定其他变量的训练预算对比、不同规模/数据域敏感性分析、或 runtime-only 与 algorithm-only 分离实验。

### 4.3 是否验证了假设

逐条对应论文假设、方法设计和实验结果。

### 4.4 收益来源归因

基于上面的技术点证据矩阵做归因。分开说明每个组件影响的是候选质量、accepted length、latency、memory，还是 serving throughput。

| 组件/变化 | 对比基线 | 指标变化 | 影响路径 | 证据强度 |
|---|---|---|---|---|
| `<component>` | `<baseline>` | `<absolute/relative delta>` | `<quality/latency/memory>` | `<matched ablation / rough inferred decomposition>` |

如果使用桥接 baseline 做粗分解，明确写“这是基于表格的近似归因，不是论文正式方差分解”。

## 5. Related Work 对比

| 类别/论文 | 方法核心 | 优点 | 局限 | 与本文关系 |
|---|---|---|---|---|
| <work> | <mechanism> | <benefit> | <limit> | <contrast> |

## 6. OpenReview 公开评审 × 论文内容交叉核验

如果论文没有公开 OpenReview 页面，写“未发现公开 OpenReview 评审”并跳过表格。不要把 reviewer 意见当作事实或独立结论；必须逐条核对论文正文、appendix、rebuttal、代码和实验，并把结论回填到方法、实验、局限、代码或 infra 相关章节。

- OpenReview 链接：
- 评审/讨论访问日期：
- decision/meta-review 状态：
- author response/rebuttal 状态：

| 来源 | 评审观点/约束/潜在问题 | 对应论文 claim/实验 | 论文/appendix/rebuttal/代码证据 | 状态 | 交叉核验后的判断 |
|---|---|---|---|---|---|
| `<review/meta-review/comment>` | `<claim>` | `<Section/Fig/Table/Eq/Code>` | `<evidence>` | `<resolved/partial/unresolved/unclear>` | `<是否实质削弱贡献、缩小适用范围、需要补实验或属于误解>` |

### 6.1 与论文证据一致的正向评价

说明哪些 reviewer 正向评价能被论文实验、理论、代码或 benchmark 证据支撑。

### 6.2 经核验仍成立的主要担忧

重点分析 novelty、正确性、baseline 公平性、消融充分性、数据泄漏、指标选择、理论假设、复现性、清晰度、伦理/安全和部署约束。

### 6.3 Rebuttal/Revision 是否真正解决问题

区分作者已回应且有证据解决的问题、只做口头解释的问题、仍未解决的问题，以及可能来自 reviewer 误解的问题。

### 6.4 对本文贡献、适用范围和潜在风险的影响

把评审线索转化为论文级判断：哪些问题会削弱核心结论，哪些只是限制外推范围，哪些提示后续复现或扩展实验。

## 7. Infra 需求分析

分开写 paper-reported facts 与 inferred estimates。

### 7.1 算力

给出 FLOPs/latency/throughput 公式。

### 7.2 显存与存储

给出参数量、activation、cache、数据缓存公式。

### 7.3 Data Types / 数值格式

记录论文或代码实际使用的数据类型和格式：fp32、fp16、bf16、fp8、int8、int4、binary/ternary、稀疏格式、混合精度、累加精度、量化/反量化、packing/unpacking、layout transform。说明收益是否依赖特定硬件指令、tensor core、NPU kernel 或定制算子。

| 对象 | 数据类型/格式 | 使用阶段 | 硬件依赖 | 对精度/速度/显存的影响 | 证据 |
|---|---|---|---|---|---|
| `<weights/activation/KV/logits/index/cache>` | `<bf16/int8/fp8/...>` | `<train/infer/serving>` | `<GPU/NPU/CPU/instruction>` | `<impact>` | `<paper/code/config>` |

### 7.4 带宽、互联与高效利用

给出通信量公式：

$$
\mathrm{Bytes}=<formula>
$$

不仅估算 raw bandwidth，还要估算/讨论有效带宽利用率：

$$
\mathrm{EffectiveBandwidth}=\frac{\mathrm{BytesMoved}}{\mathrm{RuntimeSeconds}},
\quad
\mathrm{Utilization}=\frac{\mathrm{EffectiveBandwidth}}{\mathrm{PeakBandwidth}}
$$

分析 memory locality、cache reuse、tiling、operator fusion、通信/计算 overlap、压缩传输、all-reduce/all-to-all、PCIe/NVLink/RDMA、HBM/DDR 访问，以及 bottleneck 是 memory-bound、compute-bound 还是 communication-bound。

| 路径 | 数据量 | 峰值带宽 | 有效带宽/利用率 | 优化机制 | 瓶颈判断 | 证据 |
|---|---:|---:|---:|---|---|---|
| `<HBM/PCIe/NVLink/RDMA/CPU-GPU>` | `<bytes>` | `<GB/s>` | `<GB/s or %>` | `<fusion/tiling/overlap/compression>` | `<memory/compute/comm>` | `<paper/code>` |

### 7.5 CPU/GPU/NPU 异构执行

分析方法是否依赖 CPU、GPU、NPU 或其他 accelerator 的异构协同，是否存在 host-device transfer、CPU preprocessing/postprocessing、GPU/NPU kernel、异步 copy、DMA、pinned memory、fallback path、调度 placement、pipeline overlap。

| 阶段 | CPU 角色 | GPU/NPU/加速器角色 | 数据移动 | 同步/overlap | 潜在瓶颈 | 证据 |
|---|---|---|---|---|---|---|
| `<preprocess/train/infer/serving/postprocess>` | `<role>` | `<role>` | `<path/bytes>` | `<sync/async>` | `<bottleneck>` | `<paper/code>` |

### 7.6 调度/Serving/自定义算子

说明 runtime、batching、scheduler、kernel、KV cache、CUDA graph 等需求。

## 8. 开源代码对照

- 仓库：
- commit：
- 代码范围：

| 论文机制 | 本地路径 | GitHub commit 链接 | 一致性判断 |
|---|---|---|---|
| <mechanism> | `<path>` | `<url>` | 一致/部分一致/未开源 |

明确说明 paper 技术细节不清楚时，源码如何补充；源码未覆盖时，不要过度推断。

### 8.1 开源权重/配置对照

当论文或 README 指向公开 checkpoint/model weights 时，检查 metadata/config，并与关键 baseline 做容量、结构、算法开关对比。

| 权重/Checkpoint | 公开状态 | revision/commit | 参数量 | 架构/层数/宽度 | 关键配置字段 | 与 baseline 的差异 |
|---|---|---|---:|---|---|---|
| `<model>` | `<open/gated/private/unknown>` | `<sha>` | `<params>` | `<layers/hidden/heads>` | `<flags>` | `<capacity/algorithm/runtime>` |

如果因为网络或权限无法读取配置，写明“未验证”，不要用 README 文字代替配置事实。

## 9. 优点与局限

### 优点

### 局限

### 可改进之处

## 10. 研究启发

- 可借鉴思路：
- 可延伸方向：
- 可复现实验：

## 11. 解读问题/待验证清单

这些问题用于后续复读、复现或组会讨论：

1. 论文真正优化的目标函数是什么？指标是否和目标一致？
2. 关键假设是否被实验直接验证，还是只被间接支持？
3. baseline 是否公平，是否同数据、同预算、同指标？
4. 论文是否明确解释每个核心设计为什么这样做？它针对的具体问题和因果机制是什么，还是仅由本文推断？
5. 主结果是否依赖某个特定数据域、模型规模或系统负载？
6. 消融是否足以证明每个模块必要？
7. 论文声称的每个技术点是否都有独立消融或受控对照？有没有多个改动被捆绑导致无法归因？
8. 公式中的概率、吞吐、显存或带宽估计是否有隐含单位和边界条件？
9. 论文声称的生产结果是否有足够 telemetry、SLA、负载说明？
10. 开源代码是否实现了论文核心算法，还是只实现训练/评测子集？
11. 哪些关键细节无法从论文或代码确认？
12. 如果要复现，最小闭环需要哪些数据、模型、硬件和脚本？
13. 如果有 OpenReview 公开评审，哪些 reviewer concerns 仍未被论文、rebuttal 或代码充分解决？

## 12. 一句话总结

用 1-2 句话说明本文最核心价值和最大不确定性。
```
