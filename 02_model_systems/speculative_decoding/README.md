# Speculative Decoding

本目录保存投机解码、投机推理和 block diffusion draft 方法的趋势调研与论文精读。

## 阅读顺序

1. [Evolution](surveys/evolution.md)：canonical survey，先看 token draft、tree draft、block diffusion 和推理加速时间线。
2. [Foundations and trends](surveys/foundations-and-trends.md)：看 lossless correctness contract、draft/verify 成本模型、机制分类、KV/serving 约束与开放问题。
3. [P-EAGLE](papers/p-eagle.md)、[DFlash](papers/dflash.md)、[D2SD](papers/d2sd.md)、[JetSpec](papers/jetspec.md)：理解 parallel drafting、block diffusion 和 tree drafting 主线。
4. [HyperDFlash](papers/hyperdflash.md) 与 [DSpark](papers/dspark.md)：看架构对齐、半自回归修正和 confidence scheduling。
5. [DeLS-Spec](papers/dels-spec.md)：看 DSpark 发布后的低成本算法增量——冻结 DFlash、独立训练短上下文专家并做 prior-corrected logit fusion。
6. [AngelSpec](papers/angelspec.md) 与 [TorchSpec](papers/torchspec.md)：看 workload-aware drafter、动态验证预算，以及解耦 hidden-state 训练系统。
7. [AcceptMoE](papers/acceptmoe.md)：看 MoE 树验证中的 commitment-weighted、自适应专家集合与 offload cache 剪枝。
8. [LibraSpec](papers/libraspec.md)：看扩散式 drafter 的边际收益驱动动态 speculative length。

## 文档索引

- Surveys：[Evolution](surveys/evolution.md)，[Foundations and trends](surveys/foundations-and-trends.md)， [AcceptMoE](papers/acceptmoe.md)
- Papers：[P-EAGLE](papers/p-eagle.md)，[DFlash](papers/dflash.md)，[D2SD](papers/d2sd.md)，[JetSpec](papers/jetspec.md)，[HyperDFlash](papers/hyperdflash.md)，[DSpark](papers/dspark.md)，[DeLS-Spec](papers/dels-spec.md)，[AngelSpec](papers/angelspec.md)，[TorchSpec](papers/torchspec.md)，[AcceptMoE](papers/acceptmoe.md)，[LibraSpec](papers/libraspec.md)
- Evidence：[Figure inventory](evidence/figure-inventory.md)，[AcceptMoE figure inventory](evidence/acceptmoe-figure-inventory.md)，[LibraSpec figure inventory](evidence/libraspec-figure-inventory.md)
- Supplement：[DFlash draft-model acceptance risk](supplements/dflash-acceptance-risk.html)

## Obsidian Properties

本领域 `9/9` 篇 canonical Paper 已加入统一的 Obsidian YAML Properties：

- 共同标签：`paper`、`collection/speculative-decoding`、`domain/model-systems`、`status/deep-review`。
- 每篇另有一项 `topic/*` 和一项 `method/*`，分别表达研究问题与 draft/verification 方法。
- 独立属性：`document_type`、`domain`、`collection`、`review_status`、`canonical`，用于 Properties view、Bases 和程序化筛选。
- 搜索示例：`tag:#collection/speculative-decoding` 查看本领域全部精读；`tag:#topic/block-diffusion-drafting` 查看 block diffusion 分支。

## 资产说明

- `assets/surveys/evolution/` 保存时间线汇总图。
- `assets/papers/<paper-slug>/` 保存各论文的正式图表证据。
- JetSpec 的 contact sheet 和 source-material 中间素材为零引用资产，已从正式目录移除。

## 维护规则

- 论文精读保留“资料与配图索引”，但正式引用只指向 Git 跟踪的资产和公开一手来源。
- 趋势类笔记需要区分 token-level speculative decoding、step/semantic speculation、tree draft 和 block diffusion draft。
- 加速结论必须同时看 acceptance、draft cost、verify cost、KV 增量和 serving backend。
