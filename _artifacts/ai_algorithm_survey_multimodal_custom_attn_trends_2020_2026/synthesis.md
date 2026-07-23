# Multimodal Sparse Attention Trend Synthesis

## Revision information

- Version: 1.0.0
- Revision: rev-2026-07-23-initial
- Type: initial
- Scope: initial audited trend corpus and formal survey integration.

## Scope and revision information

- Snapshot: 2026-07-23.
- Window: 2020-2026; 2026 is year-to-date.
- Venues: CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, AAAI, ACM MM; official Findings separated.
- Boundary: multimodal tasks where attention visibility, token/block selection, mask/kernel lowering, or distributed sparse attention is a core contribution.
- Counting: one paper per canonical venue version; affiliations use paper-level full counting.

## Results

The audited corpus contains 38 formal papers: 0/0/0/3/7/16/12 for 2020-2026. The corpus is an auditable lower bound, not an exhaustive bibliometric census. It contains two adjacent works and one arXiv-only work for boundary auditing. Organization metadata is directly verified for 6 formal papers only, so the organization chart is a verified subset rather than a field ranking.

## Timeline and taxonomy

- 2023: sparse video-text pretraining and progressive pruning.
- 2024: importance/instruction-guided visual-token selection and programmable mask lowering.
- 2025: dynamic video-token budgets, token merge/prune combinations, and attention-sparsity compression.
- 2026: hierarchical/object-centric compression, reinforcement-learned selectors, and non-uniform learned sparse attention.

Method families collapse into two implementation layers: selector/compression changes sequence shape and requires gather/scatter, sorting, ragged metadata and cache management; sparse-attention lowering preserves tokens but changes visible pairs and requires compact mask IR, block scheduling and load balancing. These layers can compose but need separate accounting.

## Infrastructure implications

The trend moves away from one fixed mask shared by all heads/layers. A practical runtime needs dynamic budgets, per-sample/per-head descriptors, temporal reuse, stable compaction, KV-cache lifecycle control and a dense fallback. Evaluation must report end-to-end latency and memory alongside logical sparsity because selector, packing and imbalance can dominate the saved attention FLOPs.

## Evidence caveats

ACM MM and some 2026 venue indexes remain incompletely audited. Formal counts exclude workshop, withdrawn and arXiv-only versions. Organizations are never inferred from author names; unknown affiliation arrays remain empty. New per-paper deep reviews and isolated paper agents were explicitly skipped by user request.

## Terminology and symbols

This trend census uses selector/compression for methods that change sequence shape and sparse-attention lowering for methods that change visible query-key pairs. No shared mathematical symbol table is required for the venue and affiliation counts.
