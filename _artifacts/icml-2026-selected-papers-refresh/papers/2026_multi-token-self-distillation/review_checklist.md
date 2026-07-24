# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: create/reuse one paper folder and required artifact layout.
- [done] W1 Delegated input: verify `task_packet.yaml`, skill-tree hash, and agent-contract hash without modifying the packet, or mark standalone invocation with reason.
- [done] W2 Primary sources: acquire or classify the PDF, source archive, official paper page, and metadata.
- [done] W2 Public reviews: acquire and preserve OpenReview evidence, or record why it is unavailable/not applicable.
- [done] W2 Code: acquire the official/selected repository and record remote URL plus commit hash, or classify its absence.
- [done] W3 Text: extract searchable paper text and retain the extraction path/tool evidence.
- [done] W3 Visuals: extract readable crops containing exactly one numbered figure/table and its complete caption, with unrelated page content excluded and normally only an 8-32 pixel safety margin; reject unrelated whitespace over 5% per side unless intrinsic.
- [done] W3 Inventory: complete `figure_inventory.md` for every counted visual, including source-page dimensions and exact crop bounding box `(x, y, width, height)`.
- [done] W3 Visual QA: when crops exist, use `figures/contact-sheet.png` for triage and inspect every crop individually at 100% scale; fix/reject blank, duplicate, clipped, unreadable, captionless, neighboring-content, or excessive-margin crops. Otherwise record precise visual-block and alternative-evidence details without a blank placeholder.
- [done] W4 Evidence discipline: map important claims to sections, equations, figures, tables, appendices, or code.
- [done] W4 Design rationale: for every core design, separate author-stated/inferred/not-stated rationale, identify the concrete problem, explain the causal mechanism, and record alternatives/trade-offs plus validation evidence.
- [done] W4 Claim matrix: classify every claimed technical point as direct, indirect, confounded, missing, or otherwise precisely qualified evidence.
- [done] W4 Terminology and symbols: complete one centralized `analysis.md` chapter containing sourced term and symbol tables; cover paper-specific meanings, aliases, ambiguities, and author/code/analysis-derived symbol provenance, or mark symbols not applicable only when neither sources nor review derivations use them.
- [done] W5 Related work: compare the paper's relevant method groups by mechanism, benefit, limitation, and fairness.
- [skipped-with-reason] W6 OpenReview cross-check: no public forum located; test public review claims against paper/rebuttal/code evidence, or classify unavailability.
- [done] W7 Infrastructure: analyze relevant compute, memory, bandwidth/utilization, interconnect, runtime, data types, and CPU/GPU/NPU heterogeneity.
- [done] W8 Code/config: inspect relevant architecture, loss, data, evaluation, runtime, checkpoint, and serving paths, or classify unavailable evidence.
- [done] W9 Gain attribution: separate direct, indirect, confounded, and unsupported component-level attribution.
- [done] W10 Report: write complete `analysis.md` from `references/markdown-template.md` with inline evidence visuals and limitations.
- [done] W10 Revision information: add/update the centralized revision section; preserve prior history, increment version/revision ID for changed deliveries, and bind non-initial revisions to the previous manifest SHA-256.
- [skipped-with-reason] W11 Generated diagram: responses-doc --input-file capability unavailable; no substitute generated. use the required document-input path and verify/link the PNG, or record the exact unavailable/failed reason.
- [done] D1 Delegated handoff: after W11, write the preliminary contract-compliant `agent_handoff.md`, or mark standalone invocation with reason; freeze it before final deliverable hashing.
- [done] D2 Deliverable manifest: validate a preliminary `deliverable_manifest.json`, including revision history/current revision identity; finalize/freeze checklist and handoff, recompute hashes, then pass final structural and semantic validation with no errors.
- [done] D3 Artifact manifest: in delegated runs, preflight-generate/verify `artifact_manifest.sha256` before the freeze, then regenerate/verify it last after the final deliverable manifest; do not edit covered files afterward. Mark standalone invocation with reason.
- [done] K1 Organization: resolve `$research-knowledge-publisher` organization/profile/governance and canonical owner, or classify knowledge-base integration as not applicable.
- [done] K2 Process/formal boundary: keep PDF/source/render/crop/code/QA/review artifacts under the process root and identify only stable Paper/Asset promotion candidates.
- [done] K3 Promotion responsibility: standalone runs validate the post-freeze promotion plan; delegated runs record promotion recommendations without editing parent/global/formal paths.
- [skipped-with-reason] K4 Publication validation: delegated parent-owned; record publisher validation status/path after promotion, or classify parent-owned/not-applicable responsibility precisely.

## Quality Checks

- [done] Q1 All local Markdown image links resolve.
- [done] Q2 Every accepted crop contains exactly one numbered object and its full caption, records source-page dimensions/bounding box, has readable resolution and tight boundaries, and passes both contact-sheet triage and individual 100% QA; a no-crop run has precise visual-block evidence and no blank placeholder.
- [done] Q3 Every key number maps to paper evidence or a clearly labeled calculation.
- [done] Q4 Every claimed technical point has an evidence classification; unsupported claims are explicit.
- [skipped-with-reason] Q5 Generated-diagram handling used `responses-doc --input-file analysis.md` and produced a linked PNG, or has a precise limitation.
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
- [done] Q17 Knowledge integration, when applicable, preserves canonical Paper/Asset ownership, required inbound/backlinks, process-root isolation, and separate review/publication validation states.

## Final Classification

- [done] F1 `analysis.md`, `figure_inventory.md`, and `deliverable_manifest.json` exist and agree on counted visuals; `figures/contact-sheet.png` exists when crops exist, otherwise precise visual-block evidence exists.
- [done] F2 Every workflow and quality item above is `done`, `blocked`, or `skipped-with-reason`; none remains `pending`.
- [done] F3 The final response/handoff states every material limitation and does not declare blocked evidence complete.
