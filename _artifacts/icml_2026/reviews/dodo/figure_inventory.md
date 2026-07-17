# DODO Figure Inventory

Paper: **DODO: Discrete OCR Diffusion Models**, arXiv:2602.16872v2. Source PDF: `paper.pdf`, 15 pages, US Letter. All counted crops are PDF screenshots rendered by PyMuPDF at 216 DPI (source page PNG 1836x2376); coordinates are `(x, y, width, height)` in source-page pixels. Source URL: <https://arxiv.org/pdf/2602.16872v2>.

Contact-sheet triage: `figures/contact-sheet.png`, passed on 2026-07-17 after two rejected/reworked crop rounds. Individual crops below were then opened at original resolution and inspected at 100% on 2026-07-17.

| Row | Object | PDF page | Source dimensions | Crop bbox `(x,y,w,h)` | Complete caption | Local path | Linked claim / report section | QA |
|---|---|---:|---|---|---|---|---|---|
| V1 | Figure 4 | 5 | 1836x2376 | `(110,205,780,460)` | “Full vs. block diffusion. In standard full diffusion (left), MDM sampling is applied globally to the entire sequence. In contrast, block diffusion (right) restricts parallel sampling to discrete windows, processing blocks sequentially from left to right.” | `figures/crops/fig4-full-vs-block-diffusion-caption.png` | Block diffusion bounds synchronization scope; `analysis.md` §3.3 | passed: one object, full caption, panels/labels intact, no page chrome/neighbor/paragraph, tight margins |
| V2 | Figure 5 | 6 | 1836x2376 | `(910,1580,905,625)` | “Inference throughput comparison. DODO leverages parallel decoding, block-causal attention and KV-caching to achieve ≈104 tokens/sec, a 5× speedup over the autoregressive baseline.” | `figures/crops/fig5-throughput-comparison-caption.png` | Latency/throughput evidence and confounding; `analysis.md` §4.1, §4.4 | passed: one object, full caption/title/legend/axes, no adjacent prose, readable and tight |
| V3 | Table 2 | 7 | 1836x2376 | `(105,170,815,395)` | “Impact of block structure. Vanilla MDM fails even with Oracle length; block-wise training is essential.” | `figures/crops/table2-block-structure-ablation-caption.png` | Synchronization error and block-training ablation; `analysis.md` §4.2 | passed: one object, full caption/all rows/columns, no neighbor/section text, readable and tight |
| V4 | Table 3 | 7 | 1836x2376 | `(895,170,925,665)` | “Block size and caching. Approx. KV-Cache collapses; block-causal training enables exact caching with 5× speedup.” | `figures/crops/table3-block-size-cache-caption.png` | Cache accuracy/latency trade-off; `analysis.md` §4.2, §7 | passed: one object, full caption/all groups/rows/columns, no Table 2 or following paragraph, readable and tight |

## Rejected crop history

- Initial crop coordinates were mistakenly taken from a scaled preview; all four were clipped and rejected before counting.
- Second-round Figure 4 included adjacent right-column text, Figure 5 clipped its title/caption, and Tables 2/3 clipped left edges; all were rejected and recropped.
- Third-round Figure 5 retained a 1px adjacent-column trace; left bound was tightened from 900 to 910 before final acceptance.

