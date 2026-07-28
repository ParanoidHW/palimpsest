# Speculative Decoding

本目录保存投机解码、投机推理和 block diffusion draft 方法的趋势调研与论文精读。

## 阅读顺序

1. [Evolution](surveys/evolution.md)：canonical survey，先看 token draft、tree draft、block diffusion 和推理加速时间线。
2. [Foundations and trends](surveys/foundations-and-trends.md)：看 lossless correctness contract、draft/verify 成本模型、机制分类、KV/serving 约束与开放问题。
3. [P-EAGLE](papers/p-eagle.md)、[DFlash](papers/dflash.md)、[D2SD](papers/d2sd.md)、[JetSpec](papers/jetspec.md)：理解 parallel drafting、block diffusion 和 tree drafting 主线。
4. [HyperDFlash](papers/hyperdflash.md) 与 [DSpark](papers/dspark.md)：看架构对齐、半自回归修正和 confidence scheduling。
5. [DeLS-Spec](papers/dels-spec.md)：看 DSpark 发布后的低成本算法增量——冻结 DFlash、独立训练短上下文专家并做 prior-corrected logit fusion。

## 文档索引

- Surveys：[Evolution](surveys/evolution.md)，[Foundations and trends](surveys/foundations-and-trends.md)
- Papers：[P-EAGLE](papers/p-eagle.md)，[DFlash](papers/dflash.md)，[D2SD](papers/d2sd.md)，[JetSpec](papers/jetspec.md)，[HyperDFlash](papers/hyperdflash.md)，[DSpark](papers/dspark.md)，[DeLS-Spec](papers/dels-spec.md)
- Evidence：[Figure inventory](evidence/figure-inventory.md)
- Supplement：[DFlash draft-model acceptance risk](supplements/dflash-acceptance-risk.html)

## 资产说明

- `assets/surveys/evolution/` 保存时间线汇总图。
- `assets/papers/<paper-slug>/` 保存各论文的正式图表证据。
- JetSpec 的 contact sheet 和 source-material 中间素材为零引用资产，已从正式目录移除。

## 维护规则

- 论文精读保留“资料与配图索引”，但正式引用只指向 Git 跟踪的资产和公开一手来源。
- 趋势类笔记需要区分 token-level speculative decoding、step/semantic speculation、tree draft 和 block diffusion draft。
- 加速结论必须同时看 acceptance、draft cost、verify cost、KV 增量和 serving backend。
