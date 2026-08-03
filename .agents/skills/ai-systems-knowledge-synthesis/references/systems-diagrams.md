# AI Systems Diagram Contract

Use this contract for workflow, dataflow, tensor-partition, state-ownership, collective, memory-lifecycle, and parallelism diagrams. A diagram is a mechanism explanation, not decorated prose.

## Start From The Operation

- Choose the viewpoint before drawing. For training, start with `global batch -> sampler -> rank-local micro-batch -> model forward -> loss -> backward -> accumulation -> collective -> optimizer -> updated weights`. For serving, start with request admission, scheduling, model execution, cache reads/writes, communication, and token output.
- Make model or runtime execution the primary left-to-right flow. Do not organize a training diagram solely around gradients, optimizer buffers, framework classes, or collective names.
- Show only the detail required to answer: what enters, what executes, what state changes, where ranks communicate, and what proceeds to the next step.
- Use ordinary mechanism labels such as `model forward`, `gradient accumulation`, and `optimizer`. Do not hardcode an algorithm such as Adam unless the evidence and scope require that exact optimizer. Use symbols such as `S_opt` for generic optimizer state and define them locally.

## Express Time Honestly

- Draw rank-local micro-batches as an ordered queue `m_1, m_2, ..., m_K`. Route exactly one current `m_k` through forward, loss, backward, and accumulation.
- After each `m_k` backward pass, show `G_r <- G_r + g_{r,k}`. If `k < K`, loop to dequeue `m_{k+1}`. Trigger gradient synchronization and the optimizer only at the documented accumulation boundary.
- Never place multiple micro-batches in parallel lanes merely to show accumulation; that implies simultaneous execution. Use parallel lanes only for actual pipeline stages, overlap, or concurrency and label the scheduling semantics.
- Separate training, prefill, and decode diagrams when their shapes, state lifetimes, or communication frequency differ.

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
- For ZeRO-1 implementations that use reduce-scatter, show the sequence explicitly: accumulated gradient or bucket -> reduce-scatter -> rank-local gradient shard -> local optimizer update of the owned master-weight/state shard -> all-gather updated low-precision weight shards -> full model replica. Do not leave a full synchronized gradient resident after reduce-scatter. Describe `all-reduce + local slice` only as a semantic equivalence, not as an implementation trace, unless pinned source actually materializes it.
- For ZeRO-2, distinguish when gradient shards become owned and whether a full accumulation buffer exists before bucket reduction. For ZeRO-3, distinguish persistent parameter shards from temporary all-gathered parameters used for forward or backward. Resolve both from pinned source and label the snapshot phase.
- Show what ZeRO changes relative to the baseline in the workflow itself, not only in a paragraph or legend.

## Arrow And Layout Rules

- Allocate enough distance between boxes for a visible arrow shaft. A short connector must use a smaller arrowhead; the arrowhead must not consume the entire gap.
- Align centers exactly for intended horizontal or vertical connections. Do not tolerate small coordinate differences that produce accidental diagonal arrows.
- Prefer straight arrows. Use at most one orthogonal bend for a normal transition and reserve long return loops for a loop that must be understood. When a training step ends, a compact `updated weights -> next training step` terminal is clearer than routing a long arrow back through the whole diagram.
- Put forward/tensor flow, backward/gradient flow, collective flow, and sequential control in visibly distinct styles. Use color plus line style or context; never rely on color alone.
- Route arrows to node borders, not through text. Keep arrow labels off the line and away from arrowheads. Separate the `continue accumulation` path from the `synchronize and optimize` path.
- Use rounded corners only for necessary orthogonal routes. Do not add bends for decoration.
- Align peer section headings on one baseline. Keep box sizes, gaps, and fixed-format tensor cells stable so labels and arrowheads cannot shift the layout.

## Density And Legend

- Prefer a spacious 16:9 composition for workflow diagrams. Enlarge boxes and gaps before shrinking text. The diagram must remain readable when embedded at normal document width.
- Keep prose outside the diagram. Inside boxes, use a short operation name, essential tensor/state, shape or dtype, and no paragraph-length explanation.
- Use tables only for comparison outside the workflow. Do not turn the main mechanism into a dense grid of keywords.
- Build a graphical legend with actual color swatches, filled/dashed ownership cells, and arrow samples. Label each sample tersely.

## Production And Review

- Prefer deterministic diagram sources such as TikZ for technical schematics that require exact alignment, tensor cells, and orthogonal routing. Keep `.tex`, intermediate PDF, renders, and QA files in the process workspace under `_artifacts/` unless repository policy says otherwise.
- Render a PNG for review before replacing a formal asset. Inspect the PNG at original resolution; do not approve from the PDF source or a thumbnail alone.
- Iterate on one baseline diagram first, normally pure data parallelism for ZeRO comparisons. After approval, preserve its layout, visual grammar, tensor-strip scale, and arrow styles across variants so differences encode mechanism changes rather than redesign noise.
- Do not promote or publish until the user approves the review sample when the task is explicitly iterative.

## Visual QA Checklist

A diagram passes only when all answers are yes:

- Can a reader follow the main model/runtime path without reading the surrounding prose?
- Are sequential micro-batches visibly sequential rather than concurrent?
- Are world size, rank, phase, tensor shape or slice, ownership, and dtype explicit where relevant?
- Does every collective show payload and the ownership/layout after communication?
- Are intended horizontal and vertical arrows geometrically straight, with visible shafts and unambiguous endpoints?
- Are long loops, line crossings, unnecessary bends, overlapping labels, and arrows through boxes absent?
- Do ownership cells distinguish local filled slices from non-local dashed slices graphically?
- Are optimizer and runtime components generic unless a specific implementation requires a named algorithm or class?
- Are peer headings aligned and all text readable at the target embed size?
- Does the caption state the evidence level and any omitted overlap, bucketing, checkpointing, or scheduling detail?
