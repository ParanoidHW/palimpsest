# ICML 2026 用户题单：模型系统与推理机制综述

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[README](../README.md)
> - 上位汇总：无
> - 证据资产：无（本综述不复制单篇论文资产）
> - 相关文档：[Paper index](../evidence/paper-index.md)，[Figure inventory](../evidence/figure-inventory.md)

## 范围与证据边界

本综述综合用户题单中的 12 篇论文，而不是构造 ICML 接收名单。经一手来源核验，SplAttN 与 ECHO 是 ICML 2026 spotlight，SelfJudge 的 arXiv 元数据标注 ICML 2026，Dual-Latent 有 ICML 官方 poster；DODO 属于 ICML workshop，OnlineSpec 属于 ICLR workshop，其余多篇 venue 尚未全部独立确认。完整状态见 [paper index](../evidence/paper-index.md)。

## 1. 统一生成模型：从噪声核到连续 latent

[XDLM](../papers/xdlm.md#关键实验与归因) 用 stationary kernel 连续连接 mask noise 与 uniform noise，核心价值不是单一最优点，而是把理解与少步生成的冲突显式化为预算相关的 Pareto 权衡。[LatentLM](../papers/latentlm.md#3-研究方法) 则保留 causal Transformer 主干，对连续 token 使用 next-token diffusion head，并用 σ-VAE 控制 latent variance；它把连续模态统一进自回归接口，但端到端收益仍混合了 VAE、diffusion head、GQA 与训练规模。

[DODO](../papers/dodo.md#4-关键结论) 说明离散 diffusion 在 OCR 这类确定性长序列上并非天然稳定：全局 masked diffusion 会出现同步与位置锚定错误，block training 和 block-causal cache 才同时恢复准确率与吞吐。[Flex-Forcing](../papers/flex-forcing.md#32-模型与系统架构) 则在帧轴和去噪轴上动态切分 chunk，以统一 AR、混合和双向视频扩散；完整 source 表明 K-Projection 用于对齐 clean cached keys 与当前噪声空间，但未发布代码，buffer/resume scheduler、dtype、显存和 kernel 行为仍只能按论文报告。

## 2. 多模态路由与参数效率

[LiME](../papers/lime.md#3-研究方法) 通过共享 PEFT 模块、轻量 expert modulator 与表示复用路由，避免每个 expert 复制 adapter；它的直接证据覆盖参数量、训练吞吐和主结果，但“更多专家保留更多任务信息”的理论命题不能替代真实路由负载与尾延迟测量。

[Dual-Latent Memory Routing](../papers/dual-latent-memory-routing.md#52-消融和机制证据) 已按 final PDF 核验双 latent bank、injector、eligibility gate、router、三阶段训练和 appendix latency。替换证据支持 dual bank、trainable injector 与 adaptive budget；Qwen reasoning 的报告延迟从 14.0 s 降至 11.5 s，但 delimiter、loss/reward 项与 serving 尾延迟仍未充分隔离。[OmniFit](../papers/omnifit-layer-compression.md#52-消融和机制证据) 的 final PDF 则确认 LAHP、modality retention planning、ARTS 和 profiling–execution decoupling：20% retention 的平均相对性能为 98.68%，单 H800 报告最高 2.31× TTFT、1.39× TPOT 与约 2.5× 7B VRAM 降低；不过 final PDF 对 anchor provenance、动态 preference weighting 和 prune/merge 生命周期存在内部冲突。两篇的代码与公开评审仍受限，组件收益也不能超出对应消融边界。

## 3. 解码加速：从质量放宽到在线自适应

[SelfJudge](../papers/selfjudge.md#4-关键结论) 以 target model 自监督构造 token acceptability verifier，放宽严格 speculative verification；它提升 accepted length，但变成有损 quality-speed trade-off，阈值和 suffix window 必须按任务校准。

[Multi-Token Self-Distillation](../papers/multi-token-self-distillation.md#3-研究方法) 把已有自回归模型训练成无需独立 verifier 的 standalone MTP 模型；本轮完整 source 与官方 commit `167413e` 验证了 randomized offset/span masks、online teacher feedback 和 ConfAdapt 路径。优势是部署形态简单，但 Figure 12 也直接显示置信度自适应解码的 per-token 控制开销会在并发场景限制扩展。[OnlineSpec](../papers/onlinespec.md#4-关键结论与证据矩阵) 把 target verification feedback 解释为在线学习信号，理论上连接 dynamic regret 与加速率，但其 primary source 是 ICLR workshop，不是 ICML 接收证据。

[ECHO](../papers/echo.md#4-关键结论与证据矩阵) 把高并发 speculative decoding 重新表述为全 batch verification budget 调度：sparse gate 决定截断/扩展，global scheduler 在请求间重分配深度预算，最后 flatten-and-pack 适配 dense kernel。matched ablation 支持 sparse gate 与 depth-aware threshold，但 235B、BS=256 的完整收益仍混合了树构造、调度和 packing。

## 4. 跨论文系统判断

1. **算法指标必须和 serving 指标分开。** accepted length、NED、FID 或准确率不会自动转成吞吐；ECHO、DODO、SelfJudge 与 MTP 都显示调度、cache、batch 和额外 verifier 开销可以改变最终排序。
2. **动态性需要 kernel-compatible 边界。** OnlineSpec 更新模型、MTP 动态选择 chunk、ECHO 动态树预算都会引入控制面成本；只有把动态决策压到稀疏 gate、固定窗口或 pack 阶段，才更可能保留 accelerator 利用率。
3. **缺少 dtype/bandwidth/尾延迟仍是共同缺口。** 多数论文报告 GPU 型号或吞吐，却没有 bytes moved、有效带宽、p95/p99、host-device 开销和 NPU fallback，因此 infra 结论应保持条件化。
4. **venue 与论文质量是独立维度。** 本题单混合 confirmed ICML、workshop、preprint 与未解析条目；目录收录只表示“被要求分析”，不表示接收或 endorsement。

## 5. 本轮源文件刷新：SplAttN 的证据升级

[SplAttN](../papers/splattn.md#3-研究方法) 已从“HTML + 代码可用、PDF/source 截断”升级为完整证据链：arXiv v2 PDF、LaTeX source、ICML Spotlight 页面、固定代码 commit 与公开 checkpoint 元数据均已核验。原论文 [Figure 1](../assets/papers/splattn/fig1-overall-architecture.png) 和 [Figure 8](../assets/papers/splattn/fig8-multimodal-dependency.png) 也完成了严格裁剪和逐图 QA。

这次 source/code 对照带来一个实质性修正：论文把 soft splatting 描述为连续密度并暗示连续坐标梯度，但固定 commit 的实现采用 4×4 有限窗口和整数 scatter index；更稳妥的表述是“离散邻域平滑 + 逆深度归一化”，不能直接把理论层的连续坐标梯度主张当成已实现事实。另一方面，matched ablation 仍支持 soft splat 在 PCN 上带来小幅 CD 改善，KITTI 的视觉移除实验也支持模型确实使用了视觉输入，但 CMIT 与 SCS drop 之间只能解释为相关性证据。

[Flex-Forcing](../papers/flex-forcing.md#4-关键结论) 也已从损坏 PDF 升级为完整 camera-ready PDF/source 和两张 QA-passed 图表。Table 2 的结果不是单向“全面优于”：`[15,3,3]` 在 GB200、NFE5 下相对 Self-Forcing chunk-wise 提升 0.76 VBench Total 且 FPS 增加 0.9，但细粒度 `[3×7]` 在相同 24.9 FPS 下反而低 0.28 Total。由此更合理的结论是 Flex schedule 提供可配置的速度—质量前沿，而非任意 chunk 计划都占优；论文也没有用峰值显存、GPU 数、dtype 或固定内存预算证明“device-budget”收益。

[Multi-Token Self-Distillation](../papers/multi-token-self-distillation.md#8-开源代码对照) 上次缺失的 e-print source 与官方实现也已恢复。代码与论文在 online/offline self-distillation、mask replication、position adjustment 和 confidence-adaptive decoding 上基本对齐；但仓库仍以研究脚本/notebook 为主，checkpoint 的逐 revision 配置未完全冻结。最重要的系统修正来自新提升的 [Figure 12](../assets/papers/multi-token-self-distillation/fig12-throughput-latency.png)：static MTP 能平滑交换 latency 与 throughput，而 ConfAdapt 的逐 token 决策开销在高并发原型中成为瓶颈，不能只用单请求 acceleration factor 推断 serving 排名。

## 6. 建议阅读顺序

1. 生成统一：XDLM → LatentLM → DODO。
2. 多模态参数效率：LiME → Dual-Latent（final PDF 级 memory routing）→ OmniFit（final PDF 级 token compression）。
3. 解码加速：SelfJudge → MTP → OnlineSpec → ECHO。
4. 最后对照阅读 source/code 闭环的 SplAttN、source-complete 但 code-absent 的 Flex-Forcing，以及 final-PDF-complete 但 code/review-absent 的 Dual-Latent 与 OmniFit，区分论文内证据、实现可复现性和系统外推边界。
