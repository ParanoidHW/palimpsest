---
name: technical-progress-pptx
description: Create or restyle editable PowerPoint presentations for technical project progress, engineering puncture tests, model-system status, experiment results, milestone reviews, and internal technical briefings. Use when the user requests a .pptx, slides, deck, project update, 技术进展, 穿刺汇报, 训推进展, 工程复盘, or asks to follow the project's restrained editorial presentation style. Generate with PptxGenJS, preserve evidence boundaries and placeholders, and perform rendered visual QA.
---

# Technical Progress PPTX

Create concise technical progress decks using the project's editorial visual system: warm off-white, deep navy, muted slate, small amber accents, generous whitespace, and minimal card chrome.

## Required workflow

1. Inspect every source document completely enough to identify facts, metrics, uncertainties, and placeholders.
2. If a reference deck is named, extract its text and render a contact sheet before designing. Do not reuse an unrelated prior deck merely because it exists.
3. Read [references/style-guide.md](references/style-guide.md). Read [references/content-patterns.md](references/content-patterns.md) when deciding the narrative or slide types.
4. Derive the slide count from the content. Inventory the independent conclusions, evidence blocks, boundaries, and actions first; then assign one decision-level message to each slide. Do not target a preset page range.
5. Create the deck with PptxGenJS. Set `NODE_PATH="$(npm root -g)"`; do not fall back to `python-pptx` unless the user explicitly approves.
6. Start from [scripts/deck-starter.cjs](scripts/deck-starter.cjs) or import [scripts/technical-progress-theme.cjs](scripts/technical-progress-theme.cjs). Keep task-specific build files in the task workspace or `_artifacts/`.
7. Preserve incomplete information as visible, editable placeholders. Never invent missing PRs, owners, dates, results, or production claims.
8. Run content and visual QA. Prefer Microsoft PowerPoint rendering. Inspect a contact sheet and full-resolution pages, fix at least one issue found, and render again.
9. Save the final `.pptx` where the user requested. Follow repository governance only when the deliverable is declared formal.

## Design requirements

- Use the palette and typography tokens from the theme module.
- Prefer editorial grids, rules, tables, large numerals, simple process lines, and whitespace.
- Use amber for emphasis and navigation. Use salmon only for risks, missing evidence, and warnings.
- Avoid multi-color dashboards, gradients, glossy shapes, dense rounded-card grids, decorative title underlines, and generic icon collections.
- Use a dark navy closing slide only when it materially strengthens the ending.
- Keep body text at least 14 pt on the 17.78 × 10 canvas; use 11–12 pt only for sources, footers, or compact table notes.
- Keep all text boxes explicit in size. Do not depend on auto-fit or renderer-specific wrapping.
- Bold the most important phrase inside a sentence. Do not color whole paragraphs.

## Content requirements

- Lead with the outcome, then evidence, then boundary, then next gate.
- Separate measured results from paper claims and from inferred explanations.
- State the measurement environment beside every critical metric.
- Treat acceptance rate as an intermediate metric when throughput is the real objective.
- Qualify non-strict comparisons and avoid attributing whole-system gains to one component without ablation.
- Use explicit labels such as `待补充`, `待刷新`, or `待归因` for incomplete material.

## PptxGenJS environment

```bash
export NODE_PATH="$(npm root -g)"
node path/to/build-deck.cjs output.pptx
```

Use PptxGenJS 4.x. Prefer `pptx.ShapeType.*`, fresh option objects, six-character hex colors without `#`, and non-negative shadow offsets.

## QA

Run:

```bash
bash scripts/render-qa.sh output.pptx qa-output
python3 -m markitdown output.pptx
unzip -t output.pptx
```

`render-qa.sh` prefers Microsoft PowerPoint through Windows COM when available. If PowerPoint cannot be called, it still performs package and content checks but does not pretend those checks validate layout. Run LibreOffice only with `--compat-libreoffice`; treat that result as a secondary compatibility signal, never as the primary reason to move or resize content.

Check every PowerPoint-rendered slide for missing glyphs, unexpected spacing, clipped titles, overflow, overlong lines, weak contrast, inconsistent grids, and unsupported claims. If PowerPoint rendering is unavailable, state that visual QA remains incomplete and ask for a PowerPoint-side spot check for high-stakes delivery.
