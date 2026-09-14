# Speculator 训练数据生命周期证据清单

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[投机解码的基础合同与机制分类](../surveys/foundations-and-trends.md)
> - 支持 Topic：[Speculator 训练的数据生命周期与框架策略](../topics/speculator-training-data-lifecycle.md)
> - 相关 Paper：[TorchSpec](../papers/torchspec.md)

## 资料边界

- 核验日期：`2026-09-14`。
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
| `S8` | 固定源码 | [SpecForge commit `3d64e7a`](https://github.com/sgl-project/SpecForge/tree/3d64e7a61f5fcc7f7d78ba6164c881f831943947) | `DataConfig`、`prompt_builder`、response regeneration、server capture adapter、SGLang patch 与 Mooncake feature lifecycle | 只支持该 commit；不证明未来版本或未合并分支行为 |
| `S9` | 官方文档 | [SpecForge Data Preparation](https://github.com/sgl-project/SpecForge/blob/3d64e7a61f5fcc7f7d78ba6164c881f831943947/docs/sections/basic_usage/data_preparation.md) | response regeneration 的独立两步流程；原始 conversation 与 tokenized 输入格式；target regeneration 的推荐理由 | 不证明 regeneration 是计算 target hidden states 的数学必要条件，也不提供统一 acceptance 增益数字 |
| `S10` | 官方文档 + 固定源码说明 | [SpecForge SGLang patch inventory](https://github.com/sgl-project/SpecForge/blob/3d64e7a61f5fcc7f7d78ba6164c881f831943947/specforge/inference/sglang_patch_inventory.md) | prefill capture、设备到主机（D2H）复制重叠、有上限的锁页主机缓冲区、Mooncake 写入、fresh `extra_key` 与 full-prefill 要求 | 不证明与 SGLang 原生 Prefill/Decode（PD）拓扑已集成 |
| `S11` | 官方文档 | [SGLang PD Disaggregation](https://docs.sglang.ai/backend/pd_disaggregation.html) | P/D worker 分离及 Key-Value（KV）cache transfer 的用途与配置 | 不支持推断 SpecForge hidden-state capture 自动复用 PD KV 协议 |
| `S12` | 官方文档（与源码冲突） | [SpecForge AMD ROCm guide](https://github.com/sgl-project/SpecForge/blob/3d64e7a61f5fcc7f7d78ba6164c881f831943947/docs/sections/basic_usage/AMD/amd_rocm.md) | 原文声称 Online producer regenerates full-length responses | 同 commit 的 adapter 设置 `max_new_tokens=0`；不能据此认定 capture call 会生成 response |
| `A1` | 综合推论 | 本 Topic 的跨来源分析 | response 与 hidden states 是两个独立生命周期；版本跨度是 RL 场景风险 | 不应写成任何单一 paper 或官方文档的实证结果 |
| `A2` | 综合推论 | 本 Topic 的 SpecForge PD 机制分析 | prompt-only 一体化路径需要两遍 target 计算，或新增 decode-step feature capture、拼接与生命周期管理 | 设计推论；不是当前 SpecForge 已实现能力 |

## Claim 证据矩阵

| Claim ID | 主张 | 证据等级 | 直接来源 | 证据边界 |
|---|---|---|---|---|
| `C1` | 标准 Speculators 训练数据必须包含 target 产生的 response；可用预分词行或已有 response 的自然语言对话。 | 官方文档事实 | `S1`, `S2` | 约束的是 `prepare-data` 输入，不是所有自建训练流水线。 |
| `C2` | `prepare-data` 的 render endpoint 负责 chat template、分词和 loss mask，不负责生成 response。 | 官方文档事实 + 固定源码 | `S2`, `S4` | 不能把 render 调用描述成 on-policy response generation。 |
| `C3` | Online hidden states 按需生成并丢弃，Offline 预先落盘，Hybrid 首轮生成后缓存。 | 官方文档事实 | `S1` | 文档没有给出三者在统一设置下的质量排名。 |
| `C4` | response 可以通过独立的 `regenerate-responses` 步骤由 target 生成，不要求人工书写。 | 官方文档事实 | `S3` | 生成结果仍需在进入 `prepare-data` 前成为可读数据行。 |
| `C5` | TorchSpec 把 target inference 与 draft optimization 组织成可流式传输的 producer-consumer 系统。 | Paper/技术报告事实 | `S5` | 本地 canonical 分析指出性能图不能隔离网络、调度与训练配方贡献。 |
| `C6` | RL rollout 集成可以把 response 生产放在当前 policy 的 rollout 内，但缓存/版本策略由系统自行定义。 | 论文事实 + 综合推论 | `S6`, `A1` | 不等于标准 Speculators CLI 支持 prompt-only 流式输入。 |
| `C6b` | 当前 SpecForge Online 读取已有 assistant turns 或已有 `input_ids/loss_mask`；capture 请求不生成 response。 | 官方文档事实 + 固定源码 | `S8`, `S9` | 若从 prompt-only 开始，需先运行独立 regeneration 或自建上游 generator。 |
| `C7` | Online、Offline、Hybrid 的首要差别是资源、缓存和复现性；不能据现有资料声称某模式必然提高精度、accepted length 或总训练速度。 | 综合推论 | `S1`, `S5`, `A1` | 需要 matched target、数据、训练步数和硬件预算的专门实验。 |
| `C8` | RL 中复用旧 target 的 response/hidden states 可能使 drafter loss 与当前 policy acceptance 脱钩。 | 综合推论 | `S6`, `A1` | 这是版本漂移风险分析，不是已统一验证的定量结论。 |
| `C9` | SpecForge response regeneration 是独立脚本：先调用 SGLang decode assistant turn，再把结果写入新的 JSONL。 | 官方文档事实 + 固定源码 | `S8`, `S9` | 这是官方路径；外部数据生产系统可替代该脚本。 |
| `C10` | SpecForge Online capture 提交完整 `input_ids`，设置 `max_new_tokens=0`，用 fresh `extra_key` 强制一次完整、非 chunked prefill。 | 固定源码 | `S8`, `S10` | 只覆盖固定 commit 和配套 patch；不是 response generation。 |
| `C11` | 已有完整 response 后，当前 capture 阶段不再 decode；一次 full prefill 产生所需序列 hidden states。 | 固定源码 + 机制事实 | `S8`, `S10` | 不计 response regeneration 已经发生过的 decode 成本。 |
| `C12` | KV cache 与 hidden-state features 是两条独立状态生命周期：前者服务 prefill/decode，后者经 host buffer/Mooncake 供 trainer 消费并显式释放。 | 官方文档事实 + 固定源码 | `S8`, `S10`, `S11` | 不能简写成 vanilla SGLang 内部两套同构 cache manager。 |
| `C13` | 当前证据没有显示 SpecForge 已实现 prompt-only、PD generation、decode-step hidden capture 和 trainer stream 的一遍式融合。 | 证据边界 + 综合推论 | `S8`, `S10`, `S11`, `A2` | “未在固定源码发现”不等于任何外部分支都不存在。 |
| `C14` | SpecForge 同一 commit 内存在文档冲突；运行语义应以 `server_capture.py` 的可执行请求为准。 | 证据冲突 + 综合判断 | `S8`, `S12` | AMD 指南可能陈旧或宽泛指代上游 regeneration；当前证据不能确定其作者原意。 |

## 直接回答用户问题

| 用户表述 | 可交付的严谨回答 | 证据等级 |
|---|---|---|
| “response 是否需要提前离线处理好？” | 对标准 `prepare-data`：response 行必须先存在；但可以由 `regenerate-responses` 自动生成，且可直接保存成 tokenized 行，不要求人工 QA。 | 官方文档事实 |
| “Online 是否也要提前抽 feature？” | 不需要全量预提取 hidden states；Online 在训练读样本时向 live target 请求。 | 官方文档事实 |
| “能否只给 prompt，让 prepare-data 自己生成？” | 标准命令不行；需要先运行 response regeneration 或写自定义数据生产集成。 | 官方文档事实 + 综合推论 |
| “SpecForge Online 会在 capture 时生成 response 吗？” | 不会；当前 adapter 发送已有完整序列并设置 `max_new_tokens=0`。 | 固定源码事实 |
| “已有 response 后是否还要 decode？” | 不要；当前路径用一次 full prefill 提取全序列 hidden states。 | 固定源码事实 |
| “SGLang 是否用同一 cache manager 管 KV 与训练 hidden states？” | 不是。KV 属于 SGLang serving cache；hidden states 属于 capture host buffer 与 SpecForge/Mooncake feature store。 | 官方文档 + 固定源码事实 |
| “当前是否已兼容一遍式 PD 生成与特征提取？” | 没有足够代码证据；现有 producer/consumer training disaggregation 不是 PD disaggregation。 | 证据边界 + 综合推论 |
| “哪种框架一定精度/接受长度/耗时更好？” | 现有来源没有统一匹配实证，不能下这个结论。 | 证据边界 |

## 复核缺口

1. 尚无公开 matched benchmark 同时控制 target checkpoint、response 集、hidden-state 层、训练步数、GPU-hours 和存储带宽，并比较 Speculators Online/Offline/Hybrid 与 TorchSpec。
2. 尚无统一实验把 RL policy drift、hidden-state cache 跨度和 accepted length 做成因果曲线。
3. Speculators 文档说明了 Ascend NPU 为支持加速器之一，但本清单没有据此推断各模式在具体 NPU 后端上的性能或稳定性。
4. 尚无当前 SpecForge 主线的公开 matched benchmark，量化“两遍 decode+prefill”与“一遍 decode-step capture”在吞吐、峰值内存、网络带宽和可恢复性上的差异。
5. SGLang PD 官方文档说明 KV transfer，但未在本次固定 SpecForge 源码中找到 PD worker 间 hidden-state capture、token-position 拼接或复用 KV transfer metadata 的实现合同。
