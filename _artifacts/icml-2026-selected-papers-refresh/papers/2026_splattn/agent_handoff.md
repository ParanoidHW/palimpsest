# Agent Handoff

- Agent status: complete
- Dispatch ID: dispatch-splattn-refresh-20260724
- Agent task name: splattn_refresh
- Paper key: 2026_splattn
- Task packet: task_packet.yaml
- Task packet SHA-256: c360805cfc20ff1495f77a865f6cc13aaf75ba662ff590395a845e27d8865779
- Skill used: paper-deep-review
- Skill directory: /tmp/icml-splattn-agent-work/.agents/skills/paper-deep-review
- Skill tree SHA-256: a338c821d6c79aff1aac224cc8713081d3b7462d46ea504771e5208dcdca96cd
- Agent contract: /tmp/icml-splattn-agent-work/.agents/skills/ai-algorithm-survey/references/paper-review-agent-contract.md
- Agent contract SHA-256: 4dc80bfb1d508898c25f3f3775a4d2ebc596c4944291cc0dded6f586fcc74c32
- Output folder: /tmp/icml-splattn-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_splattn
- Source/PDF/code acquired: complete arXiv v2 PDF; complete LaTeX source; official ICML poster 60900; code commit `0c279dd11ca13a70b676cd60ca9673e093526b9a`; three HF checkpoint metadata records
- Analysis: analysis.md
- Document version: 1.1.0
- Current revision ID: rev-splattn-refresh-20260724
- Revision mode: revise-existing
- Superseded revision/manifest: rev-splattn-initial / 1.0.0 / `1006a623b3473b4129ba2f3fd8ecb08fd7c299846678d0636e1b1438fef2650c`
- Checklist: review_checklist.md
- Visual inventory: figure_inventory.md
- Contact sheet: figures/contact-sheet.png
- Deliverable manifest: deliverable_manifest.json
- Deliverable schema validation: passed
- Deliverable semantic validation: passed
- Artifact manifest: artifact_manifest.sha256
- Counted visuals: mechanism 1; evidence 1
- Evidence loop: pass
- Code commit inspected: 0c279dd11ca13a70b676cd60ca9673e093526b9a
- OpenReview cross-check: unavailable / not applicable; official page and exact-title lookup preserved in `openreview_reviews.md`
- Generated diagram: skipped-with-reason — installed ICU CLI has no required `responses-doc --input-file analysis.md` path
- Knowledge organization: resolved default schema `c182904b…`, default profile `57461774…`, repository profile `3db4cfbe…`, policy `0ef10178…`; delegated process/formal separation enforced
- Promotion responsibility: parent survey agent

## Claims For Synthesis

| Claim | Evidence in paper/code | Analysis section | Confidence/caveat |
|---|---|---|---|
| Official ICML evidence verifies Spotlight status. | `venue/icml-poster-60900.html` title/authors and link `/virtual/2026/spotlight/84591` | §1 | high; primary ICML page |
| Soft splat gives a small matched PCN gain over hard CCM. | final PDF Table 4: Conv 6.56→6.48; Hybrid 6.41→6.36 | §4.2–§4.3 | high for reported PCN protocol |
| SplAttN is sensitive to visual removal on KITTI. | Figure 8: SCS 0.518→SCS* 0.383 (-26.1%), CMIT 200.5 | §4.1 | medium; counterfactual/oracle-specific, not general causality |
| Paper-level continuous-gradient language exceeds current implementation. | Eq. 3/7 vs `models/model_utils.py` finite 4×4 scatter and `.long()` indices at commit | §3.4, §8 | high code-reading confidence; no runtime gradient test |
| Runtime-quality trade-off is nontrivial. | Appendix Table 8: 40.75ms, 65.89M, 38.26G MACs, 0.58GB on RTX 3090 batch 1 | §4.4, §7 | high reported fact; no kernel profiling |

## Design Rationales For Synthesis

| Design | Rationale status/source | Concrete problem | Causal mechanism | Validation evidence | Trade-off/caveat |
|---|---|---|---|---|---|
| Gaussian soft splat | author-stated, §3.1–3.2 | sparse hard-projection support | finite neighborhood coverage + inverse depth | Table 4 direct replacement | no sigma sensitivity; x/y indices discrete |
| Hybrid tokenizer | author-stated, §3.2 | local/global geometry tension | EdgeConv neighborhoods + token self-attention | Table 4 replacement bundle | subcomponents not isolated |
| 3D→2D active attention | author-stated, Eq. 8 | passive fusion | geometry queries 3 view K/V tokens | Figure 8 indirect + code | no concat/no-attn ablation |
| TinyViT-5M pretraining | author-stated, Table 5 | visual prior/capacity balance | pretrained compact view encoder | scale/pretrain sensitivity | overfitting explanation unverified |
| Two-stage decoder | author-stated, Figure 1/4 | skeleton/detail trade-off | 256→2048→16384 structure/local refinement | code only | stage cost and necessity unablated |
| SCS/SCS* + CMIT | author-stated, §4.2/App. C–D | geometry metrics do not prove visual use | visual removal + entropy×coverage proxy | Figure 8 indirect | oracle/intervention confounds |

## Terminology And Symbols For Synthesis

| Type | Term/symbol | Alias/provenance | Paper-specific meaning | Scope/unit/value | Source | Ambiguity/caveat |
|---|---|---|---|---|---|---|
| term | Gaussian Soft Splatting | soft splat | Gaussian×inverse-depth finite rasterization | kernel 4; code σ=1.5 | §3.2; code | not full 3DGS; discrete scatter |
| term | CMIT | Cross-Modal Information Throughput | entropy×coverage proxy | not bit/s | Appendix C; Fig.8 | implementation-dependent scale |
| term | SCS/SCS* | oracle confidence / visual-removal confidence | DGCNN semantic confidence before/after intervention | [0,1] | Appendix D; Fig.8 | oracle and OOD sensitivity |
| symbol | \(\sigma\) | author-defined/code-valued | Gaussian bandwidth | 1.5 pixel in PCN code | Eq.3/7; config | numeric value absent from paper |
| symbol | \(w_k(\mathbf q)\) | author-defined | Gaussian×inverse-depth weight | per query/point | Eq.7 | code offsets make Gaussian factor position-invariant inside fixed window |
| symbol | \(\mathrm{CMIT}=H(\mathbf V)C(\mathbf V)\) | author-defined | total-yield proxy | Fig.8: 7.8×25.7≈200.5 | Appendix C | not throughput in time units |

## Knowledge Promotion Recommendations

| Canonical candidate | Existing owner/path | Suggested operation | Eligible formal assets | Required links | Ownership caveat |
|---|---|---|---|---|---|
| Paper `splattn` under the parent-selected 3D point-cloud/model-system domain | not inspected because delegated isolation forbids reading survey/global paper files | parent should search then choose create/update/link-only | Figure 1 and Figure 8 crops; both passed caption/bbox/contact-sheet/100% QA | README → Survey/Index → Paper; Paper backlinks; Paper → owned assets/evidence | parent owns canonical search, asset promotion, inventory merge, Git tracking, and publisher validation |

## Revision Summary

| Revision ID | Version | Revised at | Revised by | Type | Supersedes | Migration issue/resolution | Summary | Reason | Affected locations | Evidence | Conclusion impact |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rev-splattn-initial | 1.0.0 | 2026-07-16T12:00:00+08:00 | review_splattn | initial | none | none | first review | delegated review | analysis/checklist/inventory | HTML + initial code snapshot | minor |
| rev-splattn-refresh-20260724 | 1.1.0 | 2026-07-24T18:21:12+08:00 | splattn_refresh | mixed | rev-splattn-initial / 1.0.0 / `1006a623…` | none | recovered complete sources, visuals, venue and refreshed code/checkpoints | packet revision request | report, sources, figures, code, metadata | arXiv v2, official ICML page, commit/HF APIs | material |

## Blocking Or Skipped Items

| Requirement | Status | Attempt/evidence | Effect on conclusions |
|---|---|---|---|
| Public OpenReview reviews | skipped-with-reason / not applicable | packet URL unknown; official ICML page has no forum link; exact-title searches empty; `openreview_reviews.md` | no reviewer/rebuttal cross-check; venue conclusion unaffected |
| AI-generated analysis diagram | skipped-with-reason | installed CLI help exposes only `generate` and `edit`, not required document-input mode | no effect on factual conclusions |
| Checkpoint payload/config internals | skipped-with-reason | three open HF repos, pinned revisions and `.pth` filenames verified; large payloads not downloaded | weight key/config claims remain unverified |
