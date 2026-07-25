# Research Knowledge Rules

本文件只约束 literature survey、paper deep review、research synthesis、论文图表提取，以及对应 Markdown、PPT、HTML、assets 的新增、迁移和维护。

执行上述任务前，必须完整读取并遵守 [调研知识组织规范](00_meta/research-knowledge-organization.md)。详细解释只维护在该规范中。

- 创建文件前先确定 domain、doc type、slug 和 canonical owner。
- PDF、源码、页面渲染、裁剪过程、QA 和日志只能进入 `_artifacts/`。
- 正式内容必须进入 `surveys/`、`papers/`、`topics/`、`evidence/` 或 `supplements/`；正式资产进入 owner 对应的 `assets/`。
- 必须建立 README -> Survey -> Paper -> Asset 的正向链路，以及 Paper -> Survey/README 的反向链路。
- 正式文档只能引用被 Git 跟踪的相对路径，不得引用 `_artifacts`、绝对路径、page render 或未跟踪文件。
- 原论文图必须保留完整 caption、只含单一编号对象、紧裁剪，并逐图完成原分辨率 QA；figure inventory 必须记录页码、crop bbox 和 QA。
- 完成前必须检查链接与章节锚点、资产存在性与 Git 跟踪、孤立文档、孤立资产和 `_artifacts` 引用。
- 按领域隔离提交；不得自动提交无关修改、生成缓存或 EOL-only 变化。
- 对本文件约束范围内的任务，完成验证后默认创建本地 Git 提交；仅暂存本任务文件，按领域或元数据边界拆分提交，不推送远端。用户明确要求不提交时除外。
