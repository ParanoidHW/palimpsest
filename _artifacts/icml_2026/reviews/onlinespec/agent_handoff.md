# Agent Handoff: OnlineSpec

- Status: complete, pending final manifest/hash freeze at handoff drafting time.
- Paper: *When Drafts Evolve: Speculative Decoding Meets Online Learning*, arXiv:2603.12617v1. Primary source identifies it as a Lifelong Agent @ ICLR 2026 workshop paper; ICML 2026 acceptance is not established.
- Dispatch: `icml2026-onlinespec-009`; task: `review_onlinespec`.
- Provenance: task packet `8f07ab7b35096e66c2eb2efddce0d422dd080bab093d990bcf88719291c649b5`; complete skill tree `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`; contract `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`.
- Main artifacts: `analysis.md`, `figure_inventory.md`, `review_checklist.md`, `deliverable_manifest.json`, `paper.pdf`, `source/source.tar`, `code/OnlineSPEC` at commit `3a6cc69d1c839385fcdd5f82529c55300e503b4b`.
- Validation target: Draft 2020-12 structure and all semantic checks passed with empty error lists; final evidence is recorded in `deliverable_manifest.json` and `artifact_manifest.sha256`.

## Synthesis Claims

1. The paper's central chain is verification feedback -> online loss -> lower dynamic regret -> longer accepted sequence -> higher acceleration; see `analysis.md#32-关键公式与设计动机`, source `sections/approach.tex`, Theorem 1 and Appendix proofs.
2. Opt-Hydra uses previous-round gradients as optimism hints; gains are supported by Table 1/Figure 3, but hint error `delta_T` is not measured; see `analysis.md#42-技术点证据矩阵` and `sections/application.tex`.
3. Ens-EAGLE/3 hedges multiple learning-rate draft heads and is empirically stronger than EAGLE/OSD-EAGLE bridges, while head count/runtime overhead is not isolated; see Table 1 and `analysis.md#43-收益归因`.
4. Online-LR's DPO-style feedback is better aligned to reasoning than token-error OSD-LR on several tasks; see Table 2 and `analysis.md#41-主结果`.
5. Serving evidence remains incomplete: no hardware, dtype, memory, bandwidth, concurrency or p95 telemetry; see `analysis.md#7-infra-需求分析`.

## Promotion Candidates

- Recommended slug: `onlinespec`.
- Mechanism assets: inventory rows Figure 1 and Figure 2; source crops `figures/crops/fig1_generation_refinement_caption.png`, `figures/crops/fig2_online_spec_dimensions_caption.png`.
- Result assets: inventory rows Table 1, Table 2 and Figure 3; source crops under `figures/crops/`.
- Parent must promote selected assets to `02_model_systems/ICML/2026/assets/papers/onlinespec/` and rewrite all formal links; this agent made no formal-tree edits.

## Skipped / Limitations

- OpenReview cross-check: not applicable; no forum/reviews/decision/rebuttal linked by primary sources.
- Generated diagram: skipped because the installed ICU CLI has only `generate`/`edit`, not mandatory `responses-doc --input-file analysis.md`; prompt-only art is forbidden by the contract.
- Checkpoint metadata and full reproduction: unverified; model weights were not downloaded and GPU experiments were not run.
- No suspected out-of-folder writes by this agent; filesystem read isolation is not self-certified.
