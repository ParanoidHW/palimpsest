# LLM Foundations 图表清单与 QA

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[2026H1 model scale](../surveys/2026h1-model-scale.md)
> - 证据资产：`../assets/papers/deepseek-v4/`
> - 相关文档：[DeepSeek-V4](../papers/deepseek-v4.md)

本清单索引 DeepSeek-V4 canonical Paper 的正式论文视觉证据。三个对象均由官方 PDF/source 重新裁剪，保留完整 caption、单一编号对象、源页尺寸与 crop bbox，并通过 contact-sheet 初筛和逐图原分辨率复核；页面渲染、裁剪过程与 QA 日志仅保存在过程工作区。

| Object / source crop | 正式资产 | 完整 caption | Paper usage | QA |
|---|---|---|---|---|
| Figure 3 / PDF p.9；源页 `2481×3508`；crop `(280,350,1925,1190)` | `../assets/papers/deepseek-v4/fig3-csa-architecture-caption.png` | “Core architectures of CSA. It compresses the number of KV entries to 1/m times, and then applies DeepSeek Sparse Attention for further acceleration. Additionally, a small set of sliding window KV entries is combined with the selected compressed KV entries to enhance local fine-grained dependencies.” | CSA 压缩、索引、稀疏选择与局部窗口数据流 | pass：单一编号对象、完整 caption，2026-07-25 contact-sheet + 原分辨率 QA |
| Figure 5 / PDF p.15；源页 `2481×3508`；crop `(285,1520,1920,1060)` | `../assets/papers/deepseek-v4/fig5-ep-overlap-caption.png` | “Illustration of our EP scheme with related works. Comet (Zhang et al., 2025b) overlaps Dispatch with Linear-1, and Linear-2 with Combine, separately. Our EP scheme achieves a finer-grained overlapping by splitting and scheduling experts into waves. The theoretical speedup is evaluated in the configuration of the DeepSeek-V4-Flash architecture.” | wave-based EP overlap；速度仅为理论配置估计 | pass：三种调度、速度标注与完整 caption 可读，2026-07-25 QA |
| Table 1 / PDF p.28；源页 `2481×3508`；crop `(285,355,1920,1780)` | `../assets/papers/deepseek-v4/table1-base-evaluation-caption.png` | “Comparison among DeepSeek-V3.2-Base, DeepSeek-V4-Flash-Base, and DeepSeek-V4-Pro-Base. All models are evaluated in our internal framework and share the same evaluation setting. Scores with a gap not exceeding 0.3 are considered to be at the same level. The highest score in each row is in bold font, and the second is underlined.” | base 模型统一内部框架主结果与反例 | pass：全部 benchmark 行、列、脚注与完整 caption 可读，2026-07-25 QA |
