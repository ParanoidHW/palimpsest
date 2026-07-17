# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: owned folder and required layout created under `_artifacts/icml_2026/reviews/echo`.
- [done] W1 Delegated input: packet `e70b...16c`, skill tree `93e4...6e`, contract `33da...e21` verified; packet preserved.
- [done] W2 Primary sources: exact arXiv v2 PDF/source and `arxiv_api.xml`/`arxiv_abs.html` acquired.
- [done] W2 Public reviews: submission metadata preserved in `openreview_search.json`; forum detail HTTP 403 recorded in `openreview_reviews.md`.
- [done] W2 Code: `source/main.tex` states code will be released later; no repository URL exists, classified unavailable.
- [done] W3 Text: Poppler output at `extracted_text/paper.txt`.
- [done] W3 Visuals: Figure 3 and Figure 5 crops contain one object plus full caption with tight boundaries.
- [done] W3 Inventory: complete rows in `figure_inventory.md`.
- [done] W3 Visual QA: contact-sheet triage and both original-resolution individual inspections passed 2026-07-17.
- [done] W4 Evidence discipline: `analysis.md` maps claims and numbers to exact evidence.
- [done] W4 Design rationale: complete matrix in `analysis.md` Sec. 3.2.
- [done] W4 Claim matrix: complete matrix in Sec. 4.
- [done] W4 Terminology and symbols: centralized Sec. 0.1 covers terms and all equation/infra symbols.
- [done] W5 Related work: comparison and fairness caveat in Sec. 5.
- [done] W6 OpenReview cross-check: forum detail HTTP 403 precisely classified; no reviewer claim used.
- [done] W7 Infrastructure: Sec. 7 covers compute, memory, dtype, effective bandwidth, MoE interconnect and CPU/GPU/NPU gaps.
- [done] W8 Code/config: Appendix configuration inspected; implementation unavailable and claims bounded in Sec. 8.
- [done] W9 Gain attribution: Sec. 4.1 separates matched ablations from confounded full-system gains.
- [done] W10 Report: complete Chinese `analysis.md` with two evidence visuals.
- [done] W10 Revision information: initial revision `rev-echo-initial`, version `1.0.0`.
- [skipped-with-reason] W11 Generated diagram: installed OpenRouter ICU CLI exposes only `generate` and `edit`, not mandatory `responses-doc --input-file analysis.md`; prompt-only art prohibited by contract.
- [done] D1 Delegated handoff: `agent_handoff.md` written and frozen before final hashing.
- [done] D2 Deliverable manifest: two-pass freeze performed; Draft 2020-12 and semantic validation passed with empty errors.
- [done] D3 Artifact manifest: preliminary preflight completed; final `artifact_manifest.sha256` regenerated and verified last.

## Quality Checks

- [done] Q1 All local Markdown image links resolve.
- [done] Q2 Every accepted crop contains exactly one numbered object and its full caption, records source-page dimensions/bounding box, has readable resolution and tight boundaries, and passes both contact-sheet triage and individual 100% QA; a no-crop run has precise visual-block evidence and no blank placeholder.
- [done] Q3 Every key number maps to paper evidence or a clearly labeled calculation.
- [done] Q4 Every claimed technical point has an evidence classification; unsupported claims are explicit.
- [skipped-with-reason] Q5 Generated diagram: CLI lacks `responses-doc --input-file`; exact capability limitation is recorded in `analysis.md` and manifest.
- [done] Q6 Every code claim cites a local path and commit hash when code is available.
- [done] Q7 The centralized terminology-and-symbol chapter covers every key paper-specific term and every applicable variable used in key formulas, metrics, and tables; each entry has a source and ambiguity note.
- [done] Q8 Ambiguous mechanism terms are qualified by stage and paper/code meaning.
- [done] Q9 OpenReview reviews, decision, rebuttal, and discussion were evidence-cross-checked when publicly accessible.
- [done] Q10 Gain-attribution statements use matched evidence or are explicitly labeled rough/inferred.
- [done] Q11 Checkpoint/config claims come from inspected metadata or are marked unverified.
- [done] Q12 Failed tests, extraction tools, downloads, access, and metadata checks are recorded with their effect on conclusions.
- [done] Q13 Delegated runs preserved the task packet, produced a schema-compliant handoff and complete artifact manifest, and passed the parent-provided write-isolation mode or reported suspected out-of-folder edits; standalone runs classify this item with reason.
- [done] Q14 `deliverable_manifest.json` passes structural and semantic validation and agrees with the centralized terminology/symbol chapter, key-term/symbol coverage, artifact hashes, visual counts/missing types, evidence status, invocation mode/provenance, frozen checklist/handoff, and limitations.
- [done] Q15 Every core design has a rationale entry with source status, concrete target problem, causal mechanism, trade-off, and evidence judgment; inference is never presented as author-stated intent.
- [done] Q16 Revision metadata matches `analysis.md` and the manifest; history has one valid initial/migration bootstrap, is ordered and append-only, keeps unresolved issue IDs blocked until exactly one later migration-resolution, makes every later tracked entry point to the exact superseded revision/manifest hash, and identifies the latest frozen state.

## Final Classification

- [done] F1 `analysis.md`, `figure_inventory.md`, and `deliverable_manifest.json` exist and agree on counted visuals; `figures/contact-sheet.png` exists when crops exist, otherwise precise visual-block evidence exists.
- [done] F2 Every workflow and quality item above is `done`, `blocked`, or `skipped-with-reason`; none remains `pending`.
- [done] F3 The final response/handoff states every material limitation and does not declare blocked evidence complete.
