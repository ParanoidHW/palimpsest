# Flex-Forcing: Towards a Unified Autoregressive and Bidirectional Video Diffusion Model

> [!info] 文档关系
> - 文档类型：Paper（blocked：主 PDF 不完整）
> - 领域入口：[README](../README.md)
> - 上位汇总：[ICML 2026 selected papers](../surveys/icml-2026-selected-papers.md)
> - 证据资产：无（本次无合格图表资产）
> - 相关文档：[Paper index](../evidence/paper-index.md)

## 文档修订信息

- 当前版本：`0.1.0`
- 当前修订：`rev-initial`
- 交付状态：blocked（主 PDF 不完整，无法进行实质性论文精读）

| revision_id | version | type | supersedes | reason | impact |
|---|---|---|---|---|---|
| rev-initial | 0.1.0 | initial | 无 | 首次建立单篇审阅包；仅获得损坏的部分 PDF | material |

## 来源与证据边界

- 论文标识：`arxiv:2607.03509v1`。
- 标题、URL、候选 venue 信息来自用户题单与 arXiv 元数据；v1 于 2026-07-03 发布，ICML 2026 状态未核验。
- [arXiv:2607.03509v1](https://arxiv.org/abs/2607.03509v1) 的本次下载仅 1.8 MiB；`pdfinfo` 与 `pdftotext` 均报告 trailer/xref 损坏，无法读取正文、公式、表格、图注、附录或实验数字。
- 因此以下内容严格区分“任务包元数据”和“未验证”：不能据此声称方法机制、性能、训练配置、代码实现或 ICML 接收状态。

## 术语与符号（可验证范围）

| 术语 | 定义 | 来源 | 歧义 |
|---|---|---|---|
| Flex-Forcing | 论文标题中的方法名 | arXiv title | 论文正文不可读，无法确认具体算法含义 |
| autoregressive | 标题中的自回归生成范式 | arXiv title | 未知其在论文中对应训练、采样还是混合模式 |
| bidirectional video diffusion | 标题中的双向视频扩散范式 | arXiv title | 未知具体噪声调度、注意力掩码与条件定义 |

本次没有可可靠提取的关键公式或指标符号；`symbol_applicability=not-applicable` 仅表示当前损坏来源无法建立符号表，不表示论文没有符号。

## 方法与设计 rationale

无法执行。正文和图表不可解析，不能判断作者陈述 rationale、目标瓶颈、因果机制、替代方案、权衡或消融验证。任何进一步描述都会超出证据边界。

## 技术主张证据矩阵

| 主张 | 证据位置 | 分类 | 结论 |
|---|---|---|---|
| 统一自回归与双向视频扩散 | 仅标题 | unverified | 需要完整 PDF/源码核验 |
| Flex-Forcing 的具体训练或采样机制 | 无 | missing | 不可判断 |
| 性能、质量、效率改进 | 无 | missing | 不可判断 |
| 系统/硬件优化 | 无 | missing | 不可判断 |

## 相关工作、OpenReview 与代码

- 相关工作：不可提取论文自身分组；无公平比较。
- OpenReview：未取得 forum URL 或公开评审。
- 项目页/代码：任务包给出 NVIDIA 项目 URL，但没有可核验的本地代码快照、commit 或配置；不据 README/标题推断实现。

## 基础设施分析

无法从损坏 PDF 获得计算量、显存、带宽、互联、数据类型、CPU/GPU/NPU 分工、运行时或自定义算子信息。仅能指出视频扩散通常可能涉及高维时空张量，但这是领域常识而非本论文证据，不纳入结论。

## 增益归因

没有可用的匹配基线、消融或受控实验；所有组件级归因均标记为 missing。

## 图表证据

因 PDF trailer/xref 损坏，无法生成可审计的单对象紧裁剪；不存在可接受的机制图或结果/系统图。

## 局限、研究启发与待验证问题

1. 必须重新获取完整且可解析的 arXiv v1 PDF（或作者提供的等价版本），再执行正文、公式、图表和附录核验。
2. 需要确认 ICML 2026 的正式状态、OpenReview forum/reviews、rebuttal 和最终版本差异。
3. 需要获取项目代码和 commit，核对统一模型的 mask/conditioning、训练目标、采样流程、精度与硬件假设。
4. 在完整来源可用前，不应将标题中的“unified”解释成已验证的算法或性能结论。
