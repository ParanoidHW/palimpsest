# Custom Attention

本领域聚焦多模态稀疏 Attention、定制 Mask、selector/planner、kernel lowering 与长序列 runtime。主线从跨论文 Survey 下钻到十篇独立精读，再追溯到 selection 和 figure inventory。

## 阅读路径

1. [Multimodal custom attention](surveys/multimodal-custom-attention.md)：先看跨论文路线、kernel 设计判断和验证计划。
2. [Selection](evidence/selection.md)：核对十篇入选工作和排除边界。
3. [Venue and organization trends](evidence/venue-organization-trends-2020-2026.md)：核对 2020–2026 顶会论文计数、组织归属口径和趋势图。
4. 按 Survey 章节下钻到对应 Paper；图表来源与 QA 见 [Figure inventory](evidence/figure-inventory.md)。
5. [LazyLLM background](topics/lazyllm-background.md) 仅作 token pruning 背景，不属于十篇核心工作。

## 文档索引

- Survey：[Multimodal custom attention](surveys/multimodal-custom-attention.md)
- Papers：[FlexAttention VLM](papers/flexattention-vlm.md)，[MInference](papers/minference.md)，[Sparse VideoGen](papers/sparse-videogen.md)，[VMoBA](papers/vmoba.md)，[Token Sparse Attention](papers/token-sparse-attention.md)，[FrameDiT](papers/framedit.md)，[HASTE](papers/haste.md)，[LVSA](papers/lvsa.md)，[Causal-rCM](papers/causal-rcm.md)，[Cosmos 3](papers/cosmos-3.md)
- Topic：[LazyLLM background](topics/lazyllm-background.md)
- Evidence：[Selection](evidence/selection.md)，[Venue and organization trends](evidence/venue-organization-trends-2020-2026.md)，[Figure inventory](evidence/figure-inventory.md)
- Supplement：[Editable PPT](supplements/multimodal-custom-attention.pptx)

## 资产说明

- 原论文图归入 `assets/papers/<paper-slug>/`，由对应 Paper 和 Survey 交叉引用。
- Cosmos 3 的两张机制图由 Multimodal Generation 的 Cosmos 3 Paper 统一拥有，本领域跨目录引用，不保留副本。
- PDF、源码、整页渲染、裁剪过程、构建脚本和 QA 日志只保留为过程材料。
