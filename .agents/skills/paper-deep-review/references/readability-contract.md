# Paper Review Readability Contract

Apply this contract before drafting and again as a dedicated revision pass. The target reader is technically literate but has not read the paper. Evidence accuracy and accessibility are both completion requirements.

## 1. Formula explanation card

Do not place several equations in a row and explain them only through a remote symbol table. Immediately after every key formula, answer:

1. What question does this formula answer?
2. How should a reader say it in one ordinary sentence?
3. What goes in, and what comes out?
4. What role does each variable play here?
5. What is the intuition: increasing which quantity changes what?
6. Under which assumption, approximation, unit, range, or stage is it valid?
7. Can a small paper-derived or reviewer-created example make it concrete?

Use this compact pattern:

```markdown
**这条公式在算什么？** ...

**怎么读？** ...

**输入与输出。** 输入是 ...；输出是 ...

**变量在这里各做什么？** ...

**直觉。** ...

**边界。** ...

**小例子。** ...（论文示例 / 本文构造的说明例，不是论文实验）
```

The example may be `not-applicable` only when a numerical or toy example would mislead; explain why.

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

## 5. Final one-glance test

Before completion, reread only these four parts as if unfamiliar with the paper:

1. the first paragraph;
2. “现有方案为何不够”;
3. the algorithm overview;
4. the key-formula explanation cards.

The reader should be able to state, without consulting another section:

- what breaks in the old approach;
- what the paper changes;
- how data/state flows through the method;
- what each key equation computes;
- what the evidence proves and does not prove.

If not, revise before setting the manifest or checklist to `passed`.
