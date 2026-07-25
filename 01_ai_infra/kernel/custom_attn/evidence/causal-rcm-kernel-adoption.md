# Causal-rCM：custom-attention 采用证据

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：[Causal-rCM assets](../../../../02_model_systems/multimodal_generation/assets/papers/causal-rcm/)
> - 相关文档：[Canonical Paper](../../../../02_model_systems/multimodal_generation/papers/causal-rcm.md)，[Figure inventory](figure-inventory.md)

完整 Paper 与原论文图由 Multimodal Generation 统一拥有。本记录仅保留对 custom-attention 的可复用判断：Causal-rCM 将 clean/noisy block 的可见性编码为规则、`BlockMask` 与 JVP-aware kernel contract，而非 materialized dense mask。该设计直接支撑的是训练语义与可扩展的 mask lowering；论文报告的端到端收敛收益同时混合了 consistency method、training recipe、JVP 与系统配置，不能归因给 kernel。

可用的机制证据是 [Fig.3](../../../../02_model_systems/multimodal_generation/assets/papers/causal-rcm/fig3-causal-training-paradigms-caption.png) 和 [Fig.4](../../../../02_model_systems/multimodal_generation/assets/papers/causal-rcm/fig4_recipe_comparison_caption.png)。后续 kernel 采用应单独验证 forward、JVP 与 backward 的后端覆盖，而不是把 predicate 表达能力等同于物理 tile 跳过。
