---
name: ai-systems-knowledge-synthesis
description: Build method-first, source-traceable knowledge systems for AI training, inference, parallelism, memory, and runtimes. Use for AI systems knowledge synthesis, framework source analysis, distributed training/serving implementation comparisons, method-to-code mappings, tensor/collective walkthroughs, model-training workflow diagrams, tensor-ownership visualizations, or rewriting systems explanations to remove unexplained framework jargon. Supports Megatron Core, DeepSpeed, PyTorch FSDP/DTensor, Colossal-AI, vLLM, and SGLang without requiring a full literature survey or a fixed paper count.
---

# AI Systems Knowledge Synthesis

## Purpose

Build an explanation around stable mechanisms, then show how pinned framework revisions implement them. Treat papers, official documentation, pinned source code, measurements, and synthesis-derived analysis as distinct evidence classes. Default to Chinese prose unless the user requests another language; preserve exact API, configuration, tensor, and code identifiers.

This workflow is method-first. Do not turn every request into a literature survey or six separate framework manuals. Include only the methods and frameworks needed to answer the scope, while keeping the output contract intact.

## Mandatory Contract

Before substantive work:

1. Read the repository's `AGENTS.md` and research-knowledge policy when present.
2. Query the repository coverage matrix by title, alias, arXiv ID, model, and framework name before selecting or deep-reviewing papers.
3. Run `scripts/init_knowledge_workspace.py <slug>` from the repository root. Use its default `_artifacts/ai_systems_knowledge_<slug>/` location unless repository policy resolves another process root.
4. Classify every checklist item as `pending`, `done`, `blocked`, or `skipped-with-reason`.

Keep all working outputs in the process workspace. Formal publication is a separate, explicit promotion step.

## Load References Selectively

Read [references/evidence-and-readability.md](references/evidence-and-readability.md) for every task. Read one framework guide completely before tracing that framework:

- [references/megatron-core.md](references/megatron-core.md)
- [references/deepspeed.md](references/deepspeed.md)
- [references/pytorch-fsdp-dtensor.md](references/pytorch-fsdp-dtensor.md)
- [references/colossal-ai.md](references/colossal-ai.md)
- [references/vllm.md](references/vllm.md)
- [references/sglang.md](references/sglang.md)

Read [references/systems-diagrams.md](references/systems-diagrams.md) completely when the user requests a workflow, dataflow, tensor-partition, memory-ownership, collective, or parallelism diagram, or when a diagram is necessary to make the mechanism understandable.

Do not hardcode line numbers from a reference guide. Resolve symbols against the pinned commit and record durable repository-relative paths plus symbol names and line ranges in the trace ledger.

## Six-Phase Workflow

### 1. Scope And Canonical Reuse

- Define the user questions, included methods, lifecycle phases (`training`, `prefill`, `decode`), frameworks, and required implementation depth.
- Choose method cards before framework profiles. Typical cards include data parallelism (DP), tensor parallelism (TP), pipeline parallelism (PP), expert parallelism (EP), sequence parallelism (SP), context parallelism (CP), and Zero Redundancy Optimizer (ZeRO).
- Check canonical repository content. Use `link-only` or incremental revision when coverage and evidence versions match. Create a new canonical paper review only when the matrix misses or existing mechanism evidence is insufficient.
- Do not invoke `$ai-algorithm-survey` merely because papers are present. Invoke `$paper-deep-review` only for a missing canonical paper or a material evidence gap.

### 2. Register Evidence

- Add every paper, official document, repository, commit, release, benchmark, and accessed date to `sources.jsonl` before relying on it.
- Pin source claims to a full immutable commit SHA. Record tags only as human-readable version boundaries.
- Give every evidence object a unique ID and one class: `paper`, `official-doc`, `pinned-source`, `measurement`, or `analysis-derived`.
- Use `analysis-derived` for cross-source inference. Never present it as a paper or code claim.

### 3. Model Each Method

Create `methods/<method>.md` from the method template. Answer all of these:

- What concrete problem exists, and how does the previous design fail?
- What is the global tensor or state, and along which axis is it partitioned?
- What does each rank own, including exact local shapes?
- Which local operator runs, and which collective restores the global semantics?
- What changes across forward, backward, optimizer, prefill, and decode?
- What communication, memory, buffer lifetime, and recomputation costs result?
- How does the method compose with other axes, and under which conditions does it fail?
- Which statements come from each evidence class?

Include at least one numeric tensor walkthrough. State shape before partition, rank-local shape, payload and participants for every collective, and shape after communication.

When producing a mechanism diagram, make the model or runtime operation the main dataflow and place tensor ownership beside it. Parameterize world size as `p` and the illustrated process as rank `r`; do not imply a fixed two-rank system. For training, show micro-batches as a sequential queue unless the method actually pipelines or overlaps them. Follow the diagram contract and inspect its bundled visual examples in [references/systems-diagrams.md](references/systems-diagrams.md).

Define a visual grammar before drawing and preserve it across the diagram set. Keep tensors or weights, model compute, persistent rank-local state, collectives, and runtime actions visually distinct; never color an operation as a tensor or stored state. Keep boxes content-tight and use spacing, not empty padding, to preserve visible arrow shafts.

Before drawing, create a diagram contract in the process workspace using `assets/diagram-delivery.schema.json`. It must freeze the viewpoint, abstraction level, primary chain, allowed edges, forbidden edges, tensor shapes, communication payloads, and review regions. If the requested semantics do not determine these fields, ask the user for the missing choices instead of inferring them from labels.

Apply two composition budgets before adding detail: the mechanism's occupied content should have a stable visual center of gravity within the core frame, and each panel should use at most one heading, one subtitle, and two short explanatory notes. Exact pixel centering is not required; allow small offsets when they improve routing, grouping, or reading order. Put definitions and caveats in the caption/footer or companion prose; do not fill unused space with paragraph-like labels.

Keep method principles and framework implementation details in separate visual layers. A principle diagram must be framework-neutral in its visible title, subtitle, nodes, legend, and caption: omit repository names, commits, versions, configuration keys, class names, and source symbols. Use pinned framework source to verify the principle, identify semantic differences, and provide supplemental implementation traces; do not add buckets, hooks, fused buffers, coordinator queues, prefetch policies, or overlap schedules to a principle diagram. When implementation detail is useful, create a separately labeled framework supplement and link it back to the stable method diagram.

Keep operation nodes as the visual backbone. Show most intermediate tensors as short labels connected to the corresponding flow arrow by a thin leader with visible clearance; reserve standalone tensor boxes for inputs, outputs, persistent or owned objects, and a current item such as $m_k$ when it materially clarifies sequential execution. Never create one logical arrow from differently colored segments. For TP/EP and similar intra-layer partitions, draw a pre-norm layer-level compute flow, label normalization generically as `Norm`, show rank-local weight ownership, and insert partition layouts plus collectives at the exact operation boundary.

### 4. Trace Framework Implementations

Create `frameworks/<framework>.md` from the framework template and a matching framework guide. Pin one repository commit per trace boundary.

For every material implementation claim, add a trace with all five stages:

```text
configuration -> entry API -> runtime/module -> collective -> tensor layout
```

At every hop, explain the behavior in ordinary language. Record source path, symbol, line range, evidence ID, and the input/output state. Cover process groups, model rewriting, scheduler or engine, worker/model runner, checkpoint/optimizer state, and KV cache where relevant. Explain how the implementation matches, extends, or differs from the paper mechanism.

Treat framework tracing as comparison evidence, not as permission to rewrite the method around one runtime optimization. Preserve the method-level tensor and collective semantics first; record bucketization, hooks, fusion, scheduling, prefetch, and overlap as supplemental implementation behavior with an explicit version boundary.

### 5. Synthesize Across Frameworks

- Write `crosswalk.md` by stable method semantics, not marketing terms.
- Map configuration keys, public APIs, runtime symbols, collectives, layouts, and lifecycle phases.
- Explain composition and incompatibilities across DP/TP/PP/EP/SP/CP/ZeRO axes.
- Keep training, prefill, and decode separate. Do not write “inference is similar” where scheduling, cache ownership, batch shape, or communication differs.
- Write `synthesis.md` last: problem space, method taxonomy, composition, training-versus-serving differences, and concrete engineering decisions.

### 6. Validate And Publish

Run:

```bash
python3 scripts/validate_knowledge_package.py <workspace>
python3 /path/to/skill-creator/scripts/quick_validate.py <this-skill-directory>
```

Fix all errors. Warnings require human review and a recorded disposition. Apply the human rubric in [references/evidence-and-readability.md](references/evidence-and-readability.md): an engineer unfamiliar with the framework must be able to answer what is split, what each device owns, where communication occurs, why it is correct, what it saves, what it costs, and where source execution begins.

For every generated diagram, render the final raster at review resolution and inspect it at original size. Apply the arrow, layout, tensor-ownership, lifecycle, and evidence checks in [references/systems-diagrams.md](references/systems-diagrams.md). Do not promote a diagram whose meaning depends on accompanying prose or whose arrows, ownership snapshots, or phase transitions are ambiguous.

Diagram visual QA is a mandatory raster-level gate, not a compiler check. After every geometry, label, arrow, or node edit: render the full-resolution PNG in `_artifacts/`; inspect the whole frame at original size; crop the main flow, communication lanes, cross-rank links, ownership/timeline regions, and legend/footer into separate original-pixel QA images; inspect every crop for text-to-text overlap, text-on-line overlap, arrows crossing nodes, arrowheads landing inside boxes, unintended diagonal edges, ambiguous endpoints, and clipped content. Re-render and repeat until every crop and the whole frame pass. LaTeX/TikZ compilation success, absence of `Overfull` warnings, PDF inspection, or a scaled-down whole-image preview never constitutes visual QA. Do not report that QA passed unless the crop inspection was actually performed, and do not replace a formal asset before the user approves the `_artifacts/` review render in an iterative diagram task.

Diagram QA requires an independent reviewer. The agent that authored or edited the diagram may render it and prepare crops, but must not be the sole visual approver. When subagents are available, assign a separate QA-only subagent that does not edit files; it must inspect the current full-resolution raster and every current crop, then return severity-ordered findings. The authoring agent fixes those findings and resubmits the new raster and regenerated crops to the independent reviewer. Any geometry, label, node, or routing edit invalidates the previous review. Record the reviewer identity, reviewed render timestamp, findings disposition, and re-review status in the delivery contract. Do not claim visual QA passed from self-review alone.

Use this execution protocol for every diagram review: (1) the author renders the current source and prepares the full frame plus all named crops; (2) the author creates `_artifacts/.../diagram-qa-status.json` with `python3 <skill-root>/scripts/diagram_qa_status.py request`, then delegates the status path, request ID, exact artifact paths, diagram contract, and checklist to an independent subagent; (3) the reviewer uses the same script to `claim` the request before inspection and `complete` it with severity-ordered findings and a verdict; it does not edit source files; (4) the author reads the refreshed status file, fixes every blocking or visual finding, regenerates the full frame and every crop, and creates a new request round; (5) only the script's `verify` command succeeding for the latest request ID may close the gate. A chat response, stale status, matching filename, or prior-round `passed` is not gate evidence. If no independent subagent is available, leave the status `pending` and report the blocker; never downgrade to author self-approval.

Treat the status file as the sole main-agent/subagent coordination state. Use schema [assets/diagram-qa-status.schema.json](assets/diagram-qa-status.schema.json); use delivery-contract schema version 2 and record its path in `qa.status_file`. The main agent owns `request`; the QA subagent owns `claim` and `complete`. Both sides must use the request ID, and the main agent must read the file after subagent completion rather than infer completion from messaging. The request records the QA tool's absolute path and hash so the reviewer never searches for the updater. Tag every crop as `REGION=PATH`; the script rejects duplicate crops and any crop byte-identical to the full render. It also binds source, render, crops, and optional delivery contract SHA-256 values, updates atomically under a file lock, rejects stale request IDs, and fails verification when any artifact changed after review. Mirror the verified result into the delivery contract only as a publication snapshot; the mirror never replaces the status-file gate.

For each communication edge, the delivery contract and raster QA must additionally verify a visible shaft of non-zero length, explicit sender and receiver, payload identity, and a destination-border arrowhead. A label-only edge, a node-to-node touch with no shaft, or a line that appears to branch from an unrelated compute tensor is a failed delivery even when compilation succeeds.

The visual QA gate must also inspect composition: compare the visual weight of the primary content to the core frame, flag large one-sided empty regions, check that peer panels or lanes share a visual baseline, and verify that secondary text does not visually outweigh the primary chain. Treat centering as a perceptual balance check, not a pixel-equality test: small offsets are acceptable and must not trigger rework by themselves. A diagram fails only when its center of gravity, whitespace, or text density makes the intended hierarchy unclear.

For every visible text item, QA must identify its owner: node, edge, panel heading, legend sample, or footer. Flag isolated text with no nearby owner, labels whose nearest edge or node is ambiguous, and explanatory text that visually floats between unrelated regions. Inspect multi-line boxes for consistent line spacing, baseline alignment, and sufficient clearance from borders and arrows; a line-height collision or uneven row spacing is a visual failure even without glyph overlap.

QA must also validate semantic grouping at the panel level: headings, formulas, notes, nodes, and arrows that explain one mechanism must form one spatial group with a clear shared baseline or enclosing scope. A group that is individually readable but visually detached from the nodes it explains is a failure; treat misplaced explanatory clusters as layout defects, not merely text-placement issues.

When the user requests formal publication, invoke `$research-knowledge-publisher` and map material into existing Survey, Topic, Evidence, and Paper nodes. Do not invent a global Framework document type or change the publisher schema. Validate the process package and formal knowledge base separately.

## Required Workspace

The initializer creates:

```text
_artifacts/ai_systems_knowledge_<slug>/
├── synthesis.md
├── methods/
├── frameworks/
├── crosswalk.md
├── implementation-traces.jsonl
├── sources.jsonl
├── glossary.md
├── knowledge-package.json
├── execution_checklist.md
└── validation.json
```

Use the templates under `assets/templates/`; do not replace required files with a free-form summary. Optional recipes may be added only when the task needs them.

## Readability Rules

Treat readability as acceptance, not style polish:

- Expand each abbreviation at first use with its plain-language Chinese meaning.
- Explain a term in one ordinary-language sentence before its strict definition, tensor expression, or source symbol.
- Do not use a class name as a mechanism explanation or stack unexplained abbreviations.
- After every formula, explain every symbol and the question the formula answers.
- Describe every collective as payload, senders, receivers, and result operation: sum, concatenate, transpose, or ownership transfer.
- Explain why every core design exists and give a concrete failure example without it.
- Use tables for comparison only; keep causal explanation in prose.
- Maintain canonical terms, aliases, abbreviations, confusions, and sources in `glossary.md`; still define terms locally on first use.

The validator catches structural and obvious readability failures. Human review remains mandatory because sentence length and terminology density are warnings, not mechanical rewrite instructions.
