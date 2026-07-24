# OpenReview evidence status

- Forum: `https://openreview.net/forum?id=SFWWUr9V7c`
- Access date: 2026-07-24
- Public metadata visible through search indexing:
  - title and named authors;
  - ICML 2026 Spotlight status;
  - published 2026-04-30, last modified 2026-06-24;
  - submission number 18981;
  - an indexed originally submitted PDF link;
  - a code claim pointing to `https://github.com/Hunter-Wrynn/DLMR`.
- Independent official venue evidence: `retrieval/icml-poster.html` confirms ICML poster 63955, the authors, abstract, and a Spotlight presentation relation.

## Decision, revisions, reviews, and rebuttal

| Item | Status | Evidence / attempt | Consequence |
|---|---|---|---|
| Final decision | partially verified | Forum search metadata and official ICML page establish accepted Spotlight status. No decision-note body or note ID was accessible. | Acceptance tier is usable; decision rationale is not. |
| Exact final revision | blocked | Forum says last modified 2026-06-24. Indexed attachment is explicitly the anonymous original submission. Direct forum/API/attachment requests returned HTTP 403. | Material differences between original and final PDF cannot be assessed. |
| Official reviews | blocked | Exact-forum searches did not expose review bodies; OpenReview forum and API requests returned HTTP 403. | Reviewer concerns/scores cannot be treated as checked. |
| Meta-review | blocked | No note body or ID recovered; forum/API blocked. | Area-chair reasoning remains unknown. |
| Author response/rebuttal | blocked | No response note recovered; forum/API blocked. | Cannot classify reviewer issues as resolved or unresolved. |
| Public discussion | blocked | No discussion notes recovered; forum/API blocked. | No community claims are used. |
| Code claim | contradicted by access check | Forum index claims code at `Hunter-Wrynn/DLMR`; clone failed and GitHub public API returned 404. | Treat as stale/unfulfilled claim, not implementation evidence. |

## Cross-check conclusion

The Spotlight decision is verified at the venue/metadata level, but the public-review analysis required by the workflow could not be performed. No reviewer statement is repeated as fact. The analysis instead flags the experiment and reproducibility questions that remain open from paper/search-index evidence; these are the reviewer's own questions, not recovered OpenReview opinions.
