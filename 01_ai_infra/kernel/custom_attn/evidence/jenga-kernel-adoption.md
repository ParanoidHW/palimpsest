# Jenga / TokenCarve Kernel Adoption

- Canonical Paper：[Jenga](../../../../02_model_systems/multimodal_generation/papers/jenga.md)
- 专题 Survey：[Video generation sparse attention](../surveys/video-generation-sparse-attention.md)

Attention primitive 是 AttenCarve：把 3D latent 划分为 block，一次性产生 head-aware block mask，在选中块内部执行 dense parallel attention。完整 Jenga 还包括 progressive resolution、timestep skipping 和 kernel 实现。

归因边界：Table 1 的 AttenCarve-only 为 2.17×；8.83× 只属于组合后的 Jenga-Flash，不能作为 sparse-attention primitive 的单项收益。
