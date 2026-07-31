# Kernel Agents

本领域覆盖 LLM/agent 驱动的 GPU/NPU kernel 生成、执行反馈、专有 DSL lowering 与受预算约束的优化搜索。这里把“模型生成能力”“compiler/hardware verifier”“runtime 性能”分开记录；`s1` 只作为 test-time budget 背景，不属于 kernel-generation 主线。

## 阅读路径

1. [Paper index](evidence/paper-index.md)：先看版本、venue、代码状态和领域相关性。
2. [Towards Automated Kernel Generation](papers/towards-automated-kernel-generation.md)：建立 LLM4Kernel、Agent4Kernel、数据与 benchmark 的统一框架。
3. [AscendKernelGen](papers/ascend-kernel-gen.md)：看领域数据、SFT/DPO 与 NPU 硬件 verifier。
4. [AscendCraft](papers/ascend-craft.md)：看专家 DSL 与多 pass transcompilation 路线。
5. [s1](papers/s1-test-time-scaling.md)：只用于理解如何控制 agent 的 test-time reasoning/iteration budget。
6. [Figure inventory](evidence/figure-inventory.md)：追溯正式原论文图、PDF 页码、crop bbox 与逐图 QA。

## 文档索引

- Evidence：[Paper index](evidence/paper-index.md)，[Figure inventory](evidence/figure-inventory.md)
- Papers：[Towards Automated Kernel Generation](papers/towards-automated-kernel-generation.md)，[AscendKernelGen](papers/ascend-kernel-gen.md)，[AscendCraft](papers/ascend-craft.md)，[s1](papers/s1-test-time-scaling.md)

## Obsidian Properties

本领域 `4/4` 篇 canonical Paper 已加入统一的 Obsidian YAML Properties：

- 共同标签：`paper`、`collection/kernel-agents`、`domain/agentic-workflows`、`status/deep-review`。
- 每篇另有一项 `topic/*` 和一项 `method/*`，分别表达研究问题与核心方法。
- 独立属性：`document_type`、`domain`、`collection`、`review_status`、`canonical`，用于 Properties view、Bases 和程序化筛选。
- 搜索示例：`tag:#collection/kernel-agents` 查看本领域全部精读；`tag:#topic/kernel-generation` 查看 kernel 生成主线。

## 证据边界

- PDF、提取文本、页面 render、裁剪过程和网络核验日志只保留在过程目录；正式文档不依赖这些临时材料。
- 原论文图按 paper owner 存入 `assets/papers/<slug>/`，并由 figure inventory 记录。
- 所有性能数字必须同时注明 reference、correctness gate、sampling budget、shape/dtype 与硬件边界；编译成功不能替代功能正确。
- GitHub/Hugging Face 的“开源”状态按核验日期与 commit/revision 记录；不可访问时明确标为未验证。
