# LLM Foundations

本目录保存云侧大模型规模、长上下文架构和基础模型系统分析笔记。

## 阅读顺序

1. [2026 H1 model scale](surveys/2026h1-model-scale.md)：先看近半年云侧模型规模、精度、结构和 Attention 类型的横向表。
2. [DeepSeek-V4 精读分析](papers/deepseek-v4.md)：再看 1M context、CSA/HCA、mHC、MoE overlap 和 KV cache 的系统影响。
3. [Kimi K3 精读分析](papers/kimi-k3.md)：最后看 2.8T/104.2B-active、KDA/MLA、AttnRes、896-expert MoE、agent RL 与昇腾 CANN 0day 实现边界。
4. [Linear Attention Transformer 演化](surveys/linear-attention-transformer-evolution.md)：从 2020 feature-map 状态、RetNet、Mamba/SSD、GLA/DeltaNet 到 2026 KDA、Mamba-3、Gated DeltaNet-2，分别比较方法谱系、Qwen3-Next/Kimi K3 系统采用、kernel、cache 与 serving 约束。

## 文档索引

- Survey：[2026 H1 model scale](surveys/2026h1-model-scale.md)
- Paper：[DeepSeek-V4](papers/deepseek-v4.md)
- Paper：[Kimi K3](papers/kimi-k3.md)
- Paper：[Mamba](papers/mamba.md)
- Paper：[Linear Transformer](papers/linear-transformer.md)
- Paper：[RetNet](papers/retnet.md)
- Paper：[Mamba-2 / SSD](papers/mamba-2-structured-state-space-duality.md)
- Paper：[Gated Linear Attention](papers/gated-linear-attention.md)
- Paper：[DeltaNet](papers/deltanet.md)
- Paper：[Gated DeltaNet](papers/gated-deltanet.md)
- Paper：[Kimi Linear / KDA](papers/kimi-linear.md)
- Evidence：[Figure inventory](evidence/figure-inventory.md)
- Survey：[Linear Attention Transformer 演化](surveys/linear-attention-transformer-evolution.md)
- Evidence：[Linear Attention Transformer 证据索引](evidence/linear-attention-transformer-evidence.md)

## Obsidian Properties

本领域 `11/11` 篇 canonical Paper 已加入统一的 Obsidian YAML Properties：

- 共同标签：`paper`、`collection/llm-foundations`、`domain/model-systems`、`status/deep-review`。
- 每篇另有一项 `topic/*` 和一项 `method/*`，分别表达研究问题与核心方法。
- 独立属性：`document_type`、`domain`、`collection`、`review_status`、`canonical`，用于 Properties view、Bases 和程序化筛选。
- 搜索示例：`tag:#collection/llm-foundations` 查看本领域全部精读。

## 资产说明

- `assets/papers/deepseek-v4/`：DeepSeek-V4 精读正文实际嵌入、带完整 caption 且通过原分辨率 QA 的论文图表。
- `assets/papers/kimi-k3/`：Kimi K3 精读正文实际嵌入的十张原论文图表与一张明确标注为 AI 解释图的端到端因果图；原论文图均带完整 caption 并通过原分辨率 QA。
- PDF、源码、页面渲染、裁剪过程和 QA 日志仅保留在过程工作区；正式目录不保留未引用的 legacy 图。

## 维护规则

- 模型规模表只记录官方文档、模型卡和技术报告公开信息，未披露字段不做第三方猜测。
- 论文精读只引用 Git 跟踪的正式资产；PDF、源码、渲染页和核查日志保留为过程材料。
- 结构结论需要区分论文声称、源码证据、模型卡字段和未验证项。
