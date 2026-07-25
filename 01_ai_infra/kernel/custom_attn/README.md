# Custom Attention

本领域聚焦多模态稀疏 Attention、定制 Mask、selector/planner、kernel lowering 与长序列 runtime。主线从跨论文 Survey 下钻到七篇本领域 Paper、三条跨域 adoption evidence，再追溯到 selection 和 figure inventory。

## 阅读路径

1. [Multimodal custom attention](surveys/multimodal-custom-attention.md)：先看跨论文路线、kernel 设计判断和验证计划。
2. [Selection](evidence/selection.md)：核对七篇本领域 Paper、三条跨域采用证据和排除边界。
3. [Venue and organization trends](evidence/venue-organization-trends-2020-2026.md)：核对 2020–2026 顶会论文计数、组织归属口径和趋势图。
4. 按 Survey 章节下钻到对应 Paper；图表来源与 QA 见 [Figure inventory](evidence/figure-inventory.md)。
5. [LazyLLM background](topics/lazyllm-background.md) 仅作 token pruning 背景，不属于十篇核心工作。

## 文档索引

- Survey：[Multimodal custom attention](surveys/multimodal-custom-attention.md)
- Papers：[FlexAttention VLM](papers/flexattention-vlm.md)，[MInference](papers/minference.md)，[VMoBA](papers/vmoba.md)，[Token Sparse Attention](papers/token-sparse-attention.md)，[FrameDiT](papers/framedit.md)，[HASTE](papers/haste.md)，[LVSA](papers/lvsa.md)
- Topic：[LazyLLM background](topics/lazyllm-background.md)
- Evidence：[Selection](evidence/selection.md)，[Causal-rCM kernel adoption](evidence/causal-rcm-kernel-adoption.md)，[Cosmos 3 attention lowering](evidence/cosmos-3-attention-lowering.md)，[Sparse VideoGen kernel adoption](evidence/sparse-videogen-kernel-adoption.md)，[Venue and organization trends](evidence/venue-organization-trends-2020-2026.md)，[Figure inventory](evidence/figure-inventory.md)
- Supplement：[Editable PPT](supplements/multimodal-custom-attention.pptx)

## 资产说明

- 原论文图归入其 canonical Paper 的 `assets/papers/<paper-slug>/`，由对应 Paper 和 Survey 交叉引用。
- Causal-rCM、Cosmos 3 与 Sparse VideoGen 的完整 Paper 和全部原论文图由 [Multimodal Generation](../../../02_model_systems/multimodal_generation/README.md) 统一拥有；本领域只保留 kernel/adoption Evidence。
- PDF、源码、整页渲染、裁剪过程、构建脚本和 QA 日志只保留为过程材料。
