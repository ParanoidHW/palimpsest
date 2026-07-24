# Agent Handoff

- Agent status: complete
- Dispatch ID: dispatch-flex-forcing-refresh-20260724
- Agent task name: flex_forcing_refresh
- Paper key: 2026_flex-forcing
- Task packet: task_packet.yaml
- Task packet SHA-256: 23b8b44214240a7a6b5156da50e93136b2065219f3b829dcaad2bf68f1034409
- Skill used: paper-deep-review
- Skill directory: /tmp/icml-flex-agent-work/.agents/skills/paper-deep-review
- Skill tree SHA-256: a338c821d6c79aff1aac224cc8713081d3b7462d46ea504771e5208dcdca96cd
- Agent contract: /tmp/icml-flex-agent-work/.agents/skills/ai-algorithm-survey/references/paper-review-agent-contract.md
- Agent contract SHA-256: 4dc80bfb1d508898c25f3f3775a4d2ebc596c4944291cc0dded6f586fcc74c32
- Output folder: /tmp/icml-flex-agent-work/_artifacts/icml-2026-selected-papers-refresh/papers/2026_flex-forcing
- Source/PDF/code acquired: complete arXiv PDF and source; official project/venue metadata; no official code/checkpoint release found
- Analysis: analysis.md
- Document version: 1.0.0
- Current revision ID: rev-source-complete-20260724
- Revision mode: revise-existing
- Superseded revision/manifest: rev-initial / 0.1.0 / 075d43a87072c1b36cf647ac3a6ca1513c68dd44bdf23e86982108de8e32310d
- Checklist: review_checklist.md
- Visual inventory: figure_inventory.md
- Contact sheet: figures/contact-sheet.png
- Deliverable manifest: deliverable_manifest.json
- Deliverable schema validation: passed
- Deliverable semantic validation: passed
- Artifact manifest: artifact_manifest.sha256
- Counted visuals: mechanism 1; evidence 1
- Evidence loop: pass
- Code commit inspected: unavailable; no official implementation claimed/linked
- OpenReview cross-check: venue/front matter done; public reviews/decision/rebuttal blocked by challenge/API 403
- Generated diagram: skipped-with-reason — installed CLI lacks mandatory `responses-doc --input-file analysis.md`
- Knowledge organization: built-in publisher schema + profile `huangwei-research-vault`; profile SHA-256 `3db4cfbe7978675b5b8fbb4675c65942cef6d8aa44cb29cc2335e1d4969c3a2c`, default profile `574617743d18fac813cd4c311e45b68a6e6570f65772baebefbbdd796ea48a2e`, organization schema `c182904b3083e912117e109dcf97f6f73e93119666908ef14fedb6deb8f961dd`
- Promotion responsibility: parent survey agent

## Claims For Synthesis

| Claim | Evidence in paper/code | Analysis section | Confidence/caveat |
|---|---|---|---|
| A single trained model exposes AR, hybrid, and bidirectional inference as boundary configurations. | §3.1, Eq. 1–2, Table 1, Figure 3 | `analysis.md#2-核心贡献与证据边界`; `#32-模型与系统架构` | High for formulation and demonstrated operation; no released code. |
| `[15,3,3]` at NFE5 improves over Self-Forcing chunk-wise by +0.76 VBench Total and +0.9 FPS on GB200. | Table 2 | `analysis.md#41-5-秒主结果质量与速度分开看` | High for reported table arithmetic; hardware count/dtype/timing protocol absent. |
| Flex schedules do not uniformly dominate: fine-grained `[3×7]` is 0.28 Total below Self-Forcing chunk-wise at the same 24.9 FPS. | Table 2 | `analysis.md#41-5-秒主结果质量与速度分开看` | High; important negative evidence against broad “consistent” wording. |
| K-Projection stabilizes performance as maximum chunk size grows. | §3.3, Eq. 5–6, Figure 8 | `analysis.md#42-其他结果与系统约束`; `#43-技术-claim-证据矩阵` | Direct ablation, but no error bars or runtime isolate. |
| On 30 s videos, Ours vs Infinity-RoPE reports +1.17 Total, +5.86 FPS, and +21.01 Dynamic Degree, with several submetrics lower. | Table 4 | `analysis.md#42-其他结果与系统约束` | Reported arithmetic; confounded because Ours builds on Infinity-RoPE and uses one sample/prompt. |
| Device-budget flexibility is a configurable compute/latency claim, not a verified memory-budget result. | GB200/A100 plots; no peak-memory table | `analysis.md#42-其他结果与系统约束`; `#72-显存与-kv-cache` | High evidence for the gap; no OOM/memory frontier. |

## Design Rationales For Synthesis

| Design | Rationale status/source | Concrete problem | Causal mechanism | Validation evidence | Trade-off/caveat |
|---|---|---|---|---|---|
| Frame-axis variable chunks | author-stated, §3.1/Table 1 | AR efficiency vs bidirectional coherence | bidirectional intra-chunk + causal cached inter-chunk | Figure 4; Table 2, direct | schedule-dependent; fine-grained negative result |
| Timestep nested chunks | author-stated, §3.2/Figure 3 | global planning and local refinement need different context | split chunks as noise drops | Figure 7, direct schedule ablation | tested schedule set is small; buffering needed |
| Random flexible-chunk training | author-stated, §3.3 | one model must tolerate many masks | stochastic partitions expose mixed causal contexts | full-model multi-config behavior, confounded | no no-randomization ablation |
| DMD/VSD self-rollout training | author-stated, §3.3 | few-step train/test exposure mismatch | self-generated states + distribution matching | comparisons, confounded | largely inherited from CausVid/Self-Forcing |
| K-Projection | author-stated, §3.3/Eq. 5–6 | clean/noisy key SNR mismatch | timestep-conditioned clean-key projection | Figure 8, direct ablation | no parameter/runtime or value-projection comparison |
| Buffer/resume scheduler | author-stated, §3.2/Appendix Fig. 13 | split child lacks prior-subchunk KV | buffer parent result and resume after dependency | mechanism diagram, indirect | memory/latency/code unverified |
| Late-timestep editing | author-stated, §4.2/Figure 6 | local edits propagate globally | preserve early planning, change late refinement | qualitative matched visualization | restricts structural edits; no metric |
| Bilateral any-order editing | author-stated, §4.2/Eq. 7/Figure 5 | strict causal order blocks middle edits | condition target on past and future clean chunks | qualitative visualization | no defined success rate |

## Terminology And Symbols For Synthesis

| Type | Term/symbol | Alias/provenance | Paper-specific meaning | Scope/unit/value | Source | Ambiguity/caveat |
|---|---|---|---|---|---|---|
| term | flexible chunking | author-defined | contiguous chunks over frame and denoising axes | per timestep | §3.1–3.2 | changes attention visibility, not merely batching |
| term | K-Projection | noise-aligned projection | projects clean cached keys to current noisy space | per layer/timestep | §3.3, Eq. 5–6 | parameter sharing and V handling unspecified |
| term | NFE | author-defined | denoising evaluations; causal rows add one caching step | 2–5 in tables | Table 2 caption | not sufficient alone to predict speed |
| term | any-order editing | author-defined | middle-chunk editing using both past/future clean context | post-generation | §4.2, Eq. 7 | not strictly causal |
| term | sink/window | author-defined | long-video attention sink 3, window 21 latent frames | latent frames | §5 Implementations | no sensitivity analysis |
| symbol | \(F,T,t,K_t,k\) | author-defined | frames, denoising steps, timestep, chunk count/index | global/per timestep | §3.1 | latent vs output frame count differs |
| symbol | \(\mathbf a_t,\mathcal F_{t,k},\mathcal S_{t,k}\) | author-defined | boundaries, chunk set, inserted split points | frame indices | Eq. 1–3 | configs in tables are sizes, not boundaries |
| symbol | \(x_t,q_\theta,G_\theta\) | author-defined | latent, reverse transition, distilled generator | model/sample | Eq. 2–4 | \(q_\theta\)/\(G_\theta\) prose is not strictly unified |
| symbol | \(\Pi_{t\leftarrow0},Q_t,K_0,\tilde K_t,V_t,d\) | author-defined | key alignment and attention tensors/dimension | layer/timestep | Eq. 5–6 | only clean K is explicitly projected |
| symbol | \(B_{\mathrm{KV}}\) | analysis-derived | KV-cache byte estimate | bytes | `analysis.md#72-显存与-kv-cache` | cannot evaluate without layers/tokens/heads/dtype |

## Knowledge Promotion Recommendations

| Canonical candidate | Existing owner/path | Suggested operation | Eligible formal assets | Required links | Ownership caveat |
|---|---|---|---|---|---|
| Paper `flex-forcing` in model-systems/video-generation domain | Parent must search; not read in isolated paper run | create or update after deduplication | Figure 3 crop; Table 2 crop | domain README → Survey/Index → Paper; Paper backlinks; Paper → owned assets/evidence | Parent must choose canonical domain and run publisher validation. |
| Survey claims on adaptive video-diffusion inference | Parent survey owns | link-only to canonical Paper sections | no duplicate assets | Survey claim → Paper mechanism/results/limitations anchors | Preserve schedule-dependent and system-evidence caveats. |
| Paper figure inventory entries | Parent evidence owner | merge two QA-passed rows | same two assets | Paper/evidence inventory bidirectional links | Process crops must be promoted to Paper-owned formal assets before formal linking. |

## Revision Summary

| Revision ID | Version | Revised at | Revised by | Type | Supersedes | Migration issue/resolution | Summary | Reason | Affected locations | Evidence | Conclusion impact |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rev-initial | 0.1.0 | 2026-07-17T00:00:00+08:00 | review_flex_forcing | initial | none | none | Initial blocked review package | Truncated/unreadable PDF | analysis, inventory, checklist | old `paper.pdf`; `extracted_text/error.log` | material |
| rev-source-complete-20260724 | 1.0.0 | 2026-07-24T20:20:34+08:00 | flex_forcing_refresh | mixed | tracked rev-initial / 0.1.0 / 075d43a87072c1b36cf647ac3a6ca1513c68dd44bdf23e86982108de8e32310d | none | Source-complete method/result/visual/venue/system revision | Refresh request | analysis, inventory, reviews, verification, crops | complete arXiv PDF/source; official project/venue; table/figure QA | material |

## Blocking Or Skipped Items

| Requirement | Status | Attempt/evidence | Effect on conclusions |
|---|---|---|---|
| OpenReview reviews/decision/rebuttal/full revision history | blocked | forum and indexed PDF challenge; API v1/v2 HTTP 403; `openreview_reviews.md` | Venue/front matter verified, but reviewer concerns and submission-to-final changes cannot be assessed; parent verdict should be accepted-with-limitations. |
| Direct poster 65566 snapshot | blocked | ICML direct page HTTP 403/robots; triangulated with official NVIDIA page, ICML Downloads, OpenReview subject | Does not materially weaken Spotlight venue conclusion, but exact poster metadata is not frozen. |
| Official code/checkpoint | skipped-with-reason | official paper/project contain no link; exact GitHub repository search only unrelated results | Implementation, dtype, kernel, cache scheduler, and reproducibility claims remain paper-only/unverified. |
| Generated analysis diagram | skipped-with-reason | API key present, but installed CLI lacks mandatory `responses-doc --input-file`; `extracted_text/generated-diagram-capability.txt` | No effect on paper-derived evidence; no substitute image. |
| Memory/bandwidth/device-budget proof | blocked as evidence claim | no peak memory, GPU count, bytes/kernel trace, dtype, interconnect, or fixed-budget experiment | “Device budget” is limited to a configurable speed/quality knob, not verified memory-budget adaptation. |

