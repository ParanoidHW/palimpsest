---
name: knowledge-base-ai-survey
description: Run AI algorithm, model-system, infrastructure, or adoption-trend surveys and integrate results into a continuously maintained research knowledge base. Use for surveys that need method-first and system-first discovery, incremental updates, canonical ownership, cross-domain links, formal deliverables, and process isolation through the organization resolved by research-knowledge-publisher.
---

# Knowledge Base AI Survey

Compose research execution with governed knowledge publication.

## Required Skill Composition

1. Load and follow the available `$ai-algorithm-survey` skill for search, selection, review isolation, synthesis, evidence, and its manifest.
2. Load and follow the project `$research-knowledge-publisher` skill for canonical ownership, promotion, links, assets, and validation.
3. Resolve the publisher's skill-owned organization schema with any discovered repository profile and scoped governance. Do not require a repository-specific policy path.

Read [references/survey-kb-workflow.md](references/survey-kb-workflow.md) before creating the survey workspace.

## Survey Modes

Choose and record one mode:

- `method`: method papers and technical lineage.
- `system-adoption`: model systems, reports, code, backends, and implementation adoption.
- `hybrid`: both lanes with separate count buckets; default for AI infra and model-system surveys.

Never mix peer-reviewed method-paper counts with technical-report, native-system-adoption, optional-backend, or third-party-integration counts.

## Integrated Workflow

1. Resolve the organization, repository profile, scoped governance, target domain, existing canonical nodes, and last survey snapshot.
2. Create `<process-root>/<task>/` and the survey execution checklist.
3. Create `knowledge-promotion-plan.json` before formal files.
4. Run method-first discovery. For `system-adoption` or `hybrid`, also run entity-first discovery over official reports, model cards, repositories, configs, kernels, and dependencies.
5. Normalize papers and system entities separately; connect them with stable IDs and evidence-classified relationships.
6. Deep-review selected method papers according to `$ai-algorithm-survey`; do not require a paper review for every adoption-only repository record unless selected for deep analysis.
7. Synthesize in artifacts first. Produce a change set against existing canonical knowledge.
8. Promote only stable knowledge nodes through `$research-knowledge-publisher`.
9. Validate the survey manifest and the knowledge-base graph independently.

## Incremental Update Rule

When a canonical Survey already exists:

- use its last search date and evidence index as the baseline;
- classify records as `new`, `updated`, `venue-promoted`, `evidence-upgraded`, `reclassified`, or `unchanged`;
- update only affected Survey/Paper/Evidence sections;
- preserve stable slugs and canonical owners;
- do not create a second Paper for a later arXiv, OpenReview, or venue version.

## Required Process Artifacts

In addition to `$ai-algorithm-survey` outputs, maintain:

```text
knowledge-promotion-plan.json
knowledge-change-set.json
knowledge-validation.json
system_db.jsonl              # required for system-adoption/hybrid
source_registry.jsonl        # stable IDs and last-checked sources
```

Formal documents must never link these process files or depend on their local paths.
