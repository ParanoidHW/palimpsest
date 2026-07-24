# GitHub and Curated Discovery Sources

Metrics were accessed on 2026-07-24 and are approximate volatile snapshots. Lists are discovery aids, not venue authority.

| Repository/list | URL | Stars/Forks | Update/activity signal | Relevant section | Contribution | Trust note |
|---|---|---:|---|---|---|---|
| SplAttN | https://github.com/zay002/SplAttN | 13 / 1 | pushed 2026-07-02; 0 open issues; MIT | full repo | Official implementation and checkpoint links for SplAttN | Pinned code inspection is stronger than README claims; venue is verified separately. |
| XDLM | https://github.com/MzeroMiko/XDLM | 27 / 1 | pushed 2026-03-16; Apache-2.0 | full repo | Official XDLM implementation | Used for implementation evidence, not citation impact. |
| Microsoft UniLM | https://github.com/microsoft/unilm | 22,170 / 2,703 | pushed 2026-01-23; MIT | LatentLM subtree | Partial LatentLM ImageNet implementation | Monorepo-wide stars do not measure LatentLM adoption. |
| OnlineSPEC | https://github.com/ZinYY/OnlineSPEC | 72 / 11 | pushed 2026-07-11; 1 open issue | full repo | Official OnlineSpec implementation | Venue remains ICLR workshop, independent of repo activity. |
| MTP-LM | https://github.com/jwkirchenbauer/mtp-lm | 39 / 8 | pushed 2026-02-21; Apache-2.0 | full repo | Newly reachable implementation candidate for MTP Self-Distillation | Requires fresh code-path/commit review before formal implementation claims. |
| DLMR claimed repo | https://github.com/Hunter-Wrynn/DLMR | unavailable | GitHub API `Not Found` | none | Tests OpenReview's “code available” claim | Currently stale/private/unreleased; not counted as adoption. |
| Awesome 3D Gaussian Splatting Papers | https://github.com/Awesome3DGS/3D-Gaussian-Splatting-Papers | metric not captured | indexed/crawled 2026-07 | ICML 2026 section | Rediscovered SplAttN and its ICML Spotlight label | Curated list; verified against ICML poster/arXiv before use. |
| Hugging Face Papers: SplAttN | https://huggingface.co/papers/2605.01466 | 6 upvotes (page snapshot) | author update in May 2026 | models/checkpoints | Located PCN/ShapeNet checkpoint repos | Community page is not venue authority; checkpoint metadata was inspected separately. |
| Hugging Face Papers: Flex-Forcing | https://huggingface.co/papers/2607.03509 | 14 upvotes (page snapshot) | crawled 2026-07-22 | project link | Located project page and current paper summary | Discovery only; final paper/source governs claims. |

## Classification

- `primary-contribution`: the 12 paper records in `paper_db.jsonl`.
- `native-system-component`: inspected official paper repositories/checkpoints where the method itself is implemented.
- `optional-official-backend`: LatentLM coverage inside UniLM; it is partial, not the whole paper system.
- `third-party-integration`: DODO course repo is explicitly excluded from official implementation counts.
- `mention-only`: repositories or pages that merely mention an unavailable code release.
