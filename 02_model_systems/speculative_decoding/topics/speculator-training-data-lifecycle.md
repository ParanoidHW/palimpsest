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

针对“response 是否必须提前离线处理，以及 SGLang/SpecForge 如何提取 hidden states”这组问题，准确答案分成三层：

1. **在标准 `speculators prepare-data` 训练入口之前，target 已生成的 response 行必须已经存在。** 这些行可以是已经包含 `input_ids` 与 `loss_mask` 的数据，也可以是带有 assistant response 的自然语言对话；`prepare-data` 只负责整理、分词和生成监督掩码，不会把只有 prompt 的任意数据自动变成 target 的 on-policy response。[官方文档事实]
2. **response 不要求人工提前写好，也不等于必须和 hidden states 一起离线生成。** Speculators 提供单独的 `regenerate-responses` 命令，可以调用 target 生成 response 后再进入 `prepare-data`；hidden states 则可选在线生成、离线落盘，或第一轮生成后缓存。[官方文档事实]
3. **当前 SpecForge 主线的 Online 也只表示 hidden states 在线提取，不表示 response 在同一个训练请求中在线 decode。** 若从 prompt-only 数据开始，官方脚本先独立调用 SGLang 生成 response 并写出逐行 JSON（JSON Lines，JSONL）；训练期 feature capture（特征捕获）随后提交完整 `input_ids`，显式设置 `max_new_tokens=0`，只做一次完整 prefill。[固定源码 + 官方文档事实]

因此，“response 要提前存在”是标准命令行接口（Command-Line Interface，CLI）的数据契约；“hidden states 要提前提取”只在 Offline 模式成立。把这两件事混为一谈，会错误地认为 Online 模式可以直接吃 prompt-only 数据，或者错误地认为 Online 模式也必须准备大规模 hidden-state 文件。[综合推论]

逐条来源、证据等级与未被证明的结论见[证据清单](../evidence/speculator-training-data-lifecycle.md)。

## 1. 先分清两个数据产品

### 1.1 Response 是什么

本文用 response 指训练行中的 assistant token 序列；“target-regenerated response”则特指 target model 针对 prompt、对话历史和生成配置实际采样出的序列。标准 Speculators 文档要求后一种 on-policy 数据。当前 SpecForge 训练入口也接受已有 assistant turn 的原始 conversation，但官方建议为了更好对齐 target 输出分布而重新生成 response。[官方文档事实]

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
| **SGLang SpecForge Online capture** | 训练入口读取已经含 assistant turn 的文件；从 prompt-only 开始时，response regeneration 是独立上游任务 | 训练期间对完整序列做一次强制 full prefill，`max_new_tokens=0` | 不落 `.ckpt`；临时写入 Mooncake 分布式对象存储，消费后释放 | 无需长期保存全量 hidden-state 文件，target 与 trainer 可分池 | target prefill、设备到主机（D2H）复制和网络传输进入训练关键路径 | 固定源码 + 官方文档事实 |
| **SGLang SpecForge Offline capture** | 同上 | 训练前由 `prepare_hidden_states.py` 提取 | 是，保存 `.ckpt` | 训练期不需要 target server | 预处理、磁盘和版本管理成本 | 固定源码 + 官方文档事实 |
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

## 4. SpecForge 当前主线的精确流程

本节固定核验 SpecForge commit [`3d64e7a`](https://github.com/sgl-project/SpecForge/tree/3d64e7a61f5fcc7f7d78ba6164c881f831943947)。这里的“Online”是训练期按需提取特征，不是 prompt-only 的生成与训练融合。[固定源码事实]

### 4.1 Response 是否独立生成

**如果输入只有 prompt，答案是明确的：当前官方路径把 response 生成作为训练前的独立任务。** `scripts/regenerate_train_data.py` 调用 SGLang 的 OpenAI-compatible chat completion 接口，逐个 user turn 生成 assistant message，再把完整 conversations 写入新的 JSONL。训练配置中的 `data.train_data_path` 读取这种已有 assistant turn 的 raw conversation；`data.prompts_path` 则读取已有 `input_ids` 与 `loss_mask` 的 tokenized JSONL。两个训练入口都不是 prompt-only generator。[固定源码 + 官方文档事实]

同一 commit 的 AMD 指南有一句文字声称 Online producer 会“regenerate full-length responses”，但这与实际 adapter 的 `max_new_tokens=0` 以及 file-backed prompt builder 直接冲突。本文保留这个冲突，并以可执行的固定源码确定运行语义：capture 请求不生成 response；该句更可能是文档漂移，或把独立上游 regeneration 宽泛地称为 producer 行为。[证据冲突 + 综合判断]

不过需要收紧“必须是 target 生成”这句话：

- 要在 response token 上抽取 target 的真实 hidden states，**必须先知道完整 token 序列**；否则没有 response 位置可供 teacher-forced prefill。[机制事实]
- 这些 token 不必在数学上由 target 自己采样。Target 可以对任意合法序列计算自己的真实 hidden states；SpecForge 也允许读取原始 conversation 数据。[固定源码事实]
- 若目标是让 drafter 对齐 target 的实际输出分布，官方文档推荐用 target 重新生成 assistant responses，并称这通常有利于 acceptance；但它同时指出 EAGLE 对数据质量并不高度敏感。因此 target regeneration 是推荐的分布对齐步骤，不是特征可计算性的硬约束。[官方文档转述]

### 4.2 在线特征提取的数据流

```text
已有 assistant response 的 JSONL
  -> tokenizer/chat template 构造完整 input_ids + loss_mask
  -> producer 租约 PromptTask
  -> patched SGLang /generate
       input_ids = prompt + response
       max_new_tokens = 0
       unique extra_key
  -> 对完整序列执行一次、非 chunked 的 full prefill
  -> attention tensor parallel (TP) rank 0 捕获 aux / final hidden states
  -> GPU 临时输出 -> 有上限的锁页主机内存缓冲区
  -> 后台 batch_put_from 写入 Mooncake
  -> HTTP 只返回 sample/key/shape/dtype 元数据
  -> trainer 按 SampleRef 读取、训练、确认消费、释放/垃圾回收
```

`unique extra_key` 的作用是隔离 radix cache 命名空间，确保即使服务器允许前缀缓存，每条训练样本仍执行完整 prefill。Capture patch 还要求关闭 chunked prefill，因为只保留最后一个 chunk 会丢失完整序列的 hidden rows。[固定源码事实]

所以，一旦 response 已经存在，结论就是：**特征提取只需一次 full prefill，不再做 decode。** 这里没有隐含的第二次 response generation，也没有在 capture 请求中追加一个 token。[固定源码事实]

### 4.3 Key-Value（KV）cache 与 hidden states 是否由“两套内存机制”管理

可以说部署中有**两条独立状态生命周期**，但不能说是 vanilla SGLang 内部两套同构 cache allocator：

| 维度 | 原始 KV cache | 草稿训练 hidden-state features |
|---|---|---|
| 直接用途 | 让同一请求的后续 decode token 复用历史 attention K/V | 作为 drafter 训练输入或监督特征 |
| 主要 owner | SGLang scheduler、token/KV memory pool、radix/paged cache | patched SGLang capture sink + SpecForge `MooncakeFeatureStore` + trainer |
| 典型内容 | 每层、每 token 的 K/V | 选定 auxiliary layers、final hidden，以及透传的 IDs/mask |
| 在线路径 | prefill 写入，decode 读取并追加；Prefill/Decode（PD）模式下跨 P/D worker 传输 | prefill 产生后进行设备到主机（D2H）复制，写入 Mooncake，trainer 按 sample key 拉取 |
| 生命周期 | request/cache policy、block allocation、prefix reuse/eviction | sample ID + generation + lease；训练消费后显式 release/abort，失败由垃圾回收（GC）重试 |
| 当前 capture 的处理 | 用 fresh `extra_key` 强制完整计算，不依赖已有 prefix 命中来省 prefill | 默认最多保留 2 个尚未完成传输的 host-side batch，达到上限后阻塞 producer 形成反压 |

两条路径可以都使用 Mooncake，但传输对象和释放条件完全不同。SGLang 的 Prefill/Decode（PD）分离传的是 KV cache；SpecForge 传给 trainer 的是训练 feature object。共享传输引擎不等于共享对象协议。[官方文档 + 固定源码事实]

### 4.4 如果坚持 prompt-only 的一体化 Online 流程

当前公开实现没有证明“response decode 与训练特征提取在一次 PD 流水线内完成”。可选设计有两种：[综合推论]

1. **两遍 target 计算，兼容当前实现。** 第一遍用普通 SGLang 或 PD 部署生成 response；把 response materialize 后，第二遍把 `prompt + response` 交给 capture server 做一次 full prefill。第二遍没有 decode，也不需要在 P/D worker 间传 hidden states，但需要额外承担一次完整 prefill。
2. **一遍生成并捕获，需要新增实现。** P worker 保存 prompt 部分 hidden states，D worker 在每个 decode step 保存新 token 的 hidden states，然后按 request ID、token position、target version 和 layer schema 合并并发送给 trainer。这需要独立的 feature allocation、跨 worker 传输、乱序重组、重试、backpressure、lease 和清理协议。

SpecForge 已经提供了第二类设计所需的一部分基础设施，例如 Mooncake feature store、sample generation、lease、release/abort 与垃圾回收；但当前 capture hook 只覆盖 full prefill，`max_new_tokens=0`，没有实现 decode-step hidden-state capture 和 P/D 结果拼接。因此不能把“已有独立 feature store”外推成“已经兼容一遍式 PD 生成 + 特征提取”。[固定源码事实 + 综合推论]

## 5. 对“是否必须提前离线处理 response”的精确回答

| 问题 | 答案 | 边界 |
|---|---|---|
| 是否必须提前准备 response 行？ | **是，对标准 `prepare-data` 是必须的。** | 这里的“提前”指进入该命令前已经可读，不要求人工制作。 |
| 是否必须提前把 response 存成自然语言？ | 否。 | 预分词的 `input_ids` 与 `loss_mask` 也可直接输入。 |
| 是否必须提前提取 hidden states？ | 否。 | Online 模式按需提取；Offline/Hybrid 才分别是全量预提取或首轮缓存。 |
| 是否必须是人工 ground-truth QA？ | 否。 | 标准 Speculators 使用 target-generated response；SpecForge 可读取其他 assistant turns，但它们不能自动视为 on-policy。 |
| 是否可以在一条大流水线里边生成 response 边训练？ | 可以，但那是 custom integration 或 TorchSpec/RL rollout 级别策略。 | 需要自己定义队列、版本、失败重试和 target/trainer 同步；不能把它描述成标准 `prepare-data` 行为。 |
| SpecForge Online capture 会顺便生成 response 吗？ | **不会。** | 固定源码设置 `max_new_tokens=0`；输入已经是完整 token 序列。 |
| SpecForge 从 prompt-only 开始时，response 是否独立生成？ | **官方路径是独立生成并写出 JSONL。** | 可由其他上游数据系统替代，但训练入口本身不做。 |
| 已有 response 后还要 decode 吗？ | **不需要。** | Capture 对 `prompt + response` 做一次 full prefill。 |
| SpecForge 已实现 PD 下的一遍生成与 hidden-state capture 吗？ | **当前固定版本没有这项代码证据。** | 现有 producer/consumer 分离不是 P/D 分离；二者不要混称。 |

## 6. 选择策略时真正比较什么

### 6.1 精度与接受长度

现有公开资料证明了输入契约和数据传输方式，但没有提供一个在同一 target、同一 response 集、同一训练步数与同一硬件预算下，对 Online、Offline、Hybrid、TorchSpec 和 RL 集成路径的统一精度或 accepted length 因果比较。[证据边界]

更稳妥的推论是：在 fixed-target 场景中，只要 response、hidden-state 层和训练配方一致，Online 与 Offline 的主要差别应首先体现在数据生成时机、缓存一致性和系统成本，而不是由“在线”这个标签自动带来精度收益。[综合推论]

### 6.2 总训练耗时

总耗时应拆成 response generation、`prepare-data`、hidden-state extraction、drafter optimization、数据传输与缓存读写。Offline 把 extraction 前置并释放 target 加速卡；Online 省去完整落盘但让 target 资源持续驻留；Hybrid 让第一次生成成本服务多个 epoch。哪个更快取决于 target/drafter 的资源比例、序列长度、存储带宽和 epoch 数，不能仅凭框架名称排序。[综合推论]

### 6.3 RL 场景的额外变量

RL rollout 的 target policy 会变化，旧 response 或旧 hidden states 可能对应旧 checkpoint。把固定-target 的 Offline 缓存直接复用于变化中的 policy，可能导致 drafter loss 与当前 acceptance 脱钩；这是版本管理和稳定性风险，不是标准 Speculators 文档声称的性能结果。[综合推论]

## 7. 工程落地建议

1. 先确定最终 serving 的 target checkpoint、tokenizer、chat template、sampling 配置和 hidden-state 层，再生成 response 行；这些字段应和数据一起记录。
2. 如果目标是跑通标准 Speculators Online，准备 target-generated、预分词的 `input_ids` 与 `loss_mask` 即可，不必先做全量 hidden-state 文件。
3. 如果 target 卡紧张、训练 epoch 多或需要复现实验，选择 Offline 或 Hybrid，并为 hidden-state 文件记录 target 版本、层 ID、序列长度和数据行 ID。
4. 如果需要 target inference 与 drafter training 解耦，参考 TorchSpec 的流式 producer-consumer 设计；不要把“流式 hidden states”误写成“无需 response 数据”。
5. 如果 response 由 RL rollout 产生，保留 policy step/checkpoint ID，限制 replay 跨度，并单独评估 acceptance、drafter loss、rollout wall-clock 和最终质量。
6. 对 SpecForge Online，不要把 capture server 的 producer/trainer 分池写成 PD 分离。若需要 prompt-only 的一体化生成，先选择“两遍计算”还是“decode-step feature capture”，再据此设计状态所有权和容量预算。

## 8. 证据等级与未证明事项

- **官方文档事实：** Speculators 要求输入包含 target response；`prepare-data` 不生成 response；Online、Offline、Hybrid 只改变 hidden-state 的来源与缓存方式；`regenerate-responses` 是独立的 target response 生产步骤。
- **Paper/技术报告与代码事实：** TorchSpec 将 target inference 与 draft optimization 组织成可流式传输的 producer-consumer 系统；已有 canonical Paper 已记录其性能归因边界。
- **论文实证：** RL rollout 论文报告了各自系统下的 rollout 或端到端加速，但这些数字不是对 Speculators 三种 hidden-state 模式的匹配比较。
- **综合推论：** response 与 hidden states 是两个独立生命周期；选择 Online/Offline/Hybrid 首先是资源、缓存和复现性决策；RL 中的缓存版本跨度会带来稳定性风险。
- **当前没有统一证据：** 哪条路径在相同 GPU-hours 下必然获得更高 drafter 精度、更长 accepted length 或更短总训练时间。
- **当前 SpecForge 固定源码事实：** response regeneration 是独立脚本；Online capture 输入完整 `input_ids`，设置 `max_new_tokens=0`，执行一次 full prefill；hidden states 经 bounded host buffer 写入 Mooncake，并由独立 feature-store 生命周期管理。
- **当前没有代码证据：** SpecForge 已把 prompt-only response decode、SGLang PD KV transfer、decode-step hidden-state capture 与 trainer feature stream 合并为一次端到端执行。
