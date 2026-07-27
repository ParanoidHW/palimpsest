---
name: outline-to-pptx
description: Create, edit, or restyle editable PowerPoint presentations from Markdown outlines, notes, source documents, tables, images, or an existing deck. Use for any request to turn an outline.md or structured content into a .pptx, as well as technical updates, project reviews, academic interpretations, training material, proposals, reports, and internal briefings. Plan with a validated deck schema, generate with PptxGenJS, preserve placeholders and source meaning, and perform rendered visual QA.
---

# Outline to PPTX

Turn a Markdown outline or other structured source into a concise, editable PowerPoint. The default visual profile is light academic editorial; the content model is domain-independent.

## Required workflow

1. Read the complete input outline and resolve its headings, paragraphs, lists, tables, image links, captions, notes, and placeholders. Do not assume a research or technical-report structure unless the input has one.
2. If a reference deck is named, extract its text and render a contact sheet before designing. Use the bundled `assets/reference-style.pptx` only when no user reference is named.
3. Read [references/style-guide.md](references/style-guide.md), [references/style-paradigms.md](references/style-paradigms.md), and [references/content-patterns.md](references/content-patterns.md).
4. Copy [references/deck-plan.example.json](references/deck-plan.example.json) into the task workspace and map the outline into it. Derive slide count from the outline's independent messages and visual objects; never target a preset page range.
5. Use [references/academic-light.style.json](references/academic-light.style.json) unless the user requests another style. Any replacement profile must conform to [references/style-profile.schema.json](references/style-profile.schema.json); the plan must conform to [references/deck-plan.schema.json](references/deck-plan.schema.json).
6. Validate before building:

   ```bash
   python3 scripts/validate-specs.py \
     --style references/academic-light.style.json \
     --plan path/to/deck-plan.json
   ```

7. Create the deck with PptxGenJS 4.x. Set `NODE_PATH="$(npm root -g)"`; do not fall back to `python-pptx` unless the user explicitly approves.
8. Start from [scripts/deck-starter.cjs](scripts/deck-starter.cjs) or import [scripts/outline-pptx-theme.cjs](scripts/outline-pptx-theme.cjs). Keep task-specific build files and the validated plan beside the task or in `_artifacts/`.
9. Preserve the source meaning and incomplete fields. Never invent missing names, dates, numbers, owners, citations, or conclusions.
10. Run content and visual QA. Prefer Microsoft PowerPoint rendering. Inspect a contact sheet and full-resolution pages, fix at least one issue found, and render again.
11. Save the final `.pptx` where the user requested. Apply repository governance only when the deliverable is declared formal.

## Markdown-to-slide mapping

- Use the document title and optional lead sentence as deck-level metadata or an opening thesis.
- Use major headings as sections and show them in the running header; do not automatically create section-divider slides.
- Treat each subordinate heading or independent message as a slide candidate.
- Turn supporting paragraphs and bullets into at most three message groups per slide. A group may contain a short message plus dense detail or annotation.
- Preserve Markdown tables as editable PowerPoint tables when practical. Split oversized tables instead of shrinking below the style minimum.
- Resolve linked images and captions. Use one dominant visual field or two major columns; do not scatter unrelated images.
- Preserve `待补充`, `待刷新`, `待归因`, `[TBD]`, and equivalent markers as editable placeholders.
- Keep source notes or speaker notes when they exist in the outline; do not require them when they do not.

## Non-negotiable presentation contract

- Use a light background on normal slides. Do not introduce a dark closing slide unless the user overrides the style profile.
- Write the viewpoint or takeaway in the title as a short sentence. Avoid topic-only titles such as “背景” or “结果”.
- Communicate no more than three key message groups per slide.
- Use `Microsoft YaHei` for Chinese and `Arial` for English. If either is unavailable, use `MiSans` consistently.
- Use no more than three font-size tokens on any slide. The default profile uses `title`, `body`, and `note`; large metrics reuse `title`.
- Render critical phrases in **bold critical red**. Do not color entire paragraphs or use red as decoration.
- Do not create repeated agenda or section-divider slides. Show section context in a compact running header.
- Keep body text at or above the profile minimum. Footers, captions, sources, and compact table notes may use the `note` size.
- Set explicit `x`, `y`, `w`, and `h` for every text box. Do not depend on auto-fit or renderer-specific wrapping.

## Content integrity

- Preserve distinctions already present in the source, such as observation, quotation, calculation, interpretation, uncertainty, or action.
- Pair a comparison with its baseline, unit, and condition when the outline provides them.
- Do not promote an intermediate or substitute indicator into a stronger conclusion.
- Keep unknown information visible as editable placeholders rather than vague prose.
- Use visuals as information objects, not decoration.

## PptxGenJS environment

```bash
export NODE_PATH="$(npm root -g)"
node path/to/build-deck.cjs output.pptx
```

The theme reads `PPTX_FONT_ZH` and `PPTX_FONT_EN`. Defaults are `Microsoft YaHei` and `Arial`. When those fonts are unavailable, set both variables to `MiSans`.

Prefer `pptx.ShapeType.*`, fresh option objects, six-character hex colors without `#`, and non-negative shadow offsets.

## QA

Run:

```bash
bash scripts/render-qa.sh output.pptx qa-output
python3 scripts/lint-pptx-style.py output.pptx \
  --style references/academic-light.style.json
python3 -m markitdown output.pptx
unzip -t output.pptx
```

`render-qa.sh` prefers Microsoft PowerPoint through Windows COM. If PowerPoint cannot be called, package and content checks do not count as layout validation. Run LibreOffice only with `--compat-libreoffice`; treat it as a secondary compatibility signal and never as the primary reason to move or resize content.

Check every PowerPoint-rendered slide for:

- a viewpoint-led title and at most three message groups;
- no more than three distinct font sizes;
- correct Chinese/English font handling;
- red emphasis always bold and limited to key phrases;
- missing glyphs, clipped titles, overflow, weak contrast, and inconsistent grids;
- preservation of outline order, tables, images, captions, notes, and placeholders.

If PowerPoint rendering is unavailable, state that visual QA remains incomplete and request a PowerPoint-side spot check for high-stakes delivery.
