# Sparse VideoGen：kernel 采用证据

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：[Sparse VideoGen assets](../../../../02_model_systems/multimodal_generation/assets/papers/sparse-videogen/)
> - 相关文档：[Canonical Paper](../../../../02_model_systems/multimodal_generation/papers/sparse-videogen.md)，[Figure inventory](figure-inventory.md)

完整 Paper 与原论文图由 Multimodal Generation 统一拥有。本领域保留的采用结论是：head-level spatial/temporal pattern discovery 与 layout transformation 是两个独立环节；只有后者把非连续访问重排成连续 tile，稀疏模式才可能转化为实测 kernel 收益。

机制与系统证据分别见 [Fig.4](../../../../02_model_systems/multimodal_generation/assets/papers/sparse-videogen/fig4_svg_workflow_caption.png)、[Fig.5](../../../../02_model_systems/multimodal_generation/assets/papers/sparse-videogen/fig5_layout_transformation_caption.png) 和 [Fig.8](../../../../02_model_systems/multimodal_generation/assets/papers/sparse-videogen/fig8_sparse_kernel_latency_caption.png)。官方可审计 kernel 源码在现有材料中不可得，因此具体 metadata 格式和实现可移植性维持 `unverified`。
