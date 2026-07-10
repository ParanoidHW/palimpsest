# 影响力与价值信号

快照日期：2026-07-10。2026 预印本的引用数不足以排序，因此分离工程采用、论文状态与概念价值。

| 工作 | 论文状态 | 官方代码/信号 | 概念价值 | 入选 |
|---|---|---|---|---|
| Causal-rCM | 2026 technical report | NVlabs 750/27 | custom-mask JVP、chunk-causal、KV/cache 共设计 | 是 |
| HASTE | 2026 arXiv | 未找到可核验官方 repo | head-wise 动态预算与跨 step mask reuse | 是 |
| LVSA | 2026 arXiv | 官方仓库已核验 | 明确 CSR + FlashInfer，长视频锚点模式 | 是 |
| FrameDiT | CVPR 2026 Findings | 官方仓库已核验 | 用结构替代 token-level temporal full attention | 是 |
| Token Sparse Attention | ICML 2026 | PDF 核验；代码未核验 | token-level selection 与 kernel compatible packing | 是 |
| Cosmos 3 | 2026 technical report / 本地原始材料 | 本地精读含源码路径 | 统一 reasoner-generator 的 two-way flat attention | 是 |
| VMoBA | 2025 arXiv | 官方 64/4 | learned/route block 的 FlashAttention-varlen 打包路径 | 是 |
| Sparse VideoGen | 2025 arXiv | PDF 核验；实现未获取 | 训练无关时空 head 分型、Triton/FlashInfer 原型 | 是 |
| MInference 1.0 | NeurIPS 2024 Spotlight | 论文核验 | kernel-aware dynamic pattern，是长上下文稀疏的桥接锚点 | 是 |
| FlexAttention VLM | ECCV 2024 | 官方仓库 49/6 | 高分辨率多模态理解的 token selection + compact attention 桥接 | 是 |

交叉引用统计未以自动解析参考文献代替人工事实；谱系关系仅在 `selection.md` 与 `synthesis.md` 标为“机制继承/比较”，不声称所有后作直接引用前作。
