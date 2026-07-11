# 选篇依据

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：无
> - 相关文档：[Figure inventory](figure-inventory.md)，[LazyLLM background](../topics/lazyllm-background.md)

## 入选十篇

1. **[Causal-rCM (2026)](../papers/causal-rcm.md)**：统一视频生成与交互世界模型，唯一同时公开 custom mask、JVP、KV cache 和并行兼容代码的强证据点。
2. **[HASTE (2026)](../papers/haste.md)**：回答动态稀疏 mask 的控制面成本，而不只报告 attention FLOPs。
3. **[LVSA (2026)](../papers/lvsa.md)**：回答结构化时空稀疏如何落成 CSR 和 FlashInfer plan。
4. **[FrameDiT (2026)](../papers/framedit.md)**：架构级去掉 token-level temporal full attention，作为“不是所有优化都应表达成 mask”的反例。
5. **[Token Sparse Attention (2026)](../papers/token-sparse-attention.md)**：token 选择后复用已有 kernel，代表 selector 与 kernel 解耦。
6. **[Cosmos 3 (2026)](../papers/cosmos-3.md)**：多模态统一模型中，把通用 FlexAttention 语义拆成 causal reasoner 与 full generator 两个变长调用。
7. **[VMoBA (2025)](../papers/vmoba.md)**：训练内生 block router，将选择结果转成 FlashAttention varlen packing。
8. **[Sparse VideoGen (2025)](../papers/sparse-videogen.md)**：training-free 视频 DiT 的 spatial/temporal head 模式与 Triton/FlashInfer 原型。
9. **[MInference 1.0 (2024)](../papers/minference.md)**：长上下文 kernel-aware dynamic sparse attention 的方法/实现桥接锚点。
10. **[FlexAttention for Efficient High-Resolution Vision-Language Models (ECCV 2024)](../papers/flexattention-vlm.md)**：纯多模态理解侧的高分辨率 token selection 案例，补足“理解 - 统一 - 生成”覆盖；注意其方法名不等于 PyTorch FlexAttention API。

## 排除

- `LazyLLM`：token pruning 对理解模型有价值，但不直接给出多模态 mask 与 attention kernel 的联合证据，保留为背景。
- 仅有 README 的“multimodal sparse attention”仓库：缺少论文、官方归属或可复现 kernel 路径。
- 非 2026 的通用 FlashAttention：作为 runtime 基线分析，而不是十篇方法论文；高分辨率 VLM FlexAttention 已作为理解侧桥接工作单独纳入。

## 覆盖性

检索覆盖本地知识库、arXiv API/PDF、GitHub API/官方仓库和 CVPR 论文注释。受限项：一般搜索工具响应解码失败；HASTE 与 Token Sparse Attention 未获得可核验官方代码，相关结论仅来自 PDF。每个核心工作均已提取至少一张带完整 caption 的机制或证据图，见 [Figure inventory](figure-inventory.md)。
