# Figure Inventory

All counted crops come from the complete arXiv v1 camera-ready PDF rendered at 200 DPI. Source pages are 1700 × 2200 pixels. The contact sheet was used for batch triage, followed by individual inspection at original resolution on 2026-07-24.

| Paper | Object/type | PDF page | Source page dimensions | Crop bbox `(x, y, width, height)` | Complete caption | Local path | Linked claim | Report section | Source URL | QA status |
|---|---|---:|---|---|---|---|---|---|---|---|
| Flex-Forcing | Figure 3 / mechanism | 3 | 1700 × 2200 px | `(140, 190, 1420, 470)` | **Figure 3.** (Left) Flexible chunking for bridging the autoregressive and bidirectional video generation. Flex-Forcing adjusts chunk granularity across noise levels while a unified self-attention mechanism supports both causal and bidirectional inference. (Right) The mixed attention with causal tokens and non-causal tokens. We add a timestep dependent K-Projection at the clean cache from past frames. | `figures/crops/fig3-flexible-chunking-mechanism-caption.png` | Flexible frame/timestep chunking and noise-aligned cached-key conditioning unify causal, hybrid, and bidirectional regimes. | `analysis.md#32-模型与系统架构` | <https://arxiv.org/pdf/2607.03509> | **passed** — contact-sheet triage and individual 100% QA; exactly one numbered figure plus full caption; labels readable; no neighboring text; tight 8–32 px safety margin where layout permits. |
| Flex-Forcing | Table 2 / result-system | 6 | 1700 × 2200 px | `(835, 755, 675, 695)` | **Table 2.** Comparisons of performance for 5s videos. *: We sample videos from the official checkpoint and test its performance. Here, the NFE of the causal distillation method contains N steps for denoising and 1 step for caching. | `figures/crops/table2-five-second-performance-caption.png` | On GB200, selected Flex-Forcing schedules shift the speed–quality frontier, but matched fine-grained scheduling does not uniformly beat every Self-Forcing row. | `analysis.md#41-5-秒主结果质量与速度分开看` | <https://arxiv.org/pdf/2607.03509> | **passed after recrop** — initial crop clipped the last caption line and was rejected; final crop passes contact-sheet and individual 100% QA, includes exactly one table plus complete caption, and excludes Section 5/body text. |

## Counted visual totals

- Mechanism: 1
- Result/ablation/system evidence: 1
- Total: 2
- Contact sheet: `figures/contact-sheet.png`

