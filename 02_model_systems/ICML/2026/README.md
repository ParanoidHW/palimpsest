# ICML 2026 Paper Reviews

本目录收录用户给出的 12 篇候选论文精读。它是用户题单的知识入口，不是 ICML 2026 官方接收列表；venue 状态均按论文、arXiv、ICML 或 OpenReview 一手证据单独标注。

## 阅读路径

1. [Selected papers survey](surveys/icml-2026-selected-papers.md)：先看跨论文机制、系统趋势与证据边界。
2. [Paper index](evidence/paper-index.md)：确认每篇论文的身份、venue、资料完整度与 review 状态。
3. 单篇精读：从下表进入方法、公式、实验、Infra、代码核验和局限。
4. [Figure inventory](evidence/figure-inventory.md)：追溯正式图表的页码、bbox、caption 与父级 QA。

## 状态总览

| Paper | Venue 核验 | Review 状态 |
|---|---|---|
| [SplAttN](papers/splattn.md) | ICML 2026 Spotlight；官方 poster `60900` | complete：完整 PDF/source、代码与 2 张论文图已复核 |
| [XDLM](papers/xdlm.md) | ICML 2026 未独立核验 | complete |
| [Dual-Latent Memory Routing](papers/dual-latent-memory-routing.md) | ICML 2026 Spotlight；poster `63955`、OpenReview `SFWWUr9V7c` | limited：原投稿索引方法、公式与 Tables 1–4 已恢复；accepted final/视觉/代码/评审仍受限 |
| [LatentLM](papers/latentlm.md) | ICML 2026 未独立核验 | complete |
| [Flex-Forcing](papers/flex-forcing.md) | ICML 2026 Spotlight | complete with limitations：完整 PDF/source 与 2 张论文图已复核；代码/公开评审未取得 |
| [OmniFit layer compression](papers/omnifit-layer-compression.md) | ICML 2026 Spotlight；OpenReview `8RY20mLzup`、poster `65962` | limited：官方摘要已恢复；final PDF/source/视觉/代码/评审仍受限 |
| [LiME](papers/lime.md) | ICML 2026 未独立核验 | complete |
| [SelfJudge](papers/selfjudge.md) | arXiv `journal_ref: ICML 2026` | complete |
| [OnlineSpec](papers/onlinespec.md) | ICLR 2026 Lifelong Agent Workshop | complete，venue mismatch |
| [Multi-Token Self-Distillation](papers/multi-token-self-distillation.md) | `Preprint. Under review` | complete with limitations：完整 source、官方代码 commit 与 5 张论文图已复核；venue 未核验 |
| [DODO](papers/dodo.md) | ICML 2026 SPIGM Workshop | complete，非主会 |
| [ECHO](papers/echo.md) | ICML 2026 spotlight，OpenReview forum `L31hKCWRsN` | complete |

## 文档索引

- Survey：[ICML 2026 selected papers](surveys/icml-2026-selected-papers.md)
- Evidence：[Paper index](evidence/paper-index.md)，[Figure inventory](evidence/figure-inventory.md)
- Papers：[SplAttN](papers/splattn.md)，[XDLM](papers/xdlm.md)，[Dual-Latent](papers/dual-latent-memory-routing.md)，[LatentLM](papers/latentlm.md)，[Flex-Forcing](papers/flex-forcing.md)，[OmniFit](papers/omnifit-layer-compression.md)，[LiME](papers/lime.md)，[SelfJudge](papers/selfjudge.md)，[OnlineSpec](papers/onlinespec.md)，[Multi-Token Self-Distillation](papers/multi-token-self-distillation.md)，[DODO](papers/dodo.md)，[ECHO](papers/echo.md)

## 资产说明

正式论文图表位于 `assets/papers/<paper-slug>/`，仅包含通过父级原分辨率复核的单一编号对象和完整 caption。PDF、源码、整页渲染、contact sheet、失败裁剪、checklist、manifest 与执行日志不进入正式知识目录。
