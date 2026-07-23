# Survey-to-Knowledge-Base Workflow

## 1. Establish Baseline

Read governance and existing domain documents. Record:

- target domain and parent README;
- canonical Survey path and current revision/search date;
- existing Papers, Topics, Evidence, and formal assets;
- candidate cross-domain owners;
- requested survey mode and time window.

## 2. Create Process Workspace

Create `_artifacts/<task>/` for all search, review, source, render, code, QA, and manifest files. Initialize the `$ai-algorithm-survey` checklist plus knowledge-publication items.

## 3. Run Dual-Lane Discovery

### Method-first lane

Search mechanism names, aliases, venues, references, and citations. Normalize arXiv/OpenReview/venue versions to one paper identity.

### Entity-first lane

For `system-adoption` and `hybrid`, inventory model systems, organizations, technical reports, model cards, official repositories, configs, kernels, and dependency integrations. Search full text and code, not titles alone.

Classify technology role:

- `primary-contribution`
- `native-system-component`
- `optional-official-backend`
- `third-party-integration`
- `mention-only`

Keep publication and adoption count buckets separate.

## 4. Normalize Knowledge Identities

Use stable `canonical_id` values across paper, model, repository, and implementation records. Record aliases, source versions, canonical owner, existing path, and promotion action. A venue promotion updates an identity; it does not create a duplicate Paper.

## 5. Produce Change Set

Write `knowledge-change-set.json` with:

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

Use the change set to constrain formal edits.

## 6. Promote

Map stable content into Survey, Paper, Topic, Evidence, Supplement, and owned Asset nodes. Preserve the README -> Survey -> Paper -> Asset forward chain and Paper -> Survey/README backlinks. Use cross-domain relative links instead of copies.

## 7. Validate Independently

Run both validation layers:

1. `$ai-algorithm-survey` manifest/schema/semantic checks for research completeness.
2. `$research-knowledge-publisher` checks for repository integration.

A research survey may be complete while knowledge promotion is blocked, or vice versa. Report both states separately.

