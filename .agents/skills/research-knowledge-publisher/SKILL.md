---
name: research-knowledge-publisher
description: Promote literature surveys, paper reviews, research syntheses, evidence indexes, and assets from process workspaces into a governed research knowledge base. Use when research outputs must be created, updated, migrated, linked, deduplicated, or validated through a skill-owned organization schema with optional repository profiles and scoped policy overlays.
---

# Research Knowledge Publisher

Publish research results into the repository knowledge graph without making process artifacts canonical.

## Required Inputs

Before editing formal knowledge:

1. Read [references/organization-model.md](references/organization-model.md).
2. Resolve [references/default-profile.json](references/default-profile.json) with an optional repository profile validated by [references/repository-profile-schema.json](references/repository-profile-schema.json).
3. Read every applicable scoped governance file and every policy document named by the resolved profile.
4. Read the resolved domain entry, existing canonical documents/indexes, figure inventory, research manifest, candidate database, and synthesis.

Read [references/knowledge-base-contract.md](references/knowledge-base-contract.md) before planning promotion. Use [references/organization-schema.json](references/organization-schema.json) for the resolved organization and [references/promotion-plan-schema.json](references/promotion-plan-schema.json) for the process-side plan.

## Workflow

### 1. Discover Ownership

- Determine `domain`, `doc_type`, stable kebab-case `slug`, and canonical owner before creating files.
- Search the repository for an existing canonical paper, model, method, topic, or asset owner.
- Prefer `update` or `link-only` over duplicate creation.
- Resolve cross-domain ownership explicitly. A model-system Paper and an infrastructure adoption record may have different canonical domains and should cross-link instead of duplicating content.

### 2. Plan Promotion

Create `<process-root>/<task>/knowledge-promotion-plan.json` before formal edits. Record:

- source process artifacts;
- target canonical paths;
- operation: `create`, `update`, `link-only`, or `no-promotion`;
- canonical owner and cross-domain references;
- required README, Survey, Paper, Evidence, and Asset links;
- affected domains and validation gates.

Validate the plan against the bundled JSON Schema when `jsonschema` is available.

### 3. Promote by Semantic Document Type

- `survey`: retain cross-paper taxonomy, comparison, trends, and engineering conclusions.
- `paper`: retain complete single-paper mechanism, formula, implementation, experiments, evidence boundary, and limitations.
- `topic`: retain stable concepts or pipelines that span papers.
- `evidence`: retain selection, indexes, provenance, counts, affiliation evidence, and figure inventory.
- `supplement`: retain final PPT/HTML only when canonical Markdown exists.
- `asset`: retain only formal, QA-passed assets under the canonical Survey or Paper owner.
- process-only kinds: retain PDFs, source snapshots, page renders, crops in progress, search caches, scripts, logs, manifests, and QA output under the resolved process root.

Bind semantic types to paths through the resolved organization; do not assume directory names.

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

Run the bundled scripts from the selected skill directory:

```bash
python3 <skill-dir>/scripts/resolve_organization.py --repo-root <repo> --start <domain>
python3 <skill-dir>/scripts/validate_research_kb.py --repo-root <repo> --domain <domain>
```

Classify every error before completion. Do not silently ignore broken links, references to the resolved process root, missing domain-entry/Paper backlinks, orphan assets, or untracked formal assets. Stage or commit only when the user requests it, and keep commits domain-isolated.

Write validation output to `<process-root>/<task>/knowledge-validation.json`. Any later formal edit requires rerunning validation.

## Completion Contract

Completion requires:

- canonical ownership and promotion actions are explicit;
- formal Markdown and assets are in their owned locations;
- README, Survey, Paper, Topic, Evidence, and Asset links satisfy repository policy;
- no formal document references the resolved process root, absolute local paths, page renders, or untracked assets;
- process artifacts remain outside the formal knowledge tree;
- the promotion plan, resolved-organization provenance, and validation result remain under the process root.
