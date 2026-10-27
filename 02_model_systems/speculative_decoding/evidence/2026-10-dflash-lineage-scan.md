# 2026-10 DFlash/DSpark 谱系候选识别

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Evolution](../surveys/evolution.md)
> - 证据资产：无
> - 相关文档：无

## 范围与证据等级

- 时间范围：2026-10-01 至 2026-10-27。
- 目的：只识别是否继承或延申自 DFlash、DSpark 或同一 block/diffusion speculative decoding 路线；不替代 Paper 精读。
- 证据：arXiv 标题、摘要和项目页级别；“直接继承”仅在摘要明确写出 DFlash/DSpark 或方法名直接表明继承时使用。

## 候选识别

| arXiv | 论文 | 谱系判断 | 判断依据（摘要级） | 当前动作 |
|---|---|---|---|---|
| [2610.27379](https://arxiv.org/abs/2610.27379) | DStill | **直接延申 DFlash** | 明确以 one-step DFlash 为基线，将多步 refinement 蒸馏为一次 block draft | 观察；未建 Paper |
| [2610.26531](https://arxiv.org/abs/2610.26531) | ReAnchor | **直接延申 DFlash** | 明确使用 pretrained DFlash drafters，复用 verifier rejected states | 观察；未建 Paper |
| [2610.20175](https://arxiv.org/abs/2610.20175) | TreeSpark | **直接延申 DSpark** | 摘要明确称为 semi-autoregressive DSpark architecture 的 extension | 观察；未建 Paper |
| [2610.12570](https://arxiv.org/abs/2610.12570) | DCOCO / DFlash Contextual Corrector | **直接延申 DFlash** | 方法名直接包含 DFlash Contextual Corrector，目标是恢复 block 内上下文依赖 | 观察；未建 Paper |
| [2610.19792](https://arxiv.org/abs/2610.19792) | JetSpec++ | **同路线延申，非 DFlash 直接继承** | 保留 learned draft，加入 block 内 refinement、跨 block foresight 和流水重叠；摘要直接以 DSpark 作比较对象 | 观察；归入 parallel/block drafting 旁支 |
| [2610.24365](https://arxiv.org/abs/2610.24365) | FlashMap | **同路线延申，非 DFlash 直接继承** | flow drafter 继承 target hidden-state conditioned、single-pass block drafting 设定；以 matched DFlash 作 baseline | 观察；未建 Paper |
| [2610.33379](https://arxiv.org/abs/2610.33379) | Packed-SS | **相关但非 DFlash 继承** | diffusion drafting 与 self-speculative schedule 的 one-call-ahead 组合；摘要未指向 DFlash/DSpark | 暂不纳入 DFlash 主线 |
| [2610.24722](https://arxiv.org/abs/2610.24722) | PV-Decoding | **相关但非 DFlash 继承** | 面向 diffusion LM 的 progressive verification 和 confidence gating；未指向 DFlash/DSpark | 暂不纳入 DFlash 主线 |
| [2610.22543](https://arxiv.org/abs/2610.22543) | On the SPOT | **相关但非 DFlash 继承** | 面向 diffusion LM 的 commit-order prediction 与 candidate tree；验证对象和 DFlash block drafter 不同 | 暂不纳入 DFlash 主线 |
| [2610.20687](https://arxiv.org/abs/2610.20687) | On-Policy Residual Learning | **相关但非 DFlash 继承** | 以 residual learning 改造 diffusion LM，并与 DFlash/EAGLE3 比较；属于替代路线 | 暂不纳入 DFlash 主线 |
| [2610.23818](https://arxiv.org/abs/2610.23818) | Acceptance Is Not Speed | **分析/审计工作，非继承** | 研究 lossy speculative decoding 的 completion-length inflation，不提出 DFlash/DSpark drafter | 作为方法评测背景 |
| [2610.30644](https://arxiv.org/abs/2610.30644) | Speculative Acceptance Does Not Decay with Position | **分析/基线工作，非继承** | 研究长 CoT 中 acceptance 的位置效应，使用独立 draft-target 对，不延申 block diffusion | 作为评测背景 |

## 当前边界

本清单不把“比较了 DFlash/DSpark”视为“继承 DFlash/DSpark”。只有 DStill、ReAnchor、TreeSpark、DCOCO 被标为直接延申；JetSpec++ 与 FlashMap 是相邻的 block/parallel drafting 发展；其余候选暂不进入 DFlash 主线 Survey 的方法结论。
