# DeepSpeed Trace Guide

Pin `microsoft/DeepSpeed` to a full commit and record compatible PyTorch/CUDA boundaries when the claim depends on them.

## Search Anchors

- Configuration and entry: JSON schema/keys, `initialize`, engine construction, module/optimizer wrapping.
- ZeRO: stage selection, parameter partitioning, coordinator/fetch-release logic, gradient reduction, optimizer partition and persistence thresholds.
- Offload: CPU/NVMe parameter and optimizer paths, prefetch buckets, pinned buffers and asynchronous I/O.
- Parallelism: process groups, pipeline engine/schedule, tensor parallel integrations and sequence-parallel Ulysses paths.
- State: checkpoint consolidation, partition metadata, loss scaling and optimizer state.

## Required Questions

- For ZeRO stages 1, 2 and 3, exactly which optimizer states, gradients and parameters are sharded?
- Which hook or coordinator makes a parameter temporarily available, and when is its buffer released?
- What do reduce-scatter and all-gather carry; is the result a sum, concatenation, or ownership transfer?
- Which bucket sizes and persistence thresholds alter peak memory and communication overlap?
- For offload, where is authoritative state stored and which transfer blocks compute?
- For Ulysses, which sequence/head layout transposition occurs and how is attention restored?
- How do checkpoint save/load and model export reconstruct full state?

Distinguish public configuration semantics from source-only behavior and version-dependent integrations.
