# ICML 2026 用户题单论文索引

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Survey](../surveys/icml-2026-selected-papers.md)
> - 证据资产：无
> - 相关文档：[Figure inventory](figure-inventory.md)

| Slug | Paper / primary source | Venue evidence | Review | Visuals | Code evidence |
|---|---|---|---|---:|---|
| `splattn` | [SplAttN](../papers/splattn.md), [arXiv:2605.01466v2](https://arxiv.org/abs/2605.01466v2) | ICML 2026 Spotlight；官方 poster `60900` | complete | 2 | 官方仓 commit `0c279dd`；公开 HF checkpoints metadata 已核验 |
| `xdlm` | [XDLM](../papers/xdlm.md), [arXiv:2602.01362](https://arxiv.org/abs/2602.01362) | 未独立核验 ICML | complete | 3 | 官方仓 commit `66c34ac5` |
| `dual-latent-memory-routing` | [Dual-Latent](../papers/dual-latent-memory-routing.md), [ICML poster 63955](https://icml.cc/virtual/2026/poster/63955), [OpenReview `SFWWUr9V7c`](https://openreview.net/forum?id=SFWWUr9V7c) | ICML 2026 Spotlight | limited：original-submission 索引已恢复方法、公式与 Tables 1–4；accepted final/视觉/评审受限 | 0（`visual-evidence-skip`） | 声称的 `Hunter-Wrynn/DLMR` 当前 404 |
| `latentlm` | [LatentLM](../papers/latentlm.md), [arXiv:2412.08635](https://arxiv.org/abs/2412.08635) | 未独立核验 ICML | complete | 2 | UniLM commit `833df7e`，仅部分实现 |
| `flex-forcing` | [Flex-Forcing](../papers/flex-forcing.md), [arXiv:2607.03509v1](https://arxiv.org/abs/2607.03509v1) | ICML 2026 Spotlight；官方 NVIDIA/ICML/OpenReview 元数据交叉核验 | complete with limitations | 2 | 未发现官方代码/checkpoint |
| `omnifit-layer-compression` | [OmniFit](../papers/omnifit-layer-compression.md), [OpenReview `8RY20mLzup`](https://openreview.net/forum?id=8RY20mLzup), [ICML poster 65962](https://icml.cc/virtual/2026/poster/65962) | ICML 2026 Spotlight | limited：官方摘要已恢复；final PDF/source/公式/表图/评审受限 | 0（`visual-evidence-skip`） | 未发现官方 code link |
| `lime` | [LiME](../papers/lime.md), [arXiv:2604.02338](https://arxiv.org/abs/2604.02338) | 未独立核验 ICML | complete | 3 | 未发现官方实现 |
| `selfjudge` | [SelfJudge](../papers/selfjudge.md), [arXiv:2510.02329v2](https://arxiv.org/abs/2510.02329v2) | arXiv `journal_ref: ICML 2026` | complete | 4 | 未发布官方实现 |
| `onlinespec` | [OnlineSpec](../papers/onlinespec.md), [arXiv:2603.12617](https://arxiv.org/abs/2603.12617) | ICLR 2026 Lifelong Agent Workshop | complete | 4 | commit `3a6cc69` |
| `multi-token-self-distillation` | [MTP Self-Distillation](../papers/multi-token-self-distillation.md), [arXiv:2602.06019v2](https://arxiv.org/abs/2602.06019v2) | `Preprint. Under review`；ICML 身份未独立确认 | complete with limitations | 5 | 完整 source；官方仓 commit `167413e` |
| `dodo` | [DODO](../papers/dodo.md), [arXiv:2602.16872v2](https://arxiv.org/abs/2602.16872v2) | ICML 2026 SPIGM Workshop | complete | 4 | 未发现官方实现；第三方仓不作论文实现证据 |
| `echo` | [ECHO](../papers/echo.md), [arXiv:2604.09603v2](https://arxiv.org/abs/2604.09603v2) | ICML 2026 spotlight；OpenReview `L31hKCWRsN` | complete | 2 | 代码尚未发布 |

## 选择与排除说明

- 本索引完整保留用户题单 12 项；没有因 venue mismatch 或证据受阻而静默删除。
- SplAttN 已在 2026-07-24 刷新：完整 PDF、LaTeX source、ICML Spotlight 与代码/checkpoint 元数据均已闭环；正式提升 Figure 1 与 Figure 8。
- `OmniFit` 没有用 arXiv:2604.21575 的 3D body-fitting 同名论文替代。
- `Dual-Latent` 没有用 arXiv:2602.00471 的 visual multi-agent 工作替代。
- 2026-07-25 重新提升既有材料：Dual-Latent 从摘要级升级为 original-submission 索引正文级，OmniFit 从题名级升级为官方摘要级；两者均未把 final/视觉/代码缺口误报为已解决。
- 正式图表计数以父级复核后的资产为准；MTP Figure 12 与若干初始 SelfJudge/ECHO crop 因混入邻接内容或 caption 截断被排除/重裁。
