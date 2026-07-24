# Selection and Refresh Priorities

## Selection rule

This is an incremental continuation of a user-specified 12-paper list, not a newly constructed ICML acceptance list. All 12 records remain selected for continuity, while venue and evidence status are independently classified. Deep-review revision is limited to papers whose previous delivery had a material source/code gap; unchanged accepted paper deliveries remain prior evidence inputs.

## Priority revisions

| Paper | Evolution role | Previous blocker | Current action/status |
|---|---|---|---|
| SplAttN | core 2D–3D multimodal mechanism | truncated PDF/source; zero visuals; venue unverified | Accepted refreshed delivery: complete PDF/source, Spotlight evidence, code/checkpoints, two visual types. |
| Dual-Latent Memory Routing | core memory/router method | abstract only; no PDF/code/reviews | Exact OpenReview identity found, but local PDF remains Cloudflare-blocked and claimed repo is 404; revised delivery rejected after shared-workspace write-audit failure. |
| Flex-Forcing | core generative-model bridge | unreadable partial PDF; no method/visual evidence | Fresh independent-clone agent running with arXiv/OpenReview/ICML inputs. |
| OmniFit | core token-compression/system method | paper identity unresolved | Exact ICML Spotlight/OpenReview paper resolved; fresh independent-clone agent running. |
| LiME | bridge parameter-efficient multimodal routing | source archive partial | PDF evidence already complete; source-only retry follows the four blocked papers. |
| MTP Self-Distillation | core verifier-free decoding | source/code unavailable | Repository now resolves with 39 stars/8 forks; fresh code/source review remains pending. |
| DODO | variant/failure-repair case | source archive partial; no official code | PDF/HTML evidence already complete; source-only retry remains pending. |

## Important status exclusions

- OnlineSpec remains selected for mechanism comparison but is an ICLR 2026 workshop paper, not ICML main track.
- DODO remains selected for its failure analysis but is an ICML SPIGM workshop presentation.
- LiME, XDLM, LatentLM, and MTP Self-Distillation must not be promoted to confirmed ICML without primary venue evidence.
- arXiv:2604.21575 is excluded because it is a different 3D body-fitting work named OmniFit.
- arXiv:2602.00471 is excluded because it is a different dual-latent visual multi-agent paper.
- The DODO course repository is excluded from official-code counts.

## Search coverage

- General web: exact-title and alias queries recorded in `search_log.md`.
- GitHub/curated lists: official repositories, Hugging Face paper/checkpoint pages, and Awesome3DGS.
- arXiv: PDF and `e-print` source endpoints for all arXiv-backed priority records.
- Top venue: ICML Downloads/poster IDs and OpenReview records; final PMLR text where indexed.

## Organization distribution

| Organization | Selected papers | Evidence/caveat |
|---|---|---|
| Southwest Jiaotong University | SplAttN | paper/arXiv author block. |
| National University of Singapore + NVIDIA Research | Flex-Forcing | ICML final-paper first page. |
| Microsoft Research + Tsinghua University | LatentLM | paper first page. |
| Kuaishou Technology | ECHO | paper first page. |
| Nanjing University + UC San Diego | OnlineSpec | paper/source. |
| DLMR/OmniFit author organizations | Dual-Latent, OmniFit | exact authors resolved; affiliations await locally readable final PDF and are not inferred from names. |
| Unknown/not preserved | remaining records | Empty affiliation arrays with explicit caveats in `paper_db.jsonl`. |

## High-value signals

- Conceptual anchors: XDLM, LatentLM, SplAttN, SelfJudge.
- System/serving anchors: ECHO, OnlineSpec, MTP Self-Distillation, OmniFit.
- Recent Spotlight anchors: SplAttN, Dual-Latent, Flex-Forcing, OmniFit, ECHO.
- Repository attention is led by OnlineSPEC among dedicated paper repos; UniLM's much larger monorepo metrics are not attributed wholly to LatentLM.
- Citation API coverage is incomplete; only MTP (4) and ECHO (6, including 2 influential) returned before rate limiting.

## Access limitations

- OpenReview Cloudflare controls can expose searchable primary text while blocking local PDF/API downloads.
- Citation metrics are incomplete because unauthenticated Semantic Scholar requests were rate-limited.
- Main-repository legacy artifact cleanup broke shared-workspace write audits; accepted new revisions use independent clone-local audits.
