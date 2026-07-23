---
name: research-knowledge-publisher
description: Promote literature surveys, paper reviews, research syntheses, evidence indexes, and their assets from process workspaces into this repository's governed research knowledge base. Use when research outputs must be created, updated, migrated, linked, deduplicated, or validated under the repository's README/surveys/papers/topics/evidence/supplements/assets structure while keeping PDFs, source snapshots, rendering, QA, logs, and caches in _artifacts.
---

# Research Knowledge Publisher

Publish research results into the repository knowledge graph without making process artifacts canonical.

## Required Inputs

Before editing formal knowledge, discover and read completely:

1. Every applicable `AGENTS.md` from repository root to the target domain.
2. `00_meta/research-knowledge-organization.md` when present.
3. The target domain `README.md`, existing surveys, paper index/selection, and figure inventory.
4. The research workspace manifest, candidate database, and synthesis under `_artifacts/`.

Read [references/knowledge-base-contract.md](references/knowledge-base-contract.md) before planning promotion. Use [references/promotion-plan-schema.json](references/promotion-plan-schema.json) for the process-side plan.

## Workflow

### 1. Discover Ownership

- Determine `domain`, `doc_type`, stable kebab-case `slug`, and canonical owner before creating files.
- Search the repository for an existing canonical paper, model, method, topic, or asset owner.
- Prefer `update` or `link-only` over duplicate creation.
- Resolve cross-domain ownership explicitly. A model-system paper may live under `02_model_systems` while its adoption evidence is linked from an AI-infra survey.

### 2. Plan Promotion

Create `_artifacts/<task>/knowledge-promotion-plan.json` before formal edits. Record:

- source process artifacts;
- target canonical paths;
- operation: `create`, `update`, `link-only`, or `no-promotion`;
- canonical owner and cross-domain references;
- required README, Survey, Paper, Evidence, and Asset links;
- affected domains and validation gates.

Validate the plan against the bundled JSON Schema when `jsonschema` is available.

### 3. Promote by Document Type

- `surveys/`: retain cross-paper taxonomy, comparison, trends, and engineering conclusions.
- `papers/`: retain complete single-paper mechanism, formula, implementation, experiments, evidence boundary, and limitations.
- `topics/`: retain stable concepts or pipelines that span papers.
- `evidence/`: retain selection, indexes, provenance, counts, affiliation evidence, and figure inventory.
- `supplements/`: retain final PPT/HTML only when canonical Markdown exists.
- `assets/`: retain only formal, QA-passed assets under the canonical Survey or Paper owner.
- `_artifacts/`: retain PDFs, source snapshots, page renders, crops in progress, search caches, scripts, logs, manifests, and QA output.

Do not copy full paper analysis into a Survey. Link the Survey claim to the Paper. Do not copy an asset across domains; link its canonical owner.

### 4. Build Bidirectional Links

Enforce the primary path:

```text
README -> Survey -> Paper -> Asset
   |          |         |
   +------> Topic       +-> Evidence
   +------> Evidence
```

- Index every canonical document from the domain README.
- Link major Survey claims to Paper or Evidence entries.
- Link every Paper back to README and a parent Survey or Index.
- Add the repository-standard document relationship block after the H1.

### 5. Validate and Freeze

Run:

```bash
python3 .agents/skills/research-knowledge-publisher/scripts/validate_research_kb.py \
  --repo-root . --domain <domain>
```

Classify every error before completion. Do not silently ignore broken links, forbidden `_artifacts` references, missing README/Paper backlinks, orphan assets, or untracked formal assets. Stage or commit only when the user requests it, and keep commits domain-isolated.

Write validation output to `_artifacts/<task>/knowledge-validation.json`. Any later formal edit requires rerunning validation.

## Completion Contract

Completion requires:

- canonical ownership and promotion actions are explicit;
- formal Markdown and assets are in their owned locations;
- README, Survey, Paper, Topic, Evidence, and Asset links satisfy repository policy;
- no formal document references `_artifacts`, absolute local paths, page renders, or untracked assets;
- process artifacts remain outside the formal knowledge tree;
- the promotion plan and validation result remain in `_artifacts`.

