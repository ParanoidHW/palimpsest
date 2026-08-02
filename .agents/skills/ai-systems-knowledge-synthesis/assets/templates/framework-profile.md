# <Framework Name>

## Version Boundary

- Repository: `<url>`
- Commit: `<40-character commit>`
- Version/tag context: `<value>`
- Scope exclusions: `<value>`

## Plain-Language Architecture

<Explain process groups, rewriting, engine/scheduler, worker, and model runner.>

## User Configuration

<Explain each relevant key in ordinary language.>

## Implementation Trace

For each claim, record `configuration -> entry API -> runtime/module -> collective -> tensor layout`; explain behavior at every hop and link a trace ID.

## Process Groups And Tensor Layout

## Model Rewrite And Runtime

## Training State

<Parameters, gradients, optimizer, checkpoint; or not-applicable with reason.>

## Serving State

<Scheduler, KV cache, prefill, decode; or not-applicable with reason.>

## Paper Correspondence And Engineering Differences

## Evidence Boundary
