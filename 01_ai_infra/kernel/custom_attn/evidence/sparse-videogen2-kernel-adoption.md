# Sparse VideoGen2 Kernel Adoption

- Canonical Paper：[Sparse VideoGen2](../../../../02_model_systems/multimodal_generation/papers/sparse-videogen2.md)
- 专题 Survey：[Video generation sparse attention](../surveys/video-generation-sparse-attention.md)

SVG2 的系统链是 `Flash k-means / centroid cache → semantic permutation → Top-p cluster selection → dynamic sparse kernel`。本 Evidence 只记录其 Attention adoption：重排让语义相关 token 在地址上连续，centroid cache 摊销在线聚类；完整生成 pipeline、质量和资产仍由 `multimodal_generation` 拥有。

边界：正式精读保留了官方 repository snapshot，但本轮未完成代码级机制审计，因此 kernel/config 结论按论文报告处理。
