# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: reused `_artifacts/icml_2026/reviews/dodo`; all writes are confined to this owned paper folder.
- [done] W1 Delegated input: verified `task_packet.yaml` SHA-256 `7587ad4357aabc417e8bfd84f3e3cc3d75de3c83fdf80cc1ceb300ae377eaa29`, complete skill-tree SHA-256 `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`, and agent-contract SHA-256 `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`; packet remains parent-owned and unchanged.
- [done] W2 Primary sources: acquired arXiv v2 `paper.pdf`, `paper.html`, `arxiv_metadata.xml`, and official ICML pages; `source/source.partial.tar.gz` is precisely classified as an invalid interrupted download, not source evidence.
- [done] W2 Public reviews: `openreview_reviews.md` preserves API 403/search limitations and distinguishes the workshop-level forum from an unavailable paper-level forum.
- [done] W2 Code: no author code/checkpoint found; selected third-party repo fixed at commit `21e2043cf995d2884ab75e473e9ee214d342e23c` and classified as non-DODO.
- [done] W3 Text: arXiv HTML converted to `extracted_text/paper.md`; PyMuPDF extraction retained under `extracted_pdf/extracted_text/`.
- [done] W3 Visuals: four semantic PDF crops contain exactly one numbered object and full caption after rejecting/reworking clipped crops.
- [done] W3 Inventory: `figure_inventory.md` records 1836x2376 source pages and exact `(x,y,w,h)` for V1–V4.
- [done] W3 Visual QA: final `figures/contact-sheet.png` passed triage; V1–V4 each opened and passed original-resolution 100% inspection. Rejected rounds are documented.
- [done] W4 Evidence discipline: `analysis.md` maps synchronization, block, cache, NED and TPS claims to §§4–6, Eq. 5, Figures 4–5 and Tables 1–3.
- [done] W4 Design rationale: §3.2 covers block factorization/training, block-causal exact cache, Bidir history, masking/timestep and confidence threshold with causal mechanism/trade-off/evidence.
- [done] W4 Claim matrix: §4.3 classifies every central point as direct, indirect, confounded, sensitivity or missing.
- [done] W4 Terminology and symbols: centralized §0.1 defines eight terms and ten author/analysis symbols, including the paper's conflicting use of `B`.
- [done] W5 Related work: §5 compares specialized AR OCR, global MDM, block diffusion and the third-party OCR diffusion project.
- [skipped-with-reason] W6 OpenReview cross-check: no paper-level reviews/decision/rebuttal were publicly identifiable; exact evidence and effect are recorded in `openreview_reviews.md` and §6.
- [done] W7 Infrastructure: §7 covers compute, bf16, memory/KV formulas, unquantifiable bandwidth utilization, interconnect gaps, serving and CPU/GPU/NPU boundaries.
- [done] W8 Code/config: §8 inspects the pinned third-party repo and explains why its annealed global diffusion cannot validate DODO; official code/checkpoints are unavailable.
- [done] W9 Gain attribution: §4.4 separates block-training, cache-off parallel, exact-cache bundle and end-to-end AR comparisons.
- [done] W10 Report: complete Chinese `analysis.md` includes four inline evidence visuals, limitations, inspirations and unresolved questions.
- [done] W10 Revision information: new delivery has one `initial` revision `rev-dodo-initial`, version `1.0.0`, with no predecessor.
- [skipped-with-reason] W11 Generated diagram: parent contract states installed CLI lacks mandatory `responses-doc --input-file analysis.md`; prompt-only art is prohibited.
- [done] D1 Delegated handoff: `agent_handoff.md` contains identity/provenance, artifacts, evidence-linked claims, promotion candidates and limitations.
- [done] D2 Deliverable manifest: `deliverable_manifest.json` passed Draft 2020-12 and all required semantic checks with empty errors after frozen hashes were recomputed.
- [done] D3 Artifact manifest: `artifact_manifest.sha256` generated last over every paper-folder file except itself and verified with `sha256sum -c`.

## Quality Checks

- [done] Q1 All four local Markdown image links resolve.
- [done] Q2 V1–V4 meet single-object/full-caption/source-dimension/bbox/readability/tight-bound requirements and passed both QA stages.
- [done] Q3 NED/TPS/deltas map to Tables 1–3/Figure 5 or are labeled analysis-derived arithmetic.
- [done] Q4 §4.3 explicitly classifies supported, partial, confounded and unverified claims.
- [skipped-with-reason] Q5 Exact limitation: installed OpenRouter ICU CLI has no contract-required `responses-doc --input-file analysis.md` capability.
- [done] Q6 Third-party code claims cite local paths and commit `21e2043cf995d2884ab75e473e9ee214d342e23c`; no official-code claim is made.
- [done] Q7 §0.1 centrally covers key paper terms, formula variables, metrics and derived system symbols with sources and ambiguities.
- [done] Q8 Full/global/block diffusion, Bidir, block-causal and approximate/exact cache are stage-qualified.
- [skipped-with-reason] Q9 Paper-level public reviews/decision/rebuttal/discussion were unavailable; workshop evidence is not substituted.
- [done] Q10 Attribution uses matched Table 2 evidence or explicitly labels bundles/confounds.
- [done] Q11 DODO checkpoints/configs are marked unavailable/unverified; third-party repo identity is grounded in README/commit.
- [done] Q12 Interrupted source/PDF downloads, invalid partial source, PDF appendix XObject warnings, API 403 and their effects are recorded.
- [done] Q13 Task packet hash remains unchanged; handoff/schema/artifact manifest exist. No suspected out-of-folder edit observed; no filesystem-isolation self-certification is claimed.
- [done] Q14 Final manifest agrees with hashes, visual counts, provenance, terminology/design coverage, checklist/handoff and limitations; structural/semantic errors are empty.
- [done] Q15 §3.2 and manifest rationale entries cover all core designs without presenting inference as author intent.
- [done] Q16 Analysis/manifest both identify the single valid initial revision as latest; no migration issue exists.

## Final Classification

- [done] F1 `analysis.md`, `figure_inventory.md`, `deliverable_manifest.json` and contact sheet agree on four counted visuals (one mechanism, three result/system).
- [done] F2 No item remains pending or unclassified.
- [done] F3 Handoff states source/PDF transport, OpenReview, code/checkpoint, generated-diagram and speed-protocol limitations without upgrading unavailable evidence.
