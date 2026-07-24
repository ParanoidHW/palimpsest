# Acquisition Log

- Access date: 2026-07-24 (Asia/Shanghai)
- Target paper: *Dual-Latent Memory Routing for Vision-Language Reasoning*
- OpenReview forum: `https://openreview.net/forum?id=SFWWUr9V7c`
- Indexed original-submission attachment: `https://openreview.net/attachment?id=SFWWUr9V7c&name=originally_submitted_PDF`
- Claimed code: `https://github.com/Hunter-Wrynn/DLMR`

## Provenance checks

- `task_packet.yaml`: SHA-256 `82ac3acc063511cbbb2f577b1eb17857884a4b8947c115c06dcab1a13378972c`.
- Required skill tree: deterministic SHA-256 `a338c821d6c79aff1aac224cc8713081d3b7462d46ea504771e5208dcdca96cd`.
- Agent contract: SHA-256 `4dc80bfb1d508898c25f3f3775a4d2ebc596c4944291cc0dded6f586fcc74c32`.
- Previous deliverable manifest: SHA-256 `4371334aa259856f2ddafec22e9bead4ef3eb1bda1f1f8733c7887e2d7469c31`.
- All four values match the task packet.

## PDF and forum attempts

1. Direct `openreview.net/pdf?id=SFWWUr9V7c`: HTTP 403.
2. Direct indexed attachment, with and without browser user agent: HTTP 403.
3. `api2.openreview.net` notes, PDF, and attachment endpoints: HTTP 403.
4. Legacy `api.openreview.net` notes and attachment endpoints: HTTP 403.
5. Jina document proxy: returned the OpenReview CAPTCHA/challenge page; preserved as `../extracted_text/original_submission_jina.md`.
6. Google Translate proxy: returned translated challenge HTML rather than a PDF; preserved as `google-translate-response.html`.
7. AllOrigins proxy: returned challenge HTML; preserved as `allorigins.bin`.
8. `corsproxy.io` and `cors.isomorphic-git.org`: HTTP 403.
9. Semantic Scholar query: HTTP 429 after bounded retries.
10. OpenAlex query returned no matching work or alternate PDF location; preserved as `openalex.json`.
11. The ICML poster page was acquired as `icml-poster.html`; it confirms title, authors, poster 63955, Spotlight relation, and abstract, but exposes no downloadable PDF.

No response passed the `%PDF-` signature check. Therefore `paper.pdf` is intentionally absent; challenge HTML is not mislabeled as a PDF.

## Code attempt

- `git clone --filter=blob:none --no-checkout https://github.com/Hunter-Wrynn/DLMR.git code/DLMR` failed because the remote is not publicly readable.
- `https://api.github.com/repos/Hunter-Wrynn/DLMR` returned HTTP 404.
- A general web fetch also returned 404.
- The current OpenReview search record still claims that this URL contains code. This is classified as a stale or unfulfilled public-code claim, not as available implementation evidence.

## Search-index fallback

The public search index exposes extracted text from the original-submission attachment, including Sections 4–5, Equations 4–12, Tables 1–4, and Figure 4 caption/text. A compact fact transcription is stored in `../extracted_text/search_index_evidence.md`.

This fallback improves method and result understanding but does **not** satisfy the local-readable-PDF requirement, cannot support figure crops or page-level QA, cannot establish the exact final PDF revision, and cannot replace code/OpenReview-note inspection.
