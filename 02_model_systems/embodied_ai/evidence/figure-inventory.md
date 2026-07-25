# 具身智能正式图表清单

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[具身智能模型演进、Infra 与端云协同](../surveys/embodied-ai-evolution-infra.md)
> - 证据资产：`../assets/papers/<paper-slug>/`
> - 相关文档：[论文索引](paper-index.md)

下列 30 个文件均为原论文 PDF 中的单一编号 Figure/Table 裁剪。坐标使用源页面像素的左上角原点，格式为 `(x, y, width, height)`；caption 是完整中文转述，保持原意。所有文件先经 contact-sheet 初筛，再按表中源分辨率逐图检查；contact sheet 和裁剪过程保留在审计区，不进入正式目录。

## ACT

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 4 | PDF p.4，`1700×2200`；`(125,145,1450,475)` | “Architecture of Action Chunking with Transformers (ACT). We train ACT as a Conditional VAE (CVAE), which has an encoder and a decoder. Left: The encoder of the CVAE compresses action sequence and joint observation into z, the style variable. The encoder is discarded at test time. Right: The decoder or policy of ACT synthesizes images from multiple viewpoints, joint positions, and z with a transformer encoder, and predicts a sequence of actions with a transformer decoder. z is simply set to the mean of the prior (i.e. zero) at test time.” | [asset](../assets/papers/act/fig4-act-architecture-caption.png)；支撑[模型/系统架构](../papers/act.md#43-模型系统架构)。 | passed：单一 Figure 4、完整 caption，contact-sheet + `1450×475` 原分辨率 QA。 |
| Figure 8 | PDF p.10，`1700×2200`；`(125,8,1565,660)` | “(a) We augment two baselines with action chunking, with different values of chunk size k on the x-axis, and success rate on the y-axis. Both methods significantly benefit from action chunking, suggesting that it is a generally useful technique. (b) Temporal Ensemble (TE) improves our method and BC-ConvMLP, while hurting VINN. (c) We compare with and without the CVAE training, showing that it is crucial when learning from human data. (d) We plot the distribution of task completion time in our user study, where we task participants to perform two tasks, at 5Hz or 50Hz teleoperation frequency. Lowering the frequency results in a 62% slowdown in completion time.” | [asset](../assets/papers/act/fig8-ablation-user-study-caption.png)；支撑[技术 claim 证据矩阵](../papers/act.md#52-技术-claim-证据矩阵消融和机制证据)。 | passed：四 panel 与完整 caption，contact-sheet + `1565×660` 原分辨率 QA。 |

## Diffusion Policy

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.3，`1489×2105`；`(112,126,1259,564)` | “Figure 2. Diffusion Policy Overview. a) General formulation. At time step t, the policy takes the latest To steps of observation data Ot as input and outputs Ta steps of actions At. b) In the CNN-based Diffusion Policy, FiLM conditioning of the observation feature Ot is applied to every convolution layer, channel-wise. Starting from AtK drawn from Gaussian noise, the output of noise-prediction network is subtracted, repeating K times to get At0, the denoised action sequence. c) In the Transformer-based Diffusion Policy, the embedding of observation Ot is passed into a multi-head cross-attention layer of each transformer decoder block. Each action embedding is constrained to only attend to itself and previous action embeddings.” | [asset](../assets/papers/diffusion-policy/fig2-diffusion-policy-overview-caption.png)；支撑[问题—方案闭环](../papers/diffusion-policy.md#2-研究动机与问题方案闭环)和[研究方法](../papers/diffusion-policy.md#4-研究方法)。 | passed：单一 Figure 2、完整 caption，contact-sheet + `1259×564` 原分辨率 QA。 |
| Figure 5 | PDF p.5，`1489×2105`；`(757,733,610,557)` | “Figure 5. Diffusion Policy Ablation Study. Change (difference) in success rate relative to the maximum for each task is shown on the Y-axis. Left: trade-off between temporal consistency and responsiveness when selecting the action horizon. Right: Diffusion Policy with position control is robust against latency. Latency is defined as the number of steps between the last frame of observations to the first action that can be executed.” | [asset](../assets/papers/diffusion-policy/fig5-action-horizon-latency-ablation-caption.png)；支撑[技术点证据矩阵](../papers/diffusion-policy.md#52-技术点证据矩阵)。 | passed：单一 Figure 5、完整 caption，contact-sheet + `610×557` 原分辨率 QA。 |

## RT-2

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 1 | PDF p.2，2481 x 3508；`(244,344,1992,1050)` | RT-2 将机器人动作表示为文本 token，和 Internet-scale vision-language 数据共同训练；推理时将文本 token 反 token 化为动作，实现闭环控制，并将基础 VLM 的泛化、语义和推理迁移到机器人控制。 | [asset](../assets/papers/rt-2/fig1_rt2_overview_caption.png)；支撑 [核心机制](../papers/rt-2.md#核心机制与贡献)。 | passed：单一对象、全 panel/label/caption 完整。 |
| Table 6 | PDF p.24，2481 x 3508；`(246,1460,1980,500)` | RT-2 的消融展示参数规模和训练策略对泛化的影响。 | [asset](../assets/papers/rt-2/table6_size_training_ablation_caption.png)；支撑 [关键实验](../papers/rt-2.md#关键实验与证据)。 | passed：完整表与 caption、原分辨率可读。 |

## EmbodiedScan

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 4 | PDF p.5，1870 x 2420；`(120,190,1630,830)` | Embodied Perceptron 接收任意视图数的 RGB-D 序列和文本，多模态编码后以 dense 与 isomorphic sparse fusion 连接不同预测 decoder；融合文本的稀疏 3D 特征可用于语言 grounding。 | [asset](../assets/papers/embodiedscan/fig4-embodied-perceptron-caption.png)；支撑 [核心机制](../papers/embodiedscan.md#核心机制与贡献)。 | passed：单一对象、完整 caption、100% 原分辨率检查。 |
| Table 12 | PDF p.16，1870 x 2420；`(120,735,1630,207)` | dense fusion 的消融研究。 | [asset](../assets/papers/embodiedscan/table12-dense-fusion-ablation-caption.png)；支撑 [关键实验](../papers/embodiedscan.md#关键实验与证据)。 | passed：完整行列与 caption、100% 原分辨率检查。 |

## Genie

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 3 | PDF p.4，1819 x 2573；`(180,225,1460,550)` | Genie 训练：输入 T 帧视频，经 video tokenizer 变成离散 token z，latent action model 推断帧间 latent action；二者送进 dynamics model，迭代预测下一帧。 | [asset](../assets/papers/genie/fig3-genie-training-mechanism-caption.png)；支撑 [核心机制](../papers/genie.md#核心机制与贡献)。 | passed：单一对象、caption/labels 完整，原 1460 x 550 可读。 |
| Figure 9 | PDF p.6，1819 x 2573；`(180,255,1460,490)` | scaling results：左为不同模型规模训练曲线，中为最近 300 次更新平均的最终训练损失，右为 2.3B 模型不同 batch size 的最终训练损失。 | [asset](../assets/papers/genie/fig9-scaling-results-caption.png)；支撑 [关键实验](../papers/genie.md#关键实验与证据)。 | passed：轴、legend、caption 完整，原 1460 x 490 可读。 |

## OpenVLA

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.4，2550 x 3300；`(335,260,1880,900)` | OpenVLA 接受图像和语言指令并预测 7 维控制动作；架构由拼接 DINOv2/SigLIP 特征的视觉编码器、映射到语言空间的 projector 与 Llama 2 7B LLM backbone 组成。 | [asset](../assets/papers/openvla/fig2_openvla_architecture_caption.png)；支撑 [方法](../papers/openvla.md#方法与实现)。 | passed：Figure、caption 和 labels 完整。 |
| Table 1 | PDF p.10，2550 x 3300；`(1080,585,1170,640)` | 参数高效微调评估：LoRA 仅训练 1.4% 参数即可匹配全量微调表现；结果为部分 Franka-Tabletop 任务各方法 33 次 rollout 的均值和标准误，带星号的配置以 FSDP 分到两张 GPU。 | [asset](../assets/papers/openvla/table1_finetuning_memory_caption.png)；支撑 [关键实验](../papers/openvla.md#关键实验与证据)。 | passed：表、footnote 与 caption 完整。 |
| Figure 6 | PDF p.10，2550 x 3300；`(290,1925,1150,680)` | 各 GPU 的 OpenVLA 推理速度：bf16 和 int4 都有高吞吐，尤其 Ada Lovelace 的 RTX 4090/H100；TensorRT-LLM 等框架仍可能更快，Spade 表示模型分到两张 GPU 才能容纳。 | [asset](../assets/papers/openvla/fig6_inference_speed_caption.png)；支撑 [关键实验](../papers/openvla.md#关键实验与证据)。 | passed：Figure、legend 和 caption 完整。 |
| Table 2 | PDF p.10，2550 x 3300；`(1430,2010,820,600)` | 量化推理性能：4-bit 与默认 bf16 的表现相当，GPU memory footprint 降低超过一半；结果覆盖 8 个 BridgeData V2 代表任务、每种方法 80 次 rollout。 | [asset](../assets/papers/openvla/table2_quantization_memory_caption.png)；支撑 [关键实验](../papers/openvla.md#关键实验与证据)。 | passed：表与 caption 完整。 |

## VLFM

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.3，1700 x 2200；`(115,145,1470,625)` | VLFM 建立 occupancy map 与指向视野外目标概率的 value map；先原地旋转初始化，再从 frontier 选 waypoint，使用经 VER 训练的 PointNav 执行 frontier 和目标导航。 | [asset](../assets/papers/vlfm/fig2_vlfm_architecture_caption.png)；支撑 [核心机制](../papers/vlfm.md#核心机制与贡献)。 | passed：单一对象、完整 caption、原分辨率可读。 |
| Table II | PDF p.6，1700 x 2200；`(115,90,750,370)` | 比较 VLFM 所用不同 value-update 方法的性能。 | [asset](../assets/papers/vlfm/table2_value_update_ablation_caption.png)；支撑 [关键实验](../papers/vlfm.md#关键实验与证据)。 | passed：表头、行列与 caption 完整。 |

## Cosmos World Foundation Model Platform

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 9 | PDF p.14，1654 x 2339；`(165,525,1325,745)` | Cosmos Tokenizer 总体架构：时间因果路径处理顺序输入，encoder-decoder 结合 wavelet transform 与 causal operation 捕获空间和时间依赖。 | [asset](../assets/papers/cosmos-world-foundation-model/fig9-tokenizer-architecture-caption.png)；支撑 [核心机制](../papers/cosmos-world-foundation-model.md#核心机制与贡献)。 | passed：单一对象、完整 panel/caption、原分辨率可读。 |
| Table 12 | PDF p.22，1654 x 2339；`(165,900,1325,385)` | progressive training 的阶段和规格：低分辨率预训练为 512p、57 frames、10,240 context、FSDP 64/CP 2；高分辨率预训练与高质量微调为 720p、121 frames、56,320 context、FSDP 64/CP 8，脚注给出完整 tokenizer/patchifier context 计算。 | [asset](../assets/papers/cosmos-world-foundation-model/table12-diffusion-training-parallelism-caption.png)；支撑 [部署](../papers/cosmos-world-foundation-model.md#infra-与部署)。 | passed：表标题、内容和两条脚注完整。 |
| Table 16 | PDF p.32，1654 x 2339；`(165,225,1325,700)` | 640 x 1024 测试视频的 Cosmos AR 性能，报告以一个 conditioning frame 生成 32 帧的平均秒数和 VRAM；No DD、No DD+Medusa、With DD、With DD+Medusa 分别表示 diffusion decoder 和 Medusa heads 的组合。 | [asset](../assets/papers/cosmos-world-foundation-model/table16-ar-latency-vram-caption.png)；支撑 [关键实验](../papers/cosmos-world-foundation-model.md#关键实验与证据)。 | passed：最终裁剪包含完整 notes/caption，未含 Table 17。 |
| Figure 30 | PDF p.54，1654 x 2339；`(155,245,1345,425)` | Cosmos Guardrail 总览：pre-Guard 依据 Aegis 和关键词阻断输入，post-Guard 用视频内容安全分类器阻断输出并模糊人脸。 | [asset](../assets/papers/cosmos-world-foundation-model/fig30-guardrail-overview-caption.png)；支撑 [核心机制](../papers/cosmos-world-foundation-model.md#核心机制与贡献)。 | passed：重裁后 caption 左缘与 diagram 完整。 |

## NaVILA

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.3，2550 x 3300；`(85,215,2385,810)` | NaVILA 是两级框架：高层 VLA 处理单视图图像、生成自然语言中层动作；低层先进 locomotion policy 将其变成精确关节运动，因此同时获得 VLA 泛化与实时性。 | [asset](../assets/papers/navila/fig2-two-level-framework-caption.png)；支撑 [核心机制](../papers/navila.md#核心机制与贡献)。 | passed：单一对象、完整 caption/labels、100% 检查。 |
| Table XIII | PDF p.17，2550 x 3300；`(95,1015,2360,405)` | NaVILA 量化结果：RTX 4090、1737 context tokens、生成 10 tokens，测试样本来自 R2R-CE。 | [asset](../assets/papers/navila/table13-quantization-latency-caption.png)；支撑 [关键实验](../papers/navila.md#关键实验与证据)。 | passed：重裁后只有该表和完整 caption。 |

## VGGT

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.3，2125 x 2750；`(155,245,1820,810)` | VGGT 架构：输入图像先由 DINO patchify 成 token，并添加 camera token；随后交替进行 frame-wise 与 global self-attention，camera head 预测内外参，DPT head 预测任意稠密输出。 | [asset](../assets/papers/vggt/fig2-architecture-caption.png)；支撑 [核心机制](../papers/vggt.md#核心机制与贡献)。 | passed：单一对象、完整 caption、原 1820 x 810 可读。 |
| Table 9 | PDF p.10，2125 x 2750；`(1060,245,900,290)` | 不同输入帧数的 runtime 与 peak GPU memory usage；runtime 单位为秒，GPU memory 单位为 GB。 | [asset](../assets/papers/vggt/table9-runtime-memory-caption.png)；支撑 [关键实验](../papers/vggt.md#关键实验与证据)。 | passed：完整列和 caption、原 900 x 290 可读。 |

## MotuBrain

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 1 | PDF p.3，1870 x 2420；`(190,210,1490,1120)` | MotuBrain 架构基于统一 video-action backbone，以 text、video、action 三流 Mixture-of-Transformers、H-bridge attention 和 view-dependent 3D RoPE 支持跨模态交互与灵活多视图输入。 | [asset](../assets/papers/motubrain/fig1-architecture-caption.png)；支撑 [核心机制](../papers/motubrain.md#核心机制与贡献)。 | passed：单一对象、caption 完整、100% 可读。 |
| Table 2 | PDF p.8，1870 x 2420；`(205,225,1460,450)` | 推理优化的累计 speedup：每一行在前面全部技术之上再增加所列方法；latency 在 non-autoregressive model 上端到端测量，适用时报告 per-step latency。 | [asset](../assets/papers/motubrain/table2-inference-speed-caption.png)；支撑 [关键实验](../papers/motubrain.md#关键实验与证据)。 | passed：单一表、caption 完整、无相邻正文。 |
| Table 3 | PDF p.9，1870 x 2420；`(205,1050,1475,930)` | RoboTwin 2.0 结果：遵循既有工作，以官方 clean + randomized 数据微调预训练权重；MotuBrain-Non-AR 表示非自回归模式。 | [asset](../assets/papers/motubrain/table3-robotwin-results-caption.png)；支撑 [关键实验](../papers/motubrain.md#关键实验与证据)。 | passed：完整表与 caption、无前后正文。 |

## WAM4D

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.4，1275 x 1650；`(140,122,995,555)` | WAM4D 架构和因果可见性模式。 | [asset](../assets/papers/wam4d/fig2-wam4d-architecture-causal-visibility-caption.png)；支撑 [核心机制](../papers/wam4d.md#核心机制与贡献)。 | passed：完整可见 caption、labels 和单一对象。 |
| Table 7 | PDF p.12，1275 x 1650；`(140,127,997,221)` | depth readout interface、register placement 和 register visibility 在固定 depth head、RoboTwin 10-task split 上的消融，报告选定质量指标。 | [asset](../assets/papers/wam4d/table7-register-interface-placement-visibility-caption.png)；支撑 [关键实验](../papers/wam4d.md#关键实验与证据)。 | passed：表头、行列、caption 完整。 |
| Table 9 | PDF p.15，1275 x 1650；`(145,914,990,264)` | 单张 A800 80GB GPU 上的 compute 与 latency 对比；在可用处 latency 以 ms 均值加标准差报告，peak memory 与 Table 1 的 VRAM 测量一致。 | [asset](../assets/papers/wam4d/table9-deployment-latency-memory-caption.png)；支撑 [部署](../papers/wam4d.md#infra-与部署)。 | passed：完整表、caption 和 foot rules，无 Section 5。 |
