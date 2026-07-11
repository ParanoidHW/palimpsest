# 原论文图清单与 QA

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：`../assets/papers/`
> - 相关文档：[Selection](selection.md)

下表覆盖正式知识库保留的全部论文裁图。Caption 栏为完整中文转述，原文 caption 同时保留在图像内。`bbox` 使用正式资产像素坐标 `(0,0,width,height)`；源 PDF 页面的初始裁剪框仍属于过程记录，不作为正式依赖。全部图片于 2026-07-10 以原分辨率逐图检查，并在 2026-07-11 复核路径与单一对象约束。

| 工作 | 对象 / PDF 页 | Caption（完整中文转述） | 正式资产 / bbox | 使用 |
|---|---|---|---|---|
| FlexAttention VLM | Fig. 2 / p.6 | 低分辨率视觉与文本提供全局语义，各层依据 attention map 选择高分辨率局部 token，再进行层级 attention。 | `../assets/papers/flexattention-vlm/fig2_hierarchical_vlm_selection_caption.png` / `(0,0,900,570)` | 理解侧机制 |
| FlexAttention VLM | Table 1 / p.11 | 比较 commercial chatbots、low-resolution VLMs 与 high-resolution VLMs 在 V* Bench 和 MagnifierBench 上的结果，并记录输入分辨率。 | `../assets/papers/flexattention-vlm/table1-vqa-results-caption.png` / `(0,0,900,600)`；PDF crop `(275,260,1175,860)` on 1488x2105 | 主结果与 baseline 边界 |
| FlexAttention VLM | Fig. 4 / p.13 | 左侧比较 random、center 与 attention-map selection；右侧比较 672/1008/1344 分辨率的质量与 TFLOPs。 | `../assets/papers/flexattention-vlm/fig4-selection-resolution-ablation-caption.png` / `(0,0,1050,460)`；PDF crop `(220,210,1270,670)` | selector/resolution 消融 |
| FlexAttention VLM | Table 5 / p.14 | 在单张 NVIDIA V100 32GB 上比较 LLaVA-HD、XAttn、FlexAttn 的 MagnifierBench/TextVQA 平均 TFLOPs 与总推理时间。 | `../assets/papers/flexattention-vlm/table5-v100-latency-caption.png` / `(0,0,700,330)`；PDF crop `(380,950,1080,1280)` | 端到端 latency |
| MInference | Fig. 3 / p.3 | 长上下文 attention head 呈现 A-shape、Vertical-Slash 与 Block-Sparse 三类可被专用 kernel 利用的稀疏模式。 | `../assets/papers/minference/fig3_sparse_patterns_caption.png` / `(0,0,1080,585)` | pattern family |
| MInference | Fig. 4 / p.4 | 三类稀疏模式分别通过规则、在线索引近似或 block 选择进入对应计算路径。 | `../assets/papers/minference/fig4_three_sparse_patterns_caption.png` / `(0,0,1000,430)` | dispatch |
| MInference | Fig. 7 / p.20 | Vertical-Slash 的动态 mask 被编码为合并 range 与独立 column index，供 kernel 遍历。 | `../assets/papers/minference/fig7_vertical_slash_dynamic_mask_caption.png` / `(0,0,595,485)` | metadata |
| MInference | Fig. 10 / p.22 | 1M context 下分解 pattern approximation、index 构造和 sparse kernel 的时延与显存开销。 | `../assets/papers/minference/fig10_kernel_latency_breakdown_caption.png` / `(0,0,915,580)` | planner cost |
| Sparse VideoGen | Fig. 3 / p.3 | 视频 DiT 不同 attention head 分别呈现空间邻域与跨帧同位置的时间模式。 | `../assets/papers/sparse-videogen/fig3_spatial_temporal_head_masks_caption.png` / `(0,0,1260,620)` | mask semantics |
| Sparse VideoGen | Fig. 4 / p.4 | 在线抽样 query rows，对 full、spatial、temporal 输出做近似误差比较并逐 head 选择模式。 | `../assets/papers/sparse-videogen/fig4_svg_workflow_caption.png` / `(0,0,1250,570)` | online profiling |
| Sparse VideoGen | Fig. 5 / p.5 | 时间稀疏访问通过 layout transformation 重排为连续 tile，以改善内存合并访问。 | `../assets/papers/sparse-videogen/fig5_layout_transformation_caption.png` / `(0,0,690,515)` | data layout |
| Sparse VideoGen | Fig. 8 / p.8 | 比较原始稀疏访问与重排后的 kernel latency，显示 layout 对实际速度的影响。 | `../assets/papers/sparse-videogen/fig8_sparse_kernel_latency_caption.png` / `(0,0,675,470)` | kernel latency |
| VMoBA | Fig. 1 / p.1 | 在视频生成质量与 latency 之间比较 full attention、既有稀疏方法与 VMoBA 的折中。 | `../assets/papers/vmoba/fig1_quality_latency_tradeoff_caption.png` / `(0,0,1150,655)` | headline result |
| VMoBA | Fig. 2 / p.4 | VMoBA 先做时空 recurrent partition，再以 gate 选择 blocks，最终用 varlen attention 计算选中块。 | `../assets/papers/vmoba/fig2_vmoba_pipeline_caption.png` / `(0,0,1000,610)` | selector pipeline |
| VMoBA | Fig. 3 / p.4 | 不同层和 head 呈现 temporal、spatial 与 3D neighbor 的 block locality。 | `../assets/papers/vmoba/fig3_spatiotemporal_block_patterns_caption.png` / `(0,0,655,415)` | locality evidence |
| Token Sparse Attention | Fig. 2 / p.2 | 重要 token 会跨 layer 迁移，同一 layer 的不同 head 也需要不同 token 集。 | `../assets/papers/token-sparse-attention/fig2_token_importance_dynamics_caption.png` / `(0,0,1265,325)` | selection motive |
| Token Sparse Attention | Fig. 3 / p.3 | 按 head gather 选中 QKV，执行 compact attention，再 scatter 回原序列并与 residual 合并。 | `../assets/papers/token-sparse-attention/fig3_compress_attention_scatter_caption.png` / `(0,0,1224,510)` | kernel reuse |
| Token Sparse Attention | Fig. 6 / p.7 | 将 selector/index、QKV compression、attention 与 output decompression 的速度和额外开销分解。 | `../assets/papers/token-sparse-attention/fig6_speedup_overhead_caption.png` / `(0,0,1270,355)` | overhead |
| FrameDiT | Table 1 / p.1 | 对比 local、global 与 hybrid attention 在时序连接、复杂度和视频建模能力上的取舍。 | `../assets/papers/framedit/table1_attention_design_tradeoffs_caption.png` / `(0,0,655,540)` | design tradeoff |
| FrameDiT | Fig. 1 / p.2 | FrameDiT 用帧级 matrix attention 替代 token-level temporal full attention，并保留 local/hybrid 变体。 | `../assets/papers/framedit/fig1_matrix_attention_architecture_caption.png` / `(0,0,1270,780)` | architecture |
| FrameDiT | Fig. 3 / p.5 | 视频长度从 16 扩到 128 帧时，对比质量、FLOPs、latency 与 peak memory 的缩放。 | `../assets/papers/framedit/fig3_scaling_video_length_caption.png` / `(0,0,1265,335)` | scaling |
| HASTE | Fig. 4 / p.7 | 在线 Temporal Mask Reuse 与离线 Error-guided Budgeted Calibration 构成互补控制面。 | `../assets/papers/haste/fig4_tmr_ebc_framework_caption.png` / `(0,0,1160,670)` | framework |
| HASTE | Fig. 5 / p.9 | pooled Q/K drift 与 mask 变化相关，用作是否复用稀疏 descriptor 的低成本信号。 | `../assets/papers/haste/fig5_drift_mask_reuse_signal_caption.png` / `(0,0,1240,500)` | reuse gate |
| HASTE | Table 2 / p.14 | 在视频质量、稀疏率和端到端效率上比较 baseline、TMR、EBC 与组合配置。 | `../assets/papers/haste/table2_quality_efficiency_caption.png` / `(0,0,1240,515)` | quality/efficiency |
| LVSA | Fig. 1 / p.3 | Expanded local window 与 rotating global anchors 在固定 attention budget 下补足 basic window 的重叠浪费。 | `../assets/papers/lvsa/fig1_expanded_window_caption.png` / `(0,0,1140,850)` | sparse pattern |
| LVSA | Fig. 2 / p.4 | 全局 anchor 随时间轮转，为长视频提供周期性的远程依赖连接。 | `../assets/papers/lvsa/fig2_rotating_global_anchors_caption.png` / `(0,0,695,500)` | anchors |
| LVSA | Table 1 / p.6 | 在 80GB GPU 上比较 dense、LVSA-SDPA 与 LVSA-FlashInfer 的长视频 wall time、显存与 OOM。 | `../assets/papers/lvsa/table1_wall_time_caption.png` / `(0,0,1190,515)` | runtime evidence |
| LVSA | Fig. 4 / p.6 | 随生成 horizon 增长比较 dense 与 LVSA 的 wall-time scaling。 | `../assets/papers/lvsa/fig4_wall_time_scaling_caption.png` / `(0,0,1190,505)` | scaling |
| Causal-rCM | Fig. 1 / p.1 | 报告流式视频/世界模型在生成质量、训练收敛和在线性能上的总体结果。 | `../assets/papers/causal-rcm/fig1_streaming_performance_caption.png` / `(0,0,1195,525)` | headline result |
| Causal-rCM | Fig. 3 / p.6 | 对比 Teacher Forcing、Diffusion Forcing 与 Self Forcing 的 clean/noisy block mask、训练轨迹和 KV-cache 关系。 | `../assets/papers/causal-rcm/fig3_causal_training_paradigms_caption.png` / `(0,0,1180,515)` | special causal mask |
| Causal-rCM | Fig. 4 / p.7 | 展示先 TF-CM、后 SF-DMD 的分阶段 recipe，以及各训练范式的关系。 | `../assets/papers/causal-rcm/fig4_recipe_comparison_caption.png` / `(0,0,1180,565)` | training recipe |
| Causal-rCM | Fig. 9 / p.17 | Cosmos 3 交互式生成中，时间因果 mask 约束历史与当前 noisy block 的可见性。 | `../assets/papers/causal-rcm/fig9_cosmos3_temporal_causal_mask_caption.png` / `(0,0,1020,690)` | multimodal transfer |

## 跨领域 canonical 资产

| 工作 | 类型 | Caption / 来源 | Canonical 资产 / bbox | 使用 |
|---|---|---|---|---|
| Cosmos 3 | 官方架构图 | MoT 将 reasoner 与 generator 参数路径分离，并在统一 packed multimodal sequence 上协作。 | `../../../../02_model_systems/multimodal_generation/assets/papers/cosmos-3/mot-architecture.png` / `(0,0,1672,763)` | 参数路径 |
| Cosmos 3 | 知识库整理图 | Two-way flat attention 被 lower 为 causal reasoner 与 full generator 两次 varlen attention 调用。 | `../../../../02_model_systems/multimodal_generation/assets/papers/cosmos-3/two-way-attention-infra.png` / `(0,0,942,591)` | kernel lowering |

## QA

- 逐张在原分辨率下检查图体、legend/axis、完整 caption、外边距和相邻正文；contact sheet 仅用于批量初筛。状态：`pass`（2026-07-10），路径复核：`pass`（2026-07-11）。
- 每个 crop 只保留一个编号对象及其 caption；LVSA Table 1 与 Fig.4 已从原合并截图拆开。
- 原论文图用于机制和证据，报告中不将 AI 生成图替换为论文事实图。
- 个别工作没有可审计官方 kernel 代码时，图只支持论文级机制，不被用于证明某个具体 runtime 或 host-device placement。
