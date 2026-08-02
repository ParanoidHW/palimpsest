---
name: ai-systems-knowledge-synthesis
description: Build method-first, source-traceable knowledge systems for AI training, inference, parallelism, memory, and runtimes. Use for AI systems knowledge synthesis, framework source analysis, distributed training/serving implementation comparisons, method-to-code mappings, tensor/collective walkthroughs, or rewriting systems explanations to remove unexplained framework jargon. Supports Megatron Core, DeepSpeed, PyTorch FSDP/DTensor, Colossal-AI, vLLM, and SGLang without requiring a full literature survey or a fixed paper count.
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

### 4. Trace Framework Implementations

Create `frameworks/<framework>.md` from the framework template and a matching framework guide. Pin one repository commit per trace boundary.

For every material implementation claim, add a trace with all five stages:

```text
configuration -> entry API -> runtime/module -> collective -> tensor layout
```

At every hop, explain the behavior in ordinary language. Record source path, symbol, line range, evidence ID, and the input/output state. Cover process groups, model rewriting, scheduler or engine, worker/model runner, checkpoint/optimizer state, and KV cache where relevant. Explain how the implementation matches, extends, or differs from the paper mechanism.

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
