# 扩散语言模型与 Serving

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[Diffusion](../README.md)
> - 下位精读：[Nemotron-Labs-Diffusion](../papers/nemotron-labs-diffusion.md)
> - 证据索引：[Paper index](../evidence/paper-index.md) · [Figure inventory](../evidence/figure-inventory.md)

![扩散语言模型、dLLM Serving 与 Diffusion Draft 模型进展](../assets/language_dllm_draft_2026_map.svg)

## 范围与判断

本页关注离散/掩码扩散语言模型、block diffusion、diffusion drafting、self-speculation、候选验证、KV cache 与 serving。分类以模型的主要建模机制为准：Nemotron-Labs-Diffusion 的上位归属是 diffusion；其 self-speculation 作为下游推理模式与 speculative decoding 形成交叉。

2025 年后，这条路线的竞争不再只是“并行预测几个 token”，而是训练目标、噪声/掩码覆盖、候选接受、cache 语义、调度和硬件 kernel 的联合优化。TPF 高不必然等于 tok/s 高；任何加速结论都应同时给出模型质量、硬件、精度、并发和实现栈。

## 核心论文

| 工作 | 核心机制 | 关键证据 | 解读 |
|---|---|---|---|
| Nemotron-Labs-Diffusion | 同一参数切换 causal/bidirectional attention，统一 AR、block diffusion 与 self-speculation | 完整训练配方相对 blockwise baseline 平均 +16.05 点；Instruct 8B 的 linear/quadratic self-spec 为 5.99/6.38 TPF；系统峰值依条件最高约 3.3× | [深入解读](../papers/nemotron-labs-diffusion.md) |

## 读数原则

1. 先区分 **接受长度/TPF** 与 **墙钟吞吐**。
2. 再检查比较是否匹配硬件、量化、batch、prompt/output length 与 kernel。
3. 对累积消融只归因到“配方整体”与相邻增量，不把它当独立因果效应。
4. 对 self-speculation 同时核查 drafter 是否共享权重、是否共享 KV、verify 是否保持精确 AR 语义。

## 研究空白

- 统一训练多种 attention semantics 时的优化干扰仍缺少系统理论。
- 共享完整模型作 drafter 能省权重，但 draft forward 仍重；何时优于独立小 drafter取决于硬件与并发。
- 需要跨温度、长上下文和多轮对话的质量—吞吐曲线。
- serving scheduler 应根据负载动态选 AR/diffusion/self-spec，而现有论文多给静态工作点。

