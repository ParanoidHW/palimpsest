# SGLang Trace Guide

Pin `sgl-project/sglang` to a full commit and record the relevant runtime/backend boundary. Separate frontend language APIs from the serving runtime unless both are in scope.

## Search Anchors

- Entry/configuration: server arguments, launch path, distributed initialization and model/port configuration.
- Runtime: scheduler process, tokenizer/detokenizer, tensor-parallel worker, model runner and batch objects.
- Scheduling: request states, prefill/decode batches, overlap scheduling, chunking, preemption and load balancing.
- Model execution: TP/DP/EP layers, attention backend, CUDA graphs and collective wrappers.
- KV cache: memory pool, radix/prefix cache, token-to-KV mapping, eviction and cache-aware routing.

## Required Questions

- Which process owns request state, batch formation and worker coordination?
- How do prefill and decode batches differ in token layout, cache writes and scheduling cadence?
- Which weights and KV-cache entries are local under TP, DP and EP?
- What does each collective send, who receives it and how is the result combined?
- How do radix/prefix caching and memory pools transfer ownership or reuse blocks?
- Where do overlap scheduling and CUDA graph capture constrain shapes or buffer lifetime?
- How do multi-node or disaggregated modes change state and communication ownership?

Trace scheduler decisions into the model runner and cache mutation; a layer-only trace is incomplete.
