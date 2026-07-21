# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: created standalone paper folder `_artifacts/magi-1/` with required extraction, figure, generated-diagram, and code subdirectories.
- [skipped-with-reason] W1 Delegated input: standalone invocation by the primary agent; no parent task packet, skill-tree hash, or agent contract applies.
- [done] W2 Primary sources: complete 61-page PDF at `paper.pdf` (SHA-256 `aa0697368aa6e109788c55c1f5bff23427bea1525f15048c3e83d385f5056406`), official HTML/metadata, and a classified incomplete source download at `source.tar`.
- [done] W2 Public reviews: `openreview_reviews.md` records that no MAGI-1 forum/review/decision/rebuttal was found by exact title/arXiv search.
- [done] W2 Code: official `code/MAGI-1-repo` commit `0fcefdef8ce2df37a3b8890979433c06eb003328` and `code/MagiAttention-repo` commit `d3eb7fd2b4358510ff46fa039fdcc7b2475589f7` acquired.
- [done] W3 Text: searchable official-HTML and PDF extractions retained at `extracted_text/paper.txt` and `extracted_text/paper_pdf.txt`.
- [done] W3 Visuals: four tight, single-object, full-caption crops accepted under `figures/crops/`.
- [done] W3 Inventory: `figure_inventory.md` records 1700x2200 source pages, page numbers, complete captions, exact bboxes, uses, and QA.
- [done] W3 Visual QA: `figures/contact-sheet.png` triaged and every accepted crop inspected individually at original resolution; right-clipped superseded crops were rejected.
- [done] W4 Evidence discipline: `analysis.md` maps core numerical/mechanism/system claims to paper sections, figures, tables, or official code.
- [done] W4 Design rationale: `analysis.md#32-设计动机与证据` separates author-stated and inferred rationales, mechanisms, alternatives, and evidence judgments.
- [done] W4 Claim matrix: `analysis.md#42-技术点证据矩阵` classifies direct, confounded, partial, and missing evidence.
- [done] W4 Terminology and symbols: centralized sourced term/symbol tables are in `analysis.md#01-术语与符号`, including three distinct window meanings and token-count symbols.
- [done] W5 Related work: `analysis.md#7-related-work` compares global video DiT, Diffusion Forcing/FVDM, causal distillation, and discrete AR.
- [skipped-with-reason] W6 OpenReview cross-check: no public MAGI-1 OpenReview forum/reviews/decision/rebuttal were found; evidence retained in `openreview_reviews.md`.
- [done] W7 Infrastructure: compute, memory/KV, data types, bandwidth-utilization limits, interconnect, runtime, and CPU/GPU heterogeneity analyzed in `analysis.md#5-magiattention-与-infrastructure`.
- [done] W8 Code/config: official architecture/runtime configs and chunk/token computation paths inspected and commit-pinned in `analysis.md#6-官方代码对照`.
- [done] W9 Gain attribution: Table 6 cumulative serving gains are separated from algorithmic quality claims; confounds are explicit.
- [done] W10 Report: complete Chinese `analysis.md` written with four original evidence visuals and limitations.
- [done] W10 Revision information: initial `1.0.0` / `rev-initial-20260721` history recorded in `analysis.md` and manifest.
- [skipped-with-reason] W11 Generated diagram: the available OpenRouter ICU CLI exposes only `generate/edit`; the required `responses-doc --input-file analysis.md` document-input path is unavailable, so no prompt-only substitute was used.
- [skipped-with-reason] D1 Delegated handoff: standalone invocation; no parent task packet or agent handoff applies.
- [done] D2 Deliverable manifest: `deliverable_manifest.json` finalized after checklist freeze and validated structurally and semantically.
- [skipped-with-reason] D3 Artifact manifest: standalone invocation; delegated artifact-manifest contract does not apply.

## Quality Checks

- [done] Q1 All local Markdown image links resolve.
- [done] Q2 Four accepted crops meet single-object/full-caption/bbox/readability/tight-boundary/contact-sheet/individual-QA requirements.
- [done] Q3 Key frame, resolution, token, latency, score, memory, and model-size numbers map to paper/code or labeled calculations.
- [done] Q4 Every core technical point has an explicit evidence classification; unsupported causal claims remain qualified.
- [done] Q5 Generated-diagram limitation is precise: required document-input CLI path is absent.
- [done] Q6 Code claims cite local paths and both official commit hashes.
- [done] Q7 Central term/symbol chapter covers formulas, windows, chunk/token counts, latency metrics, and ambiguities.
- [done] Q8 Chunk count, denoising window, KV range, packed tokens, per-video tokens, and per-rank tokens are stage-qualified.
- [skipped-with-reason] Q9 No public OpenReview material exists to cross-check.
- [done] Q10 Gain attribution uses incremental Table 6 evidence or is labeled inferred/confounded.
- [done] Q11 Runtime/config claims come from inspected JSON; checkpoint tensors are explicitly unverified.
- [done] Q12 Incomplete source archive and generated-diagram tooling limitation are recorded with non-material impact on core conclusions.
- [skipped-with-reason] Q13 Standalone invocation; delegated provenance/write-isolation contract does not apply.
- [done] Q14 Final manifest passes JSON Schema and semantic consistency checks.
- [done] Q15 Core designs have rationale source status, concrete problem, mechanism, trade-off, evidence type, and judgment.
- [done] Q16 Initial revision metadata matches `analysis.md` and manifest; no predecessor/migration exists.

## Final Classification

- [done] F1 `analysis.md`, `figure_inventory.md`, `deliverable_manifest.json`, and `figures/contact-sheet.png` exist and agree on four visuals.
- [done] F2 No checklist item remains pending.
- [done] F3 Final response will state source-archive/OpenReview/training-stack limitations without overstating completeness.
