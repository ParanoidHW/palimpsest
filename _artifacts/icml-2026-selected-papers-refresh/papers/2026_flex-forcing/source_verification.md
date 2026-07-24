# Source and Venue Verification

- Access date: 2026-07-24 (Asia/Shanghai)
- arXiv record: <https://arxiv.org/abs/2607.03509>
- arXiv PDF: <https://arxiv.org/pdf/2607.03509>
- arXiv source: <https://export.arxiv.org/e-print/2607.03509>
- OpenReview forum: <https://openreview.net/forum?id=COGc3MSR7n>
- Official project page: <https://research.nvidia.com/labs/genair/flex-forcing/>
- ICML poster requested by packet: <https://icml.cc/virtual/2026/poster/65566>
- ICML downloads index: <https://icml.cc/Downloads/2026>

## Acquisition and integrity

| Object | Result | Local evidence |
|---|---|---|
| arXiv PDF | Complete 17,953,029-byte PDF; `pdfinfo` reports PDF 1.7, 16 pages, no encryption, letter page size. Text extraction and all-page rendering succeeded. | `paper.pdf`, `extracted_text/arxiv-paper.txt`, `extracted_text/arxiv-paper-layout.txt`, `figures/page_png/` |
| arXiv source | Complete 17,301,676-byte gzip archive; archive lists accepted ICML style, one main TeX file, bibliography, 13 main/appendix figure PDFs, and style files. Extraction succeeded. | `source/arxiv-source.tar`, `source/example_paper.tex`, `source/figures/`, `source/appendix_figures/` |
| arXiv revision metadata | The abs page reports only v1, submitted 2026-07-03 17:34:14 UTC. The TeX uses `\usepackage[accepted]{icml2026}`. | `evidence/arxiv-abs.html:24,126,175`, `source/example_paper.tex` |
| OpenReview forum/API | Forum and PDF URLs redirect to an anti-bot challenge; both API v1 and v2 returned HTTP 403. Search-indexed primary metadata exposes the title, authors, abstract, PDF hash URL, and subject `ICML.2026 - Spotlight`, but public reviews, decision note, rebuttal, and version history could not be preserved. | `evidence/openreview-forum.html`, `openreview_reviews.md` |
| ICML venue | The author/NVIDIA project page labels the work `ICML 2026 · Spotlight`; the official ICML 2026 Downloads index lists the exact title; the source is camera-ready ICML 2026. Direct poster 65566 retrieval was blocked (HTTP 403/robots), so its poster metadata could not be frozen. | `evidence/project-page.html:38`, `source/example_paper.tex`, search evidence summarized here |
| Official project/code | The official NVIDIA page was preserved and contains demos/method/result descriptions, but no paper, code, GitHub, model-weight, or checkpoint link. A public GitHub repository search for `"Flex-Forcing"` returned three unrelated repositories. | `evidence/project-page.html`, `evidence/github-repository-search.json` |

Additional tool note: `qpdf --check` could not run because `qpdf` is not installed. This does not lower PDF readability confidence because `file`, `pdfinfo`, both `pdftotext` modes, all-page Poppler rendering, and source extraction succeeded without parser errors. The OpenReview PDF file is absent because its download was blocked, not because a local PDF failed validation.

## Version comparison boundary

The current arXiv v1 is an accepted ICML camera-ready source. The accessible search-indexed OpenReview PDF agrees on title, authors, abstract, and Figure 1 content, but anti-bot blocking prevents byte-level acquisition of the initial submission and note-history inspection. Therefore, no claim is made that the OpenReview submission and camera-ready are textually identical; only the visible front-matter agreement is verified.
