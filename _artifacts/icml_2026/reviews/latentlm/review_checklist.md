# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: reused `_artifacts/icml_2026/reviews/latentlm/`; all generated artifacts remain below it.
- [done] W1 Delegated input: verified task packet SHA-256 `7becb24bd3e53660835329782e1e8e393a9c571b1d76c1c14ef314d20f192ac3`, complete skill-tree SHA-256 `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`, and contract SHA-256 `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`; `task_packet.yaml` is parent-owned and unchanged.
- [done] W2 Primary sources: acquired exact v1 PDF, arXiv metadata page, complete extracted LaTeX tree, and recorded source-stream trailing-garbage limitation.
- [skipped-with-reason] W2 Public reviews: `openreview_reviews.md` records exact-title API HTTP 403, failed search backend, and absence of venue/OpenReview metadata on arXiv; no review claims were available to cross-check.
- [done] W2 Code: official UniLM `LatentLM/` acquired at commit `833df7e7832e5064a281131ee64a481afa8e5b95`; public scope and missing MLLM/TTS/checkpoints classified in `analysis.md#8-开源代码对照`.
- [done] W3 Text: `pdftotext -layout` output retained at `extracted_text/paper.txt`.
- [done] W3 Visuals: accepted Figure 2 and Figure 7 crops contain one numbered object with full caption and exclude neighboring content.
- [done] W3 Inventory: `figure_inventory.md` records 1530x1980 source pages, exact `(x,y,width,height)` bboxes, captions, paths, claims, URLs, and QA.
- [done] W3 Visual QA: `figures/contact-sheet.png` triaged, then both crops opened individually at original resolution and accepted.
- [done] W4 Evidence discipline: key claims map to Sec./Eq./Fig./Table/code paths throughout `analysis.md`.
- [done] W4 Design rationale: six core designs classified with author-stated rationale, concrete problem, causal mechanism, trade-off, and evidence.
- [done] W4 Claim matrix: `analysis.md#42-技术-claim-证据矩阵` classifies direct/sensitivity/confounded/correlation/none evidence.
- [done] W4 Terminology and symbols: centralized `analysis.md#01-术语与符号解释` covers key terms, formula variables, derived infra symbols, sources, and ambiguities.
- [done] W5 Related work: `analysis.md#5-related-work-对比` compares VQ-AR, DiT, Transfusion, MAR/GIVT and fairness.
- [skipped-with-reason] W6 OpenReview cross-check: no public review/rebuttal/decision evidence could be acquired; precise attempts/effect in `openreview_reviews.md`.
- [done] W7 Infrastructure: compute, memory, data types, bandwidth utilization limits, heterogeneity, runtime, scheduler, GQA and serving analyzed in Section 7.
- [done] W8 Code/config: ImageNet architecture/loss/dtype/GQA/DPM-Solver paths inspected at pinned commit; unavailable MLLM/TTS/checkpoints explicitly unverified.
- [done] W9 Gain attribution: Section 4.4 separates matched-ish, sensitivity, confounded and unverified effects.
- [done] W10 Report: complete Chinese `analysis.md` written with inline Figure 2/7 evidence and limitations.
- [done] W10 Revision information: initial version `1.0.0`, revision `rev-latentlm-20260716-initial`, no predecessor.
- [skipped-with-reason] W11 Generated diagram: parent contract states installed CLI lacks mandatory `responses-doc --input-file analysis.md`; prompt-only generation is prohibited.
- [done] D1 Delegated handoff: `agent_handoff.md` contains status, exact identity, provenance hashes, artifacts, evidence-linked claims, promotion candidates, limitations, and suspected-write statement; frozen before final hashing.
- [done] D2 Deliverable manifest: preliminary schema/semantic validation passed; frozen checklist/handoff hashes are incorporated in the final `deliverable_manifest.json`, whose Draft 2020-12 and semantic checks pass with empty errors.
- [done] D3 Artifact manifest: preflight manifest generated and verified; final `artifact_manifest.sha256` is regenerated last and verified after final deliverable hashing.

## Quality Checks

- [done] Q1 Both local Markdown image links resolve.
- [done] Q2 FI-1/FI-2 each contain one numbered object and complete caption, exact dimensions/bbox, readable tight crops, and both QA passes.
- [done] Q3 All key numbers cite Table 1/3/4, Figure 7, or labeled relative calculations.
- [done] Q4 Section 4.2 classifies all central technical claims and repeats unsupported points in limitations.
- [skipped-with-reason] Q5 Parent contract confirms required `responses-doc --input-file analysis.md` capability is absent; no prompt-only diagram generated.
- [done] Q6 Code claims cite `code/unilm/LatentLM/...` paths and commit `833df7e7832e5064a281131ee64a481afa8e5b95`.
- [done] Q7 Centralized term/symbol tables cover method, formulas, metrics, infra derivations, sources, scope, values and ambiguities.
- [done] Q8 Diffusion timestep, AR position, backbone, token head, VAE decode, GQA runtime, and frame rate are stage-qualified.
- [skipped-with-reason] Q9 No public reviews/decision/rebuttal were accessible; exact attempts and impact are recorded.
- [done] Q10 Gain attribution labels matched-ish, sensitivity, confounded, correlation-only and unverified evidence.
- [done] Q11 README has no released checkpoints; metadata claims are explicitly unverified.
- [done] Q12 Source trailing garbage, API 403, search failure, partial public code and diagram capability are recorded with effects.
- [done] Q13 Task packet hash remains verified; handoff/schema/artifact manifest complete; no suspected out-of-folder edit observed, without self-certifying isolation.
- [done] Q14 Final manifest structural and semantic validation passes and agrees with hashes, revision, visual counts, evidence, provenance, frozen checklist/handoff and limitations.
- [done] Q15 Six core designs have complete rationale entries; inference/absence is explicit.
- [done] Q16 Initial revision metadata matches `analysis.md`; one bootstrap, current/latest identity correct, no unresolved migration.

## Final Classification

- [done] F1 Required files exist and agree on two counted visuals; contact sheet exists.
- [done] F2 No item remains pending or unclassified.
- [done] F3 Handoff states all material limitations and does not upgrade unavailable evidence.
