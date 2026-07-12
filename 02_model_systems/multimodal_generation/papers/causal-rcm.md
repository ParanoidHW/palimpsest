# Causal-rCM

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 多模态生成与 AI Infra](../surveys/multimodal-diffusion-infra.md)
> - 证据资产：`../assets/papers/causal-rcm/`

Causal-rCM 是 TF → TF-CM → self-forcing DMD 的分阶段 recipe，并通过 packed causal mask、custom-mask FA2 JVP、context parallel 与 noisy-context KV reuse 支持流式生成。论文“10x”指达到收敛所需迭代数，不是 kernel 或 wall-clock 10x。

![Causal-rCM Figure 4：训练管线比较。原论文图，PDF p.5。](../assets/papers/causal-rcm/fig4-pipeline-comparison.png)
