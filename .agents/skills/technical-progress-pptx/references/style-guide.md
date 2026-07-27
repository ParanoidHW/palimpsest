# Editorial technical deck style

## Reference signature

The project reference uses a 16:9 canvas sized 17.7778 × 10 inches, MiSans typography, large editorial margins, warm off-white pages, navy text, and sparse amber/salmon accents.

## Design tokens

| Token | Hex | Use |
| --- | --- | --- |
| canvas | `FBFAF7` | Default background |
| navy | `102A43` | Primary headings, dark closing slide |
| slate | `334E68` | Body text and secondary headings |
| muted | `829AB1` | Kicker, sources, metadata, rules |
| line | `D9E2EC` | Separators and table rules |
| soft | `F1F3F5` | Quiet panels and diagram fields |
| amber | `F4C95D` | Primary accent, step numbers, highlights |
| salmon | `E98B73` | Risks and missing evidence only |
| white | `FBFAF7` | Text on dark navy |

Do not add extra hues without a content reason.

## Typography

- Preferred: `MiSans`.
- Fallback order: `Noto Sans CJK SC`, `Microsoft YaHei`, `Noto Sans`.
- Title: 40–44 pt, bold.
- Section title: 30–34 pt, bold.
- Large metric: 44–72 pt, bold.
- Subhead: 18–22 pt, bold.
- Body: 14–16 pt.
- Metadata and footer: 10–12 pt.
- Section number watermark: 72–80 pt, amber at low visual weight.

Use sentence case for English kickers. Avoid full-width tracking on Chinese body text.

## Grid and spacing

- Canvas: 17.7778 × 10.
- Outer margin: 1.05–1.20 inches.
- Content top: about 1.55 inches after kicker/title.
- Footer baseline: about 9.55 inches.
- Primary grid: 12 columns with 0.25–0.35 inch gutters.
- Minimum gap between independent blocks: 0.35 inches.
- Prefer horizontal rules over container boxes.
- Use at most one large visual field or two major columns per content slide.

## Page grammar

### Cover

- Left-aligned title and short thesis.
- One abstract mechanism visual on the right.
- Small metadata line at the bottom.
- No KPI card row unless the user explicitly requests an executive dashboard.

### Background

- Large pale section number in the upper-right.
- Two mechanism rows or one cause–effect chain.
- A single decision sentence at the bottom, led by a short amber rule.

### Setup

- Use an editorial table with thin rules.
- Put boundary language below the table.
- Avoid putting every configuration item inside a card.

### Results

- One dominant number.
- Two supporting metrics in a clean right column.
- One measurement note and one interpretation statement.
- Use a small bar or ratio diagram only when it adds meaning.

### Training/process

- Three to five numbered steps on one horizontal line.
- Configuration list below; quality metrics in a compact side column.
- Use salmon only for the main gap or risk.

### Pending work

- Split into current workstream and missing evidence.
- Preserve editable placeholders.
- Include one explicit risk statement about what remains unproven.

### Closing

- Use navy background.
- Three next gates in columns.
- End with one amber conclusion sentence.

## Visual rules

- Use circles, lines, simple blocks, and tables before icons.
- Keep shadows extremely subtle or omit them.
- Do not use gradients.
- Do not place colored accent lines directly under every title.
- Do not create a page of equal-weight rounded cards.
- Do not center paragraphs.
- Do not use more than two accent colors on one slide.

## Renderer safety

- Set explicit `x`, `y`, `w`, and `h` for every text box.
- Keep Chinese titles within one line when possible.
- Split mixed-format formulas or long metric strings into separate text boxes.
- Use fonts installed in the PowerPoint environment.
- Re-render after every font, size, or width adjustment.
- Treat Microsoft PowerPoint as the layout reference.
- Use LibreOffice only to detect secondary compatibility issues. Do not tune the primary layout against LibreOffice-specific wrapping or font substitution.
