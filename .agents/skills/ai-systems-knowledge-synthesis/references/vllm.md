# vLLM Trace Guide

Pin `vllm-project/vllm` to a full commit and record engine-generation boundaries because scheduler, worker and model-runner layers change frequently.

## Search Anchors

- Configuration/entry: engine arguments, LLM/async entry, distributed executor selection and parallel configuration.
- Distributed state: initialization, TP/PP/DP/EP groups, custom collectives and rank coordination.
- Runtime: engine core, scheduler, executor, worker, model runner, input batching and output processing.
- Model rewrite: parallel linear/embedding layers, attention backends, expert layers and quantization.
- KV cache: block manager, allocator, cache engine, block tables, prefix caching and transfer/offload paths.

## Required Questions

- Which component decides request admission, token budgets, preemption and batch membership?
- How does prefill input shape differ from decode, and where are model inputs assembled?
- Which rank owns each weight shard and KV-cache block; which metadata is replicated?
- What payload crosses TP, PP, DP or EP collectives at each phase?
- How do custom collectives preserve the same semantics as standard operations?
- When are KV blocks allocated, populated, read, appended, evicted or transferred?
- How do speculative decoding, chunked prefill or disaggregated serving alter the trace?

Do not describe serving solely through model layers; scheduler and cache ownership are part of the mechanism.
