# Narrative Paper Review Template

This is a writing contract, not a fixed heading list. Follow the paper's argument and choose headings that help the reader. Existing canonical Papers under schema 1.7.0 keep their frozen structure until deliberately revised. For a new or substantially revised review, create the narrative outline before filling it with claims.

## Reading before drafting

Read the paper section by section. In temporary notes, write one or two sentences for each subsection: what it says; the numbers, equations, implementation details or figures that matter; and why the next subsection follows. Identify the paper's own order and any useful change of order for a reader. Do not turn those notes into a public section inventory.

## Reader-facing structure

The skeleton below is a starting point. Rename, combine or reorder sections when the paper's causal story calls for it. Preserve source and revision information, and make every consequential result traceable.

~~~markdown
---
tags:
  - paper
  - collection/<canonical-collection>
  - domain/<owner-domain>
  - status/deep-review
  - topic/<topic>
  - method/<method>
---

# <Paper title>：<the paper's actual problem>

> Source: <paper version/PDF or URL>; review revision: <id/version/date>; owner: <domain/Paper slug>. Link the parent Survey and README when this is canonical.

## <What the prior system does and where the cost or failure appears>

Begin with a concrete source-grounded or clearly labeled reconstructed situation. Establish the input, prior workflow, visible failure, practical consequence and success constraint before the paper's terms or equations. Explain the paper's relevant background in the same reading path.

## <Why the authors chose this direction>

Show the measured or argued bottleneck and the target variable. Place the paper's equations near the decision they explain. Define paper-specific terms at first use; common GPU/ML terms need no glossary lecture. Each equation gets its local variable roles, ordinary-language meaning, assumptions and a useful example when available.

## <How the design changes as the bottleneck moves>

Explain the stages or components in an order that gives the reader a reason to continue. For each meaningful choice, say what went wrong before it, what computation/state changes, how that may help and what new cost it introduces. Insert original Figure/Table objects with full captions immediately beside the explanation they support. Trace any algorithmic agents, controller, scheduler, kernel or state ownership that the paper actually defines.

## <How the experiment tests the mechanism and the final system>

Give hardware, models, data/workload, precision, baselines, decoding mode, batch size, metric aggregation and comparison denominators before interpreting gains. Place primary tables and mechanism figures next to their claims. Distinguish offline replay, microbenchmark, ablation, development benchmark and unseen/final evaluation. State which result supports a component and which only supports the combined system.

## <What transfers and what remains open>

Describe the evidence-supported conclusion, regime changes, implementation/replication constraints and relevant related work. Put limits next to the affected conclusion instead of repeating a standard disclaimer after every paragraph.

## Sources and revision

Give a concise source list (paper version, cited Figures/Tables/sections, code revision, public review status when relevant), image inventory link and append-only revision note. This section is for finding evidence, not a second summary of the report.
~~~

## Audit beside the report

- Create the v1.8 manifest from deliverable-schema.json. Its source_map indexes consequential claims and short verbatim source excerpts rather than every paragraph; paper_source is the locked extract of the actual paper, not the review author's notes. The actual Paper remains the readable source of analysis.
- Record a rendered reading pass using narrative-review-template.md. This is a human judgment with evidence and dispositions, not an automatically computed readability grade.
- Keep the existing figure inventory, source hashes, version history, relative links and publisher gates. Report review validation and knowledge publication validation separately.
