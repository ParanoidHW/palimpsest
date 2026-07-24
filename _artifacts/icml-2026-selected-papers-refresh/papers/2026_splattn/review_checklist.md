# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Preserve every item.

## Workflow

- [done] W1 Folder: reused the packet-owned paper folder and required artifact layout.
- [done] W1 Delegated input: verified `task_packet.yaml` SHA-256 `c360805cfc20ff1495f77a865f6cc13aaf75ba662ff590395a845e27d8865779`, skill-tree hash `a338c821d6c79aff1aac224cc8713081d3b7462d46ea504771e5208dcdca96cd`, contract hash `4dc80bfb1d508898c25f3f3775a4d2ebc596c4944291cc0dded6f586fcc74c32`, and previous manifest hash `1006a623b3473b4129ba2f3fd8ecb08fd7c299846678d0636e1b1438fef2650c`; packet unchanged.
- [done] W2 Primary sources: acquire or classify PDF, source archive, official venue page, and metadata.
- [done] W2 Public reviews: acquire/preserve OpenReview evidence or classify.
- [done] W2 Code: acquire official repository and record commit hash.
- [done] W3 Text: extract searchable paper text and retain tool evidence.
- [done] W3 Visuals: extract readable exact-one-object crops with complete caption and tight margins.
- [done] W3 Inventory: complete `figure_inventory.md` with page dimensions and crop boxes.
- [done] W3 Visual QA: contact-sheet triage plus individual 100% inspection.
- [done] W4 Evidence discipline: map important claims to source/code evidence.
- [done] W4 Design rationale: complete all core-design rationale dimensions.
- [done] W4 Claim matrix: classify technical-point evidence.
- [done] W4 Terminology and symbols: centralized sourced chapter.
- [done] W5 Related work: mechanism/benefit/limitation/fairness comparison.
- [skipped-with-reason] W6 OpenReview cross-check: no public record found after checking packet, official ICML page, and exact-title searches; attempts in `openreview_reviews.md`.
- [done] W7 Infrastructure: compute/memory/bandwidth/interconnect/runtime/data types/heterogeneity.
- [done] W8 Code/config: architecture/loss/data/eval/runtime/checkpoint/serving inspection.
- [done] W9 Gain attribution: direct/indirect/confounded/unsupported separation.
- [done] W10 Report: complete `analysis.md` with inline evidence visuals and limitations.
- [done] W10 Revision information: preserve history, increment version/ID, bind prior manifest.
- [skipped-with-reason] W11 Generated diagram: ICU CLI has no required `responses-doc --input-file analysis.md` command; recorded in `analysis.md` §0 and handoff.
- [done] D1 Delegated handoff: contract-compliant frozen handoff.
- [done] D2 Deliverable manifest: preliminary then final schema/semantic validation.
- [done] D3 Artifact manifest: preflight then final generation last.
- [done] K1 Organization: resolve publisher profile/governance/canonical owner.
- [done] K2 Process/formal boundary: retain all work under process root and identify candidates only.
- [done] K3 Promotion responsibility: recommendations only; no parent/global/formal edits.
- [skipped-with-reason] K4 Publication validation: delegated parent-owned after promotion; no formal/global edits were authorized.

## Quality Checks

- [done] Q1 All local Markdown image links resolve.
- [done] Q2 Every accepted crop passes exact-object, full-caption, dimensions/bbox, readability, tight-boundary, contact-sheet, and 100% QA.
- [done] Q3 Every key number maps to paper evidence or labeled calculation.
- [done] Q4 Every technical point has an evidence classification.
- [done] Q5 Generated-diagram handling uses `responses-doc --input-file analysis.md` or precise limitation.
- [done] Q6 Every code claim cites a local path and pinned commit.
- [done] Q7 Central terminology/symbol chapter covers key terms/variables, sources, ambiguity.
- [done] Q8 Ambiguous mechanism terms are stage-qualified.
- [skipped-with-reason] Q9 Public review/decision/rebuttal/discussion evidence is not publicly accessible from identified sources; `openreview_reviews.md`.
- [done] Q10 Gain attribution uses matched evidence or is labeled inferred.
- [done] Q11 Checkpoint/config claims derive from inspected metadata or are unverified.
- [done] Q12 Failed tools/downloads/access/metadata checks and effects are recorded.
- [done] Q13 Packet preserved; delegated handoff, artifact manifest, and isolation classification complete.
- [done] Q14 Final manifest structural/semantic consistency and hashes pass.
- [done] Q15 Every core design has complete rationale dimensions with inference labeled.
- [done] Q16 Revision metadata/history is append-only and binds exact prior manifest.
- [done] Q17 Knowledge integration preserves ownership and process/formal separation.

## Final Classification

- [done] F1 Required report/inventory/manifest agree on visuals and contact sheet.
- [done] F2 No item remains pending/unclassified.
- [done] F3 Handoff states all material limitations without overstating blocked evidence.

## Evidence Index

- Acquisition/text: `paper.pdf` is a readable 24-page arXiv v2 PDF; `source.tar.gz` extracts through `source/example_paper.tex`; Poppler outputs are in `extracted_text/`; official venue evidence is `venue/icml-poster-60900.html`.
- Code/checkpoints: official repo commit `0c279dd11ca13a70b676cd60ca9673e093526b9a`; architecture/renderer/loss/eval paths are cited in `analysis.md` §8; pinned HF records are in `checkpoint_metadata/`.
- Visuals: `figure_inventory.md` records page dimensions, final bboxes, complete captions, and QA; `figures/contact-sheet.png` covers both counted crops; both crop files were inspected individually at original resolution.
- Evidence discipline: centralized terminology/symbol tables are `analysis.md` §0.1; rationale matrix §3.2; evidence loop §3.1; claim matrix §4.2; gain attribution §4.3; infra §7.
- Revision/provenance: `analysis.md` revision table and `agent_handoff.md` preserve the 1.0.0 entry and append 1.1.0 bound to prior manifest `1006a623…`; delegated hashes match the packet.
- Knowledge organization: repository profile and policy were resolved read-only; promotion candidates appear only in `agent_handoff.md`; parent owns canonical search/promotion/validation.
