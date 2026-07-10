# MInference 1.0 精读

NeurIPS 2024 Spotlight。它按 head 分配 A-shape、vertical-slash、block-sparse 等模式；对输入在线近似构造动态 block mask，随后用三类 GPU kernel（PIT、Triton、FlashAttention）计算（`paper.txt:150-162`）。

这是“mask 先被近似/索引化，再按 pattern dispatch kernel”的典型路径。它解释了为何通用 dense attention 即使支持 causal 也不会自动利用任意稀疏：kernel 必须了解 pattern 并拥有相应 tile traversal。原工作主要是 LLM prefill；迁移到 bidirectional video DiT 时不能照搬 causal pattern，且多 denoising step 会重复 planner 成本。
