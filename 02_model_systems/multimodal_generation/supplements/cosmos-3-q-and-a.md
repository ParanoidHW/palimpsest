# Cosmos 3 补充问答

> [!info] 文档关系
> - 文档类型：Supplement
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion evolution](../surveys/diffusion-evolution.md)
> - 证据资产：`../assets/papers/cosmos-3/`
> - 相关文档：[Cosmos 3 Paper](../papers/cosmos-3.md)，[Figure inventory](../evidence/figure-inventory.md)

本文件保留原 Q1--Q12 中适合讨论和复读的解释，canonical 结论、公式、数字、代码 commit 与局限以 [主 Paper](../papers/cosmos-3.md) 为准。问答不引用本机源码路径或过程材料。

## Q1. 论文解决什么问题？

它试图把 Physical AI 中割裂的 VLM、world generator、audio/video simulator、forward/inverse dynamics 与 policy 统一到一个架构和训练接口。严格说是“统一 backbone/family”，不是单 checkpoint 同时达到所有榜单最优；多个 headline 结果来自 post-trained variants。详见 [问题与模型家族](../papers/cosmos-3.md#1-问题与模型家族)。

## Q2. 统一时空位置编码如何对齐？

每个 token 获得 $(p_t,p_h,p_w)$。语言三轴相同，video 同时有时间和二维空间坐标，audio/action 只占时间轴。不同 FPS 通过 $24/f$ 缩放 frame increment；不同 TPS 不必相等，只需映射到同一物理时间。默认 15,000 gap 是 position range separation，不是等待时间。详见 [mRoPE](../papers/cosmos-3.md#23-unified-3d-mrope-与物理时间)。

## Q3. 不同模态如何 encoding？

Text/vision understanding 进入 AR path；visual generation 使用 Wan video VAE latent；audio 使用 audio VAE；action 使用共享几何语义加 domain-aware projections。统一发生在 packed transformer token space，低层 codec 并不统一。详见 [Modality encoding](../papers/cosmos-3.md#21-modality-encoding)。

## Q4. MoT 为什么不是 MoE？

MoT 没有按 token 动态选择多个专家。AR 与 DM token 类型预先决定走 reasoner 或 generator tower，每层各自有 norm/QKV/MLP；信息通过 two-way attention 单向注入。它解决的是 noisy generation state 与 clean reasoning state 的参数/信息流隔离。详见 [MoT](../papers/cosmos-3.md#22-mot-与单向条件注入)。

## Q5. 有哪些模型规格？

Edge/Nano/Super 分别 28/36/64 层，hidden 2048/4096/5120，attention heads 16/32/64，均为 8 KV heads 和 128 head dim。Edge 为从头训练的 2B dense model，Nano/Super 从 Qwen3-VL 初始化；post-trained checkpoint 名称不应误认为新的 base architecture。

## Q6. 整体训练流程是什么？

先做 Reasoner pre-training/SFT，再从它初始化 Generator。Generator pre-training 学 image/video/audio rectified flow，mid-training 加 action/transfer，最后针对 T2I/I2V/policy 做 post-training。Generator pre-training 冻结 reasoner tower，但这不等于 Reasoner 在所有后续阶段永久冻结。详见 [训练阶段](../papers/cosmos-3.md#3-训练目标与阶段)。

## Q7. 数据集如何构建？

Reasoner 混合 OCR/VQA/caption/grounding/reasoning 与 Physical AI instruction；Generator media 经过 dedup、质量/运动/匹配过滤和 caption upsampling，并加入多类 synthetic data；action 进行 embodiment-aware packaging。训练 loader 按 token budget 消费，sample ratio 不等于 token ratio。详见 [Data construction](../papers/cosmos-3.md#4-data-construction)。

## Q8. 训练与 serving infra 的关键点？

训练侧是 joint loader、rank-synchronous stream、look-ahead packing、two-way varlen attention、HSDP + Ulysses、selective checkpointing、compile/AOT 与 async checkpoint。Serving 侧是 reasoner caching、CP/CFG parallelism、batching、FP8 与 diffusion cache。各项分别作用于 loader、attention、communication、storage 或 serving，不能合并归因为模型质量。

## Q9. 自研系统是否开源？

`NVIDIA/cosmos` 提供 cookbook/evaluation，`NVIDIA/cosmos-framework` 提供训练/推理与模型集成。主 Paper 固定了两个核验 commit。开源并不意味着训练数据、全部生产基础设施、所有 checkpoint 和排行榜服务均可复现；gated weights 与超大规模训练仍是边界。

## Q10. 论文有哪些 benchmark？

Reasoner 覆盖 general multimodal、robotics、smart infrastructure、driving；Generator 覆盖 T2I/T2V/I2V、Physical AI generation、audio-visual、transfer/control、physics、forward/inverse dynamics 与 policy。每组 metric 和 baseline 不同，不能平均成一个“总分”。详见 [Experiments](../papers/cosmos-3.md#6-experiments-与主结果边界)。

## Q11. 不同模态 TPS 不同，物理时间如何对齐？

假设 video 24 FPS 每帧 latent 有多个 spatial tokens，audio 每秒产生另一数量的 latent，action 以控制频率采样。先为每个 token 计算真实 timestamp，再乘统一 position scale并写入 $p_t$；同一视频帧内的 spatial tokens 可以共享时间坐标，不同 audio/action token 只要 timestamp 接近就落在相近 $p_t$。对齐的是时间坐标，不是把三个序列 resample 成相同 token 数。

## Q12. `frame_offset` 如何理解？

`frame_offset` 是某段模态在 packed sequence 内的起始物理时间/位置基准，后续 token 在此基础上累加 FPS/TPS 对应的增量。它避免多个 clip/view/segment 都从零开始而发生位置冲突。offset 属于 position metadata，不改变原始视频帧号，也不等同于 sequence array index；具体实现需与固定 commit 的 packing/config 一起核验。

## 复读提示

- 看到“统一”时，先问统一的是 architecture、token space、loss API 还是 checkpoint。
- 看到“对齐”时，先区分 physical timestamp、position id、array offset 与 attention visibility。
- 看到“加速”时，先区分 loader、kernel、parallelism、cache、dtype 与 sampling steps。
- 看到榜单第一时，记录日期、variant、prompt/steps、是否 BoN/reward reranking，以及 open/closed baseline 范围。
