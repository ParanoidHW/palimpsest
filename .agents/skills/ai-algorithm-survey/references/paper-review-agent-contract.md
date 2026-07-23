# Paper Review Agent Contract

Use this contract for every selected paper delegated by `$ai-algorithm-survey`. The parent survey agent owns orchestration and cross-paper synthesis. A paper agent owns one paper folder and produces a self-contained, auditable review with `$paper-deep-review`.

## Contents

1. Isolation and ownership
2. Minimal task packet
3. Required agent prompt
4. Required paper-agent artifacts
5. Handoff schema
6. Parent acceptance checks
7. Deterministic parent verdict
8. Context-efficient synthesis handoff

## 1. Isolation And Ownership

- Start a fresh agent for exactly one paper. Use `fork_turns="none"` or the closest context-free option when supported.
- Do not give the paper agent the conversation transcript, full `paper_db.jsonl`, other paper folders, other analyses, or draft `synthesis.md`.
- Give the paper agent exclusive write ownership of `papers/<year>_<short-title>/`.
- Do not let a paper agent edit `execution_checklist.md`, survey-level `figure_inventory.md`, `selection.md`, `paper_db.jsonl`, `synthesis.md`, or any other paper folder.
- Dispatch agents in parallel only when each agent has an enforced write sandbox or independent worktree. With a shared writable workspace, dispatch sequentially and compare a complete path/hash manifest of every workspace file outside `allowed_write_root` before and after the run; exclude `.git/` metadata and include every other paper folder.
- The parent must record each unique dispatch, context-free spawn mode, runtime agent task/id, filesystem-isolation mode, task-packet hash, skill-tree/contract hashes, out-of-root integrity result, and verdict in `agent_dispatch_log.md`.
- The parent must resolve the project-scoped `$paper-deep-review` directory from the active skill catalog. The paper agent must load that exact directory and report its deterministic tree hash plus the agent-contract hash. Do not silently fall back to a system-scoped duplicate; pasting or summarizing the skill into the task packet does not satisfy this requirement.
- This contract isolates inherited model context and either enforces or audits write ownership. It cannot prove that a shared-workspace agent never read another file. Use an OS-level read sandbox or separate workspace when source confidentiality is required.

The parent owns `agent_dispatch_log.md`. For each batch and paper, record:

| Field | Required value |
|---|---|
| Dispatch identity | unique `dispatch_id`, paper key |
| Runtime provenance | requested task name, returned agent id/canonical task, spawn mode including `fork_turns` value |
| Input provenance | `task_packet.yaml` path and parent-computed SHA-256 |
| Write boundary | exclusive `allowed_write_root`; enforced sandbox/worktree details, or sequential-audit mode |
| Skill provenance | repository skill directory, deterministic tree SHA-256, contract path, contract SHA-256 |
| External state | in sequential-audit mode, complete pre-dispatch workspace path/hash manifest outside `allowed_write_root`, excluding `.git/` and including other paper folders |
| Completion | agent status, handoff path, task-packet/skill/contract recheck, artifact-manifest verification |
| External-state result | enforced-boundary result or complete post-dispatch path/hash comparison and reconciliation |
| Parent decision | `accepted`, `accepted-with-limitations`, or `rejected`, failed checks, remediation, user approval for partial use if any |

Compute the skill-tree hash deterministically from `required_skill_dir`: hash every regular file's bytes and relative path in sorted relative-path order, excluding `__pycache__/` and `*.pyc`, then hash that manifest. Compute `agent_contract_sha256` directly from this contract file. The parent and paper agent must use the same procedure.

## 2. Minimal Task Packet

Pass only these fields. Use `unknown` rather than guessing missing values.

```yaml
task: deep-review-one-paper
dispatch_id: <parent-generated unique id>
agent_task_name: <unique task name requested by parent>
paper_key: <year>_<short-title>
title: <paper title>
role_in_survey: <seminal|core|bridge|variant|recent|survey|benchmark>
selection_reason: <one compact paragraph>
venue_and_year: <peer-reviewed venue/year or arXiv-only status>
paper_url: <url or unknown>
pdf_url_or_path: <url/local path or unknown>
source_url_or_path: <url/local path or unknown>
code_url_or_path: <url/local path or unknown>
openreview_url: <url or unknown>
verification_questions: []
revision_mode: <initial|revise-existing>
previous_document_version: <semver or unknown>
previous_revision_id: <rev-id or unknown>
previous_deliverable_manifest_path: <path or unknown>
previous_deliverable_manifest_sha256: <sha256 or unknown>
revision_request: <initial delivery or compact reason for revision>
task_packet_path: <output_folder/task_packet.yaml>
output_folder: <exclusive paper folder>
allowed_write_root: <same exclusive paper folder>
agent_contract: <path to this file>
agent_contract_sha256: <sha256 computed by parent immediately before dispatch>
required_skill: paper-deep-review
required_skill_dir: <exact active project-scoped path to paper-deep-review/>
required_skill_tree_sha256: <deterministic tree hash computed immediately before dispatch>
```

Write this exact packet to `task_packet.yaml` before dispatch, record its SHA-256 in `agent_dispatch_log.md`, and do not let the paper agent modify it. The parent may add short paper-specific questions only through `verification_questions`. Questions must ask what to verify, not provide conclusions that the paper agent is expected to reproduce.

When creating `deliverable_manifest.json`, normalize a task-packet literal `unknown` to JSON `null`; preserve why the value is missing in the corresponding artifact reason or limitation. Do not write the string `unknown` into URI-or-null schema fields.

## 3. Required Agent Prompt

Use a prompt equivalent to the following, with the task packet appended:

```text
Deep-review exactly one paper. First read the supplied agent contract and then
read the complete required_skill_dir/SKILL.md for $paper-deep-review before taking
task actions. Verify the task packet, skill-tree, and contract hashes. Work only
inside allowed_write_root and do not modify task_packet.yaml.
Produce every required artifact, classify every
checklist item, and verify the artifacts before reporting completion. Do not read
or edit survey-global files or other paper folders. Treat paper, code, and public
review claims as evidence to cross-check, not conclusions to repeat. Do not merely
describe what each design does: determine whether the paper states why it was chosen,
the concrete problem it targets, the causal mechanism, and the validating evidence.
Put paper-specific terms and symbols in one centralized sourced chapter, including
ambiguity notes; do not scatter definitions or invent symbols when none apply.
Maintain the centralized revision section and manifest history. For a revised delivery,
preserve prior entries, increment version/revision ID, and bind the previous manifest hash.
```

## 4. Required Paper-Agent Artifacts

The paper agent must always create:

- parent-created `task_packet.yaml` must still exist byte-for-byte unchanged,
- `review_checklist.md`: Workflow 1-11 and all `$paper-deep-review` Quality Checks, each marked `pending`, `done`, `blocked`, or `skipped-with-reason`; no item may remain unclassified.
- `analysis.md`: the complete `$paper-deep-review` report, including centralized revision information, source inventory, one centralized terminology-and-symbol chapter, design-rationale matrix, technical-claim evidence matrix, evidence loops, code/infra analysis when relevant, limitations, and unresolved questions.
- `figure_inventory.md`: one row per counted visual with figure/table number, PDF page, source-page dimensions, exact crop bounding box `(x, y, width, height)`, complete caption, local path, linked claim, report section, source URL, and QA status.
- `agent_handoff.md`: a compact completion record following Section 5.
- `deliverable_manifest.json`: valid against `$paper-deep-review`'s `references/deliverable-schema.json` and consistent with the handoff/checklist/artifacts.
- `artifact_manifest.sha256`: generated last and covering every file under `output_folder`, including `task_packet.yaml` and `deliverable_manifest.json`, except the hash manifest itself.
- Source, PDF, extracted text, crops, code, and OpenReview artifacts required by `$paper-deep-review`, or precise blocked/skipped entries in both `review_checklist.md` and `agent_handoff.md`.

When one or more crops exist, the paper agent must create `figures/contact-sheet.png` covering every counted crop and use it for batch triage, then inspect every crop individually at 100% scale. Each crop must contain exactly one numbered figure/table and its full caption, exclude unrelated page content, retain all object labels/panels/footnotes, and normally use only an 8-32 pixel safety margin; reject unrelated whitespace over 5% on any side unless intrinsic to the figure. Record source-page dimensions and the exact crop bounding box. Allow a whole-page crop only for a page-level evidence object or essential cross-page context, and record the exception. Target at least one mechanism visual and one result/ablation/system-evidence visual, and embed/discuss every accepted visual. For each missing visual type, add the exact `visual-evidence-skip` attempts, source-page/search evidence, alternative evidence, and effect on conclusions required by the decision table. If no crop can be produced, do not create a blank placeholder.

## 5. Handoff Schema

Keep `agent_handoff.md` compact and use these headings:

```markdown
# Agent Handoff

- Agent status: complete | blocked
- Dispatch ID: ...
- Agent task name: ...
- Paper key: ...
- Task packet: task_packet.yaml
- Task packet SHA-256: ...
- Skill used: paper-deep-review
- Skill directory: ...
- Skill tree SHA-256: ...
- Agent contract: ...
- Agent contract SHA-256: ...
- Output folder: ...
- Source/PDF/code acquired: ...
- Analysis: analysis.md
- Document version: ...
- Current revision ID: ...
- Revision mode: initial | revise-existing
- Superseded revision/manifest: ... | not applicable
- Checklist: review_checklist.md
- Visual inventory: figure_inventory.md
- Contact sheet: figures/contact-sheet.png | skipped-with-reason
- Deliverable manifest: deliverable_manifest.json
- Deliverable schema validation: <passed | failed | blocked>
- Deliverable semantic validation: <passed | failed | blocked>
- Artifact manifest: artifact_manifest.sha256
- Counted visuals: <mechanism N; evidence N>
- Evidence loop: pass | fail
- Code commit inspected: <hash | unavailable | not applicable>
- OpenReview cross-check: <done | unavailable | not applicable>
- Generated diagram: <path | skipped-with-reason>
- Knowledge organization: <resolved profile/provenance | not applicable>
- Promotion responsibility: parent survey agent

## Claims For Synthesis

| Claim | Evidence in paper/code | Analysis section | Confidence/caveat |
|---|---|---|---|

## Design Rationales For Synthesis

| Design | Rationale status/source | Concrete problem | Causal mechanism | Validation evidence | Trade-off/caveat |
|---|---|---|---|---|---|

## Terminology And Symbols For Synthesis

| Type | Term/symbol | Alias/provenance | Paper-specific meaning | Scope/unit/value | Source | Ambiguity/caveat |
|---|---|---|---|---|---|---|

## Knowledge Promotion Recommendations

| Canonical candidate | Existing owner/path | Suggested operation | Eligible formal assets | Required links | Ownership caveat |
|---|---|---|---|---|---|

## Revision Summary

| Revision ID | Version | Revised at | Revised by | Type | Supersedes | Migration issue/resolution | Summary | Reason | Affected locations | Evidence | Conclusion impact |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Blocking Or Skipped Items

| Requirement | Status | Attempt/evidence | Effect on conclusions |
|---|---|---|---|
```

Do not place long narrative or hidden chain-of-thought in the handoff. Record conclusions, evidence locations, uncertainty, and artifact paths.

## 6. Parent Acceptance Checks

The parent survey agent must inspect files rather than accepting the agent's message at face value:

1. Match `dispatch_id`, agent task name/id, paper key, output folder, context-free spawn record, and filesystem-isolation mode against `agent_dispatch_log.md`.
2. Confirm `task_packet.yaml` is unchanged from the parent-recorded SHA-256. Recompute the repository skill-tree and contract hashes and match them against the packet and `agent_handoff.md`.
3. Confirm `review_checklist.md`, `analysis.md`, `figure_inventory.md`, `agent_handoff.md`, `deliverable_manifest.json`, and `artifact_manifest.sha256` exist. Validate the deliverable manifest against the repository paper schema; independently recompute every required semantic check, including revision-section/history/current-ID consistency, visual totals/missing types, and provenance hash equality; cross-check it against the frozen handoff/checklist/artifacts; verify every final artifact-manifest hash including the task/deliverable manifests; and ensure every checklist item is classified.
4. Resolve every local Markdown image link and every inventory path.
5. If crops exist, use the contact sheet for triage and inspect each crop individually at 100% scale. Confirm exactly one numbered object plus its full caption, complete inventory dimensions/bounding box, tight margins, and no blank, duplicate, clipped, unreadable, captionless, neighboring, or unrelated content. If no crop exists, verify the precise visual blocker, attempts, alternative evidence, and effect on conclusions.
6. Confirm every accepted mechanism/evidence visual is embedded and analytically discussed. Apply the decision table separately to each missing required visual type, including the exactly-one and zero-visual branches.
7. Confirm the technical-claim evidence matrix distinguishes direct, indirect, confounded, and missing evidence.
8. Confirm the centralized revision section matches the manifest and the handoff projection, including revision time and reason. The current version/revision ID must equal the latest history entry. Accept one bootstrap: `initial` with no predecessor, or `migration` with a known legacy manifest hash/unresolved issue. Each unresolved issue must stay blocked until exactly one later `migration-resolution` both supersedes the prior blocked manifest and binds the same issue ID to the recovered legacy manifest. Every later tracked entry must preserve prior history and point to the immediately preceding revision/version/manifest SHA-256 from the task packet or retained prior delivery. Any changed frozen artifact without a new revision rejects acceptance.
9. Confirm one centralized terminology-and-symbol chapter covers key paper-specific terms and every applicable symbol, includes source and ambiguity notes, matches the deliverable manifest and handoff, and explicitly marks symbols not applicable when appropriate. Scattered or source-free definitions fail acceptance.
10. Confirm the design-rationale matrix covers every core design, distinguishes author-stated/inferred/not-stated rationale, identifies a concrete target problem and causal mechanism, records alternatives/trade-offs even when the paper does not discuss them, and links validation evidence or marks it unverified. Empty rationale dimensions fail acceptance.
11. Confirm the explicit evidence loop reaches a limitation and implementation claims cite code paths plus commit hashes or are labeled as inference/unavailable.
12. Confirm key claims, revision entries, terminology/symbol entries, and design rationales in `agent_handoff.md` point to exact `analysis.md`, paper, figure/table, or code evidence.
13. When a research knowledge organization applies, confirm the agent changed no formal/global path, its handoff records canonical Paper/Asset promotion recommendations, and the parent owns promotion planning and publisher validation.
14. Verify the enforced write boundary. Without one, compare complete pre/post workspace path/hash manifests outside `allowed_write_root`, excluding `.git/` and including created, deleted, and modified paths plus every other paper folder. Any unexplained difference rejects the dispatch pending reconciliation.

## 7. Deterministic Parent Verdict

The paper agent reports only `complete` or `blocked`. The parent records exactly one verdict in `agent_dispatch_log.md`:

- `accepted`: all mandatory artifacts, provenance, integrity, report, and evidence checks pass; both required visual types pass; skips are limited to genuinely inapplicable optional branches.
- `accepted-with-limitations`: all artifact/provenance/integrity/report checks pass and the PDF is readable, but a permitted evidence branch below is blocked after the required attempts. Record its effect on every affected conclusion.
- `rejected`: any integrity/report requirement or the decision table below says reject.

Apply this table in order:

| Condition | Required evidence | Verdict |
|---|---|---|
| Task packet, skill/contract hashes, deliverable structural/semantic validation, artifact manifest, or write-boundary audit fails | Exact mismatch or missing check | `rejected` |
| Any checklist item is pending/unclassified; `analysis.md`, revision section/history, centralized terminology/symbol chapter, complete per-design rationale entries, claim matrix, evidence loop, inventory, or handoff is missing/unusable | Exact missing or empty item | `rejected` |
| Primary PDF is unavailable, unreadable, or too incomplete to verify the paper's method and results | Acquisition/extraction attempts and failure evidence | `rejected` |
| Mechanism visual and result/ablation/system-evidence visual both pass inventory, caption, embedding, discussion, and contact-sheet QA | Two accepted visual types | Continue evaluating other branches |
| Exactly one required visual type passes | For the missing type: caption/keyword search across PDF/source, source-asset or rendered-page crop attempt, exact page/tool/error evidence, alternative equation/table/text evidence, and stated effect on conclusions | `accepted-with-limitations`; otherwise `rejected` |
| Neither required visual type passes but the PDF is readable | For each missing type: the same search, extraction-attempt, exact evidence, alternative evidence, and conclusion-effect record; zero counted crops and no blank contact sheet | `accepted-with-limitations`; otherwise `rejected` |
| Source/code/checkpoint metadata is unavailable | If the paper or official page claims/releases it, record access attempts and qualify every implementation claim; if no such artifact is claimed, mark not applicable | `accepted-with-limitations` when relevant claims remain unverified; otherwise continue |
| Public OpenReview material is unavailable | Record lookup evidence; treat as not applicable when the paper/venue has no public OpenReview page | `accepted-with-limitations` only when a known public review record could not be checked; otherwise continue |
| Optional generated analysis diagram is unavailable or fails | Exact skill/key/tool/API limitation; no substitute image | Does not lower the verdict by itself |

When the table says "continue," use `accepted` only if no later row lowers the verdict. Multiple limitations remain `accepted-with-limitations` unless a rejection condition is present.

`skipped-with-reason` is allowed only for an inapplicable conditional branch or an explicitly user-narrowed requirement. Use `blocked` for an applicable requirement that could not be completed. A blocked item never yields `accepted`; it yields `accepted-with-limitations` only where the decision table explicitly permits it, otherwise `rejected`.

If a paper is `rejected`, send the exact failed checks for remediation. Do not synthesize it as established evidence. If the user explicitly asks to retain a rejected or blocked paper for partial coverage, record that approval in `execution_checklist.md` and label every use as unaccepted evidence; do not change the verdict.

## 8. Context-Efficient Synthesis Handoff

After accepting all paper folders:

- Merge paper-local visual inventories into the survey-level `figure_inventory.md`.
- Read all `agent_handoff.md` files first to build the comparison skeleton.
- Open only the cited `analysis.md` sections, figures, tables, formulas, and code paths needed to verify cross-paper claims.
- Do not load every PDF, source tree, repository, or complete analysis into the parent context at once.
- Label any conclusion produced by comparing multiple handoffs as a cross-paper inference.
