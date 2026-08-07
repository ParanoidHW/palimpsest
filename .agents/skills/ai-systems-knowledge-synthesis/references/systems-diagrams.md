# AI Systems Diagram Contract

Use this contract for workflow, dataflow, tensor-partition, state-ownership, collective, memory-lifecycle, and parallelism diagrams. A diagram is a mechanism explanation, not decorated prose.

## Contents

- Reference examples
- Operation viewpoint and semantic visual grammar
- Tensor callouts and node economy
- Time, ownership, and collective semantics
- Data parallelism and ZeRO comparisons
- Layer-level TP and EP diagrams
- Arrow, layout, density, production, and visual QA

## Reference Examples

Before drawing a data-parallelism or ZeRO workflow, inspect these PNGs at original size and reuse the matching TikZ structure where useful:

- [Pure data parallel baseline](../assets/diagram-examples/dp-training-workflow-sample.png): model-centric flow, sequential micro-batches, and full tensor ownership.
- [ZeRO-1](../assets/diagram-examples/zero1-training-workflow-sample.png): full gradient accumulation, reduce-scatter, local optimizer update, and parameter all-gather.
- [ZeRO-2](../assets/diagram-examples/zero2-training-workflow-sample.png): owner-shard gradient accumulation and micro-batch boundary control.
- [ZeRO-3](../assets/diagram-examples/zero3-training-workflow-sample.png): repeated layer scope, explicit temporary weights, asynchronous release side paths, and persistent shard ownership.
- [Tensor parallel layer](../assets/diagram-examples/tp-layer-sample.png): pre-norm attention/FFN flow, arrow-adjacent tensor callouts, distinct column/row split patterns, residual shortcuts, and rank-local weight ownership.
- [Expert parallel layer](../assets/diagram-examples/ep-layer-sample.png): one-way MoE operation chain, routed-token callouts, dispatch/return collectives, residual shortcut, and expert-weight ownership.

Use [dp-training-workflow-sample.tex](../assets/diagram-examples/dp-training-workflow-sample.tex), [zero-training-workflow-samples.tex](../assets/diagram-examples/zero-training-workflow-samples.tex), and [layer-partitioning-samples.tex](../assets/diagram-examples/layer-partitioning-samples.tex) as editable structural references. Preserve the semantic grammar, not every coordinate or phrase; adapt spacing and scope to the mechanism being explained.

## Start From The Operation

- Choose the viewpoint before drawing. For training, start with `global batch -> sampler -> rank-local micro-batch -> model forward -> loss -> backward -> accumulation -> collective -> optimizer -> updated weights`. For serving, start with request admission, scheduling, model execution, cache reads/writes, communication, and token output.
- Make model or runtime execution the primary left-to-right flow. Do not organize a training diagram solely around gradients, optimizer buffers, framework classes, or collective names.
- Show only the detail required to answer: what enters, what executes, what state changes, where ranks communicate, and what proceeds to the next step.
- Use ordinary mechanism labels such as `model forward`, `gradient accumulation`, and `optimizer`. Do not hardcode an algorithm such as Adam unless the evidence and scope require that exact optimizer. Use symbols such as `S_opt` for generic optimizer state and define them locally.
- Declare the abstraction level. A method-principle diagram must omit runtime optimizations such as buckets, ready hooks, coordinator queues, fused buffers, prefetch thresholds, and overlap cadence unless one of them is required by the method definition. Put those details in a separate framework-implementation supplement backed by pinned source.
- Use framework source to compare against the principle: confirm matching semantics, expose deviations, and explain engineering extensions. Do not let one framework's optimization redefine the principle diagram. Link each implementation supplement back to the stable method diagram and label its repository, commit, and version boundary.
- Keep a method-principle diagram framework-neutral in every visible region. Do not put framework or repository names, commits, versions, source IDs, configuration keys, class names, or code symbols in its title, subtitle, nodes, legend, footer, or caption. Record that evidence in the ledger or a separately labeled framework supplement.

## Use A Semantic Visual Grammar

- Assign every node exactly one semantic role and show the role in a graphical legend: tensor or weight, model compute, persistent rank-local state, collective, runtime action, or control decision.
- Reserve the tensor or weight style for data objects that flow or reside, such as batches, micro-batches, parameters, gradients, activations, and temporary gathered weights. A sampler, scheduler, release, reshard, cast, or optimizer invocation is not a tensor.
- Reserve the rank-local state style for data that persists on a rank across an operation or lifecycle boundary, such as an accumulation buffer, optimizer state, parameter shard, gradient shard, or KV-cache block. A release, readiness condition, or scheduling action is not state.
- Use a neutral runtime-action style for samplers and lifecycle operations. Use a solid border for an ordinary action and a dashed border or connector for an asynchronous side action; do not overload tensor or state colors merely because the action consumes that object.
- Reserve the collective style for communication operations and the compute style for actual model arithmetic. Keep colors and border semantics stable across baseline and variants.
- Default to blue for tensors or weights, green for compute, orange for collectives, purple for persistent rank-local state, and a neutral style for runtime actions or control. A color assignment follows semantic role, never visual convenience: a DP sampler is not a tensor, and async release is not persistent state.
- Use color plus border or context, and include actual graphical samples in the legend. A reader must not need to infer a node's type from its label alone.

## Use Tensor Callouts And Boxes Deliberately

- Make operation nodes the primary chain. Between input and output, prefer short tensor text beside the tensor-flow arrow instead of turning every activation, gradient, shard, or partial result into a standalone box.
- Connect an intermediate tensor label to the relevant arrow with a thin blue solid leader. Leave a visible gap between the leader endpoint and the thick main arrow, and keep the leader away from the arrowhead, node border, and other flow lines. The label and leader must read as an annotation, not a branch in the execution graph.
- Keep standalone tensor boxes for true endpoints, persistent or independently owned objects, and semantically important current objects. For example, retain a `current m_k` box when it makes sequential micro-batch execution clearer. Do not mechanically convert every tensor box into a callout.
- Keep ownership strips separate from transient-flow callouts. A strip answers what rank $r$ resides; a callout answers what tensor crosses one operation boundary.
- When removing a tensor box between two operations, redraw the transition as one complete arrow. Never join differently colored arrow segments so they appear to be one logical edge. If a collective output directly feeds compute, one complete collective-colored arrow may connect the collective to compute while an adjacent callout names the output tensor.
- Keep operation boxes terse: operation name and only indispensable local qualifiers. Move tensor names, shapes, and dtype to callouts or ownership strips when doing so reduces clutter.

## Express Time Honestly

- Draw rank-local micro-batches as an ordered queue `m_1, m_2, ..., m_K`. Route exactly one current `m_k` through forward, loss, backward, and accumulation.
- After each `m_k` backward pass, show `G_r <- G_r + g_{r,k}`. If `k < K`, loop to dequeue `m_{k+1}`. Trigger gradient synchronization and the optimizer only at the documented accumulation boundary.
- Never place multiple micro-batches in parallel lanes merely to show accumulation; that implies simultaneous execution. Use parallel lanes only for actual pipeline stages, overlap, or concurrency and label the scheduling semantics.
- Separate training, prefill, and decode diagrams when their shapes, state lifetimes, or communication frequency differ.
- When one illustrated layer represents a repeated model, enclose the layer-local operations in a dashed scope labeled `MODEL LAYERS x L` or equivalent. Place a collective inside or outside that scope according to its semantic frequency; otherwise a direct `layer l -> collective` edge falsely implies one collective per layer.

## Show Tensor Ownership Visually

- Place compact ownership strips near the relevant workflow or in one adjacent inset. Include at least model weights, gradients, and optimizer or serving state when they are material to the method.
- Represent a full tensor as `p` logical slices, for example `s_0, ..., s_r, ..., s_{p-1}`. State that these are comparison units when the baseline does not physically partition the tensor.
- Use a filled solid cell for a slice resident on the illustrated rank `r`. Use an unfilled dashed cell for a slice not resident on rank `r`. Include graphical samples of both encodings in the legend; text alone is insufficient.
- Parameterize world size as `p` and the illustrated process as rank `r in {0, ..., p-1}`. Do not hardcode world size two or use rank 0 as if it were the general case.
- Label every ownership strip with its phase. Ownership may change after accumulation, reduce-scatter, optimizer update, all-gather, prefill, or decode; do not use one timeless strip when the method changes residency over time.
- Treat weight, gradient, master-weight, optimizer-state, activation, and KV-cache ownership as distinct. Do not merge them because they share a dtype or framework buffer.
- Make dtype explicit where it affects storage or computation, such as BF16 model weights, FP32 accumulated gradients, or FP32 master weights. Verify dtype and buffer lifetime from evidence instead of assuming mixed-precision defaults.

## Draw Collectives As State Transitions

- Name the collective and show what it carries, which ranks participate, and what each rank owns afterward. The visual or adjacent label must distinguish sum, average, concatenation, transpose, broadcast, all-gather, reduce-scatter, and ownership transfer.
- For reduce-scatter, show both reduction and local-slice output. Do not draw it as an all-reduce that leaves every rank with a full gradient unless the implementation actually materializes that intermediate.
- Keep paper semantics, pinned implementation behavior, and analysis-derived simplification distinct in the caption or evidence record.

## Compare Data Parallelism And ZeRO By Phase

- Draw and approve a pure data-parallel baseline first. At the optimizer boundary, show full low-precision weights, full synchronized gradients, and full master weights plus optimizer state on every rank when that is the selected baseline.
- Keep the baseline geometry fixed across ZeRO-1/2/3. Change ownership strips, collective boxes, and short phase transitions; do not redesign each stage so extensively that visual movement hides the mechanism difference.
- For ZeRO-1 implementations that use reduce-scatter, show the sequence explicitly: accumulated full gradient -> reduce-scatter -> rank-local gradient shard -> local optimizer update of the owned master-weight/state shard -> all-gather updated low-precision weight shards -> full model replica. Do not leave a full synchronized gradient resident after reduce-scatter. Describe `all-reduce + local slice` only as a semantic equivalence, not as an implementation trace, unless pinned source actually materializes it.
- For a method-level ZeRO-2 diagram, show `local gradient contribution -> reduce-scatter -> owner-shard accumulation`; do not introduce buckets or readiness scheduling. A framework-level diagram may add those implementation details from pinned source. For ZeRO-3, distinguish persistent parameter shards from temporary all-gathered parameters used for forward or backward, and keep runtime-specific prefetch/release timing in the framework view.
- Show what ZeRO changes relative to the baseline in the workflow itself, not only in a paragraph or legend.
- In ZeRO-3, draw `parameter all-gather -> temporary full layer weight -> FWD/BWD` as a direct tensor dependency. Do not insert a prose-only readiness box. If releasing or resharding the temporary weight is non-blocking for the main training flow, draw it as a dashed runtime-action side branch rather than an inline dataflow node.

## Draw Layer-Level TP And EP Mechanisms

- Use layer granularity for tensor parallelism (TP), expert parallelism (EP), and similar intra-layer partitions. Show the core attention and FFN/MoE operation flow, then insert the partition, rank-local tensor layout, weight ownership, and collective at the exact boundary where semantics change.
- Default Transformer examples to pre-norm: place `Norm` before attention and before FFN/MoE. Write `Norm`, not `LayerNorm`, unless the scoped mechanism or evidence requires a specific normalization operator. Do not silently draw post-norm.
- Standardize symbols as $B$ samples, $S$ sequence length, $H$ hidden size, $N$ attention heads, and $D$ head dimension, with $H=ND$. In dense TP examples, keep layer input and output tensors as $[B,S,H]$; do not substitute an unexplained flattened $[T,H]$ layout. EP may introduce locally routed token counts such as $T_r$ and $N_r$, but define them in the figure before using row layouts such as $[T_r,H]$.
- For TP, show both attention and FFN paths. Distinguish column-parallel and row-parallel operations with a non-color encoding such as vertical versus horizontal striping. Show the rank-local weight shard next to each partitioned projection, including its global shape, local shape, and split axis. Show column-parallel output as a locally consumable head/hidden shard and row-parallel output as an elementwise partial that requires sum reduction rather than concatenation.
- Draw residual shortcuts as thick dashed blue paths, visually separate from thin tensor-callout leaders and the primary operation chain. Route the attention and FFN shortcuts in separate lanes so neither crosses labels or appears to enter the wrong node.
- For EP, keep one unambiguous left-to-right chain: input -> Norm -> router -> group rows by expert owner -> all-to-all dispatch -> local expert FFN -> all-to-all return -> restore/combine -> residual add -> output. Use operation or collective rectangles only; attach intermediate routed-token layouts to the arrows as tensor callouts. Show the illustrated rank's expert-weight ownership in a separate strip.
- Avoid a format that makes TP/EP intermediate tensors look like additional compute stages. The reader should see operation order first, tensor layout changes second, and ownership third.

## Draw Communication Topologies And State Transitions

- Freeze the viewpoint before drawing: a rank-local view explains one rank's compute and peer sends/receives; a global view explains ownership rotation. Do not mix both into one undifferentiated network. Record the choice in the diagram delivery contract.
- Reuse the established layer/workflow grammar: one dominant operation chain, compact tensor boxes, distinct collective nodes, and a separate ownership or time inset when needed. The primary compute chain must remain readable without following the topology inset.
- A communication edge must originate from an explicit payload or collective node, never from an unrelated compute-flow edge. State payload, sender, receiver, and post-communication result in the contract and adjacent label.
- A time/state transition is not a payload transfer: use a neutral control style for local progression and the collective style only for communication. Never let a label substitute for a missing edge.
- Show only the minimum peer context needed to answer the question. Do not draw every participant and every state transition when a peer-rank inset establishes the mechanism more clearly.

## Arrow And Layout Rules

- Allocate enough distance between boxes for a visible arrow shaft. A short connector must use a smaller arrowhead; the arrowhead must not consume the entire gap.
- Align centers exactly for intended horizontal or vertical connections. Do not tolerate small coordinate differences that produce accidental diagonal arrows.
- Prefer straight arrows. Use at most one orthogonal bend for a normal transition and reserve long return loops for a loop that must be understood. When a training step ends, a compact `updated weights -> next training step` terminal is clearer than routing a long arrow back through the whole diagram.
- Put forward/tensor flow, backward/gradient flow, collective flow, and sequential control in visibly distinct styles. Use color plus line style or context; never rely on color alone.
- Route arrows to node borders, not through text. Keep arrow labels off the line and away from arrowheads. Separate the `continue accumulation` path from the `synchronize and optimize` path.
- Give every logical transition exactly one continuous arrow with one arrowhead. Do not splice blue, orange, or other colored segments into one apparent arrow after moving or removing a tensor node.
- Use rounded corners only for necessary orthogonal routes. Do not add bends for decoration.
- Align peer section headings on one baseline. Keep box sizes, gaps, and fixed-format tensor cells stable so labels and arrowheads cannot shift the layout.
- Size operation boxes to their actual title and essential tensor lines. Avoid equal oversized boxes and decorative internal whitespace. Preserve clarity by increasing the gap between compact boxes, which creates an arrow shaft, rather than padding the boxes themselves.
- Center the occupied mechanism, not merely the outer frame. Measure the primary content bounding box and correct large one-sided empty regions; declare an intentional asymmetric inset when one is required by the method.
- Budget visible text per panel: one heading, one short subtitle, and at most two short notes. Use symbols, labels, and the legend for definitions; move rationale, caveats, and implementation prose outside the core mechanism.

## Density And Legend

- Prefer a spacious 16:9 composition for workflow diagrams. Enlarge boxes and gaps before shrinking text. The diagram must remain readable when embedded at normal document width.
- Keep vertical margins purposeful. Do not leave large empty bands above or below the mechanism merely to center a sparse flow; use the canvas for ownership strips, legends, or larger inter-node gaps that improve arrow clarity. Judge the overall visual center of gravity rather than exact pixel symmetry; a small offset is acceptable when routing or semantic grouping benefits.
- Keep prose outside the diagram. Inside boxes, use a short operation name, essential tensor/state, shape or dtype, and no paragraph-length explanation.
- Use tables only for comparison outside the workflow. Do not turn the main mechanism into a dense grid of keywords.
- Build a graphical legend with actual color swatches, filled/dashed ownership cells, and arrow samples. Label each sample tersely.

## Production And Review

- Prefer deterministic diagram sources such as TikZ for technical schematics that require exact alignment, tensor cells, and orthogonal routing. Keep `.tex`, intermediate PDF, renders, and QA files in the process workspace under `_artifacts/` unless repository policy says otherwise.
- Render a PNG for review before replacing a formal asset. Inspect the PNG at original resolution; do not approve from the PDF source or a thumbnail alone.
- Re-render after every edit that changes coordinates, node size, labels, arrows, or line routing. A previously inspected raster does not validate a later source revision.
- Iterate on one baseline diagram first, normally pure data parallelism for ZeRO comparisons. After approval, preserve its layout, visual grammar, tensor-strip scale, and arrow styles across variants so differences encode mechanism changes rather than redesign noise.
- Do not promote or publish until the user approves the review sample when the task is explicitly iterative.
- Separate authoring from visual approval. The diagram author prepares deterministic renders and crops; an independent QA-only subagent inspects them and must not edit the diagram. After any fix, regenerate all affected crops and send the new raster back to the independent reviewer.

### Mandatory Raster QA Procedure

1. Render the review PNG at the final review resolution under `_artifacts/` and verify that its timestamp is newer than the source and PDF.
2. Inspect the full PNG at original size for hierarchy, margins, density, and unused space.
3. Create original-pixel crops for every dense or independently routed region: the main operation chain, each communication lane, every cross-rank or return path, ownership/time views, and the legend/footer.
4. Inspect each crop for text-to-text overlap, text sitting on an arrow or border, arrows crossing nodes, arrowheads landing inside boxes, accidental diagonals, shared or ambiguous endpoints, clipped glyphs, and labels without a clear owning edge.
5. Inspect composition in the full frame: visual center of gravity, one-sided whitespace, alignment of peer lanes, and whether secondary labels outweigh the primary chain. Do not fail a diagram for a few pixels of offset or require mathematical centering; fail only when the offset creates a visible imbalance or weakens hierarchy.
6. Inspect text ownership and typography: every visible text item must belong to a node, edge, panel heading, legend, or footer; flag isolated labels, ambiguous nearest edges, inconsistent multi-line leading, uneven baselines, and text too close to borders or arrows.
7. Inspect semantic grouping: headings, formulas, notes, nodes, and arrows that explain one mechanism must occupy one spatial group with a shared baseline or enclosing scope. A readable but detached explanatory cluster fails QA.
8. Fix every visible defect, re-render, recreate the affected crops, and repeat both crop and whole-frame inspection. Do not reuse stale crops.
9. Record the inspected raster and crop paths in the work log or handoff. Only then may the result be described as visually checked.
10. Record the independent reviewer identity, reviewed render timestamp, severity-ordered findings, disposition for every finding, and whether the exact final raster was re-reviewed. Self-review cannot close the QA gate.

### File-Based Main/Reviewer Handshake

Use one `_artifacts/.../diagram-qa-status.json` file as the authoritative state for each diagram. Do not use chat delivery, subagent lifecycle status, or a remembered hash as the gate signal.

1. The main agent runs `<skill-root>/scripts/diagram_qa_status.py request` after rendering. Tag each crop as `REGION=PATH`. The command snapshots SHA-256 values for the QA tool, source, full raster, every crop, and optional delivery contract, rejects duplicate/full-frame pseudo-crops, writes `pending`, and returns a request ID `<round>-<render-hash-prefix>`.
2. Pass the status path and request ID to the QA-only subagent. The reviewer reads `request.qa_tool.path` from the status file and uses that exact tool to run `claim` before opening artifacts; the file becomes `reviewing` and records reviewer identity and time. Do not make the reviewer search the repository for the script.
3. The reviewer inspects exactly the artifacts in the status file. It writes findings as a JSON array with `severity`, `region`, `description`, and `resolved`, then runs `complete`. The file becomes `changes-requested`, `passed`, or `error`.
4. The main agent polls by reading the file. `pending` and `reviewing` are incomplete. `changes-requested` requires a new render and a new request round. `error` requires diagnosis and a new request. Never edit a reviewer verdict into the file manually.
5. Before promotion, the main agent runs `verify` with the latest request ID. Verification must confirm `passed`, independent reviewer ownership, matching request/render/crop hashes, unchanged current artifacts, and no unresolved findings.

Run all commands from the same repository/workspace root so repository-relative artifact paths resolve identically. Keep one status file per diagram, preserve its diagram ID, and strictly increment `review_round`; the updater rejects same-round resets and diagram reuse.

Example:

```bash
qa=_artifacts/path/diagram-qa-status.json
qa_tool=/absolute/path/to/skill/scripts/diagram_qa_status.py
request_id=$(python3 "$qa_tool" request \
  --status-file "$qa" --diagram-id example --round 1 \
  --source _artifacts/path/example.tex \
  --render _artifacts/path/example.png \
  --crop main-flow=_artifacts/path/example-main.png)

# QA subagent
python3 "$qa_tool" claim \
  --status-file "$qa" --request-id "$request_id" --reviewer qa-agent
python3 "$qa_tool" complete \
  --status-file "$qa" --request-id "$request_id" --reviewer qa-agent \
  --verdict passed --summary "all required regions passed"

# Main agent
python3 "$qa_tool" show --status-file "$qa"
python3 "$qa_tool" verify \
  --status-file "$qa" --request-id "$request_id"
```

Compiler output is supporting evidence only. Successful TikZ/LaTeX compilation, zero `Overfull` or `Underfull` warnings, a valid PDF, or inspection of a scaled-down whole-frame preview does not satisfy visual QA and must never be reported as a pass by itself.

## Visual QA Checklist

A diagram passes only when all answers are yes:

- Can a reader follow the main model/runtime path without reading the surrounding prose?
- Are sequential micro-batches visibly sequential rather than concurrent?
- Are world size, rank, phase, tensor shape or slice, ownership, and dtype explicit where relevant?
- Does every collective show payload and the ownership/layout after communication?
- Are intended horizontal and vertical arrows geometrically straight, with visible shafts and unambiguous endpoints?
- Are long loops, line crossings, unnecessary bends, overlapping labels, and arrows through boxes absent?
- At original raster size and in every required crop, are text-to-text overlap, text-on-line overlap, clipped content, and arrowheads inside nodes absent?
- Were all crops regenerated after the last geometry or routing edit, rather than inspected from an older render?
- Do ownership cells distinguish local filled slices from non-local dashed slices graphically?
- Are optimizer and runtime components generic unless a specific implementation requires a named algorithm or class?
- Are peer headings aligned and all text readable at the target embed size?
- Does the caption state the evidence level and any omitted overlap, bucketing, checkpointing, or scheduling detail?
- Does every node's visual type match what it is: data object, compute, persistent state, collective, runtime action, or decision?
- Are intermediate tensors presented as readable callouts where boxes would interrupt the operation flow, while independently meaningful current or owned tensors remain boxed?
- Does each logical edge use one continuous style and color rather than multiple segments that look spliced together?
- If a layer-local mechanism repeats, does an explicit `x L` scope make the collective frequency unambiguous?
- Is every non-blocking lifecycle action off the primary dataflow, with temporary tensors shown as explicit compute inputs?
- For TP/EP, is pre-norm explicit, normalization generic unless evidence says otherwise, $B/S/H/N/D$ notation consistent, and rank-local weight ownership visible?
- Are residual shortcuts clearly dashed and separated from tensor-callout leaders and the main operation path?
- Is the principle diagram free of visible framework names, commits, versions, configuration keys, and source symbols?
