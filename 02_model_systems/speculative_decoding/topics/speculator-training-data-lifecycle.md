---
tags:
  - topic/speculator-training-data
  - collection/speculative-decoding
  - domain/model-systems
document_type: topic
domain: model-systems
collection: speculative-decoding
review_status: maintained
canonical: true
---

# Speculator 训练的数据生命周期与框架策略

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[投机解码的基础合同与机制分类](../surveys/foundations-and-trends.md)
> - 证据资产：[框架策略证据清单](../evidence/speculator-training-data-lifecycle.md)
> - 相关 Paper：[TorchSpec](../papers/torchspec.md)
> - 相关 Topic：[RL 期间的 drafter 联合适配](rl-drafter-cotraining.md)

## 结论先行

针对“vLLM Speculators 的 response 是否必须提前离线处理”这个问题，准确答案分成两层：

1. **在标准 `speculators prepare-data` 训练入口之前，target 已生成的 response 行必须已经存在。** 这些行可以是已经包含 `input_ids` 与 `loss_mask` 的数据，也可以是带有 assistant response 的自然语言对话；`prepare-data` 只负责整理、分词和生成监督掩码，不会把只有 prompt 的任意数据自动变成 target 的 on-policy response。[官方文档事实]
2. **response 不要求人工提前写好，也不等于必须和 hidden states 一起离线生成。** Speculators 提供单独的 `regenerate-responses` 命令，可以调用 target 生成 response 后再进入 `prepare-data`；hidden states 则可选在线生成、离线落盘，或第一轮生成后缓存。[官方文档事实]

因此，“response 要提前存在”是标准 CLI 的数据契约；“hidden states 要提前提取”只在 Offline 模式成立。把这两件事混为一谈，会错误地认为 Online 模式可以直接吃 prompt-only 数据，或者错误地认为 Online 模式也必须准备大规模 hidden-state 文件。[综合推论]

逐条来源、证据等级与未被证明的结论见[证据清单](../evidence/speculator-training-data-lifecycle.md)。

## 1. 先分清两个数据产品

### 1.1 Response 是什么

这里的 response 是 target model 针对某个 prompt、对话历史和生成配置实际采样出的 assistant token 序列。它不是人工标准答案，也不是任意其他模型产生的回答。Speculators 的文档接受两种输入：已经带 `input_ids` 和 `loss_mask` 的 speculator-format 行，或包含 target response 的自然语言对话。[官方文档事实]

### 1.2 Hidden states 是什么

hidden states 是 target 在这些 token 上产生的内部表示，供 drafter 训练使用。它们必须和 token 顺序、target checkpoint、tokenizer、chat template 以及抽取层配置相互对齐；hidden-state 提取不会替代 response 生成。[综合推论]

### 1.3 `prepare-data` 做什么、不做什么

自然语言对话需要通过 target 的 render endpoint 应用 serving chat template、分词并推导 assistant-turn 的 loss mask；已经预分词的数据则可直接复用自己的 `input_ids` 与 `loss_mask`。官方实现明确说明 render 只是转换表示，不会生成 response，也不会把 arbitrary conversation 变成 on-policy 数据。[官方文档事实]

## 2. 公开框架的策略对比

| 框架/路径 | response 何时产生 | hidden states 何时产生 | 是否要落盘 hidden states | 主要收益 | 主要代价 | 证据等级 |
|---|---|---|---|---|---|---|
| **vLLM Speculators Online** | 在 `prepare-data` 前已由 target 生成；可来自 `regenerate-responses` 或外部 on-policy pipeline | 训练读取样本时由 live vLLM 按需生成，用完丢弃 | 否 | 节省大规模缓存空间，hidden states 跟随当前 live target | 训练期间占用 target serving 资源，target 不可用时训练停顿 | 官方文档事实 |
| **vLLM Speculators Offline** | 同上，必须先有 target response 行 | 训练前由 target 批量生成并保存 | 是 | 训练阶段可释放 target 加速卡，结果可复放 | 磁盘、预处理时间和版本管理成本高 | 官方文档事实 |
| **vLLM Speculators Hybrid** | 同上 | 第一个 epoch 按需生成，随后缓存复用 | 第一个 epoch 后是 | 兼顾首次生成和后续复用 | 首轮仍占 target 资源，缓存失效规则要清楚 | 官方文档事实 |
| **SGLang SpecForge** | 取决于选用的训练 recipe；现有 D²SD 代码证据使用 target 生成的数据行 | 由具体算法 recipe 决定，不能从框架名推定 Online/Offline | 由 recipe 决定 | 与 SGLang serving 路径贴近，便于做训练-推理语义对齐 | 不同算法支持度不均，需按固定 revision 核验训练 glue 和 hidden-state 路径 | Paper/代码分析 |
| **TorchSpec train-with-decode** | target inference group 可在训练流水线中持续生成 | 通过 producer-consumer 流直接传给 draft trainer | 主路径避免完整离线 materialization | target 推理组与训练组可独立扩缩，长序列不必先做百 TB 级缓存 | 网络、队列、backpressure 和分布式运维更复杂 | Paper/技术报告与代码分析 |
| **RL rollout 集成路径** | 当前 policy 在 rollout 中产生 response | rollout 或 trainer 即时消费当前 policy 的表示，具体实现各异 | 由 replay/cache 策略决定 | 数据天然贴近变化中的 policy，减少固定 drafter 失配 | policy drift、版本混用和训练稳定性需要额外控制 | Paper 实证 + 综合推论 |

表中“response 已存在”只针对标准 Speculators CLI；TorchSpec 或 RL 系统可以把 response generation 放进更大的在线流水线，但这不改变标准 `prepare-data` 本身不负责采样 response 的事实。[综合推论]

## 3. 标准 Speculators 的实际时序

### 路径 A：已有 target response 的数据

```text
target response rows
  -> prepare-data
  -> input_ids + loss_mask + token statistics
  -> Online / Offline / Hybrid hidden-state strategy
  -> drafter training
```

如果上游已经保存了 `input_ids` 与 `loss_mask`，`prepare-data` 可跳过 render endpoint；这就是官方 Online 示例所采用的“预先 tokenized、训练时只在线取 hidden states”路径。[官方文档事实]

### 路径 B：只有 prompt 或原始对话

```text
prompt / raw conversations
  -> target vLLM + regenerate-responses
  -> target response rows
  -> prepare-data
  -> Online / Offline / Hybrid hidden-state strategy
```

`regenerate-responses` 是 response 生成步骤，不是 hidden-state feature extraction。它可以在训练前运行，也可以作为更大系统中的数据生产服务运行；但标准 `prepare-data` 仍接收已经产生的行。[官方文档事实]

## 4. 对“是否必须提前离线处理 response”的精确回答

| 问题 | 答案 | 边界 |
|---|---|---|
| 是否必须提前准备 response 行？ | **是，对标准 `prepare-data` 是必须的。** | 这里的“提前”指进入该命令前已经可读，不要求人工制作。 |
| 是否必须提前把 response 存成自然语言？ | 否。 | 预分词的 `input_ids` 与 `loss_mask` 也可直接输入。 |
| 是否必须提前提取 hidden states？ | 否。 | Online 模式按需提取；Offline/Hybrid 才分别是全量预提取或首轮缓存。 |
| 是否必须是人工 ground-truth QA？ | 否。 | 文档契约是 target-generated response；人工答案可作为实验数据，但不能自动视为 on-policy。 |
| 是否可以在一条大流水线里边生成 response 边训练？ | 可以，但那是 custom integration 或 TorchSpec/RL rollout 级别策略。 | 需要自己定义队列、版本、失败重试和 target/trainer 同步；不能把它描述成标准 `prepare-data` 行为。 |

## 5. 选择策略时真正比较什么

### 5.1 精度与接受长度

现有公开资料证明了输入契约和数据传输方式，但没有提供一个在同一 target、同一 response 集、同一训练步数与同一硬件预算下，对 Online、Offline、Hybrid、TorchSpec 和 RL 集成路径的统一精度或 accepted length 因果比较。[证据边界]

更稳妥的推论是：在 fixed-target 场景中，只要 response、hidden-state 层和训练配方一致，Online 与 Offline 的主要差别应首先体现在数据生成时机、缓存一致性和系统成本，而不是由“在线”这个标签自动带来精度收益。[综合推论]

### 5.2 总训练耗时

总耗时应拆成 response generation、`prepare-data`、hidden-state extraction、drafter optimization、数据传输与缓存读写。Offline 把 extraction 前置并释放 target 加速卡；Online 省去完整落盘但让 target 资源持续驻留；Hybrid 让第一次生成成本服务多个 epoch。哪个更快取决于 target/drafter 的资源比例、序列长度、存储带宽和 epoch 数，不能仅凭框架名称排序。[综合推论]

### 5.3 RL 场景的额外变量

RL rollout 的 target policy 会变化，旧 response 或旧 hidden states 可能对应旧 checkpoint。把固定-target 的 Offline 缓存直接复用于变化中的 policy，可能导致 drafter loss 与当前 acceptance 脱钩；这是版本管理和稳定性风险，不是标准 Speculators 文档声称的性能结果。[综合推论]

## 6. 工程落地建议

1. 先确定最终 serving 的 target checkpoint、tokenizer、chat template、sampling 配置和 hidden-state 层，再生成 response 行；这些字段应和数据一起记录。
2. 如果目标是跑通标准 Speculators Online，准备 target-generated、预分词的 `input_ids` 与 `loss_mask` 即可，不必先做全量 hidden-state 文件。
3. 如果 target 卡紧张、训练 epoch 多或需要复现实验，选择 Offline 或 Hybrid，并为 hidden-state 文件记录 target 版本、层 ID、序列长度和数据行 ID。
4. 如果需要 target inference 与 drafter training 解耦，参考 TorchSpec 的流式 producer-consumer 设计；不要把“流式 hidden states”误写成“无需 response 数据”。
5. 如果 response 由 RL rollout 产生，保留 policy step/checkpoint ID，限制 replay 跨度，并单独评估 acceptance、drafter loss、rollout wall-clock 和最终质量。

## 7. 证据等级与未证明事项

- **官方文档事实：** Speculators 要求输入包含 target response；`prepare-data` 不生成 response；Online、Offline、Hybrid 只改变 hidden-state 的来源与缓存方式；`regenerate-responses` 是独立的 target response 生产步骤。
- **Paper/技术报告与代码事实：** TorchSpec 将 target inference 与 draft optimization 组织成可流式传输的 producer-consumer 系统；已有 canonical Paper 已记录其性能归因边界。
- **论文实证：** RL rollout 论文报告了各自系统下的 rollout 或端到端加速，但这些数字不是对 Speculators 三种 hidden-state 模式的匹配比较。
- **综合推论：** response 与 hidden states 是两个独立生命周期；选择 Online/Offline/Hybrid 首先是资源、缓存和复现性决策；RL 中的缓存版本跨度会带来稳定性风险。
- **当前没有统一证据：** 哪条路径在相同 GPU-hours 下必然获得更高 drafter 精度、更长 accepted length 或更短总训练时间。
