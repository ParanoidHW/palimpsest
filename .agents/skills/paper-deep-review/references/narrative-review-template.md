# Narrative review record

Use this short record after reading the rendered report. It is an audit trail, not a substitute for the Paper or an automatic score. Keep it beside the review artifacts; the manifest points to it. An author self-review is allowed but must be labeled; independent reading is preferred for a publication claim about readability.

```markdown
# Narrative review — <paper key>

- Reviewer and role: <name; author self-review / independent reader / domain reviewer>
- Reviewed at: <ISO 8601 date-time>
- Source version: <paper version>
- Report revision and hash: <revision ID; SHA-256>
- Rendered copy or renderer: <command/preview and result>

## Reading path

1. <report anchor> → <paper §/Figure/Table>: what problem is visible, what changes, and why the following section belongs here.
2. <report anchor> → <paper §/Figure/Table>: how a key mechanism or formula affects the measured variable.
3. <report anchor> → <paper §/Figure/Table>: which baseline and denominator support a representative result.

For each checked claim, compare the cited source passage with the report wording, not only the location label. Include at least one formula or mechanism and one main experimental gain in these checks.

## Findings and disposition

Write one concise note for each point that caused confusion or needed re-reading: the report location, what was missing in the causal chain, the edit made, and whether the issue is resolved. If none arose, name the passages examined and what made the transitions intelligible. Do not invent a finding to fill a table.

## Judgment

<One short paragraph explaining whether an unfamiliar technical reader can retell the causal thread, and any remaining ambiguity. Do not use an ungrounded numeric readability score.>

Reading verdict: ready / revise — <reason grounded in the reading path and findings>
```
