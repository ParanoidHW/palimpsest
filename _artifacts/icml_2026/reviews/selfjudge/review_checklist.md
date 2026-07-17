# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: owned folder `_artifacts/icml_2026/reviews/selfjudge`; required subdirectories are created during acquisition/extraction.
- [done] W1 Delegated input: `task_packet.yaml` SHA-256 `6a68355f02b360d73ff4fc3a70a86f68d788767d831b3be21dd5dbb883c6ba18`; skill-tree SHA-256 `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`; agent-contract SHA-256 `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`; all match packet/dispatch and packet remains parent-owned.
- [done] W2 Primary sources: exact v2 `paper.pdf`, `source/source.tar.gz`, extracted `source/`, and `arxiv_abs.html`; arXiv journal_ref confirms ICML 2026.
- [done] W2 Public reviews: `openreview_reviews.md` records no discoverable SelfJudge forum, exact-title API HTTP 403, and source/arXiv searches.
- [done] W2 Code: PDF/arXiv/source contain no official SelfJudge repo; code snapshot classified unavailable and implementation claims remain unverified.
- [done] W3 Text: `extracted_text/paper.txt`, generated with `pdftotext -layout`; 1,177 lines.
- [done] W3 Visuals: four final crops in `figures/crops/`, each exactly one Figure with full caption.
- [done] W3 Inventory: `figure_inventory.md` has page, 1530x1980 dimensions, exact `(x,y,width,height)`, caption, claim, URL, and QA for all four.
- [done] W3 Visual QA: `figures/contact-sheet.png` triaged; each crop inspected at original resolution. Figure 3 was recropped after caption truncation and Table 1 contamination were detected.
- [done] W4 Evidence discipline: `analysis.md` maps claims to §/Eq./Figure/Table/Appendix and labels reviewer inference.
- [done] W4 Design rationale: §3.2 covers seven core designs with why status, problem, mechanism, trade-off, evidence, and judgment.
- [done] W4 Claim matrix: §4.2 classifies direct ablation, sensitivity, runtime, indirect/confounded, and unverified claims.
- [done] W4 Terminology and symbols: centralized §0.1 defines nine terms and thirteen symbol groups with sources/ambiguity.
- [done] W5 Related work: §5 compares Standard SD, JudgeDecoding, AutoJudge, Top-k, and drafting-side methods.
- [done] W6 OpenReview cross-check: precise public-evidence unavailability in §6 and `openreview_reviews.md`; no reviewer claim presented as fact.
- [done] W7 Infrastructure: §7 covers compute, memory, dtype gaps, bandwidth formula/utilization, TP interconnect, CPU/GPU/NPU, and serving.
- [done] W8 Code/config: §8 classifies code unavailable; checks paper/source paths and marks checkpoint metadata unverified.
- [done] W9 Gain attribution: §4.4 separates accepted-length, two-stage, verifier overhead, and runtime evidence.
- [done] W10 Report: complete Chinese `analysis.md` with four inline evidence visuals and all mandatory sections.
- [done] W10 Revision information: §修订信息 has initial 1.0.0 / rev-selfjudge-initial entry with no predecessor.
- [skipped-with-reason] W11 Generated diagram: parent contract records installed OpenRouter ICU CLI lacks mandatory `responses-doc --input-file analysis.md`; prompt-only art is prohibited.
- [done] D1 `agent_handoff.md` written with exact paper identity, provenance, artifact paths, six synthesis claims, promotion candidates, limitations, and write-isolation note; frozen before final manifest.
- [done] D2 Preliminary manifest passed Draft 2020-12 structural validation; final manifest is regenerated after checklist/handoff freeze and validated again.
- [done] D3 `artifact_manifest.sha256` is generated last after final manifest; verification excludes itself and covers every other file in the owned folder.

## Quality Checks

- [done] Q1 All four local Markdown image links resolve to `figures/crops/`.
- [done] Q2 Four accepted crops contain one numbered Figure plus full caption; inventory and both QA passes are complete.
- [done] Q3 Key numbers cite Table 1/3, §4.5, Appendix, or are marked approximate/derived.
- [done] Q4 §4.2 explicitly classifies every central claim; likelihood-as-semantics is unverified.
- [skipped-with-reason] Q5 Generated-diagram handling: required `responses-doc --input-file analysis.md` capability is absent per parent contract; no prompt-only diagram will be made.
- [skipped-with-reason] Q6 Code is unavailable; paper/source claims cite `source/main.tex`, and no commit hash is invented.
- [done] Q7 §0.1 covers key terms, formula variables, metrics, provenance, sources, and ambiguity.
- [done] Q8 §0.1 and §3.3 distinguish offline suffix labeling, online hidden-state judge, alignment verification, and serving.
- [skipped-with-reason] Q9 No public SelfJudge OpenReview material was discoverable; `openreview_reviews.md` records attempts and effect.
- [done] Q10 §4.4 marks bridge comparisons as non-causal and separately labels direct timing/ablation.
- [done] Q11 §8.1 explicitly marks revision/config/dtype/chat template unverified.
- [done] Q12 Initial sandbox DNS failure, OpenReview HTTP 403, missing code/config, and generated-diagram limitation are recorded.
- [done] Q13 Task packet preserved; handoff and artifact manifest are produced; no suspected out-of-folder write observed (isolation not self-certified).
- [done] Q14 Final manifest structural and semantic checks pass and agree with terminology, rationale, visuals, provenance, checklist, handoff, and limitations.
- [done] Q15 Seven core designs have explicit rationale status, problem, mechanism, trade-off, and evidence judgment; inference is labeled.
- [done] Q16 Revision metadata is initial 1.0.0 with one bootstrap entry and matches analysis/manifest.

## Final Classification

- [done] F1 `analysis.md`, `figure_inventory.md`, manifest, four crops, and contact sheet exist and agree on 1 mechanism + 3 result/system visuals.
- [done] F2 Every workflow and quality item is done, blocked, or skipped-with-reason; no pending items remain.
- [done] F3 Final handoff and manifest state code, OpenReview, generated-diagram, network, and metadata limitations without claiming unavailable evidence.
