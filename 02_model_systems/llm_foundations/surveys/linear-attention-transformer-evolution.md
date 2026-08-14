---
tags:
  - survey
  - collection/llm-foundations
  - domain/model-systems
  - status/deep-review
  - topic/long-context
  - method/hybrid-linear-attention
document_type: survey
domain: llm_foundations
collection: LLM Foundations
review_status: blocked-with-usable-system-synthesis
canonical: true
---

# Linear Attention Transformer 演化

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[LLM Foundations README](../README.md)
> - 证据索引：[Linear attention evidence](../evidence/linear-attention-transformer-evidence.md)
> - 相关 Paper：[Kimi K3](../papers/kimi-k3.md)

## 结论

线性注意力的演化不是从 softmax attention 直接替换为单一算子，而是经历了四步：feature-map 重排把前缀交互压成固定状态；retention/GLA 引入衰减与门控；DeltaNet/Gated DeltaNet 引入 erase-then-write 的内容寻址；近期模型采用 hybrid attention，用少量 full-attention 层补回精确检索能力。

Qwen3-Next-80B-A3B 使用 48 层、每 4 层一个周期的 `3 Gated DeltaNet + 1 Gated Attention`，linear branch 配置为 16 个 QK heads、32 个 V heads、128 维 head 和 4-token causal conv，原生 262,144 context。Kimi K3 使用 69 层 KDA + 24 层 Gated MLA，KDA 采用 bounded log-decay 与 delta-rule 状态更新，并配套 FlashKDA、KCP 和双粒度 prefix cache；这些机制与既有 [Kimi K3 精读](../papers/kimi-k3.md) 的原始图表证据相连。

## 方法谱系

| 阶段 | 代表工作 | 状态语义 | 系统变化 |
|---|---|---|---|
| 2020 | Linear Transformer | feature-map 外积前缀状态 | 线性序列复杂度，表达力与归一化受限 |
| 2023 | RetNet | decayed retention state | parallel/recurrent/chunkwise 三路执行 |
| 2023/24 | Mamba | 输入依赖 selective SSM | content-based forget 与专用 scan；不是严格 linear attention |
| 2023/24 | GLA | gated matrix state | FlashLinearAttention 解决 I/O 与 chunkwise kernel |
| 2024/25 | DeltaNet/Gated DeltaNet | delta erase/write + gate | 解决记忆冲突并成为 Qwen3-Next 的 linear branch |
| 2026 | Kimi K3 KDA | bounded decay + delta write | 69:24 KDA/MLA hybrid，面向 1M context serving |

## 系统判断

- 收敛方向：多数层用固定状态降低 KV/HBM 流量，少量 full attention 作为内容寻址锚点。
- 关键瓶颈：状态更新必须支持 chunk/tile、Tensor Core、数值稳定和跨 rank 可组合；理论 $O(N)$ 不自动等于端到端吞吐。
- 证据边界：本次新增六篇方法 Paper 的 PDF/source/code deep-review 在隔离环境中受网络限制而 blocked；方法细节应视为带限制的机制导航。Qwen3-Next 官方 config/model card 与 Kimi K3 canonical Paper 的系统结构证据可用。

完整演化、公式、Qwen/Kimi KDA 细节和阻断记录保留在本任务 process workspace；正式 Paper/Asset 不复制过程文件。
