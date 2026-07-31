---
tags:
  - evidence
  - collection/parallel-partitioning
  - domain/ai-infra
document_type: evidence
domain: parallelism
canonical: true
---

# 并行切分主张—证据矩阵

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 方法体系：[并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md)
> - Figure provenance：[Figure inventory](figure-inventory.md)

| Claim | Primary evidence | Control | Strength | Accepted interpretation |
|---|---|---|---|---|
| column→row TP 可让 GeLU/head-local | [Megatron-LM Eq./Figure 3](../papers/megatron-lm.md#42-列并行与行并行到底切哪个维度) | 代数/机制 | direct | 机制成立 |
| Megatron 8-way TP 77% weak scaling | [Figure 5](../papers/megatron-lm.md#51-扩展效率证据) | 模型随设备变化 | system | 不等于固定模型 speedup |
| micro-batch 摊薄 PP bubble | [GPipe F3/Table 2](../papers/gpipe.md#43-关键公式) | \(M\) sensitivity；batch 可调整 | partial | \(M/K\) 趋势成立 |
| ZeRO 三阶段按 \(O/G/P\) 降状态内存 | [ZeRO Figure 1/F1](../papers/zero.md#41-三阶段与训练步内状态流) | theory + mechanism | direct | 平均状态内存，不等于峰值 |
| ZeRO headline speedup | [ZeRO Figure 2](../papers/zero.md#51-主结果与口径) | baseline/GPU 数不完全匹配 | confounded | full-system capacity/throughput |
| GShard experts shard、普通层复制 | [GShard Figure 3](../papers/gshard.md#42-专家并行与通信的准确位置) | mechanism | direct | placement 成立 |
| GShard all-to-all 随 expert scale 成压力 | [GShard Figure 8](../papers/gshard.md#52-系统性能证据) | measured/roofline | system | dispatch/combine 是主要扩展压力 |
| Ulysses sequence↔head transpose | [Ulysses Figure 2/code](../papers/deepspeed-ulysses.md#42-精确-layout-与前反向通信) | mechanism/code | direct | 均匀 head 路径成立 |
| Ulysses 2.5× 来自 all-to-all | [Ulysses results](../papers/deepspeed-ulysses.md#51-主结果与边界) | ZeRO/SP/config 同变 | weak | 只能归因系统 bundle |
| Ring online merge 是精确 attention | [Ring F1/F2/code](../papers/ring-attention.md#43-关键公式) | theory/code | direct | 浮点顺序差异不等于近似算法 |
| Ring communication 可零开销 | [Ring F3/Table 4](../papers/ring-attention.md#43-关键公式) | 无 overlap-off 消融 | partial | 只在 block/topology 条件下 |
| Ring context 随设备数扩展 | [Ring Table 3](../papers/ring-attention.md#51-最大上下文长度) | 设备资源同步变化 | capacity | tested configs 支持 |
| causal Ring 与 non-causal 同样均衡 | [Ring code/analysis](../papers/ring-attention.md#44-causal-mask-与负载边界) | 无论文对比 | unsupported | 存在三角 imbalance 风险 |
| custom shard 一定更快 | 跨域案例 | 缺统一 matched baseline | unsupported as universal | 必须逐 operator/profile 判断 |

## 证据等级

- `direct`：代数、机制或 matched implementation 直接核验；
- `system`：端到端配置支持，但组件归因混杂；
- `partial`：理论 + 间接结果，缺匹配消融；
- `code-only`：当前实现存在，论文未验证；
- `unsupported`：不能从现有证据接受。

## 跨论文推断

以下是本 Survey 的综合推断，不是单篇论文原话：

- 选择并行轴等价于选择 global-to-local placement 与 redistribution；
- 多轴组合的收益不会独立相乘；
- communication overlap 是受 block、kernel、topology 和 balance 约束的条件命题；
- operator-specific shard 的主要价值常是移动 collective 或减少 reshard。
