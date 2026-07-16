# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: reused `_artifacts/icml_2026/reviews/xdlm/` and created the required artifact layout within the owned boundary.
- [done] W1 Delegated input: verified `task_packet.yaml` SHA-256 `384e3460ef83446ce9da2c3aa0bb431e397050f4e103b9cd9851eeb6ab4759db`, deterministic complete skill-tree SHA-256 `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`, and agent-contract SHA-256 `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e`; packet unmodified.
- [done] W2 Primary sources: acquired exact arXiv v1 PDF and metadata; classified corrupt `source.tar` as blocked after `Unexpected EOF`.
- [skipped-with-reason] W2 Public reviews: no public OpenReview forum/review/decision was discoverable; API query returned HTTP 403; recorded in `openreview_reviews.md`.
- [done] W2 Code: acquired official GitHub snapshot at commit `66c34ac5a3945d61e0e398f302bf751b5fadfa24` under `code/XDLM/`.
- [done] W3 Text: extracted 32-page searchable text with the skill helper under `extracted_text/pdf_assets/extracted_text/`; retained ar5iv cross-check text.
- [done] W3 Visuals: accepted Figure 1, Figure 3, and Figure 4 crops with complete captions and single numbered objects.
- [done] W3 Inventory: completed `figure_inventory.md` with 1360x1760 source dimensions and exact bboxes.
- [done] W3 Visual QA: `figures/contact-sheet.png` triage passed; all three crops inspected individually at original resolution and recropped until clean.
- [done] W4 Evidence discipline: important claims mapped to sections/equations/figures/tables/code in `analysis.md`.
- [done] W4 Design rationale: six core designs recorded with source status, target problem, mechanism, trade-offs, and evidence.
- [done] W4 Claim matrix: technical claims classified as theory, sensitivity, direct, indirect, bundled/confounded, or unverified.
- [done] W4 Terminology and symbols: centralized chapter covers eight key terms and twelve applicable symbols with provenance and ambiguity notes.
- [done] W5 Related work: MDLM, UDLM, GIDD, and Flow Matching compared by mechanism and fairness.
- [skipped-with-reason] W6 OpenReview cross-check: public review evidence unavailable as documented; no reviewer claim was inferred.
- [done] W7 Infrastructure: compute, memory, bandwidth-unavailability, dtype, DDP, CPU/GPU/NPU heterogeneity analyzed.
- [done] W8 Code/config: architecture/loss/data/evaluation/runtime inspected; checkpoint metadata marked unverified.
- [done] W9 Gain attribution: mechanism, scalar algebra, continual pretraining, and system effects separated.
- [done] W10 Report: complete Chinese `analysis.md` written with inline evidence and limitations.
- [done] W10 Revision information: initial `1.0.0` / `rev-initial-xdlm` history matches manifest and has no predecessor.
- [skipped-with-reason] W11 Generated diagram: installed CLI lacks mandatory `responses-doc --input-file analysis.md`; prompt-only art prohibited.
- [done] D1 Delegated handoff: contract-compliant `agent_handoff.md` finalized and frozen.
- [done] D2 Deliverable manifest: preliminary and final Draft 2020-12 structural and semantic validations passed with empty errors.
- [done] D3 Artifact manifest: preflight verified; final regeneration/verification is the last operation after frozen manifest.

## Quality Checks

- [done] Q1 All local Markdown image links resolve.
- [done] Q2 All three accepted crops contain one object and full caption, have recorded dimensions/bbox, tight boundaries, and both QA passes.
- [done] Q3 Every key number maps to paper evidence or is labeled as unavailable/derived.
- [done] Q4 Every claimed technical point has an evidence classification; unsupported attribution is explicit.
- [skipped-with-reason] Q5 Generated diagram precisely skipped because mandatory document-input capability is absent.
- [done] Q6 Code claims cite local paths and pinned commit hash.
- [done] Q7 Central terminology/symbol chapter and manifest entries cover all key notation used in the review.
- [done] Q8 Noise mask, attention mask, forward corruption, reverse sampling, and serving/runtime meanings are stage-qualified.
- [skipped-with-reason] Q9 Public OpenReview evidence was not accessible; attempts and impact recorded.
- [done] Q10 Gain attribution uses matched evidence or explicit bundled/inferred labels.
- [done] Q11 Checkpoint metadata is explicitly unverified; inspected local configs are distinguished.
- [done] Q12 Source corruption, API 403, PDF transfer retries, missing qpdf, checkpoint metadata, and diagram capability are recorded with effects.
- [done] Q13 Task packet preserved; delegated handoff and artifact manifest produced; no suspected out-of-folder write, without self-certifying isolation.
- [done] Q14 Final schema and semantic validation pass with manifest/artifact/checklist consistency.
- [done] Q15 Every core design has a complete rationale entry; code-derived inference is labeled.
- [done] Q16 Revision metadata matches and contains exactly one valid initial bootstrap entry.

## Final Classification

- [done] F1 Required documents exist and agree on 3 counted visuals; contact sheet exists.
- [done] F2 No workflow or quality item remains pending or unclassified.
- [done] F3 Handoff states every material limitation and keeps source/checkpoint/review evidence qualified.
