# Light academic technical deck style

## Reference signature

Use a 16:9 canvas sized 17.7778 × 10 inches. Normal slides use a warm white or near-white background, dark neutral text, thin gray rules, and one critical red. The visual language should resemble a well-edited academic presentation: viewpoint, content object, interpretation, and optional notes.

The machine-readable authority is [academic-light.style.json](academic-light.style.json). This guide explains how to apply it.

## Color roles

| Role | Default | Use |
| --- | --- | --- |
| canvas | `FAFAF8` | All normal slide backgrounds |
| ink | `1D2939` | Titles and primary text |
| body | `344054` | Body text |
| muted | `667085` | Running header, metadata, sources |
| line | `D0D5DD` | Rules, table dividers, axes |
| soft | `F2F4F7` | Quiet content or placeholder fields |
| critical red | `B42318` | Bold key phrases, risks, decisive deltas |
| white | `FFFFFF` | Figure/table fields only when needed |

Do not add hues merely to distinguish blocks. Use position, rules, labels, and weight first.

## Typography

- Chinese primary: `Microsoft YaHei`.
- English primary: `Arial`.
- Fallback for either: `MiSans`.
- Default size tokens: title `34 pt`, body `17 pt`, note `11 pt`.
- Use no more than these three sizes on one slide.
- Large metrics reuse title size; subheads reuse body size; running headers, sources, captions, and footers reuse note size.
- Bold only the decisive phrase. Critical red text must also be bold.

For mixed Chinese and English in one sentence, either use explicit text runs or use `MiSans` for the whole sentence when reliable mixed-font runs would add fragility.

## Grid and spacing

- Outer margin: 1.05–1.20 inches.
- Running header baseline: about 0.55 inches.
- Viewpoint title: about 1.05–1.65 inches.
- Content field starts around 2.1 inches.
- Footer baseline: about 9.55 inches.
- Use a 12-column grid with 0.25–0.35 inch gutters.
- Keep at least 0.30 inches between independent blocks.
- Use one large content field or two major columns; avoid three equal cards.

## Page grammar

Every content slide should answer one decision-level question:

1. **Viewpoint title** — short takeaway, not a topic label.
2. **Content field** — text, figure, table, process, comparison, or other source object.
3. **Up to three message groups** — each supports the title viewpoint.
4. **Optional notes** — captions, sources, qualifications, or placeholders in note size.
5. **Running header** — section name and optional progress marker.

Standalone directory and repeated section-divider slides are disabled by default. Use the running header to show navigation.

## Critical emphasis

Use red bold for:

- the most important phrase;
- a confirmed warning or risk;
- a boundary or qualification that must not be missed;
- the exact phrase the audience should remember.

Do not color a whole bullet, paragraph, table row, or title red. Aim for one to three emphasized fragments per slide.

## Renderer safety

- Set explicit text-box geometry.
- Keep Chinese titles to one line where possible and under the profile title-length limit.
- Split mixed-format equations or long metrics into separate text boxes.
- Use fonts installed in the PowerPoint environment.
- Re-render after any font, size, or width adjustment.
- Treat Microsoft PowerPoint as the layout authority.
- Use LibreOffice only for secondary compatibility checks.
