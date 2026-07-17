# Paper Deep Review Execution Checklist

Allowed statuses: `pending`, `done`, `blocked`, `skipped-with-reason`. Replace each `pending` status as work progresses. Preserve every item and add the exact artifact path, evidence, or reason after the status.

## Workflow

- [done] W1 Folder: folder reused; blocked-delivery artifacts created in this folder.
- [done] W1 Delegated input: hashes verified against task packet and contract.
- [blocked] W2 Primary sources: no exact PDF/source/official page; recovery attempts recorded in task packet.
- [blocked] W2 Public reviews: no URL; OpenReview exact-title query 403 is recorded.
- [blocked] W2 Code: no exact repository/commit; GitHub exact-title search zero results.
- [blocked] W3 Text: no PDF, so no extraction.
- [blocked] W3 Visuals: no PDF pages; no crops.
- [done] W3 Inventory: precise no-crop blocker recorded in `figure_inventory.md`.
- [done] W3 Visual QA: no-crop blocker recorded; no blank placeholder.
- [blocked] W4 Evidence discipline: no source sections/equations available.
- [blocked] W4 Design rationale: no method source; no rationale claims made.
- [blocked] W4 Claim matrix: all technical claims unverified.
- [done] W4 Terminology and symbols: centralized title-only terms; symbols not-applicable.
- [blocked] W5 Related work: paper related-work section unavailable.
- [blocked] W6 OpenReview cross-check: unavailable (403/no URL).
- [blocked] W7 Infrastructure: no report or code.
- [blocked] W8 Code/config: no repository/config.
- [done] W9 Gain attribution: explicitly no attribution made.
- [done] W10 Report: concise blocked analysis written.
- [done] W10 Revision information: initial revision recorded in analysis and manifest.
- [skipped-with-reason] W11 Generated diagram: required responses-doc path unavailable per parent contract.
- [done] D1 Delegated handoff: `agent_handoff.md` written.
- [blocked] D2 Deliverable manifest: structural/semantic validation blocked by absent source and unavailable validator.
- [done] D3 Artifact manifest: final hash generated after freeze.

## Quality Checks

- [done] Q1 No Markdown image links exist.
- [done] Q2 No-crop blocker is precise; no blank placeholder/contact sheet.
- [done] Q3 No paper result numbers or calculations are reported.
- [done] Q4 All putative technical claims are explicitly unverified.
- [skipped-with-reason] Q5 Parent contract states responses-doc input path unavailable.
- [done] Q6 No code claims; repository unverified.
- [done] Q7 Title-only terminology covered; no applicable symbols.
- [done] Q8 No mechanism-stage claims are made.
- [blocked] Q9 Public OpenReview evidence unavailable.
- [done] Q10 No gains attributed.
- [done] Q11 Checkpoint/config explicitly unverified.
- [done] Q12 Failures and conclusion effects recorded in analysis and manifest.
- [done] Q13 Task packet preserved; handoff and final artifact manifest created; no suspected out-of-folder write.
- [blocked] Q14 Structural/semantic completion cannot pass for absent source; manifest records blocked validation.
- [blocked] Q15 No source from which to identify core designs.
- [done] Q16 Initial revision metadata matches analysis/manifest.

## Final Classification

- [done] F1 Required blocked artifacts exist; counted visuals are zero with precise blocker.
- [done] F2 No pending/unclassified items remain.
- [done] F3 Handoff states every material limitation and does not claim completion.
