# Kernel Agents Paper Index

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 证据资产：`../assets/papers/`
> - 相关文档：[Figure inventory](figure-inventory.md)

## 收录合同

主线要求工作直接处理 kernel 生成、优化或 hardware-grounded evaluation。相邻背景必须显式解释迁移关系，不能伪装成 kernel paper。版本、venue 与代码状态核验于 2026-07-11。

| Paper | 版本 / venue | 领域角色 | 正式证据入口 | 代码/数据状态 |
|---|---|---|---|---|
| [Towards Automated Kernel Generation in the Era of LLMs](../papers/towards-automated-kernel-generation.md) | arXiv:2601.15727v3；venue 未确认 | 主线 survey：LLM4Kernel、Agent4Kernel、数据与 benchmark | [方法谱系](../papers/towards-automated-kernel-generation.md#2-方法谱系)，[evaluation contract](../papers/towards-automated-kernel-generation.md#3-evaluation-contract-与成本模型) | 配套清单可访问；commit `6e6b68e...`，不是实验代码 |
| [AscendKernelGen](../papers/ascend-kernel-gen.md) | arXiv:2601.07160v2；venue 未确认 | 主线：Ascend-CoT + SFT/DPO + NPUKernelBench | [主结果](../papers/ascend-kernel-gen.md#3-实验设置与主结果)，[代码边界](../papers/ascend-kernel-gen.md#8-代码与-checkpoint-对照) | 论文声称公开；旧 GitHub URL 404，commit/checkpoint 未验证 |
| [AscendCraft](../papers/ascend-craft.md) | arXiv:2601.22760v1；venue 未确认 | 主线：专家 DSL + LLM multi-pass lowering | [方法](../papers/ascend-craft.md#2-方法)，[证据矩阵](../papers/ascend-craft.md#4-技术主张证据矩阵与收益归因) | 未发现公开实现/checkpoint |
| [s1: Simple test-time scaling](../papers/s1-test-time-scaling.md) | arXiv:2501.19393v3；正式 venue 未确认 | 相邻背景：可迁移的 reasoning/iteration budget controller | [迁移边界](../papers/s1-test-time-scaling.md#8-迁移到-kernel-agent-的边界) | 官方代码/数据可访问；commit `77272c6e...` |

## 交叉阅读结论

- AscendKernelGen 把领域知识放进训练数据与模型参数；AscendCraft 把知识放进 DSL、few-shot examples 和 lowering rules。两者 benchmark、baseline 与公开程度不同，数字不可直接排名。
- Survey 给出分类与评估合同，但单组件收益必须回到单篇论文的 matched ablation。
- s1 只支持“预算可控”的解码思想；kernel agent 必须把新增回合绑定 compiler/profiler observation。
