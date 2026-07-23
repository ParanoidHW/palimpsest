---
name: paper-deep-review
description: Rigorous academic paper and technical-report review workflow for one paper, arXiv article, OpenReview submission, PDF, LaTeX source, whitepaper, or model/system report. Produce auditable Markdown with classified checks, original figures, formulas, evidence chains, related-work and public-review analysis, infrastructure and source-code cross-checks, isolated-agent provenance, and optional promotion into a governed project knowledge base through $research-knowledge-publisher.
---

# Paper Deep Review

## Overview

Use this skill to turn a paper or technical report into a rigorous Markdown review grounded in the source document, figures/tables, related work, system implications, and implementation code when available.

## Project Knowledge Base Integration

When `$research-knowledge-publisher` is available or a repository research-knowledge profile can be resolved, read [references/knowledge-base-integration.md](references/knowledge-base-integration.md) before creating the paper folder.

- Resolve the organization and use its process root for PDF, source, render, crop, code, QA, checklist, manifest, handoff, and working `analysis.md` artifacts.
- Treat the review delivery and canonical Paper as separate lifecycle objects. Freeze and validate the review before formal promotion.
- In standalone mode, promote through `$research-knowledge-publisher` only after review validation.
- In delegated mode, do not edit Survey/global/formal knowledge; record promotion recommendations in the handoff for the parent agent.
- Keep original-paper formal assets under one canonical Paper owner and keep render/crop process files under the process root.

## Mandatory Execution Contract

Treat this skill as a required workflow rather than optional guidance.

- Review exactly one paper per invocation. In delegated runs, do not expand into a multi-paper survey.
- Before substantive analysis, copy `references/review-checklist-template.md` to `review_checklist.md` in the paper folder. Keep every Workflow and Quality Check item and mark it `pending`, `done`, `blocked`, or `skipped-with-reason`.
- Update the checklist after acquisition, extraction/visual QA, evidence analysis, code/OpenReview checks, report writing, and generated-diagram handling.
- Put a centralized revision-information section near the top of `analysis.md`. Record an `initial` entry for a new delivery. When onboarding a pre-history delivery, use `migration` with a `legacy-manifest` predecessor when its hash is known; use a stable `unresolved` issue only after documented recovery attempts and keep the delivery blocked until a later `migration-resolution` entry supplies the recovered legacy predecessor. For later tracked revisions, increment the document version, append a revision entry, identify the superseded revision/manifest hash, and state changed locations, reason/evidence, and impact on conclusions.
- Create paper-local `figure_inventory.md`; when one or more crops exist, create and inspect `figures/contact-sheet.png`. If no crop can be produced, record the precise visual blocker and alternative evidence instead of creating a blank placeholder.
- When invoked by a parent agent, read the supplied agent contract completely, respect its folder ownership and input boundaries, and write the required `agent_handoff.md`.
- In delegated runs, verify parent-owned `task_packet.yaml` and do not modify it. Verify the complete skill-tree hash and agent-contract hash before analysis.
- After all analysis and diagram work, finalize delivery with the two-pass freeze protocol below. Validate both JSON Schema structure and the manifest's required semantic checks; set the delivery to `blocked` instead of claiming completion when either validation fails or cannot run.
- Classify unavailable PDFs, source, code, reviews, model metadata, tools, API keys, and network access precisely. Do not silently weaken the workflow or substitute unsupported claims.
- Before reporting completion, reread `review_checklist.md` and verify that no mandatory item is pending or unclassified. Completion is determined by artifacts and checks, not by a prose summary.

## Workflow

1. **Create or reuse a paper folder.** Use `<paper-id>_<short-title>` when no folder exists; reuse the user-provided folder for offline papers. Under a resolved knowledge organization, treat this as a process workspace rather than the canonical Paper path. Keep materials under that folder:
   - `paper.pdf` or original PDF name
   - `task_packet.yaml` when supplied by a parent agent
   - `source/` for LaTeX/source archives when available
   - `extracted_text/`
   - `review_checklist.md`
   - `figure_inventory.md`
   - `deliverable_manifest.json`
   - `figures/page_png/`
   - `figures/crops/`
   - `figures/contact-sheet.png` when one or more crops exist
   - `figures/generated/` for optional generated analysis diagrams
   - `code/<repo-name>/`
   - `openreview_reviews.md` when public OpenReview reviews/discussion exist
   - `agent_handoff.md` when required by a parent-agent contract
   - `artifact_manifest.sha256` when required by a parent-agent contract
   - `analysis.md`

2. **Acquire source material.**
   - If the user gives a local/offline PDF, use it as the primary source and do not assume arXiv/source exists.
   - If the user gives an arXiv ID or paper URL, fetch the PDF and source archive when network access is allowed; use original LaTeX figures when available.
   - If the user gives an OpenReview URL or the paper has an OpenReview page, collect publicly visible reviews, meta-review, decision, author response/rebuttal, and public discussion when accessible. Save a concise evidence-preserving summary to `openreview_reviews.md` with URLs, forum/note IDs when visible, reviewer scores/confidence when visible, and access date.
   - If a code repo is provided, clone it into `code/`, record remote URL and commit hash, and inspect code rather than relying only on README claims.

3. **Extract text and figures.**
   - Prefer original LaTeX/vector assets if source exists.
   - If source does not exist, render PDF pages to PNG and crop figures/tables manually. Clearly state that screenshots are PDF crops, not original assets.
   - Use `scripts/extract_pdf_assets.py` for offline PDFs when PyMuPDF is available, or use Poppler tools (`pdftoppm`, `pdftocairo`) when installed.
   - Use `scripts/crop_pdf_figures.py` to batch crop figures from rendered page PNGs using a JSON crop spec, then generate a contact sheet for visual review.
   - Screenshot/crop requirements are strict:
     - Every Markdown-embedded screenshot of a Figure/Table must include its full caption. A crop without the visible `Figure`, `Fig.`, or `Table` label and caption text is incomplete and must be recropped.
     - Crop exactly one numbered figure or table together with its full caption. Split adjacent numbered objects into separate files even when they share a page.
     - Exclude page headers/footers, section headings, preceding/following body paragraphs, neighboring figures/tables, page numbers, and unrelated equations.
     - Use tight but non-destructive bounds: retain every panel, legend, axis, label, footnote, and caption belonging to the object, then leave only a small safety margin, normally 8-32 pixels at the stored resolution. Reject unrelated whitespace over 5% on any side unless intrinsic to the figure layout.
     - Use a whole rendered page only when the page itself is the evidence object or cropping would remove essential cross-page context; record that exception in `figure_inventory.md`.
     - Do not crop the caption separately from the visual unless the paper layout makes one combined crop unreadable. If split crops are unavoidable, embed the visual and caption together in adjacent Markdown and label both paths in the figure inventory.
     - Preserve enough resolution for axis labels, legends, table entries, and caption text to be readable at normal Markdown viewing width. Re-render pages at higher DPI before accepting blurry crops.
     - Name crops by source and semantic target, for example `fig3_method_caption.png` or `table2_main_results_caption.png`, so the file name signals that the caption is included.
   - For every figure embedded in Markdown, verify it includes the intended plot/table and full caption/title, has narrow clean boundaries, and excludes unrelated surrounding text.
   - Record every counted crop in `figure_inventory.md` with paper title, figure/table number, PDF page, source-page dimensions, exact crop bounding box `(x, y, width, height)`, complete caption, local path, linked claim, report section, source URL, and QA status.
   - Generate `figures/contact-sheet.png` after cropping and use it only for batch triage. Then inspect every counted crop individually at 100% scale and record both passes in the inventory and `review_checklist.md`. If no crop exists, do not generate an empty contact sheet; record the exact visual-evidence skip instead.

4. **Read with evidence discipline.**
   - Map every important claim to a paper section, figure, table, appendix, or code path.
   - Explain the logic chain: problem -> assumption -> method -> measurement -> conclusion.
   - Do not stop at describing what the method does. Build a **design-rationale matrix** for every core component, architecture choice, loss/objective, data construction step, training recipe, inference procedure, and system/runtime optimization.
   - For each design, state whether the paper explicitly explains why it was chosen. Cite the exact section/equation/figure when the rationale is `author-stated`; otherwise label it `inferred` or `not-stated` rather than presenting reviewer inference as author intent.
   - Identify the concrete failure mode, bottleneck, ambiguity, constraint, or baseline weakness the design is meant to solve, then explain the causal mechanism by which the design could address that problem. Include alternatives/trade-offs and whether ablations or controlled evidence validate the rationale.
   - Build a **technical-claim evidence matrix** for the paper's claimed technical points: each new component, architecture choice, loss/objective, data construction, training recipe, inference procedure, kernel/runtime optimization, benchmark design, or analysis claim must be mapped to supporting evidence.
   - For every claimed technical point, check whether the paper provides direct ablation, replacement baseline, sensitivity analysis, controlled experiment, mechanism visualization, theoretical proof, or code/config evidence. Mark unsupported points explicitly as unverified, correlation-only, or plausible but not isolated.
   - Use LaTeX math for formulas. Do not leave formulas as plain-text approximations when exact notation matters.
   - Mark assumptions and inferred calculations explicitly.
   - Build one centralized **terminology and symbol explanation** chapter before the method/formula discussion; do not scatter glossary definitions across unrelated sections. Define paper-specific terms and every symbol used in key equations, metrics, tables, or reviewer-derived formulas, including meaning, provenance (`author-defined`, `code-defined`, or `analysis-derived`), scope/indexing, units or values, source equation/section/derivation, and ambiguity. Do not assume a symbol has the same meaning across papers.
   - Cover non-obvious terms such as regenerated data, teacher/student logits, oracle/target/draft model, temperature setting, budget, tree width/depth, or benchmark variants. Mark symbols `not-applicable` only when neither the source nor the review uses meaningful symbols; do not invent entries.
   - Separate **paper-level conceptual claims** from **implementation-level behavior**. If a term such as causal mask, tree mask, block mask, branch conditioning, verification, or drafting appears in multiple stages, state exactly which stage it belongs to and whether the code implements the same object.
   - When the paper's prose is imprecise, reconcile it against equations, figures, appendix text, and code before writing the review. Prefer a qualified statement over copying an ambiguous phrase.

5. **Compare related work.**
   - Extract the paper's own related-work groups.
   - Compare against the current paper by mechanism, benefit, limitation, and fairness of the comparison.
   - Avoid broad literature essays; focus on why the paper's design differs and what trade-off it makes.

6. **Cross-check OpenReview public reviews against the paper when available.**
   - Trigger this step for OpenReview URLs, OpenReview-hosted submissions, or papers whose official venue page links to OpenReview.
   - Treat reviews as hypotheses and reading leads, not a standalone section of opinions. For each important reviewer claim, map it to the exact paper claim, method assumption, experiment, table, appendix item, rebuttal statement, or code path it challenges or supports.
   - Separate public reviewer claims from your own analysis. Do not treat reviewer criticism as ground truth until checked against the paper, appendix, rebuttal, code, or experiments.
   - Extract recurring reviewer concerns: novelty, correctness, missing baselines, experiment design, dataset leakage, metric choice, ablation gaps, theoretical assumptions, reproducibility, clarity, ethical/safety concerns, and deployment constraints.
   - Extract positive signals: strong contributions, convincing experiments, useful benchmark or dataset, clear system design, open-source implementation, or community interest.
   - Compare review-stage issues with the final paper when possible: which issues were resolved by rebuttal/revision, which remain unresolved, which are weakened by paper/code evidence, and which are reviewer misunderstandings.
   - For each major concern, write an evidence-based conclusion: whether it materially weakens the paper's contribution, only narrows the valid scope, suggests an extra experiment, or is not supported after checking the paper.
   - Integrate review-derived findings into the relevant analysis sections too: constraints in basic information, missing baselines in experiments, unresolved assumptions in methods, reproducibility issues in code checks, and deployment concerns in infra analysis.
   - Include a compact OpenReview cross-check table in `analysis.md`:
     - review/source
     - claim or concern
     - severity
     - linked paper claim or experiment
     - evidence in paper/rebuttal/code
     - status: resolved, partially resolved, unresolved, or unclear
     - your reading impact after cross-check
   - If reviews are private, missing, blocked, or hidden after acceptance, state that public OpenReview analysis could not be performed.

7. **Analyze infrastructure requirements.**
   - Include compute, memory, bandwidth, interconnect, scheduler/runtime, custom-operator, data-type, and heterogeneous-hardware implications when relevant.
   - Provide formulas for derived estimates, such as parameter count, activation/cache size, communication volume, expected throughput, or latency.
   - Separate paper-reported numbers from your own calculations.
   - Separate mechanism effects from system effects. For example, distinguish candidate-set quality, verification algorithm, custom kernels, batching, KV-cache layout, CUDA graphing, and scheduler policy. Do not attribute accepted-length gains to an execution kernel unless the paper/code shows that the kernel changes the candidate set or scoring.
   - Track data types and numeric formats: fp32, fp16, bf16, fp8, int8, int4, binary/ternary, sparse formats, mixed precision, quantization/dequantization, packing/unpacking, accumulation precision, layout transforms, and whether the claimed speed/memory benefit depends on a specific format or hardware support.
   - Analyze bandwidth utilization, not only raw bandwidth. Estimate effective bandwidth when possible:
     `effective_bandwidth = bytes_moved / runtime_seconds`; `utilization = effective_bandwidth / peak_bandwidth`. Discuss memory locality, cache reuse, tiling, operator fusion, communication/computation overlap, compression, all-reduce/all-to-all traffic, PCIe/NVLink/RDMA use, and whether kernels are memory-bound or compute-bound.
   - Analyze CPU/GPU/NPU and accelerator heterogeneity when relevant: host-device transfer, CPU preprocessing/postprocessing, GPU/NPU kernels, accelerator-specific operators, DMA, pinned memory, async copy, pipeline overlap, scheduler placement, fallback paths, and whether the method assumes homogeneous accelerators or mixed CPU/GPU/NPU deployment.

8. **Cross-check code when available.**
   - Inspect configs, model architecture, loss, data pipeline, evaluation, and serving/inference paths.
   - Link local file paths and, when possible, stable GitHub URLs pinned to a commit.
   - State what is implemented, what is only described in the paper, and what remains ambiguous.
   - If public model weights/checkpoints are referenced, inspect their metadata and configuration when accessible: open/gated/private status, files present, commit/revision, parameter count, architecture class, critical hyperparameters, and paper-specific flags. Compare these configs against baseline checkpoints when the paper claims architectural or capacity differences.
   - For code/config comparisons, explicitly distinguish capacity changes (layers, width, heads, parameter count), algorithmic changes (masking, scoring, sampling, loss), and runtime changes (kernels, cache, graphing).
   - If network access or model metadata access fails, state the limitation and do not infer checkpoint configuration from README claims alone.

9. **Attribute gains carefully.**
   - Before attributing gains, enumerate the paper's claimed technical points and identify which claims are actually tested by ablations or controlled comparisons.
   - Distinguish direct evidence (component removed/replaced under matched settings), indirect evidence (trend or visualization), confounded evidence (multiple changes bundled together), and no evidence.
   - When explaining why a method improves results, build a component-level attribution table if the paper has enough baselines: data/training objective, draft/candidate generation, search/tree construction, target verification, and serving/runtime.
   - Use bridge baselines (for example, baseline -> tree variant -> proposed method) to estimate contributions only as a rough decomposition. Mark such calculations as inferred, not paper-proven, unless the paper reports matched ablations.
   - Report both absolute and relative changes in the paper's primary metric, and identify when a component affects accepted length/quality versus latency/throughput.
   - If a technical point is central to the contribution but lacks ablation or controlled evidence, surface it again in limitations and unresolved reading questions.

10. **Write `analysis.md`.**
   - Use the reusable template in `references/markdown-template.md`.
   - Include the centralized revision-information section near the top. Keep its current version/revision ID and complete history identical to `deliverable_manifest.json`; do not rewrite or drop earlier entries.
   - Include a source/figure inventory near the top.
   - Include OpenReview public-review cross-check when available, combining reviewer concerns with paper content, rebuttal, appendix, experiments, and code evidence instead of listing reviews separately.
   - Include the technical-claim evidence matrix before or inside the key-results section, so claimed technical points are visibly tied to ablation/mechanism evidence or marked as unsupported.
   - Include the design-rationale matrix in the method section. A component description without its stated/inferred rationale, concrete target problem, causal mechanism, and evidence status is incomplete.
   - Include one centralized terminology-and-symbol chapter near the top before the method section. Put both the term table and symbol table inside it, and make every manifest entry traceable to this chapter and its paper/code source or explicit reviewer derivation.
   - Include images inline near the discussion they support.
   - End with practical limitations, research inspirations, and unresolved reading questions.

11. **Generate and insert an analysis diagram from the Markdown document when `$openrouter-icu-image` is available.**
   - After `analysis.md` is complete, use `$openrouter-icu-image` if it is installed and `OPENROUTER_ICU_API_KEY` is available. If the skill or API key is unavailable, do not block the review; add a short note in the final response.
   - The completed `analysis.md` must be the reference document for image generation. Use the `responses-doc` document-input path with `analysis.md` as `--input-file`.
   - Do not generate the diagram from prompt text alone. Do not paste the Markdown into the prompt, summarize the Markdown into the prompt, or use `/v1/images/edits` for Markdown input. If document upload through `responses-doc` cannot be used, skip image generation and state the limitation.
   - Generate a high-quality, high-resolution PNG under `figures/generated/`, for example `figures/generated/algorithm-analysis.png`.
   - Use `--quality high`, `--output-format png`, and a 16:9 high-resolution size such as `1792x1008` or `2048x1152` when supported. If high-resolution stalls or fails, retry at `1024x1024`.
   - Prompt for a shallow-gold background and flat technical infographic style. The visual should summarize the paper's design rationale, concrete target problem, causal mechanism, evidence chain, key technical claims, ablation support, limitations, and infra implications without inventing numeric results.
   - Include infra visual cues for data types, bandwidth utilization, and CPU/GPU/NPU heterogeneous execution when they are relevant to the paper.
   - Verify the image file exists, then insert it near the top of `analysis.md` after the source/figure inventory with a relative Markdown link and caption that labels it as an AI-generated analysis diagram.
   - Confirm the inserted image path is relative to `analysis.md` and does not break Markdown rendering.
   - Do not replace paper figures or factual plots with generated art. Keep generated diagrams clearly separate from paper-derived evidence.

After Workflow step 11, use this freeze protocol:

1. Before hashing, finalize the revision-information section. Start new history with `initial`; bootstrap a legacy delivery with `migration` and either its known `legacy-manifest` hash or an `unresolved` predecessor that blocks completion. For a changed tracked delivery, increment the document version, append a new revision entry, and bind `supersedes` to the previous revision and deliverable-manifest SHA-256.
2. Write the delegated `agent_handoff.md` when applicable, then create a preliminary `deliverable_manifest.json`, including revision history and the centralized terminology/symbol chapter location and entries, and run Draft 2020-12 structural validation plus every `semantic_validation` check required by the schema.
3. In delegated runs, generate and verify a preliminary `artifact_manifest.sha256`. Use these preliminary results to finalize every checklist/handoff status, then freeze `review_checklist.md`, `agent_handoff.md`, `analysis.md`, inventories, figures, and other referenced artifacts.
4. Recompute all frozen artifact hashes in `deliverable_manifest.json`, rerun structural and semantic validation, and freeze the final deliverable manifest. A `passed` validation must have an empty error list.
5. In delegated runs, regenerate and verify `artifact_manifest.sha256` last so it covers the frozen task packet, checklist, handoff, deliverable manifest, and all other files except itself. Do not edit any covered file afterward. Any post-freeze artifact change starts a new revision: restart at step 1, increment the document version, append the revision record, and recompute every affected hash.

Keep the handoff compact: record status, dispatch/task-packet/skill-tree/contract provenance, artifact paths, synthesis claims with evidence locations, and blocked/skipped items; do not include hidden chain-of-thought. Normalize task-packet literal `unknown` values to JSON `null` in `deliverable_manifest.json` and preserve the reason in the corresponding absent/blocked artifact entry.

When knowledge-base integration applies, execute the publication protocol only after the review freeze. Do not modify frozen review artifacts to make canonical links convenient; create a formal Paper projection with owned formal assets and traceable source references.

## Quality Checks

Before finishing:

- Confirm `review_checklist.md` exists, was updated throughout the run, and has no pending or unclassified mandatory items.
- Confirm `deliverable_manifest.json` exists, conforms to `references/deliverable-schema.json`, and agrees with artifact paths, hashes, visual counts, evidence status, invocation mode, and limitations.
- Confirm `semantic_validation` passed: artifact paths/hashes resolve; the revision section matches the manifest; revision history starts with exactly one bootstrap entry (`initial` with no predecessor, or `migration` with a legacy/unresolved predecessor), uses unique IDs/versions, advances time/version, and makes every later tracked entry supersede the immediately preceding revision/version/manifest hash; every unresolved issue has at most one later `migration-resolution`, and any unresolved issue without a valid resolution forces blocked status; current version/ID equals the final entry; terminology/symbol entries match the centralized `analysis.md` chapter and cover key terms/applicable symbols; every core design has a complete rationale entry consistent with `analysis.md`; visual counts and missing types agree; delegated provenance hashes match; and the frozen checklist/handoff agree with the final manifest.
- Confirm `figure_inventory.md` exists; if crops exist, confirm `figures/contact-sheet.png` exists and every counted crop has a complete inventory row and reviewed QA status. If no crop exists, confirm the precise blocker and alternative evidence are recorded.
- Confirm all Markdown image links resolve.
- Use the contact sheet for crop triage, then open every selected crop individually at 100% scale. Confirm exactly one numbered figure/table with its full caption, recorded source-page dimensions/bounding box, tight margins, and no next paragraph, page chrome, section heading, neighboring content, unrelated equation, excessive whitespace, or truncated caption.
- Confirm every key number in the review maps to a paper section/table/figure or a clearly stated calculation.
- Confirm every claimed technical point has been checked for ablation/control/mechanism evidence and unsupported claims are explicitly marked.
- Confirm every core design has a design-rationale entry separating author-stated rationale from inference, naming the concrete problem it targets, explaining the causal mechanism, and checking whether evidence supports that explanation.
- If `$openrouter-icu-image` was available, confirm `analysis.md` was passed as the `responses-doc --input-file` reference document, the generated analysis diagram exists, and it is linked from `analysis.md`; if unavailable or failed, state the limitation.
- Confirm code claims include file paths and commit hashes.
- Confirm the centralized terminology-and-symbol chapter defines every key paper-specific term and every variable used in key formulas, metrics, and tables; require source and ambiguity notes for every entry.
- Confirm the revision section includes the current version/revision ID and complete ordered history. A migration may use a known legacy manifest hash with unknown legacy version/ID; an unresolved predecessor must record a stable issue ID and recovery attempts. Completion remains blocked until a later `migration-resolution` entry both supersedes the prior blocked manifest and binds that issue ID to the recovered legacy manifest. Every later tracked revision must identify the exact superseded revision and manifest hash, changed locations, reason/evidence, and conclusion impact; no post-freeze change may reuse the prior revision ID.
- Confirm ambiguous mechanism terms are stage-qualified: drafting vs tree construction vs target verification vs serving/runtime.
- For OpenReview papers, confirm public reviews/meta-review/decision/rebuttal were checked when accessible, saved or summarized in `openreview_reviews.md`, and cross-checked against paper content, appendix, rebuttal, experiments, and code before drawing conclusions.
- Confirm gain-attribution statements are supported by matched ablations or explicitly marked as rough/inferred decompositions.
- Confirm checkpoint/config claims are grounded in inspected metadata or clearly marked as unverified.
- In delegated runs, confirm `agent_handoff.md` follows the supplied schema, every synthesis claim points to exact evidence, and `artifact_manifest.sha256` covers all files except itself. Report any suspected out-of-folder edit to the parent; do not self-certify filesystem read isolation.
- When a knowledge organization is resolved, confirm process/formal separation, canonical Paper and Asset ownership, promotion responsibility (`standalone` reviewer or delegated parent), and publisher validation status are explicitly classified.
- If tests or extraction tools could not run, state that limitation in the final response.

## Resources

- `references/markdown-template.md`: reusable Chinese Markdown structure, including the standard paper review sections and "解读问题/待验证清单".
- `references/deliverable-schema.json`: Draft 2020-12 schema for the required paper-level `deliverable_manifest.json`.
- `references/review-checklist-template.md`: mandatory per-paper execution and quality checklist; copy it into the paper folder before substantive analysis and preserve every item.
- `scripts/extract_pdf_assets.py`: optional helper to extract PDF text and render page PNGs for offline papers.
- `scripts/crop_pdf_figures.py`: optional helper to batch crop figures/tables from page PNGs and create a contact sheet for QA.
- `$openrouter-icu-image`: optional post-processing skill for generating a high-quality flat technical analysis diagram from the completed `analysis.md`.
- `references/knowledge-base-integration.md`: conditional review-to-canonical-Paper publication contract.
- `$research-knowledge-publisher`: project skill for organization resolution, canonical ownership, promotion planning, link/asset validation, and process/formal separation.
