# Agent Handoff: XDLM

- Status: complete; final Draft 2020-12 structural validation and all semantic checks passed with empty errors; final artifact manifest verified.
- Paper: Balancing Understanding and Generation in Discrete Diffusion Models, arXiv:2602.01362v1.
- Venue: ICML 2026 candidate list only; no primary acceptance/decision evidence found.
- Recommended formal slug: `xdlm`.
- Dispatch: `icml2026-xdlm-002`; task: `review_xdlm`.
- Provenance: task packet `384e3460ef83446ce9da2c3aa0bb431e397050f4e103b9cd9851eeb6ab4759db`; skill tree `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`; contract `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`.

## Artifact paths

- Analysis: `analysis.md`; checklist: `review_checklist.md`; inventory: `figure_inventory.md`.
- PDF: `paper.pdf` (SHA-256 `2f2c23227f5d2202831a4a20dcb5364a708c044d591a463ad2d92c52fc1e0924`).
- Code: `code/XDLM/`, GitHub master commit `66c34ac5a3945d61e0e398f302bf751b5fadfa24`.
- Visuals: `figures/crops/fig1_stationary-kernel_tradeoff_caption.png`, `fig3_llada-xdlm_caption.png`, `fig4_training-dynamics_caption.png`; contact sheet `figures/contact-sheet.png`.
- Validation: passed in `deliverable_manifest.json`; frozen artifact coverage verified by `artifact_manifest.sha256`.

## Synthesis claims

1. XDLM's stationary kernel (K=kJ/N+(1-k)M) analytically recovers MDLM at (k=0) and UDLM at (k=1); evidence: `analysis.md` §“核心公式”, paper §3.1/§3.3 Eq. (5)-(19), Figure 1.
2. Scalar posterior/KL removes explicit transition-matrix construction but still consumes vocabulary-wide logits; evidence: `analysis.md` §“基础设施分析”, paper §3.2 Eq. (9)-(15), `code/XDLM/xdm_utils.py`.
3. The empirical optimum is budget/task-dependent, not universally (k=0.1); evidence: `analysis.md` §“关键实验与归因”, Figure 1, Figure 4, Tables 3/4/18/19.
4. The 8B MBPP gain (15.0 vs 6.8) is confounded by 600 continual-pretraining steps and initialization; evidence: Figure 3 and `analysis.md` technical-claim matrix.
5. XDLM's reported sample memory is 31.414 GB versus UDLM 59.683 GB on H800, but bandwidth utilization cannot be derived; evidence: paper Appendix K/Table 17 and `analysis.md` §“计算、内存与带宽”.

## Promotion candidates

- Mechanism: Figure 1 crop, inventory row 1; canonical candidate `assets/papers/xdlm/fig1-stationary-kernel-tradeoff.png`.
- Large-model result: Figure 3 crop, inventory row 2; canonical candidate `assets/papers/xdlm/fig3-llada-xdlm.png`.
- Training dynamics: Figure 4 crop, inventory row 3; canonical candidate `assets/papers/xdlm/fig4-training-dynamics.png`.

## Limitations / skips

- `source.tar` is corrupt/incomplete (`Unexpected EOF`), so original LaTeX assets were unavailable; PDF and ar5iv text remain sufficient primary evidence.
- No public OpenReview forum/reviews/decision/rebuttal was accessible; venue status remains unverified.
- Hugging Face checkpoint metadata was not acquired; the 8B architecture/checkpoint claim remains paper-reported.
- Generated analysis diagram skipped: installed OpenRouter ICU CLI lacks mandatory `responses-doc --input-file analysis.md`; prompt-only art was not used.
- No suspected out-of-folder write was observed; filesystem isolation is not self-certified.
