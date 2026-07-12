# Multimodal Generation

本目录保存多模态生成、diffusion/flow 演进、训推数据集和 Cosmos 3 系统分析笔记。

## 阅读顺序

1. [Model pipeline](topics/model-pipeline.md)：先看典型多模态生成管线和 infra 负载位置。
2. [Training data](topics/training-data.md)：补充多模态生成训练数据和阶段配置。
3. [Diffusion evolution](surveys/diffusion-evolution.md)：看 diffusion/flow 从图像到视频、音频、3D、world model 的时间线。
4. [Diffusion 多模态生成与 AI Infra](surveys/multimodal-diffusion-infra.md)：从 2026 最新算法推导 serving、并行、kernel、内存、互联和硬件趋势。
5. [Cosmos 3](papers/cosmos-3.md)：深入 reasoner/generator、MoT、数据管线、训练和 serving infra。
6. [Cosmos 3 Q&A](supplements/cosmos-3-q-and-a.md)：按 Q1--Q12 复读位置编码、模态编码、训练数据与系统问题。
7. [Figure inventory](evidence/figure-inventory.md)：追溯正式资产的原编号、source/PDF 页码、caption、owner 与 QA。

## 文档索引

- Survey：[Diffusion evolution](surveys/diffusion-evolution.md)，[Diffusion 多模态生成与 AI Infra](surveys/multimodal-diffusion-infra.md)
- Topics：[Model pipeline](topics/model-pipeline.md)，[Training data](topics/training-data.md)
- Paper：[LDM](papers/ldm.md)，[DiT](papers/dit.md)，[Transfusion](papers/transfusion.md)，[BAGEL](papers/bagel.md)，[PixelDiT](papers/pixeldit.md)，[DC-AE](papers/dcae.md)，[HunyuanVideo 1.5](papers/hunyuanvideo-1-5.md)，[Sparse VideoGen](papers/sparse-videogen.md)，[FEB-Cache](papers/feb-cache.md)，[SwiftFusion](papers/swiftfusion.md)，[Causal-rCM](papers/causal-rcm.md)，[Cosmos 3](papers/cosmos-3.md)
- Supplement：[Cosmos 3 Q&A](supplements/cosmos-3-q-and-a.md)
- Word 交付：[Diffusion 多模态生成与 AI Infra](supplements/multimodal-diffusion-infra.docx)
- Evidence：[Figure inventory](evidence/figure-inventory.md)

## 资产说明

- `assets/topics/model-pipeline/`：多模态生成管线草图。
- `assets/surveys/diffusion-evolution/`：diffusion 演进与长序列 diffusion 图表。
- `assets/surveys/multimodal-diffusion-infra/`：本次跨论文整理图与 AI 生成趋势图。
- `assets/papers/cosmos-3/`：Cosmos 3 paper-owned 原论文图与明确标注的知识库整理图。

## 维护规则

- 图像引用优先使用相对 Markdown 图片路径，避免只靠 Obsidian wikilink。
- 多模态生成结论需要同时标注模型机制、数据管线、attention/quantization/KV cache 和 serving 影响。
- 临时生成或重复中间图只在确认零引用后移除。
