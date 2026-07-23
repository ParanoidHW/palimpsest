# Search Log

- Search date: 2026-07-23
- Time window: 2020-01-01 through 2026-07-23
- Main venues: CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, AAAI, ACM MM
- Counting policy: main conference and official Findings in the formal count; workshop, arXiv-only, technical-report, withdrawn, and under-review records are reported separately.
- Inclusion rule: attention visibility, token/block selection, sparse mask/kernel lowering, or distributed attention must be a core multimodal contribution.

## Query Log

| Source | Query | Purpose | Status |
|---|---|---|---|
| Local seed | existing custom-attention paper DB and formal survey | seed candidates and method aliases | done; all venue/affiliation facts require re-verification |
| General web | `site:openaccess.thecvf.com CVPR 2024 sparse attention multimodal video attention` | test official CVF discovery | done; found LoRA-Sparse and neighboring non-sparse efficiency papers |
| OpenReview web | `site:openreview.net sparse attention multimodal` with ICLR/NeurIPS years | discover formal/workshop/submission variants | in progress |
| PMLR web | `site:proceedings.mlr.press sparse attention multimodal` | discover ICML papers | in progress |
| OpenAlex API | multimodal/video/VLM sparse-attention aliases, 2020-2026 | broad candidate discovery and metadata | pending |
| GitHub/awesome | multimodal/video sparse attention paper lists and official repositories | code/adoption discovery only | pending |

## Known Boundary Examples

- Include: LoRA-Sparse, because sparse attention approximation is the paper's primary multi-modal LLM contribution.
- Exclude from main count: Mirasol3B, unless subsequent full-text screening shows sparse attention itself is a core contribution; compact representation alone is insufficient.
- Bridge-only: generic LLM sparse attention such as MInference does not count toward strict multimodal totals unless the paper directly evaluates a multimodal setting as a core contribution.
