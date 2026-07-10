# Sparse VideoGen 精读

论文观察 Video DiT head 可呈 spatial 或 temporal 稀疏模式，在线 profiling 后将采样 token 分给 full、spatial sparse、temporal sparse attention（`paper.txt:145-189,459-474`）。它声称原型使用 Triton 和 FlashInfer（`:168-169`）。

伪码中的 `mask_spatial` / `mask_temporal` 是概念性 mask；论文未在本次材料中给出可审计的最终稀疏格式与 host-device 路径。故本报告只把它作为“模式识别 + 专用 kernel dispatch”谱系锚点，不将其计为 CSR 或 kernel predicate 的证据。
