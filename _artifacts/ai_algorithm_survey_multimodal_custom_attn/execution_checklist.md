# 多模态稀疏 Attention 与定制 Mask Kernel 调研：执行检查表

检索时间锚点：2026-07-10（Asia/Shanghai）  
硬件范围：NVIDIA CUDA；其他平台只作可移植性备注。

| 状态 | 项目 | 证据/产物 |
|---|---|---|
| done | 1. 范围、9 篇深读目标与输出目录确定 | 用户确认：2026 前沿、理解/生成/统一模型、内核评审型 PPT |
| done | 2. 当前检索、GitHub/awesome、arXiv、会议来源记录 | `search_log.md`、`github_sources.md` |
| done | 3. 候选影响力信号 | `impact_signals.md` |
| done | 4. 候选论文标准化与机构信息 | `paper_db.jsonl`；PDF 未提取的机构标为 unknown/限制 |
| done | 5. 9 篇选择及排除依据 | `selection.md` |
| done | 6. 逐篇 paper-deep-review、PDF/source/code 获取与核验 | 9 个核心 `papers/*/analysis.md`；4 个官方 repo 已 clone |
| done | 7. 跨论文综合、mask 表达和 kernel 数据流结论 | `synthesis.md` 与知识库最终 Markdown |
| skipped-with-reason | 8. 基于 synthesis 的 PNG 趋势图 | API key 已配置但无 `responses-doc`，无法满足规定的 `responses-doc --input-file synthesis.md` 文档输入；未用 prompt-only 图替代 |
| done | 9. 知识库最终 Markdown | `01_ai_infra/kernel/custom_attn/` |
| done | 10. 可编辑 PPTX 及内容 QA | `01_ai_infra/kernel/custom_attn/`、`ppt_qa/content_check.md` |
| blocked | 11. PPT 视觉渲染、问题修复和复验 | LibreOffice headless 两种 profile 均 exit 1 且不输出 PDF；见 `ppt_qa/qa_report.md`。已完成内容修复和 XML/文本复验。 |
| done | QC. 检索覆盖 general/GitHub/arXiv/venue | 在 `search_log.md` 和 `selection.md` 交叉核验 |
| done | QC. 机构、引用、repo、交叉引用和 awesome 信号齐全 | `paper_db.jsonl` 与 `impact_signals.md`；缺失字段已显式标注 |
| done | QC. 每个入选方法都有清晰谱系角色和代码证据状态 | `selection.md`、`papers/*/analysis.md` |
| done | QC. 所有关键结论标明论文、代码或推断来源 | 最终 Markdown 与每篇 analysis |
| done | QC. 最终文件、链接、PPTX 文本与渲染检查 | 静态检查、PPTX 内容检查；视觉渲染限制另列 |
