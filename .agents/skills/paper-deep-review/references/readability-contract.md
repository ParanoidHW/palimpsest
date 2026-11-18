# Paper Review Readability Contract

Apply this contract before drafting and again as a dedicated revision pass. The target reader is technically literate but has not read the paper. Evidence accuracy and accessibility are both completion requirements.

## Narrative first, audit second

Read each paper subsection as prose before assigning it to a review field. In a private outline, record (a) what that subsection says, (b) its consequential details, and (c) why the next subsection follows. Use those transitions to choose the report's reading order. The reader-facing Paper should be continuous explanation with source-located figures and equations; the manifest, checklist and claim index are audit records, not a script for paragraphs.

Do not turn each paragraph into a short question, a stock answer and a final disclaimer. State evidence boundaries where the reader needs them, usually at the claim or experiment they qualify. Keep familiar terms such as GPU, token, target, drafter and kernel when they make the prose clearer. Define paper-specific or ambiguous terms at first use, for example whether a paper's `row` means a verification node/GEMM M-axis row or a concurrent request.

## 0. Problem-first opening

Before method acronyms, component names, and equations, make the problem observable through at least one concrete end-to-end scenario. The scenario must identify:

1. who or what is operating;
2. the input, workload, or environment;
3. what the current/prior approach does;
4. the exact step where it fails;
5. the visible quality, correctness, cost, latency, memory, or safety consequence;
6. what behavior a successful method must preserve and what it must change.

Prefer a motivating example, case study, Figure, trace, or measured failure from the paper. If the paper has no suitable example, construct the smallest useful scenario and label it “本文为便于理解所做的重构，不是论文逐字案例/实验”. Do not invent measurements, implementation details, or author intent.

The scenario must appear near the opening or in “2.1 出发点与背景痛点”, before the reader is expected to understand the proposed solution. A taxonomy, abstract paraphrase, contribution list, or table of failure labels is not a substitute. After reading the scenario alone, an unfamiliar reader should be able to answer: “What specifically goes wrong today, and what must this paper make different?”

## 1. Formula explanation card

Do not place several equations in a row and explain them only through a remote symbol table. Immediately after every key formula, answer:

1. What question does this formula answer?
2. How should a reader say it in one ordinary sentence?
3. What goes in, and what comes out?
4. What role does each variable play here?
5. What is the intuition: increasing which quantity changes what?
6. Under which assumption, approximation, unit, range, or stage is it valid?
7. Can a small paper-derived or reviewer-created example make it concrete?

These questions are an editing checklist, not seven mandatory labels. Put the displayed equation next to the passage whose logic needs it, explain its variables and implication in surrounding sentences, and use a small source-derived example when helpful. Group tightly coupled equations when one explanation covers the group. If a numerical example would mislead, omit it rather than writing a formulaic `not-applicable` sentence.

## 2. Jargon policy

Retain a specialized term only when at least one condition holds:

- the paper defines it and later reasoning depends on that exact name;
- the notation is mathematically necessary;
- it is widely used in the relevant engineering or research community.

At first use, keep the exact term and add an ordinary-language explanation. Prefer Chinese prose afterward unless the exact term prevents ambiguity.

Rewrite review-internal shorthand when it hides the conclusion:

| Avoid using alone | Prefer |
|---|---|
| `confounded` | 多项改动同时发生，无法判断是哪一项带来收益 |
| `plausible` | 机制上说得通，但论文没有直接验证 |
| `supported` | 有直接/间接证据支持，并说明证据是哪一种 |
| `frontier` | 在质量与成本之间取得的最好折中边界 |
| `proxy` | 用来间接代表目标的替代指标 |
| `telemetry` | 线上监控数据 |
| `lifecycle` | 从产生、使用到删除的完整过程 |

Do not mechanically translate paper-defined names such as model/module acronyms. Explain them once, then use the shortest unambiguous form.

## 3. “Why prior methods are insufficient”

For every central prior-method failure, include:

- the affected approach or common practice;
- an observable symptom;
- a concrete scenario;
- the root cause or ignored variable;
- why an obvious patch is insufficient;
- the evidence source and whether the scenario is paper-provided or reviewer-created.

Prefer the paper's Figure, case study, motivating example, or measured failure. If none exists, construct a small scenario and label it “本文构造的说明例，不是论文实验”.

Bad: “Uniform compression ignores heterogeneity.”

Better: “Suppose a 32-layer model removes 80% of tokens in every layer. The paper's layer probe shows early layers are more sensitive, so the same 80% cut can erase low-level audiovisual alignment before later layers use it, while later redundant layers still keep more tokens than needed. Merely lowering the global compression ratio protects early layers by spending extra compute everywhere; it does not allocate budget where it matters.”

Add a problem illustration when the scenario still requires the reader to hold three or more interacting stages or variables in working memory.

## 4. Algorithm overview

A reader-usable overview must show:

- input and output;
- the main stages in execution order;
- which objects are learned, cached, selected, merged, routed, or decoded;
- train/calibration/inference boundaries;
- the state or resource changed by each stage;
- unresolved branches or paper inconsistencies when material.

Prefer a clear original-paper overview. Otherwise generate an explanatory diagram using this fallback order:

1. `$openrouter-icu-image` with `gpt-image-2`;
2. installed `imagegen` or equivalent image-generation skill;
3. mark the delivery blocked if no reader-usable overview can be produced and no original Figure suffices.

Use the completed analysis as document input when supported. Otherwise create a short evidence-bound visual brief from cited content. Generated diagrams must be labeled as explanatory, visually inspected at full resolution, and never treated as experimental evidence.

## 4.1 Evidence-visual completeness

The final review must place every paper Figure/Table that carries method rationale, algorithm detail, ablation, mechanism evidence, or a primary result in the Markdown reading path near the claim it supports. A crop or asset that is only listed in an inventory does not count as delivery. For tables, use the complete readable figure/table or reproduce all decision-relevant rows and columns in Markdown with a source link. Mark genuinely redundant visuals explicitly in the inventory; do not silently omit them.

### Asset completeness and method prose

Every extracted crop is part of the delivery contract. The review is incomplete when a crop exists under `figures/crops/` or the formal asset owner but has no Markdown image reference and no nearby explanatory claim. Freeze only after the crop directory, figure inventory, and `analysis.md` form a one-to-one usage mapping; the validator must reject unused crops.

For the method section, a design-rationale table is an index for scanning, not a substitute for explanation. The component-rationale subsection must contain one or more plain-language paragraphs per core design (or an explicitly grouped explanation when the paper defines a coupled block). Each paragraph should answer: what would go wrong without it, what changes in the computation or system, why that could fix the concrete failure, what it costs, and what evidence supports or leaves the explanation uncertain. A table-only or label-only method discussion fails the readability gate.

## 5. Final one-glance test

Before completion, reread only these four parts as if unfamiliar with the paper:

1. the first paragraph;
2. the concrete motivating scenario;
3. “现有方案为何不够”;
4. the algorithm overview;
5. the key-formula explanation cards.

The reader should be able to state, without consulting another section:

- what breaks in the old approach;
- where the failure occurs in a concrete workflow and what consequence is visible;
- what the paper changes;
- how data/state flows through the method;
- what each key equation computes;
- what the evidence proves and does not prove.

If not, revise before setting the manifest or checklist to `passed`.

## 6. Review the actual reading path

For a qualitative audit, ask a reviewer to read the rendered report without the manifest, then trace two or three consequential claims back to the cited paper passages. Record the reviewer's identity/role, date, which report passages and source sections were checked, concrete comprehension or logical gaps found, and how they were resolved. The reviewer should be able to retell the route from observed problem to design choice to measurement, and identify the baseline/denominator for a representative gain. An empty issues list or a score is not evidence that this happened.

Machine checks may verify that source excerpts occur in the locked paper text, claim locations and images resolve, equations are paired, and a review record names the current report hash. A human must check that the cited passage actually supports the claim, the figure is read correctly, the baseline and denominator are right, and the causal explanation can be followed. No citation substring or score proves those judgments. Report structural validation and human reading judgment separately; never label a machine pass as proof of readability.
