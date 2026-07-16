# Exact-paper recovery log

- Access date: 2026-07-16 (Asia/Shanghai)
- Exact title: `Dual-Latent Memory Routing for Vision-Language Reasoning`
- Required identity rule: exact-title sources only; `Dual Latent Memory for Visual Multi-agent System` was explicitly rejected as a different paper.

## Confirmed primary source

- ICML 2026 official search returned poster `63955`: <https://icml.cc/virtual/2026/poster/63955>.
- The official page confirms the title, authors Hao-Xuan Ma, Jin-Fei Qi, YiCheng Xiao, and Han-Jia Ye, ICML 2026, poster schedule, and an abstract.
- The official Spotlight Posters search/event result also includes the exact title.
- Local snapshot: `icml-poster-63955.html`.
- The page's action-button container contains no PDF, OpenReview, project, source, or code link.

## Recovery attempts

| Source | Exact query/result | Classification |
|---|---|---|
| arXiv API | Exact-title query: `totalResults=0`; Hao-Xuan Ma author query returned three different papers | exact PDF/source unavailable |
| OpenAlex API | `display_name.search` exact-title query: `count=0` | metadata/PDF unavailable |
| DBLP API | Exact-title token query: `hits.total=0` | metadata unavailable |
| Crossref API | Top five title-query results were different works | exact DOI/PDF unavailable |
| Semantic Scholar API | HTTP 429 rate limit | access blocked; no result claimed |
| GitHub repository API | Exact-title and author-plus-DLMR searches: `total_count=0` | official code unavailable |
| OpenReview API v1/v2 | Both exact-title requests returned `ChallengeRequiredError` HTTP 403 | public reviews/forum inaccessible |
| ICML official site | Exact search found poster `63955`; poster and `/paper/63955` expose abstract but no media links | identity confirmed; PDF absent |

## Conclusion

The exact paper identity is confirmed from ICML, but no exact PDF, source archive, code repository, or accessible OpenReview forum could be recovered. The available abstract is insufficient for a full paper-deep-review; delivery remains blocked.
