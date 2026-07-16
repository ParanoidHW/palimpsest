# ICML 2026 Paper Deep Review Agent Contract

## Scope

- Review exactly one paper identified by the parent-owned `task_packet.yaml`.
- Read and obey `/mnt/d/huangwei/markdown/AGENTS.md`, `00_meta/research-knowledge-organization.md`, and the complete `/home/hw/.codex/skills/paper-deep-review/SKILL.md` plus all three referenced templates/schema before substantive work.
- Treat the paper folder named in the packet as the only writable ownership boundary. Do not modify `task_packet.yaml`, this contract, another review folder, or `02_model_systems/ICML/2026/`.
- Intermediate PDFs, source, code snapshots, extracted text, page renders, crops, contact sheets, QA, logs, manifests, and `analysis.md` remain in the owned `_artifacts` paper folder.

## Provenance Verification

- Before analysis, compute and compare the SHA-256 of `task_packet.yaml` against the hash reported by the parent dispatch message.
- Compute the deterministic complete skill-tree hash with all files under `/home/hw/.codex/skills/paper-deep-review`; it must match `expected_skill_tree_sha256` in the packet.
- Compute the SHA-256 of this contract; it must match `expected_agent_contract_sha256` in the packet.
- Record all three verified hashes in `agent_handoff.md` and `deliverable_manifest.json`. A mismatch blocks the run.

## Required Workflow

- Create `review_checklist.md` from the complete skill template before substantive analysis and update statuses throughout the run.
- Acquire the exact primary paper; do not substitute a similarly named work. Prefer the packet URL, then official arXiv/OpenReview/author sources. Record unsuccessful recovery attempts.
- Extract searchable text and at least one mechanism visual plus one result/system visual when the PDF permits. Every accepted crop must contain one numbered object and its complete caption, use a semantic filename, record exact page dimensions and `(x, y, width, height)`, pass contact-sheet triage, and pass individual 100% inspection.
- Write a rigorous Chinese `analysis.md` using the skill template. Include revision information, source/figure inventory, centralized terminology and symbols, design-rationale matrix, technical-claim evidence matrix, related-work comparison, OpenReview cross-check or precise unavailability, infrastructure analysis, code/config cross-check or precise unavailability, gain attribution, limitations, inspirations, and unresolved questions.
- The installed OpenRouter ICU CLI exposes only `generate` and `edit`, not the mandatory `responses-doc --input-file analysis.md` path. Therefore do not generate prompt-only art. Mark W11/Q5 and the manifest generated-diagram artifact `skipped-with-reason` with this exact capability limitation.
- Apply the two-pass freeze protocol. Validate `deliverable_manifest.json` against `/home/hw/.codex/skills/paper-deep-review/references/deliverable-schema.json` with Draft 2020-12 and run/record all semantic checks. Completion must be `blocked` if required validation cannot pass.
- Generate `artifact_manifest.sha256` last, covering every file in the paper folder except itself. Do not edit covered files afterward.

## Delegated Handoff

Write a compact `agent_handoff.md` containing:

- status and exact paper identity;
- dispatch ID, agent task name, task-packet hash, skill-tree hash, and contract hash;
- artifact paths and validation results;
- 3-6 synthesis claims, each pointing to exact sections/tables/figures/code paths;
- accepted formal-promotion candidates with source crop paths and inventory rows;
- all blocked/skipped items and their effect on conclusions;
- any suspected out-of-folder write (do not self-certify filesystem isolation).

## Formal Promotion Boundary

- The parent owns formal promotion to `02_model_systems/ICML/2026/`.
- Recommend a stable lowercase kebab-case paper slug in the handoff.
- `analysis.md` may reference local artifact evidence during the delegated run. The parent will rewrite formal links so canonical documents never reference `_artifacts`, absolute paths, page renders, contact sheets, or untracked files.
- Do not commit or stage files.
