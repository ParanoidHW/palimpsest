# LazyLLM 记录（排除的背景工作）

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：无
> - 相关文档：[Selection](../evidence/selection.md)

LazyLLM 是动态 token pruning 背景，非十篇核心方法。它说明先删/压缩 token 可以避免构造 token-pair mask，但会改变模型状态；对视频会有运动与身份信息被永久删除的风险。仅作对照，不纳入跨模态 mask/kernel 结论。
