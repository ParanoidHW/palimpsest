# Agent handoff: ECHO

- Status: complete.
- Exact paper: *ECHO: Elastic Speculative Decoding with Sparse Gating for High-Concurrency Scenarios*, arXiv:2604.09603v2; OpenReview forum `L31hKCWRsN`; independently verified `ICML 2026 spotlight`.
- Dispatch: `icml2026-echo-012`; task: `review_echo`.
- Provenance: task packet SHA-256 `e70b71ec11742df090f2e57d61ad76f0c478af568637e4ac0b35a245db76816c`; skill-tree SHA-256 `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`; agent-contract SHA-256 `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`.
- Artifacts: `analysis.md`, `figure_inventory.md`, `review_checklist.md`, `deliverable_manifest.json`, `openreview_reviews.md`, `figures/contact-sheet.png`, `artifact_manifest.sha256`.
- Validation: Draft 2020-12 schema and required semantic checks passed with empty errors; final artifact manifest verified.
- Recommended formal slug: `echo`.

## Synthesis claims

1. ECHO's core reframing is batch-level verification-budget scheduling, not merely a better per-request tree; evidence: `analysis.md` Sec. 2-3, paper Eq. 4 and Figure 3.
2. Sparse gating has a matched ablation: LLaMA3.1-8B at BS256 improves 10,978 to 11,551 tok/s (+5.22%) over dense gating; evidence: `analysis.md` Sec. 4, Figure 5.
3. Depth-aware thresholds have a matched ablation: Qwen3-235B at BS256 improves 3,046 to 3,207 tok/s (+5.29%) over fixed threshold; evidence: `analysis.md` Sec. 4, Figure 5.
4. The 14.41% Qwen3-235B gain over EAGLE3 is an end-to-end, confounded result because tree initialization, gating, scheduling and packing co-vary; evidence: `analysis.md` Sec. 3.5/4.1 and Appendix configuration.
5. Implementation and bandwidth claims remain unverified: no code, kernel timing, bytes moved, profiler, interconnect topology or tail-latency evidence; evidence: `analysis.md` Sec. 7-9 and `source/main.tex` Appendix Evaluation Details.

## Formal-promotion candidates

- Mechanism: `figures/crops/fig3_echo_framework_caption.png`, inventory row Figure 3. Promote to canonical paper assets after parent rewrites links.
- Result/system: `figures/crops/fig5_high_load_results_caption.png`, inventory row Figure 5. Promote to canonical paper assets after parent rewrites links.

## Blocked/skipped evidence

- Code/config implementation cross-check beyond paper appendix: unavailable because authors state code will be released later; kernel-level conclusions remain unverified.
- OpenReview review/meta-review/rebuttal text: forum notes endpoint returned HTTP 403; venue/spotlight status remains verified from primary submission metadata, but reviewer concerns were not used.
- Generated diagram: skipped because installed CLI has only `generate/edit`, not mandatory `responses-doc --input-file analysis.md`.
- No suspected out-of-folder write. Files were intentionally written only in the owned ECHO artifact folder; filesystem isolation is not self-certified.

