# Kernel Agents

本目录保存 LLM/Agent 驱动 kernel 生成、NPU kernel 自动化和 test-time scaling 的论文笔记。

## 阅读顺序

1. [Paper index](evidence/paper-index.md)：先看论文清单和当前关注范围。
2. [Towards Automated Kernel Generation](papers/towards-automated-kernel-generation.md)：看 LLM4Kernel / Agent4Kernel 的整体范式。
3. [AscendKernelGen](papers/ascend-kernel-gen.md) 与 [AscendCraft](papers/ascend-craft.md)：看昇腾 NPU kernel generation 的数据、训练、DSL 和 transcompilation 路线。
4. [s1](papers/s1-test-time-scaling.md)：补充 test-time scaling 和 budget forcing 的方法线索。

## 文档索引

- Evidence：[Paper index](evidence/paper-index.md)
- Papers：[Towards Automated Kernel Generation](papers/towards-automated-kernel-generation.md)，[AscendKernelGen](papers/ascend-kernel-gen.md)，[AscendCraft](papers/ascend-craft.md)，[s1](papers/s1-test-time-scaling.md)

## 资产说明

- `assets/papers/towards-automated-kernel-generation/`：综述论文的范式图与定量分析图。
- `assets/papers/ascend-craft/`：AscendCraft 总览图。

## 维护规则

- 论文索引用 Markdown 链接指向本地笔记，避免只依赖 Obsidian wikilink。
- 图片引用使用相对 Markdown 图片路径，保留原始 pasted image 文件名。
- kernel agent 结论需要区分数据构建、SFT/RL、执行反馈、硬件闭环和 DSL/编译器边界。
