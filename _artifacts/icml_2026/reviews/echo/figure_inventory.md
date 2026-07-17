# ECHO Figure Inventory

- Paper: *ECHO: Elastic Speculative Decoding with Sparse Gating for High-Concurrency Scenarios*
- Source: arXiv:2604.09603v2, `paper.pdf`; rendered at 180 DPI with Poppler to 1489 x 2105 PNG pages.
- Contact-sheet triage: `figures/contact-sheet.png`, passed 2026-07-17.
- Individual inspection: both crops opened at original resolution and inspected at 100%, passed 2026-07-17.

| Object | PDF page | Source dimensions | Crop bbox `(x,y,w,h)` | Complete caption | Local path | Linked claim / report section | Source URL | QA |
|---|---:|---|---|---|---|---|---|---|
| Figure 3 | 4 | 1489 x 2105 px | `(135,190,1220,850)` | **Overview of the ECHO Framework.** (1) Super-Tree Construction: Draft trees are evaluated (truncated or extended) only at sparse gates. (2) Unified Elastic Budget Scheduler: Under a global verification cap ($K_{max}$), the scheduler dynamically adapts resource allocation. In Low-Load scenarios, the budget saved by truncation is reused locally to widen the current tree. In High-Load scenarios, budget saved from truncated low-confidence requests is reallocated to extend the depth of high-confidence requests. (3) Flatten & Pack: Finally, the ragged batch formed by requests with varying token counts is packed into a dense, kernel-compatible layout for efficient verification. | `figures/crops/fig3_echo_framework_caption.png` | Super-tree, sparse gating, elastic budget scheduling, flatten-and-pack / Sec. 3 | https://arxiv.org/pdf/2604.09603v2 | Passed contact-sheet and individual 100% QA; exactly one numbered object, complete caption, no page chrome/neighboring object/body paragraph; narrow safety margins. |
| Figure 5 | 10 | 1489 x 2105 px | `(135,190,1220,830)` | **Main results on High-Load Case (BS > 1).** We evaluate ECHO against EAGLE3 and two ECHO variants on three benchmarks using four model configurations. The maximum improvement percentage below each column is against EAGLE3. | `figures/crops/fig5_high_load_results_caption.png` | High-concurrency throughput and dense/fixed ablations / Sec. 4 | https://arxiv.org/pdf/2604.09603v2 | Passed contact-sheet and individual 100% QA; exactly one numbered object, complete caption, no section heading/body paragraph/page chrome; axes and legends readable. |

