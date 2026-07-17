# DODO Delegated Handoff

- Status: complete
- Paper: *DODO: Discrete OCR Diffusion Models*, arXiv:2602.16872v2
- Verified venue: ICML 2026 **workshop presentation** at 4th Structured Probabilistic Inference & Generative Modeling; not verified as Main Conference acceptance
- Recommended formal slug: `dodo`
- Dispatch: `icml2026-dodo-011`; agent task: `review_dodo`
- Task packet SHA-256: `7587ad4357aabc417e8bfd84f3e3cc3d75de3c83fdf80cc1ceb300ae377eaa29`
- Skill-tree SHA-256: `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`
- Agent-contract SHA-256: `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`

## Artifacts And Validation

- Core: `analysis.md`, `figure_inventory.md`, `review_checklist.md`, `openreview_reviews.md`
- Sources: `paper.pdf`, `paper.html`, `arxiv_metadata.xml`, `extracted_text/paper.md`, `extracted_pdf/extracted_text/`
- Venue evidence: `logs/icml_virtual_search.html`, `logs/icml_workshop_54089.html`
- Selected third-party code: `code/Discrete-OCR-Diffusion-Models/`, commit `21e2043cf995d2884ab75e473e9ee214d342e23c`; explicitly not DODO implementation
- Visuals: four accepted crops V1–V4 and `figures/contact-sheet.png`; all passed contact-sheet and individual original-resolution QA
- `deliverable_manifest.json`: Draft 2020-12 structural validation passed; all required semantic checks passed with empty errors
- `artifact_manifest.sha256`: generated last and verified with `sha256sum -c`

## Synthesis Claims

1. Vanilla global MDM OCR fails through irreversible coordinate synchronization: unknown length and positional anchoring combine with carry-over unmasking so early offset errors cannot be shifted. Evidence: `analysis.md` §3.1–3.4, paper §4.2, Figure 4.
2. Block structure is strongly supported, but training consistency is essential: inference-only block decoding gives NED 0.951, while matched block training gives 0.067. Evidence: `analysis.md` §4.2, Table 2/V3.
3. Exact caching changes algorithm semantics, not only runtime: approximate freezing of a Bidir model collapses NED to 0.805–0.978, while block-causal train/test gives 0.069 at block 32. Evidence: `analysis.md` §4.2 and §7, Table 3/V4.
4. The paper's 5× result is an end-to-end bundle: 103.69/21.00=4.94× versus cached AR; cache-off parallel decoding gives 42.80/2.18=19.63×. Inference hardware/batch/timing are absent, so no hardware-independent latency claim is made. Evidence: `analysis.md` §4.1/§4.4/§7, Figure 5/V2.
5. Accuracy is competitive but comparisons remain training-confounded: DODO improves same-size Qwen2.5-VL-3B NED 0.184→0.069, yet uses specialized OCR diffusion training. Evidence: `analysis.md` §4.1, paper Table 1.

## Promotion Candidates

- V1 Figure 4 mechanism: `figures/crops/fig4-full-vs-block-diffusion-caption.png`, PDF p.5, bbox `(110,205,780,460)`.
- V2 Figure 5 throughput: `figures/crops/fig5-throughput-comparison-caption.png`, PDF p.6, bbox `(910,1580,905,625)`.
- V3 Table 2 synchronization/block ablation: `figures/crops/table2-block-structure-ablation-caption.png`, PDF p.7, bbox `(105,170,815,395)`.
- V4 Table 3 cache trade-off: `figures/crops/table3-block-size-cache-caption.png`, PDF p.7, bbox `(895,170,925,665)`.

## Blocked Or Skipped Evidence

- arXiv source: interrupted e-print transfer left only invalid `source/source.partial.tar.gz`; PDF+HTML are primary evidence.
- PDF transport: `paper.pdf` text and selected pages are readable, but interrupted range transport mismatches arXiv ETag and emits appendix XObject warnings; every counted crop comes from individually verified clean-rendering pages 5–7.
- Public reviews: no paper-level forum/reviews/decision/rebuttal identified; workshop-level forum is not substituted.
- Official code/checkpoints: unavailable. The pinned repo is a third-party pre-paper seminar project and cannot validate DODO.
- Generated diagram: skipped because installed CLI lacks mandatory `responses-doc --input-file analysis.md`; no prompt-only substitute.
- Speed reproducibility: inference GPU, dtype, batch, length distribution and timing protocol are missing, limiting the 5× claim to the paper's environment.
- Suspected out-of-folder edits: none observed; this is not a filesystem-isolation self-certification.

