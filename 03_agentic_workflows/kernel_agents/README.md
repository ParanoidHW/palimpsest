# Kernel Agents

本目录保存 LLM/Agent 驱动 kernel 生成、NPU kernel 自动化和 test-time scaling 的论文笔记。

## 阅读顺序

1. [Awesome Papers on LLM&Agent for kernel](0.%20Awesome%20Papers%20on%20LLM&Agent%20for%20kernel.md)：先看论文索引和当前关注列表。
2. [Towards Automated Kernel Generation in the Era of LLMs](Towards%20Automated%20Kernel%20Generation%20in%20the%20Era%20of%20LLMs.md)：看 LLM4Kernel / Agent4Kernel 的整体范式。
3. [AscendKernelGen](AscendKernelGen.md) 与 [AscendCraft](AscendCraft.md)：看昇腾 NPU kernel generation 的数据、训练、DSL 和 transcompilation 路线。
4. [s1 Simple test-time scaling](s1%20Simple%20test-time%20scaling.md)：补充 test-time scaling 和 budget forcing 的方法线索。

## 资产说明

- `assets/Pasted image 20260614204147.png`、`assets/Pasted image 20260614204608.png`、`assets/Pasted image 20260614204647.png`、`assets/Pasted image 20260614204218.png`：由 Towards Automated Kernel Generation 笔记引用。
- `assets/Pasted image 20260614223507.png`：由 AscendCraft 笔记引用。

## 维护规则

- 论文索引用 Markdown 链接指向本地笔记，避免只依赖 Obsidian wikilink。
- 图片引用使用相对 Markdown 图片路径，保留原始 pasted image 文件名。
- kernel agent 结论需要区分数据构建、SFT/RL、执行反馈、硬件闭环和 DSL/编译器边界。
