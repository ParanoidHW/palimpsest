# FrameDiT 精读

FrameDiT（CVPR 2026 Findings）以 frame-level matrix attention 取代 token-level temporal full attention，是架构级降复杂度而非“更复杂 mask”。对多模态视频生成的启示是：若语义可先聚合到 frame/state，最经济的 sparse mask 是根本不生成 token-pair mask。

官方 commit `359bd123bf077ffd197d3e059422f4bf309bc050` 的公开代码主要沿用 Diffusers attention；`models/latte_t2v.py:761-779` 将 2D/3D mask 转为 `-10000` attention bias。这是 dense/broadcast bias 路径，不能作为长序列 custom sparse kernel 的实现证据。该不一致需在落地时避免：论文算法级压缩不自动给出 kernel 级稀疏。
