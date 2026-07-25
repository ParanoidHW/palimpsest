# Cosmos 3：two-way attention lowering 证据

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：[Cosmos 3 assets](../../../../02_model_systems/multimodal_generation/assets/papers/cosmos-3/)
> - 相关文档：[Canonical Paper](../../../../02_model_systems/multimodal_generation/papers/cosmos-3.md)，[Figure inventory](figure-inventory.md)

Cosmos 3 的完整模型分析、数据与运行时证据由 Multimodal Generation 维护。本领域只记录一条 adoption 结论：将 AR reasoner 与 diffusion generator 的混合可见性拆成 causal reasoner call 与读取同样本 reasoner 条件的 generator call，可把通用 mixed-mask 语义 lower 为少数规则化的 varlen attention 调用。

这是一项系统设计判断，而非“更稀疏的 kernel”主张。机制整理图 [two-way attention](../../../../02_model_systems/multimodal_generation/assets/papers/cosmos-3/two-way-attention-infra.png) 与原论文 MoT 图共同解释分流；吞吐或 latency 的归因仍须以 canonical Paper 的实验和 backend 条件为准。
