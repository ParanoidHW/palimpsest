# Knowledge Base Integration

Use this reference when `$research-knowledge-publisher` is available or a repository research-knowledge profile can be resolved.

## 1. Resolve Before Search

Load `$research-knowledge-publisher`, resolve its built-in organization plus optional repository profile, and read profile-listed and scoped governance. Record:

- process root;
- target domain and semantic document paths;
- canonical Survey and existing Paper/Topic/Evidence nodes;
- current revision and last search date;
- cross-domain canonical owners;
- organization/default-profile/repository-profile/policy hashes.

Create the survey workspace under `<process-root>/<task>/`. Do not let formal documents depend on process paths.

## 2. Plan Promotion

Before formal edits, create `knowledge-promotion-plan.json` under the task workspace and validate it with the publisher schema. Record each stable entity's canonical ID, owner, operation (`create`, `update`, `link-only`, `no-promotion`), target semantic path, source artifacts, required links, and organization binding.

For an existing Survey, create `knowledge-change-set.json` with:

```json
{
  "new": [],
  "updated": [],
  "venue_promoted": [],
  "evidence_upgraded": [],
  "reclassified": [],
  "unchanged": [],
  "stale_claims": [],
  "affected_documents": []
}
```

Use the change set to constrain formal edits. Preserve stable slugs and update one canonical record when an arXiv/OpenReview work gains a venue version.

## 3. Separate Research and Publication

The survey workspace is the complete research record. Promote only stable knowledge:

- cross-work synthesis to the resolved Survey path;
- complete selected-paper analysis to the resolved Paper path;
- stable shared concepts to Topic;
- selection, provenance, counts, adoption records, and figure inventory to Evidence;
- final derivative presentations to Supplement when canonical Markdown exists;
- QA-passed assets to their single canonical Survey or Paper owner.

Use cross-domain relative links instead of duplicate Papers or assets.

## 4. Validate Independently

Run both gates:

1. this skill's deliverable-manifest structural and semantic validation;
2. `$research-knowledge-publisher` organization, link, owner, asset, forbidden-reference, tracking, and orphan validation.

A survey may be research-complete while publication is blocked, or publication-valid while selected-paper review remains incomplete. Report both states separately and keep their validation outputs under the process root.
