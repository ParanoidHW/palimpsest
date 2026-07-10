# Cosmos 3 精读（本地一手材料）

Cosmos 3 是本调研的统一多模态锚点：reasoner 使用 causal attention，generator 使用 full attention；两者混在一般 FlexAttention mask 中会使 kernel 对语义结构不透明。本地精读材料 `02_model_systems/multimodal_generation/典型模型/Cosmos3.md:3213-3257` 记录其 two-way flat attention 将该层拆为两个 variable-length kernel invocation，并报告相对 FlexAttention baseline 的 Nano 训练吞吐 +22%。

这不是把一个任意稀疏 `[L,L]` mask 交给通用 kernel，而是在模型层先按语义切分 token stream，分别落到 causal/full 的高效变长调用。对统一模型的工程结论：若可见性由少数矩形/流边界描述，优先 lowering 为多个 dense/causal varlen call；只有无法分解的 window/anchor/route 才应使用 block sparse runtime。

硬件后端记录：Hopper 使用 FlashAttention-3，GB200 使用 NATTEN/CUTLASS 路径；该事实来自本地论文/source audit，不扩展为普适性能结论。
