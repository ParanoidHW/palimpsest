# Multimodal Generation

本目录保存多模态生成、diffusion/flow 演进、训推数据集和 Cosmos 3 系统分析笔记。

## 阅读顺序

1. [Model pipeline](topics/model-pipeline.md)：先看典型多模态生成管线和 infra 负载位置。
2. [Training data](topics/training-data.md)：补充多模态生成训练数据和阶段配置。
3. [Diffusion evolution](surveys/diffusion-evolution.md)：看 diffusion/flow 从图像到视频、音频、3D、world model 的时间线。
4. [近半年多模态视觉生成模型全景](surveys/visual-generation-model-landscape.md)：按 Dense/MoT、total/active 参数、数据模态与 dtype、AR/diffusion/hybrid 比较 2026-01-28 至 2026-07-28 的 25 个系统。
5. [Diffusion 多模态生成与 AI Infra](surveys/multimodal-diffusion-infra.md)：从 2026 最新算法推导 serving、并行、kernel、内存、互联和硬件趋势。
6. [Qwen-Image-2.0](papers/qwen-image-2-0.md)、[SANA-Video 2.0](papers/sana-video-2.md)、[Helios](papers/helios.md)、[Vega](papers/vega.md)：本次全景 Survey 的新精读。
7. [BAGEL](papers/bagel.md)、[Cosmos 3](papers/cosmos-3.md)：复用的参数稀疏/统一系统 canonical 精读。
8. [MAGI-1](papers/magi-1.md)：精读 chunkwise-AR、帧/chunk/token 核算、MagiAttention 与实时 serving。
9. [Cosmos 3 Q&A](supplements/cosmos-3-q-and-a.md)：按 Q1--Q12 复读位置编码、模态编码、训练数据与系统问题。
10. [Figure inventory](evidence/figure-inventory.md)：追溯正式资产的原编号、source/PDF 页码、caption、owner 与 QA。

## 文档索引

- Sparse-attention pipeline Papers：[Sparse VideoGen](papers/sparse-videogen.md)，[Sparse VideoGen2](papers/sparse-videogen2.md)，[Jenga / TokenCarve](papers/jenga.md)
- Attention 专题入口：[Video generation sparse attention](../../01_ai_infra/kernel/custom_attn/surveys/video-generation-sparse-attention.md)

- Survey：[Diffusion evolution](surveys/diffusion-evolution.md)，[近半年多模态视觉生成模型全景](surveys/visual-generation-model-landscape.md)，[Diffusion 多模态生成与 AI Infra](surveys/multimodal-diffusion-infra.md)
- Topics：[Model pipeline](topics/model-pipeline.md)，[Training data](topics/training-data.md)
- Paper：[LDM](papers/ldm.md)，[DiT](papers/dit.md)，[Transfusion](papers/transfusion.md)，[Qwen-Image-2.0](papers/qwen-image-2-0.md)，[BAGEL](papers/bagel.md)，[PixelDiT](papers/pixeldit.md)，[DC-AE](papers/dcae.md)，[HunyuanVideo 1.5](papers/hunyuanvideo-1-5.md)，[SANA-Video 2.0](papers/sana-video-2.md)，[Helios](papers/helios.md)，[Vega](papers/vega.md)，[Sparse VideoGen](papers/sparse-videogen.md)，[FEB-Cache](papers/feb-cache.md)，[SwiftFusion](papers/swiftfusion.md)，[Causal-rCM](papers/causal-rcm.md)，[MAGI-1](papers/magi-1.md)，[Cosmos 3](papers/cosmos-3.md)
- Supplement：[Cosmos 3 Q&A](supplements/cosmos-3-q-and-a.md)
- Word 交付：[Diffusion 多模态生成与 AI Infra](supplements/multimodal-diffusion-infra.docx)
- Evidence：[Figure inventory](evidence/figure-inventory.md)

## Obsidian Properties

本领域 `19/19` 篇 canonical Paper 已加入统一的 Obsidian YAML Properties：

- 共同标签：`paper`、`collection/multimodal-generation`、`domain/model-systems`、`status/deep-review`。
- 每篇另有一项 `topic/*` 和一项 `method/*`，分别表达生成任务与核心方法。
- 独立属性：`document_type`、`domain`、`collection`、`review_status`、`canonical`，用于 Properties view、Bases 和程序化筛选。
- 搜索示例：`tag:#collection/multimodal-generation` 查看本领域全部精读；`tag:#topic/video-generation` 聚合视频生成论文。

## 资产说明

- `assets/topics/model-pipeline/`：多模态生成管线草图。
- `assets/surveys/diffusion-evolution/`：diffusion 演进与长序列 diffusion 图表。
- `assets/surveys/visual-generation-model-landscape/`：近半年视觉生成模型趋势与 Infra 整理图。
- `assets/surveys/multimodal-diffusion-infra/`：本次跨论文整理图与 AI 生成趋势图。
- `assets/papers/qwen-image-2-0/`、`assets/papers/sana-video-2/`、`assets/papers/helios/`、`assets/papers/vega/`：本次新精读的原论文机制与证据图。
- `assets/papers/magi-1/`：MAGI-1 chunkwise-AR、ARDF、MagiAttention 与 latency 原论文证据图。
- `assets/papers/cosmos-3/`：Cosmos 3 paper-owned 原论文图与明确标注的知识库整理图。

## 维护规则

- 图像引用优先使用相对 Markdown 图片路径，避免只靠 Obsidian wikilink。
- 多模态生成结论需要同时标注模型机制、数据管线、attention/quantization/KV cache 和 serving 影响。
- 临时生成或重复中间图只在确认零引用后移除。
