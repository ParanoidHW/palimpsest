---
name: ai-algorithm-survey
description: Search, select, deep-review, and synthesize research for an AI algorithm, model-system, infrastructure, or adoption field. Use for method-first paper discovery, system-first technical-report/model-card/code discovery, top-venue and organization trends, implementation adoption, isolated $paper-deep-review agents, cross-work synthesis, presentations, and publication into a governed project knowledge base through $research-knowledge-publisher when available.
---

# AI Algorithm Survey

## Overview

Use this skill to turn a user-specified AI algorithm field into a traceable literature survey: search broadly, select the most relevant papers, delegate each selected paper to an isolated sub-agent running `$paper-deep-review`, validate its artifacts, then synthesize the technical lineage and evolution trend across the works.

Default output language is Chinese unless the user asks otherwise. Keep paper titles, method names, datasets, formulas, and code identifiers in their original language when that preserves precision.

## Project Knowledge Base Integration

When `$research-knowledge-publisher` is available or the repository contains a research-knowledge profile, read [references/knowledge-base-integration.md](references/knowledge-base-integration.md) and follow it as an additional publication contract.

- Resolve the publisher's skill-owned organization before creating the survey workspace.
- Keep search, PDF, source, render, review, code, QA, and manifest work under the resolved process root.
- Maintain canonical ownership and incremental change records before editing formal knowledge.
- Validate the survey deliverable and knowledge-base publication independently.
- Repository profiles and scoped governance bind or tighten the portable organization; do not hardcode repository paths in this skill.

## Mandatory Execution Contract

Treat this skill as a required workflow, not a set of suggestions. Once this skill is selected or explicitly invoked, every numbered workflow section and every Quality Check below is mandatory unless the user explicitly narrows the task and accepts the reduced standard.

Before starting substantive work:

- Create `execution_checklist.md` in the survey folder.
- Convert Workflow sections 1-8 and the Quality Checks into concrete checklist items.
- Mark each item as `pending`, `done`, `blocked`, or `skipped-with-reason`.
- Keep the checklist updated after each phase and before any final response.
- Put a centralized revision-information section near the top of `synthesis.md`. Record `initial` for a new survey; use `migration` for a pre-history survey, with `legacy-manifest` when the old manifest hash is known or a stable `unresolved` issue plus blocked status after failed recovery. Resolve it append-only with a later `migration-resolution` entry when the legacy manifest is recovered. For later tracked changes, increment the document version, append history, bind the superseded revision/manifest hash, and state affected locations, reason/evidence, and impact on conclusions.
- After all paper, synthesis, diagram, and optional presentation work, create `deliverable_manifest.json` conforming to `references/deliverable-schema.json`. Run Draft 2020-12 structural validation and every required `semantic_validation` cross-check. Record errors and do not declare completion when either validation fails or cannot run.

Do not silently substitute different artifacts for required outputs:

- A short summary is not a substitute for `$paper-deep-review`.
- Running all selected-paper reviews in the parent survey context is not a substitute for isolated per-paper agents when sub-agents are available.
- A generated SVG, hand-written diagram, prompt-only image, or image generated from pasted/summarized Markdown is not a substitute for Section 8.
- If `$openrouter-icu-image` is installed and `OPENROUTER_ICU_API_KEY` is available, Section 8 must produce `figures/generated/survey-trends-infra.png` from `responses-doc --input-file synthesis.md`.
- If a required tool, API key, PDF, source, code repository, or network access is unavailable, record the exact limitation in `execution_checklist.md`, the relevant report file, and the final response.

Before final response, reread `execution_checklist.md` and verify every mandatory item is either completed or explicitly blocked/skipped with evidence. Do not declare the survey complete while any mandatory item remains unclassified.

### Agent Isolation Contract

Read `references/paper-review-agent-contract.md` completely before dispatching selected papers. Treat it as the required task and acceptance contract for Section 6.

- Keep search, selection, global inventory merging, cross-paper comparison, synthesis, and final reporting in the parent survey agent.
- Start one fresh sub-agent per selected paper. Never ask one sub-agent to deep-review multiple papers.
- Use a context-free spawn such as `fork_turns="none"` when supported. Pass only the single-paper task packet defined in the contract; do not pass the conversation transcript, full candidate database, other paper analyses, or the parent's evolving synthesis.
- Require every paper agent to load and follow `$paper-deep-review`. An agent prompt alone is not a substitute for the skill.
- Give each paper agent exclusive write ownership of its paper folder. Paper agents must not edit survey-global files or another paper folder. The parent merges paper-local inventories and status reports after agents finish.
- Treat this as model-context isolation plus auditable write ownership, not automatic filesystem security. Use parallel paper agents only when each has an enforced write sandbox or independent worktree. Otherwise run fresh agents sequentially and compare complete pre/post file manifests outside the assigned folder. Use an OS-level read sandbox or separate workspace if source confidentiality requires enforceable read isolation.
- Do not weaken the one-paper-per-agent boundary to increase throughput.
- Judge completion from files and acceptance checks, not from the sub-agent's final message. Record dispatch provenance, protected-file hashes, artifact manifests, verdicts, and remediation in `agent_dispatch_log.md` and summarize them in `execution_checklist.md`.
- If sub-agents are unavailable, mark agent isolation as `blocked` and tell the user that in-context sequential review has weaker isolation. Continue only if the user explicitly accepts that reduced standard.

### Original-Paper Visual Evidence Contract

Treat original-paper visuals as evidence, not decoration. Apply these requirements to every selected method paper unless its PDF is unavailable or genuinely contains no usable visual:

- Target at least two original visuals: one mechanism, architecture, mask, algorithm, or system-design figure; and one result, ablation, profiling, comparison, or system-evidence figure/table. For each missing type, apply the visual-evidence skip contract independently.
- Preserve the complete original caption with every extracted crop. Include the paper title, figure/table number, PDF page number, and source URL in the surrounding Markdown.
- Crop exactly one numbered figure or table together with its full caption. Exclude page headers/footers, section headings, preceding/following body paragraphs, neighboring figures/tables, page numbers, and unrelated equations. Split adjacent figures and tables into separate files even when they appear on the same page.
- Use tight but non-destructive bounds: retain all panels, legends, axes, labels, footnotes belonging to the numbered object, and its caption; then leave only a small safety margin, normally 8-32 pixels at the stored resolution. Reject a crop when unrelated whitespace on any side exceeds 5% of that image dimension unless the whitespace is intrinsic to the figure layout.
- A whole rendered page is acceptable only when the page itself is the evidence object or cropping would remove essential cross-page context. Record that exception in the inventory.
- Create `figure_inventory.md` with one row per extracted visual and fields for paper, PDF page, figure/table number, source page dimensions, crop bounding box `(x, y, width, height)`, caption, local path, report section, linked claim, and QA status.
- When one or more crops exist, generate `figures/contact-sheet.png` after extraction and use it only for batch triage. Then inspect every selected crop individually at 100% scale for crop boundaries, unrelated context, excessive margins, readability, caption completeness, duplicates, and accidental blank pages; record both review passes in `execution_checklist.md`. If no crop exists, do not create a blank placeholder; record the precise blocker and alternative evidence.
- Embed and explain the selected visuals in the corresponding `analysis.md` and reuse the most informative visuals in `synthesis.md`. An image that is only stored on disk, listed in the inventory, or shown without analytical discussion does not count.
- For each missing visual type, add `visual-evidence-skip: <type and precise reason>` to that paper's `analysis.md`; record the exact PDF page/search evidence, attempted extraction method, alternative table/equation/text evidence, and effect on conclusions. Do not silently reduce the visual count.

For each selected method paper, build an explicit evidence loop in `analysis.md`:

```text
problem -> original-paper visual -> mechanism -> code/operator/kernel path -> claimed evidence -> limitation
```

Do not replace original-paper visuals with generated diagrams. Generated diagrams may summarize the survey, but they are not evidence for a paper's mechanism or results.

## Output Layout

Create one workspace folder per survey:

```text
ai_algorithm_survey_<field_slug>/
├── execution_checklist.md
├── deliverable_manifest.json
├── search_log.md
├── github_sources.md
├── impact_signals.md
├── paper_db.jsonl
├── selection.md
├── agent_dispatch_log.md
├── figure_inventory.md
├── figures/
│   ├── contact-sheet.png
│   └── generated/
│       └── survey-trends-infra.png
├── papers/
│   └── <year>_<short-title>/
│       ├── task_packet.yaml
│       ├── paper.pdf
│       ├── source/
│       ├── review_checklist.md
│       ├── figure_inventory.md
│       ├── agent_handoff.md
│       ├── deliverable_manifest.json
│       ├── artifact_manifest.sha256
│       ├── figures/
│       │   ├── page_png/
│       │   ├── crops/
│       │   └── contact-sheet.png
│       └── analysis.md
└── synthesis.md
```

Use `references/synthesis-template.md` when writing `synthesis.md`.

## Workflow

### 1. Scope the Field

Extract or ask for only the missing high-impact constraints:

- target algorithm field or keyword set,
- expected paper count; default to 6 selected papers when not specified,
- time window; default to no hard cutoff but include seminal, bridge, and recent work,
- domain boundaries, such as CV, NLP, robotics, generative models, optimization, systems, or multimodal learning,
- whether to include surveys, benchmarks, code repositories, or only peer-reviewed papers.

Choose and record a survey mode:

- `method`: method papers and technical lineage;
- `system-adoption`: model systems, technical reports, model cards, official code, backends, and integrations;
- `hybrid`: both lanes with separate count buckets; default for AI infrastructure and model-system trends.

Normalize the field into a compact slug, then create the output folder before searching.

Immediately after creating the folder, write the initial `execution_checklist.md` with all workflow and Quality Check items. This checklist is part of the required output.

### 2. Build Search Queries

Search must be current. Use the available internet/search tools and record exact query strings, source names, and search date in `search_log.md`.

Generate aliases before searching:

- exact user phrase,
- common abbreviations,
- related method names,
- benchmark/dataset names,
- predecessor and successor terms discovered during search.

Cover at least four source categories when possible:

- general search engine queries for broad discovery,
- GitHub repositories and `awesome-*` paper lists for actively maintained subfield collections,
- arXiv queries and arXiv IDs for preprints/source material,
- venue/proceedings queries for peer-reviewed versions.

For `system-adoption` and `hybrid`, also run an entity-first lane:

- inventory relevant organizations, model families, technical reports, model cards, official repositories, configs, kernels, and dependencies;
- search PDF/README/model-card/config/code full text rather than titles alone;
- expand functional terms such as efficient inference, long context/video, high resolution, memory efficiency, and scalable serving into mechanism and implementation terms;
- reverse-search kernel/runtime repositories for adopters and integrations;
- classify each hit as `primary-contribution`, `native-system-component`, `optional-official-backend`, `third-party-integration`, or `mention-only`.

Do not add system-adoption records to peer-reviewed paper counts. Keep technical-report, native adoption, optional backend, and third-party integration totals separate.

Use venue-focused patterns such as:

```text
"<keyword>" arxiv
"<keyword>" github awesome papers
site:github.com "<keyword>" "awesome"
site:github.com "awesome-<keyword>"
site:github.com "<keyword>" "paper list"
"<keyword>" "CVPR" OR "ICCV" OR "ECCV"
"<keyword>" "ICML" OR "ICLR" OR "NeurIPS"
"<keyword>" "AAAI"
"<keyword>" "TPAMI" OR "T-PAMI" OR "IEEE Transactions on Pattern Analysis and Machine Intelligence"
"<keyword>" "TIP" OR "IEEE Transactions on Image Processing"
"<keyword>" "IROS" OR "ICRA" OR "RA-L"
site:openreview.net "<keyword>"
site:proceedings.mlr.press "<keyword>"
site:papers.nips.cc "<keyword>"
site:openaccess.thecvf.com "<keyword>"
site:ojs.aaai.org "<keyword>"
site:ieeexplore.ieee.org "<keyword>"
```

For NLP, data mining, graphics, systems, or theory topics, add the appropriate venues, such as ACL, EMNLP, NAACL, KDD, SIGIR, SIGGRAPH, MLSys, OSDI, SOSP, JMLR, IJCV, TNNLS, or COLT.

For GitHub/awesome sources:

- Search for repositories named `awesome-<topic>`, `<topic>-papers`, `<topic>-survey`, `<topic>-reading-list`, and `<topic>-resources`.
- Prefer repositories with recent commits, maintained paper tables, venue/year fields, links to arXiv/OpenReview/proceedings, or taxonomy sections.
- Record useful repositories in `github_sources.md` with repo URL, owner, stars, forks, open issues or PR activity if visible, last update signal, accessed date, relevant sections, and what papers or subfields were discovered there.
- Treat GitHub lists as discovery sources, not authority. Verify each selected paper against arXiv, proceedings, OpenReview, journal pages, or the paper PDF before deep review.

### 3. Collect Impact Signals

For each serious candidate, collect lightweight popularity and value signals before final selection:

- repository popularity for official or widely used code: stars, forks, watchers if visible, recent commit/release date, issue/PR activity, license, and whether the repo is official or third-party,
- awesome/list frequency: how many GitHub lists or curated resources include the paper, and whether those lists are recently maintained,
- academic citation signal: citation count and source when visible from Google Scholar snippets, Semantic Scholar, OpenAlex, Crossref, Connected Papers, Papers with Code, publisher pages, or search results,
- cross-paper reference frequency inside the candidate set: how many other candidate/selected papers cite, compare against, benchmark against, or name the paper in related work,
- implementation adoption: whether the method has official code, multiple reimplementations, Papers with Code entries, benchmark leaderboards, or downstream libraries.

Write the signal summary to `impact_signals.md`. Always record the date and source of volatile metrics such as stars and citation counts. Treat all metrics as approximate unless obtained from a primary or API-backed source.

### 4. Normalize the Candidate Database

Write every serious candidate to `paper_db.jsonl`. Use one JSON object per paper:

```json
{
  "title": "...",
  "year": 2025,
  "venue": "ICLR",
  "authors": ["..."],
  "affiliations": ["University A", "Company B"],
  "affiliation_evidence": "paper first page / author block / OpenReview / project page / unknown",
  "paper_url": "https://...",
  "pdf_url": "https://...",
  "arxiv_id": "2501.00000",
  "code_url": "https://github.com/...",
  "repo_metrics": {
    "stars": 0,
    "forks": 0,
    "recent_update": "2026-07-05",
    "official": true,
    "evidence": "GitHub page accessed 2026-07-05"
  },
  "citation_metrics": {
    "count": 0,
    "source": "Semantic Scholar / Google Scholar snippet / OpenAlex / unknown",
    "accessed": "2026-07-05"
  },
  "cross_reference_count": 0,
  "cross_reference_evidence": ["cited by candidate paper X related work", "benchmarked by paper Y"],
  "awesome_list_count": 0,
  "source": ["arXiv", "OpenReview", "GitHub awesome list"],
  "github_discovery_source": "https://github.com/owner/awesome-topic#section",
  "value_signals": ["highly cited", "official repo widely starred", "frequently benchmarked"],
  "keywords": ["..."],
  "role": "seminal|core|bridge|variant|recent|survey|benchmark",
  "relevance_reason": "...",
  "selected": false
}
```

Deduplicate arXiv, OpenReview, proceedings, and journal entries. Prefer the peer-reviewed version for venue/year, but keep arXiv IDs and source URLs when they provide PDF or source access.

Record paper-level affiliations/organizations for every candidate when available. Extract them from the paper PDF author block, arXiv metadata, OpenReview page, proceedings page, project page, or official code README. Do not infer affiliations from author names alone. If affiliations are unavailable or ambiguous, use an empty list and set `affiliation_evidence` to `unknown` or a precise caveat.

For `system-adoption` and `hybrid`, also write `system_db.jsonl`. Use stable entity IDs across reports, model cards, repositories, checkpoints, and integrations. Record canonical organization, model/system identity, technology role, evidence level, official source locators, implementation identifiers, and links to related paper records. A model, paper, repository, and integration are related records, not interchangeable count units.

### 5. Select Papers for Deep Review

Default selection is 6 papers. Adjust only when the user asks for a different scope or the field genuinely needs a smaller/larger set.

Select papers to cover the algorithmic evolution, not just the newest results:

- one or two seminal or problem-defining works,
- one or two core method papers that established the main mechanism,
- one bridge or variant paper that changed assumptions, training data, architecture, or evaluation,
- one or two recent or high-impact papers from top venues/journals,
- optional survey/benchmark paper for taxonomy only; do not count it as a method paper unless it contains a core technical contribution.

Prioritize high-value papers when they also serve the evolution narrative. High value is not one metric; use a combined judgment from:

- academic impact: citation count, cross-reference frequency, and whether later papers use it as a baseline or taxonomy anchor,
- practical impact: official repo popularity, active maintenance, forks/reimplementations, and downstream adoption,
- conceptual impact: introduces a problem formulation, mechanism, benchmark, or evaluation protocol that later papers inherit,
- recency-adjusted impact: recent papers may have low citation counts but high GitHub/list activity or strong top-venue placement.

Do not let raw GitHub stars override paper relevance or evidence quality. Mark popularity-only papers as such if the method is not central to the field's technical lineage.

Write `selection.md` with:

- selected papers and why each was selected,
- important candidates excluded and why,
- evidence that search covered GitHub/awesome sources, arXiv, and top venues/journals relevant to the field,
- organization/university distribution of selected papers, with caveats for missing affiliations,
- high-value signal summary, including citation counts, cross-reference counts, repo popularity, and awesome/list frequency where available,
- access limitations such as paywalls, missing PDF, or blocked code.

### 6. Deep-Review Each Selected Paper

For every selected paper, delegate a single-paper task under `references/paper-review-agent-contract.md`. The paper agent must use `$paper-deep-review` and follow its complete workflow. Do not replace the deep review with a short abstract summary or perform the batch inside the parent context.

The one-paper-per-agent contract applies to selected method papers and technical reports chosen for mechanism-level analysis. Adoption-only code/config/backend records do not require a paper review unless they are promoted into the selected deep-review set; they still require source and implementation evidence in the parent survey database.

Before dispatch:

- create `papers/<year>_<short-title>/`, assign it to exactly one paper agent, and record a unique `dispatch_id`, runtime agent task/id, context-free spawn mode, and filesystem-isolation mode in `agent_dispatch_log.md`,
- write the exact minimal task packet to parent-owned `task_packet.yaml` with metadata, role, URLs, known local inputs, verification questions, output folder, acceptance-contract path/hash, and the exact repository `$paper-deep-review` directory/tree hash; record the packet hash and do not allow the paper agent to modify it,
- with an enforced per-agent write sandbox/worktree, record its boundary and permit parallel dispatch; otherwise dispatch sequentially and snapshot every file path/hash outside the assigned paper folder before and after the run,
- ensure no two active agents own the same paper folder and no paper agent is asked to edit survey-global files.

Each paper agent must:

- create and maintain `review_checklist.md`, then acquire PDF/source/code when available,
- render relevant PDF pages and extract visuals under `figures/crops/` according to the Original-Paper Visual Evidence Contract,
- inspect each caption and surrounding paper text before using a visual, but exclude that surrounding body text from the crop,
- record source-page dimensions and the exact crop bounding box, maintain paper-local `figure_inventory.md`, and when crops exist use the contact sheet for triage plus inspect every crop individually at 100% scale; otherwise record the precise visual blocker without a blank placeholder,
- write `analysis.md`, embedding and discussing every accepted mechanism/evidence visual next to the corresponding explanation; target both required types and document the complete skip evidence for each missing type,
- include paper revision version/ID in the handoff and paper manifest, preserving prior revision history when remediating an existing paper delivery,
- place paper-specific terminology and symbols in one centralized `analysis.md` chapter, with sources and ambiguity notes; explicitly mark symbols not applicable when appropriate,
- analyze why every core design was chosen, what concrete problem it targets, and how it could solve that problem; distinguish author-stated rationale from inference/not-stated and check the rationale against ablations or other evidence,
- trace implementation claims to source code, operator APIs, kernel code, or an explicitly labeled inference,
- complete the `problem -> original-paper visual -> mechanism -> code/operator/kernel path -> claimed evidence -> limitation` loop,
- preserve paper/source/code URLs and commit hashes when code is inspected,
- write `agent_handoff.md` using the contract schema, with every incomplete requirement classified as blocked or skipped-with-reason,
- write and validate `deliverable_manifest.json` against the repository `$paper-deep-review` deliverable schema,
- generate `artifact_manifest.sha256` last for all files in the assigned folder except the hash manifest itself; it must include the unchanged `task_packet.yaml` and validated `deliverable_manifest.json`.

If `$paper-deep-review` is unavailable, stop and tell the user it must be installed or provided before the batch survey can meet the requested standard.

After each paper agent finishes, validate the folder against the acceptance contract before accepting it. Recompute the task-packet, skill-tree, and contract hashes; verify `artifact_manifest.sha256`; and compare the enforced sandbox/worktree result or complete out-of-root pre/post manifests. Record the deterministic verdict (`accepted`, `accepted-with-limitations`, or `rejected`) in `agent_dispatch_log.md`. Update `execution_checklist.md` with the dispatch/agent identity, paper folder, `analysis.md` and `agent_handoff.md` paths, whether PDF/source/code were acquired, extracted visual count and types, paper-local inventory/contact-sheet status, evidence-loop status, failed acceptance checks, remediation, and any `$paper-deep-review` limitations.

After all paper reviews, merge paper-local inventories into survey-level `figure_inventory.md`. If accepted crops exist, generate and inspect `figures/contact-sheet.png` and update every row's QA status; if no accepted crop exists, do not create a blank placeholder and record the precise no-crop evidence in the inventory and checklist. Read each compact `agent_handoff.md` first; load only the cited sections of `analysis.md`, figures, code paths, or source material needed for cross-paper verification and synthesis.

### 7. Synthesize the Field

After all selected papers have `analysis.md`, write `synthesis.md` from the deep-review outputs and original paper metadata.

Include:

- search scope and selection criteria,
- one centralized revision-information section with current version/revision ID and append-only history,
- GitHub/awesome repositories used as discovery sources and what they contributed,
- high-heat/high-value paper ranking with evidence, separating academic citations, cross-paper references, GitHub popularity, and conceptual importance,
- timeline of the selected works,
- affiliation/organization distribution across candidate and selected papers,
- taxonomy of method families,
- lineage graph or relation table showing which paper extends, replaces, critiques, or benchmarks against which earlier work,
- comparison table by problem formulation, core mechanism, data/benchmark, metrics, compute/system cost, strengths, and limitations,
- one centralized terminology-and-symbol chapter that normalizes key field terms while preserving paper-specific meanings, aliases, overloaded symbols, and source evidence; label each normalized definition as paper-stated or cross-paper synthesis and cite its canonical sources,
- evolution of assumptions, architectures, training objectives, inference procedures, and evaluation protocols,
- evolution of design rationales: which concrete failure modes or bottlenecks motivated each change, whether the papers state those motivations explicitly, which alternatives/trade-offs were available, and whether later evidence supports or revises them,
- soft/hardware infrastructure evolution, including data types, bandwidth utilization, CPU/GPU/NPU heterogeneity, kernels/operators, memory, interconnect, serving, and deployment constraints,
- trend summary: what is converging, what remains unsettled, and where the next likely research directions are,
- caveats about evidence quality, venue status, and whether claims come from paper text, code inspection, or your own inference.

For `system-adoption` and `hybrid`, separately report peer-reviewed method-paper counts, technical-report counts, native-system adoption, optional official backends, and third-party integrations. Connect them through stable identities and evidence-classified relations; never collapse them into one publication total.

For each core paper, include a compact subsection that introduces the problem, explains each core design's author-stated or inferred rationale, names the concrete problem it targets, traces why the mechanism could solve it, compares alternatives/trade-offs, walks through the accepted original mechanism visual and implementation path, cites the result/ablation/system evidence, and states the limitation. For a visual type accepted as missing under the agent verdict table, show the recorded alternative evidence and limitation instead of inventing or substituting a generated visual. Cross-paper tables and conclusions do not replace these per-paper explanations.

Do not claim a paper is the "latest" or "state of the art" unless the current search supports that statement and the search date is recorded.

### 8. Generate and Insert a Survey Diagram from the Markdown Document

After `synthesis.md` is complete, use `$openrouter-icu-image` if it is installed and `OPENROUTER_ICU_API_KEY` is available:

- The completed `synthesis.md` must be the reference document for image generation. Use `responses-doc --input-file synthesis.md` so the Markdown is uploaded as document context.
- Do not generate the diagram from prompt text alone. Do not paste the Markdown into the prompt, summarize the Markdown into the prompt, or use `/v1/images/edits` for Markdown input. If document upload through `responses-doc` cannot be used, skip image generation and state the limitation.
- Save the PNG under `figures/generated/survey-trends-infra.png`.
- Use high quality, PNG output, and a 16:9 high-resolution size such as `1792x1008` or `2048x1152` when supported; retry at `1024x1024` if high-resolution fails.
- Prompt for a shallow-gold background, flat technical infographic style, clean labels, and dense but readable layout.
- The diagram should mainly show:
  - the field's algorithm evolution timeline,
  - major method-family branches and convergence/divergence,
  - the concrete bottlenecks and design rationales that caused major branch changes, clearly separating paper-stated motivation from cross-paper inference,
  - high-value papers as anchors,
  - software infra dimensions such as data pipeline, data types/numeric formats, training framework, inference/runtime, scheduler, serving stack, kernels/operators, evaluation tooling, and reproducibility tooling,
  - hardware infra dimensions such as compute, CPU/GPU/NPU heterogeneity, accelerator type, memory capacity, memory bandwidth, effective bandwidth utilization, interconnect, storage, and deployment constraints.
- Do not invent numeric results or paper claims. Use the synthesis as source material and keep generated visuals separate from evidence tables.
- Verify the image exists, then insert a relative Markdown link near the top of `synthesis.md` after the scope section.
- Confirm the inserted image path is relative to `synthesis.md` and does not break Markdown rendering.

If `$openrouter-icu-image` or `OPENROUTER_ICU_API_KEY` is unavailable, skip generation and state the limitation in the final response.

Record the exact Section 8 outcome in `execution_checklist.md`: command path or invocation method, whether `responses-doc --input-file synthesis.md` was used, output image path, link insertion status, or the precise reason generation was skipped. Do not mark Section 8 as done for non-PNG substitutes.

After Section 8 and any requested presentation are complete, finalize the survey delivery in two passes:

1. Before hashing, finalize the revision-information section. Start new history with `initial`; bootstrap a legacy survey with `migration` and either a known legacy manifest hash or an unresolved predecessor that blocks completion. For a changed tracked survey, increment the document version, append a revision entry, and bind it to the previous revision and deliverable-manifest SHA-256.
2. Write a preliminary root `deliverable_manifest.json` from parent-accepted paper manifests and dispatch records; include the survey revision history plus each paper's current document version/revision ID, then run Draft 2020-12 validation and all semantic checks.
3. Use the preliminary result to finalize `execution_checklist.md`, then freeze every referenced global and per-paper artifact.
4. Recompute frozen artifact hashes in the deliverable manifest, rerun structural and semantic validation, and freeze the final manifest. A `passed` validation must have an empty error list. Any later change starts a new revision and requires version/revision increment, appended history, and complete re-finalization.

Semantic validation must confirm actual relative paths and hashes; the revision section matches the manifest; revision history starts with exactly one bootstrap entry (`initial` with no predecessor, or `migration` with a legacy/unresolved predecessor), uses unique IDs/versions, advances time/version, and makes every later tracked entry supersede the immediately preceding revision/version/manifest hash; every unresolved issue has at most one later `migration-resolution`, and any unresolved issue without a valid resolution forces blocked status; current version/ID equals the final entry; each paper version/revision ID matches its accepted manifest; selected-paper count equals the paper array length; paper keys/folders/dispatch IDs and runtime agent task/IDs are unique; the centralized terminology/symbol chapter matches the manifest, gives every canonical definition valid sources and a paper-stated/cross-paper-synthesis status, and reconciles accepted paper glossaries without erasing paper-specific differences; every paper entry and per-design rationale array matches its accepted paper manifest and covers all core designs; global visual totals match paper manifests plus the merged inventory; and the frozen checklist agrees with the final manifest.

## Presentation Deliverables

Apply this section whenever the user requests a PPT, slide deck, or presentation in addition to the Markdown survey:

- Use the applicable presentation skill and keep the deck editable.
- Include at least one accepted sourced original-paper visual for every core paper when available. Prefer a mechanism figure; add a result or system-evidence visual when needed. If a core paper was accepted with no usable visual, show its sourced alternative evidence and explicit limitation; do not use a generated visual as a substitute.
- Put the paper title or short citation, figure/table number, PDF page, and source in the slide or speaker notes.
- Give every core paper enough slide space to explain its problem, why the core design was chosen, the concrete issue and causal mechanism it targets, alternatives/trade-offs, implementation path, evidence, and limitation. Overview, taxonomy, and conclusion slides cannot substitute for per-paper visual slides.
- Reuse only visuals that passed the contact-sheet and inventory QA. Do not use captionless crops, unreadable screenshots, or generated diagrams as substitutes for paper evidence.
- Render the final deck and inspect every slide for image readability, clipping, overlap, citation visibility, and layout consistency. Record the result or exact blocker in `execution_checklist.md`.

## Quality Checks

Before finishing:

- Confirm `execution_checklist.md` exists, was updated after each major phase, and has no unclassified mandatory items.
- Confirm `deliverable_manifest.json` exists, conforms to `references/deliverable-schema.json`, and agrees with all global artifacts, per-paper manifests/verdicts, visual QA, agent isolation, synthesis coverage, presentation state, and limitations.
- Confirm survey `semantic_validation` passed with empty errors for artifact hashes, revision-section/history/latest-ID consistency, paper revision identity reconciliation, selected-paper count, paper and runtime-agent identity uniqueness, paper-manifest/dispatch reconciliation, per-design rationale equality/core-design coverage, visual aggregation, and frozen-checklist consistency.
- Confirm `search_log.md`, `github_sources.md`, `impact_signals.md`, `paper_db.jsonl`, `selection.md`, `agent_dispatch_log.md`, `figure_inventory.md`, each selected paper `analysis.md`, and `synthesis.md` exist; require `figures/contact-sheet.png` when accepted crops exist, otherwise require precise survey-level no-crop evidence.
- Confirm search covered general search, GitHub/awesome repositories, arXiv, and relevant top venues/journals when available.
- For `system-adoption` or `hybrid`, confirm entity-first discovery covered official reports/model cards/repositories/configs, full-text mechanism and implementation terms, and reverse kernel/runtime adopters.
- Confirm paper, technical-report, native-adoption, optional-backend, and third-party-integration count buckets remain separate.
- Confirm candidate papers record `affiliations` and `affiliation_evidence`, using explicit caveats where affiliations are unavailable.
- Confirm candidate papers record impact signals: repo metrics, citation metrics, cross-reference count/evidence, and awesome-list frequency where available.
- Confirm every selected paper has a clear role in the evolution narrative.
- Confirm each selected method paper was analyzed with `$paper-deep-review`.
- Confirm each selected paper has one unique `dispatch_id` and fresh runtime agent task/id, no agent reviewed multiple papers, and each spawn mode/verdict is recorded in `agent_dispatch_log.md`; if agents were unavailable, confirm the reduced standard was explicitly accepted by the user.
- Confirm each paper folder contains a fully classified `review_checklist.md`, paper-local `figure_inventory.md`, `agent_handoff.md`, and valid `artifact_manifest.sha256`; require inspected `figures/contact-sheet.png` when one or more crops exist, otherwise require precise visual-block evidence.
- Confirm each dispatch used an enforced write sandbox/worktree or sequential complete out-of-root pre/post manifests; any unexpected path/hash change rejects the dispatch pending reconciliation. Then merge all accepted local inventories into the global inventory.
- Confirm every selected method paper has at least one mechanism visual and one result/ablation/system-evidence visual; for each missing type, require a separate precise `visual-evidence-skip` entry with attempted extraction, alternative evidence, and effect on conclusions.
- Confirm every counted visual has a complete caption, figure/table number, PDF page, source-page dimensions, exact crop bounding box, valid local path, linked claim, report location, and reviewed QA status in `figure_inventory.md`.
- When accepted crops exist, confirm `figures/contact-sheet.png` was inspected and every selected crop was also opened individually at 100% scale; otherwise confirm precise no-crop evidence and no blank placeholder.
- Confirm each crop contains exactly one numbered figure/table and its full caption, with no page header/footer, section heading, neighboring object, unrelated body paragraph, or excessive outer margin. Reject caption clipping even when the figure body itself is intact.
- Confirm each counted visual is embedded and analytically discussed in `analysis.md` or `synthesis.md`; files that are merely present on disk do not count.
- Confirm each selected method paper completes the `problem -> original-paper visual -> mechanism -> code/operator/kernel path -> claimed evidence -> limitation` loop.
- Confirm each selected paper analyzes why its core designs were chosen, the specific problems they address, the causal mechanism, alternatives/trade-offs, and supporting evidence, while separating author-stated rationale from inference or missing rationale.
- Confirm synthesis claims cite selected papers or their `analysis.md` files; label cross-paper inferences explicitly.
- Confirm `synthesis.md` contains one centralized terminology-and-symbol chapter, defines key field terms, and preserves paper-specific usages and symbol meanings with sources even when symbols are not overloaded. Mark symbols not applicable only when every accepted paper glossary does so and the synthesis introduces no analysis-derived symbols; never invent entries.
- Confirm `synthesis.md` contains revision information matching the manifest: current version/revision ID, ordered append-only history, a valid initial or migration bootstrap, exact predecessor identity/hash for later tracked revisions, changed locations, reason/evidence, and impact on conclusions. Unresolved predecessors must use stable issue IDs, record recovery attempts, and remain blocked until a later append-only `migration-resolution` binds the recovered legacy manifest. Confirm every paper's recorded version/revision ID matches its accepted paper manifest.
- If a presentation was requested, confirm every available core-paper visual has its figure/table number and PDF page; for accepted no-visual papers, confirm sourced alternative evidence and the limitation are visible. Confirm the rendered deck passed visual QA.
- If a presentation was requested, confirm every core paper's design rationale, concrete target problem, causal mechanism, alternatives/trade-offs, and rationale evidence are visible or recorded in speaker notes with author-stated/inferred/not-stated qualification.
- If `$openrouter-icu-image` was available, confirm `synthesis.md` was passed as the `responses-doc --input-file` reference document, `figures/generated/survey-trends-infra.png` exists, and it is linked from `synthesis.md`; if unavailable or failed, state the limitation.
- Confirm no required artifact was replaced by an easier substitute unless it is explicitly marked as skipped-with-reason.
- Separate peer-reviewed versions from arXiv-only preprints.
- State missing access, blocked downloads, paywalls, unavailable code, or extraction failures in the final response.

## Resources

- `references/synthesis-template.md`: Chinese structure for the final cross-paper survey and trend synthesis.
- `references/deliverable-schema.json`: Draft 2020-12 schema for the required survey-level `deliverable_manifest.json`.
- `references/paper-review-agent-contract.md`: mandatory isolated sub-agent task packet, ownership rules, artifact schema, and parent acceptance checks for each selected paper.
- `$paper-deep-review`: required per-paper workflow and source for original-paper figures, formulas, implementation evidence, and limitations.
- `$pptx` or another applicable presentation skill: required when the user requests an editable presentation deliverable.
- `$openrouter-icu-image`: optional post-processing skill for generating a shallow-gold flat technical infographic from `synthesis.md`.
- `references/knowledge-base-integration.md`: conditional process/promotion contract when a governed research knowledge base is available.
- `$research-knowledge-publisher`: project publication skill for organization resolution, canonical ownership, promotion plans, links, assets, and knowledge-base validation.
