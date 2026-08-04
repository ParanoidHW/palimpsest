# Research Paper 与领域覆盖矩阵

本矩阵是 literature survey、paper deep review 和 research synthesis 的**前置查重入口**。它回答两件事：

1. 哪些研究领域/子领域已经有正式 Survey 或 Paper；
2. 某篇论文是否已经完成 canonical 分析，应当复用、链接或增量更新，而不是重新生成一份。

> 快照日期：2026-07-31。当前共登记 9 个正式 paper domain、84 篇 canonical Paper。
>
> 作者机构元数据：`84/84` 已按论文 PDF 标题页、机构编号和角色脚注核验（2026-07-31）。其中 75 篇为个人作者署名，记录首位列名作者、明确共同一作、明确通讯作者/联系人与去重机构；9 篇为机构署名，仅记录署名机构。未披露字段保持“无法核验”，不按邮箱域名或外部履历推断。
>
> Obsidian 元数据：`84/84` canonical Paper 已加入统一 YAML Properties（2026-07-31）。每篇均有 `paper`、collection、domain、`status/deep-review` 四项共同层级标签，以及各一项 `topic/*`、`method/*`；独立属性保留文档类型、canonical 状态和集合归属。12 篇 ICML 2026 Paper 先行试验，确认 schema 后推广到其余 Paper。

## 使用规则

开始检索或派发单篇精读前：

1. 先在本矩阵按论文标题、简称、arXiv ID、模型名和常见别名查找。
2. 命中 canonical Paper 时，优先读取现有正文、修订信息、上位 Survey 和 evidence/figure inventory。
3. 证据版本一致且结论仍适用：采用 `link-only` 或直接复用，不重复精读、复制资产或创建第二个 slug。
4. 论文/source/code/checkpoint 有新版本，或现有文档缺关键字段：采用 `evidence-update` / `content-update`，在原 canonical Paper 追加修订。
5. 只有确认未覆盖，或现有内容明确只是短 note 且任务要求完整精读时，才创建新的 Paper。
6. 正式发布、迁移、合并或删除 Paper 后，同步更新本矩阵；domain 内容与 meta 变更分开提交。

### 状态标签

| 标签 | 含义 | 默认动作 |
|---|---|---|
| `深度精读` | versioned canonical Paper，通常含证据、局限与父级 Survey | 复用或增量更新 |
| `Paper note` | canonical Paper 已存在，但未见统一修订元数据或内容较短 | 先读取；必要时原位补全 |
| `待修链路` | Paper 已分析，但父级 Survey/Index 反链不完整 | 不重复分析；优先修链 |
| `未覆盖` | 本矩阵没有命中 | 才进入新建评审流程 |

## 领域覆盖总览

| Domain / 子领域 | 已分析 Paper | 主要覆盖 | 当前汇总入口 | 维护判断 |
|---|---:|---|---|---|
| `01_ai_infra/parallelism` | 6 | DP/TP/EP/PP/SP/CP/CFGP、状态切分、通信开销与定制切分 | [Parallel partitioning taxonomy](../01_ai_infra/parallelism/surveys/parallel-partitioning-taxonomy.md) | 首版方法体系、选型、定制切分与六篇基础 Paper 已落盘；跨域系统案例采用 `link-only` |
| `01_ai_infra/kernel/custom_attn` | 20 | LLM/VLM 与视频 diffusion 的 mask、selector、layout、kernel、量化、并行 | [Video generation sparse attention](../01_ai_infra/kernel/custom_attn/surveys/video-generation-sparse-attention.md) | 已形成跨算法—系统专题精读簇 |
| `02_model_systems/ICML/2026` | 12 | diffusion/latent LM、speculative decoding、MoE/压缩、3D/多模态 | [ICML 2026 selected papers](../02_model_systems/ICML/2026/surveys/icml-2026-selected-papers.md) | 会议批次已覆盖 |
| `02_model_systems/diffusion` | 1 | language diffusion 与 AR/diffusion/self-speculative 统一 | [Language diffusion serving](../02_model_systems/diffusion/surveys/language-diffusion-serving.md) | 单篇锚点，可继续扩展 |
| `02_model_systems/embodied_ai` | 13 | VLA、导航、操作策略、world model、3D/4D perception、数据合成 | [Embodied AI evolution](../02_model_systems/embodied_ai/surveys/embodied-ai-evolution-infra.md) | 核心谱系已覆盖 |
| `02_model_systems/llm_foundations` | 2 | frontier LLM 架构、规模与 Infra | [2026 H1 model scale](../02_model_systems/llm_foundations/surveys/2026h1-model-scale.md) | Kimi K3 父级链路需复核 |
| `02_model_systems/multimodal_generation` | 19 | image/video diffusion、AR/flow、MoT、VAE、cache、稀疏 attention、serving | [Visual generation landscape](../02_model_systems/multimodal_generation/surveys/visual-generation-model-landscape.md) | Sparse VideoGen 方法族与 Jenga pipeline 已覆盖 |
| `02_model_systems/speculative_decoding` | 9 | diffusion draft、tree/parallel drafting、解耦 local correction、workload-aware drafting、hidden-state training、serving | [Evolution](../02_model_systems/speculative_decoding/surveys/evolution.md) | 近期系统分支已覆盖 |
| `03_agentic_workflows/kernel_agents` | 4 | LLM 自动 kernel 生成、Ascend/NPU、test-time scaling | [Paper index](../03_agentic_workflows/kernel_agents/evidence/paper-index.md) | 当前为 Paper note，适合按需补全 |

## Paper 明细

### Parallelism（6）

| Paper | 状态 | Canonical |
|---|---|---|
| Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism（arXiv:1909.08053） | 深度精读 | [megatron-lm](../01_ai_infra/parallelism/papers/megatron-lm.md) |
| GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism（arXiv:1811.06965） | 深度精读；代码快照受限 | [gpipe](../01_ai_infra/parallelism/papers/gpipe.md) |
| ZeRO: Memory Optimizations Toward Training Trillion Parameter Models（arXiv:1910.02054） | 深度精读；现代代码快照受限 | [zero](../01_ai_infra/parallelism/papers/zero.md) |
| GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding（arXiv:2006.16668） | 深度精读；OpenReview 受限 | [gshard](../01_ai_infra/parallelism/papers/gshard.md) |
| DeepSpeed Ulysses: System Optimizations for Enabling Training of Extreme Long Sequence Transformer Models（arXiv:2309.14509） | 深度精读；复合收益归因受限 | [deepspeed-ulysses](../01_ai_infra/parallelism/papers/deepspeed-ulysses.md) |
| Ring Attention with Blockwise Transformers for Near-Infinite Context（arXiv:2310.01889） | 深度精读；OpenReview 受限 | [ring-attention](../01_ai_infra/parallelism/papers/ring-attention.md) |

### Custom attention（20）

| Paper | 状态 | Canonical |
|---|---|---|
| FlexAttention for Efficient High-Resolution Vision-Language Models | 深度精读 | [flexattention-vlm](../01_ai_infra/kernel/custom_attn/papers/flexattention-vlm.md) |
| FrameDiT / FrameDiT editing | 深度精读 | [framedit](../01_ai_infra/kernel/custom_attn/papers/framedit.md) |
| HASTE | 深度精读 | [haste](../01_ai_infra/kernel/custom_attn/papers/haste.md) |
| LVSA | 深度精读 | [lvsa](../01_ai_infra/kernel/custom_attn/papers/lvsa.md) |
| MInference 1.0 | 深度精读 | [minference](../01_ai_infra/kernel/custom_attn/papers/minference.md) |
| Token Sparse Attention | 深度精读 | [token-sparse-attention](../01_ai_infra/kernel/custom_attn/papers/token-sparse-attention.md) |
| VMoBA | 深度精读 | [vmoba](../01_ai_infra/kernel/custom_attn/papers/vmoba.md) |
| Accelerating Text-to-Video Generation with Calibrated Sparse Attention（CalibAtt；arXiv:2603.05503） | 深度精读 | [calibatt](../01_ai_infra/kernel/custom_attn/papers/calibatt.md) |
| Fast Video Generation with Sliding Tile Attention（STA；arXiv:2502.04507） | 深度精读 | [sliding-tile-attention](../01_ai_infra/kernel/custom_attn/papers/sliding-tile-attention.md) |
| XAttention: Block Sparse Attention with Antidiagonal Scoring（arXiv:2503.16428） | 深度精读 | [xattention](../01_ai_infra/kernel/custom_attn/papers/xattention.md) |
| VSA: Faster Video Diffusion with Trainable Sparse Attention（arXiv:2505.13389） | 深度精读 | [vsa](../01_ai_infra/kernel/custom_attn/papers/vsa.md) |
| DSV: Exploiting Dynamic Sparsity to Accelerate Large-Scale Video DiT Training（arXiv:2502.07590） | 深度精读 | [dsv](../01_ai_infra/kernel/custom_attn/papers/dsv.md) |
| FPSAttention（arXiv:2506.04648） | 深度精读 | [fpsattention](../01_ai_infra/kernel/custom_attn/papers/fpsattention.md) |
| SpargeAttn / SpargeAttention（arXiv:2502.18137） | 深度精读 | [spargeattn](../01_ai_infra/kernel/custom_attn/papers/spargeattn.md) |
| Training-free and Adaptive Sparse Attention for Efficient Long Video Generation（AdaSpa；arXiv:2502.21079） | 深度精读 | [adaspa](../01_ai_infra/kernel/custom_attn/papers/adaspa.md) |
| PAROAttention: Pattern-Aware ReOrdering for Efficient Sparse and Quantized Attention（arXiv:2506.16054；OpenReview UPELg2oUo3） | 深度精读 | [paroattention](../01_ai_infra/kernel/custom_attn/papers/paroattention.md) |
| VMonarch / Video Monarch Attention（arXiv:2601.22275） | 深度精读 | [vmonarch](../01_ai_infra/kernel/custom_attn/papers/vmonarch.md) |
| VORTA: Efficient Video Diffusion via Routing Sparse Attention（arXiv:2505.18809） | 深度精读 | [vorta](../01_ai_infra/kernel/custom_attn/papers/vorta.md) |
| RainFusion: Adaptive Video Generation Acceleration via Multi-Dimensional Visual Redundancy（arXiv:2505.21036） | 深度精读 | [rainfusion](../01_ai_infra/kernel/custom_attn/papers/rainfusion.md) |
| RainFusion2.0: Temporal-Spatial Awareness and Hardware-Efficient Block-wise Sparse Attention（arXiv:2512.24086；extends RainFusion） | 深度精读 | [rainfusion-2](../01_ai_infra/kernel/custom_attn/papers/rainfusion-2.md) |

### ICML 2026 selected papers（12）

> Obsidian Properties 首批试验：本组 `12/12` canonical Paper 于 2026-07-30 先行加入统一 YAML 属性、共同层级标签及逐篇 `topic/*`、`method/*` 标签；该 schema 已于 2026-07-31 推广至覆盖矩阵全部 Paper。本题单身份仍不等于正式 ICML 2026 接收状态。

| Paper | 状态 | Canonical |
|---|---|---|
| DODO | 深度精读 | [dodo](../02_model_systems/ICML/2026/papers/dodo.md) |
| Dual-Latent Memory Routing | 深度精读 | [dual-latent-memory-routing](../02_model_systems/ICML/2026/papers/dual-latent-memory-routing.md) |
| ECHO | 深度精读 | [echo](../02_model_systems/ICML/2026/papers/echo.md) |
| Flex-Forcing | 深度精读 | [flex-forcing](../02_model_systems/ICML/2026/papers/flex-forcing.md) |
| Multimodal Latent Language Modeling | 深度精读 | [latentlm](../02_model_systems/ICML/2026/papers/latentlm.md) |
| LiME | 深度精读 | [lime](../02_model_systems/ICML/2026/papers/lime.md) |
| Multi-Token Prediction via Self-Distillation | 深度精读 | [multi-token-self-distillation](../02_model_systems/ICML/2026/papers/multi-token-self-distillation.md) |
| OmniFit | 深度精读 | [omnifit-layer-compression](../02_model_systems/ICML/2026/papers/omnifit-layer-compression.md) |
| OnlineSPEC | 深度精读 | [onlinespec](../02_model_systems/ICML/2026/papers/onlinespec.md) |
| SelfJudge | 深度精读 | [selfjudge](../02_model_systems/ICML/2026/papers/selfjudge.md) |
| SplAttN | 深度精读 | [splattn](../02_model_systems/ICML/2026/papers/splattn.md) |
| XDLM | 深度精读 | [xdlm](../02_model_systems/ICML/2026/papers/xdlm.md) |

### Language diffusion（1）

| Paper | 状态 | Canonical |
|---|---|---|
| Nemotron-Labs-Diffusion | 深度精读 | [nemotron-labs-diffusion](../02_model_systems/diffusion/papers/nemotron-labs-diffusion.md) |

### Embodied AI（13）

| Paper | 状态 | Canonical |
|---|---|---|
| ACT | 深度精读 | [act](../02_model_systems/embodied_ai/papers/act.md) |
| Cosmos World Foundation Model | 深度精读 | [cosmos-world-foundation-model](../02_model_systems/embodied_ai/papers/cosmos-world-foundation-model.md) |
| Diffusion Policy | 深度精读 | [diffusion-policy](../02_model_systems/embodied_ai/papers/diffusion-policy.md) |
| EmbodiedScan | 深度精读 | [embodiedscan](../02_model_systems/embodied_ai/papers/embodiedscan.md) |
| Genie | 深度精读 | [genie](../02_model_systems/embodied_ai/papers/genie.md) |
| MotuBrain | 深度精读 | [motubrain](../02_model_systems/embodied_ai/papers/motubrain.md) |
| NaVILA | 深度精读 | [navila](../02_model_systems/embodied_ai/papers/navila.md) |
| OpenVLA | 深度精读 | [openvla](../02_model_systems/embodied_ai/papers/openvla.md) |
| RT-2 | 深度精读 | [rt-2](../02_model_systems/embodied_ai/papers/rt-2.md) |
| VGGT | 深度精读 | [vggt](../02_model_systems/embodied_ai/papers/vggt.md) |
| VLFM | 深度精读 | [vlfm](../02_model_systems/embodied_ai/papers/vlfm.md) |
| WAM4D | 深度精读 | [wam4d](../02_model_systems/embodied_ai/papers/wam4d.md) |
| Xiaomi-Robotics-U0 | 深度精读 | [xiaomi-robotics-u0](../02_model_systems/embodied_ai/papers/xiaomi-robotics-u0.md) |

### LLM foundations（2）

| Paper | 状态 | Canonical |
|---|---|---|
| DeepSeek-V4 | 深度精读 | [deepseek-v4](../02_model_systems/llm_foundations/papers/deepseek-v4.md) |
| Kimi K3 | 深度精读；待修链路 | [kimi-k3](../02_model_systems/llm_foundations/papers/kimi-k3.md) |

### Multimodal generation（19）

| Paper | 状态 | Canonical |
|---|---|---|
| BAGEL | 深度精读；近半年 Survey 已复用 | [bagel](../02_model_systems/multimodal_generation/papers/bagel.md) |
| Causal-rCM | 深度精读 | [causal-rcm](../02_model_systems/multimodal_generation/papers/causal-rcm.md) |
| Cosmos 3 | 深度精读；近半年 Survey 已复用 | [cosmos-3](../02_model_systems/multimodal_generation/papers/cosmos-3.md) |
| DC-AE | 深度精读 | [dcae](../02_model_systems/multimodal_generation/papers/dcae.md) |
| DiT | 深度精读 | [dit](../02_model_systems/multimodal_generation/papers/dit.md) |
| FEB-Cache | 深度精读 | [feb-cache](../02_model_systems/multimodal_generation/papers/feb-cache.md) |
| Helios | 深度精读 | [helios](../02_model_systems/multimodal_generation/papers/helios.md) |
| HunyuanVideo 1.5 | 深度精读 | [hunyuanvideo-1-5](../02_model_systems/multimodal_generation/papers/hunyuanvideo-1-5.md) |
| LDM | 深度精读 | [ldm](../02_model_systems/multimodal_generation/papers/ldm.md) |
| MAGI-1 | 深度精读 | [magi-1](../02_model_systems/multimodal_generation/papers/magi-1.md) |
| PixelDiT | 深度精读 | [pixeldit](../02_model_systems/multimodal_generation/papers/pixeldit.md) |
| Qwen-Image-2.0 | 深度精读 | [qwen-image-2-0](../02_model_systems/multimodal_generation/papers/qwen-image-2-0.md) |
| SANA-Video 2.0 | 深度精读 | [sana-video-2](../02_model_systems/multimodal_generation/papers/sana-video-2.md) |
| Sparse VideoGen | 深度精读 | [sparse-videogen](../02_model_systems/multimodal_generation/papers/sparse-videogen.md) |
| Sparse VideoGen2: Accelerate Video Generation with Sparse Attention via Semantic-Aware Permutation（SVG2；arXiv:2505.18875） | 深度精读 | [sparse-videogen2](../02_model_systems/multimodal_generation/papers/sparse-videogen2.md) |
| Training-Free Efficient Video Generation via Dynamic Token Carving（Jenga；TokenCarve；arXiv:2505.16864） | 深度精读；单一 canonical 条目 | [jenga](../02_model_systems/multimodal_generation/papers/jenga.md) |
| SwiftFusion | 深度精读 | [swiftfusion](../02_model_systems/multimodal_generation/papers/swiftfusion.md) |
| Transfusion | 深度精读 | [transfusion](../02_model_systems/multimodal_generation/papers/transfusion.md) |
| Vega | 深度精读 | [vega](../02_model_systems/multimodal_generation/papers/vega.md) |

### Speculative decoding（7）

| Paper | 状态 | Canonical |
|---|---|---|
| D²SD | 深度精读 | [d2sd](../02_model_systems/speculative_decoding/papers/d2sd.md) |
| DFlash | 深度精读 | [dflash](../02_model_systems/speculative_decoding/papers/dflash.md) |
| DeLS-Spec / arXiv:2607.07409 | 深度精读；首轮协同与下标映射已澄清 | [dels-spec](../02_model_systems/speculative_decoding/papers/dels-spec.md) |
| DSpark | 深度精读 | [dspark](../02_model_systems/speculative_decoding/papers/dspark.md) |
| HyperDFlash | 深度精读 | [hyperdflash](../02_model_systems/speculative_decoding/papers/hyperdflash.md) |
| JetSpec | 深度精读 | [jetspec](../02_model_systems/speculative_decoding/papers/jetspec.md) |
| P-EAGLE | 深度精读 | [p-eagle](../02_model_systems/speculative_decoding/papers/p-eagle.md) |
| AngelSpec / arXiv:2607.25852 | 深度精读 | [angelspec](../02_model_systems/speculative_decoding/papers/angelspec.md) |
| TorchSpec / PyTorch Blog 2026-03-19 | 深度精读；技术博客与代码系统 | [torchspec](../02_model_systems/speculative_decoding/papers/torchspec.md) |

### Kernel agents（4）

| Paper | 状态 | Canonical |
|---|---|---|
| AscendCraft | Paper note | [ascend-craft](../03_agentic_workflows/kernel_agents/papers/ascend-craft.md) |
| AscendKernelGen | Paper note | [ascend-kernel-gen](../03_agentic_workflows/kernel_agents/papers/ascend-kernel-gen.md) |
| s1: Simple test-time scaling | Paper note | [s1-test-time-scaling](../03_agentic_workflows/kernel_agents/papers/s1-test-time-scaling.md) |
| Towards Automated Kernel Generation | Paper note | [towards-automated-kernel-generation](../03_agentic_workflows/kernel_agents/papers/towards-automated-kernel-generation.md) |

## 维护审计

更新本文件时至少检查：

- `rg --files | rg '(^|/)papers/[^/]+\.md$' | rg -v '^(_artifacts|99_references)/'` 的结果与明细表一一对应；
- domain 汇总计数等于明细行数；
- 每条 canonical 链接可解析；
- 新 Paper 的状态、父级 Survey/Index 和资产 owner 已确认；
- rename/合并后旧 slug 不再残留；
- 本文件只登记正式知识，不登记 `_artifacts` 内的临时 review package。
