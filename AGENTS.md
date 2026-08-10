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
