# Paper Review Knowledge Base Integration

Apply this contract when `$research-knowledge-publisher` is available or a repository research-knowledge profile can be resolved.

## 1. Resolve Ownership Before Work

Load `$research-knowledge-publisher` and resolve its skill-owned organization plus repository profile and scoped governance. Determine:

- process root and task/paper workspace;
- stable paper identity and slug;
- candidate canonical Paper path and owning domain;
- existing Paper/version, parent Survey or Evidence index, and domain entry;
- formal Paper asset path;
- organization/default-profile/repository-profile/policy hashes.

Search the repository before creating a canonical Paper. Prefer `update` or `link-only` when the paper/model/report already has an owner in another domain.

## 2. Preserve Lifecycle Separation

The review workspace owns:

- PDF and source snapshots;
- extracted text and page renders;
- crop specifications, contact sheets, and QA output;
- code snapshots and OpenReview evidence;
- checklist, handoff, manifests, and working `analysis.md`;
- generated review diagrams and logs.

The formal knowledge base owns only:

- the stable canonical Paper Markdown projection;
- QA-passed original-paper assets under the Paper owner;
- figure inventory/evidence entries required by repository policy;
- links from domain entry and parent Survey/Index, plus Paper backlinks.

Formal Markdown must not reference the process root or process-only images.

## 3. Promotion Responsibility

### Standalone invocation

After the review manifest is frozen and valid:

1. create a publisher `knowledge-promotion-plan.json` under the process workspace;
2. create/update/link the canonical Paper and formal assets;
3. update required domain-entry, Survey/Index, Evidence, and figure-inventory links;
4. run publisher validation and store the result under the process root;
5. report review status and publication status independently.

### Delegated invocation

Do not edit survey-global or formal knowledge paths. Add compact promotion recommendations to `agent_handoff.md`:

- canonical ID/slug and suggested owner/path;
- whether an existing canonical Paper was found;
- accepted mechanism and result/system visuals eligible for promotion;
- claims suitable for Survey synthesis with exact review evidence locations;
- cross-domain links and unresolved ownership questions.

The parent Survey agent owns promotion planning, formal edits, inventory merging, and publisher validation.

## 4. Promotion Gates

- Review structural and semantic validation passed, or limitations are explicitly blocked.
- Canonical owner and operation are explicit.
- Formal Paper is a stable projection, not a copy of the entire process workspace.
- Every promoted original-paper image passed caption, crop, inventory, and individual-resolution QA.
- Domain entry and parent Survey/Index link the Paper; Paper links back as required.
- Formal files use resolvable relative links and tracked assets.
- Process and publication validation outputs remain separate.
