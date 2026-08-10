# <Method Name>

## Plain-Language Summary

<Explain the mechanism without framework jargon.>

## Symbol Table

| Symbol | Plain-language meaning | Shape or value domain | Lifecycle or owner |
| --- | --- | --- | --- |
| `<symbol>` | `<ordinary-language definition>` | `<shape/range>` | `<phase/owner>` |

## Problem And Failure Without It

<State the concrete bottleneck and a numeric failure example.>

## Global State And Partition Axis

<Name the global tensor/state, shape, ownership, and partition axis.>

## Tensor Walkthrough

- Before partition: `<name>`, shape `<numeric shape>`.
- Rank-local ownership: world size `<p>`; rank `<r>` owns `<slice>` with shape `<numeric shape>`.
- Local operator: `<operation>` maps `<shape>` to `<shape>`.
- Collective: `<payload>` is sent by `<senders>` to `<receivers>` and combined by `<sum|concat|transpose|ownership transfer>`.
- After communication: shape `<numeric shape>`; correctness follows because `<reason>`.

## Lifecycle Differences

### Training Forward

### Training Backward And Optimizer

### Prefill

### Decode

## Cost And Buffer Lifetime

<Communication volume, persistent memory, temporary memory, recomputation, and lifetime.>

## Composition And Failure Conditions

<Other axes, divisibility/topology constraints, and concrete invalid cases.>

## Evidence Boundary

<Map claims to paper, official-doc, pinned-source, measurement, or analysis-derived IDs.>
