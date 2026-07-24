# Search Log

- Search date: 2026-07-24
- Scope: incremental refresh of the existing 12-paper ICML 2026 user list; priority is recovering previously missing PDF/source/code and correcting venue status.
- Survey mode: hybrid. Peer-reviewed papers, workshops/preprints, repositories/checkpoints, and implementation-adoption records remain separate.

## Aliases

- Venue: `ICML 2026`, `PMLR 306`, `43rd International Conference on Machine Learning`, `icml.cc/Downloads/2026`.
- Missing-source papers: `SplAttN`, `Dual-Latent Memory Routing`, `DLMR`, `Flex-Forcing`, `OmniFit`, `Layer-Adaptive Heterogeneity Profiling`, `LAHP`, `Alignment-Rectified Token Selection`, `ARTS`.
- Source terms: `arXiv PDF`, `export.arxiv.org/e-print`, `OpenReview originally_submitted_PDF`, `ICML poster`, `project page`, `GitHub`, `checkpoint`, `Hugging Face`.
- Mechanism terms: `Gaussian Soft Splatting`, `dual latent memory`, `dynamic router`, `flexible chunking`, `video diffusion`, `layer-adaptive token compression`, `omnimodal LLM`.

## General web search

| Exact query | Source | Outcome |
|---|---|---|
| `"Dual-Latent Memory Routing for Vision-Language Reasoning"` | web search | Resolved OpenReview forum `SFWWUr9V7c`, ICML Spotlight metadata, original-submission attachment, and claimed code URL. |
| `"OmniFit: Bridging Modalities via Layer-Adaptive Token Compression"` | web search | Resolved ICML/OpenReview identity `8RY20mLzup`; rejected the unrelated arXiv:2604.21575 body-fitting paper. |
| `"Flex-Forcing" "2607.03509"` | web search | Resolved arXiv paper, ICML final text, OpenReview original submission `COGc3MSR7n`, and Spotlight status. |
| `"SplAttN" "2605.01466"` | web search | Resolved arXiv, official repo/checkpoints, Southwest Jiaotong affiliation, and ICML Spotlight evidence. |
| `"Dual-Latent Memory Routing" arxiv` | web search | No arXiv version found; OpenReview remains the primary paper source. |
| `"OmniFit" "Zining Wang" pdf` | web search | Resolved author pages and ICML identity; exact paper is not the same as 3D body fitting OmniFit. |

## arXiv/source lane

| Paper | Query/URL | Outcome |
|---|---|---|
| SplAttN | `https://arxiv.org/pdf/2605.01466`, `https://export.arxiv.org/e-print/2605.01466` | Independent-clone agent acquired a complete 24-page PDF and complete source archive. |
| Flex-Forcing | `https://arxiv.org/pdf/2607.03509`, `https://export.arxiv.org/e-print/2607.03509` | Refresh agent dispatched; prior 1.8 MiB partial is not reused as evidence. |
| LiME | `https://export.arxiv.org/e-print/2604.02338` | Prior source was partial; source-only refresh remains pending after higher-priority blocked papers. |
| MTP Self-Distillation | `https://export.arxiv.org/e-print/2602.06019` | Prior source was partial; GitHub repository now resolves via API. |
| DODO | `https://export.arxiv.org/e-print/2602.16872` | Prior source was partial; official implementation still not identified. |

## Venue/proceedings lane

| Source | Exact lookup | Outcome |
|---|---|---|
| ICML Downloads 2026 | title find/click for SplAttN, Dual-Latent, Flex-Forcing, OmniFit | Poster IDs: SplAttN `60900`, Dual-Latent `63955`, Flex-Forcing `65566`, OmniFit `65962`. |
| ICML poster 60900 | saved HTML and Spotlight link | Primary evidence supports SplAttN as ICML 2026 Spotlight. |
| OpenReview `SFWWUr9V7c` | forum/PDF/attachment/API | Metadata and indexed primary text accessible; direct local PDF/API/attachment downloads returned Cloudflare 403. |
| OpenReview `COGc3MSR7n` | forum/original-submission attachment | Flex-Forcing review/final-version cross-check delegated. |
| OpenReview `8RY20mLzup` | forum/PDF | OmniFit review/final-version cross-check delegated. |
| ICML Downloads title index | exact-title search | Confirms all four priority titles occur in ICML 2026 official download index. |

## GitHub/implementation lane

| Exact query/API | Outcome |
|---|---|
| `GET api.github.com/repos/zay002/SplAttN` | Official repo available; 13 stars, 1 fork, MIT, pushed 2026-07-02. |
| `GET api.github.com/repos/MzeroMiko/XDLM` | Official repo available; 27 stars, 1 fork, Apache-2.0. |
| `GET api.github.com/repos/microsoft/unilm` | Organization monorepo; 22,170 stars, 2,703 forks; only partial LatentLM coverage. |
| `GET api.github.com/repos/ZinYY/OnlineSPEC` | Official repo available; 72 stars, 11 forks. |
| `GET api.github.com/repos/jwkirchenbauer/mtp-lm` | Claimed MTP repo now available; 39 stars, 8 forks, Apache-2.0. |
| `GET api.github.com/repos/Hunter-Wrynn/DLMR` | HTTP/API `Not Found`; OpenReview's code-available claim is currently stale or private. |
| `site:github.com "OmniFit" "Layer-Adaptive Token Compression"` | No verified official repo in parent search; delegated agent continues exact-paper check. |
| `site:github.com "Flex-Forcing"` | Project/code availability delegated; do not infer implementation from title or project page. |

## Impact APIs

- GitHub REST API accessed 2026-07-24; metrics are volatile snapshots.
- Semantic Scholar Graph API returned counts for MTP Self-Distillation (4 citations, 0 influential) and ECHO (6 citations, 2 influential), but rate-limited most other requests. Missing counts are recorded as unknown, not zero.
- OpenAlex work-by-arXiv endpoint returned a non-JSON gateway response in this environment; no counts were taken from it.

## Access limitations

- OpenReview direct PDF/API/attachment downloads can be blocked by Cloudflare 403 even when search indexing exposes primary text.
- Semantic Scholar unauthenticated API rate limiting prevented a uniform 12-paper citation snapshot.
- The main repository's unrelated legacy `_artifacts/output/` population was concurrently garbage-collected; paper agents were moved to independent `/tmp` Git clones for auditable write isolation.
