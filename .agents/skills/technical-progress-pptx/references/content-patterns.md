# Technical progress narrative patterns

## Content-driven slide count

Determine the page count only after building a content inventory. Treat each of these as a candidate unit:

- an independent decision or conclusion;
- the evidence required to support it;
- a material boundary that changes how the result should be interpreted;
- a distinct process, architecture, comparison, or experiment;
- an action gate with its own success criterion.

Combine units when they support the same conclusion and fit comfortably at readable type sizes. Split them when any of the following is true:

- the page would contain more than one decision-level conclusion;
- two diagrams or dense tables would compete for attention;
- body text would need to fall below 14 pt;
- a setup table exceeds roughly six substantive rows;
- measured results, paper claims, and inference cannot be visually separated;
- placeholders would crowd out the known evidence;
- the audience must make different decisions from different parts of the page.

Merge or omit a page when it contains only a repeated environment note, one minor fact, decorative context, or a conclusion already established elsewhere.

Stop adding pages when every material conclusion has evidence, boundary, and next action where applicable, and removing another page would force unrelated messages together. The final page count is an output of this process, not a target.

## Optional narrative modules

Select only the modules the content needs; do not include all of them by default:

- **Cover / thesis** — what the project is trying to turn into a real outcome.
- **Background / mechanism** — only the minimum technical context needed to understand the work.
- **Setup / evidence boundary** — model, hardware, dataset, framework, feature switches, and what is not covered.
- **Results / interpretation** — dominant metric, supporting metrics, measurement basis, and cautious meaning.
- **Training or implementation progress** — process, cost, configuration, and present quality.
- **Pending work / risks** — missing PRs, serving data, secondary branches, blockers, and placeholders.
- **Next gates** — concrete validation gates and the final decision sentence.

Cover and closing slides are optional. Use them only when the presentation context benefits from an opening thesis or deliberate conclusion.

## Slide title test

A good title states the conclusion:

- Good: `等效 TPOT 4.51 ms/token，框架内吞吐提升 2.2×`
- Weak: `推理结果`

- Good: `训练链路已打通，平均接受率仍只有 15%`
- Weak: `训练进展`

## Evidence hierarchy

Use this order:

1. Directly measured project result.
2. Measurement environment and comparison baseline.
3. Interpretation supported by the result.
4. Explicit boundary or missing validation.
5. Next experiment that closes the gap.

Do not mix paper metrics into project measurements without a label.

## Placeholder pattern

Use an editable text region with field names:

```text
【待刷新】内部 Serving
框架 / 版本：________
并发 / GBS：________
吞吐 / TPOT / P99：________
显存 / 稳定性：________
```

Do not replace missing content with vague prose.

## Metric wording

- State `相对 infer 仓 MTP-1` instead of an unlabeled `2.2×`.
- State `首 token / 平均接受率` instead of an unlabeled percentage pair.
- State `轻量框架结果，不代表真实 Serving` beside framework-only gains.
- Use `已显示性能潜力` instead of `已证明生产收益` until deployment evidence exists.
