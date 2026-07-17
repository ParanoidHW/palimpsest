# Agent Handoff: SelfJudge

- Status: complete; final structural and semantic validation passed after freeze.
- Exact paper: `arxiv:2510.02329v2`, SelfJudge: Faster Speculative Decoding via Self-Supervised Judge Verification, ICML 2026 (`journal_ref` verified).
- Recommended formal slug: `selfjudge`.
- Dispatch: `icml2026-selfjudge-008`; task: `review_selfjudge`.
- Task packet SHA-256: `6a68355f02b360d73ff4fc3a70a86f68d788767d831b3be21dd5dbb883c6ba18`.
- Skill tree SHA-256: `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`.
- Agent contract SHA-256: `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`.

## Artifacts

- `analysis.md`: Chinese deep review and inline evidence.
- `paper.pdf`, `source/`, `extracted_text/paper.txt`: exact v2 primary material.
- `figure_inventory.md`, `figures/crops/`, `figures/contact-sheet.png`: four accepted figures and QA.
- `openreview_reviews.md`: precise public-review unavailability record.
- `review_checklist.md`, `deliverable_manifest.json`, `artifact_manifest.sha256`: frozen workflow and hash records.

## Synthesis Claims

1. SelfJudge labels draft/target mismatch tokens using a target-model prefix+suffix likelihood difference, then trains a logistic verifier; evidence: `analysis.md` §3.3–3.4, paper Eq.(6–8), Figure 2.
2. The online verifier does not see suffix tokens: it reads target hidden state and operates in parallel with alignment verification; evidence: `analysis.md` §0.1, §3.3, paper §3.2–3.4.
3. On one A100, SelfJudge-F reports +23.5% GSM8K and +46.3% MMLU throughput versus SD, with -0.2/-0.7 accuracy points; evidence: `analysis.md` §4.1, paper Table 3.
4. Suffix context has sensitivity evidence (Figure 4), while the claim that target likelihood equals semantic truth remains unverified without independent semantic/factual labels; evidence: `analysis.md` §4.2–4.3.
5. The OR combination relaxes strict target-distribution equivalence; reported quality preservation is benchmark-level, not a sampling theorem; evidence: `analysis.md` §3.2, §4.3, paper Eq.(3–5), Appendix Table 9.
6. Runtime attribution is incomplete because vLLM code, dtype, kernels, KV layout and telemetry are unavailable; evidence: `analysis.md` §7–8.

## Promotion Candidates

- Figure 2 mechanism: `figures/crops/fig2_method_caption.png`, inventory row Figure 2.
- Figure 1 cross-domain result: `figures/crops/fig1_intro_caption.png`, inventory row Figure 1.
- Figure 3 trade-off: `figures/crops/fig3_speed_performance_caption.png`, inventory row Figure 3.
- Figure 4 suffix sensitivity: `figures/crops/fig4_suffix_caption.png`, inventory row Figure 4.

## Limitations / Skips

- Official implementation and checkpoint metadata are unavailable; code/config conclusions remain unverified.
- No SelfJudge OpenReview forum/reviews/rebuttal/decision were discoverable; public review cross-check is skipped with evidence.
- Generated diagram skipped because mandatory `responses-doc --input-file analysis.md` capability is absent; prompt-only art prohibited.
- Initial sandbox DNS download failed and succeeded after approved curl escalation; OpenReview exact-title API returned HTTP 403.
- No suspected out-of-folder write. Filesystem isolation is not self-certified; ownership compliance is based on observed paths.
