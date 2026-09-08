# Approximate Speculative Decoding Figure Inventory

Paper: *Approximate Speculative Decoding* (`arXiv:2608.03447v3`).

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Evolution](../surveys/evolution.md)
> - 对应论文：[Approximate Speculative Decoding](../papers/approximate-speculative-decoding.md)
> - 正式资产：`../assets/papers/approximate-speculative-decoding/`

All crops were rendered from the arXiv v3 PDF at 180 dpi. Source page dimensions are 1530 x 1980 pixels. Bounding boxes use `(x, y, width, height)` in source-page pixels. Every counted crop is embedded exactly once in the canonical Paper, adjacent to the claim it supports. Batch contact-sheet QA and individual 100% QA passed after recropping Figure 1 and Figure 5 captions.

| Object | PDF page | Crop bbox | Complete caption | Local crop | Linked claim / section | Source URL | QA |
|---|---:|---|---|---|---|---|---|
| Figure 1 | 1 | `(798, 572, 597, 658)` | “Figure 1: ASD verification. Strict verification stops at mismatch E. ASD accepts E within budget, reuses the target-greedy suffix F, G under the realized prefix, and recovers at H after the same target pass.” | `../assets/papers/approximate-speculative-decoding/fig1_asd_verification_caption.png` | Algorithm overview; §0.3, §2.1, §4.5 | https://arxiv.org/abs/2608.03447v3 | passed; recropped then individually inspected |
| Figure 3 | 3 | `(134, 140, 598, 633)` | “Figure 3: Verifier-side opportunity. (a) Omega-hat(tau,3) measures low-regret mismatches followed by at least three target-greedy draft tokens. (b) Fixed-workload TPS change over strict DSpark. The panels are complementary, not causal.” | `../assets/papers/approximate-speculative-decoding/fig3_opportunity_caption.png` | Opportunity existence and non-causal boundary; §2.2 | https://arxiv.org/abs/2608.03447v3 | passed; individually inspected |
| Figure 4 | 3 | `(797, 141, 600, 503)` | “Figure 4: Preliminary speed-quality frontier. Budget and cap move the discovery trade-off, motivating joint local and request-level controls. The frontier selects a conservative configuration; it is not a holdout result.” | `../assets/papers/approximate-speculative-decoding/fig4_speed_quality_frontier_caption.png` | Discovery-only control selection; §6.3 | https://arxiv.org/abs/2608.03447v3 | passed; individually inspected |
| Table 1 | 5 | `(134, 134, 1266, 427)` | “Table 1: Results for Qwen3-14B with DSpark-14B (B = 8, g = 0.25, M = 2). Speedups are relative to target-only decoding. ASD consistently outperforms matched strict speculative decoding, with small task-dependent accuracy changes under natural-EOS decoding. Parentheses denote confidence-interval half-widths; accuracy changes are reported per task and not averaged across heterogeneous metrics.” | `../assets/papers/approximate-speculative-decoding/table1_main_results_caption.png` | Seven-task primary results and numeric inconsistency; §6.1 | https://arxiv.org/abs/2608.03447v3 | passed; individually inspected |
| Figure 5 | 5 | `(790, 610, 610, 385)` | “Figure 5: Regret-gate sweep on GSM8K under natural-EOS decoding (n = 256, one seed).” | `../assets/papers/approximate-speculative-decoding/fig5_regret_gate_caption.png` | Gate/quality trend; §5.1 | https://arxiv.org/abs/2608.03447v3 | passed; recropped then individually inspected |
| Table 2 | 6 | `(135, 135, 1262, 488)` | “Table 2: Cross-family ASD results under matched fixed-work and natural-EOS protocols. Speedups are measured relative to target-only decoding. Values in parentheses denote the corresponding confidence intervals.” | `../assets/papers/approximate-speculative-decoding/table2_cross_family_caption.png` | DSpark/EAGLE3/Medusa transfer; §6.2 | https://arxiv.org/abs/2608.03447v3 | passed; individually inspected |
| Table 3 | 6 | `(135, 678, 590, 421)` | “Table 3: One-at-a-time ASD control sweeps on GSM8K. Blue cells indicate the selected operating points.” | `../assets/papers/approximate-speculative-decoding/table3_control_sweeps_caption.png` | B/g/M one-at-a-time sensitivity; §5.2, §6.3 | https://arxiv.org/abs/2608.03447v3 | passed; individually inspected |
| Figure 6 | 7 | `(134, 141, 600, 638)` | “Figure 6: ASD ablations with Qwen3-14B + DSpark-14B: (a) request-budget response, (b) draft-horizon response under fixed-work decoding (n = 64, one seed), (c) MARS-style and Fuzzy-style local controls at B = 8, and (d) synchronized per-token latency.” | `../assets/papers/approximate-speculative-decoding/fig6_system_ablation_caption.png` | Control mechanism and latency attribution; §6.4 | https://arxiv.org/abs/2608.03447v3 | passed; individually inspected |
| Figure 7 | 7 | `(798, 141, 598, 655)` | “Figure 7: DeepSeek-V4-Flash + DSpark acceptance ablations on eight H20 GPUs: (a) GSM8K gate sweep (n = 256), (b) GSM8K power-set evaluation (n = 744), (c) GSM8K-Confirm validation (n = 1,000), and (d) cross-task accepted tokens per proposal (A/P).” | `../assets/papers/approximate-speculative-decoding/fig7_deepseek_acceptance_caption.png` | Acceptance-only large-model evidence; §6.5 | https://arxiv.org/abs/2608.03447v3 | passed; individually inspected |

## Omitted source visual

- Figure 2 is intentionally not extracted as a delivery crop. It illustrates that different token trajectories can yield the same normalized arithmetic answer, but carries no additional algorithm, ablation, primary-result, or guarantee evidence beyond the report's explicit warning that token divergence may or may not preserve task correctness. The claim is reconstructed in prose and the visual is redundant for the review's decision boundary.

Coverage check: 9 crops, 9 inventory rows, 9 Markdown image references. No extracted crop is unused. Contact sheet: `figures/contact-sheet.png`.
