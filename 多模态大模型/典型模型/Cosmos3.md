# Cosmos 3 论文阅读与问答记录

创建日期：2026-06-08

## 材料索引

本地材料：

- 论文 PDF：`paper/2606.02800.pdf`
- arXiv LaTeX 源码包：`source/2606.02800.tar`
- 解包后的 LaTeX 源码：`source/src/`
- NVIDIA/cosmos 官方 cookbook 快照：`code/src/cosmos-main/`
- NVIDIA/cosmos-framework 官方框架快照：`code/src/cosmos-framework-main/`
- 后续问答记录：本文件

外部来源：

- arXiv abstract：https://arxiv.org/abs/2606.02800
- arXiv PDF：https://arxiv.org/pdf/2606.02800
- arXiv source：https://arxiv.org/e-print/2606.02800
- NVIDIA/cosmos：https://github.com/NVIDIA/cosmos
- NVIDIA/cosmos-framework：https://github.com/NVIDIA/cosmos-framework
- Hugging Face Cosmos3 collection：https://huggingface.co/collections/nvidia/cosmos3
- 项目页：https://research.nvidia.com/labs/cosmos-lab/cosmos3

代码快照：

- `NVIDIA/cosmos` zip 快照 commit：`4e4f3001fae9238384f9551f1723fcb0f651c42c`
- `NVIDIA/cosmos-framework` zip 快照 commit：`3a5314b7dd3c3abb84df71627ecb10ef8423dbdd`

注意：已准备官方代码和模型仓库链接，但没有下载模型 checkpoint。Cosmos3 权重体积大且部分 gated，需要 Hugging Face 授权后按需下载。

## 论文主线摘要

Cosmos 3 是 NVIDIA 提出的 omnimodal world model family，用一个统一 Mixture-of-Transformers 架构处理并生成 language、image、video、audio、action。论文把模型分成两个运行面：

- Reasoner：输入 text/vision，输出 text，用于世界理解、grounding、物理推理、任务规划、动作预测等。
- Generator：输入 text/vision/sound/action，输出 vision/sound/action，用于世界生成、仿真、未来预测、合成数据、策略学习等。

架构核心：

- 多模态 encoder 把语言、视觉、音频、动作映射到统一 token 空间；视觉理解使用 ViT，视觉生成使用 Wan2.2-TI2V-5B video VAE；音频生成使用 audio VAE；动作使用 domain-aware projection。
- token 排布固定为 AR subsequence 在前、diffusion subsequence 在后。AR 负责 reasoner/understanding，DM 负责 generation/denoising。
- MoT 每层有两套路径参数：reasoner tower 处理 AR token，generator tower 处理 diffusion token。
- Attention 是 dual-stream：AR token 只做 causal self-attention；DM token 对同一样本内 AR+DM token 做 full attention，保证生成 token 能看 prompt/条件和其他生成 token，但 AR 不被 DM 反向污染。
- 位置编码采用 unified 3D mRoPE，并对 video/audio/action 使用物理时间轴对齐；论文设置 AR 和 diffusion temporal gap 为 `15000`。

训练主线：

- Reasoner 先训练：约 `24.2M` samples，其中 `22.0M` pre-training，`2.2M` Physical AI SFT。
- Generator 从训练好的 Reasoner 权重初始化。Generator pre-training 使用 rectified flow matching，训练 image/video/audio，随后 mid-training 加入 action 和 transfer 数据。
- Generator pre-training 中 reasoner tower 冻结，只更新 generation-specific 参数，以保留语言/视觉理解能力。
- Post-training 产生专用模型：`Cosmos3-Super-Text2Image`、`Cosmos3-Super-Image2Video`、`Cosmos3-Nano-Policy-DROID`。

基础设施主线：

- data loader 用 token-budgeted packed sequence、joint data loader、rank-synchronous stream selection、look-ahead packing 解决多模态样本长度差异。
- custom two-way flat attention 把 reasoner causal attention 和 generator full attention 拆成两个 variable-length kernel 调用。
- 分布式训练结合 HSDP 和 Ulysses context parallelism。
- 推理侧支持 PyTorch reference、vLLM/TensorRT-LLM Reasoner、vLLM-Omni Generator，并使用 reasoner tower caching、CFG parallelism、context parallelism、batching、Cache-DiT、FP8 等优化。

结果主线：

- Reasoner 在 48 个 benchmark 上评估，分 general、robotics、smart infrastructure、driving 四类。
- Generator 覆盖 image/video/audio-visual/transfer/action/policy 等任务。
- 论文称写作时 post-trained Cosmos 3 在 Artificial Analysis 的 open-source T2I/I2V 排名领先，并在 RoboArena policy 评测中领先。

## LaTeX 源码入口

- 主入口：`source/src/main.tex`
- 摘要：`source/src/sections/0__abstract.tex`
- 引言：`source/src/sections/1__introduction.tex`
- 模型架构：`source/src/sections/2__model.tex`
- 数据：`source/src/sections/3__data.tex`
- 训练：`source/src/sections/4__training.tex`
- 基础设施：`source/src/sections/5__infrastructure.tex`
- 结果：`source/src/sections/6__results.tex`
- Reasoner 结果：`source/src/sections/results/reasoner.tex`
- Generator 结果：`source/src/sections/results/generator.tex`
- 参考文献：`source/src/main.bib`

关键图表素材：

- Cosmos 3 overview：`source/src/figures/introduction/tikz_cosmos3_overview.pdf`
- Cosmos platform：`source/src/figures/introduction/tikz_cosmos_platform.pdf`
- MoT architecture：`source/src/figures/model_architecture/tikz_mot_architecture.pdf`
- mRoPE coordinate assignment：`source/src/figures/model_architecture/tikz_mrope_coordinate_assignment.pdf`
- action representation：`source/src/figures/model_architecture/action/tikz_action_representation.pdf`
- action modes：`source/src/figures/model_architecture/action/tikz_action_modes.pdf`
- training data mix：`source/src/figures/training/tikz_generator_datamix.pdf`
- infrastructure overview：`source/src/figures/infrastructure/tikz_infra_overview.pdf`
- official cookbook architecture PNG：`code/src/cosmos-main/cookbooks/cosmos3/cosmos3-model-architecture.png`

关键表格：

- model variants：`source/src/tables/model_architecture/model_variants.tex`
- generation resolution specs：`source/src/tables/training/generation_resolution_specs.tex`
- mid-training modality mix：`source/src/tables/training/midtraining_modality_mix.tex`
- reasoner benchmark group：`source/src/tables/results/reasoner_benchmark_group.tex`
- T2I results：`source/src/tables/results/score_t2i.tex`
- action post-training summary：`source/src/tables/results/action_posttraining_summary_wide.tex`
- training throughput：`source/src/tables/training/training_throughput.tex`
- serving batching：`source/src/tables/serving/batching.tex`

## 模型代码索引

`NVIDIA/cosmos` 仓库更偏 cookbook 和示例入口：

- repo README：`code/src/cosmos-main/README.md`
- Cosmos3 cookbook setup：`code/src/cosmos-main/cookbooks/cosmos3/README.md`
- Reasoner cookbook：`code/src/cosmos-main/cookbooks/cosmos3/reasoner/README.md`
- Generator action cookbook：`code/src/cosmos-main/cookbooks/cosmos3/generator/action/README.md`
- Generator audiovisual cookbook：`code/src/cosmos-main/cookbooks/cosmos3/generator/audiovisual/README.md`

`NVIDIA/cosmos-framework` 是训练/推理框架和模型集成主入口：

- 框架 README：`code/src/cosmos-framework-main/README.md`
- 代码结构文档：`code/src/cosmos-framework-main/docs/code_structure.md`
- 推理文档：`code/src/cosmos-framework-main/docs/inference.md`
- 训练文档：`code/src/cosmos-framework-main/docs/training.md`
- SFT 配置文档：`code/src/cosmos-framework-main/docs/sft_config.md`
- inference 入口：`code/src/cosmos-framework-main/cosmos_framework/inference/`
- batch inference script：`code/src/cosmos-framework-main/examples/inference.py`
- SFT examples：`code/src/cosmos-framework-main/examples/toml/sft_config/`

核心实现文件：

- Diffusers Generator pipeline：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py`
- Diffusers sequence packing：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py`
- Diffusers transformer/MoT：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py`
- Transformers Reasoner wrapper：`code/src/cosmos-framework-main/packages/transformers-cosmos3/transformers_cosmos3/model.py`
- vLLM Reasoner wrapper：`code/src/cosmos-framework-main/packages/vllm-cosmos3/vllm_cosmos3/model.py`
- action data utilities：`code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/`

源码对应关系：

- two-way attention：`transformer.py:74` 的 `CosmosAttnProcessor3_0` 实现 causal understanding 和 full generation 两路 attention。
- MoT attention projection：`transformer.py:333` 的 `PackedAttentionMoT` 为 generation path 增加独立 `add_q/k/v_proj` 和 `to_add_out`。
- MoT decoder layer：`transformer.py:481` 的 `Cosmos3VLTextMoTDecoderLayer` 对 und/gen token 分别走 layernorm、attention、MLP。
- mRoPE：`transformer.py:205` 的 `Cosmos3VLTextRotaryEmbedding` 处理 3D position ids。
- temporal gap / model config：`transformer.py:580` 的 `Cosmos3OmniTransformer` 默认 `unified_3d_mrope_temporal_modality_margin=15000`。
- action domain-aware projection：`transformer.py:158` 的 `DomainAwareLinear` 对每个 embodiment domain 使用独立 weight/bias。
- sequence split metadata：`sequence_packing.py:77` 初始化 causal/full indices 和 offsets。
- pack sequence：`sequence_packing.py:1295` 统一打包 text/vision/action/sound，并设置 full attention segment。
- Transformers/vLLM Reasoner 只加载 understanding tower：`transformers_cosmos3/model.py:8` 的 `DROP_PATTERNS` 丢弃 generation/audio/action 权重；`vllm_cosmos3/model.py:30` 过滤非 understanding 权重。

稳定 GitHub 代码链接：

- two-way attention：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py#L74-L118
- DomainAwareLinear：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py#L158-L189
- mRoPE：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py#L205-L263
- MoT layer：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py#L333-L578
- OmniTransformer config：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py#L580-L710
- sequence packing：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py#L1295-L1570
- Transformers Reasoner wrapper：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/transformers-cosmos3/transformers_cosmos3/model.py#L1-L70
- vLLM Reasoner wrapper：https://github.com/NVIDIA/cosmos-framework/blob/3a5314b7dd3c3abb84df71627ecb10ef8423dbdd/packages/vllm-cosmos3/vllm_cosmos3/model.py#L1-L56

## 后续问答记录

后续所有问题都追加到这里。建议格式：

```md
### Q1. 问题标题

**问题：** ...

**回答：** ...

**原文依据：**
- `source/src/...`

**源码依据：**
- `code/src/...`

**图片/表格：**
- `source/src/figures/...`
```

### Q1. 这篇 paper 解决了一个什么问题？

**问题：** 这篇 paper 解决了一个什么问题？需要给出背景和分析过程。

**一句话结论：** Cosmos 3 要解决的是 Physical AI 中“理解、生成/仿真、动作预测被多个割裂模型分别承担”的系统性问题，目标是把 VLM、视频/图像/音频生成模型、world simulator、forward/inverse dynamics、VLA/WAM/action policy 统一到一个可扩展的 omnimodal world model 中。

![Cosmos 3 overview](cosmos3_overview.png)

#### 背景：Physical AI 的核心瓶颈

论文从 Physical AI agents 的训练需求出发：机器人、自动驾驶、智能基础设施等智能体需要感知真实世界、理解语义和动态、预测未来，并输出可执行动作。但直接在真实世界训练有三个硬约束：慢、昂贵、危险。因此必须依赖可控的模拟世界、合成数据、未来状态预测和可验证的 action rollout 来扩展训练。

这里出现了两个耦合能力：

- **Understanding：** 从局部观测中理解语义、空间关系、物理状态、时序动态、任务意图。
- **Generation / Simulation：** 生成或预测可能的未来世界，包括图像、视频、音频、动作及其结果。

论文的关键判断是：这两个能力不能长期分开做。理解需要对未来和动作后果有建模能力；生成也需要紧凑、结构化的世界语义和 agent 行为表示。如果理解模型不懂动作后果，规划会弱；如果生成模型没有强语义理解，仿真会不稳定、不可信。

#### 现有范式的问题：模型栈割裂

论文用“家庭机器人清理餐桌”这类任务说明现有 pipeline 的问题。传统方案通常要拼接多个模型：

- VLM：识别餐具、理解场景、生成计划。
- VLA / WAM：生成动作序列。
- Forward Dynamics / World Model：模拟动作执行后的未来状态。
- Video/Image/Audio Generator：生成视觉或多模态数据。

这种拼装式架构有几个问题：

- **表示不共享：** 每个模型有自己的 token、latent、任务接口，语义和物理动态不能自然迁移。
- **计算浪费：** 感知、规划、仿真、动作预测重复编码同一场景。
- **错误累积：** 上游 VLM 的理解错误会传给 action model，action model 的输出又可能和 world model 的状态空间不一致。
- **训练不可扩展：** 每个能力都要独立收集数据、独立训练、独立部署，很难形成统一的 Physical AI backbone。
- **跨模态控制弱：** 现实任务需要 text、image、video、audio、action 联合建模，而不是只做单一模态生成或识别。

因此，论文实际要回答的问题是：

> 能不能设计一个统一模型，在不改架构的情况下，根据不同输入输出配置，同时承担理解、生成、世界仿真和动作建模？

#### 分析过程：从需求到模型设计

**第一步：抽象 Physical AI 任务的共同结构。**  
无论是 VQA、视频理解、T2I、I2V、V2V、音视频生成、forward dynamics、inverse dynamics 还是 policy，本质上都是“给定一组条件 token，预测另一组目标 token”。区别只在于 token 的模态、是否自回归、是否扩散去噪、哪些 token 是 clean conditioning、哪些是 noisy target。

**第二步：把 action 也提升为核心模态。**  
论文没有把 action 当作后处理控制信号，而是定义为导致世界状态变化的 causal variable。连续视频 token 间的 action token 表示从上一状态到当前状态的转移。这样，action 可以和 video/audio/text 一起进入统一序列，支持 forward dynamics、inverse dynamics 和 policy 三种方向。

**第三步：用 AR subsequence + diffusion subsequence 统一任务形式。**  
Cosmos 3 把输入序列拆成两段：

- **AR subsequence：** 语言 token 和用于理解的 ViT visual token，负责 reasoner/VLM 式自回归理解。
- **Diffusion subsequence：** VAE visual token、audio token、action token，负责 generator/world simulation/action denoising。

这样，语言输出仍然按 next-token prediction 做；图像、视频、音频、动作则通过 iterative denoising 生成。

**第四步：用 MoT 解决“理解”和“生成”的参数冲突。**  
如果所有 token 走同一套 transformer 参数，理解能力和扩散生成能力可能互相干扰。Cosmos 3 使用 Mixture-of-Transformers：每层有 reasoner tower 和 generator tower 两套参数。AR token 走 reasoner tower，DM token 走 generator tower；attention 交互是非对称的，DM token 可以读取 AR 条件，AR token 不会 attend 或被 DM token 更新。

**第五步：用 dual-stream attention 保持条件信息流正确。**  
论文设计的 attention 方向很关键：

- AR token 只看 AR 内部过去 token，保持 VLM/LLM 的 causal 生成属性。
- DM token 对同一样本内 AR+DM 做 full bidirectional attention，从而能利用 prompt、条件帧、动作、音频等所有上下文。
- AR token 不被 DM token 更新，避免 noisy target 反向污染 conditioning pathway。

这就是论文所谓理解和生成统一但不互相破坏的核心机制。

**第六步：用统一时空位置编码对齐多模态时间。**  
视频、音频、动作采样率不同，单纯按 token index 编位置会让物理时间错位。Cosmos 3 用 3D mRoPE 和 FPS modulation，把 video/audio/action token 对齐到共同的物理时间轴。论文还在 AR 和 diffusion token 之间插入 temporal gap `15000`，减少文本到视觉 token 过近导致的 artifact。

#### 论文的解决方案映射

![Cosmos 3 model architecture](code/src/cosmos-main/cookbooks/cosmos3/cosmos3-model-architecture.png)

| 痛点 | Cosmos 3 的对应设计 |
| --- | --- |
| VLM、视频生成、world model、action model 割裂 | 一个 omnimodal MoT backbone 支持 language/image/video/audio/action |
| 理解和生成目标不同，容易互相干扰 | AR subsequence + diffusion subsequence，分别路由到 reasoner/generator tower |
| 生成 token 需要看语义条件，但语义 token 不能被 noisy token 污染 | dual-stream attention：AR causal，DM full-attend AR+DM |
| action 与视觉世界模型接口不统一 | action token + domain-aware projection，把不同 embodiment 映射到共享 latent action space |
| 多模态时间尺度不同 | 3D mRoPE + FPS modulation，对齐 video/audio/action 的物理时间轴 |
| 真实世界训练成本高、风险高 | 用 Cosmos 3 作为合成数据生成器、任务专用模型初始化点、未来训练环境生成基础 |
| 下游任务差异大 | 通过 post-training 派生 T2I、I2V、DROID policy 等专家模型，无需改主架构 |

#### 更准确地说，它不是只在解决“生成质量”问题

Cosmos 3 当然报告了 T2I、I2V、video/audio/action policy 等结果，但论文的核心问题不是单纯提升某个 leaderboard，而是构建一个 Physical AI backbone。它试图让同一个模型既能“看懂世界”，又能“模拟世界”，还能“预测/生成动作及其后果”。因此它比普通视频生成模型多了 action 建模和 reasoner；比普通 VLM 多了 diffusion generator 和 world simulation；比普通 VLA 多了视觉/音频/动作联合生成能力。

#### 原文依据

- `source/src/sections/1__introduction.tex:4`：指出 Physical AI 直接真实世界训练慢、贵且危险，需要安全可扩展的 simulated worlds；并把核心能力分成 understanding 和 generation。
- `source/src/sections/1__introduction.tex:6`：明确批评现有范式把 VLM、video generator、forward dynamics、VLA/WAM 分开，导致 fragmented architecture。
- `source/src/sections/1__introduction.tex:8`：提出 Cosmos 3 作为 joint language/image/video/audio/action 的 omnimodal world model。
- `source/src/sections/1__introduction.tex:15`：说明 Cosmos 3 面向 synthetic data generation、task-specific specialization、training environment 三类 Physical AI 扩展路径。
- `source/src/sections/2__model.tex:4`：说明 Cosmos 3 处理多模态输入输出，并把 action 作为核心模态。
- `source/src/sections/2__model.tex:54`：定义 AR subsequence 和 diffusion subsequence。
- `source/src/sections/2__model.tex:99`：定义 action 的 forward dynamics、inverse dynamics、policy 三种模式。
- `source/src/sections/2__model.tex:111`：定义 MoT，每层包含 reasoner/generator 两套参数。
- `source/src/sections/2__model.tex:123` 与 `source/src/sections/2__model.tex:131`：定义 AR causal attention 和 DM full attention。
- `source/src/sections/4__training.tex:4`：说明 Reasoner 先训练，Generator 用 Reasoner 权重初始化，把语义和世界知识迁移到生成模型。

#### 源码依据

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:74`：`CosmosAttnProcessor3_0` 实现 causal understanding attention 和 full generation attention。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:333`：`PackedAttentionMoT` 为 generation pathway 增加独立 Q/K/V 和输出投影。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:481`：`Cosmos3VLTextMoTDecoderLayer` 对 understanding/generation token 分别走 layernorm、attention、MLP。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:580`：`Cosmos3OmniTransformer` 默认支持 `joint_attn_implementation="two_way"`、`position_embedding_type="unified_3d_mrope"`、`unified_3d_mrope_temporal_modality_margin=15000`、`action_gen`、`sound_gen`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:158`：`DomainAwareLinear` 对不同 action embodiment domain 使用独立投影。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1295`：`pack_input_sequence` 统一打包 text、vision、action、sound，并维护 mRoPE、FPS modulation、full attention segment。

#### 图片素材

- `assets/cosmos3_overview.png`
- `assets/cosmos_platform.png`
- `code/src/cosmos-main/cookbooks/cosmos3/cosmos3-model-architecture.png`
- 原始论文图：`source/src/figures/introduction/tikz_cosmos3_overview.pdf`
- 原始论文图：`source/src/figures/introduction/tikz_cosmos_platform.pdf`

### Q2. 统一时空位置编码是什么，怎么做对齐？

**问题：** 解释一下统一时空位置编码，怎么做的对齐。

**一句话结论：** Cosmos 3 的统一时空位置编码是一个扩展版 3D mRoPE。它给每个 token 分配三维坐标 $(t,h,w)$，再把 video、audio、action 的 $t$ 坐标换算到同一个物理时间轴上。核心不是“第几个 token”，而是“这个 token 对应真实世界里的哪个时间点和空间位置”。

![mRoPE coordinate assignment](mrope_coordinate_assignment.png)

#### 为什么需要统一时空位置编码

Cosmos 3 在同一个 attention 序列里同时放 language、image、video、audio、action。普通 RoPE 或原始 3D MRoPE 有两个不足：

- 对语言来说，1D token index 足够。
- 对图像/视频理解来说，$t/h/w$ 的离散位置基本够用。
- 但对 Cosmos 3 的生成路径来说，video、audio、action 会同时生成或互相条件化，它们采样率不同。如果只按 token index 递增，24fps 视频、60fps 视频、25Hz audio token、15Hz action token 会被错误地看成相同时间间隔。

所以论文引入 absolute temporal modulation：把不同模态的时间坐标换算到共享物理时间轴上，让同一真实时间附近的 video/audio/action token 在 RoPE 空间中也接近。

#### 坐标怎么分配

Cosmos 3 的 position id 是三行，形状类似 $\left[3,\mathrm{seq\_len}\right]$，三行分别对应 $t$、$h$、$w$。

| token 类型 | $t$ 坐标 | $h/w$ 坐标 | 目的 |
| --- | --- | --- | --- |
| language token | $t=h=w$，单调递增 | 同 $t$ | 退化成标准 1D RoPE，兼容 LLM/VLM |
| AR visual token, ViT encoded | 同一帧共享 $t$ | patch 网格位置 | 兼容 Qwen3-VL 式图像/视频理解 |
| diffusion video token, VAE encoded | latent frame 的物理时间坐标 | VAE latent patch 网格 | 用于图像/视频生成和仿真 |
| diffusion image token | 单帧 video，$t$ 固定 | 图像 patch 网格 | 统一 image 和 video |
| audio token | audio hop 的物理时间坐标 | $h=w=0$ | 与视频/action 在时间上对齐 |
| action token | action sampling step 的物理时间坐标 | $h=w=0$ | 与状态转移对应 |

论文还规定 diffusion token 的空间坐标在每个 vision segment 内 reset。也就是说，一个视频片段内部用自己的 $(t,h,w)$ 坐标，不把它当作全局长序列里的普通 token offset。这样做更像“物理坐标系”，不是“序列拼接坐标系”。

#### 时间对齐的公式

论文先定义 temporal steps per second，简称 $\mathrm{TPS}$：

$$
\mathrm{TPS}_{\mathrm{video}}
= \frac{\mathrm{fps}_{\mathrm{video}}}{c_{\mathrm{video}}},
\qquad
\mathrm{TPS}_{\mathrm{audio}}
= \frac{48000}{1920}
= 25,
\qquad
\mathrm{TPS}_{\mathrm{action}}
= f_{\mathrm{action}}.
$$

Cosmos 3 选择 $24$fps 视频作为 base。由于 video VAE temporal compression factor 是 $4$，所以：

$$
\mathrm{TPS}_{\mathrm{base}}
= \frac{24}{4}
= 6.
$$

每前进一步时，真实使用的 temporal increment 是：

$$
\Delta t
= \frac{\mathrm{TPS}_{\mathrm{base}}}{\mathrm{TPS}}.
$$

这就是对齐的核心。不同模态可以有不同 token 频率，但都换算到同一个 base temporal unit。

| 模态示例 | 原始频率 | 压缩因子 | $\mathrm{TPS}$ | $\Delta t = \frac{6}{\mathrm{TPS}}$ | 含义 |
| --- | ---: | ---: | ---: | ---: | --- |
| 24fps video | $24$ | $4$ | $6$ | $1.0$ | base case，一个 latent step 对应 1 个 base 时间单位 |
| 60fps video | $60$ | $4$ | $15$ | $0.4$ | 60fps 更密，同样一个 latent step 代表更短真实时间 |
| 16fps video | $16$ | $4$ | $4$ | $1.5$ | 16fps 更稀，一个 latent step 跨更长真实时间 |
| audio | $48000$Hz, hop $1920$ | $1$ | $25$ | $0.24$ | audio token 更密，时间坐标步长更小 |
| 15Hz action | $15$ | $1$ | $15$ | $0.4$ | action step 与 60fps video latent step 在物理时间尺度上相近 |

所以如果两个 token 分别来自 video 和 action，只要它们对应相近真实时间，经过这个缩放后，它们的 $t$ 坐标也会接近。attention 中的 RoPE 相位关系就能表达“这些 token 在同一时刻附近”。

#### AR 和 diffusion 之间为什么要加 `15000` gap

论文说，如果 diffusion token 直接接在最后一个 AR token 后面，初始视频帧容易出现过饱和和 checkerboard artifacts。作者推测原因是最后的 language token 和第一帧 vision token 的 temporal embedding 太接近，模型难以区分“文本条件”和“视觉生成起点”。

解决办法是在 AR subsequence 和 diffusion subsequence 之间插入固定 temporal gap：

$$
\texttt{unified\_3d\_mrope\_temporal\_modality\_margin}
= 15000.
$$

这不是额外 token，而是把 diffusion token 的 $t$ 坐标整体平移一大段，给文本到视觉/音频/action 的转换留出位置空间缓冲。

#### 源码里怎么实现

第一，pipeline 把 transformer config 传给 sequence packing：

- `position_embedding_type`
- `unified_3d_mrope_reset_spatial_ids`
- `unified_3d_mrope_temporal_modality_margin`
- `enable_fps_modulation`
- `base_fps`
- `temporal_compression_factor`

位置：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:627`

第二，`pack_input_sequence` 先判断是否使用 unified mRoPE，然后在打包 text 后加 temporal gap：

```python
packed_seq._use_mrope = position_embedding_type == "unified_3d_mrope"
packed_seq._mrope_temporal_offset += unified_3d_mrope_temporal_modality_margin
```

位置：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1350`、`sequence_packing.py:1386`

第三，核心函数 `get_3d_mrope_ids_vae_tokens` 负责生成 $(t,h,w)$。当 `fps` 存在时，它启用 FPS modulation：

```python
tps = fps / temporal_compression_factor
base_tps = base_fps / effective_base_tcf
scaled_t = (frame_indices + start_frame_offset) / tps * base_tps + temporal_offset
```

位置：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:535`

第四，vision/action/sound 都复用同一个 3D mRoPE 生成函数，只是 `grid_h/grid_w` 不同：

- vision：`grid_t=latent_t, grid_h=patch_h, grid_w=patch_w`
- action：`grid_t=action_split_len, grid_h=1, grid_w=1`
- sound：`grid_t=sound_split_len, grid_h=1, grid_w=1`

位置：`sequence_packing.py:949`、`sequence_packing.py:1027`、`sequence_packing.py:1104`

第五，transformer 里真正使用这些三维 position ids。`Cosmos3VLTextRotaryEmbedding` 会把 position ids 扩展成 $\left[3,B,N\right]$，分别计算 $T/H/W$ 的 rotary frequency，然后用 `mrope_section=[24,20,20]` 做 interleaved mRoPE：

位置：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:205`

#### 一个具体例子

假设 prompt 后面生成一个 24fps 视频和 15Hz action，video VAE temporal compression factor 是 4：

- 文本 token 先按 1D RoPE 编号。
- 文本结束后，diffusion 的 temporal offset 加 `15000`。
- 24fps video latent token 的 $\mathrm{TPS}$ 是 $\frac{24}{4}=6$，所以每个 latent frame 的 $t$ 增量是 $1.0$。
- 15Hz action token 的 $\mathrm{TPS}$ 是 $15$，所以每个 action step 的 $t$ 增量是 $0.4$。
- 如果某个 action step 对应视频状态转移附近，它的 $t$ 会落在视频 latent frame 之间或附近，而不是被简单放在 action 序列的第几个 token 上。

这样，模型在 attention 中看到的是物理时间对齐后的相对位置，而不是“视频 token 第 3 个、action token 第 3 个”这种无物理意义的位置。

#### 为什么这对 Cosmos 3 重要

统一时空位置编码支撑了 Cosmos 3 的 omnimodal 目标：

- T2V/I2V/V2V 需要视频内部时空一致性。
- video + audio 需要画面与声音同步。
- video + action 需要动作和状态转移对齐。
- transfer/control video 需要控制信号和 RGB 目标帧对齐。
- policy 模式需要 action token 和未来 visual consequence 对齐。

如果没有这个对齐，模型虽然可以把多模态 token 拼在一起，但 attention 看到的时间关系是错的。Cosmos 3 的做法是让所有非文本生成模态共享同一个物理时间坐标系，再用 MoT 和 dual-stream attention 在这个坐标系上建模。

#### 原文依据

- `source/src/sections/2__model.tex:144`：说明 Cosmos 3 设计 3D MRoPE with absolute temporal indexing，用于对齐 video、audio、action。
- `source/src/sections/2__model.tex:148`：说明 language token 退化为 1D RoPE，AR visual token 使用 Qwen3-VL 式 3D MRoPE。
- `source/src/sections/2__model.tex:152`：说明 diffusion video/image/audio/action 的坐标分配方式。
- `source/src/sections/2__model.tex:154`：说明 AR-DM 之间插入 fixed temporal gap，值为 `15000`。
- `source/src/sections/2__model.tex:157`：说明不同 FPS/采样率会导致 token temporal step 对应不同物理时间。
- `source/src/sections/2__model.tex:159`：定义 video/audio/action 的 TPS。
- `source/src/sections/2__model.tex:161`：给出 $\Delta t = \mathrm{TPS}_{\mathrm{base}} / \mathrm{TPS}$。
- `source/src/sections/2__model.tex:166`：说明 $\mathrm{TPS}_{\mathrm{base}} = 24 / 4 = 6$。

#### 源码依据

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:535`：`get_3d_mrope_ids_vae_tokens` 生成 `(t,h,w)` position ids。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:571`：实现 $\mathrm{TPS} = \mathrm{fps} / c_{\mathrm{temporal}}$ 和 $\mathrm{TPS}_{\mathrm{base}} = \mathrm{fps}_{\mathrm{base}} / c_{\mathrm{base}}$。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:575`：实现 scaled temporal index。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:586`：生成 spatial `h/w` grid。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:949`：vision token 调用 mRoPE 生成函数。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1027`：action token 调用同一函数，`grid_h=grid_w=1`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1104`：sound token 调用同一函数，`grid_h=grid_w=1`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1386`：文本后加入 `unified_3d_mrope_temporal_modality_margin`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:205`：`Cosmos3VLTextRotaryEmbedding` 把三维 position ids 变成 rotary cos/sin。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:593`：默认 `base_fps=24`，`enable_fps_modulation=True`，`position_embedding_type="unified_3d_mrope"`，`unified_3d_mrope_temporal_modality_margin=15000`。

#### 图片素材

- `assets/mrope_coordinate_assignment.png`
- 原始论文图：`source/src/figures/model_architecture/tikz_mrope_coordinate_assignment.pdf`

### Q3. 模型如何针对不同模态进行 encoding？

#### 结论

Cosmos 3 的 encoding 不是“所有模态共用一个 encoder”，而是：

```text
raw modality input
  -> modality-specific tokenizer / encoder
  -> modality token
  -> linear or domain-aware projection into transformer hidden space
  -> add modality embedding for non-language modalities
  -> pack into AR subsequence or DM subsequence
  -> MoT backbone
```

论文在 `Model Architecture / Encoders` 里明确说：语言、视觉、音频、动作先通过各自 encoder 映射到统一 representation space；为了让共享 transformer 和 positional embedding 区分模态，还会对非语言模态加入可学习的 modality-specific embedding。随后这些 token 被放进统一序列格式中：AR subsequence 负责理解/推理，DM subsequence 负责扩散式生成。

![Cosmos 3 model architecture](code/src/cosmos-main/cookbooks/cosmos3/cosmos3-model-architecture.png)

#### 总体分工：AR 编码 vs DM 编码

Cosmos 3 把 token 分成两段：

- `AR subsequence`：用于语言生成、图文/视频理解。里面放 language token，以及由 ViT/Qwen3-VL 视觉塔编码的 image/video token。
- `DM subsequence`：用于图像、视频、音频、动作生成。里面放由 VAE/audio VAE/action interface 得到的 token，模型通过 iterative denoising 预测 clean token。

这意味着同一个 image/video 在不同任务里可能走两套视觉编码路径：

- 做理解时：image/video -> ViT visual encoder -> AR visual tokens。
- 做生成或 world modeling 时：image/video -> video VAE -> latent tokens -> DM vision tokens。

这是 Cosmos 3 的核心设计之一：理解侧保留 VLM 风格的视觉语义编码，生成侧使用连续 latent token 更适合 diffusion/flow matching。

#### 1. Language encoding

语言是最接近传统 LLM 的路径：

```text
text prompt
  -> tokenizer / chat template
  -> token ids
  -> embedding table embed_tokens
  -> AR subsequence
```

在 diffusers pipeline 里，caption 会先经过 tokenizer 的 chat template，得到 text token ids；进入模型时由 `embed_tokens` 查表得到 hidden states。

源码对应：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:193`：`tokenize_caption` 使用 chat template 组织 prompt。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:668`：`encode_text` 把 `packed_seq.text_ids` 编成 hidden states。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:634`：`self.embed_tokens = nn.Embedding(...)`。

理解版 Reasoner 更接近标准 Qwen3-VL：released wrapper 只加载 understanding tower，即 language model 和 visual tower；generation/audio/action 相关权重会被过滤掉。

源码对应：

- `code/src/cosmos-framework-main/packages/transformers-cosmos3/transformers_cosmos3/model.py:8`：定义需要丢弃的 generation/audio/action 权重模式。
- `code/src/cosmos-framework-main/packages/vllm-cosmos3/vllm_cosmos3/model.py:17`：只保留 `lm_head`、`model.language_model`、`model.visual` 前缀。

#### 2. Image / Video understanding encoding

论文说视觉输入有两个 encoder。第一个是 understanding encoder：

```text
image / video
  -> ViT encoder pretrained with vision-language alignment
  -> 16 x 16 visual patches
  -> 2-layer MLP merges 2 x 2 visual tokens
  -> transformer latent space
  -> AR subsequence
```

它还沿用 Qwen3-VL 的两个机制：

- `DeepStack`：聚合 ViT 多层视觉特征。
- text-based video timestamps：把文本形式的时间戳和视频帧交织，让模型知道视频帧的时间位置。

这里的编码目标是“理解”：把图像/视频变成和语言可对齐的语义 token。所以它放在 AR subsequence，模型像 VLM 一样做 caption、QA、planning、reasoning。

原文依据：

- `source/src/sections/2__model.tex:10`：说明 visual understanding 使用 ViT encoder，patch size 为 $16 \times 16$，MLP 合并 $2 \times 2$ token，并使用 DeepStack 和视频时间戳。
- `source/src/sections/2__model.tex:57`：说明 AR subsequence 包含 language token 和 ViT 编码的 image/video token。

#### 3. Image / Video generation encoding

第二个视觉 encoder 是 generation encoder，走 video VAE：

```text
image / video frames
  -> Wan2.2 video VAE encoder, frozen
  -> latent
  -> spatial 2 x 2 latent patch merge
  -> patch latent vector
  -> linear projection vae2llm / proj_in
  -> DM vision tokens
```

其中 video VAE 的输入/输出形状可以写成：

$$
\mathbf{x}_{\mathrm{video}} \in \mathbb{R}^{B \times 3 \times T \times H \times W}
\quad\longmapsto\quad
\mathbf{z}_{\mathrm{vae}} \in \mathbb{R}^{B \times d_z \times T/4 \times H/16 \times W/16}.
$$

论文说 VAE 总体压缩率是时间 $4\times$、空间 $32\times32$：代码里 VAE 本身输出 $H/16, W/16$ latent，再通过 `latent_patch_size=2` 的 patchify 合并 $2\times2$ latent patch，因此等价于论文里的 $16\times16$ VAE spatial compression + $2\times2$ patch merge。

generation 侧不是把 pixel 直接送入 transformer，而是把 VAE latent patch 投影到 hidden dimension。论文明确提到这一层，但没有使用源码里的名字 `vae2llm` 或 `proj_in`。原文是：“We use a linear layer to project each VAE token into the transformer's hidden dimension before feeding the latents into the MoT backbone.” 位置：`source/src/sections/2__model.tex:10`。

对应到源码：

- 训练侧叫 `vae2llm`：`code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:157`
- diffusers 导出侧叫 `proj_in`：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:651`
- 权重映射里明确把 `proj_in.*` 映射为 `vae2llm.*`：`code/src/cosmos-framework-main/cosmos_framework/inference/model.py:81`

为什么 generation 必须要这个 projection：VAE latent token 和 transformer hidden state 维度不一样。源码默认配置里：

- $\mathrm{hidden\_size}=4096$
- $\mathrm{latent\_channel}=48$
- $\mathrm{latent\_patch\_size}=2$
- $\mathrm{patch\_latent\_dim}=192$

因为：

$$
\mathrm{patch\_latent\_dim}
= \mathrm{latent\_channel}\cdot \mathrm{latent\_patch\_size}^{2}
= 48 \cdot 2^{2}
= 192.
$$

VAE latent patch 是 $192$ 维，而 MoT/LLM backbone 的 token hidden state 是 $4096$ 维。如果没有 `vae2llm/proj_in` 完成

$$
\mathbb{R}^{192}
\longrightarrow
\mathbb{R}^{4096},
$$

VAE token 不能直接进入 transformer 的 attention、MLP、RMSNorm 等层。

此外，VAE 是 frozen tokenizer，不负责适配 MoT hidden space。VAE 的职责只是把 pixel/video 压缩成连续 latent，不会自己学习成 MoT 可用的 $4096$ 维 token 表示。这个适配任务必须由一个可训练的 projection layer 完成。

输出时再走反方向：

$$
\mathbf{z}_{\mathrm{patch}}
\in \mathbb{R}^{192}
\xrightarrow{\mathrm{vae2llm/proj\_in}}
\mathbf{h}
\in \mathbb{R}^{4096}
\xrightarrow{\mathrm{llm2vae/proj\_out}}
\widehat{\mathbf{z}}_{\mathrm{patch}}
\in \mathbb{R}^{192}.
$$

模型在 diffusion/flow matching 过程中不是预测文字 token，而是预测 noisy VAE latent 的 denoising/velocity 目标。所以最后必须把 transformer hidden state 投回 VAE latent patch 维度，才能 unpatchify 并交给 VAE decoder 还原图像/视频。

这里要区分 Cosmos 3 的 `patchify` 和 `vae2llm/proj_in`。它们相关，但不是同一个东西：

$$
\mathbf{z}_{\mathrm{vae}}
\in \mathbb{R}^{C \times T \times H \times W}
\xrightarrow{\mathrm{patchify/pack}}
\mathbf{p}
\in \mathbb{R}^{N_{\mathrm{patch}} \times d_{\mathrm{patch}}}
\xrightarrow{\mathrm{vae2llm/proj\_in}}
\mathbf{h}
\in \mathbb{R}^{N_{\mathrm{patch}} \times d_{\mathrm{model}}}.
$$

`patchify` 主要解决 tokenization / 序列化问题：把 VAE latent 的空间块合并成一个个 patch token。它改变的是 token 数量和每个 token 覆盖的空间范围。以默认配置为例：

$$
d_{\mathrm{patch}}
= 2 \times 2 \times 48
= 192.
$$

源码里 patchify 基本是 reshape + einsum：

```python
latent = latent.reshape(latent_channel, t_actual, h_patches, p, w_patches, p)
latent = torch.einsum("cthpwq->thwpqc", latent).reshape(-1, p * p * latent_channel)
```

位置：`code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:279`

`vae2llm/proj_in` 解决的是 hidden-space adapter 问题：把 patchify 后的 $192$ 维 VAE patch vector 映射到 MoT backbone 的 $4096$ 维 hidden state。和常见 diffusion transformer 的 patch embedding 相比，`patchify + vae2llm` 合起来类似 patch embedding；但严格讲，`patchify` 本身不是 `vae2llm/proj_in`，`vae2llm/proj_in` 是 patchify 之后的可训练线性适配层。

源码对应：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:82`：`DiffusersWan22VAE` 是 Wan2.2 VAE wrapper。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:131`：VAE encode，把 $\left[B,3,T,H,W\right]$ 编成 $\left[B,d_z,T/4,H/16,W/16\right]$。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:253`：`patchify_and_pack_latents` 做 latent patch merge 和 flatten。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:699`：generation pipeline 将 vision latents patchify。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:702`：`proj_in` 把 VAE latent patch 投影到 hidden space。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:590`：默认 `hidden_size=4096`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:596`：默认 `latent_channel=48`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:605`：默认 `latent_patch_size=2`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:611`：默认 `patch_latent_dim=192`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:652`：diffusers 侧 `proj_out`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:157`：训练侧命名为 `vae2llm`，即 VAE latent -> LLM hidden。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:158`：训练侧 `llm2vae`，即 LLM hidden -> VAE latent。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:636`：`packed_tokens_vision = self.vae2llm(...)`。

#### 4. Audio encoding

音频走 audio VAE：

```text
raw stereo audio, 48 kHz
  -> audio VAE, frozen
  -> 25 tokens / second
  -> linear projection sound2llm / audio_proj_in
  -> add sound/audio modality embedding
  -> DM sound tokens
```

论文指定 raw audio 是 48 kHz stereo，audio VAE hop size 是 1920 samples，所以 $\frac{48000}{1920}=25$ tokens/s。audio VAE 冻结，只训练进入 MoT 前后的线性投影和后续 MoT 参数。

对应的 token rate 是：

$$
\mathrm{TPS}_{\mathrm{audio}}
= \frac{48000}{1920}
= 25.
$$

源码里训练侧更完整：`encode_sound` 先把 waveform 编成 $\left[C_{\mathrm{sound}},T_{\mathrm{sound}}\right]$ latent，然后 `sound2llm` 投影到 hidden dimension，并加 `sound_modality_embed`。diffusers wrapper 中对应字段命名为 `audio_proj_in/audio_proj_out/audio_modality_embed`。

源码对应：

- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2878`：检测 sound/audio 数据并调用 `encode_sound`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:4295`：`encode_sound` 把 waveform 编成 audio latent。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:4311`：调用 `tokenizer_sound_gen.encode(...)` 得到 $\left[1,C_{\mathrm{sound}},T_{\mathrm{sound}}\right]$。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:215`：`sound2llm = nn.Linear(sound_dim, hidden_size)`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:217`：定义 `sound_modality_embed`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:887`：`sound2llm(packed_tokens_sound) + sound_modality_embed`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:661`：diffusers 侧对应 `audio_proj_in`。

#### 5. Action encoding

Action 是 Cosmos 3 相比普通 VLM / video model 更特殊的模态。它不是文本 token，也不是图像 patch，而是物理控制/状态转移 token。

![Action representation](action_representation.png)

论文先把不同 embodiment 的控制信号统一成 action interface：

```text
embodiment-specific native controls
  -> normalized action vector
     - ego pose delta
     - effector pose delta
     - grasp state
  -> domain-aware projection with domain id k
  -> action hidden token
  -> add action modality embedding
  -> DM action tokens
```

动作 token 的语义是“从上一个世界状态到当前世界状态的因果变量”。例如连续视频状态 $\mathbf{v}_{t-1}$ 到 $\mathbf{v}_{t}$ 之间，action token $\mathbf{a}_t$ 表示导致这个状态变化的控制量。

为了兼容自动驾驶、机器人、相机运动、egocentric human motion 等不同 embodiment，Cosmos 3 不直接把每个系统的原生命令塞进模型，而是把它们归一到共享几何结构：

- `ego pose`：主体观察坐标系的位姿变化。
- `effector pose`：末端执行器或手腕等 effectors 的位姿变化。
- `grasp state`：夹爪开合、指尖位置等当前操作状态。

位姿变化用相邻 SE(3) 的相对变换表示：

$$
\Delta \mathbf{T}_{t}
= \mathbf{T}_{t-1}^{-1}\mathbf{T}_{t}.
$$

旋转采用 6D rotation representation；预测后再通过 SVD 转回合法的 `SO(3)` 旋转矩阵。

关键是 `domain-aware projection`。不同 embodiment 的 action 维度和语义不同，所以代码不是用一个普通 Linear，而是按 domain id 选择不同权重：

$$
\mathbf{z}
= \mathbf{W}_{\mathrm{in}}^{(k)}\mathbf{x}
+ \mathbf{b}_{\mathrm{in}}^{(k)},
\qquad
\mathbf{x}
= \mathbf{W}_{\mathrm{out}}^{(k)}\mathbf{z}
+ \mathbf{b}_{\mathrm{out}}^{(k)}.
$$

其中 $k$ 是 embodiment domain id。这样共享 MoT backbone，但 action 输入/输出投影保留 domain-specific structure。

源码对应：

- `source/src/sections/2__model.tex:17`：说明支持 autonomous vehicles、camera motion、robots、egocentric human motion 等 embodiment。
- `source/src/sections/2__model.tex:20`：定义 action token 表示世界状态转移的因果变量。
- `source/src/sections/2__model.tex:25`：定义 $\Delta \mathbf{T}_{t} = \mathbf{T}_{t-1}^{-1}\mathbf{T}_{t}$。
- `source/src/sections/2__model.tex:33`：说明 action tokenization 使用 domain-aware projection。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:158`：`DomainAwareLinear`，每个 domain 一套 weight/bias。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:183`：根据 `domain_id` 取出对应权重。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:188`：`action2llm = DomainAwareLinear(...)`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:755`：action token 经 `action2llm` 投影。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/mot/cosmos3_vfm_network.py:768`：加 `action_modality_embed`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2874`：从 batch 中归一化并取出 `raw_state_action, action_domain_id`。

#### 6. Encoding 后如何统一到一条序列

不同模态各自编码后，会进入统一 packing：

```text
AR part:
  language tokens
  ViT image/video understanding tokens

DM part:
  VAE image/video tokens
  audio VAE tokens
  action tokens
```

DM 内部还有固定顺序：

```text
clean conditioning tokens first
noisy target tokens later
vision -> audio -> action
```

源码中 `GenerationDataClean` 明确保存不同模态的 clean tokens：`x0_tokens_vision`、`x0_tokens_action`、`x0_tokens_sound`。随后 `_pack_vision_tokens`、`_pack_sound_tokens`、`_pack_action_tokens` 分别把各模态 token 写入统一 `PackedSequence`，并记录 sequence index、condition mask、noisy frame index、mse loss index 和 3D mRoPE position ids。

源码对应：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:13`：`GenerationDataClean` 数据结构。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:878`：pack vision tokens。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:969`：pack action tokens。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1049`：pack sound/audio tokens。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/pipeline.py:627`：generation pipeline 调用 `pack_input_sequence`。

#### 源码和论文对齐后的理解

从 paper 到 code，可以把 Cosmos 3 的 encoding 理解成四类接口：

- `text2llm`：离散文本 token 经 embedding table 进入 AR。
- `vit2llm`：理解侧视觉 token 经 ViT/Qwen3-VL visual tower 进入 AR。
- `vae2llm / sound2llm`：连续生成 latent 经线性投影进入 DM。
- `action2llm`：连续物理动作向量经 domain-aware projection 进入 DM。

所以 Cosmos 3 的“统一”不是统一 encoder，而是统一 latent space、统一时空位置编码、统一 packing 格式和统一 MoT backbone。前端 encoding 仍然保留模态专用结构，这是它能同时处理 language、vision、audio、action 的关键。

#### 原文依据

- `source/src/sections/2__model.tex:4`：说明 Cosmos 3 支持 multimodal inputs/outputs，并把 action 作为核心模态。
- `source/src/sections/2__model.tex:7`：说明不同模态用 modality-specific encoders 投影到统一表示空间，并对非语言模态加 modality-specific embedding。
- `source/src/sections/2__model.tex:10`：说明 image/video 的 ViT encoder 和 VAE encoder 双路径。
- `source/src/sections/2__model.tex:13`：说明 audio VAE、48 kHz、hop size 1920、25 tokens/s。
- `source/src/sections/2__model.tex:17`：说明 action 跨 embodiment 的统一接口。
- `source/src/sections/2__model.tex:33`：说明 action 使用 domain-aware input/output projections。
- `source/src/sections/2__model.tex:50`：说明所有 segment 编码后使用统一 token arrangement。
- `source/src/sections/2__model.tex:57`：说明 AR subsequence 包含 language 和 ViT image/video tokens。
- `source/src/sections/2__model.tex:60`：说明 DM subsequence 包含 VAE image/video、audio 和 action tokens。
- `source/src/sections/2__model.tex:62`：说明 DM 内部 clean conditioning、noisy diffusion、vision/audio/action 的顺序。

#### 图片素材

- `code/src/cosmos-main/cookbooks/cosmos3/cosmos3-model-architecture.png`
- `assets/action_representation.png`
- 原始 action 图：`source/src/figures/model_architecture/action/tikz_action_representation.pdf`

### Q4. MoT 结构是什么？为什么 Cosmos 3 要用 Mixture-of-Transformers？

#### 一句话结论

Cosmos 3 的 MoT 是“同一条 packed multimodal sequence + 每层两套 transformer pathway”。AR subsequence 走 reasoner tower，保留 VLM/LLM 的理解和自回归生成能力；diffusion subsequence 走 generator tower，学习图像、视频、音频、动作的扩散/flow matching 生成能力。两套参数分离，但 diffusion token 可以通过 dual-stream joint attention 读取 AR token 的条件信息。

![MoT architecture](mot_architecture.png)

#### MoT 解决的核心冲突

Cosmos 3 同时要做两类目标：

- `Reasoner / understanding`：语言、图像/视频理解、规划、问答，要求 causal autoregressive behavior，继承 VLM 的语义能力。
- `Generator / world simulation`：图像、视频、音频、动作 denoising，要求 diffusion/flow matching behavior，目标是连续 latent 的生成质量和时空一致性。

如果所有 token 都共享同一套 transformer 参数，两个训练目标会互相干扰：reasoning 需要稳定的 causal language/vision representation；generation 需要处理 noisy latent、timestep embedding、full attention 和连续输出头。MoT 的设计是把这两个能力放到同一个 layer 里，但用不同参数路径承载。

#### Layer 级结构：一层里有两条路径

论文说每个 transformer decoder layer 有两套参数：

- reasoner pathway：处理 AR subsequence。
- generator pathway：处理 diffusion subsequence。

标准 transformer decoder layer 通常由 self-attention、FFN/MLP、normalization 组成。Cosmos 3 的 MoT layer 把这些模块复制成两套：

| 模块 | Reasoner tower | Generator tower |
| --- | --- | --- |
| input norm | `input_layernorm` | `input_layernorm_moe_gen` |
| attention Q/K/V | `to_q`, `to_k`, `to_v` | `add_q_proj`, `add_k_proj`, `add_v_proj` |
| attention output | `to_out` | `to_add_out` |
| post-attn norm | `post_attention_layernorm` | `post_attention_layernorm_moe_gen` |
| MLP | `mlp` | `mlp_moe_gen` |
| final norm | `norm` | `norm_moe_gen` |

源码中 `Cosmos3VLTextMoTDecoderLayer` 明确有两套 norm 和 MLP；`PackedAttentionMoT` 则在 Qwen3-VL 原有 attention projection 外，额外加了 generation pathway 的 Q/K/V/out projection。

#### Token 路由：AR 走 reasoner，DM 走 generator

在 sequence packing 阶段，Cosmos 3 把 token 标成两类 attention mode：

- text / AR visual understanding tokens 被标成 `causal`。
- VAE vision、audio、action 等 diffusion tokens 被标成 `full`。

源码里 `_init_sequence_pack` 根据 `attn_modes` 建立两组索引：

$$
\mathcal{I}_{\mathrm{AR}}
= \{i \mid \mathrm{attn\_mode}_i = \mathrm{causal}\},
\qquad
\mathcal{I}_{\mathrm{DM}}
= \{i \mid \mathrm{attn\_mode}_i = \mathrm{full}\}.
$$

进入 transformer layer 后：

$$
\mathbf{H}_{\mathrm{AR}}
= \mathbf{H}[\mathcal{I}_{\mathrm{AR}}],
\qquad
\mathbf{H}_{\mathrm{DM}}
= \mathbf{H}[\mathcal{I}_{\mathrm{DM}}].
$$

`get_und_seq(pack)` 取出 reasoner/understanding tokens，`get_gen_seq(pack)` 取出 generator tokens。处理完后再用 `from_und_gen_splits(...)` 合回同一个 packed sequence。

#### Dual-stream joint attention：参数分离，信息流是单向条件注入

MoT 容易被误解成两套完全隔离的模型，或者误解成 reasoner/generator 双向互相 attend。实际都不准确。参数路径分离，但 attention 里只允许 diffusion token 读取 AR 条件；AR/reasoner token 不会 attend generator/DM 内容。

论文定义 AR attention 为 causal self-attention：

$$
\mathbf{O}_{\mathrm{AR}}
= \operatorname{Attn}_{\mathrm{causal}}
\left(
\mathbf{Q}_{\mathrm{AR}},
\mathbf{K}_{\mathrm{AR}},
\mathbf{V}_{\mathrm{AR}}
\right).
$$

也就是 AR token 只看 AR 内部过去 token，保持 VLM/LLM 的 causal 属性。

DM attention 是 full attention，query 来自 DM token，但 key/value 来自 AR 和 DM 的拼接：

$$
\mathbf{O}_{\mathrm{DM}}
= \operatorname{Attn}_{\mathrm{full}}
\left(
\mathbf{Q}_{\mathrm{DM}},
\left[\mathbf{K}_{\mathrm{AR}};\mathbf{K}_{\mathrm{DM}}\right],
\left[\mathbf{V}_{\mathrm{AR}};\mathbf{V}_{\mathrm{DM}}\right]
\right).
$$

这表示生成 token 可以看文本 prompt、条件图像/视频 token、其他 diffusion token，从而做条件生成和保持时空一致性。反过来，AR token 的 attention 只在 AR causal stream 内部计算，既不会把 DM token 放进自己的 K/V，也不会被 DM token 更新。因此 noisy generation target 不会污染 conditioning pathway。

源码实现也正是这个方向：

- `causal_out`：用 causal Q/K/V，`is_causal=True`。
- `full_out`：用 generation/full Q，但 K/V 是 `get_all_seq(...)`，也就是同样本内全部 AR+DM token，`is_causal=False`。

更严格地说，论文里 “tokens from the diffusion subsequence interact with the AR subsequence” 的主语是 diffusion subsequence。这里的 interaction 不是两个塔互相读，而是 generator stream 对 reasoner stream 的单向条件读取。代码上也能直接看出来：`causal_out` 的 Q/K/V 都来自 `get_causal_seq(...)`，没有调用 `get_all_seq(...)`；只有 `full_out` 的 K/V 使用 `get_all_seq(...)`。

更直观地说，attention mask 对两路 query 的上下文是：

| query 来源 | 可 attend 的 K/V | 是否看另一塔 |
| --- | --- | --- |
| AR / reasoner query | AR 过去 token | 不看 DM |
| DM / generator query | AR + DM token | 看 AR 条件 |

#### 代码里的 MoT forward 流程

在 `PackedAttentionMoT.forward` 中，reasoner 和 generator 的 Q/K/V 是分开投影的：

```python
q_und_in = self.to_q(get_und_seq(pack))
q_gen_in = self.add_q_proj(get_gen_seq(pack))

k_und_in = self.to_k(get_und_seq(pack))
k_gen_in = self.add_k_proj(get_gen_seq(pack))

v_und_in = self.to_v(get_und_seq(pack))
v_gen_in = self.add_v_proj(get_gen_seq(pack))
```

随后把 reasoner 和 generator 的 Q/K/V 合成 packed states，交给 `CosmosAttnProcessor3_0` 做 two-way attention。attention 输出后又按路径拆开：

```python
und_seq = self.to_out(get_und_seq(packed_attn_output))
gen_seq = self.to_add_out(get_gen_seq(packed_attn_output))
```

然后 `Cosmos3VLTextMoTDecoderLayer.forward` 分别做 residual、post-attention norm 和 MLP：

```python
ln_out_und = self.post_attention_layernorm(residual_und)
ln_out_gen = self.post_attention_layernorm_moe_gen(residual_gen)

mlp_out_und_unpadded = self.mlp(ln_out_und_unpadded)
mlp_out_gen_unpadded = self.mlp_moe_gen(ln_out_gen_unpadded)
```

所以代码层面可以把一层 MoT 写成：

$$
\mathbf{H}'_{\mathrm{AR}}
= \mathrm{Layer}_{\mathrm{reasoner}}
\left(\mathbf{H}_{\mathrm{AR}};\mathbf{H}_{\mathrm{AR}}\right),
$$

$$
\mathbf{H}'_{\mathrm{DM}}
= \mathrm{Layer}_{\mathrm{generator}}
\left(\mathbf{H}_{\mathrm{DM}};\left[\mathbf{H}_{\mathrm{AR}};\mathbf{H}_{\mathrm{DM}}\right]\right).
$$

分号前可以理解为 query 来源，分号后是 key/value 上下文。

#### 为什么不是普通 MoE？

这里的 `MoT` 不是 token-level expert router 的普通 MoE。普通 MoE 通常是在 MLP 层里根据 token 动态选择 expert；Cosmos 3 的 MoT 是按序列区域和任务类型固定路由：

- AR subsequence 固定走 reasoner tower。
- DM subsequence 固定走 generator tower。
- 两个 tower 都是 transformer pathway，而不是只替换 FFN expert。
- attention 信息流是人为设计的：AR causal，DM full-attend AR+DM。

所以更准确地说，Cosmos 3 的 MoT 是 task-pathway mixture，而不是 sparse expert mixture。

#### 和训练策略的关系

论文强调 Cosmos 3 的 Generator 从训练好的 Reasoner 初始化。MoT 让这个策略可行：

- reasoner tower 可以继承并保留 VLM 的语言/视觉理解能力。
- generator tower 可以从同样的 VLM 权重初始化，然后专门学习 diffusion/flow matching。
- Generator pre-training 时可以冻结 reasoner tower，只更新 generation-specific 参数，避免生成训练破坏语言/视觉理解。

这也是为什么 MoT 对 Cosmos 3 很关键：它不是为了“多加参数”本身，而是为了把 VLM reasoning 和 world generation 放进一个模型，同时降低互相破坏。

#### 原文依据

- `source/src/sections/2__model.tex:111`：说明每个 decoder layer 有 reasoner 和 generator 两套参数。
- `source/src/sections/2__model.tex:118`：说明每条 pathway 都是标准 transformer layer，包含 norm、attention projection、FFN，并且 AR 路由到 reasoner，diffusion 路由到 generator。
- `source/src/sections/2__model.tex:121`：定义 AR/DM 的 Q/K/V。
- `source/src/sections/2__model.tex:123`：定义 AR causal self-attention。
- `source/src/sections/2__model.tex:132`：定义 DM full bidirectional attention，K/V 来自 AR+DM。
- `source/src/sections/2__model.tex:142`：说明 AR tokens 不会基于 DM tokens 更新，保护 conditioning pathway 的 causal integrity。

#### 源码依据

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:77`：根据 `attn_modes` 初始化 causal/full token 索引。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:127`：`to_factored_sequence_pack` 把 packed sequence 拆成 `causal_seq` 和 `full_only_seq`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:345`：`from_und_gen_splits` 把 reasoner/generator 输出合回序列。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:364`：`get_und_seq` 取 reasoner/understanding tokens。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:397`：`get_gen_seq` 取 generator tokens。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:871`：text segment 标成 `causal`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1563`：diffusion segment 标成 `full`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:74`：`CosmosAttnProcessor3_0` 实现 causal/full two-way attention。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:333`：`PackedAttentionMoT` 定义双路径 attention。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:353`：generation pathway 额外 Q/K/V/out projection。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:394`：reasoner/generator 分别投影 Q/K/V。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:476`：reasoner/generator attention 输出分别走 `to_out` 和 `to_add_out`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:481`：`Cosmos3VLTextMoTDecoderLayer` 定义 MoT decoder layer。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:501`：reasoner/generator 各自 MLP。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:504`：reasoner/generator 各自 norm。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:635`：`Cosmos3OmniTransformer` 堆叠 `Cosmos3VLTextMoTDecoderLayer`。

#### 图片素材

- `assets/mot_architecture.png`
- 原始论文图：`source/src/figures/model_architecture/tikz_mot_architecture.pdf`

### Q5. Cosmos 3 有多少个不同规格的模型？模型结构超参是多少？

#### 结论

按论文的 architecture scale 来看，Cosmos 3 有三种规格：

- `Cosmos3-Edge`：4B-parameter MoT model，基于 dense 2B transformer。
- `Cosmos3-Nano`：16B-parameter MoT model，基于 dense 8B transformer。
- `Cosmos3-Super`：64B-parameter MoT model，基于 dense 32B transformer。

论文当前 open-weight 发布的是 Nano 和 Super，以及基于它们 post-training 得到的专家 checkpoint；Edge 在论文中说明为 later release。Post-trained 模型如 `Cosmos3-Super-Text2Image`、`Cosmos3-Super-Image2Video`、`Cosmos3-Nano-Policy-DROID` 不是新的结构规格，它们和对应 mid-trained base model 共享相同 architecture。

#### 三档结构超参

论文的 model variants 表给出的核心 LLM/MoT backbone 超参如下：

| Variant | MoT total params | Dense transformer base | LLM layers | Hidden dim | Attn heads | KV heads | Head dim | FFN dim |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Cosmos3-Edge` | 4B | 2B | $28$ | $2048$ | $16$ | $8$ | $128$ | $9216$ |
| `Cosmos3-Nano` | 16B | 8B | $36$ | $4096$ | $32$ | $8$ | $128$ | $12288$ |
| `Cosmos3-Super` | 64B | 32B | $64$ | $5120$ | $64$ | $8$ | $128$ | $25600$ |

这里 “MoT total params” 可以理解为双塔 MoT 后的总规模；“dense transformer base” 是对应单塔 dense transformer/VLM 初始化规模。论文表格的 caption 也强调：每层有 reasoner/generator 两套独立参数集，所以 MoT 总参数大约是 dense base 的两倍，再加上多模态 encoder/projection/head 等外围参数。

#### 初始化来源

三档模型的初始化方式不同：

- `Cosmos3-Edge`：使用 2B dense transformer 设计，从 scratch 训练 LLM，整体设计接近 Qwen3-1.7B，但去掉 QK norm，FFN activation 使用 ReLU-squared。
- `Cosmos3-Nano`：适配 Qwen3-VL 8B，LLM 结构为 $36$ layers、$4096$ hidden、$32$ attention heads。
- `Cosmos3-Super`：适配 Qwen3-VL 32B，LLM 结构为 $64$ layers、$5120$ hidden、$64$ attention heads。

#### 代码默认值对应哪一档？

当前 diffusers wrapper 的 `Cosmos3OmniTransformer` 默认 config 对应 Nano 规格：

$$
L = 36,\quad
d_{\mathrm{model}} = 4096,\quad
n_{\mathrm{heads}} = 32,\quad
n_{\mathrm{kv}} = 8,\quad
d_{\mathrm{head}} = 128,\quad
d_{\mathrm{ffn}} = 12288.
$$

源码位置：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:590`：`hidden_size=4096`
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:592`：`intermediate_size=12288`
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:608`：`num_attention_heads=32`
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:609`：`num_hidden_layers=36`
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:610`：`num_key_value_heads=8`
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:588`：`head_dim=128`

同一个 config 还包含 generation 侧通用超参：

| 超参 | 默认值 | 含义 |
| --- | ---: | --- |
| `latent_channel` | $48$ | Wan VAE latent channel |
| `latent_patch_size` | $2$ | VAE latent 上的 spatial patch merge size |
| `patch_latent_dim` | $192$ | $48 \times 2^2$ |
| `base_fps` | $24$ | unified 3D mRoPE FPS base |
| `position_embedding_type` | `unified_3d_mrope` | 统一时空位置编码 |
| `unified_3d_mrope_temporal_modality_margin` | $15000$ | AR-DM temporal gap |
| `vocab_size` | $151936$ | text vocab size |
| `max_position_embeddings` | $262144$ | max positions |

#### Open-weight checkpoint 数量如何理解？

论文模型表列出的 open-weight checkpoint 有 5 个：

- `Cosmos3-Super`
- `Cosmos3-Nano`
- `Cosmos3-Super-Text2Image`
- `Cosmos3-Super-Image2Video`
- `Cosmos3-Nano-Policy-DROID`

但从 architecture scale 角度，只有 Nano/Super 两档已发布；T2I/I2V/Policy-DROID 是 post-trained specialization。论文的数据课程图和 generator data 章节都说明这些 specialized models 与对应 mid-trained model 使用相同 architecture。

#### 原文依据

- `source/src/sections/2__model.tex:170`：说明 Cosmos 3 有 Edge、Nano、Super 三个 model scales，并给出 4B/16B/64B 与 2B/8B/32B dense base 的对应关系。
- `source/src/sections/2__model.tex:172`：说明 Edge 的层数、hidden size、attention heads、KV heads、head dim、FFN dim，以及从 scratch 训练和 Qwen3-1.7B 近似设计。
- `source/src/sections/2__model.tex:174`：说明 Nano 适配 Qwen3-VL 8B 和关键结构超参。
- `source/src/sections/2__model.tex:176`：说明 Super 适配 Qwen3-VL 32B 和关键结构超参。
- `source/src/tables/model_architecture/model_variants.tex:14`：Edge 表格行。
- `source/src/tables/model_architecture/model_variants.tex:15`：Nano 表格行。
- `source/src/tables/model_architecture/model_variants.tex:16`：Super 表格行。
- `source/src/sections/0__model_table.tex:34`：列出 open-weight `Cosmos3-Super`。
- `source/src/sections/0__model_table.tex:35`：列出 open-weight `Cosmos3-Nano`。
- `source/src/sections/0__model_table.tex:36`：列出 open-weight `Cosmos3-Super-Text2Image`。
- `source/src/sections/0__model_table.tex:37`：列出 open-weight `Cosmos3-Super-Image2Video`。
- `source/src/sections/0__model_table.tex:38`：列出 open-weight `Cosmos3-Nano-Policy-DROID`。
- `source/src/sections/data/generator.tex:4`：说明 post-trained 专家模型与对应 mid-trained model 共享相同 architecture。
- `source/src/figures/data/data_curriculum.tex:9`：说明 post-training 产生 T2I/I2V/Policy-DROID，且架构不变。

#### 源码依据

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:580`：`Cosmos3OmniTransformer` config 定义入口。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:588`：默认 `head_dim=128`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:590`：默认 `hidden_size=4096`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:592`：默认 `intermediate_size=12288`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:596`：默认 `latent_channel=48`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:601`：默认 `position_embedding_type="unified_3d_mrope"`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:603`：默认 `unified_3d_mrope_temporal_modality_margin=15000`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:605`：默认 `latent_patch_size=2`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:608`：默认 `num_attention_heads=32`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:609`：默认 `num_hidden_layers=36`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:610`：默认 `num_key_value_heads=8`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:611`：默认 `patch_latent_dim=192`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:625`：默认 `vocab_size=151936`。

---

### Q6. 这些模型都是怎么训练出来的？整体流程是什么？

#### 结论先行

Cosmos 3 的训练不是“一个模型从头端到端直接训完”，而是一个分阶段 curriculum：

1. 先训练 `Reasoner`，目标是理解、推理、空间/时间/物理/动作语义建模。
2. 用训练好的 `Reasoner` 权重初始化 `Generator`，因为两者共享 transformer block 形态，语义和世界知识可以迁移到生成塔。
3. `Generator` 再走 progressive curriculum：先学 image/video/audio 生成，再在 mid-training 引入 action 和 transfer control，最后对 T2I、I2V、robot policy 做独立 post-training。

论文的数据课程图如下：

![Cosmos 3 generator data curriculum](data_curriculum.png)

用公式概括，Reasoner 是自回归监督学习：

$$
\mathcal{L}_{\text{AR}}
=
-\sum_{t=1}^{T} w_t \log p_{\theta}(y_t \mid y_{<t}, x_{\text{media}})
$$

其中 $x_{\text{media}}$ 是 image/video/text context，$w_t$ 是论文提到的 square-root normalized per-token weighting。

Generator 是 rectified flow matching：

$$
x_{\sigma}
=
\sigma \epsilon + (1-\sigma)x_0,
\qquad
\epsilon \sim \mathcal{N}(0,I),
\qquad
\sigma \in [0,1]
$$

$$
v^{\star}
=
\epsilon - x_0
$$

$$
\mathcal{L}_{\text{FM}}
=
\frac{1}{|\Omega|}
\sum_{i \in \Omega}
m_i
\left\|
v_{\theta}(x_{\sigma},\sigma,c)_i - v^{\star}_i
\right\|_2^2
$$

其中 $m_i = 1$ 表示 noisy/generation token 参与 loss，$m_i = 0$ 表示 clean conditioning token 不参与 loss。源码里对应的是 `noisy_mask_i = 1.0 - condition_mask[i]`。

#### 总流程表

| 阶段 | 训练对象 | 数据 | Loss | 训练方式 | 目的 |
| --- | --- | --- | --- | --- | --- |
| Reasoner pre-training | LM + ViT + multimodal projector | $22.0$M multimodal samples：image-text、video-text、text-only | next-token prediction / cross entropy | 所有组件从开始 joint training，不做 projector-only alignment；训练 $2$ epochs，最长 $16$k tokens | 建立通用视觉语言理解、OCR、grounding、VQA、reasoning 能力 |
| Reasoner SFT | 同上 | $2.2$M Physical AI SFT samples，混入 filtered pretraining data，比例为 pretrain:SFT $=1:4$，另有 $800$K instruction data | supervised next-token prediction / cross entropy | importance-aware sampling，$8200$ iterations，global batch $512$ | 专门强化 robotics、AV、smart infrastructure、空间/时间/物理推理 |
| Generator initialization | MoT Generator | 不引入新数据 | 无独立 loss | 用 Reasoner 权重初始化 Generator；pre-training 时 reasoner tower frozen，只更新 generation-specific params | 把 Reasoner 的语义/世界知识迁移到生成模型 |
| Generator pre-training | Generator tower + generation projections | $767$M images、$347.7$M videos、$138.9$M usable audio-video clips | rectified flow matching masked MSE | T2I/T2V/I2V/V2V + audio-video 联合训练；多分辨率 $256p/480p/720p$；token packing $74$K | 学会 image/video/audio latent generation 和长视频时空建模 |
| Generator mid-training | Generator + action/audio/transfer heads | $15.6$M images、$74.7$M videos、$18.8$M curated audio clips、$8.4$M action episodes、transfer data | 多模态 rectified flow matching，action loss $\times 10$ | 保留 pretrain modes，同时引入 action、general transfer、driving transfer | 从通用生成器变成 Physical AI world model：能预测未来、反推动作、生成动作、按控制信号生成 |
| T2I post-training | Cosmos3-Super-Text2Image | high-quality image SFT：Stage 1 为 $45\%$ real + $40\%$ synthetic + $15\%$ text-rendering；Stage 2 为 $470$K ultra-HQ image-caption pairs | 沿用 image rectified flow SFT objective | Stage 1 $20$K steps，Stage 2 $2$K steps，只训 $>720p$ images，context $70$K | 强化文本到图像质量、prompt alignment、英文 text rendering |
| I2V post-training | Cosmos3-Super-Image2Video | filtered pretraining videos + targeted retrieved examples + $1000$ manually curated videos + $\sim 20$K synthetic clips，另混 $20\%$ T2I tokens | 沿用 video rectified flow SFT objective | 全部 video sequence 用 I2V formulation，目标 $480p$、$189$ frames、约 $8$s，$10$K iterations | 专门强化 image-to-video 的物理连续性、物体恒常性、运动合理性 |
| Robot policy post-training | Cosmos3-Nano-Policy-DROID | DROID：$76$K trajectories、$350$ hours、$86$ tasks、$564$ scenes | action/video rectified flow objective；action 相关模块更高 LR | 从 mid-trained Nano resume；新初始化 action encoder、action-decoding MLP、action tokens；预测 $32$ future actions + auxiliary RGB video | 把 world model 适配成闭环机器人 policy |

#### 1. Reasoner pre-training：先把“看懂世界”的模型训出来

论文说 Reasoner pre-training 从 language model、ViT encoder、multimodal projector 开始。Edge 使用内部预训练模型，Nano 使用 Qwen3-VL-8B，Super 使用 Qwen3-VL-32B。关键点是它没有单独先冻住 VLM 只训 projector，而是从一开始 joint training：

$$
\theta_{\text{Reasoner}}
=
\{\theta_{\text{LM}}, \theta_{\text{ViT}}, \theta_{\text{proj}}\}
$$

$$
\theta_{\text{Reasoner}}^{\star}
=
\arg\min_{\theta}
\mathcal{L}_{\text{AR}}
$$

数据方面，Reasoner curriculum 有 $24.2$M samples，其中 pre-training $22.0$M，SFT $2.2$M。pre-training 的模态表是：

| Modality | Pre-training |
| --- | ---: |
| Image-text | $18{,}814{,}952$ |
| Video-text | $1{,}016{,}299$ |
| Text only | $2{,}170{,}762$ |
| Total | $22{,}002{,}013$ |

数据构建过程是：

- 从 Nemotron Nano 2 data collection 选 $19.7$M samples，再补 $2.3$M samples 增强 math、video、spatial grounding、instruction-following。
- 先做 semantic deduplication。image/text 用 Qwen3-VL-Embedding-8B，video 用 PE-Core-G14-448，聚类后用 cosine similarity 去重，阈值为 $0.95$。
- 再做 AI-judge filtering。Gemma-4-31B-it 对 Faithfulness、Completeness、Correctness 三项打 $1$ 到 $5$ 分。
- pre-training 用较宽松阈值 $2$，保留约 $78\%$，避免过度损失多样性。

训练配置：

$$
T_{\max}=16\text{k tokens}
$$

$$
N_{\text{image tokens}} \le 2048,
\qquad
N_{\text{video tokens}} \le 8192
$$

优化器是 AdamW：

$$
\eta_{\text{LM/proj}} = 5 \times 10^{-5},
\qquad
\eta_{\text{ViT}} = 5 \times 10^{-6}
$$

$$
(\beta_1,\beta_2)=(0.9,0.999),
\qquad
\lambda_{\text{wd}}=0.05,
\qquad
\|\nabla\|_2 \le 1.0
$$

目的不是直接生成，而是把图像、视频、文本、空间关系、物理关系对齐到一个能做自回归推理的 backbone 中。

#### 2. Reasoner SFT：把通用 VLM 转成 Physical AI Reasoner

SFT 阶段仍然是 supervised next-token prediction：

$$
\mathcal{L}_{\text{SFT}}
=
-\sum_{t=1}^{T}
\log p_{\theta}(y_t \mid y_{<t}, x_{\text{media}}, q)
$$

不同点是数据从通用 image-text 为主，转向 Physical AI。SFT 的模态表是：

| Modality | Supervised fine-tuning |
| --- | ---: |
| Image-text | $1{,}051{,}513$ |
| Video-text | $1{,}079{,}200$ |
| Text only | $40{,}960$ |
| Total | $2{,}171{,}673$ |

主要数据块：

- general spatial understanding：2D/3D grounding、real-world spatial QA、simulator-grounded embodied spatial reasoning。
- general temporal understanding：dense temporal captions、$55$K videos / $2.6$K hours / $743$K event triplets、FoundationMotion QA、camera motion、physical plausibility judgment。
- autonomous vehicle：$10$K+ human-labeled driving videos、$\sim 1.1$M auto-labeled decision-rich videos、Nexar $24$K videos、MADS 3D vehicle grounding。
- robotics：robot action CoT、MimicGen $3.6$K Omniverse-rerendered videos、BEHAVIOR-1K $83$K samples、ERQA、robotic surgery VQA $398$K conversations over $2.2$M images。
- smart infrastructure：warehouse spatial intelligence、dense pedestrian localization、traffic/anomaly reasoning。

训练时混入 filtered high-quality pre-training data：

$$
\text{budget}_{\text{pretrain}} : \text{budget}_{\text{SFT}}
=
1 : 4
$$

优化器配置：

$$
\eta_{\text{LM/proj}} = 1 \times 10^{-5},
\qquad
\eta_{\text{ViT}} = 1 \times 10^{-6}
$$

$$
(\beta_1,\beta_2)=(0.9,0.95),
\qquad
\lambda_{\text{wd}}=0.1,
\qquad
\|\nabla\|_2 \le 1.0
$$

这个阶段的目的，是把 Reasoner 从“通用多模态模型”变成“Physical AI 场景下能理解空间、时间、动作、物理合理性和任务意图的模型”。

#### 3. Generator pre-training：在 Reasoner 初始化上学习生成

Generator 不是重新随机初始化的大扩散模型。论文明确说：

$$
\theta_{\text{Generator}}^{(0)}
\leftarrow
\theta_{\text{Reasoner}}^{\star}
$$

因为 MoT 的 reasoner/generator 两个 tower 都是 transformer decoder layer 形态，所以可以用 Reasoner 权重初始化 Generator，把语义和世界知识迁移过去。pre-training 时：

$$
\theta_{\text{Reasoner tower}}
\text{ frozen}
$$

$$
\theta_{\text{generation-specific}}
\text{ updated}
$$

Generator 的 clean latent 是 $x_0$，可以来自 image/video VAE、audio VAE 或 action token。训练时采样噪声 $\epsilon$ 和 noise level $\sigma$，构造：

$$
x_{\sigma}
=
\sigma \epsilon + (1-\sigma)x_0
$$

模型预测 velocity：

$$
\hat{v}
=
v_{\theta}(x_{\sigma},\sigma,c)
$$

监督目标是：

$$
v^{\star}
=
\epsilon-x_0
$$

带 condition mask 的 loss 是：

$$
\mathcal{L}_{m}
=
\operatorname{MSE}
\left(
(1-M_m)\odot \hat{v}_m,
(1-M_m)\odot v_m^{\star}
\right)
$$

其中 $m$ 表示 modality，$M_m=1$ 的 token 是 clean condition，不加噪也不算 loss。

pre-training 数据：

- image/video：从 $7.8$B raw images 和 $3$B raw source videos 处理过滤后得到 $767$M images 和 $347.7$M video clips。
- audio：来自 pre-training video pool，其中 $138.9$M clips 有 usable audio tracks，$62.5$M 短于 $30$s 的 clips 用 Qwen3-Omni-Captioner 生成 audio descriptions。

pre-training generation modes：

| Mode | 比例 | 条件设置 |
| --- | ---: | --- |
| T2I | $20\%$ | image 作为 $T=1$ 的特殊 video |
| T2V | $56\%$ | $T_{\text{cond}}=0$，全视频 noised |
| I2V | $16\%$ | $T_{\text{cond}}=1$，首个 latent frame clean |
| V2V | $8\%$ | $T_{\text{cond}}=2$，约等于前 $5$ 个 RGB frames clean |

多分辨率训练：

| Resolution | FPS | Frames |
| --- | --- | --- |
| $256p$ | $10$--$30$ | $5$--$400$ |
| $480p$ | $10$--$30$ | $5$--$400$ |
| $720p$ | $10$--$30$ | $5$--$300$ |

resolution-adaptive shift：

$$
s_{256p}=1,
\qquad
s_{480p}=3,
\qquad
s_{720p}=5
$$

shift reparameterization：

$$
\bar{t}=1-t
$$

$$
\sigma
=
\frac{s\bar{t}}{1+(s-1)\bar{t}}
$$

优化：

$$
\eta=10^{-4},
\qquad
(\beta_1,\beta_2)=(0.9,0.99),
\qquad
\lambda_{\text{wd}}=0.05,
\qquad
\|\nabla\|_2 \le 1.0
$$

classifier-free guidance 通过 text dropout 实现：

$$
p_{\text{text-dropout}}=0.1
$$

训练 token 量：

| Model | Generator pre-training tokens | GPUs |
| --- | ---: | ---: |
| Cosmos3-Nano | $31.05$T | $1024$ GB200 |
| Cosmos3-Super | $17.86$T | $2048$ GB200 |

#### 4. Generator mid-training：引入动作、控制和 Physical AI domain

mid-training 的核心是继续从 pre-trained Generator 出发，把模型从 image/video/audio generator 扩展成 omnimodal world model。

论文给了两个目标：

$$
\text{domain specialization}
$$

$$
\text{multimodal integration}
$$

数据变成高质量、Physical AI、control/action oriented：

- image：$15.6$M mid-training pool，包含 high-quality real、synthetic、text-rendering，比例约为 $60\%/36\%/4\%$。
- video：$74.7$M curated clips，覆盖 robotics、driving、human activity、physics、synthetic simulation。
- audio：$18.8$M curated clips，其中 $12.8$M non-speech，$6$M speech-synchronized。
- action：$8.4$M episodes，$61.3$K hours，覆盖 egocentric motion、robotics、autonomous vehicles、camera motion。
- transfer：$3$M high-quality videos 做 edge/blur/depth/segmentation control；driving transfer 使用 MADS world-scenario maps，MADS 有 $1.1$M samples。

mid-training data mixture：

| Training stream | Modes / conditioning | Share |
| --- | --- | ---: |
| Image | T2I | $10\%$ |
| Video | T2V, I2V, V2V | $32\%$ |
| Video + Audio | T2(V+Audio), I2(V+Audio), V2(V+Audio) | $8\%$ |
| Action | forward dynamics, inverse dynamics, policy | $25\%$ |
| General Transfer | edge, blur, depth, segmentation controls | $20\%$ |
| Driving Transfer | world-scenario-map controls | $5\%$ |

Action 训练有三种任务：

| Action mode | 条件 | 预测目标 | 目的 |
| --- | --- | --- | --- |
| Forward dynamics | first frame + all actions | future video | 学 $p(x_{t+1:t+H}\mid x_t,a_{t:t+H})$ |
| Inverse dynamics | observed video frames | actions | 学 $p(a_{t:t+H}\mid x_{t:t+H})$ |
| Policy | first frame / observation | actions + future video | 学可执行动作和未来结果 |

源码里的 `build_sequence_plan_from_mode` 对这三种模式的 condition mask 做了对应区分：forward dynamics 把 action steps 都设成 clean conditioning；inverse dynamics 把 video frames 设成 observed context；policy 则让 action 被 supervised/predicted。

mid-training loss 是各模态 velocity MSE 的加权和：

$$
\mathcal{L}_{\text{mid}}
=
\sum_{m \in \{\text{vision},\text{audio},\text{action}\}}
\lambda_m \mathcal{L}_m
$$

其中 action loss 额外放大：

$$
\lambda_{\text{action}}=10
$$

论文解释原因是 normalized action vectors 的 per-element MSE 较小，因此需要补偿。mid-training 的 shift 也提高：

$$
s_{256p}=3,
\qquad
s_{480p}=5,
\qquad
s_{720p}=10
$$

训练 token 量：

| Model | Generator mid-training tokens | GPUs |
| --- | ---: | ---: |
| Cosmos3-Nano | $2.4$T | $1024$ GB200 |
| Cosmos3-Super | $1.9$T | $2048$ GB200 |

mid-training 结束后得到 base open models：

$$
\text{Cosmos3-Nano}
$$

$$
\text{Cosmos3-Super}
$$

#### 5. T2I post-training：把 Super 专门调成高质量文生图

T2I post-training 从 Cosmos3-Super 出发，得到 Cosmos3-Super-Text2Image。论文说这是 two-stage SFT：

Stage 1：

$$
N_{\text{steps}}=20{,}000
$$

$$
p_{\text{real}}=45\%,
\qquad
p_{\text{synthetic}}=40\%,
\qquad
p_{\text{text-rendering}}=15\%
$$

$$
\eta=10^{-4},
\qquad
N_{\text{warmup}}=2000
$$

Stage 2：

$$
N_{\text{steps}}=2000
$$

$$
N_{\text{ultra-HQ image-caption}}=470{,}000
$$

两个阶段都只训高分辨率图像：

$$
\text{resolution} > 720p,
\qquad
T_{\text{context}}=70\text{k tokens}
$$

论文没有为 T2I post-training 定义新的 loss，因此按上下文它沿用 Generator 的 image rectified flow SFT objective。目的很明确：把通用 world model 的 physical grounding 迁移到高质量 image generation 上，尤其是 scene-level alignment、prompt following 和 text rendering。

#### 6. I2V post-training：把 Super 专门调成图生视频

I2V post-training 从 Cosmos3-Super 出发，得到 Cosmos3-Super-Image2Video。训练数据是：

- filtered pre-training data，经过 topic diversity refinement。
- agentic workflow 找模型弱点，再从 pre-training set 检索 targeted examples。
- $1000$ high-quality manually curated videos。
- $\sim 20$K synthetic video clips，占总 token 约 $6\%$。
- 额外混入 $20\%$ T2I image tokens，保持 semantic alignment。

训练 formulation 是全部 video sequence 都改成 I2V：

$$
T_{\text{cond}}=1
$$

$$
x_{0,1}
\text{ clean},
\qquad
x_{0,2:T}
\text{ noised}
$$

目标设置：

$$
\text{resolution}=480p
$$

$$
N_{\text{frames}}=189
$$

$$
\text{duration}\approx 8\text{s at }24\text{FPS}
$$

训练 schedule：

$$
N_{\text{iter}}=10{,}000,
\qquad
\eta=10^{-5},
\qquad
N_{\text{tokens}}\approx 50\text{B}
$$

目的不是新增架构能力，而是让已有 Generator 在 I2V 分布上更稳定：首帧一致性、物体恒常性、几何延续、运动合理性和物理 plausibility。

#### 7. Robot policy post-training：把 Nano 调成闭环机器人策略

Robot policy post-training 从 mid-trained Cosmos3-Nano 出发，得到 Cosmos3-Nano-Policy-DROID。数据是 DROID：

$$
N_{\text{trajectories}}=76{,}000
$$

$$
T_{\text{interaction}}=350\text{ hours}
$$

$$
N_{\text{tasks}}=86,
\qquad
N_{\text{scenes}}=564
$$

数据处理：

- 输入分辨率为 $360 \times 640$。
- 使用 idle-frame filtering 和 failure-demonstration removal。
- 训练时使用 random image augmentation。
- 三视角 observation 被拼成 $540 \times 640$ canvas。

模型改动不是换 backbone，而是新初始化 action 相关模块：

$$
\theta_{\text{action encoder}},
\theta_{\text{action decoding MLP}},
\theta_{\text{action tokens}}
\sim
\text{fresh init}
$$

action 相关参数使用更高学习率：

$$
\eta_{\text{action params}}
=
5\eta_{\text{base}}
$$

整体学习率：

$$
\eta=2\times10^{-4}
$$

训练目标：

$$
\hat{a}_{t:t+31}
=
f_{\theta}(o_t, q)
$$

其中 $o_t$ 包含当前 proprioceptive state 和三视角视觉 observation，$q$ 是 DROID short task instruction。模型同时预测 auxiliary RGB video frames：

$$
(\hat{a}_{t:t+31}, \hat{x}_{t:t+31})
=
f_{\theta}(o_t,q)
$$

控制频率：

$$
f_{\text{control}}=15\text{Hz}
$$

论文没有给 policy 单独定义新 loss，而是说其他 hyperparameters follow mid-training setup。因此更准确的解读是：policy post-training 沿用 action/video rectified flow training 框架，只是数据、输入组织、action head、action LR multiplier 和预测 horizon 变成 DROID policy setting。

#### 8. 源码里 loss 和 mask 是怎么对应论文的？

`compute_flow_matching_loss` 直接实现了论文中的 masked velocity MSE：

$$
\text{sqerr}_i
=
(\hat{v}_i-v_i^{\star})^2
$$

$$
\text{noisy\_mask}_i
=
1-\text{condition\_mask}_i
$$

$$
\mathcal{L}_i
=
\operatorname{mean}
\left(
\text{sqerr}_i
\odot
\text{noisy\_mask}_i
\right)
$$

action padding 也会被处理：

$$
\text{sqerr}_i
\leftarrow
\text{sqerr}_i[:, :d_i^{\text{raw action}}]
$$

所以 padded action channels 不参与 loss。

`_add_noise_to_input` 里对 vision/action/sound 都做同一件事：先生成 $\epsilon$，再通过 condition mask 把 clean conditioning token 的有效 $\sigma$ 置零：

$$
\sigma_{\text{eff}}
=
\sigma \odot (1-M)
$$

当 $M=1$ 时：

$$
\sigma_{\text{eff}}=0,
\qquad
x_{\sigma}=x_0
$$

当 $M=0$ 时：

$$
x_{\sigma}
=
\sigma\epsilon+(1-\sigma)x_0
$$

这解释了为什么 I2V/V2V/forward dynamics 里的条件帧或条件动作不会被模型“重建监督”，它们只是作为 context 参与注意力和条件输入。

#### 原文依据

- `source/src/sections/4__training.tex:4`：总训练流程，两大阶段：先 Reasoner，再用 Reasoner 初始化 Generator，并做 pre/mid/post-training。
- `source/src/sections/4__training.tex:13`：Reasoner 初始化来源，以及不做 projector-only alignment、从开始 joint training。
- `source/src/sections/4__training.tex:15`：Reasoner pre-training 的 next-token prediction、$2$ epochs、$16$k context、image/video token limits。
- `source/src/sections/4__training.tex:17`：square-root normalized per-token loss weighting。
- `source/src/sections/4__training.tex:20`：Reasoner pre-training optimizer 超参。
- `source/src/sections/4__training.tex:24`：Reasoner SFT 的 importance-aware sampling。
- `source/src/sections/4__training.tex:26`：SFT 中 pretraining:SFT $=1:4$，以及 $800$K instruction-following data。
- `source/src/sections/4__training.tex:28`：Reasoner SFT iterations、batch size、optimizer 超参。
- `source/src/sections/4__training.tex:36`：Generator rectified flow matching objective、$x_{\sigma}$、$v^{\star}$、masked MSE。
- `source/src/sections/4__training.tex:38`：noise sampling 和 shift reparameterization。
- `source/src/sections/4__training.tex:42`：Generator pre-training 的 T2I、Text-to-(Video+Audio)、Image-to-(Video+Audio)、Video-to-(Video+Audio)。
- `source/src/sections/4__training.tex:45`：多分辨率训练、resolution stream、batch composition。
- `source/src/sections/4__training.tex:54`：T2I/T2V/I2V/V2V 比例和条件帧设置。
- `source/src/sections/4__training.tex:68`：pre-training 只更新 generation-specific parameters，reasoner tower frozen，text dropout $10\%$。
- `source/src/sections/4__training.tex:70`：Generator pre-training tokens 和 GPU 规模。
- `source/src/sections/4__training.tex:74`：mid-training 的目标：domain specialization 和 multimodal integration。
- `source/src/sections/4__training.tex:77`：mid-training image/video 数据规模。
- `source/src/sections/4__training.tex:83`：action training 的 forward dynamics、inverse dynamics、policy 目标。
- `source/src/sections/4__training.tex:86`：video transfer control signals。
- `source/src/sections/4__training.tex:95`：mid-training loss、per-modality velocity MSE、action loss $\times 10$。
- `source/src/sections/4__training.tex:100`：mid-training tokens 和 GPU 规模。
- `source/src/sections/4__training.tex:111`：T2I post-training Stage 1 数据比例和 schedule。
- `source/src/sections/4__training.tex:113`：T2I post-training Stage 2 的 $470$K ultra-HQ image-caption pairs。
- `source/src/sections/4__training.tex:127`：I2V post-training 数据 mixture。
- `source/src/sections/4__training.tex:129`：I2V 的 $480p$、$189$ frames、约 $8$s 设置。
- `source/src/sections/4__training.tex:131`：I2V 的 $10$K iterations、$\eta=10^{-5}$、约 $50$B tokens。
- `source/src/sections/4__training.tex:142`：DROID 数据规模。
- `source/src/sections/4__training.tex:145`：Policy-DROID 的 action modules、$5\times$ LR multiplier、三视角输入、$32$ future actions、$15$Hz。
- `source/src/sections/data/reasoner.tex:4`：Reasoner 数据总量和 pretraining/SFT 划分。
- `source/src/sections/data/reasoner.tex:12`：Reasoner pretraining 数据来源。
- `source/src/sections/data/reasoner.tex:16`：semantic deduplication embedding。
- `source/src/sections/data/reasoner.tex:21`：Gemma-4-31B-it AI judge。
- `source/src/sections/data/reasoner.tex:36`：AI-judge threshold 和 retention。
- `source/src/sections/data/reasoner.tex:38`：Reasoner pretraining category composition。
- `source/src/sections/data/image_and_video.tex:7`：image/video pretraining 数据规模。
- `source/src/sections/data/image_and_video.tex:22`：mid-training image/video 数据组成。
- `source/src/sections/data/image_and_video.tex:26`：transfer data 和 MADS 数据。
- `source/src/sections/data/audio.tex:7`：audio pre-training 数据规模。
- `source/src/sections/data/audio.tex:10`：mid-training audio pool。
- `source/src/sections/data/action.tex:4`：引入 text-video-action 的原因。
- `source/src/sections/data/action.tex:6`：action mid-training 数据规模。
- `source/src/tables/training/midtraining_modality_mix.tex:10`：mid-training image share。
- `source/src/tables/training/midtraining_modality_mix.tex:11`：mid-training video share。
- `source/src/tables/training/midtraining_modality_mix.tex:12`：mid-training video+audio share。
- `source/src/tables/training/midtraining_modality_mix.tex:13`：mid-training action share。
- `source/src/tables/training/midtraining_modality_mix.tex:14`：mid-training general transfer share。
- `source/src/tables/training/midtraining_modality_mix.tex:15`：mid-training driving transfer share。
- `source/src/figures/data/data_curriculum.tex:4`：data curriculum 图说明。
- `source/src/figures/data/data_curriculum.tex:8`：action 和 transfer 在 mid-training 才引入。
- `source/src/figures/data/data_curriculum.tex:9`：post-training 得到 T2I/I2V/Policy-DROID，且与对应 mid-trained model 架构相同。

#### 源码依据

- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/algorithm/loss/flow_matching.py:17`：`compute_flow_matching_loss` 入口。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/algorithm/loss/flow_matching.py:34`：target velocity 是 $v=\epsilon-x_0$。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/algorithm/loss/flow_matching.py:35`：`condition_mask` 中 $1$ 表示 clean/conditioning，$0$ 表示 noisy/generation。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/algorithm/loss/flow_matching.py:73`：计算 squared error。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/algorithm/loss/flow_matching.py:74`：`noisy_mask_i = 1.0 - condition_mask[i]`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/algorithm/loss/flow_matching.py:75`：action raw dim mask，padding channel 不算 loss。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/algorithm/loss/flow_matching.py:81`：masked MSE。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:1320`：`_add_noise_to_input` 对 clean latent 加噪。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:1338`：conditioning latent frames 的 $\sigma$ 被乘以 $(1-\text{condition\_mask})$。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:1401`：vision 调用 `rectified_flow.get_interpolation` 得到 $x_{\sigma}$ 和 $v_t$。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:1454`：action 调用 `rectified_flow_action.get_interpolation`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:1492`：sound 调用 `rectified_flow_sound.get_interpolation`。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/transforms.py:253`：action training modes 定义。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/transforms.py:294`：不同 mode 下 vision conditioning frame indexes。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/transforms.py:305`：不同 mode 下 action conditioning indexes。

---

### Q7. 数据集是怎么构建的？

#### 总体思路

Cosmos 3 的数据集不是一个单一 corpus，而是两条互补数据管线：

$$
\mathcal{D}_{\text{Cosmos3}}
=
\mathcal{D}_{\text{Reasoner}}
\cup
\mathcal{D}_{\text{Generator}}
$$

Reasoner 数据面向理解和推理，因此核心是 image-text、video-text、text-only 的监督样本：

$$
(x_{\text{image/video/text}}, q, y)
$$

Generator 数据面向生成、模拟和行动，因此核心是 image/video/audio/action 的 latent reconstruction / flow-matching 样本：

$$
(x_0^{\text{vision}}, x_0^{\text{audio}}, x_0^{\text{action}}, c)
$$

其中 $c$ 是 text prompt、clean conditioning frames、control maps 或 action context。论文明确说 Reasoner 和 Generator 虽然共享 transformer/token 表示，但数据类型和训练目标不同。

#### 1. Reasoner 数据：从多模态 QA/grounding/caption 样本构建

Reasoner 数据总量约：

$$
|\mathcal{D}_{\text{Reasoner}}|
\approx
24.2\text{M}
$$

分为：

$$
|\mathcal{D}_{\text{pretrain}}|=22.0\text{M},
\qquad
|\mathcal{D}_{\text{SFT}}|=2.2\text{M}
$$

模态分布：

| Modality | Pre-training | SFT |
| --- | ---: | ---: |
| Image-text | $18{,}814{,}952$ | $1{,}051{,}513$ |
| Video-text | $1{,}016{,}299$ | $1{,}079{,}200$ |
| Text only | $2{,}170{,}762$ | $40{,}960$ |
| Total | $22{,}002{,}013$ | $2{,}171{,}673$ |

Reasoner pre-training 和 SFT 的类别分布图如下：

![Reasoner pretraining category mix](reasoner_pretraining_category_mix.png)

![Reasoner SFT category mix](reasoner_sft_category_mix.png)

Reasoner pre-training 数据构建流程：

1. 从 Nemotron Nano 2 data collection 子选 $19.7$M samples。
2. 额外补充 $2.3$M samples，用于增强 math、video、spatial grounding、instruction-following。
3. 做 semantic deduplication。
4. 做 AI-judge quality filtering。
5. 按 capability category 形成最终训练 mixture。

去重阶段把一个完整 conversation 视为一个训练样本：

$$
s_i
=
(\text{media}_i, \text{instruction}_i, \text{response}_i)
$$

对样本计算联合 embedding：

$$
e_i
=
\operatorname{concat}
\left(
f_{\text{media}}(\text{media}_i),
f_{\text{text}}(\text{instruction}_i,\text{response}_i)
\right)
$$

然后在聚类内用 cosine similarity 删除近重复：

$$
\operatorname{sim}(e_i,e_j)
=
\frac{e_i^\top e_j}{\|e_i\|_2\|e_j\|_2}
>
0.95
$$

则视为 near-duplicate。image-text 和 text-only 使用 Qwen3-VL-Embedding-8B；video-text 使用 PE-Core-G14-448。

AI judge 阶段用 Gemma-4-31B-it 对每个样本打三类分：

$$
r_i
=
\left(
r_i^{\text{Faithfulness}},
r_i^{\text{Completeness}},
r_i^{\text{Correctness}}
\right),
\qquad
r_i^k \in \{1,2,3,4,5\}
$$

保留规则是：

$$
\min_k r_i^k \ge \tau
$$

其中 pre-training 用较低阈值：

$$
\tau_{\text{pretrain}}=2
$$

SFT 用严格阈值：

$$
\tau_{\text{SFT}}=5
$$

论文报告 multimodal dedup 删除 $4.23\%$，AI judge 在阈值 $2$ 和 $5$ 下分别保留 $78\%$ 和 $46\%$。这里的设计逻辑是：pre-training 更重覆盖度和多样性，SFT 更重精确监督。

Reasoner SFT 数据构建则进一步偏向 Physical AI，主要包括：

- general spatial understanding：2D/3D grounding、real-world spatial QA、simulator-grounded embodied spatial reasoning。
- general temporal understanding：dense temporal caption、event localization、FoundationMotion QA、camera motion、physical plausibility judgment。
- autonomous vehicle：human-labeled driving CoT、auto-labeled decision-rich videos、Nexar temporal events、MADS 3D vehicle grounding。
- robotics：robot action CoT、MimicGen、BEHAVIOR-1K、ERQA、robotic surgery VQA。
- smart infrastructure：warehouse spatial intelligence、dense pedestrian localization、traffic/anomaly reasoning。

#### 2. Generator 图像/视频数据：从 raw media 到训练 shard

Generator 的 image/video 数据构建管线更像大规模媒体清洗系统。论文把它分成五步：

1. raw data collection and preprocessing。
2. embedding and deduplication。
3. categorization and basic filtering。
4. annotation。
5. 按 resolution 和 duration grouping 成 training-ready shards。

可以写成：

$$
\mathcal{D}_{\text{raw}}
\xrightarrow{\text{preprocess}}
\mathcal{D}_{\text{clip}}
\xrightarrow{\text{embed+dedup}}
\mathcal{D}_{\text{unique}}
\xrightarrow{\text{filter}}
\mathcal{D}_{\text{clean}}
\xrightarrow{\text{caption}}
\mathcal{D}_{\text{annotated}}
\xrightarrow{\text{shard}}
\mathcal{D}_{\text{train}}
$$

规模：

$$
7.8\text{B raw images}
\rightarrow
767\text{M images}
$$

$$
3\text{B raw source videos}
\rightarrow
347.7\text{M video clips}
$$

视频预处理包括：

- 用 TransNetV2 做 scene-change detection，把长视频切成时间一致的 clips。
- 用 `ffmpeg cropdetect` 去黑边。
- 重新编码到 canonical format，保证存储和播放一致。

去重和分布建模：

- image embedding 使用 Qwen3-VL-Embedding-8B。
- video embedding 使用 nvidia/Cosmos-Embed1-448p。
- 采样 $147$M images 和 $400$M videos 分别做 cuML KMeans。
- image/video 各自使用 $20{,}000$ clusters。
- 在每个 cluster 内按 cosine similarity 去 near duplicates。

过滤逻辑：

- 用内部 VLM 模型打 semantic tags 和 quality tags。
- image/video 被分到 $47$ 个层级类别，包含 General 和 Physical AI domains。
- image 过滤 collage、watermark、white background、NSFW，并按 aesthetic score / photorealism score 筛选。
- video 过滤 split-screen、rotated video、static video 等 major artifacts。
- video 同时记录 DOVER aesthetic、DOVER technical、VTSS training suitability 三个 $0$ 到 $9$ 连续分，以及约 $100$ 个 artifact tags。

结构化 caption 是 Generator 数据构建的关键。论文认为普通自由文本 caption 往往“准确但不完整”，所以所有训练阶段都改用 structured JSON caption：

$$
c
=
\{
\text{subjects},
\text{background},
\text{lighting},
\text{aesthetics},
\text{cinematography},
\text{temporal dynamics},
\text{actions},
\text{state changes},
\ldots
\}
$$

他们 fine-tune 了两个 Qwen3-VL-8B captioner，分别服务 image 和 video。caption 质量用 assertion-level precision/recall 评估：

$$
\text{Precision}
=
\frac{|\text{supported claims}|}{|\text{generated claims}|}
$$

$$
\text{Recall}
=
\frac{|\text{covered ground-truth assertions}|}{|\text{ground-truth assertions}|}
$$

这个设计直接服务生成训练：让 prompt 覆盖主体、空间关系、动作、物理变化和镜头语言，而不是只给一个短 caption。

#### 3. mid-training 图像/视频数据：从大池子筛成高质量 Physical AI mixture

mid-training 的 image/video 数据不再追求最大规模，而是构建更高质量、更贴近 Physical AI 的 mixture：

$$
\mathcal{D}_{\text{mid}}
=
\mathcal{D}_{\text{HQ real}}
\cup
\mathcal{D}_{\text{synthetic}}
\cup
\mathcal{D}_{\text{text-rendering}}
\cup
\mathcal{D}_{\text{transfer}}
$$

image mid-training pool：

$$
|\mathcal{D}_{\text{image-mid}}|=15.6\text{M}
$$

比例约为：

$$
p_{\text{real}}=60\%,
\qquad
p_{\text{synthetic}}=36\%,
\qquad
p_{\text{text-rendering}}=4\%
$$

video mid-training pool：

$$
|\mathcal{D}_{\text{video-mid}}|=74.7\text{M}
$$

其中：

$$
p_{\text{filtered pretrain video}}=46.0\%
$$

$$
p_{\text{domain-specific video}}=43.9\%
$$

$$
p_{\text{capability-oriented hard cases}}=10.1\%
$$

synthetic 数据用来补长尾 Physical AI 场景，包含：

- SDG-PhyxSim：刚体碰撞、 articulated object dynamics、deformable materials、fluid dynamics、optical effects。
- SDG-RobotSim：$6$--$8$ 种机器人 embodiment 的 manipulation 和 locomotion。
- SDG-DriveSim：常规和 corner-case driving scenarios。
- SDG-SynHuman：human dynamics、camera motion priors、多角色交互。
- SDG-Warehouse：warehouse safety、人和叉车交互。

这部分的目标是修补 web-scale 数据的长尾不足：

$$
p_{\text{web}}(\text{rare physical interaction})
\ll
p_{\text{target}}(\text{Physical AI})
$$

因此通过 synthetic data 提高目标场景覆盖度。

#### 4. video transfer 数据：构建“控制信号到 RGB”的数据

transfer 数据用于让模型学会 control-conditioned generation：

$$
(\text{control}, c)
\rightarrow
\text{RGB image/video}
$$

控制信号包括：

$$
\text{edge},
\text{blur},
\text{depth},
\text{segmentation},
\text{world-scenario map}
$$

构建方式：

- 从 pre-training video pool 选 $3$M high-quality videos，重点是 robotics 和 autonomous driving。
- edge/blur 在训练时 on-the-fly 生成。
- depth 用 Video Depth Anything 预计算。
- segmentation 用 SAMv2 预计算。
- driving world-scenario map 使用 Cosmos-Drive-Dreams 的 MADS 数据。

MADS 规模：

$$
|\mathcal{D}_{\text{MADS}}|=1.1\text{M samples}
$$

每个样本有 $7$ 个同步相机：

$$
\{\text{front-wide}, \text{front-tele}, \text{cross-left}, \text{cross-right}, \text{rear-left}, \text{rear-right}, \text{rear-tele}\}
$$

world-scenario map 编码 lane lines、road boundaries、traffic lights、vehicle/pedestrian 3D boxes。

源码里开源实现对应了这些 transfer control augmentors：

- Canny edge：`cv2.Canny` 生成 edge maps。
- blur：Gaussian / bilateral 等 blur augmentation。
- depth：把 `data_dict["depth"]` resize 到 video shape 后作为 `control_input_depth`。
- segmentation：读取 segmentation masks / RLE，采样 mask，转成 colored segmentation mask。

也就是说，论文里的 transfer data 不只是离线文件；训练 loader 里还可以动态构造部分 control input。

#### 5. audio 数据：从 raw video audio 到因果对齐音频

audio pre-training 数据来自 pre-training video pool：

$$
|\mathcal{D}_{\text{audio-pre}}|=138.9\text{M clips}
$$

这些 clips 包含 diegetic/non-diegetic speech、voiceover、BGM、ambient sound、music、physical events。对短于 $30$s 的 $62.5$M clips，用 Qwen3-Omni-Captioner 生成 synthetic audio descriptions。

mid-training audio 则更重视 audio-video causal alignment：

$$
|\mathcal{D}_{\text{audio-mid}}|=18.8\text{M clips}
$$

拆成：

$$
|\mathcal{D}_{\text{non-speech}}|=12.8\text{M}
$$

$$
|\mathcal{D}_{\text{speech-synchronized}}|=6\text{M}
$$

构建原则是：

$$
\text{keep speech}
\iff
\text{speech synchronized with visible face}
$$

$$
\text{remove off-screen speech from non-speech examples}
$$

$$
\text{remove non-instrumental BGM if it dominates target audio}
$$

具体流程：

1. SAM-Audio 做 source separation，分离 speech stem 和 remaining stem。
2. SyncNet 对 speech stem 和 video 做 lip-sync scoring。
3. 定义：

$$
\text{speech\_synced}
=
(\text{has\_face}=\text{True})
\land
(\text{lip\_sync\_confidence}\ge 3.0)
$$

4. FireRedASR2S 估计：

$$
\text{speech\_ratio},
\qquad
\text{music\_ratio}
$$

5. 定义：

$$
\text{high\_music}
=
(\text{music\_ratio}\ge 0.1)
$$

6. Qwen3-VL 判断 high-music clip 是否是可见乐器演奏：

$$
\text{is\_music\_instrument}
$$

7. speech branch 保留 lip-synced speech，并在需要时移除非乐器 BGM。
8. non-speech branch 移除 off-screen speech / vocals，并过滤 near-silent 音频。
9. 如果音频被 source separation 或 music removal 改过，则重新 caption，避免 caption 描述已经被删除的声音。

非静音过滤条件包括：

$$
\text{max\_abs}\ge 0.007,
\qquad
\text{p50\_db}\ge -80,
\qquad
\text{active\_ratio}\ge 0.2
$$

这解释了为什么 Cosmos 3 的音频不是“随便拿视频原声”：原始 web audio 里 narration、voiceover、BGM 往往不是画面事件导致的声音，会污染视频到声音的因果学习。

#### 6. action 数据：把不同 embodiment 的动作统一成可训练 token

Action 数据只在 mid-training 引入，因为它的作用是给 Generator 一个“可控干预变量”：

$$
x_{t+1}
\sim
p(x_{t+1}\mid x_t,a_t)
$$

论文构建了四类 action 数据：

![Action data distribution](action_data_distribution.png)

总规模：

$$
|\mathcal{D}_{\text{action}}|=8.4\text{M episodes}
$$

$$
T_{\text{action}}=61.3\text{K hours}
$$

四类来源：

| Pillar | Hours | Share | 构建方式 |
| --- | ---: | ---: | --- |
| Egocentric motion | $41.3$K | $67.4\%$ | proprietary bimanual hand manipulation，head-mounted RGB，每帧同步 head-camera pose 和双手 $21$ keypoint 3D pose |
| Autonomous vehicle | $10.0$K | $16.3\%$ | NVIDIA Hyperion driving logs，按目标 driving scenario distribution 挖掘，并把轨迹转到 front-wide camera coordinate frame |
| Robotics | $5.4$K | $8.7\%$ | 聚合 open-source robotics datasets，$90.4$K tasks、$516.7$K episodes，用 state difference 构造 pseudo-actions |
| Camera motion | $4.6$K | $7.5\%$ | 从 pre-training videos 挖掘，用 ViPE 和 DepthAnything3 估计 camera poses，过滤 jitter/异常 intrinsics |

统一处理流程：

$$
a_{\text{raw}}^{(d)}
\xrightarrow{\text{unified action tokenization}}
a^{(d)}
\xrightarrow{\text{normalization}}
\tilde{a}^{(d)} \in [-1,1]
$$

其中 $d$ 表示不同 domain/embodiment。对不同来源计算 per-dimension normalizers，让 action channel 数值落在近似统一范围：

$$
\tilde{a}_{k}
=
\frac{a_k-\mu_k}{s_k}
$$

多视角数据会拼成一个 canvas，并把视角布局写入 structured JSON prompt。论文图中 DROID 多视角格式是：上方 wrist camera，下方左右两个 third-person views。

![DROID multiview packaging](source/src/figures/data/action/multiview_droid_16164052.jpg)

源码里的 DROID wrapper 也对应这个构建思路：

- `DROIDLeRobotDataset` 默认 `fps=15.0`。
- `chunk_length=16`。
- 支持 `concat_view`。
- action layout 是 $10$D：

$$
a
=
[\Delta p_{1:3}, \Delta R_{\text{6D}}, g]
\in
\mathbb{R}^{10}
$$

其中 $g$ 是 gripper。训练时还会随机选择 action mode：

$$
\text{mode}
\in
\{\text{forward dynamics}, \text{inverse dynamics}, \text{policy}\}
$$

#### 7. post-training 数据：小而精，用来修补具体能力

post-training 数据不是继续加大 web-scale corpus，而是面向专家模型构建 targeted SFT sets。

T2I post-training：

$$
\mathcal{D}_{\text{T2I-post}}
=
\mathcal{D}_{\text{synthetic image}}
\cup
\mathcal{D}_{\text{text-rendering image}}
\cup
\mathcal{D}_{\text{high-quality real image}}
$$

论文明确说 general web-scale pre-training data 被排除，目的是直接针对高保真内容和能力缺口。Stage 1 的比例是：

$$
p_{\text{real}}=45\%,
\qquad
p_{\text{synthetic}}=40\%,
\qquad
p_{\text{text-rendering}}=15\%
$$

Stage 2 使用：

$$
470\text{K ultra-high-quality image-caption pairs}
$$

I2V post-training：

$$
\mathcal{D}_{\text{I2V-post}}
=
\mathcal{D}_{\text{filtered pretrain video}}
\cup
\mathcal{D}_{\text{manual curated}}
\cup
\mathcal{D}_{\text{synthetic video}}
\cup
\mathcal{D}_{\text{retrieved failure cases}}
$$

其中包括 $1000$ manually curated videos 和约 $20$K synthetic clips。还混入：

$$
20\%\ \text{T2I image tokens}
$$

作用是防止 I2V 专项训练破坏 semantic alignment。

Policy-DROID post-training：

$$
\mathcal{D}_{\text{DROID}}
=
76\text{K trajectories}
$$

$$
=350\text{ hours},\quad 86\text{ tasks},\quad 564\text{ scenes}
$$

数据构建包括：

- high resolution ingest：$360\times640$。
- community idle-frame filtering。
- failure-demonstration removal。
- random image augmentation。
- three-view canvas：wrist view + two external views。
- short task instructions 作为 prompts。

#### 8. 训练时如何消费这些数据：ratio sampling + token packing

论文里的数据构建是离线 pipeline；开源代码里能看到训练时如何消费这些数据。

多数据流按 ratio 配置：

$$
p_j
=
\frac{r_j}{\sum_k r_k}
$$

源码 `PackingIterableDataset` 接收：

```python
datasets_cfg = {
    name: {
        "dataset": dataset,
        "ratio": ratio,
    }
}
```

然后用 ratio 从多个 iterator 里采样。`JointDataLoader` 也接受多 dataloader：

```python
dataloaders = {
    "image_data": {"dataloader": ..., "ratio": 4},
    "video_data": {"dataloader": ..., "ratio": 1},
}
```

并按 tokenizer spatial compression、temporal compression、patch size、sound latent FPS 等估算 token 数，做 sequence packing。其目标是满足：

$$
\sum_{i \in B} n_i
\le
N_{\text{max tokens}}
$$

论文中 Generator 训练使用固定 token budget：

$$
N_{\text{max tokens}}=74{,}000
$$

这和数据构建的最后一步 “grouping samples into training-ready shards based on resolution and duration” 是配套的：离线 shard 保证数据可流式读取，在线 dataloader 再按 token budget 和 modality ratio 组 batch。

#### 小结

Cosmos 3 的数据构建可以理解成三层：

1. 质量层：dedup、AI judge、artifact filtering、aesthetic/technical score、caption precision/recall。
2. 能力层：Reasoner 强化 OCR/grounding/VQA/temporal/physical reasoning；Generator 强化 image/video/audio/action/transfer。
3. curriculum 层：pre-training 大而广，mid-training 高质量且 Physical AI 定向，post-training 小而精并针对具体专家能力。

最关键的设计不是“数据越大越好”，而是每个阶段的数据分布都服务对应目标：

$$
\mathcal{D}_{\text{pretrain}}
\rightarrow
\text{coverage}
$$

$$
\mathcal{D}_{\text{midtrain}}
\rightarrow
\text{Physical AI relevance + modality integration}
$$

$$
\mathcal{D}_{\text{posttrain}}
\rightarrow
\text{expert specialization}
$$

#### 原文依据

- `source/src/sections/3__data.tex:4`：Reasoner 和 Generator 使用不同数据目标，Reasoner 学理解，Generator 学合成/模拟/行动。
- `source/src/sections/3__data.tex:6`：两条 curriculum 都是 multi-stage，数据组成随阶段变化。
- `source/src/sections/data/reasoner.tex:4`：Reasoner 数据总量、pre-training/SFT 划分和 SFT 中 video-text 比例。
- `source/src/sections/data/reasoner.tex:12`：Reasoner pre-training 来源：Nemotron Nano 2 子选和额外 curated samples。
- `source/src/sections/data/reasoner.tex:16`：semantic deduplication 的 embedding 设计。
- `source/src/sections/data/reasoner.tex:18`：KMeans + cosine similarity 去重，阈值 $0.95$。
- `source/src/sections/data/reasoner.tex:21`：Gemma-4-31B-it AI judge。
- `source/src/sections/data/reasoner.tex:36`：dedup 删除比例、AI judge retention 和 SFT 阈值。
- `source/src/sections/data/reasoner.tex:38`：Reasoner pre-training 最终类别组成。
- `source/src/sections/data/reasoner.tex:44`：Reasoner SFT 总量和 Physical AI 领域。
- `source/src/sections/data/reasoner.tex:60`：temporal captions、$55$K videos、$743$K event triplets。
- `source/src/sections/data/reasoner.tex:64`：physical plausibility 数据。
- `source/src/sections/data/reasoner.tex:71`：AV human-labeled 和 auto-labeled CoT 数据。
- `source/src/sections/data/reasoner.tex:80`：robot action CoT 构建。
- `source/src/sections/data/reasoner.tex:83`：MimicGen、BEHAVIOR-1K、ERQA。
- `source/src/sections/data/reasoner.tex:86`：robotic surgery VQA。
- `source/src/sections/data/image_and_video.tex:4`：image/video 数据五步 pipeline。
- `source/src/sections/data/image_and_video.tex:7`：raw image/video 到 pre-training corpus 的规模。
- `source/src/sections/data/image_and_video.tex:11`：video scene-change detection、cropdetect、canonical re-encoding。
- `source/src/sections/data/image_and_video.tex:13`：embedding、KMeans、dedup。
- `source/src/sections/data/image_and_video.tex:15`：categorization、image/video filtering、artifact tags。
- `source/src/sections/data/image_and_video.tex:22`：mid-training high-quality image/video 构成。
- `source/src/sections/data/image_and_video.tex:24`：SDG synthetic datasets。
- `source/src/sections/data/image_and_video.tex:26`：video transfer 数据、control signals、MADS。
- `source/src/sections/data/image_and_video.tex:31`：post-training image corpus。
- `source/src/sections/data/image_and_video.tex:35`：post-training video corpus。
- `source/src/sections/data/image_and_video.tex:38`：structured JSON caption 原因。
- `source/src/sections/data/image_and_video.tex:40`：Qwen3-VL-8B image/video captioners。
- `source/src/sections/data/image_and_video.tex:42`：caption precision/recall benchmark。
- `source/src/sections/data/audio.tex:7`：audio pre-training 数据规模和 caption。
- `source/src/sections/data/audio.tex:10`：audio mid-training 数据规模和原则。
- `source/src/sections/data/audio.tex:13`：SAM-Audio source separation。
- `source/src/sections/data/audio.tex:14`：SyncNet lip-sync scoring。
- `source/src/sections/data/audio.tex:15`：FireRedASR2S speech/music ratio。
- `source/src/sections/data/audio.tex:16`：Qwen3-VL instrument detection。
- `source/src/sections/data/audio.tex:17`：speech branch filtering。
- `source/src/sections/data/audio.tex:18`：non-speech branch filtering。
- `source/src/sections/data/audio.tex:19`：audio caption annotation。
- `source/src/sections/data/action.tex:4`：为什么引入 text-video-action 数据。
- `source/src/sections/data/action.tex:6`：action 数据总规模。
- `source/src/sections/data/action.tex:11`：egocentric motion 数据。
- `source/src/sections/data/action.tex:12`：autonomous vehicle action 数据。
- `source/src/sections/data/action.tex:13`：robotics action 数据和 pseudo-actions。
- `source/src/sections/data/action.tex:14`：camera motion 数据。
- `source/src/sections/data/action.tex:19`：unified action tokenization、normalization、multi-view canvas、idle metadata。
- `source/src/figures/data/action/action_multiview_packaging.tex:45`：多视角拼接和 JSON prompt metadata。

#### 源码依据

- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/packing_iterable_dataset.py:49`：`datasets_cfg` 使用 `{dataset, ratio}`。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/packing_iterable_dataset.py:100`：检查每个数据流必须有 `dataset` 和 `ratio`。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/packing_iterable_dataset.py:124`：保存 dataset name。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/packing_iterable_dataset.py:125`：保存 sampling ratio。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/packing_iterable_dataset.py:175`：按 ratio 从多个 iterator 采样。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:148`：`JointDataLoader` 是 image/video joint loader。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:157`：`dataloaders` 配置入口。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:178`：每个 dataloader 使用 `ratio`。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:223`：检查 dataloader 配置。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:229`：保存 data ratios。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/augmentors/transfer_control_input/control_input.py:110`：Canny edge map 生成。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/augmentors/transfer_control_input/control_input.py:262`：depth control input augmentor。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/augmentors/transfer_control_input/control_input.py:296`：segmentation control input augmentor。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/augmentors/transfer_control_input/control_input.py:487`：segmentation mask 转 colored control input。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/datasets/droid_lerobot_dataset.py:50`：DROID dataset wrapper。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/datasets/droid_lerobot_dataset.py:53`：DROID action layout 为 $10$D。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/datasets/droid_lerobot_dataset.py:62`：默认 `fps=15.0`。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/datasets/droid_lerobot_dataset.py:67`：默认 `viewpoint="concat_view"`。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/datasets/droid_lerobot_dataset.py:147`：加载多视角 concat video。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/datasets/droid_lerobot_dataset.py:148`：构造 raw action。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/action/datasets/droid_lerobot_dataset.py:150`：从 task instruction 构造 caption。

---

### Q8. 训练 recipe 和 infra 是怎么样的？包括训练/推理框架、rollout、并行切分，以及哪些 infra 工作提升了吞吐或性能

#### 总览

Cosmos 3 的 infra 不是只为训练服务，而是覆盖数据处理、训练、serving、benchmark 四个环节：

![Cosmos 3 infrastructure overview](infra_overview.png)

论文把 infra stack 分成四个 pillar：

$$
\text{Infrastructure}
=
\{\text{Data engineering},\text{Large-scale training},\text{Model serving},\text{Benchmarking/validation}\}
$$

其中和训练吞吐最直接相关的是：

$$
\text{Training throughput}
\approx
f(
\text{data loader},
\text{parallelism},
\text{attention kernel},
\text{activation memory},
\text{compile},
\text{VAE tokenizer},
\text{checkpointing}
)
$$

需要先澄清一点：论文没有把 “rollout” 描述成 RL 里的 environment rollout / policy improvement loop。Cosmos 3 这里更接近 inference rollout 或 generation rollout：Reasoner 的 autoregressive loop、Generator 的 diffusion denoising loop、prompt upsampling、batch generation、robot policy action sampling。下面按这个口径解释。

#### 1. 训练 recipe：Reasoner 和 Generator 共用统一训练框架

论文说 Reasoner 和 Generator 使用同一个 unified training framework，共享：

- trainer
- parallelization architecture
- optimizers
- learning-rate schedulers
- tokenizers
- data loaders
- monitoring utilities

训练 loop 风格接近 TorchTitan：

$$
\text{for step } t:
\quad
\text{batch}
\rightarrow
\text{forward}
\rightarrow
\mathcal{L}
\rightarrow
\text{backward}
\rightarrow
\text{optimizer step}
\rightarrow
\text{scheduler step}
\rightarrow
\text{checkpoint/metrics}
$$

源码里的 trainer 也对应这个流程：

1. 初始化 optimizer/scheduler/grad scaler。
2. 从 checkpoint load 状态。
3. 按 DDP/FSDP 分布式模式包装或使用已 parallelized model。
4. dataloader 取 batch。
5. batch 移到 CUDA。
6. 调 `model.training_step(...)`。
7. 按 `save_iter` 触发 checkpoint。

Reasoner loss 是 cross entropy / next-token prediction：

$$
\mathcal{L}_{\text{Reasoner}}
=
-\sum_t w_t \log p_\theta(y_t\mid y_{<t},x)
$$

Generator loss 是 rectified-flow velocity matching：

$$
x_\sigma
=
\sigma \epsilon +(1-\sigma)x_0
$$

$$
v^\star
=
\epsilon-x_0
$$

$$
\mathcal{L}_{\text{Generator}}
=
\sum_m \lambda_m
\operatorname{MSE}
\left(
(1-M_m)\odot v_\theta(x_\sigma,\sigma,c),
(1-M_m)\odot v^\star
\right)
$$

其中 $M_m$ 是 condition mask，condition tokens 不参与 loss。

#### 2. Data loader：异构多模态训练的核心瓶颈

Cosmos 3 的 data loader 要处理 image、video、audio、action、text，且分辨率、帧数、token 数差异很大。论文强调一个问题：如果像普通 LLM 一样按 fixed sample count 分 batch，会导致严重低效。

原因是单个样本 token 数差异超过两个数量级：

$$
n_{\text{tokens}}(\text{720p video})
\gg
n_{\text{tokens}}(\text{image})
\gg
n_{\text{tokens}}(\text{text caption})
$$

attention 成本近似：

$$
\operatorname{FLOPs}_{\text{attn}}
\propto
T^2
$$

所以不同 rank 如果拿到不同 modality/resolution，会出现：

$$
T_{\rho_1}\ne T_{\rho_2}
\Rightarrow
\text{step time}_{\rho_1}\ne \text{step time}_{\rho_2}
$$

最终导致 padding waste、rank imbalance、甚至 NCCL collective timeout。

Cosmos 3 用四个机制解决：

1. token-budgeted packed sequences。
2. joint data loader。
3. rank-synchronous stream selection。
4. look-ahead packing。

Joint DataLoader 图：

![Joint data loader](joint_dataloader.png)

##### 2.1 Token-budgeted packed sequences

每个 rank 不固定 sample count，而是固定 token budget：

$$
\sum_{i\in B_\rho} n_i
\le
T_{\max}
$$

Generator 训练里：

$$
T_{\max}=74{,}000
$$

这样不同长度样本可以 pack 到一个 sequence，减少 padding：

$$
\text{padding waste}
=
1
-
\frac{\sum_i n_i}{|B| \cdot \max_i n_i}
$$

packed sequence 的目标就是让这个 waste 尽量接近 $0$。

##### 2.2 Rank-synchronous stream selection


###### 简短结论

基本可以这样理解：

$$
\text{at each global iteration, all ranks select the same stream}
$$

也就是说，在第 $i$ 个 global training step，所有 distributed ranks 都会选择同一个 active stream，例如：

$$
k_i = \text{720p video stream}
$$

或：

$$
k_i = \text{image 480p stream}
$$

但这不等于所有 rank 取同一批样本。更准确地说：

$$
\forall r,\quad \text{rank}_r \text{ selects the same stream } k_i
$$

但：

$$
\text{batch}_{i,r}
\neq
\text{batch}_{i,r'}
$$

每个 rank 仍然从自己的本地 shard / worker / buffer 中取不同样本，只是这些样本属于同一个 stream。

###### stream 是什么？

论文里的 stream 不是 CUDA stream，也不是推理时的 streaming output。这里的 stream 是 data stream，即 Joint DataLoader 里被单独封装的一路数据加载器。

论文原文说：

$$
\text{Each modality, dataset, or finer-grained data stream is encapsulated in its own loader}
$$

所以 stream 可以是：

$$
\text{stream}
\in
\{
\text{modality},
\text{dataset},
\text{modality-resolution bucket},
\text{更细粒度的数据子集}
\}
$$

例如可能拆成：

$$
\begin{aligned}
s_1 &= \text{image-256p}\\
s_2 &= \text{image-480p}\\
s_3 &= \text{video-256p}\\
s_4 &= \text{video-720p}\\
s_5 &= \text{action-DROID-480p}\\
s_6 &= \text{audio-video}
\end{aligned}
$$

源码实现里，stream 对应 `dataloaders` 字典中的一个 named dataloader：

$$
\mathcal{S}
=
\{s_1,\ldots,s_K\}
$$

每个 $s_k$ 有自己的：

$$
\text{dataloader}_k,\quad
\text{ratio}_k,\quad
\text{buffer}_k
$$

所以 `stream` 的粒度取决于配置。如果配置把不同分辨率拆成不同 dataloader，那么它就是“模态 + 分辨率桶”；如果配置只按数据集拆，它也可以是“数据集 stream”。

###### 每个 step 是否只取一种模态 / 分辨率桶？

在 rank-synchronous stream selection 的语义下，是的：

$$
\text{one global step}
\rightarrow
\text{one selected stream } k_i
$$

如果这个 stream 本身定义为“某个模态 / 某个分辨率桶”，那么该 step 所有 rank 都会处理这个模态 / 分辨率桶的数据。

论文原文更具体地说：

$$
\text{all ranks process samples drawn from the same modality and resolution bucket at every step}
$$

也就是：

$$
\forall r,\quad
x_{i,r}
\sim
\mathcal{D}_{k_i}
$$

其中 $\mathcal{D}_{k_i}$ 是第 $i$ 步选中的那个 stream 的数据分布。

但是，每个 rank 会在这个 stream 内按 token budget 打包多个样本：

$$
B_i^{(r)}
=
\{x_{i,r,1},x_{i,r,2},\ldots,x_{i,r,n_r}\}
$$

满足：

$$
\sum_{j=1}^{n_r} T(x_{i,r,j})
\le
T_{\max}
$$

其中 $T(x)$ 是样本序列化后的 token 数，$T_{\max}$ 是该 rank 每 step 的 token budget。

因此它不是：

$$
\text{每 step 只取一个样本}
$$

而是：

$$
\text{每 step 每个 rank 从同一个 stream 中 pack 一批样本}
$$

###### 为什么要这么做？

核心原因是多模态样本 token 数差异非常大：

$$
T(\text{720p video})
\gg
T(\text{256p image})
\gg
T(\text{text caption})
$$

论文给的例子是：

$$
T(\text{video})
>
100 \times T(\text{image})
$$

并且：

$$
T(\text{720p video})
>
10 \times T(\text{256p video})
$$

如果各 rank 独立随机选 stream，就可能出现同一个 distributed step 内：

$$
\begin{aligned}
\text{rank}_0 &: \text{720p video}\\
\text{rank}_1 &: \text{256p image}\\
\text{rank}_2 &: \text{text/action short sequence}\\
\text{rank}_3 &: \text{480p video}
\end{aligned}
$$

这样会导致：

$$
\text{FLOPs}_r
\propto
T_r^2
$$

尤其 attention 是近似二次复杂度：

$$
\operatorname{cost}_{\text{attn}}
=
O(T^2 d)
$$

所以不同 rank 的 step time 会差很多：

$$
\Delta t
=
\max_r t_r - \min_r t_r
$$

在 FSDP / distributed training 中，每个 step 都要做 collective communication。如果某些 rank 很快进入 collective，而另一些 rank 还在处理长视频 batch，就会造成：

$$
\text{rank imbalance}
\rightarrow
\text{idle wait}
\rightarrow
\text{NCCL timeout risk}
$$

rank-synchronous stream selection 的目标就是让所有 rank 在同一个 step 的 token length distribution 接近：

$$
T_{i,0}
\approx
T_{i,1}
\approx
\cdots
\approx
T_{i,R-1}
$$

不是为了让数据完全一样，而是为了让计算负载和显存占用一致。

###### 它怎么保证全局比例不被破坏？

源码里有两种方式。

第一种是带 seed 的随机选择。第 $i$ 步用：

$$
\operatorname{rng}_i
=
\operatorname{RandomState}(\text{seed}+i)
$$

然后按配置比例采样：

$$
k_i
\sim
\operatorname{Categorical}(p_1,\ldots,p_K)
$$

其中：

$$
p_k
=
\frac{\rho_k}{\sum_{m=1}^{K}\rho_m}
$$

因为所有 rank 的 $\text{seed}$ 和 $\text{global\_id}=i$ 相同，所以都会得到相同的 $k_i$。

第二种是不带 seed 的 deterministic round-robin。设 ratio 为：

$$
\rho_1:\rho_2:\cdots:\rho_K
$$

则根据：

$$
d_i
=
i \bmod \sum_k \rho_k
$$

映射到对应 stream。比如 image:video = $2:1$，则：

$$
\text{image},\text{image},\text{video},\text{image},\text{image},\text{video},\ldots
$$

这样长期看仍然满足配置比例：

$$
\lim_{N\to\infty}
\frac{\#\{i<N:k_i=k\}}{N}
=
p_k
$$

###### 源码对应关系

`IterativeJointDataLoader` 的核心逻辑是：

$$
\text{index\_id}
=
\operatorname{choice}
\left(
\{1,\ldots,K\},
p
=
\text{data\_probs}
\right)
$$

代码里对应：

- `cosmos_framework/data/vfm/joint_dataloader.py:506`：注释说明 seed 不为 `None` 时，每个 iteration 按 ratio 随机选择 modality。
- `cosmos_framework/data/vfm/joint_dataloader.py:510`：使用 `seed + global_id`，保证 synchronized global_id 下所有 rank 选择相同 modality。
- `cosmos_framework/data/vfm/joint_dataloader.py:559`：`rng = np.random.RandomState(self.seed + self.global_id)`。
- `cosmos_framework/data/vfm/joint_dataloader.py:560`：`index_id = rng.choice(len(self.dataloader_list), p=self.data_probs)`。
- `cosmos_framework/data/vfm/joint_dataloader.py:591`：计算当前样本 token 数。
- `cosmos_framework/data/vfm/joint_dataloader.py:593`：判断加入当前样本是否超过 `max_sequence_length`。
- `cosmos_framework/data/vfm/joint_dataloader.py:614`：未超预算则累加 token 数。
- `cosmos_framework/data/vfm/joint_dataloader.py:617`：把样本追加进当前 output batch。
- `cosmos_framework/data/vfm/joint_dataloader.py:628`：每 yield 一个 batch 后 `global_id += 1`。

###### 一句话总结

`rank-synchronous stream selection` 的含义是：

$$
\boxed{
\text{同一个 global step，所有 rank 选择同一个数据 stream；各 rank 在该 stream 内取不同样本并按 token budget pack。}
}
$$

如果 stream 被配置成“模态 / 分辨率桶”，那么可以理解为：

$$
\boxed{
\text{每个 step 只训练一种模态 / 分辨率桶，但不是只训练一个样本，也不是所有 rank 拿同样数据。}
}
$$

##### 2.3 Look-ahead packing

纯 greedy packing 遇到下一个样本放不下时会停止，留下 residual capacity：

$$
\Delta
=
T_{\max}-\sum_{i\in B} n_i
$$

look-ahead packing 的做法是：如果当前候选样本太大但 batch 已非空，就暂存到 look-aside buffer，继续向后找更小样本填满剩余预算。

论文说 production 中 look-ahead cap 用 $10$，吞吐收益是：

$$
\text{effective sequence length improvement}=8\%
$$

$$
\text{training throughput improvement}\approx 8\%
$$

源码 `IterativeJointDataLoader` 中能看到 `lookahead_limit`、`skipped_samples`、`current_sequence_length + num_tokens_in_current_sample >= max_sequence_length` 这些逻辑。

##### 2.4 Cold-start handling

多个 data stream 首 batch 可能很慢：worker spawn、filesystem metadata cache、shard deserialization 都会造成 cold-start latency。Cosmos 3 的 Joint DataLoader 在构造阶段对每个 stream 做 pre-warm，并在训练 loop 前 barrier：

$$
\text{prewarm all streams}
\rightarrow
\text{distributed barrier}
\rightarrow
\text{first forward}
$$

这不是提升 steady-state token/s 的主要来源，但能避免第一步撞上 NCCL watchdog timeout。

#### 3. Attention infra：two-way flat attention 替代 FlexAttention baseline

MoT 的 attention mask 很特殊：

- Reasoner pathway：AR tokens causal attention，且只看 Reasoner tokens。
- Generator pathway：Generator tokens bidirectionally attend 自己样本内的 Reasoner + Generator tokens。

论文指出，直接用通用 FlexAttention 虽然正确，但 mask 结构对 kernel 不透明，会做 padding-equivalent work。

Cosmos 3 的 two-way flat attention 把一次 layer attention 分成两个 kernel invocation：

$$
\operatorname{Attn}_{R}
=
\operatorname{CausalSDPA}(Q_R,K_R,V_R)
$$

$$
\operatorname{Attn}_{G}
=
\operatorname{BiAttn}(Q_G,[K_R,K_G],[V_R,V_G])
$$

packed batch 内按 sample granularity 组织：

$$
[R_0,G_0,R_1,G_1,\ldots,R_n,G_n]
$$

这样每个 Generator query 只 attend 自己样本内的 $[R_i,G_i]$，避免跨样本污染。

two-way attention 图：

![Two-way attention infrastructure](two_way_attention_infra.png)

论文报告，相比 FlexAttention baseline，Cosmos3-Nano 的端到端训练吞吐提升：

$$
\text{throughput improvement}=22\%
$$

backend 选择：

- H100/H200：FlashAttention-3。
- GB200：NATTEN，基于 CUTLASS，适配 Blackwell tensor cores 和 memory hierarchy。

#### 4. 分布式切分并行：HSDP + Ulysses CP

训练使用：

$$
\text{Parallelism}
=
\text{HSDP}
\oplus
\text{CP}
$$

其中 HSDP 是 Hybrid Sharded Data Parallelism：

$$
\text{world size}
=
d_{\text{replicate}}
\times
d_{\text{shard}}
$$

HSDP 在 shard group 内切分：

$$
\{\theta,\nabla,\text{optimizer states}\}
\rightarrow
\text{shards}
$$

同时在 replicate groups 之间复制，以在显存和通信之间折中。

CP 是 context parallelism，用来切 sequence dimension：

$$
X\in\mathbb{R}^{B\times T\times H}
\rightarrow
\{X^{(r)}\in\mathbb{R}^{B\times T/R_{\text{CP}}\times H}\}_{r=1}^{R_{\text{CP}}}
$$

Cosmos 3 使用 Ulysses CP。每层 attention 做两次 all-to-all：

1. sequence-sharded $\rightarrow$ head-sharded：

$$
\text{shard over } T
\xrightarrow{\text{all-to-all}}
\text{shard over heads}
$$

2. attention 后再从 head-sharded 还原到 sequence-sharded：

$$
\text{shard over heads}
\xrightarrow{\text{all-to-all}}
\text{shard over } T
$$

最大 CP degree 受 query heads 数限制：

$$
R_{\text{CP}}\le H_{\text{query}}
$$

论文给出：

$$
R_{\text{CP,max}}=32
\quad \text{for Cosmos3-Nano}
$$

$$
R_{\text{CP,max}}=64
\quad \text{for Cosmos3-Super}
$$

源码 `ParallelDims` 把并行 mesh 拆成：

$$
\text{dp\_mesh}
=(d_{\text{replicate}},d_{\text{shard}})
$$

$$
\text{cp\_mesh}
=R_{\text{CP}}
$$

$$
\text{cfgp\_mesh}
=R_{\text{CFGP}}
$$

注意 `cp` 和 `cfgp` 在源码里是 overlay axes，不消耗 FSDP rank slots：

$$
d_{\text{replicate}}\cdot d_{\text{shard}}
=
\text{world\_size}
$$

$$
\text{cfgp}\cdot\text{cp}
\mid
\text{world\_size}
$$

训练时 cfgp 被禁用，只有 inference mode 才允许：

$$
R_{\text{CFGP}}>1
\Rightarrow
\text{enable\_inference\_mode}=\text{True}
$$

#### 5. Selective Activation Checkpointing：减少重算成本

标准 activation checkpointing 只保留 block input，反向时重算 block 内部。论文说这会让每步 FLOPs 增加约：

$$
\Delta \operatorname{FLOPs}\approx 33\%
$$

Cosmos 3 使用 Selective Activation Checkpointing，按 FLOPs-to-memory ratio 选择值得保留的中间激活：

$$
\operatorname{score}(o)
=
\frac{\operatorname{FLOPs}_{\text{recompute}}(o)}
\operatorname{Memory}(o)
$$

优先保留：

$$
o^\star
=
\arg\max_o \operatorname{score}(o)
$$

对长序列 transformer 来说，attention output 最划算，因为 attention 重算代价近似 $O(T^2)$，但 output tensor 大小是 $O(T)$。

论文报告，在 Cosmos3-Nano、$74{,}000$ token budget 下：

$$
\text{SAC throughput improvement}=13\%
$$

#### 6. torch.compile：训练侧和推理侧都用

训练侧：

$$
\texttt{torch.compile(fullgraph=True, dynamic=True)}
$$

其中：

- `fullgraph=True`：减少 CPU overhead，帮助 operator fusion。
- `dynamic=True`：适配多模态 batch 的 variable sequence length。

论文报告 Cosmos3-Nano Generator training：

$$
\text{torch.compile throughput improvement}=41\%
$$

推理侧 plain PyTorch path 也用 torch compile + CUDA graphs，但捕获粒度是 transformer layer，而不是整个 outer inference loop：

$$
\text{captured graph}
=
\text{repeated transformer block computation}
$$

$$
\text{not captured}
=
\text{prompt handling}+\text{timestep scheduling}+\text{sampler update}+\text{CFG orchestration}+\text{decoding}
$$

T2I generation 上 CUDA Graphs 带来：

$$
\text{speedup}=30\%\sim 60\%
$$

#### 7. Video tokenizer / VAE：on-the-fly 编码但做了专门优化

Cosmos 3 训练不是先离线抽 latent，而是在 training loop 里 on-the-fly 调 Wan2.2 VAE：

$$
\text{raw video frames}
\xrightarrow{\text{Wan2.2 VAE}}
x_0^{\text{vision latent}}
\xrightarrow{\text{MoT}}
\mathcal{L}_{\text{FM}}
$$

优点是 augmentation、encoding、training 保持同步；缺点是 VAE 可能成为 critical path，尤其是 Edge/Nano 这种 transformer compute 较小的模型。

论文做了三类优化：

##### 7.1 Chunked encoding

Wan2.2 causal tokenizer 默认每次处理一个 latent chunk，即 prime frame 后每 $4$ pixel frames 一个 latent chunk。Cosmos 3 改成一次 encode 多帧，提高 kernel arithmetic intensity。

经验 chunk sizes：

| Resolution | Encode chunk size |
| --- | ---: |
| $256p$ | $68$ frames |
| $480p$ | $24$ frames |
| $720p$ | $12$ frames |

##### 7.2 AOTInductor sharded compilation

VAE 编译有：

$$
3\ \text{resolutions}
\times
5\ \text{aspect ratios}
\times
3\ \text{modes}
=
45\ \text{graphs}
$$

如果每个 rank 串行编译 $45$ 个 graph，启动慢约 $15$ 分钟。Cosmos 3 用 AOTInductor，把编译分摊到 DP ranks：

$$
\text{rank}_i
\rightarrow
\text{compile graph}_i
$$

然后写共享文件系统，所有 rank 再加载完整 artifacts。启动 overhead 降到：

$$
<1\text{ minute}
$$

##### 7.3 Known frame-count specialization

对机器人 action dataset 这种固定 clip 长度的数据，直接为精确 shape 编译，避免 padding-and-crop 的 padded-tail compute。

#### 8. Checkpointing：异步保存 + 保存计划复用 + object-store 优化

同步 checkpoint 会让训练 loop 停在 I/O 上。Cosmos 3 使用异步 checkpoint：

$$
\text{training process}
\rightarrow
\text{snapshot state on device}
\rightarrow
\text{background writer}
\rightarrow
\text{remote object storage}
$$

关键点：

- checkpoint I/O 走独立 Gloo process group，不占训练 NCCL communicator。
- child process 用 multiprocessing queue 接收 save request。
- 第一次 save 计算 save plan，后续复用。
- replicated tensors 做 dedup。
- `dedup_to_lowest_rank=True`，replicated tensors 只存最低 rank，减少 load 时每个 rank 需要读的文件。
- RNG/data-loader state 也保存/恢复，保证 resume 的可复现性。

论文报告，30 分钟保存间隔下，相比 synchronous checkpoint：

| Model | Mean save time | Max save time | Async speedup |
| --- | ---: | ---: | ---: |
| Cosmos3-Nano | $72$s | $250$s | $4\%$ |
| Cosmos3-Super | $167$s | $736$s | $9\%$ |

save plan memorization 进一步减少 checkpoint overhead：

$$
\text{checkpoint overhead reduction}\approx 60\%
$$

#### 9. Serving / rollout：Reasoner AR loop + Generator diffusion loop

论文 serving infra 分三类：

1. Plain PyTorch reference backend。
2. Reasoner production backend：TensorRT-LLM 和 vLLM。
3. Generator production backend：vLLM-Omni。

Plain PyTorch path 是 reference implementation，完整 rollout 包括：

$$
\text{input preparation}
\rightarrow
\text{AR loop}
\rightarrow
\text{diffusion loop}
\rightarrow
\text{decode/postprocess}
$$

Reasoner rollout：

$$
y_t
\sim
p_\theta(y_t\mid y_{<t},x_{\text{context}})
$$

源码 `generate_reasoner_text` 明确只走 reasoner tower，bypass generation pathway：

$$
\text{Reasoner AR}
=
\text{und-pathway weights}
+\text{embed/norm/lm\_head}
+\text{optional Qwen3-VL visual tower}
$$

Generator rollout 是 diffusion/rectified-flow sampling。源码 `generate_samples_from_batch` 的流程是：

1. build sequence plans。
2. encode condition。
3. initialize noise with conditioning。
4. build velocity function。
5. run sampler。

采样器支持：

$$
\text{sampler}\in\{\text{UniPC},\text{EDM}\}
$$

每个 denoising step 里：

$$
\hat{v}
=
v_\theta(x_t,t,c)
$$

CFG 组合为：

$$
\hat{v}_{\text{cfg}}
=
\hat{v}_{\text{uncond}}
s\left(
\hat{v}_{\text{cond}}
-
\hat{v}_{\text{uncond}}
\right)
$$

源码 `_run_classifier_free_guidance` 支持 CFG parallelism：

- `cfgp_rank=0` 跑 conditional branch。
- `cfgp_rank=1` 跑 unconditional branch。
- 两边通过 point-to-point exchange 交换 velocity。

这对应论文中说的 CFG-Parallel：每步条件/无条件两次 forward 可以并行，理论上接近减半 CFG latency。

#### 10. 推理并行和 serving 优化

推理时使用：

$$
\text{Inference parallelism}
=
\text{CP}
\oplus
\text{CFG parallelism}
\oplus
\text{optional HSDP/CPU offload/VAE patch parallel}
$$

##### 10.1 Context parallelism for inference

推理也沿用 Ulysses CP：

$$
T
\rightarrow
T/R_{\text{CP}}
$$

它有两个作用：

- 支持超过单卡显存的长 context generation。
- 即使单卡放得下，也能通过多卡分担 forward 降低 latency。

##### 10.2 CFG parallelism

CFG 每步需要：

$$
\hat{v}_{\text{cond}},
\qquad
\hat{v}_{\text{uncond}}
$$

串行需要两次 forward：

$$
t_{\text{CFG,serial}}
\approx
2t_{\text{forward}}
$$

并行后：

$$
t_{\text{CFG,parallel}}
\approx
t_{\text{forward}}+t_{\text{sync}}
$$

##### 10.3 Reasoner tower caching

T2I/T2V/I2V/V2V 中，Reasoner conditioning 在整个 sampling trajectory 不变：

$$
c_R
=
f_R(\text{text/image/video condition})
$$

与 denoising step $t$ 无关：

$$
c_R^{(1)}
=
c_R^{(2)}
=
\cdots
=
c_R^{(N)}
$$

所以可以只算一次并缓存：

$$
\text{cost}
=
\operatorname{cost}(f_R)
+N\cdot \operatorname{cost}(f_G)
$$

而不是：

$$
N\cdot
\left(
\operatorname{cost}(f_R)
+\operatorname{cost}(f_G)
\right)
$$

##### 10.4 Batching

推理 batcher 复用训练的 variable-length sequence packing：

$$
\sum_i n_i \le T_{\max}
$$

T2V 189-frame outputs 上，论文报告 batching 的收益：

| Backend | Nano T2V-256 | Nano T2V-480 | Super T2V-256 | Super T2V-480 |
| --- | ---: | ---: | ---: | ---: |
| H100 80GB | $8\%$ | $2\%$ | $55\%$ | $5\%$ |
| GB200 | $40\%$ | $2\%$ | $9\%$ | $1\%$ |

720p 没列，因为 $74$K context window 下只能放：

$$
B=1
$$

所以 batching 没收益。

Serving latency 图：

![Cosmos 3 serving latency](serving_latency_combined.png)

##### 10.5 vLLM-Omni features

Generator 接入 vLLM-Omni，支持：

- Cache-DiT：跨相邻 denoising steps 复用 transformer-block outputs。
- Ulysses CP：长 image/video token sequence 多卡切分。
- CFG-Parallel：条件/无条件 forward 分到不同 GPU。
- HSDP：FSDP2 shard weights，forward 时按需 gather。
- CPU offload：参数在 CPU/GPU 间 layer-wise offload。
- VAE-Patch-Parallel：VAE encode/decode 按 spatial tiles 并行。
- dynamic FP8 quantization：降低 dominant compute 精度，减少 latency 和显存。

这些是 serving 侧对“rollout”效率最直接的优化。

#### 11. 训推硬件：论文和开源仓库分别提到了什么？

需要区分三类“硬件信息”：

$$
\text{paper-scale training hardware}
\ne
\text{open-source SFT recipe hardware}
\ne
\text{inference benchmark hardware}
$$

##### 11.1 论文级 Generator 训练硬件

论文正文明确写 Generator pre-training / mid-training 用的是 NVIDIA GB200 GPUs。

Generator pre-training：

| Model | Tokens | GPUs |
| --- | ---: | ---: |
| Cosmos3-Nano | $31.05$T | $1024$ GB200 |
| Cosmos3-Super | $17.86$T | $2048$ GB200 |

Generator mid-training：

| Model | Tokens | GPUs |
| --- | ---: | ---: |
| Cosmos3-Nano | $2.4$T | $1024$ GB200 |
| Cosmos3-Super | $1.9$T | $2048$ GB200 |

论文训练吞吐表也在 GB200 上报告 dense model steady-state throughput，但这里有一个细节：正文训练 token 段落写的是：

$$
\text{Nano/Super}
=
1024/2048\ \text{GB200 GPUs}
$$

而 training throughput 表 caption 写 benchmark runs 使用：

$$
\text{Nano/Super}
=
2048/4096\ \text{GB200 GPUs}
$$

这两个数字在论文中并不完全一致。更稳妥的写法是：大规模训练和吞吐 benchmark 都基于 GB200，但具体 GPU 数按对应段落/表格分别引用。

##### 11.2 公开 Cosmos-Framework 的 SFT recipe 硬件

开源仓库不是复现论文级预训练规模，而是提供 SFT / runnable recipe。README 里明确说 shipped recipes 是 $8$ GPU configs，并且测试在：

$$
8\times \text{H100 80GB}
$$

也就是：

$$
\text{open-source recipe hardware}
=
8\times \text{H100 80GB}
$$

用户可以按自己的硬件调整：

$$
\text{NPROC\_PER\_NODE},\quad
\text{DP/CP/FSDP shard degrees}
$$

所以这里不能把开源 SFT recipe 的 $8\times$ H100 80GB 理解成论文预训练用的硬件规模。

##### 11.3 推理 / serving benchmark 提到的硬件

Cosmos 主仓库的 inference benchmark 覆盖了更多硬件，尤其包括你提到的 RTX：

$$
\text{RTX PRO 6000 Blackwell}
$$

benchmark 文档中 Generator / Reasoner 表格提到的 GPU 包括：

| Hardware | 出现场景 |
| --- | --- |
| RTX PRO 6000 Blackwell | Generator latency、Reasoner serving benchmark |
| H20 | Generator latency、Reasoner serving benchmark |
| H100 NVL | Generator latency、Reasoner serving benchmark |
| H200 NVL | Generator latency、Reasoner serving benchmark |
| H100 80GB HBM3 / SXM | Generator latency、Reasoner serving benchmark |
| H200 141GB HBM3 | Generator latency、Reasoner serving benchmark |
| B200 | Generator latency、Reasoner serving benchmark |
| B300 | benchmark 表中列出，部分项为空或待测 |

其中 Generator benchmark 比较三条路径：

$$
\text{PyTorch}
\quad
\text{vs}
\quad
\text{vLLM-Omni}
\quad
\text{vs}
\quad
\text{Diffusers}
$$

并按：

$$
\text{GPU}\times\text{engine}\times\text{resolution}\times\text{TP degree}
$$

报告 latency。RTX PRO 6000 Blackwell 在表里不是训练硬件，而是推理 benchmark / workstation-class Blackwell 硬件。

这些 case 是有性能数据的，但要区分 Generator 和 Reasoner 的指标：

$$
\text{Generator metrics}
=
\text{diffusion-path latency in seconds}
$$

$$
\text{Reasoner metrics}
=
\{\text{TTFT},\text{request latency},\text{request throughput},\text{output token throughput}\}
$$

其中：

$$
\text{TTFT}
=
\text{time to first token}
$$

Generator benchmark 是 image/video generation 的采样时延；Reasoner benchmark 是 vLLM serving 下的文本生成服务指标。二者不能直接用同一个数字比较，因为 Generator 是 diffusion rollout，Reasoner 是 autoregressive text decoding。

###### Generator 代表性时延：Nano T2V, 720p, 189 frames

下表摘的是 Cosmos3-Nano Text-to-Video 的 $720p$ 代表项，单位是秒。`/1`、`/4`、`/8` 表示 tensor parallel degree：

| Hardware | PyTorch $720p/1$ | PyTorch $720p/4$ | PyTorch $720p/8$ | vLLM-Omni $720p/8$ | Diffusers $720p/1$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| RTX PRO 6000 Blackwell | $786.37$ | $225.45$ | $127.57$ | $68.66$ | $392.00$ |
| H20 | $931.39$ | $268.88$ | $157.71$ | - | $926.00$ |
| H100 NVL | $297.27$ | $94.15$ | $61.63$ | $54.01$ | $324.20$ |
| H200 NVL | $244.39$ | $77.35$ | $45.70$ | - | $276.20$ |
| H100 80GB HBM3 | $207.78$ | $66.94$ | $41.81$ | - | $240.00$ |
| H200 141GB HBM3 | $214.28$ | $67.48$ | $41.26$ | - | $239.60$ |
| B200 | $114.85$ | $39.75$ | $26.27$ | $22.87$ | $117.00$ |
| B300 | - | - | - | - | $139.40$ |

这个表能看出两个点：

$$
\text{multi-GPU TP}
\Rightarrow
\text{lower latency}
$$

以及：

$$
\text{vLLM-Omni}
\text{ 在已覆盖硬件/配置上通常低于 PyTorch reference path}
$$

但文档也明确说明：空单元格表示该组合尚未测量，不代表不支持。

###### Generator 代表性时延：Super T2V, 720p

Cosmos3-Super 的覆盖更窄。代表性 $720p$ T2V 时延如下，单位同样是秒：

| Hardware | PyTorch $720p/4$ | PyTorch $720p/8$ | vLLM-Omni $720p/8$ | Diffusers $720p/1$ |
| --- | ---: | ---: | ---: | ---: |
| RTX PRO 6000 Blackwell | $789.03$ | $427.16$ | - | - |
| H20 | - | $492.41$ | - | - |
| H100 NVL | $330.04$ | $186.19$ | - | - |
| H200 NVL | $258.34$ | $139.37$ | - | $1036.00$ |
| H200 141GB HBM3 | $224.43$ | $123.49$ | - | $886.20$ |
| B200 | $118.38$ | $65.93$ | $62.11$ | $414.40$ |
| B300 | - | - | - | $424.80$ |

Super 的 benchmark 文档特别说明：

$$
\text{coverage}_{\text{Super}}
<
\text{coverage}_{\text{Nano}}
$$

也就是很多硬件/engine 组合还没有实测。

###### Reasoner 代表性 serving 指标：Nano, vLLM

Reasoner benchmark 不是 diffusion 时延，而是 vLLM 下的服务指标。下面摘一个常用代表负载：

$$
\text{Input}=50,\quad
\text{Output}=100,\quad
\text{Video}=1\ \text{FPS},\quad
\text{Concurrency}=128
$$

单位：TTFT / request latency 为毫秒，throughput 为 token/s。

| Hardware | TTFT | Request latency | Output token throughput |
| --- | ---: | ---: | ---: |
| RTX PRO 6000 Blackwell | $4627.08$ | $18541.90$ | $682.18$ |
| H20 | $10973.05$ | $37514.21$ | $339.57$ |
| H100 NVL | $5022.58$ | $18061.43$ | $702.48$ |
| H200 NVL | $3180.20$ | $10054.55$ | $1259.60$ |
| H100 80GB HBM3 | $2906.00$ | $9818.73$ | $1286.89$ |
| H200 141GB HBM3 | $2839.97$ | $9364.20$ | $1352.41$ |
| B200 | $2111.97$ | $5001.20$ | $2523.07$ |
| B300 | $1444.68$ | $4750.02$ | $2657.14$ |

趋势上：

$$
\text{B200/B300}
\text{ 的 Reasoner token throughput 明显高于 H100/H200/RTX PRO 6000}
$$

###### Reasoner 代表性 serving 指标：Super, vLLM

同样负载下，Cosmos3-Super 的覆盖更少，但 benchmark 也给了代表硬件数据：

$$
\text{Input}=50,\quad
\text{Output}=100,\quad
\text{Video}=1\ \text{FPS},\quad
\text{Concurrency}=128
$$

| Hardware | TTFT | Request latency | Output token throughput |
| --- | ---: | ---: | ---: |
| RTX PRO 6000 Blackwell | $54400.80$ | $69193.77$ | $149.69$ |
| H20 | $108988.21$ | $135784.46$ | $77.81$ |
| H100 NVL | $54861.82$ | $67203.81$ | $154.58$ |
| H200 NVL | $16053.68$ | $40187.13$ | $305.57$ |
| H200 141GB HBM3 | $14328.53$ | $35613.84$ | $344.42$ |
| B200 | $5574.27$ | $17572.41$ | $721.29$ |
| B300 | $4999.71$ | $17203.60$ | $736.64$ |

这个表说明：同一 Reasoner serving workload 下，Super 的 latency 明显高于 Nano，token throughput 也更低：

$$
\text{Cosmos3-Super}
\Rightarrow
\text{larger model, higher latency, lower serving throughput}
$$

##### 11.4 硬件和 attention backend 的对应关系

论文 infra 里还提到了 backend 与硬件架构的对应：

| Hardware / architecture | Attention backend |
| --- | --- |
| H100 / H200, Hopper | FlashAttention-3 |
| GB200, Blackwell | NATTEN, CUTLASS-based |

可以写成：

$$
\text{Hopper}
\rightarrow
\text{FlashAttention-3}
$$

$$
\text{Blackwell/GB200}
\rightarrow
\text{NATTEN + CUTLASS}
$$

这说明 Cosmos 3 的 infra 不是只抽象地写 PyTorch operator，而是针对不同 NVIDIA GPU generation 选择不同 attention backend。

##### 11.5 总结

硬件层面的准确总结是：

$$
\boxed{
\text{论文级训练：GB200；开源 SFT recipe：8}\times\text{H100 80GB；推理 benchmark：RTX PRO 6000 Blackwell、H20、H100/H200、B200/B300 等。}
}
$$

其中 RTX 相关描述主要来自开源仓库的 inference benchmark，不是论文正文中的大规模训练硬件。

#### 12. 训练吞吐结果

论文在 GB200 上报告 dense model steady-state throughput：

| Model | Iter time | TFLOPS/GPU | MFU | Iter/hr | Img Tok/hr/GPU | Vid Tok/hr/GPU |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cosmos3-Nano | $7.1$s | $520$ | $0.23$ | $507$ | $4.56$M | $16.23$M |
| Cosmos3-Super | $19.5$s | $673$ | $0.30$ | $185$ | $1.66$M | $5.91$M |

注意论文正文和表格 GPU 数有一个不完全一致的地方：正文说 Nano/Super throughput benchmark 用 $1024/2048$ GB200 GPUs；表格 caption 写 Nano/Super runs took $2048/4096$ GPUs。这里应保留原文差异，不做自行修正。

#### 13. 哪些 infra 工作明确提升了吞吐/性能？

论文明确量化的提升：

| Infra 工作 | 提升 |
| --- | ---: |
| rank-synchronous stream selection | end-to-end training throughput $+54\%$ |
| look-ahead packing | effective sequence length $+8\%$，对应 throughput $+8\%$ |
| two-way flat attention vs FlexAttention baseline | Cosmos3-Nano training throughput $+22\%$ |
| Selective Activation Checkpointing | Cosmos3-Nano, $74$K token budget, throughput $+13\%$ |
| `torch.compile(fullgraph=True,dynamic=True)` | Cosmos3-Nano Generator training throughput $+41\%$ |
| tokenizer `torch.compile` | VAE encode latency reduction $52\%$ |
| AOTInductor sharded compile | startup from $\sim 15$ min to $<1$ min |
| async checkpointing | Nano training time $-4\%$，Super training time $-9\%$ |
| checkpoint save-plan memorization | checkpoint overhead reduction $\sim 60\%$ |
| PyTorch CUDA graphs for T2I serving | speedup $30\%\sim60\%$ |
| inference batching | T2V speedup $1\%\sim55\%$ depending model/resolution/backend |
| SILA data infra | curation throughput $10\times$ over previous architecture |
| SILA startup latency | $30$--$60$ min 降到约 $5$ min |

未单独给出百分比、但机制上重要的：

- HSDP：降低参数/梯度/optimizer states 显存压力。
- Ulysses CP：支持 $74$K 及更长 context，降低单卡 activation memory。
- FlashAttention-3 / NATTEN：提升 variable-length attention kernel 效率。
- reasoner tower caching：减少 diffusion steps 中重复算固定条件的开销。
- CFG parallelism：把 CFG 的 cond/uncond 双 forward 并行化。
- VAE-Patch-Parallel、CPU offload、FP8 quantization：降低 serving 侧显存和 latency。

#### 原文依据

- `source/src/sections/5__infrastructure.tex:4`：infra 四个 pillar 总览。
- `source/src/sections/5__infrastructure.tex:6`：data engineering 输出 WebDataset 格式训练数据。
- `source/src/sections/5__infrastructure.tex:7`：large-scale training 依赖并行、数据加载、checkpoint、collective primitives。
- `source/src/sections/5__infrastructure.tex:8`：serving 支持高效低延迟 reasoning/generation。
- `source/src/sections/infrastructure/data.tex:3`：SILA 数据平台定义。
- `source/src/sections/infrastructure/data.tex:13`：Lance unified columnar data layer。
- `source/src/sections/infrastructure/data.tex:16`：fragment-level coordination 和 fault recovery。
- `source/src/sections/infrastructure/data.tex:19`：staged Ray execution。
- `source/src/sections/infrastructure/data.tex:22`：node-local model endpoints。
- `source/src/sections/infrastructure/data.tex:30`：SILA 将 startup latency 从 $30$--$60$ min 降到约 $5$ min，throughput 提升 $10\times$。
- `source/src/sections/infrastructure/training.tex:7`：data loader 功能、异步 worker、pinned-memory staging。
- `source/src/sections/infrastructure/training.tex:9`：HSDP + CP。
- `source/src/sections/infrastructure/training.tex:11`：TorchTitan-style training loop、optimizer/scheduler/loss、on-the-fly VAE。
- `source/src/sections/infrastructure/training.tex:13`：async checkpoint。
- `source/src/sections/infrastructure/training.tex:21`：data loader 三个要求。
- `source/src/sections/infrastructure/training.tex:34`：多模态 token 数差异导致 padding waste、rank imbalance、NCCL timeout。
- `source/src/sections/infrastructure/training.tex:36`：data loader 四个机制。
- `source/src/sections/infrastructure/training.tex:43`：token-budgeted packed sequences。
- `source/src/sections/infrastructure/training.tex:46`：joint data loader。
- `source/src/sections/infrastructure/training.tex:63`：rank-synchronous stream selection 和 $54\%$ throughput improvement。
- `source/src/sections/infrastructure/training.tex:67`：look-ahead packing 机制。
- `source/src/sections/infrastructure/training.tex:69`：look-ahead packing $8\%$ improvement。
- `source/src/sections/infrastructure/training.tex:74`：cold-start prewarm。
- `source/src/sections/infrastructure/training.tex:77`：data loader observability metrics。
- `source/src/sections/infrastructure/training.tex:81`：MoT attention 的两个 attention requirements。
- `source/src/sections/infrastructure/training.tex:83`：two-way flat attention 设计。
- `source/src/sections/infrastructure/training.tex:87`：two-way attention 相比 FlexAttention 提升 $22\%$。
- `source/src/sections/infrastructure/training.tex:91`：Hopper 用 FlashAttention-3，GB200 用 NATTEN。
- `source/src/sections/infrastructure/training.tex:95`：HSDP + CP 分布式训练。
- `source/src/sections/infrastructure/training.tex:99`：Ulysses CP 的 all-to-all 机制。
- `source/src/sections/infrastructure/training.tex:101`：CP 最大 degree 受 query heads 限制，Nano $32$、Super $64$。
- `source/src/sections/infrastructure/training.tex:105`：为什么不用 ring attention。
- `source/src/sections/infrastructure/training.tex:109`：标准 activation checkpointing 重算开销约 $33\%$。
- `source/src/sections/infrastructure/training.tex:111`：SAC 的 FLOPs-to-memory heuristic。
- `source/src/sections/infrastructure/training.tex:113`：SAC 吞吐提升 $13\%$。
- `source/src/sections/infrastructure/training.tex:117`：torch.compile 训练吞吐提升 $41\%$。
- `source/src/sections/infrastructure/training.tex:121`：VAE tokenizer 是 critical path。
- `source/src/sections/infrastructure/training.tex:125`：chunked encoding 的 $68/24/12$ frame operating points。
- `source/src/sections/infrastructure/training.tex:131`：VAE torch.compile 降低 encode latency $52\%$，$45$ graphs。
- `source/src/sections/infrastructure/training.tex:133`：AOTInductor sharded compile 从 $15$ min 到 $<1$ min。
- `source/src/sections/infrastructure/training.tex:137`：known frame-count specialization。
- `source/src/sections/infrastructure/training.tex:141`：async checkpoint 降低训练时间 $4\%/9\%$。
- `source/src/sections/infrastructure/training.tex:147`：save plan memorization 减少 checkpoint overhead $60\%$。
- `source/src/sections/infrastructure/training.tex:149`：object storage dedup/load 优化。
- `source/src/sections/infrastructure/training.tex:158`：Nano/Super steady-state throughput。
- `source/src/tables/training/training_throughput.tex:11`：Nano throughput 表格行。
- `source/src/tables/training/training_throughput.tex:12`：Super throughput 表格行。
- `source/src/tables/training/checkpointing.tex:15`：Nano async checkpointing 表格行。
- `source/src/tables/training/checkpointing.tex:16`：Super async checkpointing 表格行。
- `source/src/sections/infrastructure/serving.tex:4`：Reasoner 用 TensorRT-LLM/vLLM，Generator 用 vLLM-Omni，另有 PyTorch reference。
- `source/src/sections/infrastructure/serving.tex:12`：input preparation。
- `source/src/sections/infrastructure/serving.tex:13`：Reasoner autoregressive loop。
- `source/src/sections/infrastructure/serving.tex:14`：Generator diffusion loop。
- `source/src/sections/infrastructure/serving.tex:23`：torch compile + CUDA graphs serving speedup $30\%$--$60\%$。
- `source/src/sections/infrastructure/serving.tex:27`：inference CP。
- `source/src/sections/infrastructure/serving.tex:29`：CFG parallelism。
- `source/src/sections/infrastructure/serving.tex:33`：Reasoner tower caching。
- `source/src/sections/infrastructure/serving.tex:37`：inference batching 复用 variable-length sequence packing。
- `source/src/sections/infrastructure/serving.tex:39`：batching speedups 和 720p $B=1$ 限制。
- `source/src/sections/infrastructure/serving.tex:45`：prompt upsampling pipeline。
- `source/src/sections/infrastructure/serving.tex:53`：Reasoner 的 vLLM/TensorRT-LLM 集成复用 Qwen3-VL。
- `source/src/sections/infrastructure/serving.tex:59`：Generator 接入 vLLM-Omni。
- `source/src/sections/infrastructure/serving.tex:65`：Cache-DiT。
- `source/src/sections/infrastructure/serving.tex:67`：Ulysses context parallelism in vLLM-Omni。
- `source/src/sections/infrastructure/serving.tex:69`：CFG-Parallel。
- `source/src/sections/infrastructure/serving.tex:71`：HSDP serving。
- `source/src/sections/infrastructure/serving.tex:73`：CPU offload。
- `source/src/sections/infrastructure/serving.tex:75`：VAE-Patch-Parallel。
- `source/src/sections/infrastructure/serving.tex:77`：dynamic FP8 quantization。
- `source/src/tables/serving/batching.tex:19`：H100 batching speedup。
- `source/src/tables/serving/batching.tex:22`：GB200 batching speedup。
- `source/src/sections/4__training.tex:70`：Generator pre-training 使用 $1024/2048$ GB200 GPUs。
- `source/src/sections/4__training.tex:100`：Generator mid-training 使用 $1024/2048$ GB200 GPUs。
- `source/src/tables/training/training_throughput.tex:3`：training throughput 表说明 Nano/Super runs 使用 $2048/4096$ GB200 GPUs。

#### 源码依据

- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:7`：`dp_replicate * dp_shard == world_size`。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:8`：`cp` 和 `cfgp` 是 overlay axes。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:18`：`dp_mesh` 形状。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:19`：`cp_mesh`。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:20`：`cfgp_mesh`。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:25`：VLM training 使用 dp shard/replicate，cp/cfgp 为 $1$。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:26`：VFM training 使用 dp + optional cp。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:27`：VFM inference 使用 dp + cfgp/cp overlays。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:61`：CP size 配置。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:62`：CFG parallel size 配置。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:87`：`cfgp` 只能是 $1$ 或 $2$。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:89`：非 inference mode 禁止 `cfgp > 1`。
- `code/src/cosmos-framework-main/cosmos_framework/utils/vfm/parallelism.py:149`：build dp/cp/cfgp meshes。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:139`：CP 下 fetch/broadcast data。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:166`：CP ranks 中只有一个 owner rank 取数据。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:184`：CP group 内 broadcast data batch。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:209`：初始化 optimizer/scheduler/grad scaler。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:215`：load checkpoint。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:219`：分布式并行模式日志。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:265`：训练循环中 dataload。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:289`：执行 `training_step`。
- `code/src/cosmos-framework-main/cosmos_framework/trainer/__init__.py:307`：按迭代保存 checkpoint。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:508`：按 ratio 随机选 modality。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:510`：`seed + global_id` 保证所有 rank 同步选择。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:552`：计算 data probabilities。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:558`：每 iteration 构造 seeded RNG。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:591`：计算样本 token 数。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:593`：检查是否超过 max sequence length。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:608`：大样本临时放入 buffer，继续 look-ahead。
- `code/src/cosmos-framework-main/cosmos_framework/data/vfm/joint_dataloader.py:619`：把 skipped samples 放回 buffer。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2054`：`_run_classifier_free_guidance`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2076`：无 CFG parallel 时串行跑 cond/uncond。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2082`：读取 `cfgp_rank/cfgp_size/cfgp_group`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2087`：`cfgp_rank=0` 跑 conditional branch。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2090`：其他 rank 跑 unconditional branch。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2094`：用 P2P ops 交换 velocity。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2179`：`generate_samples_from_batch` 推理入口。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2211`：推理流程：sequence plan、encode condition、init noise、sampling loop。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2314`：CP 下同步 seed。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2317`：CFGP 下同步 seed。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2327`：prompt upsampling。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2393`：构造 per-step `velocity_fn`。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2430`：FSDP 对齐 CFG/control-CFG forward 数。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2492`：CFG velocity 组合。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2529`：运行 sampler。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2532`：UniPC sampler。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:2563`：EDM sampler。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:3760`：Reasoner AR generation 入口。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:3775`：Reasoner autoregressive text generation。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:3803`：Reasoner generation 只使用 und-pathway，bypass generation pathway。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:4056`：CP/CFGP group 内 broadcast 输出，统一各 rank 结果。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:4059`：prompt upsampling 入口。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:4092`：T2V/T2I text-only upsampling。
- `code/src/cosmos-framework-main/README.md:62`：公开 training recipes 是 $8$ GPU configs，测试在 $8\times$ H100 80GB。
- `code/src/cosmos-main/README.md:98`：支持 NVIDIA Ampere、Hopper、Blackwell GPU architectures。
- `code/src/cosmos-main/inference_benchmarks.md:18`：Reasoner benchmark 包含 RTX PRO 6000 Blackwell。
- `code/src/cosmos-main/inference_benchmarks.md:39`：Generator benchmark 比较 PyTorch、vLLM-Omni、Diffusers，并按 resolution / GPU / TP degree 报告。
- `code/src/cosmos-main/inference_benchmarks.md:45`：Nano T2V 表中 RTX PRO 6000 Blackwell latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:48`：Nano T2V 表中 H20 latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:51`：Nano T2V 表中 H100 NVL latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:54`：Nano T2V 表中 H200 NVL latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:57`：Nano T2V 表中 H100 80GB HBM3 latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:60`：Nano T2V 表中 H200 141GB HBM3 latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:63`：Nano T2V 表中 B200 latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:66`：Nano T2V 表中 B300 行。
- `code/src/cosmos-main/inference_benchmarks.md:140`：Super Generator benchmark 覆盖更窄，空单元格是 pending measurements。
- `code/src/cosmos-main/inference_benchmarks.md:146`：Super T2V 表中 RTX PRO 6000 Blackwell latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:152`：Super T2V 表中 H100 NVL latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:164`：Super T2V 表中 B200 latency 行。
- `code/src/cosmos-main/inference_benchmarks.md:239`：Nano Reasoner benchmark 指标定义，包含 TTFT、request latency、throughput。
- `code/src/cosmos-main/inference_benchmarks.md:241`：Nano Reasoner 使用 AIPerf，concurrency 为 $1/64/128/256$。
- `code/src/cosmos-main/inference_benchmarks.md:269`：Nano Reasoner RTX PRO 6000 Blackwell 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:311`：Nano Reasoner H20 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:353`：Nano Reasoner H100 NVL 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:395`：Nano Reasoner H200 NVL 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:437`：Nano Reasoner H100 80GB HBM3 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:479`：Nano Reasoner H200 141GB HBM3 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:521`：Nano Reasoner B200 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:563`：Nano Reasoner B300 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:587`：Super Reasoner benchmark 指标定义。
- `code/src/cosmos-main/inference_benchmarks.md:589`：Super Reasoner 空单元格表示未完成测量。
- `code/src/cosmos-main/inference_benchmarks.md:617`：Super Reasoner RTX PRO 6000 Blackwell 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:659`：Super Reasoner H20 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:701`：Super Reasoner H100 NVL 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:743`：Super Reasoner H200 NVL 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:785`：Super Reasoner H200 141GB HBM3 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:827`：Super Reasoner B200 代表 workload TTFT。
- `code/src/cosmos-main/inference_benchmarks.md:869`：Super Reasoner B300 代表 workload TTFT。
- `code/src/cosmos-framework-main/cosmos_framework/model/vfm/omni_mot_model.py:4096`：I2V image-conditioned upsampling。

---

### Q9. 自研多模态训推系统有开源吗？

#### 简短结论

有开源，但不是论文里所有生产级 infra 都完整开源。

已经开源的是 Cosmos 3 面向用户和研究者可运行的训练/推理框架，主要是：

$$
\text{Cosmos-Framework}
$$

它是一个 end-to-end framework，用于训练和 serving world models，包括 Cosmos3。官方 README 明确写了两块：

- Training：distributed FSDP / TP / CP / PP trainer，DCP checkpoint，HuggingFace `safetensors` import/export，JSONL / WebDataset / LeRobot dataset adapters，入口是 `cosmos_framework.scripts.train`。
- Inference：Diffusers / Transformers / vLLM backends，offline batch generation，online serving，入口是 `cosmos_framework.scripts.inference`。

本地源码位置：

```text
arxiv_2606_02800/code/src/cosmos-framework-main/
```

官方仓库：

```text
https://github.com/NVIDIA/cosmos-framework
```

Cosmos 主仓库也开源了模型使用、cookbook、vLLM-Omni / vLLM / Diffusers / Cosmos Framework 的集成示例：

```text
https://github.com/NVIDIA/Cosmos
```

#### 已开源的部分

从当前仓库看，开源内容包括：

| 模块 | 是否开源 | 说明 |
| --- | --- | --- |
| Cosmos model inference | 是 | `cosmos_framework.scripts.inference`，支持 Generator / Reasoner 多模式推理 |
| Cosmos SFT training framework | 是 | `cosmos_framework.scripts.train`，docs 里提供 supervised fine-tuning recipes |
| distributed trainer | 是 | 自研 trainer，支持 FSDP/CP 等并行配置 |
| DCP checkpoint 转换/保存/加载 | 是 | 支持 DCP 与 HuggingFace safetensors import/export |
| JSONL / WebDataset / LeRobot adapters | 是 | 用于训练数据接入 |
| action / vision / sound inference examples | 是 | 包括 forward dynamics、inverse dynamics、policy 等示例 |
| Diffusers / Transformers / vLLM shim packages | 是 | `packages/` 下提供生态集成 wrapper |
| vLLM-Omni production serving recipes | 部分在 vLLM-Omni 侧 | Cosmos 主仓库指向 vLLM-Omni recipes |

#### 不是完整开源或不能简单等同开源的部分

论文中讲的完整生产 infra 不应理解为全部开源，包括：

$$
\text{SILA}
$$

也就是论文里的 Scalable Infrastructure for Large-scale data processing and Annotation。它包含 Lance 数据层、fragment lease、Ray staged execution、node-local model endpoints、opportunistic cluster utilization、agentic orchestration 等。这些在论文里是 NVIDIA 内部大规模数据处理平台的设计描述；当前公开仓库里没有看到一个可直接部署的完整 SILA 平台实现。

同理，以下也不能认为完整开源：

- 论文级预训练生产 recipe：例如 $31.05$T / $17.86$T token 级别训练的完整数据、集群配置、调度和内部 recipes。
- 内部数据处理 pipelines：如大规模 captioning、AI judge、dedup、quality scoring、SDG 数据生成的全量生产脚本。
- 内部训练集和大部分 proprietary datasets。
- NVIDIA 内部 cluster orchestration、object store、monitoring dashboard、生产 Ray/Lance 作业配置。

#### 更准确的表述

可以这样说：

$$
\text{Open-sourced}
=
\text{model checkpoints}
+\text{inference code}
+\text{SFT/training framework}
+\text{examples/cookbooks}
+\text{some dataset adapters}
$$

但：

$$
\text{Not fully open-sourced}
=
\text{full production pretraining infra}
+\text{SILA implementation}
+\text{internal data curation pipelines}
+\text{full proprietary training data}
$$

所以如果你的问题是“能不能拿来做 Cosmos3 的 SFT、推理、forward dynamics / inverse dynamics / policy demo、接自己的数据做微调”，答案是：

$$
\text{可以}
$$

如果你的问题是“论文里 NVIDIA 用来从几十亿/几百亿候选样本构建数据、跑万卡级预训练的完整系统是否全部开源”，答案是：

$$
\text{没有证据表明完整开源}
$$

#### 本地源码依据

- `code/src/cosmos-framework-main/README.md:16`：说明 Cosmos-Framework 是训练和 serving world models 的 end-to-end framework。
- `code/src/cosmos-framework-main/README.md:18`：Training 支持 distributed FSDP / TP / CP / PP trainer、DCP checkpoint、JSONL / WebDataset / LeRobot adapters。
- `code/src/cosmos-framework-main/README.md:19`：Inference 支持 Diffusers / Transformers / vLLM backends、offline batch generation、online serving。
- `code/src/cosmos-framework-main/README.md:62`：公开 SFT recipes 是 8-GPU 配置，测试在 $8\times$ H100 80GB。
- `code/src/cosmos-framework-main/docs/training.md:24`：说明 fine-tune pre-trained Cosmos3 model on your own dataset using SFT。
- `code/src/cosmos-framework-main/docs/training.md:32`：runnable artifacts 在 `examples/`。
- `code/src/cosmos-main/README.md:611`：Generator research/model development 推荐 Diffusers。
- `code/src/cosmos-main/README.md:612`：Generator production inference 推荐 vLLM-Omni。
- `code/src/cosmos-main/README.md:616`：Runnable setup/training/evaluation 使用 Cosmos Framework。
- `code/src/cosmos-main/README.md:625`：Generator with Cosmos Framework notebook。
- `code/src/cosmos-main/README.md:627`：Forward dynamics with Cosmos Framework notebook。
- `code/src/cosmos-main/README.md:629`：Inverse dynamics with Cosmos Framework notebook。
- `code/src/cosmos-main/README.md:631`：Reasoner with Cosmos Framework notebook。

#### 官方链接

- `https://github.com/NVIDIA/cosmos-framework`
- `https://github.com/NVIDIA/Cosmos`

---

### Q10. 为了验证模型效果，paper 里提到了哪些 benchmark？

#### 总览

论文的效果验证覆盖两条主线：

$$
\text{Evaluation}
=
\text{Reasoner understanding benchmarks}
\cup
\text{Generator multimodal generation benchmarks}
$$

Reasoner 侧共评估：

$$
48\ \text{benchmarks}
=
19_{\text{general}}
+17_{\text{robotics}}
+9_{\text{smart infra}}
+3_{\text{driving}}
$$

Generator 侧覆盖：

$$
\text{T2I}
\cup
\text{T2V/I2V/V2V}
\cup
\text{Audio-Visual}
\cup
\text{Transfer/Control}
\cup
\text{Action/Policy}
$$

下面只列 benchmark / evaluation suite 清单，不展开每个分数。

#### 1. Reasoner benchmarks：多模态理解 / 推理

##### 1.1 General multimodal understanding

论文列了 $19$ 个 general benchmark：

| 能力方向 | Benchmark |
| --- | --- |
| broad VQA / multimodal understanding | MMBench-Dev |
| broad VQA / real-world scenes | RealWorldQA |
| diagram / scene understanding | AI2D |
| spatial / grounding / quantitative reasoning | CVBench |
| spatial reasoning | BlinkSpatial |
| depth reasoning | BlinkDepth |
| referring grounding | RefCOCO |
| counting | CountBenchQA |
| document understanding | DocVQA |
| infographic understanding | InfoVQA |
| OCR / scene text | OCRBench-v2 |
| video temporal understanding | MVBench |
| physical plausibility in video | VideoPhy2 |
| physical / causal video reasoning | MVPBench |
| cause-effect reasoning | CausalVQA |
| visual logic | LogicVista |
| expert multimodal reasoning | MMMU-Pro |
| hallucination resistance | HallusionBench |
| instruction following | IFBench |

##### 1.2 Robotics / embodied reasoning

论文列了 $17$ 个 robotics benchmark：

| 能力方向 | Benchmark |
| --- | --- |
| embodied commonsense | Cosmos-ER |
| embodied commonsense | Cosmos-CS |
| robot spatial grounding | RefSpatial |
| scene geometry / spatial intelligence | VSI-Bench |
| spatial planning / free-space reasoning | SparBench |
| robotic reasoning suite | RynnBrain-Area |
| robotic spatial reasoning | RynnBrain-Spatial |
| trajectory reasoning | RynnBrain-Trajectory |
| affordance reasoning | RynnBrain-Affordance |
| object-centric reasoning | RynnBrain-Object |
| grounding | RynnBrain-Grounding |
| multi-view / multi-frame embodied reasoning | MMSIBench |
| video embodied reasoning | MMSIVideoBench |
| operating-room understanding | HealthSurgiBench |
| embodied robotics QA | ERQA |
| home spatial reasoning | RoboSpatialHome |
| placement reasoning | Where2Place |

##### 1.3 Smart infrastructure

论文列了 $9$ 个 smart-infrastructure benchmark / subtasks：

| Benchmark / subtask | 评估内容 |
| --- | --- |
| VANTAGE-2DGrounding | $2$D grounding |
| VANTAGE-Astro2D | astrometric / spatial localization |
| VANTAGE-2DPointing | pointing |
| VANTAGE-DVC | dense video captioning |
| VANTAGE-EventVerif | event verification |
| VANTAGE-SOT | single-object tracking |
| VANTAGE-Temporal | temporal understanding |
| VANTAGE-VQA | visual question answering |
| TARBench | traffic anomaly reasoning |

其中 VANTAGE-Bench 覆盖 warehouse logistics、transportation、fixed-camera smart infrastructure；TAR 是 AI City Challenge 2026 Track 3 相关的 traffic anomaly reasoning suite。

##### 1.4 Driving

论文列了 $3$ 个 driving benchmark：

| Benchmark | 评估内容 |
| --- | --- |
| LingoQA | driving scene VQA / reasoning |
| AVSpecialCollisionBench | collision / near-collision / no-collision classification |
| AVSpecialStopBehaviorBench | stop-sign behavior classification |

#### 2. Image generation benchmarks：T2I

T2I 侧主要验证语义跟随、文字渲染、人类偏好和美学质量：

| Benchmark / metric | 评估内容 |
| --- | --- |
| UniGenBench | text-to-image semantic prompt following |
| UniGenBench-Phys | 论文新增的 Physical-AI prompt subset |
| CVTG-500L | English scene-text rendering，使用 GNED / PNED |
| CVTG-102ch | Chinese character rendering，使用 GNED / PNED |
| HPSv3 | prompt-aware human preference score |
| Aesthetic V2 / LAION aesthetic | prompt-independent visual aesthetics |
| Artificial Analysis Text-to-Image Leaderboard | crowdsourced public voting / real-world leaderboard |

对应论文里的聚合可以写成：

$$
\text{T2I eval}
=
\{\text{UniGenBench},\text{CVTG},\text{HPSv3},\text{AestheticV2},\text{ArtificialAnalysis}\}
$$

#### 3. Video generation benchmarks：T2V / I2V / V2V

视频生成侧覆盖 automated metrics、physics-specific benchmark 和 human evaluation：

| Benchmark | 模式 | 评估内容 |
| --- | --- | --- |
| PAIBench-G | T2V / I2V | Physical AI video generation，含 Quality Score / Domain Score |
| RBench | I2V | embodied robotics video generation，任务正确性和物理合理性 |
| Physics-IQ | I2V / V2V | physical outcome prediction / physical plausibility |
| Cosmos HUE | T2V / I2V | human evaluation，atomic binary verification |
| Human World Bench, HWB | I2V / egocentric | human motion, instruction following, physical plausibility |
| Artificial Analysis Image-to-Video Leaderboard | I2V | crowdsourced public voting / real-world leaderboard |

其中 PAIBench-G 覆盖六个 Physical AI domains：

$$
\{\text{Human},\text{Autonomous Vehicle},\text{Common Sense},\text{Robotics},\text{Physics},\text{Industry}\}
$$

RBench 覆盖：

$$
\text{task-oriented split}
\cup
\text{embodiment-specific split}
$$

Physics-IQ 覆盖五类物理现象：

$$
\{\text{solid mechanics},\text{fluid dynamics},\text{optics},\text{thermodynamics},\text{magnetism}\}
$$

#### 4. Audio-visual generation benchmarks

音频生成侧主要是 Cosmos-SoundBench：

| Benchmark / metric | 评估内容 |
| --- | --- |
| Cosmos-SoundBench | audio-visual prompt following and synchronization |
| AVQ | final audiovisual quality score |
| SAV | semantic audiovisual quality |
| SA | semantic audio correctness |
| AVAlign | audiovisual alignment |
| VisualSupport | prompt-critical visual support |
| audiobox-aesthetics PQ | low-level perceptual audio production quality |

论文中定义：

$$
\mathrm{SAV}
=
0.60\,\mathrm{SA}
+0.30\,\mathrm{AVAlign}
+0.10\,\mathrm{VisualSupport}
$$

以及：

$$
\mathrm{AVQ}
=
0.5\,\mathrm{SAV}
+0.5\,\mathrm{AQ}
$$

#### 5. Transfer / control generation benchmarks

控制生成侧主要验证 control fidelity、结构一致性和视频质量：

| Benchmark | Control type | Metrics |
| --- | --- | --- |
| PAIBench-C | blur / edge / segmentation / depth | Blur SSIM, Edge F1, Seg. mIoU, Depth si-RMSE, DOVER |
| AVBench-C | world-scenario-map driving control | ego drift, dynamic/static object matching, environment VLM judge, human video quality, lane-line fidelity |

PAIBench-C 包含：

$$
600\ \text{clips}
=
200_{\text{AgiBot}}
+200_{\text{OpenDV}}
+200_{\text{Ego-Exo-4D}}
$$

AVBench-C 包含：

$$
486\ \text{single-view driving clips}
$$

#### 6. Action / dynamics / policy benchmarks

Action 侧验证 forward dynamics、inverse dynamics、policy 三类能力：

| Benchmark / dataset | 模式 | Metrics |
| --- | --- | --- |
| in-house autonomous driving dataset | inverse dynamics, ID | RRE, RTE, ATE |
| internal camera-motion dataset | forward dynamics, FD | RRE, RTE, ATE |
| Human World Bench, HWB | egocentric FD | PSNR |
| DROID | robot FD | PSNR |
| RoboLab-120 | robot policy | task success rate |
| RoboArena | real-world robot policy | crowdsourced pairwise preference / leaderboard rating |
| LIBERO-10 | adaptation to new embodiment | closed-loop success rate |
| PushT | FD / ID / policy synergy ablation | ID MSE, FD PSNR, policy coverage |

动作相关指标可以概括为：

$$
\text{ID metrics}
=
\{\text{RRE},\text{RTE},\text{ATE},\text{MSE}\}
$$

$$
\text{FD metrics}
=
\{\text{PSNR},\text{trajectory consistency}\}
$$

$$
\text{Policy metrics}
=
\{\text{success rate},\text{coverage},\text{pairwise preference rating}\}
$$

#### 7. Ablation / analysis benchmarks

论文还用一些 benchmark 做训练和数据 ablation：

| Ablation | Evaluation benchmark / metric |
| --- | --- |
| SDG dataset ablation | PAIBench-G T2V |
| understanding tower initialization ablation | PAIBench T2V / I2V |
| audio pretraining ablation | PAIBench T2V / I2V |
| FPS control ablation | DOVER video quality, motion fidelity, composite score |
| action data synergy | FD PSNR, ID MSE, policy PSNR / MSE / coverage |
| LIBERO adaptation speed | LIBERO-10 success rate over post-training iterations |

#### 8. 一句话总结

如果只保留最核心的 benchmark 名称，可以写成：

$$
\boxed{
\begin{aligned}
\text{Reasoner} &: \text{48 benchmarks: MMBench, RealWorldQA, CVBench, DocVQA, MVBench, MMMU-Pro, VANTAGE, TAR, LingoQA, etc.}\\
\text{T2I} &: \text{UniGenBench, CVTG, HPSv3, AestheticV2, Artificial Analysis T2I}\\
\text{Video} &: \text{PAIBench-G, RBench, Physics-IQ, Cosmos HUE, HWB, Artificial Analysis I2V}\\
\text{Audio} &: \text{Cosmos-SoundBench}\\
\text{Transfer} &: \text{PAIBench-C, AVBench-C}\\
\text{Action/Policy} &: \text{DROID, RoboLab-120, RoboArena, LIBERO-10, PushT, HWB}
\end{aligned}
}
$$

#### 原文依据

- `source/src/sections/results/reasoner.tex:5`：Reasoner 共评估 $48$ 个 benchmarks，分为 general、robotics、smart infrastructure、driving。
- `source/src/sections/results/reasoner.tex:7`：General benchmarks 数量为 $19$。
- `source/src/sections/results/reasoner.tex:9`：MMBench-Dev、RealWorldQA、AI2D。
- `source/src/sections/results/reasoner.tex:10`：CVBench、BlinkSpatial、BlinkDepth、RefCOCO、CountBenchQA。
- `source/src/sections/results/reasoner.tex:12`：DocVQA、InfoVQA、OCRBench-v2。
- `source/src/sections/results/reasoner.tex:14`：MVBench、VideoPhy2、MVPBench、CausalVQA。
- `source/src/sections/results/reasoner.tex:16`：LogicVista、MMMU-Pro、HallusionBench、IFBench。
- `source/src/sections/results/reasoner.tex:21`：Robotics benchmarks 数量为 $17$。
- `source/src/sections/results/reasoner.tex:23`：Cosmos-ER、Cosmos-CS、ERQA、Where2Place。
- `source/src/sections/results/reasoner.tex:25`：RefSpatial、VSI-Bench、SparBench、RoboSpatialHome。
- `source/src/sections/results/reasoner.tex:27`：RynnBrain、ERQA。
- `source/src/sections/results/reasoner.tex:28`：MMSIVideoBench。
- `source/src/sections/results/reasoner.tex:29`：HealthSurgiBench。
- `source/src/sections/results/reasoner.tex:34`：VANTAGE-Bench、TAR。
- `source/src/sections/results/reasoner.tex:36`：LingoQA、AVSpecialCollisionBench、AVSpecialStopBehaviorBench。
- `source/src/tables/results/reasoner_benchmark_group.tex:19`：Reasoner 表格从 MMBench-Dev 开始列出 individual benchmarks。
- `source/src/sections/results/generator/image.tex:5`：T2I 评估四个轴：prompt following、scene text、human preference、aesthetics。
- `source/src/sections/results/generator/image.tex:13`：UniGenBench。
- `source/src/sections/results/generator/image.tex:15`：UniGenBench-Phys。
- `source/src/sections/results/generator/image.tex:19`：CVTG。
- `source/src/sections/results/generator/image.tex:21`：CVTG-500L、CVTG-102ch。
- `source/src/sections/results/generator/image.tex:25`：HPSv3。
- `source/src/sections/results/generator/image.tex:27`：Aesthetic V2。
- `source/src/sections/results/generator/image.tex:32`：Artificial Analysis T2I leaderboard。
- `source/src/sections/results/generator/video.tex:4`：Video evaluation 使用 PAIBench-G、RBench、Physics-IQ、Cosmos HUE、HWB。
- `source/src/sections/results/generator/video.tex:7`：PAIBench-G 定义和六个 domains。
- `source/src/sections/results/generator/video.tex:12`：RBench 定义。
- `source/src/sections/results/generator/video.tex:16`：Physics-IQ。
- `source/src/sections/results/generator/video.tex:34`：Cosmos HUE。
- `source/src/sections/results/generator/video.tex:40`：Human World Bench。
- `source/src/sections/results/generator/video.tex:56`：Artificial Analysis I2V leaderboard。
- `source/src/sections/results/generator/audio.tex:5`：Cosmos-SoundBench。
- `source/src/sections/results/generator/audio.tex:14`：SA、AVAlign、VisualSupport 和 SAV。
- `source/src/sections/results/generator/audio.tex:23`：AVQ 公式。
- `source/src/sections/results/generator/transfer.tex:10`：PAIBench-C。
- `source/src/sections/results/generator/transfer.tex:29`：AVBench-C。
- `source/src/sections/results/generator/action.tex:6`：action FD / ID benchmarks across camera motion、driving、robotics、egocentric motion。
- `source/src/sections/results/generator/action.tex:11`：action metrics RRE、RTE、ATE、PSNR、success rate。
- `source/src/sections/results/generator/action.tex:58`：DROID。
- `source/src/sections/results/generator/action.tex:70`：RoboLab、RoboArena。
- `source/src/sections/results/generator/action.tex:99`：LIBERO-10。
- `source/src/tables/results/sdg_ablation.tex:8`：SDG ablation evaluated on PAIBench-G T2V。
- `source/src/tables/appendix/training_ablations/understanding_tower.tex:7`：understanding tower ablation on PAIBench T2V / I2V。
- `source/src/tables/appendix/training_ablations/audio_pretraining.tex:3`：audio pretraining ablation on PAIBench T2V / I2V。
- `source/src/tables/results/fps_control_ablation.tex:5`：FPS control ablation metrics。
- `source/src/tables/results/action_pusht_synergy_open_loop.tex:3`：PushT action-mode synergy。

### Q11. 所谓“物理时间对齐”：几个模态的 TPS 都不同，具体怎么对齐？请配合代码给一个示例

#### 1. 结论

Cosmos 3 的物理时间对齐不是把 video/audio/action 重采样成相同 token 数，也不是要求不同模态在 sequence 里的 token index 相同；它做的是把每个模态自己的 token index 映射到同一个连续的 3D mRoPE temporal coordinate 系统里。

设某个模态的时间采样率为 $\operatorname{TPS}_m$，基准时间格为 $\operatorname{TPS}_{\mathrm{base}}$，第 $i$ 个 token 的共享时间坐标为：

$$
t_m(i)
=
o
+
\frac{i + \Delta_m}{\operatorname{TPS}_m}
\cdot
\operatorname{TPS}_{\mathrm{base}}
$$

其中：

$$
\operatorname{TPS}_m
=
\frac{\operatorname{fps}_m}{c_m}
$$

$$
\operatorname{TPS}_{\mathrm{base}}
=
\frac{\operatorname{base\_fps}}{c_{\mathrm{base}}}
$$

这里 $o$ 是该 generation block 的 temporal offset，$\Delta_m$ 是模态内的起始 frame offset，$c_m$ 是该模态的 temporal compression factor。对 Cosmos 3 默认 video latent 来说：

$$
\operatorname{base\_fps}=24,\qquad
c_{\mathrm{base}}=4,\qquad
\operatorname{TPS}_{\mathrm{base}}=6
$$

所以共享时间坐标可以理解为“以 $24$ FPS 视频经过 VAE temporal compression $4$ 后得到的 $6$ latent steps/s 作为统一时间尺”。不同模态的 TPS 不同，只会导致时间坐标步长不同：

$$
\Delta t_m
=
\frac{\operatorname{TPS}_{\mathrm{base}}}{\operatorname{TPS}_m}
$$

同一个物理时刻 $\tau$ 秒对应的不同模态 token 虽然 index 不同，但会落到相同或非常接近的 mRoPE temporal coordinate：

$$
t_m(\tau)
=
o + \tau \cdot \operatorname{TPS}_{\mathrm{base}}
$$

这就是论文里说的 physical temporal alignment / FPS modulation 的具体含义。

#### 2. 源码对应

核心实现在 `get_3d_mrope_ids_vae_tokens`：

```python
tps = fps / temporal_compression_factor
base_tps = base_fps / effective_base_tcf
frame_indices = torch.arange(grid_t, dtype=torch.float32)
scaled_t = (frame_indices + start_frame_offset) / tps * base_tps + temporal_offset
```

对应公式为：

$$
\operatorname{TPS}_m = \frac{\operatorname{fps}}{c_m}
$$

$$
t_m(i)
=
o
+
\frac{i+\Delta_m}{\operatorname{TPS}_m}
\cdot
\operatorname{TPS}_{\mathrm{base}}
$$

这里的代码没有把 `scaled_t` 立即取整，而是使用 `torch.float32` 位置：

```python
t_index = scaled_t.view(-1, 1).expand(-1, grid_h * grid_w).flatten()
t_dtype = torch.float32
mrope_ids = torch.stack([t_index, h_index.to(torch.float32), w_index.to(torch.float32)], dim=0)
```

因此 FPS modulation 下的 temporal position 可以是浮点数，例如 $0.24, 0.4, 1.5$。后续 mRoPE 直接基于这些 position id 计算旋转相位，而不是只支持整数帧号。

代码引用：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:535`：`get_3d_mrope_ids_vae_tokens` 入口。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:571`：计算 `tps = fps / temporal_compression_factor`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:573`：计算 `base_tps = base_fps / effective_base_tcf`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:575`：用真实时间比例生成 `scaled_t`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:594`：FPS modulation 开启时，mRoPE id 使用 `float32`。

#### 3. 不同模态如何共享同一个时间原点

sequence packing 时，文本之后会加一个较大的 modality margin，generation 模态从同一个 `vision_start_temporal_offset` 开始：

```python
packed_seq._mrope_temporal_offset += unified_3d_mrope_temporal_modality_margin
vision_start_temporal_offset = packed_seq._mrope_temporal_offset
```

然后普通 packing 路径里：

```python
action_temporal_offset=vision_start_temporal_offset
sound_temporal_offset=vision_start_temporal_offset
```

因此 video、action、sound/audio 的时间坐标共享同一个 generation 起点 $o$。文本和 generation 之间的 offset margin 只是为了把 AR text 区域和 diffusion generation 区域在位置空间里隔开，不改变 generation 内部 video/audio/action 的相对物理时间对齐。

公式化地说，generation block 内各模态使用同一个 $o$：

$$
t_{\mathrm{video}}(i)
=
o
+
\frac{i+\Delta_{\mathrm{video}}}{\operatorname{TPS}_{\mathrm{video}}}
\operatorname{TPS}_{\mathrm{base}}
$$

$$
t_{\mathrm{audio}}(j)
=
o
+
\frac{j+\Delta_{\mathrm{audio}}}{\operatorname{TPS}_{\mathrm{audio}}}
\operatorname{TPS}_{\mathrm{base}}
$$

$$
t_{\mathrm{action}}(k)
=
o
+
\frac{k+\Delta_{\mathrm{action}}}{\operatorname{TPS}_{\mathrm{action}}}
\operatorname{TPS}_{\mathrm{base}}
$$

当它们表示同一个物理时刻 $\tau$ 时：

$$
\frac{i+\Delta_{\mathrm{video}}}{\operatorname{TPS}_{\mathrm{video}}}
\approx
\frac{j+\Delta_{\mathrm{audio}}}{\operatorname{TPS}_{\mathrm{audio}}}
\approx
\frac{k+\Delta_{\mathrm{action}}}{\operatorname{TPS}_{\mathrm{action}}}
\approx
\tau
$$

于是：

$$
t_{\mathrm{video}}
\approx
t_{\mathrm{audio}}
\approx
t_{\mathrm{action}}
\approx
o + \tau \cdot \operatorname{TPS}_{\mathrm{base}}
$$

代码引用：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1367`：每个 sample 初始化 `_mrope_temporal_offset`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1386`：文本后增加 `unified_3d_mrope_temporal_modality_margin`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1388`：记录 `vision_start_temporal_offset`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1502`：action 使用 `action_temporal_offset=vision_start_temporal_offset`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1531`：sound 使用 `sound_temporal_offset=vision_start_temporal_offset`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:603`：默认 `unified_3d_mrope_temporal_modality_margin=15000`。

#### 4. 各模态的 TPS 进入方式

Video token 的 temporal grid 是 VAE latent grid，默认 temporal compression factor 为 $4$：

$$
\operatorname{TPS}_{\mathrm{video}}
=
\frac{\operatorname{fps}_{\mathrm{video}}}{4}
$$

代码里 vision packing 把真实 video fps 传入 `get_3d_mrope_ids_vae_tokens`：

```python
vision_mrope_ids, packed_seq._mrope_temporal_offset = get_3d_mrope_ids_vae_tokens(
    grid_t=latent_t,
    grid_h=patch_h,
    grid_w=patch_w,
    temporal_offset=packed_seq._mrope_temporal_offset,
    fps=effective_fps,
    base_fps=base_fps,
    temporal_compression_factor=temporal_compression_factor,
)
```

Action token 通常是每个 action step 一个 token，代码中使用：

$$
c_{\mathrm{action}}=1
$$

$$
\operatorname{TPS}_{\mathrm{action}}
=
\operatorname{fps}_{\mathrm{action}}
$$

普通 action packing 还设置：

$$
\Delta_{\mathrm{action}}=1
$$

对应代码：

```python
action_mrope_ids, _ = get_3d_mrope_ids_vae_tokens(
    grid_t=action_split_len,
    grid_h=1,
    grid_w=1,
    temporal_offset=action_temporal_offset,
    fps=effective_fps,
    base_fps=base_fps,
    temporal_compression_factor=1,
    base_temporal_compression_factor=base_temporal_compression_factor,
    start_frame_offset=1,
)
```

这个 `start_frame_offset=1` 表示普通 action 序列的第一个 action token 被放在视频起点之后的第一个 action step，而不是严格放在 $\tau=0$。如果 action 频率是 $15$ Hz，则第一个 action token 的物理时间约为：

$$
\tau_{\mathrm{action},0}
=
\frac{1}{15}
\operatorname{s}
$$

Audio/sound token 默认 latent fps 是 $25$，代码配置里为：

$$
\operatorname{fps}_{\mathrm{sound}}=25
$$

$$
c_{\mathrm{sound}}=1
$$

$$
\operatorname{TPS}_{\mathrm{sound}}=25
$$

sound packing 使用：

```python
sound_mrope_ids, _ = get_3d_mrope_ids_vae_tokens(
    grid_t=sound_split_len,
    grid_h=1,
    grid_w=1,
    temporal_offset=sound_temporal_offset,
    fps=effective_fps,
    base_fps=base_fps,
    temporal_compression_factor=1,
    start_frame_offset=0,
)
```

代码引用：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:949`：vision 启用 FPS modulation 后传入 `vision_fps`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:951`：vision 调用 `get_3d_mrope_ids_vae_tokens`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1027`：action 启用 mRoPE。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1037`：action 的 `temporal_compression_factor=1`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1039`：普通 action 的 `start_frame_offset=1`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1104`：sound 启用 mRoPE。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1114`：sound 的 `temporal_compression_factor=1`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1115`：sound 的 `start_frame_offset=0`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/transformer.py:620`：默认 `sound_latent_fps=25.0`。

#### 5. 数值示例：$24$ FPS video、$25$ Hz audio、$15$ Hz action 如何对齐

假设 generation block 的起始 temporal offset 为：

$$
o = 15000
$$

默认：

$$
\operatorname{TPS}_{\mathrm{base}} = \frac{24}{4}=6
$$

##### 5.1 Video：$24$ FPS，VAE temporal compression $4$

$$
\operatorname{TPS}_{\mathrm{video}}
=
\frac{24}{4}
=
6
$$

$$
\Delta t_{\mathrm{video}}
=
\frac{6}{6}
=
1
$$

所以 video latent index $i$ 的时间坐标是：

$$
t_{\mathrm{video}}(i)
=
15000 + i
$$

例如 $1$ 秒处的 video latent index 是：

$$
i = 1 \cdot 6 = 6
$$

$$
t_{\mathrm{video}}(6)
=
15006
$$

##### 5.2 Audio：$25$ Hz latent

$$
\operatorname{TPS}_{\mathrm{audio}}=25
$$

$$
\Delta t_{\mathrm{audio}}
=
\frac{6}{25}
=
0.24
$$

所以 audio token index $j$ 的时间坐标是：

$$
t_{\mathrm{audio}}(j)
=
15000 + 0.24j
$$

$1$ 秒处的 audio token index 是：

$$
j = 1 \cdot 25 = 25
$$

$$
t_{\mathrm{audio}}(25)
=
15000 + 0.24 \cdot 25
=
15006
$$

##### 5.3 Action：$15$ Hz，普通 packing 路径

普通 action packing 中：

$$
\operatorname{TPS}_{\mathrm{action}}=15
$$

$$
\Delta_{\mathrm{action}}=1
$$

$$
\Delta t_{\mathrm{action}}
=
\frac{6}{15}
=
0.4
$$

所以 action token index $k$ 的时间坐标是：

$$
t_{\mathrm{action}}(k)
=
15000 + 0.4(k+1)
$$

如果看 $1$ 秒处，则满足：

$$
\frac{k+1}{15}=1
$$

$$
k=14
$$

于是：

$$
t_{\mathrm{action}}(14)
=
15000 + 0.4 \cdot 15
=
15006
$$

这说明在普通 packing 路径里，$1$ 秒处对齐的是：

$$
\boxed{
t_{\mathrm{video}}(6)
=
t_{\mathrm{audio}}(25)
=
t_{\mathrm{action}}(14)
=
15006
}
$$

注意 action 的 index 是 $14$ 而不是 $15$，原因正是源码中的：

$$
\Delta_{\mathrm{action}}=1
$$

即 `start_frame_offset=1`。

##### 5.4 如果是 $60$ FPS video

对于 $60$ FPS video：

$$
\operatorname{TPS}_{\mathrm{video},60}
=
\frac{60}{4}
=
15
$$

$$
\Delta t_{\mathrm{video},60}
=
\frac{6}{15}
=
0.4
$$

于是：

$$
t_{\mathrm{video},60}(i)
=
15000 + 0.4i
$$

$1$ 秒处：

$$
i = 15
$$

$$
t_{\mathrm{video},60}(15)
=
15006
$$

因此 $60$ FPS video 的 latent token 更密，但它在 mRoPE temporal coordinate 上仍然和 $24$ FPS video、$25$ Hz audio、$15$ Hz action 对齐到同一个物理时刻。

#### 6. 最小可运行的伪代码示例

下面这段代码等价于源码中的时间坐标计算逻辑：

```python
def mrope_time_ids(num_tokens, fps, temporal_compression_factor, offset=15000,
                   base_fps=24, base_temporal_compression_factor=4,
                   start_frame_offset=0):
    tps = fps / temporal_compression_factor
    base_tps = base_fps / base_temporal_compression_factor
    return [
        offset + (i + start_frame_offset) / tps * base_tps
        for i in range(num_tokens)
    ]

video_24 = mrope_time_ids(12, fps=24, temporal_compression_factor=4)
audio_25 = mrope_time_ids(50, fps=25, temporal_compression_factor=1)
action_15 = mrope_time_ids(30, fps=15, temporal_compression_factor=1,
                           start_frame_offset=1)
video_60 = mrope_time_ids(30, fps=60, temporal_compression_factor=4)

print(video_24[6])   # 15006.0, 1 second
print(audio_25[25])  # 15006.0, 1 second
print(action_15[14]) # 15006.0, 1 second because start_frame_offset=1
print(video_60[15])  # 15006.0, 1 second
```

对应的物理时间关系为：

$$
\tau_{\mathrm{video24}}(6)
=
\frac{6}{6}
=
1
$$

$$
\tau_{\mathrm{audio25}}(25)
=
\frac{25}{25}
=
1
$$

$$
\tau_{\mathrm{action15}}(14)
=
\frac{14+1}{15}
=
1
$$

$$
\tau_{\mathrm{video60}}(15)
=
\frac{15}{15}
=
1
$$

它们映射到同一个 mRoPE temporal coordinate：

$$
o + 1 \cdot \operatorname{TPS}_{\mathrm{base}}
=
15000 + 6
=
15006
$$

#### 7. 和 attention 的关系

这种物理时间对齐只解决“位置编码相位是否表达同一物理时间”的问题；它不自动保证任意两个 token 都能互相 attend。token 是否可见仍由 attention mask / split packing 决定。

因此更准确的表述是：

$$
\text{physical time alignment}
\neq
\text{resampling}
\neq
\text{cross-modal attention permission}
$$

它的作用是：当 attention mask 允许跨模态交互时，video/audio/action 中同一物理时刻附近的 token 拥有一致的 temporal positional phase，从而让模型更容易学习同步关系，例如画面事件和声音、机器人动作和视觉状态之间的时序对应。

#### 原文依据

- `source/src/sections/4__training.tex:64`：论文说明使用 FPS modulation 来处理不同 physical temporal spacing。
- `source/src/sections/4__training.tex:65`：temporal axis of 3D MRoPE is assigned in proportion to real-world time rather than token index，并以 $24$ FPS 为基准。
- `source/src/sections/4__training.tex:81`：action、audio、control、video tokens share same temporal coordinate system。
- `source/src/sections/4__training.tex:145`：action policy operates at $15$ Hz。

---

### Q12. 模态内起始的 `frame_offset` 怎么理解？

#### 1. 先给结论

源码里的 `start_frame_offset` 不是 raw video frame 的编号，也不是把整段视频裁掉几帧；它是在某个模态自己的时间 token grid 上，对 token index 做一个起始相位偏移。

核心公式仍然是：

$$
t_m(i)
=
o
+
\frac{i+\Delta_m}{\operatorname{TPS}_m}
\cdot
\operatorname{TPS}_{\mathrm{base}}
$$

其中：

$$
i = \text{modality-local token index}
$$

$$
\Delta_m = \texttt{start\_frame\_offset}
$$

所以 `start_frame_offset` 的作用是让“该模态第 $0$ 个 token”不一定表示物理时间 $\tau=0$，而可以表示：

$$
\tau_{m,0}
=
\frac{\Delta_m}{\operatorname{TPS}_m}
$$

#### 2. 为什么 video/audio 通常是 $0$

对 video latent 来说，第 $0$ 个 video latent 通常就是 generation block 的起点：

$$
\Delta_{\mathrm{video}}=0
$$

所以：

$$
t_{\mathrm{video}}(0)
=
o
$$

对 audio/sound 来说，第 $0$ 个 sound token 也对应音频片段起点：

$$
\Delta_{\mathrm{audio}}=0
$$

所以：

$$
t_{\mathrm{audio}}(0)
=
o
$$

代码里 sound packing 明确传入：

```python
start_frame_offset=0
```

对应源码：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1115`：sound 的 `start_frame_offset=0`。

#### 3. 为什么普通 action packing 是 $1$

普通 action packing 中传入：

```python
start_frame_offset=1
```

这表示 action 的第 $0$ 个 token 不放在 generation 起点 $\tau=0$，而是放在第一个 action step 的时间位置：

$$
\tau_{\mathrm{action},0}
=
\frac{1}{\operatorname{TPS}_{\mathrm{action}}}
$$

如果 action 频率是 $15$ Hz：

$$
\operatorname{TPS}_{\mathrm{action}}=15
$$

$$
\tau_{\mathrm{action},0}
=
\frac{1}{15}\operatorname{s}
$$

对应的 mRoPE temporal coordinate 是：

$$
t_{\mathrm{action}}(0)
=
o
+
\frac{1}{15}
\cdot
6
=
o+0.4
$$

这背后的语义是：action token 通常表示“从当前观测状态出发的未来控制/未来动作”，而不是视频起点时刻已经发生的视觉状态本身。换句话说：

$$
x_0
\xrightarrow{a_0}
x_1
$$

这里 $a_0$ 更自然地和从 $x_0$ 到 $x_1$ 的未来时间步相关，而不是和 $x_0$ 的同一瞬间完全重合。因此实现上把普通 action 的第一个 token 放到起点之后的一个 action step。

源码对应：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1029`：action 调用 `get_3d_mrope_ids_vae_tokens`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1037`：action 使用 `temporal_compression_factor=1`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1039`：普通 action 使用 `start_frame_offset=1`。

#### 4. 一个更直观的例子

假设：

$$
o=15000,\qquad
\operatorname{TPS}_{\mathrm{base}}=6,\qquad
\operatorname{TPS}_{\mathrm{action}}=15
$$

如果不加 offset：

$$
t_{\mathrm{action}}(0)
=
15000
$$

这会把 action 第 $0$ 个 token 和 video 第 $0$ 个 latent、audio 第 $0$ 个 token 放在完全同一时刻。

但源码实际使用：

$$
\Delta_{\mathrm{action}}=1
$$

所以：

$$
t_{\mathrm{action}}(0)
=
15000
+
\frac{0+1}{15}
\cdot
6
=
15000.4
$$

action 第 $14$ 个 token 才对应 $1$ 秒：

$$
t_{\mathrm{action}}(14)
=
15000
+
\frac{14+1}{15}
\cdot
6
=
15006
$$

而 video/audio 在 $1$ 秒处分别是：

$$
t_{\mathrm{video24}}(6)
=
15000
+
\frac{6}{6}
\cdot
6
=
15006
$$

$$
t_{\mathrm{audio25}}(25)
=
15000
+
\frac{25}{25}
\cdot
6
=
15006
$$

因此：

$$
\boxed{
t_{\mathrm{video24}}(6)
=
t_{\mathrm{audio25}}(25)
=
t_{\mathrm{action15}}(14)
=
15006
}
$$

#### 5. supertoken temporal-causal 路径里的特殊处理

在 `video_temporal_causal=True` 的 supertoken packing 里，源码还做了更细的 action 对齐：

```python
if latent_t > 1:
    null_ids_3d = null_ids.reshape(3, 1, tcf)
    real_ids_3d = _real_action_ids(latent_t - 1, start_frame_offset=1)
    action_ids_3d = torch.cat([null_ids_3d, real_ids_3d], dim=1)
elif input_action_tokens is None:
    action_ids_3d = null_ids.reshape(3, 1, tcf)
else:
    action_ids_3d = _real_action_ids(1, start_frame_offset=0)
```

这里的含义是：

- 当有多帧 video latent 时，第一个 video latent 对应起点状态，前面配一个 `null action` 占位；真实 action 从下一步开始，所以 `start_frame_offset=1`。
- 当只有一帧且真的有 action token 时，源码允许 `start_frame_offset=0`，因为这时没有完整的“首帧状态 + 后续帧转移”结构，需要按当前单帧 case 处理。

公式上，多帧 temporal-causal case 更接近：

$$
\text{frame }0:\quad x_0,\ \text{null action}
$$

$$
\text{frame }1:\quad x_1,\ a_0
$$

$$
\text{frame }2:\quad x_2,\ a_1
$$

也就是说，action token 被看作驱动状态转移的控制量，因此它在时间位置上天然比初始视觉状态晚一步。

源码对应：

- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1224`：supertoken 路径中 `_real_action_ids` 接收 `start_frame_offset`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1235`：传入 `start_frame_offset`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1241`：多帧时真实 action 使用 `start_frame_offset=1`。
- `code/src/cosmos-framework-main/packages/diffusers-cosmos3/diffusers_cosmos3/sequence_packing.py:1246`：单帧且有 action 时使用 `start_frame_offset=0`。

#### 6. 最容易误解的一点

`start_frame_offset=1` 不是说 action 延迟了一个 raw video frame。它延迟的是一个 action-token 时间步：

$$
\Delta \tau
=
\frac{1}{\operatorname{TPS}_{\mathrm{action}}}
$$

当 $\operatorname{TPS}_{\mathrm{action}}=15$ 时：

$$
\Delta \tau
=
\frac{1}{15}\operatorname{s}
$$

当某个模态是 video latent 且 $\operatorname{TPS}_{\mathrm{video}}=6$ 时，如果设置 $\Delta_{\mathrm{video}}=1$，那才表示偏移一个 video latent step：

$$
\Delta \tau
=
\frac{1}{6}\operatorname{s}
$$

所以 `start_frame_offset` 的单位不是统一的 raw frame，而是“当前模态的时间 token index 单位”。真正统一到物理时间，是通过：

$$
\frac{i+\Delta_m}{\operatorname{TPS}_m}
$$

这一步完成的。
