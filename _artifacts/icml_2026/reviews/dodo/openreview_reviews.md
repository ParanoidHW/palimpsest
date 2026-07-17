# OpenReview and Venue Check: DODO

Access date: 2026-07-17 (Asia/Shanghai).

## Venue status

- arXiv metadata (`arxiv_metadata.xml`, `logs/arxiv_abs.html`) identifies only arXiv:2602.16872v2, submitted 2026-02-18 and revised 2026-05-27; it does not claim ICML main-conference acceptance.
- The official ICML 2026 search capture (`logs/icml_virtual_search.html`) returns the exact title and authors as one result of type **Workshop**, linking `/virtual/2026/workshop/54089`.
- The linked official event capture (`logs/icml_workshop_54089.html`) is the ICML 2026 workshop “4th Structured Probabilistic Inference & Generative Modeling,” scheduled 2026-07-09. Therefore the independently verified venue label is **ICML 2026 workshop presentation**, not ICML 2026 Main Conference paper.

## Public review availability

- Exact-title calls to both OpenReview API hosts returned HTTP 403; the public search page capture (`logs/openreview_search.html`) remained a client-side loading shell and exposed no paper forum ID.
- The ICML workshop event links OpenReview forum `FtTsaDTlnQ`, but that is the workshop-level forum, not a DODO submission/review forum.
- The workshop project schedule capture (`logs/spigm_schedule.html`) did not expose a DODO paper forum or public reviewer notes.

Conclusion: no publicly accessible paper-level reviews, scores, meta-review, decision note, rebuttal, or discussion could be identified. OpenReview opinion cross-check is therefore `skipped-with-reason`; this limits assessment of reviewer-raised novelty/reproducibility concerns but does not affect paper-derived method and ablation readings.

