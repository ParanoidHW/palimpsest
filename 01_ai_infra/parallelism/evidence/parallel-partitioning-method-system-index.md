---
tags:
  - evidence
  - collection/parallel-partitioning
  - domain/ai-infra
document_type: evidence
domain: parallelism
canonical: true
---

# 并行切分方法与系统索引

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 方法体系：[并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md)
> - 选型指南：[并行策略选型](../surveys/parallel-strategy-selection.md)

## 1. Canonical Papers

| Method | Canonical Paper | Mechanism | Primary communication |
|---|---|---|---|
| TP | [Megatron-LM](../papers/megatron-lm.md) | column→row GEMM/head partition | all-reduce |
| PP | [GPipe](../papers/gpipe.md) | layer stages + micro-batches | send/recv |
| State sharding | [ZeRO](../papers/zero.md) | optimizer/gradient/parameter shard | gather/reduce-scatter |
| EP / sharding compiler | [GShard](../papers/gshard.md) | expert shard + token route | all-to-all |
| Ulysses-SP | [DeepSpeed Ulysses](../papers/deepspeed-ulysses.md) | sequence↔head layout transpose | all-to-all |
| Ring-SP/CP | [Ring Attention](../papers/ring-attention.md) | local Q + rotating KV | ring P2P |

## 2. Frameworks

| Entity | Evidence class | Relevant abstractions | Version boundary |
|---|---|---|---|
| NVIDIA Megatron Core | official docs + code | TP、PP、DP、EP、CP、sequence parallel | current docs/code；不等于 2019 Paper |
| DeepSpeed | official docs + code | ZeRO、Ulysses | current repo；不等于 SC20/2023 全部实验 |
| PyTorch DTensor TP | official docs | `ColwiseParallel`、`RowwiseParallel`、`SequenceParallel` | API 可演进 |
| PyTorch DTensor CP | official docs | `context_parallel`、buffer placement | API 可演进 |
| Ring Attention JAX | official paper repo | blockwise ring forward/backward | commit 由 Paper 固定 |

## 3. 扩展方法

以下工作可作为后续增量选篇候选：

- Megatron-LM 2021 cluster-scale 3D parallelism；
- PipeDream/1F1B/interleaved pipeline；
- FSDP 与 ZeRO-Infinity；
- Switch Transformer、Tutel、DeepSpeed-MoE；
- DistFlashAttn、USP、LoongTrain、Striped Attention；
- Alpa、GSPMD、DTensor、XLA SPMD partitioner；
- topology-aware and heterogeneous parallel runtimes。

它们当前只作为方法图谱扩展，不在本轮计入六篇独立精读。

## 4. 证据分类

- `paper mechanism`：定义算法和数学语义；
- `official code`：核验当前实现路径；
- `official docs`：核验当前 API/adoption；
- `native component`：系统内建的一等能力；
- `optional backend`：官方可选集成；
- `third-party integration`：非上游采用；
- `mention-only`：仅在文档或列表出现。

数量统计必须按这些单位分开，不能把 Paper、repository 和 backend 混为“采用数”。
