# Speculator 训练数据生命周期证据清单

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[投机解码的基础合同与机制分类](../surveys/foundations-and-trends.md)
> - 支持 Topic：[Speculator 训练的数据生命周期与框架策略](../topics/speculator-training-data-lifecycle.md)
> - 相关 Paper：[TorchSpec](../papers/torchspec.md)

## 资料边界

- 核验日期：`2026-09-12`。
- 本清单只核验 response 是否需要在标准训练入口前存在、hidden-state 的 Online/Offline/Hybrid 选项，以及公开框架对这两个阶段的编排方式。
- `官方文档事实`、`Paper/技术报告事实`、`论文实证` 与 `综合推论` 分开记录；综合推论不伪装成单一来源的实验结果。

## 来源登记

| ID | 类型 | 来源 | 支持的内容 | 不支持的内容 |
|---|---|---|---|---|
| `S1` | 官方文档 | [Speculators training tutorial](https://docs.vllm.ai/projects/speculators/en/latest/user_guide/tutorials/train/) | target response 输入契约；Online、Offline、Hybrid 的 hidden-state 时序 | 不支持跨模式的统一精度/总耗时因果比较 |
| `S2` | 官方文档 | [prepare-data CLI reference](https://github.com/vllm-project/speculators/blob/main/docs/cli/prepare_data.md) | render 只转换已有对话；`input_ids` 与 `loss_mask` 可直接输入 | 不支持把 prompt-only 数据自动变成 on-policy response |
| `S3` | 官方文档 | [response regeneration CLI reference](https://github.com/vllm-project/speculators/blob/main/docs/cli/response_regeneration.md) | 可调用 target 生成 response 行，再供训练使用 | 不支持把 regeneration 等同于 hidden-state extraction |
| `S4` | 固定源码 | [vllm-project/speculators commit `35081a4`](https://github.com/vllm-project/speculators/tree/35081a47fa5881504c35ad9a7be25af742b91e52) | `prepare_data.py`、preprocessing、hidden-state client 与 connector 的实现边界 | 不支持推导其他版本或其他后端的性能 |
| `S5` | Paper/技术报告 | [TorchSpec canonical analysis](../papers/torchspec.md) 与 [PyTorch technical report](https://pytorch.org/blog/torchspec-speculative-decoding-training-at-scale/) | disaggregated target inference、流式 hidden-state producer-consumer 设计及其证据局限 | 不支持 TorchSpec 对 Speculators 模式的匹配 benchmark |
| `S6` | 论文 | [Training-Free Speculative Decoding for RL Rollouts](https://arxiv.org/abs/2511.16665) | RL rollout 中把当前 policy 产生的数据接入投机路径的系统级对比 | 不支持固定-target Speculators 数据契约，也不支持统一训练时长排序 |
| `S7` | Paper/代码分析 | [D2SD canonical analysis](../papers/d2sd.md) 中记录的 [SpecForge revision](https://github.com/sgl-project/SpecForge/tree/fec8f8586de51e6b6baf007861898e5c4e95df03) | SGLang SpecForge 的算法 recipe 与训练代码边界 | 不支持把 D2SD recipe 概括成所有 SpecForge 算法的统一模式 |
| `A1` | 综合推论 | 本 Topic 的跨来源分析 | response 与 hidden states 是两个独立生命周期；版本跨度是 RL 场景风险 | 不应写成任何单一 paper 或官方文档的实证结果 |

## Claim 证据矩阵

| Claim ID | 主张 | 证据等级 | 直接来源 | 证据边界 |
|---|---|---|---|---|
| `C1` | 标准 Speculators 训练数据必须包含 target 产生的 response；可用预分词行或已有 response 的自然语言对话。 | 官方文档事实 | `S1`, `S2` | 约束的是 `prepare-data` 输入，不是所有自建训练流水线。 |
| `C2` | `prepare-data` 的 render endpoint 负责 chat template、分词和 loss mask，不负责生成 response。 | 官方文档事实 + 固定源码 | `S2`, `S4` | 不能把 render 调用描述成 on-policy response generation。 |
| `C3` | Online hidden states 按需生成并丢弃，Offline 预先落盘，Hybrid 首轮生成后缓存。 | 官方文档事实 | `S1` | 文档没有给出三者在统一设置下的质量排名。 |
| `C4` | response 可以通过独立的 `regenerate-responses` 步骤由 target 生成，不要求人工书写。 | 官方文档事实 | `S3` | 生成结果仍需在进入 `prepare-data` 前成为可读数据行。 |
| `C5` | TorchSpec 把 target inference 与 draft optimization 组织成可流式传输的 producer-consumer 系统。 | Paper/技术报告事实 | `S5` | 本地 canonical 分析指出性能图不能隔离网络、调度与训练配方贡献。 |
| `C6` | RL rollout 集成可以把 response 生产放在当前 policy 的 rollout 内，但缓存/版本策略由系统自行定义。 | 论文事实 + 综合推论 | `S6`, `A1` | 不等于标准 Speculators CLI 支持 prompt-only 流式输入。 |
| `C6b` | SpecForge 的 response/hidden-state 生命周期必须按算法 recipe 和固定 revision 核验，不能用 SGLang serving 集成推断训练路径。 | Paper/代码分析 | `S7` | 当前证据只覆盖 D2SD trace，不覆盖所有 SpecForge 算法。 |
| `C7` | Online、Offline、Hybrid 的首要差别是资源、缓存和复现性；不能据现有资料声称某模式必然提高精度、accepted length 或总训练速度。 | 综合推论 | `S1`, `S5`, `A1` | 需要 matched target、数据、训练步数和硬件预算的专门实验。 |
| `C8` | RL 中复用旧 target 的 response/hidden states 可能使 drafter loss 与当前 policy acceptance 脱钩。 | 综合推论 | `S6`, `A1` | 这是版本漂移风险分析，不是已统一验证的定量结论。 |

## 直接回答用户问题

| 用户表述 | 可交付的严谨回答 | 证据等级 |
|---|---|---|
| “response 是否需要提前离线处理好？” | 对标准 `prepare-data`：response 行必须先存在；但可以由 `regenerate-responses` 自动生成，且可直接保存成 tokenized 行，不要求人工 QA。 | 官方文档事实 |
| “Online 是否也要提前抽 feature？” | 不需要全量预提取 hidden states；Online 在训练读样本时向 live target 请求。 | 官方文档事实 |
| “能否只给 prompt，让 prepare-data 自己生成？” | 标准命令不行；需要先运行 response regeneration 或写自定义数据生产集成。 | 官方文档事实 + 综合推论 |
| “哪种框架一定精度/接受长度/耗时更好？” | 现有来源没有统一匹配实证，不能下这个结论。 | 证据边界 |

## 复核缺口

1. 尚无公开 matched benchmark 同时控制 target checkpoint、response 集、hidden-state 层、训练步数、GPU-hours 和存储带宽，并比较 Speculators Online/Offline/Hybrid 与 TorchSpec。
2. 尚无统一实验把 RL policy drift、hidden-state cache 跨度和 accepted length 做成因果曲线。
3. Speculators 文档说明了 Ascend NPU 为支持加速器之一，但本清单没有据此推断各模式在具体 NPU 后端上的性能或稳定性。
