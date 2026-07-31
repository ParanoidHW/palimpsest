---
tags:
  - evidence
  - collection/parallel-partitioning
  - domain/ai-infra
document_type: evidence
domain: parallelism
canonical: true
---

# 并行切分选篇与影响力证据

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 上位 Survey：[并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md)
> - 系统索引：[方法与系统索引](parallel-partitioning-method-system-index.md)

## 1. 选择目标

本轮选择六篇 Paper，覆盖“切什么、怎么切、在哪里通信、开销是什么”的六个基础轴：

| Paper | 轴 | 选择理由 | 判决 |
|---|---|---|---|
| [Megatron-LM](../papers/megatron-lm.md) | TP | column/row parallel 与 collective 边界 | accepted |
| [GPipe](../papers/gpipe.md) | PP | layer/stage、micro-batch、bubble | accepted-with-limitations |
| [ZeRO](../papers/zero.md) | state sharding | \(O/G/P\) 三阶段与 DP 关系 | accepted-with-limitations |
| [GShard](../papers/gshard.md) | EP / compiler | expert dispatch 与 sharding annotation | accepted-with-limitations |
| [DeepSpeed Ulysses](../papers/deepspeed-ulysses.md) | Ulysses-SP | sequence/head all-to-all transpose | accepted-with-limitations |
| [Ring Attention](../papers/ring-attention.md) | Ring-SP/CP | local Q、rotating KV、online softmax | accepted-with-limitations |

覆盖矩阵在选篇前按标题、简称、arXiv ID、模型名和别名查询，六篇均未命中现有 canonical Paper。

## 2. Link-only

以下工作已有 canonical 分析，本领域只链接：

- [DeepSeek-V4](../../../02_model_systems/llm_foundations/papers/deepseek-v4.md)
- [Kimi K3](../../../02_model_systems/llm_foundations/papers/kimi-k3.md)
- [SwiftFusion](../../../02_model_systems/multimodal_generation/papers/swiftfusion.md)
- [Cosmos 3](../../../02_model_systems/multimodal_generation/papers/cosmos-3.md)
- [Causal-rCM](../../../02_model_systems/multimodal_generation/papers/causal-rcm.md)
- [MAGI-1](../../../02_model_systems/multimodal_generation/papers/magi-1.md)
- [DSV](../../kernel/custom_attn/papers/dsv.md)
- [LVSA](../../kernel/custom_attn/papers/lvsa.md)

## 3. 易变影响力信号

> 访问日期：2026-07-31。数值仅用于解释选篇影响力，不证明技术正确性。

| Work | OpenAlex citations | 角色 |
|---|---:|---|
| Megatron-LM | 828 | TP 奠基 |
| GPipe | 236 | PP 奠基 |
| ZeRO | 774 | 状态切分奠基 |
| GShard | 351 | EP/自动切分桥梁 |
| DeepSpeed Ulysses | 7 | 长序列核心机制 |
| Ring Attention | 13 | 长序列核心机制 |

Semantic Scholar API 本次多数返回 429，且一次 GPipe 搜索疑似错配，因此未作为引用交叉源。

## 4. 官方实现信号

| Repository | Stars | Forks | Last pushed | Accessed |
|---|---:|---:|---|---|
| NVIDIA/Megatron-LM | 17,265 | 4,311 | 2026-07-31 | 2026-07-31 |
| deepspeedai/DeepSpeed | 42,837 | 4,921 | 2026-07-31 | 2026-07-31 |
| haoliuhl/ringattention | 773 | 52 | 2025-10-13 | 2026-07-31 |

实现采用与论文版本分开记录。当前 Megatron/DeepSpeed 功能不能自动回填为 2019/2020 论文证据。

## 5. 访问限制

- GPipe：未冻结 Lingvo code snapshot。
- ZeRO：现代 DeepSpeed clone 未完成。
- GShard、Ring Attention：OpenReview review/rebuttal 文本被 403/browser challenge 阻断。
- Ulysses：只核验有限官方文件/commit；headline speedup 为混合系统收益。
