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
| Figure 1 | 最终 PMLR PDF p.2，`1700×2200` @ 200 DPI；`(285,190,1133,566)` | “RT-2 overview: we represent robot actions as another language, which can be cast into text tokens and trained together with Internet-scale vision-language datasets. During inference, the text tokens are de-tokenized into robot actions, enabling closed loop control. This allows us to leverage the backbone and pretraining of vision-language models in learning robotic policies, transferring some of their generalization, semantic understanding, and reasoning to robotic control. We demonstrate examples of RT-2 execution on the project website: robotics-transformer2.github.io.” | [asset](../assets/papers/rt-2/fig1-rt2-overview-caption.png)；支撑[研究方法](../papers/rt-2.md#4-研究方法)。 | passed：单一 Figure 1、完整 caption，contact-sheet + `1133×566` 原分辨率 QA。 |
| Table 7 | 最终 PMLR PDF p.19，`1700×2200` @ 200 DPI；`(330,365,1050,285)` | “Ablations of RT-2 showcasing the impact of parameter count and training strategy on generalization.” | [asset](../assets/papers/rt-2/table7-size-training-ablation-caption.png)；支撑[技术点证据矩阵与消融](../papers/rt-2.md#52-技术点证据矩阵与消融)。 | passed：单一 Table 7、完整行列/caption，contact-sheet + `1050×285` 原分辨率 QA。 |

## EmbodiedScan

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 4 | source-compiled PDF p.5，`2125×2750`；`(120,15,1885,1147)` | “Figure 4. Embodied Perceptron accepts RGB-D sequence with any number of views along with texts as multi-modal input. It uses classical encoders to extract features for each modality and adopts dense and isomorphic sparse fusion with corresponding decoders for different predictions. The 3D features integrated with the text feature can be further used for language-grounded understanding.” | [asset](../assets/papers/embodiedscan/fig4-embodied-perceptron-caption.png)；支撑[研究方法](../papers/embodiedscan.md#4-研究方法)。 | passed：单一 Figure 4、完整 caption，contact-sheet + `1885×1147` 原分辨率 QA。 |
| Table 12 | source-compiled PDF p.16，`2125×2750`；`(160,835,1810,240)` | “Table 12. Ablation studies for dense fusion.” | [asset](../assets/papers/embodiedscan/table12-dense-fusion-ablation-caption.png)；支撑[技术 claim 证据矩阵](../papers/embodiedscan.md#51-技术-claim-证据矩阵)。 | passed：完整行列与 caption，contact-sheet + `1810×240` 原分辨率 QA。 |

## Genie

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 3 | PDF p.4，`1489×2105`；`(145,190,1199,460)` | “Genie model training: Genie takes in $T$ frames of video as input, tokenizes them into discrete tokens $z$ via the video tokenizer, and infers the latent actions $\tilde a$ between each frame with the latent action model. Both are then passed to the dynamics model to generate predictions for the next frames in an iterative manner.” | [asset](../assets/papers/genie/fig3-genie-training-mechanism-caption.png)；支撑 [核心机制](../papers/genie.md#核心机制与贡献)。 | passed：单一 Figure 3、完整 caption，contact-sheet + `1199×460` 原分辨率 QA。 |
| Table 2 | PDF p.9，`1489×2105`；`(758,1030,600,258)` | “Latent action model input ablation. We see that Genie achieves higher controllability.” | [asset](../assets/papers/genie/table2-lam-input-ablation-caption.png)；支撑 [技术点证据矩阵](../papers/genie.md#42-技术点证据矩阵)。 | passed：单一 Table 2、完整行列与 caption，contact-sheet + `600×258` 原分辨率 QA。 |

## OpenVLA

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.4，`1700×2200` @ 200 DPI；`(285,190,1145,555)` | “OpenVLA model architecture. Given an image observation and a language instruction, the model predicts 7-dimensional robot control actions. The architecture consists of three key components: (1) a vision encoder that concatenates Dino V2 and SigLIP features, (2) a projector that maps visual features to the language embedding space, and (3) the LLM backbone, a Llama 2 7B-parameter large language model.” | [asset](../assets/papers/openvla/fig2_architecture_caption.png)；支撑[研究方法](../papers/openvla.md#4-研究方法)。 | passed：单一 Figure 2、完整 caption，contact-sheet + `1145×555` 原分辨率 QA。 |
| Figure 3 | PDF p.7，`1700×2200` @ 200 DPI；`(290,185,1125,675)` | “BridgeData V2 WidowX robot evaluation tasks and results. We evaluate OpenVLA and prior state-of-the-art generalist robot policies on a comprehensive suite of tasks covering several axes of generalization, as well as tasks that specifically assess language conditioning ability. OpenVLA achieves highest overall performance and even outperforms closed-source model RT-2-X in all categories except for semantic generalization. Average success rates ± StdErr are computed across 170 total rollouts per approach. See Table 4 for detailed results.” | [asset](../assets/papers/openvla/fig3_bridge_results_caption.png)；支撑[主结果](../papers/openvla.md#51-主结果)。 | passed：单一 Figure 3、完整 caption，contact-sheet + `1125×675` 原分辨率 QA。 |
| Table 1 | PDF p.10，`1700×2200` @ 200 DPI；`(735,395,665,390)` | “Parameter-efficient fine-tuning evaluation. LoRA fine-tuning achieves the best performance-compute trade-off, matching full fine-tuning performance while training only 1.4% of the model parameters. Mean success ± StdErr computed across 33 rollouts per approach on select Franka-Tabletop tasks (see Table 8 for details). *: Sharded across 2 GPUs with FSDP.” | [asset](../assets/papers/openvla/table1_peft_caption.png)；支撑[PEFT 与资源归因](../papers/openvla.md#53-peft-与资源归因)。 | passed：单一 Table 1、完整 footnote/caption，contact-sheet + `665×390` 原分辨率 QA。 |
| Table 9 | PDF p.34，`1700×2200` @ 200 DPI；`(295,205,1120,475)` | “BridgeData V2 WidowX ablation experiment results. We evaluate various methods on a subset of 8 representative tasks to assess the importance of different components of the OpenVLA model architecture and training scheme. OpenVLA-Bridge is a version of OpenVLA without OpenX training (it is trained only on BridgeData V2), and OpenVLA-Bridge-SigLIP additionally ablates the fused vision backbone by removing the DinoV2 encoder (its vision backbone only consists of the SigLIP encoder). We observe that both OpenX training and the fused vision encoder improve policy performance, though the former has a much greater effect than the latter.” | [asset](../assets/papers/openvla/table9_ablation_caption.png)；支撑[技术点证据矩阵](../papers/openvla.md#52-技术点证据矩阵)。 | passed：单一 Table 9、完整行列/caption，contact-sheet + `1120×475` 原分辨率 QA。 |

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
| Figure 2 | PDF p.3，`1530×1980`；`(100,120,1330,500)` | “NaVILA is a two-level framework combining high-level visual language understanding with low-level locomotion control. Our VLA model processes single-view images to produce mid-level actions in natural language, which are then converted into precise joint movements by an advanced low-level locomotion policy. This integration allows for strong generalization and adaptability across different real-world environments, and can operate the robot in real-time.” | [asset](../assets/papers/navila/fig2_two_level_framework_caption.png)；支撑[研究方法](../papers/navila.md#4-研究方法)。 | passed：单一 Figure 2、完整 caption，contact-sheet + `1330×500` 原分辨率 QA。 |
| Figure 3 | PDF p.4，`1530×1980`；`(95,0,1340,660)` | “Overview of our VLA framework. We denote the purple blocks as memory tokens sampled from historical frames, and the red blocks as the current observation tokens. The flame symbol denotes trainable parameters. In our experiments, we tested configurations with 8 to 64 frames for $t$.” | [asset](../assets/papers/navila/fig3_vla_framework_caption.png)；支撑[研究方法](../papers/navila.md#4-研究方法)。 | passed：单一 Figure 3、完整 caption，contact-sheet + `1340×660` 原分辨率 QA。 |
| Table I | PDF p.6，`1530×1980`；`(110,125,1310,730)` | “Comparison with state-of-the-art methods on the Val-Unseen split of R2R-CE and RxR-CE. * indicates methods using the waypoint predictor from Hong et al. NaVILA outperforms all methods that do not rely on simulator pre-trained waypoint predictors, even when those methods leverage additional inputs such as depth, panoramic views, and odometry.” | [asset](../assets/papers/navila/table1_vln_ce_main_results_caption.png)；支撑[主结果](../papers/navila.md#51-主结果与系统数字)。 | passed：单一 Table I、完整行列和 caption，contact-sheet + `1310×730` 原分辨率 QA。 |
| Table V | PDF p.7，`1530×1980`；`(780,715,635,190)` | “Low level policy performance.” | [asset](../assets/papers/navila/table5_low_level_policy_caption.png)；支撑[主结果](../papers/navila.md#51-主结果与系统数字)。 | passed：单一 Table V、完整行列和 caption，contact-sheet + `635×190` 原分辨率 QA。 |
| Table VIII | PDF p.14，`1530×1980`；`(105,1535,550,315)` | “Results on R2R-CE using additional real data from human touring videos. † indicates models trained without human touring videos.” | [asset](../assets/papers/navila/table8_human_video_ablation_caption.png)；支撑[收益来源归因](../papers/navila.md#54-收益来源归因)。 | passed：重裁后单一 Table VIII、完整 footnote 和 caption，contact-sheet + `550×315` 原分辨率 QA。 |

## VGGT

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.3，2125 x 2750；`(155,245,1820,810)` | VGGT 架构：输入图像先由 DINO patchify 成 token，并添加 camera token；随后交替进行 frame-wise 与 global self-attention，camera head 预测内外参，DPT head 预测任意稠密输出。 | [asset](../assets/papers/vggt/fig2-architecture-caption.png)；支撑 [核心机制](../papers/vggt.md#核心机制与贡献)。 | passed：单一对象、完整 caption、原 1820 x 810 可读。 |
| Table 9 | PDF p.10，2125 x 2750；`(1060,245,900,290)` | 不同输入帧数的 runtime 与 peak GPU memory usage；runtime 单位为秒，GPU memory 单位为 GB。 | [asset](../assets/papers/vggt/table9-runtime-memory-caption.png)；支撑 [关键实验](../papers/vggt.md#关键实验与证据)。 | passed：完整列和 caption、原 900 x 290 可读。 |

## MotuBrain

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 1 | PDF p.3，`1700×2200` @ 200 DPI；`(180,200,1340,1035)` | “Overview of Motubrain’s architecture. Motubrain builds on a unified video-action backbone and adopts a three-stream Mixture-of-Transformers architecture with text, video, and action streams. It further uses an H-bridge attention design to balance cross-modal interaction and efficiency, while supporting flexible multiview inputs through view-dependent 3D RoPE offsets.” | [asset](../assets/papers/motubrain/fig1-architecture-caption.png)；支撑[研究方法](../papers/motubrain.md#4-研究方法)。 | passed：单一 Figure 1、完整 caption，contact-sheet + `1340×1035` 原分辨率 QA。 |
| Table 2 | PDF p.8，`1700×2200` @ 200 DPI；`(180,15,1350,590)` | “Cumulative speedup from inference optimizations. Each row applies the listed technique on top of all preceding ones. Latency is measured end-to-end on the non-autoregressive model. Per-step latency is reported where applicable.” | [asset](../assets/papers/motubrain/table2-inference-speed-caption.png)；支撑[推理优化证据](../papers/motubrain.md#52-runtime-ladder)。 | passed：重裁后单一 Table 2、完整 caption，contact-sheet + `1350×590` 原分辨率 QA。 |
| Table 3 | PDF p.9，`1700×2200` @ 200 DPI；`(180,955,1350,835)` | “Robotwin 2.0 Results. Following previous works, Motubrain is fine-tuned from pre-trained weights on the official RoboTwin 2.0 dataset (clean + randomized), yielding the evaluation results presented in the table. Motubrain-Non-AR represents non-autoregressive mode.” | [asset](../assets/papers/motubrain/table3-robotwin-results-caption.png)；支撑[主结果](../papers/motubrain.md#51-robotwin)。 | passed：重裁后单一 Table 3、完整 caption，contact-sheet + `1350×835` 原分辨率 QA。 |

## WAM4D

| Object | Source | Caption（完整中文转述） | Crop / usage | QA |
| --- | --- | --- | --- | --- |
| Figure 2 | PDF p.4，1275 x 1650；`(140,122,995,555)` | WAM4D 架构和因果可见性模式。 | [asset](../assets/papers/wam4d/fig2-wam4d-architecture-causal-visibility-caption.png)；支撑 [核心机制](../papers/wam4d.md#核心机制与贡献)。 | passed：完整可见 caption、labels 和单一对象。 |
| Table 7 | PDF p.12，1275 x 1650；`(140,127,997,221)` | depth readout interface、register placement 和 register visibility 在固定 depth head、RoboTwin 10-task split 上的消融，报告选定质量指标。 | [asset](../assets/papers/wam4d/table7-register-interface-placement-visibility-caption.png)；支撑 [关键实验](../papers/wam4d.md#关键实验与证据)。 | passed：表头、行列、caption 完整。 |
| Table 9 | PDF p.15，1275 x 1650；`(145,914,990,264)` | 单张 A800 80GB GPU 上的 compute 与 latency 对比；在可用处 latency 以 ms 均值加标准差报告，peak memory 与 Table 1 的 VRAM 测量一致。 | [asset](../assets/papers/wam4d/table9-deployment-latency-memory-caption.png)；支撑 [部署](../papers/wam4d.md#infra-与部署)。 | passed：完整表、caption 和 foot rules，无 Section 5。 |
