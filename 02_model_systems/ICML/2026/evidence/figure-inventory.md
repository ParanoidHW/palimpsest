# ICML 2026 用户题单正式 Figure Inventory

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Survey](../surveys/icml-2026-selected-papers.md)
> - 证据资产：[`../assets/papers/`](../assets/papers/)
> - 相关文档：[Paper index](paper-index.md)

本清单只记录正式目录中的 31 个资产。caption 列保留原 caption 或其完整中文转述；bbox 坐标系均以渲染页左上角为原点，格式 `(x,y,width,height)`。所有资产在子任务 contact sheet 初筛后，由父级再次以原始分辨率逐图打开；父级发现并修正/排除了 SplAttN、Flex-Forcing、SelfJudge、OnlineSpec、MTP 和 ECHO 的边界问题。

## splattn

| Object | Source | Crop | Caption（完整原文） | Usage | QA |
|---|---|---|---|---|---|
| Figure 1 | arXiv:2605.01466v2，PDF p2，2550×3300，300 DPI | `(216,278,2048,900)`；[asset](../assets/papers/splattn/fig1-overall-architecture.png) | **The overall architecture of our proposed SplAttN.** The pipeline consists of two integral stages. **(a) Dual-Branch Feature Extraction.** The GS-Bridge branch extracts comprehensive global representations by using geometric tokens \(\mathcal{F}_{geo}\) to actively query visual features \(\mathcal{F}_{vis}\) derived from Gaussian Soft Splatting. In parallel, the Local Encoder captures topology-aware local details \(\mathcal{F}_l\) through an EdgeConv module followed by Multi-Head Self-Attention and projection. **(b) Global-Local Decoder.** This module unifies the generation process. It first predicts a sparse skeleton \(\mathcal{P}_0\) from the global feature \(\mathcal{F}_g\) via an MLP, incorporating input priors through the \(\mathcal{P}_{in}\)-Merge module. Subsequently, it hierarchically upsamples the point cloud \((\mathcal{P}_0 \to \mathcal{P}_2)\). As detailed in the decoding block, each upsampling stage integrates Structure Self-Attention to model geometric consistency and Cross-Attention to inject the extracted local features \(\mathcal{F}_l\) (as \(\mathcal{K},\mathcal{V}\)) for fine-grained refinement. | [SplAttN](../papers/splattn.md#33-模型系统架构) | 2026-07-24 contact sheet 初筛与父级原分辨率逐图 QA 均通过；单一 Figure 1、caption 完整、边界紧。 |
| Figure 8 | 同上，PDF p8，2550×3300 | `(1265,260,1000,875)`；[asset](../assets/papers/splattn/fig8-multimodal-dependency.png) | **Verification of Multi-Modal Dependency.** We compare SCS sensitivity against Cross-Modal Information Throughput (CMIT). Unlike baselines with low CMIT showing negligible sensitivity, SplAttN achieves a dominant CMIT of **200.5**. This high throughput strictly correlates with a substantial consistency drop upon visual removal, confirming a valid cross-modal dependency rather than template retrieval. | [SplAttN](../papers/splattn.md#41-scscmit-结果与证据边界) | 初裁混入页眉后被拒绝并重裁；最终 crop 通过 contact sheet 与父级原分辨率 QA，单一 Figure 8、caption 完整。 |

## flex-forcing

| Object | Source | Crop | Caption（完整原文） | Usage | QA |
|---|---|---|---|---|---|
| Figure 3 | arXiv:2607.03509v1，PDF p3，1700×2200，200 DPI | `(140,190,1420,470)`；[asset](../assets/papers/flex-forcing/fig3-flexible-chunking-mechanism.png) | **Figure 3.** (Left) Flexible chunking for bridging the autoregressive and bidirectional video generation. Flex-Forcing adjusts chunk granularity across noise levels while a unified self-attention mechanism supports both causal and bidirectional inference. (Right) The mixed attention with causal tokens and non-causal tokens. We add a timestep dependent K-Projection at the clean cache from past frames. | [Flex-Forcing](../papers/flex-forcing.md#32-模型与系统架构) | 2026-07-24 contact sheet 与父级原分辨率 QA 通过；单一 Figure 3、caption 完整、标签可读。 |
| Table 2 | 同上，PDF p6，1700×2200 | `(835,755,675,695)`；[asset](../assets/papers/flex-forcing/table2-five-second-performance.png) | **Table 2.** Comparisons of performance for 5s videos. *: We sample videos from the official checkpoint and test its performance. Here, the NFE of the causal distillation method contains N steps for denoising and 1 step for caching. | [Flex-Forcing](../papers/flex-forcing.md#41-5-秒主结果质量与速度分开看) | 初裁截断 caption 后被拒绝并重裁；最终单一 Table 2、caption 完整，contact sheet 与父级原分辨率 QA 通过。 |

## xdlm

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 1 | arXiv:2602.01362v1，PDF p2，1360×1760，160 DPI | `(100,130,1160,500)`；[asset](../assets/papers/xdlm/fig1-stationary-kernel-tradeoff.png) | 左图以 stationary kernel 连接 UDLM 的 uniform noise 与 MDLM 的 absorbing mask；右图比较 zero-shot PPL 与 32-step generation PPL，并把 `k=0.1` 标为 sweet spot。 | [XDLM](../papers/xdlm.md#问题方法与证据链) | 2026-07-17 父级原分辨率通过；单一对象、caption 完整、边界紧。 |
| Figure 3 | 同上，PDF p7，1360×1760 | `(100,140,570,920)`；[asset](../assets/papers/xdlm/fig3-llada-xdlm.png) | 评估把 LLaDA-8B 适配为 LLaDA-XDLM：多基准整体优于 baseline，MBPP 的 generation failure 明显减少。 | [XDLM](../papers/xdlm.md#关键实验与归因) | 通过。 |
| Figure 4 | 同上，PDF p7，1360×1760 | `(680,140,580,790)`；[asset](../assets/papers/xdlm/fig4-training-dynamics.png) | 文本与图像生成的训练动态；背景色表示阶段占优模型，颜色切换表示性能交叉点。 | [XDLM](../papers/xdlm.md#关键实验与归因) | 通过。 |

## latentlm

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 2 | arXiv:2412.08635v1，PDF p3，1530×1980，180 DPI | `(240,110,1060,710)`；[asset](../assets/papers/latentlm/fig2-latentlm-architecture.png) | LatentLM 统一连续与离散数据：σ-VAE 把连续数据编码为 latent vectors，causal Transformer 逐 token 建模，diffusion head 条件于 Transformer state 生成连续 vectors，最后由 decoder 还原输出。 | [LatentLM](../papers/latentlm.md#3-研究方法) | 2026-07-17 父级原分辨率通过。 |
| Figure 7 | 同上，PDF p9，1530×1980 | `(240,100,1060,570)`；[asset](../assets/papers/latentlm/fig7-inference-throughput.png) | 比较 DiT 与 LatentLM 在不同模型规模、batch size 下的 inference throughput；GQA 指 grouped-query attention。 | [LatentLM](../papers/latentlm.md#4-关键结论) | 通过。 |

## lime

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 1 | arXiv:2604.02338v1，PDF p1，1020×1320，120 DPI | `(80,290,860,360)`；[asset](../assets/papers/lime/fig1-architecture.png) | 对比 MoE-LoRA 的逐 expert adapter/router 与 LiME 的共享 PEFT + 轻量 modulator；同时展示表示复用零参数路由、n-gram routing、Auto Top-K 和 load balancing。 | [LiME](../papers/lime.md#3-研究方法) | 2026-07-17 父级原分辨率通过。 |
| Table 2 | 同上，PDF p6，1020×1320 | `(80,95,860,380)`；[asset](../assets/papers/lime/table2-main-results.png) | 七类 benchmark 的平均结果；LiME 行高亮，粗体/下划线分别表示第一/第二，`#TTP` 是总 trainable parameters。 | [LiME](../papers/lime.md#4-关键结论) | 通过。 |
| Figure 2 | 同上，PDF p6，1020×1320 | `(80,485,860,320)`；[asset](../assets/papers/lime/fig2-efficiency.png) | 比较吞吐、训练时间、peak memory、trainable parameters 和总模型大小；LiMEPromptTuning 最快，frozen backbone 主导峰值显存，LiME 最多减少 4× trainable parameters。 | [LiME](../papers/lime.md#7-infra-需求分析) | 通过。 |

## selfjudge

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 1 | arXiv:2510.02329v2，PDF p2，1530×1980，180 DPI | 父级重裁 `(120,170,1290,420)`；[asset](../assets/papers/selfjudge/fig1-domain-comparison.png) | GSM8K/MMLU 上比较 SD 方法的 inference efficiency 与任务表现；AutoJudge 在数学有效但跨域退化，SelfJudge 在两域保持较一致表现；γ 为每轮 draft token 数。 | [SelfJudge](../papers/selfjudge.md#4-关键结论) | 2026-07-17 父级移除页眉后通过。 |
| Figure 2 | 同上，PDF p4，1530×1980 | 父级重裁 `(110,165,1310,710)`；[asset](../assets/papers/selfjudge/fig2-training-data-generation.png) | SelfJudge 训练数据生成：替换 mismatch token，用 target likelihood 比较语义保持度，超过阈值 τ 标 acceptable，再训练 inference verifier。 | [SelfJudge](../papers/selfjudge.md#3-研究方法) | 父级移除页眉后通过。 |
| Figure 3 | 同上，PDF p7，1530×1980 | `(110,495,1310,515)`；[asset](../assets/papers/selfjudge/fig3-speed-performance.png) | 搜索各方法阈值，报告 accuracy 与对应 average accepted length 的速度/质量曲线。 | [SelfJudge](../papers/selfjudge.md#4-关键结论) | 通过。 |
| Figure 4 | 同上，PDF p9，1530×1980 | 父级重裁 `(110,165,1310,410)`；[asset](../assets/papers/selfjudge/fig4-suffix-window.png) | 比较 suffix length `N`；semantic score 纳入未来 `N` 个 token 的 likelihood。 | [SelfJudge](../papers/selfjudge.md#4-关键结论) | 父级移除页眉和后续正文后通过。 |

## onlinespec

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 1 | arXiv:2603.12617v1，PDF p2，1700×2200，200 DPI | `(300,160,1120,405)`；[asset](../assets/papers/onlinespec/fig1-generation-refinement.png) | generation-refinement：draft 快速提交序列，target 验证并提供 feedback，形成“draft commits → feedback provides → draft adapts”循环。 | [OnlineSpec](../papers/onlinespec.md#3-研究方法) | 2026-07-17 父级原分辨率通过。 |
| Table 1 | 同上，PDF p8，1700×2200 | `(285,150,1145,700)`；[asset](../assets/papers/onlinespec/table1-main-results.png) | 跨 benchmark 比较 generation-refinement 方法，报告三次运行的 AvgLen 与 wall-clock SpeedUp 均值/标准差，粗体为最佳。 | [OnlineSpec](../papers/onlinespec.md#4-关键结论与证据矩阵) | 通过。 |
| Table 2 | 同上，PDF p8，1700×2200 | `(285,850,1145,360)`；[asset](../assets/papers/onlinespec/table2-reasoning-results.png) | reasoning benchmark 上报告 target/draft 组合的 AvgLen、括号内 wall-clock speedup 与 accuracy，三次运行均值/标准差。 | [OnlineSpec](../papers/onlinespec.md#4-关键结论与证据矩阵) | 通过。 |
| Figure 3 | 同上，PDF p9，1700×2200 | 父级重裁 `(285,150,1145,405)`；[asset](../assets/papers/onlinespec/fig3-tps-evolution.png) | GSM8K 上 Opt-Hydra、Ens-EAGLE、Ens-EAGLE-3、Online-LR 的 TPS 随部署迭代演化。 | [OnlineSpec](../papers/onlinespec.md#4-关键结论与证据矩阵) | 父级移除下一节标题后通过；Figure 2 因 caption 截断未提升。 |

## multi-token-self-distillation

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 1 | arXiv:2602.06019v2，PDF p1，1530×1980 | `(250,1240,1030,530)`；[asset](../assets/papers/multi-token-self-distillation/fig1-gsm8k-chunks.png) | Qwen3-4B MTP 的 GSM8K 示例：90% confidence-adaptive、无二次验证，每个色块是一轮 forward 生成的 1–7 token chunk，平均 chunk 3.04。 | [MTP](../papers/multi-token-self-distillation.md#4-关键结论) | 2026-07-17 父级原分辨率通过。 |
| Figure 2 | 同上，PDF p6，1530×1980 | `(250,165,1030,470)`；[asset](../assets/papers/multi-token-self-distillation/fig2-tokenization-masking.png) | 展示 sequence tokenization/masking、多个 MTP region、target replication 与 position adjustment；online objective 的 target 来自 teacher feedback，可在单序列并行物化多个 MTP 问题。 | [MTP](../papers/multi-token-self-distillation.md#3-研究方法) | 通过。 |
| Figure 3 | 同上，PDF p7，1530×1980 | `(250,175,1030,435)`；[asset](../assets/papers/multi-token-self-distillation/fig3-attention-masks.png) | rolling offset 与 variable `k` attention masks，使同一训练覆盖不同 prefix length 与 MTP window。 | [MTP](../papers/multi-token-self-distillation.md#3-研究方法) | 通过。 |
| Figure 4 | 同上，PDF p8，1530×1980 | `(250,175,1040,675)`；[asset](../assets/papers/multi-token-self-distillation/fig4-accuracy-acceleration.png) | 两个 MTP LM 在 GSM8K 上约 100k steps 后的 acceleration factor–accuracy Pareto；adaptive decoding 呈 Pareto-optimal trade-off。 | [MTP](../papers/multi-token-self-distillation.md#4-关键结论) | 通过。 |
| Figure 12 | 同上，PDF p23，1530×1980 | 父级重裁 `(250,420,1030,760)`；[asset](../assets/papers/multi-token-self-distillation/fig12-throughput-latency.png) | 比较 L3.1-8B-Magpie（单 GPU）与 Qwen 32B（4 GPU tensor parallel）的吞吐—单请求 latency；static MTP 平滑交换二者，而 ConfAdapt 的逐 token 开销在原型实现中限制并发扩展。 | [MTP](../papers/multi-token-self-distillation.md#76-调度serving自定义算子) | 2026-07-24 contact sheet 和父级原分辨率 QA 通过；单一 Figure 12、caption 完整、无邻接正文。 |

## dodo

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 4 | arXiv:2602.16872v2，PDF p5，1836×2376，216 DPI | `(110,205,780,460)`；[asset](../assets/papers/dodo/fig4-full-vs-block-diffusion.png) | full diffusion 全序列并行 sampling；block diffusion 限制并行窗口并按 block 从左到右处理。 | [DODO](../papers/dodo.md#3-研究方法) | 2026-07-17 父级原分辨率通过。 |
| Figure 5 | 同上，PDF p6，1836×2376 | `(910,1580,905,625)`；[asset](../assets/papers/dodo/fig5-throughput-comparison.png) | DODO 结合 parallel decoding、block-causal attention 与 KV cache，报告约 104 token/s 和约 5× 相对 AR baseline。 | [DODO](../papers/dodo.md#4-关键结论) | 通过。 |
| Table 2 | 同上，PDF p7，1836×2376 | `(105,170,815,395)`；[asset](../assets/papers/dodo/table2-block-structure-ablation.png) | Vanilla MDM 即使 oracle length 仍失败，block-wise training 是关键。 | [DODO](../papers/dodo.md#4-关键结论) | 通过。 |
| Table 3 | 同上，PDF p7，1836×2376 | `(895,170,925,665)`；[asset](../assets/papers/dodo/table3-block-size-cache.png) | block size/cache 对比：approximate KV cache 崩溃，block-causal training 支持 exact cache 与 5× speedup。 | [DODO](../papers/dodo.md#7-infra-需求分析) | 通过。 |

## echo

| Object | Source | Crop | Caption（完整中文转述） | Usage | QA |
|---|---|---|---|---|---|
| Figure 3 | arXiv:2604.09603v2，PDF p4，1489×2105，180 DPI | 父级重裁 `(135,190,1220,900)`；[asset](../assets/papers/echo/fig3-framework.png) | ECHO pipeline：continuous batch → sparse-gated super-tree → global cap 下的低负载 request 内宽度扩展/高负载 request 间深度重分配 → flatten-and-pack → single-pass target verification。 | [ECHO](../papers/echo.md#3-研究方法) | 2026-07-17 父级补全 caption 后通过。 |
| Figure 5 | 同上，PDF p10，1489×2105 | `(135,190,1220,830)`；[asset](../assets/papers/echo/fig5-high-load-results.png) | BS>1 高负载主结果：四组模型、三项 benchmark，对比 EAGLE3、ECHO(dense/fixed) 与完整 ECHO，列下百分比为相对 EAGLE3 最大提升。 | [ECHO](../papers/echo.md#4-关键结论与证据矩阵) | 父级原分辨率通过。 |

## 排除记录

- Dual-Latent、OmniFit：当前没有可满足单一编号对象 + 完整 caption + 原分辨率 QA 的正式图表。
- SplAttN Figure 8 初裁：混入页眉，已重裁后提升。
- Flex-Forcing Table 2 初裁：caption 最后一行截断，已重裁后提升。
- SelfJudge 初始 Figure 1/2/4：含页眉或后续正文，已重裁后提升。
- OnlineSpec Figure 2：caption 被截断，未提升；Figure 3 去掉下一节标题后提升。
- MTP Figure 12 初裁：顶部混入前文且底部 caption 截断；本轮重裁后提升。
- ECHO Figure 3：初始 crop caption 最后一行截断，已从 page render 扩展 bbox 后提升。
