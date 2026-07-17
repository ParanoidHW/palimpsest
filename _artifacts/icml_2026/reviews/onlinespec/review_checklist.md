# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: reused `_artifacts/icml_2026/reviews/onlinespec`; ownership is restricted to this one-paper folder.
- [done] W1 Delegated input: task packet, complete skill tree, and contract hashes match expected values: `8f07ab...`, `93e435...`, `33da33...`; packet unchanged.
- [done] W2 Primary sources: `paper.pdf`, arXiv metadata/HTML and `source/source.tar` acquired for exact arXiv:2603.12617v1; source identifies ICLR 2026 workshop, not verified ICML acceptance.
- [skipped-with-reason] W2 Public reviews: primary arXiv/source metadata exposes no OpenReview forum, review, decision, meta-review or rebuttal.
- [done] W2 Code: official paper repository cloned at `code/OnlineSPEC`, remote `https://github.com/ZinYY/OnlineSPEC`, commit `3a6cc69d1c839385fcdd5f82529c55300e503b4b`.
- [done] W3 Text: PyMuPDF extraction under `extracted_text/`; independent `pdftotext -layout` output at `extracted_text/pdftotext.txt`.
- [done] W3 Visuals: accepted Figure 1/2/3 and Table 1/2 crops under `figures/crops/`; each includes exactly one numbered object and full caption.
- [done] W3 Inventory: `figure_inventory.md` records 1700x2200 pages, exact `(x,y,width,height)` boxes, captions, claims, paths and QA.
- [done] W3 Visual QA: `figures/contact-sheet.png` triage passed and all five crops individually inspected at original resolution; Table 1 was recropped to restore all rows.
- [done] W4 Evidence discipline: `analysis.md` maps claims to sections, equations, figures, tables, appendix and code.
- [done] W4 Design rationale: complete rationale matrix in `analysis.md#32-关键公式与设计动机`.
- [done] W4 Claim matrix: complete matrix in `analysis.md#42-技术点证据矩阵`.
- [done] W4 Terminology and symbols: centralized sourced tables in `analysis.md#01-术语与符号解释`.
- [done] W5 Related work: mechanism/benefit/limitation/fairness comparison in `analysis.md#5-相关工作比较`.
- [skipped-with-reason] W6 OpenReview cross-check: no public OpenReview records linked or discoverable from primary metadata; limitation recorded without treating venue status as accepted.
- [done] W7 Infrastructure: compute, memory, dtype uncertainty, bandwidth/utilization formulas, CPU/GPU/NPU heterogeneity and serving discussed in `analysis.md#7-infra-需求分析`.
- [done] W8 Code/config: Hydra/EAGLE/LR training and pipeline paths inspected at commit `3a6cc69...`; checkpoints/hardware metadata explicitly unverified.
- [done] W9 Gain attribution: direct/indirect/confounded evidence and bridge-baseline caveats in `analysis.md#43-收益归因`.
- [done] W10 Report: complete Chinese `analysis.md` with five inline paper-evidence visuals and limitations.
- [done] W10 Revision information: initial revision `rev-onlinespec-initial`, version `1.0.0`, centralized near top and mirrored in manifest.
- [skipped-with-reason] W11 Generated diagram: contract states installed ICU CLI lacks mandatory `responses-doc --input-file analysis.md`; prompt-only generation is forbidden.
- [done] D1 Delegated handoff: `agent_handoff.md` contains provenance, claims, promotion candidates and limitations.
- [done] D2 Deliverable manifest: `deliverable_manifest.json` passed Draft 2020-12 and all semantic checks with empty errors after frozen artifact hashes were computed.
- [done] D3 Artifact manifest: final `artifact_manifest.sha256` generated last and verified; no covered file edited afterward.

## Quality Checks

- [done] Q1 All five local Markdown image links resolve.
- [done] Q2 All accepted crops meet one-object/full-caption/dimensions/bbox/readability/tight-boundary/contact-sheet/individual-QA requirements.
- [done] Q3 Key numbers are tied to Table 1/2/4, Figure 3 or labeled formulas.
- [done] Q4 Every central technical point has an evidence classification; 24% and component attribution are qualified.
- [skipped-with-reason] Q5 Mandatory responses-doc path is unavailable in installed ICU CLI; no prompt-only art generated.
- [done] Q6 Code claims cite local paths and commit `3a6cc69d1c839385fcdd5f82529c55300e503b4b`.
- [done] Q7 Centralized term/symbol tables cover key equations, metrics, units, provenance and ambiguities.
- [done] Q8 Drafting, verification, feedback/update and serving/runtime stages are explicitly separated.
- [skipped-with-reason] Q9 No public OpenReview evidence exists in primary metadata, so no review claim can be cross-checked.
- [done] Q10 Gain attribution uses matched/bridge distinctions and labels rough inference.
- [done] Q11 Checkpoint/model capacity metadata not locally inspected is marked unverified.
- [done] Q12 Initial arxiv.org PDF DNS failure, successful export.arxiv.org recovery, unavailable OpenReview, absent responses-doc, and no GPU reproduction are classified with conclusion effects.
- [done] Q13 Task packet preserved; handoff/schema/artifact manifest produced; no suspected out-of-folder writes reported, without self-certifying read isolation.
- [done] Q14 Structural and semantic validation passed; manifest agrees with artifact hashes, 5 visual counts, provenance, terminology, design rationales, checklist and limitations.
- [done] Q15 Every core design has why status, source, target problem, causal mechanism, trade-off and evidence judgment.
- [done] Q16 Initial revision metadata matches analysis and manifest; no predecessor or unresolved migration exists.

## Final Classification

- [done] F1 Required artifacts exist and agree on five counted visuals; contact sheet exists.
- [done] F2 No workflow or quality item remains pending.
- [done] F3 Handoff and final classification state venue, OpenReview, generated-diagram, checkpoint, hardware and reproduction limitations.
