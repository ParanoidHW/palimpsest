# Megatron Core Trace Guide

Pin `NVIDIA/Megatron-LM` or the exact Megatron Core repository boundary to a full commit. Record the package/version relation because documentation and repository layouts can diverge.

## Search Anchors

- Configuration: model parallel sizes, sequence/context parallel flags, expert parallel settings, distributed optimizer, pipeline split and virtual stages.
- Group construction: `parallel_state`, tensor/pipeline/context/expert/data process groups and rank helpers.
- Tensor parallelism: mappings/autograd functions, column/row parallel linear layers, vocabulary parallel embeddings and cross entropy.
- Pipeline parallelism: schedules, point-to-point communication, interleaving, microbatch calculation and activation transfer.
- Context and expert parallelism: CP communication utilities, attention paths, expert group construction, token dispatcher and all-to-all paths.
- State: distributed optimizer, sharded checkpoints and RNG state.

## Required Questions

- Which group owns each axis when TP, PP, CP, EP and DP coexist, and what is the rank-coordinate order?
- For column-parallel and row-parallel linear layers, which weight dimension is local and where do gather/reduce operations appear in forward and backward?
- When sequence parallelism is enabled, which activation dimension becomes rank-local and which reduce-scatter/all-gather pair preserves semantics?
- Which pipeline schedule controls warmup, steady state and cooldown; what payload crosses stages?
- How do CP attention and EP token dispatch differ in payload, routing, and collective semantics?
- Which parameters, gradients, optimizer shards and checkpoint objects are persistent on each rank?

Trace actual symbols at the pinned revision. Do not infer a collective merely from a configuration name.
