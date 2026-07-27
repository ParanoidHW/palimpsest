# Markdown outline to slide patterns

## Parse the outline before designing

Map the source structure without assuming a domain:

| Markdown source | Deck-plan role |
| --- | --- |
| document title | deck title or opening viewpoint |
| lead paragraph | subtitle, thesis, or speaker note |
| major heading | section and running header |
| subordinate heading | slide candidate |
| paragraph | message detail |
| bullet list | message groups, table rows, or process steps |
| image link + caption | visual source + caption |
| Markdown table | editable table candidate |
| blockquote | quote or highlighted statement |
| code block | code visual, appendix, or speaker note depending on purpose |
| `待补充` / `[TBD]` | editable placeholder |

Do not create one slide per heading mechanically. Combine or split according to meaning and readability.

## Content-driven slide count

Treat each independent viewpoint, visual object, comparison, process, or action as a candidate unit.

Combine units when they support the same title viewpoint and fit at the profile's three sizes. Split them when:

- the slide would need more than three message groups;
- two dense visuals compete;
- a table would become unreadable;
- a long process cannot be understood in one view;
- placeholders crowd out known content;
- the audience must make different decisions from different parts.

Stop when every material source item has a clear home and removing another slide would force unrelated messages together.

## Viewpoint title test

Good titles tell the audience what to take away:

- `当前方案优先解决可用性，再扩展覆盖范围`
- `三项变化共同解释了结果差异`
- `下一步先关闭两个关键缺口`

Weak titles name only a topic:

- `背景`
- `结果`
- `下一步`

If the outline provides only a topic heading, derive the title from its supporting text without adding new facts.

## Three-group discipline

A message group may contain:

```text
short message
detail
annotation
```

Use at most three groups. Move setup, citations, and secondary qualifications into a note band, caption, table, or speaker notes instead of creating a fourth group.

## Visual selection

- Use `figure` for one dominant image or chart.
- Use `table` for repeated fields and exact comparisons.
- Use `process` for dependent steps.
- Use `timeline` for state change over time.
- Use `comparison` for aligned alternatives.
- Use `two-column` only when both sides answer the same viewpoint title.
- Use `statement` when text itself is the information object.

Avoid decorative visuals that do not help the audience understand the outline.

## Placeholder pattern

Keep incomplete fields editable:

```text
【待补充】视觉对象
类型：________
标题 / caption：________
来源 / 备注：________
```

Do not replace missing content with invented examples unless the user explicitly requests sample content.
