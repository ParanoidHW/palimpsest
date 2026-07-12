# DiT

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 多模态生成与 AI Infra](../surveys/multimodal-diffusion-infra.md)
> - 证据资产：`../assets/papers/dit/`

DiT 证明 latent patch transformer 可以替代 diffusion U-Net。论文的受控 sweep 显示更大模型或更小 latent patch 对 FID 有利，但 Gflops 与 wall-clock throughput 不能等同；更小 patch 会二次放大 attention score 与 activation 成本。

![DiT Figure 3：标准 DiT block。原论文图，PDF p.3。](../assets/papers/dit/fig3-dit-architecture.png)
