# PyTorch FSDP And DTensor Trace Guide

Pin `pytorch/pytorch` to a full commit. Record whether the profile covers FSDP1, FSDP2/composable APIs, or both; do not merge their runtime behavior.

## Search Anchors

- Device topology: `DeviceMesh`, named mesh dimensions and process-group creation.
- Distributed tensor: `DTensor`, placements (`Shard`, `Replicate`, `Partial`), redistribution and operator propagation.
- FSDP: public wrapping/composable entry, parameter grouping/flattening, all-gather, reduce-scatter, prefetch and reshard policies.
- State: mixed precision, CPU offload, optimizer state dict, sharded/full state dict and checkpoint integration.

## Required Questions

- What does each placement mean for the global-to-local shape, and which uneven-shard rules apply?
- Which operator propagation rule preserves or changes placements?
- Which redistribution invokes all-gather, reduce-scatter, all-to-all or local slicing?
- When does FSDP materialize full parameters, free/reshard them, and reduce gradients?
- What differs between original parameters, flattened storage and DTensor-backed parameters?
- How do 1D and 2D meshes compose data, tensor and sequence axes?
- How are model and optimizer checkpoints represented and restored?

Treat placement metadata as a semantic contract, then verify the actual collective path at the pinned source revision.
