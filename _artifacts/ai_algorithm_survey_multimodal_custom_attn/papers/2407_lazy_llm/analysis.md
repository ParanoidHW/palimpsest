# LazyLLM 记录（排除的背景工作）

LazyLLM 是动态 token pruning 背景，非九篇核心方法。它说明先删/压缩 token 可以避免构造 token-pair mask，但会改变模型状态；对视频会有运动与身份信息被永久删除的风险。仅作对照，不纳入跨模态 mask/kernel 结论。
