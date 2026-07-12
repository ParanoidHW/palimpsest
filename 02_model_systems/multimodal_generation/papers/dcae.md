# Deep Compression Autoencoder

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 多模态生成与 AI Infra](../surveys/multimodal-diffusion-infra.md)
> - 证据资产：`../assets/papers/dcae/`

DC-AE 将更深空间压缩移到 tokenizer。对图像宽高 `H,W`、VAE 每维压缩 `f`、latent patch `p`，DiT token 数为 `N=HW/(fp)²`；latent channel `c` 改变 token 宽度和载荷，不改变 token 数。论文 H100 数据显示显著吞吐/显存收益，但运行时、batch 和 TensorRT 配置仍是边界条件。

![DC-AE Table 3：ImageNet efficiency。原论文表，PDF p.9。](../assets/papers/dcae/table3-imagenet-efficiency.png)
