# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: reused the exclusive packet folder and created the required process layout under the allowed root.
- [done] W1 Delegated input: `task_packet.yaml` SHA-256 `23b8b44214240a7a6b5156da50e93136b2065219f3b829dcaad2bf68f1034409`; skill tree `a338c821d6c79aff1aac224cc8713081d3b7462d46ea504771e5208dcdca96cd`; contract `4dc80bfb1d508898c25f3f3775a4d2ebc596c4944291cc0dded6f586fcc74c32`; packet unchanged.
- [done] W2 Primary sources: complete 16-page `paper.pdf`, `source/arxiv-source.tar`, extracted source tree, `evidence/arxiv-abs.html`, `evidence/project-page.html`, and venue audit in `source_verification.md`.
- [blocked] W2 Public reviews: the known OpenReview forum/PDF and both APIs were blocked by browser challenge/HTTP 403; indexed metadata and exact effect are preserved in `openreview_reviews.md`.
- [skipped-with-reason] W2 Code: neither paper nor official project page claims/links an implementation or checkpoint; `evidence/github-repository-search.json` contains three unrelated exact-search results, so no repository/commit exists to inspect.
- [done] W3 Text: `pdftotext` extraction retained at `extracted_text/arxiv-paper.txt` and `extracted_text/arxiv-paper-layout.txt`; LaTeX source is searchable at `source/example_paper.tex`.
- [done] W3 Visuals: accepted Figure 3 mechanism and Table 2 result/system crops under `figures/crops/`; each contains one numbered object and full caption.
- [done] W3 Inventory: `figure_inventory.md` records page dimensions and exact `(x,y,width,height)` for both counted visuals.
- [done] W3 Visual QA: `figures/contact-sheet.png` passed batch triage; both crops passed individual 100% inspection. An initially clipped Table 2 caption was rejected and recropped before acceptance.
- [done] W4 Evidence discipline: `analysis.md` maps all major claims to sections/equations/figures/tables and distinguishes paper-only implementation statements.
- [done] W4 Design rationale: `analysis.md#34-设计动机与具体问题映射` covers eight core designs with source status, problem, causal mechanism, alternatives, evidence, and judgment.
- [done] W4 Claim matrix: `analysis.md#43-技术-claim-证据矩阵` classifies direct, indirect, confounded, paper-only, and missing evidence.
- [done] W4 Terminology and symbols: centralized `analysis.md#01-术语与符号解释` covers paper-specific terms and all variables used in key formulas/infra derivations with provenance and ambiguity.
- [done] W5 Related work: `analysis.md#5-related-work-对比` compares bidirectional, native AR, causal distillation, long-video, and Diffusion Forcing groups.
- [blocked] W6 OpenReview cross-check: venue/front matter cross-check completed, but public reviews/decision/rebuttal/version history remain inaccessible; see `analysis.md#6-openreview-公开评审--论文内容交叉核验`.
- [done] W7 Infrastructure: `analysis.md#7-infra-需求分析` covers compute, cache/buffer memory formulas, dtype gaps, bandwidth/utilization, interconnect, runtime, and heterogeneity.
- [done] W8 Code/config: official project/page/repository checks are classified in `analysis.md#8-开源代码配置与权重对照`; implementation claims remain paper-only and code-unverified.
- [done] W9 Gain attribution: `analysis.md#45-收益归因` separates matched-ish, direct-ablation, indirect, confounded, and negative evidence.
- [done] W10 Report: complete `analysis.md` includes inline mechanism/result visuals and evidence-bound limitations.
- [done] W10 Revision information: history preserves `rev-initial`, advances to `1.0.0` / `rev-source-complete-20260724`, and binds previous manifest `075d43a87072c1b36cf647ac3a6ca1513c68dd44bdf23e86982108de8e32310d`.
- [skipped-with-reason] W11 Generated diagram: API key exists, but installed skill/CLI lacks the mandatory `responses-doc --input-file analysis.md` path; evidence in `extracted_text/generated-diagram-capability.txt`; no prompt-only substitute.
- [done] D1 Delegated handoff: contract-compliant `agent_handoff.md` written and frozen before final deliverable hashing.
- [done] D2 Deliverable manifest: `deliverable_manifest.json` passes Draft 2020-12 structural validation and all listed semantic checks with empty errors.
- [done] D3 Artifact manifest: preliminary coverage was checked; final `artifact_manifest.sha256` is regenerated and verified last, excluding only itself.
- [done] K1 Organization: resolved built-in publisher organization plus clone profile `huangwei-research-vault` and governing policies; hashes recorded in `source_verification.md`/handoff.
- [done] K2 Process/formal boundary: all sources/renders/crops/code-search/QA/review artifacts remain in this process root; two QA-passed promotion candidates are named in the handoff.
- [done] K3 Promotion responsibility: delegated parent owns canonical Paper/Asset promotion; no global/formal path was edited.
- [skipped-with-reason] K4 Publication validation: publication did not occur in this delegated run; publisher validation is explicitly parent-owned.

## Quality Checks

- [done] Q1 All two local Markdown image links resolve.
- [done] Q2 Both accepted crops include exactly one numbered object/full caption, complete inventory fields, tight readable boundaries, and passed contact-sheet plus individual 100% QA.
- [done] Q3 Every reported number is tied to Table 2/Table 3/Table 4/§5/Appendix or labeled as an arithmetic derivation.
- [done] Q4 The technical-claim matrix explicitly marks direct, indirect, confounded, paper-only, and missing evidence.
- [done] Q5 Generated-diagram limitation is precise and preserved in `extracted_text/generated-diagram-capability.txt`.
- [skipped-with-reason] Q6 No official code is claimed or available; consequently no code claim or commit citation is made.
- [done] Q7 The centralized term/symbol chapter covers flexible chunks, cache/alignment/editing terms and \(F,T,t,K_t,k,\mathbf a_t,\mathcal F,x,q_\theta,\mathcal S,G_\theta,\Pi,Q,K,V,d,B_{\mathrm{KV}}\).
- [done] Q8 Causal/non-causal attention, cache, chunking, editing, training, and serving/runtime meanings are stage-qualified.
- [blocked] Q9 OpenReview public reviews/decision/rebuttal/discussion could not be accessed despite forum/PDF/API attempts; no reviewer claim is used.
- [done] Q10 Gain attribution uses exact arithmetic and labels long-video/schedule attribution confounded or matched-ish where appropriate.
- [done] Q11 No Flex checkpoint/config is claimed; Wan2.1 names are paper-reported and unverified as Flex release metadata.
- [done] Q12 Initial sandbox network failure, OpenReview/ICML access blocks, absent code, and generated-diagram capability gap are recorded with effects.
- [done] Q13 Packet was preserved, handoff/manifest are schema-consistent, all writes stayed inside `allowed_write_root`, and no out-of-folder edit is suspected; parent owns external-state audit.
- [done] Q14 Final manifest structural/semantic validation passes with empty errors and agrees with frozen artifacts/statuses.
- [done] Q15 Eight rationale entries cover every core design without presenting reviewer inference as author intent.
- [done] Q16 Revision section/manifest/handoff preserve one initial bootstrap and one tracked update pointing to the exact predecessor hash; current identity is latest.
- [done] Q17 Process/formal separation is preserved; canonical ownership/link validation remains a named parent responsibility.

## Final Classification

- [done] F1 `analysis.md`, `figure_inventory.md`, `deliverable_manifest.json`, and `figures/contact-sheet.png` exist and agree on 1 mechanism + 1 result/system visual.
- [done] F2 Every workflow/quality item is classified; no `pending` remains.
- [done] F3 Handoff lists OpenReview/version-history, code, infra-metadata, and generated-diagram limitations without promoting blocked evidence to fact.
