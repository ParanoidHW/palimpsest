# 调研知识组织规范

> [!info] 规范层级
> 本文件是当前仓库的补充 policy，由根目录 `research-knowledge.profile.json` 绑定。可移植的节点类型、默认目录、关系、owner、promotion 和验证语义由项目 skill `research-knowledge-publisher` 内建的 organization schema 定义；本文件负责本仓库的具体约束、解释和示例。仓库没有本文件时，skill 仍可使用内建默认 organization；本文件不得静默放宽内建的可追溯与过程隔离约束。

本规范适用于 literature survey、paper deep review、research synthesis、论文图表提取，以及相应 Markdown、PPT、HTML 和资产的新增、迁移与维护。目标是让每条汇总结论都能沿着“领域入口 -> 汇总调研 -> 单篇精读 -> 图表证据”追溯，同时把检索和渲染过程与正式知识库分开。

## 1. 标准目录与职责

正式调研领域使用以下结构：

```text
<domain>/
├── README.md
├── surveys/
├── papers/
├── topics/
├── evidence/
├── supplements/
└── assets/
    ├── surveys/<survey-slug>/
    └── papers/<paper-slug>/
```

| 位置 | 唯一职责 |
| --- | --- |
| `README.md` | 领域入口、推荐阅读路径、完整正式文档索引；不承载长篇技术分析。 |
| `surveys/` | 跨论文归纳、分类、时间线、趋势、比较与工程判断。 |
| `papers/` | 单篇论文的公式、实现、实验、证据边界与局限。 |
| `topics/` | 跨论文概念、数据、管线和背景知识；不承载单篇实验结论。 |
| `evidence/` | 选篇依据、论文索引、figure inventory、证据矩阵和可追溯元数据。 |
| `supplements/` | PPT、HTML 和不属于 canonical Markdown 的补充讨论。 |
| `assets/` | 正式文档引用且由 Git 跟踪的图表资产，按 survey 或 paper 的 canonical owner 归档。 |
| `_artifacts/` | PDF、源码快照、整页渲染、裁剪过程、QA、检索缓存和执行日志；不是正式知识入口。 |

空目录不需要占位文件；只有出现对应类型内容时才创建。

## 2. 命名规则

- Markdown 文件和资产目录使用稳定、简短、全小写 kebab-case slug，例如 `deepseek-v4.md`、`speculative-tree-drafting.md`。
- slug 表达稳定主题或论文简称，不嵌入版本号、日期戳、中文全标题或“精读分析”等可变描述。
- 论文完整标题、作者、venue、年份和 arXiv ID 保留在正文资料区；arXiv ID 不替代 slug。
- 图片名使用 `<figure-or-table>-<semantic-description>.<ext>`，例如 `fig2-routing-overview.png`、`table1-latency.png`；不得使用 `Pasted image ...`、`image1.png` 等无语义名称。
- 同一论文的新版本沿用 paper slug；正文记录核验版本。只有方法本身成为独立工作时才创建新 slug。

## 3. 关系模型

正式知识链路为：

```text
README -> canonical Survey -> Paper -> Asset
   |              |            |
   +----------> Topic          +-> Evidence
   +----------> Evidence
```

- README 必须链接全部 canonical survey、topic、paper 和关键 evidence/index。
- Survey 的主要论文结论必须链接到对应 Paper，优先定位到具体章节锚点。
- Paper 必须反向链接领域 README 和父级 Survey；若由 Index 而非 Survey 收录，也需链接该 Index。
- Survey 只保留跨论文比较和综合判断；Paper 保留单篇完整证据，避免两处复制整段分析。
- Topic 解释跨论文概念、数据或管线，不将某篇论文的实验数字写成通用事实。
- Evidence 记录“为何选、证据在哪里、如何得到”，不替代 Survey 或 Paper 的分析正文。
- 每张图片只有一个 canonical owner 和一个权威文件位置。其他文档通过相对路径跨文档引用，不复制文件。

## 4. 文档关系区块

每篇 Survey、Paper、Topic 和 Evidence 在一级标题后使用以下区块；不适用项写“无”或删除该行，不保留错误链接。

```markdown
> [!info] 文档关系
> - 文档类型：Survey / Paper / Topic / Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Survey](../surveys/example.md)
> - 证据资产：`../assets/papers/example/`
> - 相关文档：[Evidence](../evidence/figure-inventory.md)
```

README 不需要关系区块，但必须在开头说明领域范围，并提供“阅读路径”和“文档索引”。

## 5. 资产归属

- 原论文图表归属单篇 Paper：`assets/papers/<paper-slug>/`。
- Survey 自制的时间线、分类图和跨论文汇总图归属 Survey：`assets/surveys/<survey-slug>/`。
- AI 生成或人工绘制的解释图必须在 caption 或邻近正文标明“生成图/整理图”，不得伪装为原论文证据。
- PDF 页面、整页截图、contact sheet、未裁剪图片、OCR、临时转换文件和 QA 截图只放 `_artifacts/`。
- 一个资产被多篇文档使用时，仍只保留 canonical owner 的一份；引用方使用跨目录相对路径。
- 正式文档不得链接 `_artifacts`、绝对本地路径、未跟踪文件或临时 page render。

## 6. Figure Inventory 与视觉 QA

引用原论文 Figure/Table 前，在 `evidence/figure-inventory.md` 或等价领域清单中记录：

| 字段 | 要求 |
| --- | --- |
| Paper | paper slug、完整标题或可定位简称。 |
| Object | 原编号，例如 Figure 3、Table 1。 |
| Source | 论文版本、PDF 页码；有源码时记录源文件。 |
| Caption | 完整原 caption，或不改变含义的完整中文转述并标明转述。 |
| Crop | 正式资产相对路径和 crop bbox（`x0,y0,x1,y1`，注明坐标系/分辨率）。 |
| Usage | 支撑的正文结论和引用文档。 |
| QA | 原分辨率检查结果、检查日期；必要时记录替换历史。 |

每张正式论文图必须满足：只包含一个编号对象、caption 完整、边界紧凑但不截断 legend/axis/注释、分辨率可读。逐图以原分辨率检查；contact sheet 只能初筛，不能替代逐图 QA。

## 7. Promotion Checklist

将 `_artifacts` 内容提升为正式知识前逐项确认：

- [ ] 已确定 domain、doc type、slug 和 canonical owner。
- [ ] 分析正文已移入 `surveys/`、`papers/`、`topics/` 或 `evidence/`。
- [ ] 正式引用图已移入 owner 对应的 `assets/`，过程文件留在 `_artifacts`。
- [ ] 已补文档关系区块和 README 索引。
- [ ] Survey 结论已链接 Paper；Paper 已反链 Survey/README。
- [ ] Figure inventory 含 caption、页码、bbox 和逐图 QA。
- [ ] 所有正式路径为可解析的 Git-tracked 相对路径。
- [ ] 正式文档已清除 `_artifacts`、page render 和绝对路径引用。

## 8. 标准落盘流程

1. **检索**：查询日志、候选库、PDF、网页快照和源码进入 `_artifacts/<task>/`。
2. **筛选**：在 artifacts 中形成候选与排除理由；确定入选后，将稳定版本提升到 `evidence/selection.md`。
3. **精读**：每篇入选论文形成独立 `papers/<slug>.md`，记录版本、证据边界、公式、实现、实验和局限。
4. **图表**：整页渲染和裁剪过程留在 artifacts；通过 QA 的单一对象进入 `assets/papers/<slug>/`，并更新 figure inventory。
5. **汇总**：在 `surveys/<slug>.md` 写跨论文比较，主要结论链接到 Paper 章节，不复制精读全文。
6. **连接**：更新 README 阅读路径和完整索引，为 Paper 建立父级 Survey/Index 反链。
7. **交付**：Markdown 进入对应 doc type；PPT/HTML 进入 `supplements/`，引用同一正式资产，不复制临时截图。
8. **验证**：运行链接、锚点、资产、Git 跟踪、孤立项和 forbidden-reference 检查后再提交。

## 9. Markdown、PPT 与 HTML

- canonical 技术内容必须有 Markdown 版本；PPT/HTML 是补充交付件，不是唯一知识载体。
- Survey/Topic/Paper Markdown 分别进入其职责目录；PPT 和专题 HTML 进入 `supplements/`。
- PPT 构建脚本、渲染 PNG、缩略图、QA 报告与日志留在 `_artifacts`；最终 `.pptx` 进入 `supplements/`。
- HTML 若是最终可读补充件可进入 `supplements/`；其构建缓存和截图仍留在 `_artifacts`。
- 交付件只能引用 Git-tracked 的正式资产；不能依赖作者机器的绝对路径或 artifacts 临时目录。

## 10. 完成前验证

至少检查以下项目：

1. Markdown 相对链接目标存在，带 `#anchor` 的链接能解析到目标标题。
2. Markdown/HTML/PPT 所引用的正式资产存在且被 Git 跟踪。
3. 正式知识目录不含 `_artifacts`、绝对路径、page render 或未跟踪目标引用。
4. 每篇 Paper 至少被 README 和一个 Survey/Index 引用。
5. 每个 Survey 的主要单篇结论都有 Paper 证据入口。
6. 没有未解释的孤立正式文档；孤立资产要么补引用/清单，要么移回 artifacts。
7. 根 README 和根 `AGENTS.md` 都能链接本规范。

验证器无法理解的动态链接或特殊 Obsidian 语法应人工复核，并在提交说明中记录例外，不能静默忽略。

## 11. Git 规则

- 按领域独立提交：meta、各 domain 迁移和内容修订不混在一个提交中。
- 提交前检查 staged diff 和 staged 文件列表，确保领域边界清晰。
- 不自动提交无关工作区改动、编辑器状态、生成缓存或 EOL-only 变化。
- 移动使用 Git 可识别的 rename；不保留旧路径 redirect stub，全库更新内部链接。
- 不通过复制规避 rename，也不删除用户未提交的内容改动。

## 12. 最小合规示例

```text
example_domain/
├── README.md
├── surveys/
│   └── inference-evolution.md
├── papers/
│   └── example-method.md
├── evidence/
│   ├── paper-index.md
│   └── figure-inventory.md
├── supplements/
│   └── inference-evolution.pptx
└── assets/
    ├── surveys/inference-evolution/timeline.png
    └── papers/example-method/fig2-overview.png
```

`README.md` 同时链接 survey、paper 和 evidence；`surveys/inference-evolution.md` 的 Example Method 结论链接 `../papers/example-method.md#核心机制`；Paper 顶部反链 README 与 Survey，并引用 `../assets/papers/example-method/fig2-overview.png`；figure inventory 记录该图的 caption、页码、bbox 与 QA。PPT 使用同一正式图片，构建和渲染过程保留在 `_artifacts`。
