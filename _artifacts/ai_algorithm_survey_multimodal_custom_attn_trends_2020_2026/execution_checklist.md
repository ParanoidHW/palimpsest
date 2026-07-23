# Multimodal Sparse Attention Trend Survey Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`.

## Workflow

- [done] W1 Scope: 2020-2026; strict multimodal tasks; CVPR/ICCV/ECCV/NeurIPS/ICML/ICLR plus AAAI/ACM MM; main/official Findings separated from arXiv-only and technical reports.
- [done] W1 Counting: paper-level full counting for affiliations; each organization counts at most once per paper; 2026 is year-to-date through 2026-07-23.
- [done] W2 Search: general web, official proceedings, arXiv/OpenAlex, GitHub/awesome discovery, exact query/date logging.
- [done] W3 Candidate database: normalize, deduplicate, classify modality/method family, and record inclusion/exclusion reasons.
- [done] W3 Venue status: verify counted formal records against official proceedings or conference pages; unresolved exact pages are marked as audit limitations.
- [blocked] W3 Affiliations: direct first-page affiliation verification completed for 6/38 formal papers; remaining records stay unknown.
- [skipped-with-reason] W4 Impact signals: no popularity ranking requested; recent-paper citation signals are unstable.
- [skipped-with-reason] W5 New paper selection/deep review: user explicitly requested trend census without new paper-deep-review; existing formal paper notes are used only as mechanism anchors.
- [skipped-with-reason] W6 Agent isolation/dispatch: no new per-paper reviews by user request; use `reduced-user-accepted` in the manifest.
- [done] W7 Synthesis: write `synthesis.md` with revision information, timeline, venue counts, taxonomy, organization distribution, infra trend, evidence caveats, and centralized terms/symbols.
- [skipped-with-reason] W8 Generated survey diagram: no compatible `responses-doc --input-file` path; statistical charts are sufficient for this trend update.
- [done] W9 Formal promotion: update the canonical survey, add a formal evidence page and derived charts, then update README/figure inventory links.
- [done] W10 Manifest: create and structurally validate `deliverable_manifest.json`; classify semantic limitations caused by intentionally skipped per-paper deep reviews.

## Quality Checks

- [done] Q1 Conference and arXiv versions deduplicate to one canonical paper record.
- [done] Q2 Workshops, withdrawn submissions, under-review papers, arXiv-only papers, and technical reports do not enter formal top-conference counts.
- [done] Q3 Included papers have attention visibility, selection, mask/kernel lowering, or distributed attention as a core contribution.
- [done] Q4 Token pooling, generic compression, MoE, and ordinary factorized attention are excluded from the main count unless attention sparsity is core.
- [done] Q5 Venue-year subtotals reconcile with the formal-paper total.
- [blocked] Q6 Organization counts follow paper-level full counting, but affiliation verification is incomplete.
- [done] Q7 Derived Markdown charts are reproducible from CSV/JSONL artifacts.
- [done] Q8 Volatile scope is dated 2026-07-23 and 2026 is explicitly YTD.
- [done] Q9 Formal Markdown links/anchors resolve; formal assets exist; no formal `_artifacts` or absolute-path references.
- [done] Q10 Reduced deep-review scope and 2026 partial-year bias are explicit.

## Final Classification

- [done] F1 Required survey-level artifacts exist and agree on counts.
- [done] F2 No checklist item remains pending.
- [done] F3 Final response distinguishes audited corpus counts from claims of exhaustive field coverage.
