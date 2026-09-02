# Research Knowledge Rules

本文件只约束 literature survey、paper deep review、research synthesis、论文图表提取，以及对应 Markdown、PPT、HTML、assets 的新增、迁移和维护。

执行上述任务前，必须完整读取并遵守 [调研知识组织规范](00_meta/research-knowledge-organization.md)。详细解释只维护在该规范中。

- 在检索、选篇或派发 paper deep review 前，必须先查询 [Research Paper 与领域覆盖矩阵](00_meta/research-paper-coverage-matrix.md)，按标题、简称、arXiv ID、模型名和别名确认是否已有 canonical 分析。
- 已覆盖且证据版本一致时，优先 `link-only`、直接复用或增量修订；不得重复创建 Paper、复制资产或仅因新任务另建 slug。只有矩阵未命中或现有内容明确不足时才新建精读。
- 新增、迁移、合并、删除或实质更新正式 Paper 后，必须同步维护覆盖矩阵；domain 内容与 meta 规则/矩阵按边界分开提交。
- 创建文件前先确定 domain、doc type、slug 和 canonical owner。
- PDF、压缩源码归档和确需留存的证据过程文件只能进入 `_artifacts/`；展开的源码树、页面渲染、裁剪过程、QA、日志和代理生成的辅助脚本/过程文档默认使用系统临时目录，并在交付前删除。
- Obsidian vault 内禁止新增或残留嵌套的 `CLAUDE.md`、`AGENT.md`、`AGENTS.md` 等代理控制文件。外部源码中的同名文件只可保留在压缩归档内；交付前必须扫描 `_artifacts/`，清理代理生成的计划、提示词、检查表、临时 Markdown、辅助脚本、展开源码和其他不再需要的中间产物。
- 正式内容必须进入 `surveys/`、`papers/`、`topics/`、`evidence/` 或 `supplements/`；正式资产进入 owner 对应的 `assets/`。
- 必须建立 README -> Survey -> Paper -> Asset 的正向链路，以及 Paper -> Survey/README 的反向链路。
- 正式文档只能引用被 Git 跟踪的相对路径，不得引用 `_artifacts`、绝对路径、page render 或未跟踪文件。
- 原论文图必须保留完整 caption、只含单一编号对象、紧裁剪，并逐图完成原分辨率 QA；figure inventory 必须记录页码、crop bbox 和 QA。
- 完成前必须检查链接与章节锚点、资产存在性与 Git 跟踪、孤立文档、孤立资产、`_artifacts` 引用，以及 vault 内的代理控制文件和已完成任务的中间产物残留。
- 按领域隔离提交；不得自动提交无关修改、生成缓存或 EOL-only 变化。
- 对本文件约束范围内的任务，完成验证后默认创建本地 Git 提交；仅暂存本任务文件，按领域或元数据边界拆分提交，不推送远端。用户明确要求不提交时除外。

## 强制执行顺序与禁止降级

以下顺序是调研知识任务的硬性流程，不得因已有初版、时间压力或“内容已经齐全”而跳过或倒置：

1. **模板先行**：起草或实质修改 Paper、Survey、Evidence 前，必须完整读取适用 skill 的模板、schema、readability contract 和 publisher contract。必须先按模板建立章节骨架，再填入论文内容；已有初版只能视为草稿，不能作为格式、字段或章节完整性的依据。
2. **结构对照**：正式冻结前，至少将交付件与一个已通过验证的同类型 canonical 文档（优先同域 Paper）逐项对照章节顺序、标题层级、关系区块、术语/符号、图表、修订信息、证据矩阵和缺口章节。发现格式漂移时，先统一结构，再继续发布。
3. **状态不得手写**：`deliverable_manifest.json`、`knowledge-validation.json`、checklist 和 promotion plan 中的 `passed`/`complete` 只能来自实际验证器或明确的人工检查记录。禁止先写 `passed` 再补验证；验证失败、未运行、字段不完整或结果过期时，必须写 `failed` 或 `blocked`，不得用正文已完成替代机器校验。
4. **版本必须锁定**：生成 manifest 前必须读取实际使用的 schema 文件并记录其版本；组织配置版本、deliverable schema 版本和 promotion-plan schema 版本不得混用。禁止凭记忆或沿用旧 manifest 写入版本号。

当前仓库/skill 的版本登记（以实际文件为准）：

- 组织 schema：`.agents/skills/research-knowledge-publisher/references/organization-schema.json`，`1.0.0`。
- 默认组织 profile：`.agents/skills/research-knowledge-publisher/references/default-profile.json`，`1.0.0`。
- 仓库 profile：`research-knowledge.profile.json`，`profile_version=1.0.0`，兼容组织 schema major `1`。
- Promotion plan schema：`.agents/skills/research-knowledge-publisher/references/promotion-plan-schema.json`，`1.1.0`。
- Paper deliverable schema：`.agents/skills/paper-deep-review/references/deliverable-schema.json`，`1.7.0`。

“default profile/organization schema 1.0.0”不等于“Paper deliverable schema 1.7.0”；没有在文件中找到更新版本时，不得擅自改写版本号或声称存在“最新 default scheme”。
5. **冻结顺序**：先完成正文、图表 inventory、逐图 QA、checklist、promotion plan 和 manifest，再运行 review validator 与 publisher validator；两者均通过且错误列表为空后才能将交付标为 `complete`。之后任何正式文件、资产、哈希或链接变化都必须新增 revision 并重新执行全流程。
6. **发布门禁**：publisher validator、promotion-plan schema、正式资产 Git-tracked 检查、相对链接/孤立项/禁用引用检查任一失败，canonical 发布状态必须保持 `blocked`。不得以“主验证器通过”“正文可读”或“稍后再修”宣称 publisher 通过。
7. **图表约束不可弱化**：原论文图必须在保留完整 caption、单一编号对象、legend/axis/注释的前提下紧裁剪；默认安全边距为 8–32 像素，必须记录原始尺寸、精确 bbox、contact-sheet 初筛和逐图原分辨率 QA。直接转存整页或带大块画布留白的源码图不得标为 QA 通过。
8. **交付前复核**：最终回复必须分别报告 review validation、publisher validation、promotion-plan validation、Git 提交和剩余阻塞；任一未完成项不得使用“已完成交付”“审核通过”等含混表述。
