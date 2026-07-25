# LLM Foundations

本目录保存云侧大模型规模、长上下文架构和基础模型系统分析笔记。

## 阅读顺序

1. [2026 H1 model scale](surveys/2026h1-model-scale.md)：先看近半年云侧模型规模、精度、结构和 Attention 类型的横向表。
2. [DeepSeek-V4 精读分析](papers/deepseek-v4.md)：再看 1M context、CSA/HCA、mHC、MoE overlap 和 KV cache 的系统影响。

## 文档索引

- Survey：[2026 H1 model scale](surveys/2026h1-model-scale.md)
- Paper：[DeepSeek-V4](papers/deepseek-v4.md)
- Evidence：[Figure inventory](evidence/figure-inventory.md)

## 资产说明

- `assets/papers/deepseek-v4/`：DeepSeek-V4 精读正文实际嵌入的源码图。
- DeepSeek-V4 表格已整理为 Markdown 摘录，不再保留零引用的 caption/table 截图副本。

## 维护规则

- 模型规模表只记录官方文档、模型卡和技术报告公开信息，未披露字段不做第三方猜测。
- 论文精读只引用 Git 跟踪的正式资产；PDF、源码、渲染页和核查日志保留为过程材料。
- 结构结论需要区分论文声称、源码证据、模型卡字段和未验证项。
