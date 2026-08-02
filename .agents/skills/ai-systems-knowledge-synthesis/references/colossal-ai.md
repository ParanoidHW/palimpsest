# Colossal-AI Trace Guide

Pin `hpcaitech/ColossalAI` to a full commit and record plugin/version boundaries because Booster plugins intentionally choose different runtime strategies.

## Search Anchors

- Entry: `Booster`, plugin selection, launch/distributed initialization and model/optimizer preparation.
- Sharding: `ShardConfig`, policy/model rewrite, shard handlers and tensor-parallel modules.
- ZeRO/Gemini: chunk management, placement policy, parameter/gradient/optimizer partitioning and memory movement.
- Pipeline: stage manager, schedule, microbatching and point-to-point communication.
- State: checkpoint I/O, optimizer wrappers, mixed precision and state-dict conversion.

## Required Questions

- Which plugin owns model rewriting, process groups, optimizer wrapping and scheduling?
- Which `ShardConfig` option maps to a specific tensor dimension and collective?
- In Gemini/ZeRO paths, where is authoritative parameter state and when is it gathered or moved?
- What lifecycle does a chunk follow across device placement, compute, reduction and release?
- Which pipeline schedule determines stage payloads and backward ordering?
- How do plugins differ semantically rather than only by class name?
- How are sharded checkpoints portable across topology changes?

Explain each plugin in mechanism terms before naming its class.
