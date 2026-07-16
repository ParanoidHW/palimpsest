# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: reused `_artifacts/icml_2026/reviews/dual-latent-memory-routing`; artifact layout will remain inside this ownership boundary.
- [done] W1 Delegated input: verified `task_packet.yaml` SHA-256 `b04ac648321bf1209d43be2a7a5ef731686e4c1f997a888c250cbefe8ba4dc05`, deterministic complete skill-tree SHA-256 `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`, and agent-contract SHA-256 `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e`; packet unchanged.
- [blocked] W2 Primary sources: exact identity confirmed at ICML poster `63955`, but PDF/source remained unavailable after the attempts in `recovery/recovery_log.md`; no similarly named work substituted.
- [blocked] W2 Public reviews: official page exposes no forum; OpenReview v1/v2 exact-title APIs returned challenge HTTP 403; recorded in `openreview_reviews.md`.
- [blocked] W2 Code: official page has no code/project link and exact GitHub repository searches returned zero; recorded in `recovery/recovery_log.md`.
- [blocked] W3 Text: no paper PDF/source exists to extract; only the official abstract is retained in `recovery/icml-poster-63955.html` and qualified in `analysis.md`.
- [blocked] W3 Visuals: no PDF/source or numbered figure/table with caption was available; no crop was fabricated.
- [done] W3 Inventory: `figure_inventory.md` records zero counted visuals, both missing types, exact blocker, and alternative abstract evidence.
- [skipped-with-reason] W3 Visual QA: zero crops because exact PDF/source is unavailable; no blank contact sheet was created, so contact-sheet and individual-crop QA are not applicable.
- [done] W4 Evidence discipline: every retained claim in `analysis.md` is mapped to the official ICML abstract or explicitly marked unverified; inaccessible evidence types are named.
- [done] W4 Design rationale: `analysis.md#32-设计动机矩阵` covers every design identifiable from the abstract and marks all validation unverified; full-paper coverage is blocked.
- [done] W4 Claim matrix: `analysis.md#4-技术声明证据矩阵与收益归因` classifies all abstract claims as unsupported by available experiments.
- [done] W4 Terminology and symbols: centralized `analysis.md#01-术语与符号解释` defines five abstract terms; symbols are not applicable because neither available source nor review uses formulas.
- [blocked] W5 Related work: paper references/related-work section unavailable; `analysis.md#5-related-work-对比` declines speculative comparison.
- [blocked] W6 OpenReview cross-check: public review evidence inaccessible; exact failure and effect are in `openreview_reviews.md` and `analysis.md#6-openreview-公开评审--论文内容交叉核验`.
- [blocked] W7 Infrastructure: abstract lacks dimensions, hardware, runtime, data types, and traffic; `analysis.md#7-infra-需求分析` enumerates the non-estimable fields without inventing values.
- [blocked] W8 Code/config: no official code, checkpoint, or metadata located; `analysis.md#8-开源代码与配置对照` records the boundary.
- [blocked] W9 Gain attribution: no matched ablation or numeric results; `analysis.md#4-技术声明证据矩阵与收益归因` explicitly rejects component attribution.
- [done] W10 Report: `analysis.md` is a concise Chinese abstract-level blocked report following the reusable section structure and preserving all material limitations.
- [done] W10 Revision information: `analysis.md#修订信息` records the initial `1.0.0` / `rev-initial-20260716` entry with no predecessor.
- [skipped-with-reason] W11 Generated diagram: parent contract states the installed CLI has only `generate`/`edit`, not mandatory `responses-doc --input-file analysis.md`; prompt-only art is forbidden.
- [pending] D1 Delegated handoff: after W11, write the preliminary contract-compliant `agent_handoff.md`, or mark standalone invocation with reason; freeze it before final deliverable hashing.
- [pending] D2 Deliverable manifest: validate a preliminary `deliverable_manifest.json`, including revision history/current revision identity; finalize/freeze checklist and handoff, recompute hashes, then pass final structural and semantic validation with no errors.
- [pending] D3 Artifact manifest: in delegated runs, preflight-generate/verify `artifact_manifest.sha256` before the freeze, then regenerate/verify it last after the final deliverable manifest; do not edit covered files afterward. Mark standalone invocation with reason.

## Quality Checks

- [done] Q1 All local Markdown image links resolve: `analysis.md` contains no image links because no evidence crop/diagram exists.
- [skipped-with-reason] Q2 No crop exists; `figure_inventory.md` records the precise PDF/source blocker and alternative official-abstract evidence, and no blank contact sheet exists.
- [done] Q3 Every retained date, ID, author name, and zero-result/access code maps to the official snapshot or recovery log; no performance number or derived calculation is asserted.
- [done] Q4 Every abstract technical claim is classified `unverified` in the claim matrix.
- [skipped-with-reason] Q5 Mandatory `responses-doc --input-file analysis.md` capability is absent per parent contract; no prompt-only image generated.
- [skipped-with-reason] Q6 No code claim or code repository exists; implementation behavior is explicitly unverified.
- [done] Q7 Centralized terminology covers all terms used for abstract-level mechanism discussion with source and ambiguity notes; symbols are correctly not applicable.
- [done] Q8 Memory/router terms are qualified as abstract-level inference-stage claims; implementation-level behavior is explicitly unknown.
- [blocked] Q9 OpenReview reviews, decision, rebuttal, and discussion could not be accessed because official page has no link and APIs returned challenge 403.
- [done] Q10 No gain attribution is made; absent matched evidence is explicit.
- [skipped-with-reason] Q11 No checkpoint/config is linked or found; all configuration claims are marked unverified.
- [done] Q12 Failed/empty acquisition and access checks, including Semantic Scholar 429 and OpenReview 403, are recorded with effects in `recovery/recovery_log.md`.
- [pending] Q13 Delegated runs preserved the task packet, produced a schema-compliant handoff and complete artifact manifest, and passed the parent-provided write-isolation mode or reported suspected out-of-folder edits; standalone runs classify this item with reason.
- [pending] Q14 `deliverable_manifest.json` passes structural and semantic validation and agrees with the centralized terminology/symbol chapter, key-term/symbol coverage, artifact hashes, visual counts/missing types, evidence status, invocation mode/provenance, frozen checklist/handoff, and limitations.
- [done] Q15 Every design identifiable from the abstract has a complete rationale row with author-stated source, target problem, stated mechanism, reviewer-supplied alternatives, and `unverified` evidence judgment; unknown full-paper designs are disclosed.
- [pending] Q16 Revision metadata matches `analysis.md` and the manifest; history has one valid initial/migration bootstrap, is ordered and append-only, keeps unresolved issue IDs blocked until exactly one later migration-resolution, makes every later tracked entry point to the exact superseded revision/manifest hash, and identifies the latest frozen state.

## Final Classification

- [pending] F1 `analysis.md`, `figure_inventory.md`, and `deliverable_manifest.json` exist and agree on counted visuals; `figures/contact-sheet.png` exists when crops exist, otherwise precise visual-block evidence exists.
- [pending] F2 Every workflow and quality item above is `done`, `blocked`, or `skipped-with-reason`; none remains `pending`.
- [pending] F3 The final response/handoff states every material limitation and does not declare blocked evidence complete.
