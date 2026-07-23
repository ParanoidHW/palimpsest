# AI 算法领域综述模板

用于 `ai-algorithm-survey` 的 `synthesis.md`。根据实际任务删减空节，但不要删除证据、选择依据和局限性部分。

## 修订信息

- 当前文档版本：`<semver, e.g. 1.0.0>`
- 当前修订 ID：`<rev-...>`
- 当前修订时间：`<ISO 8601 datetime>`
- 替代版本：`<previous version/revision/manifest sha256 or none for initial>`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `<rev-id>` | `<version>` | `<datetime>` | `<agent task/name or human role>` | `<initial/migration/migration-resolution/content-update/evidence-update/correction/format-only/mixed>` | `<tracked revision+version+hash / legacy hash / unresolved recovery record / none>` | `<issue-id + attempts / recovered legacy manifest / none>` | `<what changed>` | `<why>` | `<synthesis.md#section; artifact paths>` | `<user request/source/validation evidence>` | `<none/minor/material>` |

全新交付记录 `initial`。接入旧交付时记录 `migration`：旧 manifest hash 可得时使用 `legacy-manifest`，允许旧版本/修订 ID 未知；若 hash 也无法恢复，记录稳定 `issue_id`、`unresolved` 和恢复尝试，并将交付标为 blocked。恢复后追加 `migration-resolution`，它既指向前一 blocked manifest，也把同一 issue ID 绑定到恢复出的 legacy manifest；不要改写原 unresolved 记录。此后继续只追加记录；冻结后的任何内容变化都必须递增版本、生成新的修订 ID、精确指向前一 manifest SHA-256，并重新计算交付 hash。

## 1. 领域与检索范围

- 用户输入领域：
- 规范化关键词：
- 检索日期：
- 检索来源：
- GitHub/awesome 来源：
- 引用/热度指标来源：
- 时间范围：
- 纳入/排除标准：

## 2. AI 生成趋势与 Infra 示意图

如果 `$openrouter-icu-image` 可用且已成功生成图片，在这里插入。该图用于概括算法整体趋势和软硬件 infra 需求维度，不替代证据表格。

![AI-generated survey trends and infra diagram](figures/generated/survey-trends-infra.png)

> 图注：AI 生成的浅金色扁平化技术示意图，基于本文综述 Markdown 生成，用于呈现算法演进、方法族分支、高价值论文锚点，以及数据/训练/推理/serving/kernel/算力/显存/带宽/互联/部署等软硬件 infra 维度。

## 3. 术语与符号解释

将跨论文术语和符号统一集中在本节，不要把定义散落在时间线、方法谱系或各论文小节。统一字段级术语时保留各论文的特定用法；同一符号在不同论文中含义不同时逐篇列出，禁止强行合并。

### 3.1 术语表

| 术语 | 综述中的规范解释 | 定义性质 | 别名 | 各论文的特定用法 | 规范解释来源 | 易混点 |
|---|---|---|---|---|---|---|
| `<term>` | `<canonical definition>` | `<paper-stated/cross-paper-synthesis>` | `<aliases or none>` | `<paper: usage>` | `<paper/section/code>` | `<ambiguity>` |

### 3.2 符号表

| 符号 | 来源类型 | 论文/综述 | 含义 | 作用域/索引 | 单位/取值 | 证据或推导来源 | 易混点 |
|---|---|---|---|---|---|---|---|
| `<symbol>` | `<paper-specific/survey-analysis>` | `<paper/survey synthesis>` | `<meaning>` | `<scope/indexing>` | `<unit/range>` | `<equation/section/table/analysis derivation>` | `<ambiguity>` |

只有当每个已接受单篇 manifest 都将符号标记为 `not-applicable`，且综述自身也未引入分析推导符号时，才写“符号不适用”。否则保留每篇论文的符号及其特定含义，即使该符号没有跨论文重载；不要虚构条目，也不要因无法统一而删除。

## 4. GitHub/awesome 资源

| 仓库/列表 | URL | Stars/Forks | 更新线索 | 相关小节 | 贡献的候选论文/子领域 | 可信度备注 |
|-----------|-----|-------------|----------|----------|------------------------|------------|
| | | | commit/release/README 更新日期 | | | |

## 5. 高热度/高价值信号

| 论文 | 引用数/来源 | 候选集交叉引用次数 | GitHub 热度 | awesome/list 出现次数 | 价值判断 | 证据备注 |
|------|-----------|----------------------|-------------|--------------------|----------|----------|
| | | | stars/forks/更新 | | 高学术影响/高工程采用/概念锚点/新兴高热度 | |

## 6. 候选论文概览

| 年份 | 论文 | venue/status | 归属机构/高校 | 热度/价值信号 | 角色 | 纳入/排除 | 原因 |
|------|------|--------------|----------------|----------------|------|-----------|------|
| | | | | | | | |

## 7. 组织/高校分布

| 机构/高校 | 类型 | 相关论文 | 贡献主题 | 备注 |
|-----------|------|----------|----------|------|
| | university/company/lab | | | |

## 8. 入选论文时间线

| 年份 | 论文 | 归属机构/高校 | 核心问题 | 设计动机 | 替代方案/权衡 | 关键机制 | 热度/价值信号 | 相比前作的变化 |
|------|------|----------------|----------|----------|---------------|----------|----------------|----------------|
| `<year>` | `<paper>` | `<affiliation>` | `<problem>` | `<author-stated/inferred/not-stated>` | `<alternatives/trade-offs>` | `<mechanism>` | `<impact>` | `<change>` |

## 9. 方法谱系与关联

| 起点工作 | 后续工作 | 关系类型 | 继承内容 | 改动内容 | 动机/目标问题如何变化 | 是否交叉引用 | 证据 |
|----------|----------|----------|----------|----------|----------------------|--------------|------|
| `<earlier>` | `<later>` | 扩展/替代/对比/消融/基准 | `<inherited>` | `<changed>` | `<motivation/problem shift>` | 是/否 | `<source>` |

## 10. 横向对比

| 论文 | 归属机构/高校 | 问题设定 | 为什么这样设计 | 解决的具体问题 | 因果机制 | 替代方案/权衡 | 数据/benchmark | 主要指标 | 系统/计算代价 | 优势 | 局限 |
|------|----------------|----------|----------------|----------------|----------|---------------|----------------|----------|---------------|------|------|
| `<paper>` | `<affiliation>` | `<setting>` | `<rationale status/source>` | `<specific problem>` | `<causal mechanism>` | `<alternatives/trade-offs>` | `<data>` | `<metrics>` | `<cost>` | `<strength>` | `<limitation>` |

## 11. 技术演进趋势

### 11.1 问题定义如何变化

### 11.2 设计动机与目标问题如何变化

区分论文明确写出的动机、跨论文推断的动机和没有说明的动机。说明每个关键设计针对的具体失败模式/瓶颈、当时可用的替代方案与权衡，以及后续论文是否验证、修正或替换了这条设计逻辑。

### 11.3 模型/算法结构如何变化

### 11.4 训练目标、数据构造或监督信号如何变化

### 11.5 推理、部署或系统代价如何变化

### 11.6 评测协议与 benchmark 如何变化

### 11.7 主要研究组织如何推动分支演化

### 11.8 高热度论文如何影响后续分支

## 12. 软硬件 Infra 需求维度

| 维度 | 需求/瓶颈 | 关联方法族/论文 | 演进趋势 | 证据 |
|------|-----------|----------------|----------|------|
| 数据管线 | | | | |
| Data types / 数值格式 | fp32/fp16/bf16/fp8/int8/int4/稀疏/混合精度等格式如何影响精度、显存、吞吐和硬件依赖 | | | |
| 训练框架/并行策略 | | | | |
| 推理 runtime / serving | | | | |
| kernel/operator | | | | |
| 算力 | | | | |
| CPU/GPU/NPU 异构 | CPU preprocessing/postprocessing、GPU/NPU kernel、host-device transfer、异步 copy、fallback path、调度 placement | | | |
| 显存/内存容量 | | | | |
| 带宽/互联 | HBM/DDR/PCIe/NVLink/RDMA/all-reduce/all-to-all 等通信路径 | | | |
| 高效带宽利用 | memory locality、cache reuse、tiling、fusion、通信/计算 overlap、压缩传输、有效带宽/峰值带宽利用率 | | | |
| 存储/数据加载 | | | | |
| 部署约束 | | | | |

## 13. 当前共识与分歧

- 共识：
- 分歧：
- 不同论文之间不可直接比较的原因：

## 14. 后续研究方向

| 方向 | 动机 | 可能方法 | 风险/难点 | 关联论文 |
|------|------|----------|-----------|----------|
| | | | | |

## 15. 证据与局限性

- 明确来自论文正文的结论：
- 来自代码/配置检查的结论：
- 推断性结论：
- AI 生成示意图状态与局限：
- 机构/高校归属来源与不确定性：
- GitHub/awesome 来源的更新性和偏差：
- GitHub stars/forks、引用数、交叉引用频率的来源与时间戳：
- 检索或访问限制：
- 尚未解决的阅读问题：
