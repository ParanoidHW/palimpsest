# Sparse VideoGen

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 多模态生成与 AI Infra](../surveys/multimodal-diffusion-infra.md)
> - 证据资产：`../assets/papers/sparse-videogen/`

Sparse VideoGen 用 1% query rows 在线判别 spatial/temporal heads，配合 frame-major layout 和定制 kernel。HunyuanVideo 报告的 2.33x 是 profiling、稀疏算法、layout、kernel 与 FP8 的组合收益；官方 commit 可定位但未得到可审计 worktree，因此 kernel 细节按论文主张处理。

![Sparse VideoGen Figure 7：端到端性能分解。原论文图，PDF p.8。](../assets/papers/sparse-videogen/fig7-end-to-end-breakdown.png)
