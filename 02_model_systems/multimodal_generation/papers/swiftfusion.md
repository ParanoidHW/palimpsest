# SwiftFusion

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 多模态生成与 AI Infra](../surveys/multimodal-diffusion-infra.md)
> - 证据资产：`../assets/papers/swiftfusion/`

SwiftFusion 将会收缩数据量的 Ulysses 放到慢的跨机链路，将 Ring 放到机内，并用 Torus stages 与 NVSHMEM one-sided put/get 重叠通信。平均 1.35x、最大 1.77x 只适用于测试的最优配置；短图像和部分双机组合可能退化。

![SwiftFusion Figure 6：Torus scheduling。原论文图，PDF p.7。](../assets/papers/swiftfusion/fig6-torus-scheduling.png)
