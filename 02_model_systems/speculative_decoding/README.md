# Speculative Decoding

本目录保存投机解码、投机推理和 block diffusion draft 方法的趋势调研与论文精读。

## 阅读顺序

1. [投机推理方法时间演进调研](投机推理方法时间演进调研.md)：先看 token draft、tree draft、block diffusion 和推理加速的时间线。
2. [【Trends】Speculative Decoding](【Trends】Speculative%20Decoding.md)：补充投机推理问题背景和路线概览。
3. [P-EAGLE 精读](P-EAGLE%20Parallel-Drafting%20EAGLE%20with%20Scalable%20Training%20精读分析.md)：理解 parallel drafting 的早期形态。
4. [DFlash 精读](DFlash%202602.06036v2%20精读分析%20DFlash%20Block%20Diffusion%20for%20Flash%20Speculative%20Decoding.md)、[D2SD 精读](D2SD%20Accelerating%20Speculative%20Decoding%20with%20Dual%20Diffusion%20Draft%20Models%20精读分析.md)、[JetSpec 精读](JetSpec%202606.18394v3%20精读分析%20Breaking%20the%20Scaling%20Ceiling%20of%20Speculative%20Decoding%20with%20Parallel%20Tree%20Drafting.md)：重点看 block diffusion draft、dual draft 和 parallel tree drafting。
5. [HyperDFlash 精读](HyperDFlash%202606.26744v1%20精读分析%20MHC-Aligned%20Block%20Speculative%20Decoding%20with%20Gated%20Residual%20Reduction.md)、[DSpark 精读](DSpark%20Confidence-Scheduled%20Speculative%20Decoding%20with%20Semi-Autoregressive%20Generation%20精读分析.md)：看 confidence scheduling 与样本/模型自适应方向。

## 资产说明

- `assets/` 保存正文实际使用的论文图、表格截图和趋势图。
- `alpha_trajectory.png`、`length_distribution_reasoning.png`、`jetspec_table3_lr_ablation_caption.png`、`jetspec_tables8_9_tree_gap_caption.png` 等图虽未全部以图片语法嵌入，但被正文图表索引或清单引用，需保留。
- JetSpec 的 contact sheet 和 source-material 中间素材为零引用资产，已从正式目录移除。

## 维护规则

- 论文精读保留“资料与配图索引”，明确 PDF、source、截图、代码仓库和本地核查状态。
- 趋势类笔记需要区分 token-level speculative decoding、step/semantic speculation、tree draft 和 block diffusion draft。
- 加速结论必须同时看 acceptance、draft cost、verify cost、KV 增量和 serving backend。
