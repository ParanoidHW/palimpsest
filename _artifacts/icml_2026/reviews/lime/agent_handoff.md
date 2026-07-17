# LiME delegated handoff

- Status: `complete` for paper-evidence review; source archive, code snapshot, OpenReview and generated diagram are explicitly unavailable/skipped and do not support conclusions.
- Identity: `arxiv:2604.02338v1`, “LiME: Lightweight Mixture of Experts for Efficient Multimodal Multi-task Learning”; recommended formal slug `lime`; formal destination owned by parent: `02_model_systems/ICML/2026/papers/lime.md`.
- Provenance: dispatch `icml2026-lime-007`; agent `review_lime`; task packet SHA-256 `ca2ce31b5b862df5b71febe5f878201121b5cb0a38893e1792757df59c1315da`; skill-tree SHA-256 `93e435dbedfea453d129ba1f62cbc35f718472624053003f80461892f872be6e`; contract SHA-256 `33da33ba0fc320e994da7067084d7d0384e83bc3a5bb5c58d9633f5be54d0e21`.
- Artifacts: `analysis.md`; `figure_inventory.md`; `figures/crops/fig1_architecture_caption.png`; `figures/crops/table2_results_caption.png`; `figures/crops/fig2_efficiency_caption.png`; `figures/contact-sheet.png`; `extracted_text/paper.txt`; `paper.pdf`; `openreview_reviews.md`; `review_checklist.md`; `deliverable_manifest.json`; `artifact_manifest.sha256`.

## Synthesis claims

1. LiME replaces per-expert PEFT replication with `|ϕ|+E d_o` shared-plus-vector parameters (Eq. (1), parameter formula, Figure 1); this is the direct mechanism behind lower trainable parameter counts.
2. Zero-parameter routing reuses normalized slices of frozen/adapted outputs (Eq. (3), Figure 4); matched ablation reports comparable accuracy to learned routing, but no kernel-level latency evidence.
3. MMT-47 Table 2 shows competitive category means and Figure 2 reports 4× fewer trainable parameters/29% faster paired training; exact comparison is paper-reported and has differing parameter-count scopes that are called out in `analysis.md`.
4. Auto Top-K, n-gram routing and balance losses have sensitivity/mechanism evidence (Figures 3-5, Appendix F), but their individual runtime contributions are not isolated; 29% is a bundled system comparison.
5. Theorem 1/2/3 are plausible design rationale, with probe/CKA/scaling evidence, not direct proofs of finite-data risk or mutual-information claims.

## Visual promotion candidates

Promote only after parent copies to formal tracked assets and rewrites links: Figure 1 (`figures/crops/fig1_architecture_caption.png`, inventory row Figure 1); Table 2 (`table2_results_caption.png`, inventory row Table 2); Figure 2 (`fig2_efficiency_caption.png`, inventory row Figure 2). Each crop includes one numbered object and complete caption and passed contact-sheet plus 100% QA.

## Blocked/skipped

- Source archive: `source.tar` is invalid gzip after bounded acquisition; no source-derived claims.
- Code: exact-title GitHub candidate discovered, but no local worktree/commit was available; architecture/config claims are paper-only.
- OpenReview: public API DNS failure; no reviews/decision/rebuttal cross-check.
- Generated diagram: installed CLI lacks required `responses-doc --input-file analysis.md`; no prompt-only image.
- No suspected out-of-folder writes; all authored artifacts are under `_artifacts/icml_2026/reviews/lime/`.
