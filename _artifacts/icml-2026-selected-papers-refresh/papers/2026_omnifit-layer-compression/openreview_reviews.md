# OpenReview Access Record

- Forum: `https://openreview.net/forum?id=8RY20mLzup`
- PDF: `https://openreview.net/pdf?id=8RY20mLzup`
- API: `https://api2.openreview.net/notes?forum=8RY20mLzup&limit=1000`
- Access date: 2026-07-24

## Identity

Exact title: *OmniFit: Bridging Modalities via Layer-Adaptive Token Compression for Omnimodal Large Language Models*.

Authors from matching ICML/public metadata: Zining Wang, Zhihang Yuan, Yingjie Zhai, Wenshuo Li, Han Shu, Ruihao Gong, Jinyang Guo, Xianglong Liu.

## Access attempts

1. `curl -L --fail --retry 3` against the exact PDF returned HTTP 403; no PDF bytes were retained.
2. Browser retrieval of the forum redirected to OpenReview's “Verifying your browser” challenge.
3. Browser retrieval of the PDF/API was unavailable.
4. `curl` against OpenReview API v2 returned HTTP 403; no review-note JSON was retained.
5. The official ICML Downloads page and poster `65962` were readable and confirmed title, authors, abstract, and Spotlight relation `84897`, but exposed no review, rebuttal, decision-note, PDF, source, or code links.

## Classification

Decision, meta-review, individual reviews, scores/confidences, rebuttal/author response, discussion, final revision, and affiliations are `blocked`. No reviewer claim is repeated or inferred. Public metadata that labels the submission `ICML.2026 - Spotlight` is identity evidence only, not a substitute for the decision note.
