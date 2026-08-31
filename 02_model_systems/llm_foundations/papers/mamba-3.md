---
tags: [paper, collection/llm-foundations, domain/model-systems, status/deep-review, topic/selective-state-space-models, method/complex-mimo-ssm]
document_type: paper
domain: llm_foundations
collection: LLM Foundations
review_status: accepted-with-limitations
canonical: true
---

# Mamba-3: Improved Sequence Modeling using State Space Principles

![统一结构示意图](../assets/papers/mamba-3/mamba-3-architecture.png)

Mamba-3 extends the selective state-space branch with exponential-trapezoidal discretization, complex-valued rotations, and rank-$R$ MIMO heads. It is a selective SSM, not strict feature-map linear attention: its linear-length execution comes from semiseparable state transitions and scan/SSD kernels.

## Evidence And Boundary

The fresh review covers arXiv 2603.15569v1, the official `state-spaces/mamba` snapshot, three caption-complete original-paper visuals, and schema validation with zero errors. Reported gains are limited to 180M-1.5B FineWeb-Edu models and single-H100 measurements; components co-vary, the paper-era code commit is unavailable, and cross-hardware portability is unverified.

## Mechanism

The trapezoidal update blends previous and current input endpoints, reducing discretization bias. Complex rotations add state geometry needed for parity-like tracking, while MIMO rank $R$ lets one state serve multiple input/output streams. Prefill uses SSD/Triton block multiplication; decode keeps a constant recurrent state and no growing KV cache. These properties explain the systems distinction from GLA/DeltaNet matrix-state attention and from full attention's exact token-pair retrieval.

## Visual Evidence

![Mamba-3 exponential-trapezoidal mechanism](../assets/papers/mamba-3/fig1-exponential-trapezoidal-caption.png)

![Mamba-3 pretraining perplexity](../assets/papers/mamba-3/fig5-pretraining-perplexity-caption.png)

![Mamba-3 state-size Pareto](../assets/papers/mamba-3/fig6-state-size-caption.png)

## Links

- Survey: [Linear Attention Transformer 演化](../surveys/linear-attention-transformer-evolution.md)
- Evidence: [Linear attention evidence](../evidence/linear-attention-transformer-evidence.md)
- README: [LLM Foundations](../README.md)
