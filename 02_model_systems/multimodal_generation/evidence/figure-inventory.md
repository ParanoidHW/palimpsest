# Multimodal Generation 原论文图清单与 QA

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion evolution](../surveys/diffusion-evolution.md)
> - 证据资产：`../assets/papers/`
> - 相关文档：[MAGI-1](../papers/magi-1.md)，[Cosmos 3](../papers/cosmos-3.md)，[Q&A supplement](../supplements/cosmos-3-q-and-a.md)

Cosmos 3 资产来自 arXiv:2606.02800v1 的 LaTeX/TikZ/source-native figures；PDF 页码按 139 页 v1 核验。`bbox` 对 source-native export 使用资产自身 `(0,0,width,height)`。这些资产是论文图体的无损/高分辨率导出，完整 caption 在本清单中保留；正文邻近段落提供中文解释。2026-07-11 以原分辨率逐图检查图体、legend、文字与边缘。

| Object / PDF 页 | Caption（完整中文转述） | Source | 正式资产 / bbox | Owner / usage | QA |
|---|---|---|---|---|---|
| Figure 1 / p.5 | Cosmos 3 是 Physical AI 的通用 backbone：联合建模 language、image、video、audio、action 的理解与生成，在一个架构中统一 VLM、image/video/audio generator、policy/world-action、forward 与 inverse dynamics。 | `figures/introduction/cosmos3_overview.tex` | `../assets/papers/cosmos-3/overview.png`; `(0,0,7273,2317)` | cosmos-3 / problem scope | pass；单一 Fig.1 图体、源级清晰 |
| Figure 2 / p.6 | Cosmos 3 可在不修改架构的情况下针对不同 Physical AI 应用后训练；论文展示 synthetic data generation 与 robot policy。 | `figures/introduction/cosmos_platform.tex` | `../assets/papers/cosmos-3/platform.png`; `(0,0,1235,644)` | cosmos-3 / platform variants | pass |
| Figure 3 / p.8 | 将异构 embodiment control 映射为共享几何组件构成的紧凑 action vector：ego/effector 使用 3D translation + 6D rotation 的 relative-pose pseudo-actions，grasp state 表示当前操控状态，domain-aware projections 处理不同长度。 | `figures/model_architecture/action/action_representation.tex` | `../assets/papers/cosmos-3/action-representation.png`; `(0,0,1134,504)` | cosmos-3 / action encoding | pass |
| Figure 5 / p.11 | 单一 sequence 包含 AR 与 DM subsequence；AR reasoner 与 DM generator 在每层使用独立参数，DM 通过 joint attention 读取 AR 条件，而 AR 不读取 noisy DM。 | `figures/model_architecture/mot_architecture.tex` | `../assets/papers/cosmos-3/mot-architecture.png`; `(0,0,1672,763)` | cosmos-3 / MoT | pass |
| Figure 6 / p.13 | 3D MRoPE 为 packed language/video/audio/action token 分配 $(t,h,w)$；语言三轴相同、video 三轴变化、audio/action 只用时间轴；FPS modulation 使相同真实时长在 16/24/30 FPS 下覆盖相等 position range。 | `figures/model_architecture/mrope_coordinate_assignment.tex` | `../assets/papers/cosmos-3/mrope-coordinate-assignment.png`; `(0,0,1308,320)` | cosmos-3 / position alignment | pass |
| Reasoner data composition (pre-training) / p.15 | Reasoner 的 22.0M pre-training samples 按 OCR、VQA、reasoning、captioning、grounding、instruction 等 capability category 分解。 | `figures/data/reasoner/reasoner_stats.tex` | `../assets/papers/cosmos-3/reasoner-pretraining-mix.png`; `(0,0,497,373)` | cosmos-3 / data stages | pass；单一子图、原分辨率复核 |
| Reasoner data composition (SFT) / p.15 | Reasoner 的 2.2M SFT samples 按 OCR、VQA、reasoning、captioning、grounding、instruction 等 capability category 分解。 | `figures/data/reasoner/reasoner_stats.tex` | `../assets/papers/cosmos-3/reasoner-sft-mix.png`; `(0,0,497,373)` | cosmos-3 / data stages | pass；单一子图、原分辨率复核 |
| Generator data curriculum / p.20 | Generator 按 pre-training、mid-training 与 post-training 逐步引入 image/video/audio、action/transfer 和专用任务数据。 | `figures/data/data_curriculum.tex` | `../assets/papers/cosmos-3/data-curriculum.png`; `(0,0,1151,350)` | cosmos-3 / curriculum | pass |
| Action distribution / data section | 展示不同 action domain/embodiment 在训练数据中的分布，用于说明 domain-aware projection 和 sampling mixture。 | action data source figure | `../assets/papers/cosmos-3/action-data-distribution.png`; `(0,0,523,313)` | cosmos-3 / supplement data detail | pass；未用于 headline conclusion |
| Multiview packaging / data section | 多视角 action sample 将 camera views 拼成单 canvas，并在 JSON prompt 中附 view-layout metadata。 | `figures/data/action/action_multiview_packaging.tex` | `../assets/papers/cosmos-3/droid-multiview-packaging.jpg`; `(0,0,640,540)` | cosmos-3 / Q&A data construction | pass；source-native raster |
| Infrastructure overview / p.33 | Cosmos 3 infra 总览覆盖 joint loader、distributed training、attention/compiler/checkpoint 与 serving stack。 | `figures/infrastructure/infra_overview.tex` | `../assets/papers/cosmos-3/infra-overview.png`; `(0,0,1458,167)` | cosmos-3 / infra | pass；超宽图以原分辨率复核文字 |
| JointDataLoader / p.38 | Joint Data-Loader 从多模态 streams 取样，以 rank-synchronous selection 和 token-budgeted/look-ahead packing 构建设备 batch。 | `sections/infrastructure/training.tex` | `../assets/papers/cosmos-3/joint-dataloader.png`; `(0,0,957,397)` | cosmos-3 / loader | pass |
| Serving performance / p.50 | (a) Nano 720p T2V 单 GPU H100 NVL/B200 latency；(b) Nano 720p T2I 单 GPU latency；(c) B200 上 Nano/Super 720p T2V 从 1 到 8 GPU 的 latency scaling；均 lower-is-better。 | `figures/infrastructure/serving/cosmos3_serving_latency_combined_1x3_figure.tex` | `../assets/papers/cosmos-3/serving-latency.png`; `(0,0,2219,922)` | cosmos-3 / serving | pass；三个 panel 属同一 Figure，未拆成不同编号对象 |
| Knowledge-base diagram / 无原编号 | 将 two-way mask lowering 为 AR causal varlen attention 与 DM full varlen attention 两次调用；这是知识库整理图，不是原论文证据。 | 基于 Sec.5 与固定代码快照整理 | `../assets/papers/cosmos-3/two-way-attention-infra.png`; `(0,0,942,591)` | cosmos-3 / explanation | pass；已明确标注整理图 |

## 清理结论

- 14 个现有资产均有 canonical owner、来源与用途；没有未解释资产。
- `reasoner-sft-mix.png` 与 `action-data-distribution.png` 不在主 Paper 重复嵌入，但分别用于阶段对照和 data evidence，保留在 inventory。
- `two-way-attention-infra.png` 明确是知识库整理图，不替代论文 Figure 或 runtime measurement。

## Multimodal Diffusion Infra Survey 新增资产（2026-07-12）

以下原论文对象均由独立 deep review 从 PDF 裁剪，完整 caption 随图保留；源页渲染为 `1530x1980` 或对应论文原始渲染尺寸，bbox 和逐图 QA 的精确记录保存在各 paper-local inventory。正式资产以 paper 为 canonical owner。

| Paper / Object | Source / usage | 正式资产 | QA |
|---|---|---|---|
| LDM Figure 2 | arXiv:2112.10752，PDF p.3；pixel→latent 管线 | `../assets/papers/ldm/fig2-perceptual-semantic-compression.png` | pass；单一对象、完整 caption、原分辨率复核 |
| DiT Figure 3 | arXiv:2212.09748，PDF p.3；backbone | `../assets/papers/dit/fig3-dit-architecture.png` | pass |
| Transfusion Figure 4 | arXiv:2408.11039，PDF p.4；mixed mask | `../assets/papers/transfusion/fig4-mixed-attention-mask.png` | pass |
| BAGEL Figure 2 | arXiv:2505.14683，PDF p.4；MoT | `../assets/papers/bagel/fig2-mot-architecture.png` | pass |
| PixelDiT Figure 2 | arXiv:2511.20645，PDF p.4；dual-level pixel path | `../assets/papers/pixeldit/fig2-dual-level-architecture.png` | pass |
| DC-AE Table 3 | arXiv:2410.10733，PDF p.9；效率/显存 | `../assets/papers/dcae/table3-imagenet-efficiency.png` | pass |
| HunyuanVideo 1.5 Table 7 | arXiv:2511.18870，PDF p.11；SSTA latency | `../assets/papers/hunyuanvideo-1-5/table7-inference-speed.png` | pass |
| Sparse VideoGen Figure 7 | arXiv:2502.01776，PDF p.8；端到端分解 | `../assets/papers/sparse-videogen/fig7-end-to-end-breakdown.png` | pass |
| FEB-Cache Figure 3 | arXiv:2503.07120，PDF p.4；cache mechanism | `../assets/papers/feb-cache/fig3-cache-mechanism.png` | pass |
| SwiftFusion Figure 6 | arXiv:2601.20273，PDF p.7；Torus scheduling | `../assets/papers/swiftfusion/fig6-torus-scheduling.png` | pass |
| Causal-rCM Figure 4 | arXiv:2606.25473，PDF p.5；训练管线 | `../assets/papers/causal-rcm/fig4-pipeline-comparison.png` | pass |
| Survey stack/workload | 知识库整理图 | `../assets/surveys/multimodal-diffusion-infra/stack-and-workload.svg` | pass；SVG 原分辨率/文字边界复核 |
| Survey pipeline evolution | 知识库整理图 | `../assets/surveys/multimodal-diffusion-infra/pipeline-evolution.svg` | pass |
| Survey optimization matrix | 知识库整理图 | `../assets/surveys/multimodal-diffusion-infra/optimization-infra-matrix.svg` | pass |
| Survey trends/infra | OpenRouter ICU 基于完整 Survey Markdown 生成的整理图；request `74741304-81a2-4ba7-a4b6-37d0a6b9969e` | `../assets/surveys/multimodal-diffusion-infra/survey-trends-infra-generated.png` | pass；1024x1024 原分辨率复核，无重叠/空白 |

## 完整 Paper 精读新增视觉（2026-07-12）

## Cross-domain canonicalization（2026-07-25）

Causal-rCM 与 Sparse VideoGen 原先在 custom-attention 下的重复资产已迁入本 domain 的 canonical Paper owner。它们继续作为原论文证据使用；custom-attention 只通过跨域 adoption Evidence 引用，未复制图体。

| Paper / Object / PDF 页 | 完整 caption（中文转述） | 正式资产 / bbox | Usage / QA |
|---|---|---|---|
| Causal-rCM Figure 1 / p.1 | 流式视频/世界模型的生成质量、训练收敛和在线性能总体结果。 | `../assets/papers/causal-rcm/fig1_streaming_performance_caption.png`; `(0,0,1195,525)` | headline result；pass，单一对象、完整 caption、原分辨率复核 |
| Causal-rCM Figure 3 / p.6 | 对比 Teacher Forcing、Diffusion Forcing 与 Self Forcing 的 clean/noisy block mask、训练轨迹和 KV-cache 关系。 | `../assets/papers/causal-rcm/fig3_causal_training_paradigms_caption.png`; `(0,0,1180,515)` | custom-mask mechanism；pass |
| Causal-rCM Figure 4 / p.7 | 展示先 TF-CM、后 SF-DMD 的分阶段 recipe，以及各训练范式的关系。 | `../assets/papers/causal-rcm/fig4_recipe_comparison_caption.png`; `(0,0,1180,565)` | training-recipe boundary；pass |
| Causal-rCM Figure 9 / p.17 | 交互式生成中，时间因果 mask 约束历史与当前 noisy block 的可见性。 | `../assets/papers/causal-rcm/fig9_cosmos3_temporal_causal_mask_caption.png`; `(0,0,1020,690)` | multimodal transfer；pass |
| Sparse VideoGen Figure 3 / p.3 | 视频 DiT 的 attention head 分别呈现空间邻域与跨帧同位置的时间模式。 | `../assets/papers/sparse-videogen/fig3_spatial_temporal_head_masks_caption.png`; `(0,0,1260,620)` | mask semantics；pass |
| Sparse VideoGen Figure 4 / p.4 | 在线抽样 query rows，对 full、spatial、temporal 输出做近似误差比较并逐 head 选择模式。 | `../assets/papers/sparse-videogen/fig4_svg_workflow_caption.png`; `(0,0,1250,570)` | online profiling；pass |
| Sparse VideoGen Figure 5 / p.5 | 时间稀疏访问通过 layout transformation 重排为连续 tile，以改善内存合并访问。 | `../assets/papers/sparse-videogen/fig5_layout_transformation_caption.png`; `(0,0,690,515)` | layout mechanism；pass |
| Sparse VideoGen Figure 8 / p.8 | 比较原始稀疏访问与重排后的 kernel latency，显示 layout 对实际速度的影响。 | `../assets/papers/sparse-videogen/fig8_sparse_kernel_latency_caption.png`; `(0,0,675,470)` | kernel latency；pass |

以下是完整精读提升后新增的第二类证据图。bbox 使用各 paper review 的 PDF page render 像素坐标 `(x,y,width,height)`；每张图均经过 contact-sheet 初筛和原分辨率逐图 QA。

| Paper / Object / PDF 页 | 完整 caption | Source dimensions / bbox | 正式资产 / usage | QA |
|---|---|---|---|---|
| LDM Table 18 / p.28 | Comparing compute requirements during training and inference throughput with state-of-the-art generative models. Compute during training in V100-days; throughput measured in samples/sec on one NVIDIA A100; footnotes preserve source and evaluation qualifications. | `1530x1980`; `(120,240,1290,770)` | `../assets/papers/ldm/table18_compute_throughput_caption.png`; compute/throughput evidence | pass |
| DiT Figure 6 / p.6 | Scaling the DiT model improves FID at all stages of training. The top row holds patch size constant; the bottom row holds model size constant. | `1530x1980`; `(110,145,1315,610)` | `../assets/papers/dit/fig6-scaling-curves-caption.png`; model/patch scaling | pass |
| Transfusion Table 5 / p.10 | Performance of 0.76B Transfusion models with and without intra-image bidirectional attention. Patch size is 2x2 latent pixels. | `1836x2376`; `(325,620,1195,365)` | `../assets/papers/transfusion/table5-attention-ablation-caption.png`; mask ablation | pass |
| Transfusion Table 8 / p.12 | Performance with and without limiting sampled diffusion noise to `t=500` when images precede the caption; models use U-Net adapters encoding 2x2 latent patches. | `1836x2376`; `(325,205,1195,395)` | `../assets/papers/transfusion/table8-noise-limit-caption.png`; noisy-image/text conflict | pass |
| DC-AE Figure 4 / p.4 | Illustration of Residual Autoencoding. Non-parametric shortcuts let neural modules learn residuals around space-to-channel operations; `C` is channel count and `R` image size. | `1700x2200`; `(225,180,1350,625)` | `../assets/papers/dcae/fig4-residual-autoencoding-caption.png`; mechanism | pass |
| Sparse VideoGen Figure 5 / p.5 | Hardware-efficient layout transformation: non-contiguous temporal-head sparsity is converted from token-major to contiguous frame-major layout for block-sparse attention. | `1700x2200`; `(848,172,753,560)` | `../assets/papers/sparse-videogen/fig5-layout-transformation-caption.png`; layout mechanism | pass |
| FEB-Cache Table 5 / p.6 | Ablation on method components. | `1700x2200`; `(125,1275,690,190)` | `../assets/papers/feb-cache/table5_component_ablation_caption.png`; component attribution | pass |
| BAGEL Figure 7 / p.13 | Emerging curves across pre-training stages. Capabilities improve at different rates; understanding/generation emerge before editing, and VAE+ViT features outperform VAE-only especially for intelligent editing. | `1530x1980`; `(145,170,1220,1190)` | `../assets/papers/bagel/fig7-emerging-curves-caption.png`; checkpoint/result evidence | pass |
| HunyuanVideo 1.5 Figure 2 / p.4 | Architecture of the Unified Diffusion Transformer. | `1701x2200`; `(280,800,1200,960)` | `../assets/papers/hunyuanvideo-1-5/fig2_unified_dit_caption.png`; unified DiT mechanism | pass |
| PixelDiT Table 5 / p.8 | Ablations of PixelDiT-XL on ImageNet 256x256; incremental components include RoPE/RMSNorm, dual-level path, token compaction and pixel-wise AdaLN. OOM marks the uncompacted dual-level variant. | `1489x2105`; `(755,1115,620,450)` | `../assets/papers/pixeldit/table5_core_ablation_caption.png`; core ablation | pass |
| SwiftFusion Figure 10 / p.12 | Ablation studies in SwiftFusion. | `1700x2200`; `(135,270,1555,295)` | `../assets/papers/swiftfusion/fig10-ablation-caption.png`; component attribution | pass |
| Causal-rCM Table 5 / p.16 | Ablation of initialization strategies for 4-step SF-DMD. | `1786x2526`; `(435,250,920,530)` | `../assets/papers/causal-rcm/table5_initialization_ablation_caption.png`; initialization evidence | pass |
| MAGI-1 Figure 1 / p.2 | (Left) MAGI-1 performs chunk-wise autoregressive denoising. The video is generated in chunks of 24 frames, where each chunk attends to all previously denoised chunks. Once a chunk reaches a certain denoising level, the next chunk begins generation. (Right) A block-causal attention mask enforces temporal causality across chunks, enabling pipelined and parallel generation. | `1700x2200`; `(285,1150,1135,515)` | `../assets/papers/magi-1/fig1-chunkwise-ar.png`; chunkwise-AR order, 24-frame unit, causal mask | pass；单一 Figure 1、完整 caption、原分辨率复核 |
| MAGI-1 Figure 3 / p.5 | Model Architecture of Auto-Regressive Denoising Model. | `1700x2200`; `(390,1080,1030,900)` | `../assets/papers/magi-1/fig3-ardf-architecture.png`; ARDF architecture | pass；单一 Figure 3、完整 caption、紧边界 |
| MAGI-1 Figure 14 / p.24 | Overview of MagiAttention: (1) Flex-Flash-Attention(FFA), an efficient attention supports flexible mask patterns and native considers distribution requirements; (2) The dispatch solver shards and dispatches packed data with ultra-long contexts and heterogeneous masks, ensuring load-balanced computation; (3) Group-Cast and Group-Reduce primitives eliminate redundant communication; (4) The adaptive multi-stage overlap strategy effectively hides communication latency; (5) Forward and backward timelines of MagiAttention. With all techniques together, MagiAttention reach linear scalability under diverse scenarios. | `1700x2200`; `(285,170,1135,990)` | `../assets/papers/magi-1/fig14-magi-attention.png`; distributed attention, load balance, overlap | pass；单一 Figure 14、完整 caption 含末句 |
| MAGI-1 Table 6 / p.29 | Inference Optimization and Latency Gain. | `1700x2200`; `(285,640,1135,450)` | `../assets/papers/magi-1/table6-inference-latency.png`; TTFC/TPOC attribution | pass；单一 Table 6、完整标题、无相邻章节 |

以下三张为 paper-level AI 生成解释图，不属于原论文证据，均由对应完整 `analysis.md` 作为 OpenRouter ICU document input 生成并在原分辨率检查：

| Owner | 正式资产 | 用途 / QA |
|---|---|---|
| BAGEL | `../assets/papers/bagel/algorithm-analysis-generated.png` | 机制、证据边界与 Infra 总结；pass |
| DC-AE | `../assets/papers/dcae/algorithm-analysis-generated.png` | 压缩率、token 与系统收益总结；pass |
| Causal-rCM | `../assets/papers/causal-rcm/algorithm-analysis-generated.png` | TF/CM/SF 与 custom kernel 关系；pass |
- Source-native figures 未把 PDF 页眉、页码或相邻正文带入正式资产；过程 render/crop 不进入正式引用。
