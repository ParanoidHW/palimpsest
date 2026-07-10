# Multimodal Generation

本目录保存多模态生成、diffusion/flow 演进、训推数据集和 Cosmos 3 系统分析笔记。

## 阅读顺序

1. [多模态模型管线](多模态模型管线.md)：先看典型多模态生成管线和 infra 负载位置。
2. [训推用数据集](训推用数据集.md)：补充多模态生成训练数据和阶段配置。
3. [Diffusion模型多模态演进调研](Diffusion模型多模态演进调研.md)：看 diffusion/flow 从图像到视频、音频、3D、world model 的时间线。
4. [典型模型/Cosmos3](典型模型/Cosmos3.md)：深入 Cosmos 3 的 reasoner/generator、MoT、数据管线、训练和 serving infra。

## 资产说明

- `assets/多模态管线*.png`：多模态生成管线草图，由 [多模态模型管线](多模态模型管线.md) 引用。
- `assets/diffusion_multimodal_evolution_wide_flat.png` 与 `assets/diffusion_longseq/`：diffusion 演进与长序列 diffusion 图表。
- `assets/cosmos3_overview.png`、`assets/mot_architecture.png`、`assets/cosmos_platform.png` 等：Cosmos 3 论文图与问答素材，其中 `cosmos_platform.png` 由正文图片素材清单引用。

## 维护规则

- 图像引用优先使用相对 Markdown 图片路径，避免只靠 Obsidian wikilink。
- 多模态生成结论需要同时标注模型机制、数据管线、attention/quantization/KV cache 和 serving 影响。
- 临时生成或重复中间图只在确认零引用后移除。
