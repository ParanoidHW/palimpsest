# ICML 2026 用户题单：模型系统与推理机制综述

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[README](../README.md)
> - 上位汇总：无
> - 证据资产：无（本综述不复制单篇论文资产）
> - 相关文档：[Paper index](../evidence/paper-index.md)，[Figure inventory](../evidence/figure-inventory.md)

## 范围与证据边界

本综述综合用户题单中的 12 篇论文，而不是构造 ICML 接收名单。经一手来源核验，ECHO 是 ICML 2026 spotlight，SelfJudge 的 arXiv 元数据标注 ICML 2026，Dual-Latent 有 ICML 官方 poster；DODO 属于 ICML workshop，OnlineSpec 属于 ICLR workshop，其余多篇 venue 未独立确认。完整状态见 [paper index](../evidence/paper-index.md)。

## 1. 统一生成模型：从噪声核到连续 latent

[XDLM](../papers/xdlm.md#关键实验与归因) 用 stationary kernel 连续连接 mask noise 与 uniform noise，核心价值不是单一最优点，而是把理解与少步生成的冲突显式化为预算相关的 Pareto 权衡。[LatentLM](../papers/latentlm.md#3-研究方法) 则保留 causal Transformer 主干，对连续 token 使用 next-token diffusion head，并用 σ-VAE 控制 latent variance；它把连续模态统一进自回归接口，但端到端收益仍混合了 VAE、diffusion head、GQA 与训练规模。

[DODO](../papers/dodo.md#4-关键结论) 说明离散 diffusion 在 OCR 这类确定性长序列上并非天然稳定：全局 masked diffusion 会出现同步与位置锚定错误，block training 和 block-causal cache 才同时恢复准确率与吞吐。题单中的 [Flex-Forcing](../papers/flex-forcing.md#来源与证据边界) 试图统一双向与自回归 video diffusion，但本次 PDF 损坏，无法把摘要主张提升为已验证结论。

## 2. 多模态路由与参数效率

[LiME](../papers/lime.md#3-研究方法) 通过共享 PEFT 模块、轻量 expert modulator 与表示复用路由，避免每个 expert 复制 adapter；它的直接证据覆盖参数量、训练吞吐和主结果，但“更多专家保留更多任务信息”的理论命题不能替代真实路由负载与尾延迟测量。

[Dual-Latent Memory Routing](../papers/dual-latent-memory-routing.md#3-研究方法设计动机与证据边界) 的官方摘要提出视觉/推理双 latent memory 与动态 routing，但缺少 PDF、公式和实验表，因此只保留摘要级设计线索。[OmniFit](../papers/omnifit-layer-compression.md#证据与状态声明) 的精确论文身份仍未恢复，不能用同名 3D body-fitting 工作替代。

## 3. 解码加速：从质量放宽到在线自适应

[SelfJudge](../papers/selfjudge.md#4-关键结论) 以 target model 自监督构造 token acceptability verifier，放宽严格 speculative verification；它提升 accepted length，但变成有损 quality-speed trade-off，阈值和 suffix window 必须按任务校准。

[Multi-Token Self-Distillation](../papers/multi-token-self-distillation.md#3-研究方法) 把已有自回归模型训练成无需独立 verifier 的 standalone MTP 模型；优势是部署形态简单，代价是置信度自适应解码的 per-token 控制开销会在并发场景限制扩展。[OnlineSpec](../papers/onlinespec.md#4-关键结论与证据矩阵) 把 target verification feedback 解释为在线学习信号，理论上连接 dynamic regret 与加速率，但其 primary source 是 ICLR workshop，不是 ICML 接收证据。

[ECHO](../papers/echo.md#4-关键结论与证据矩阵) 把高并发 speculative decoding 重新表述为全 batch verification budget 调度：sparse gate 决定截断/扩展，global scheduler 在请求间重分配深度预算，最后 flatten-and-pack 适配 dense kernel。matched ablation 支持 sparse gate 与 depth-aware threshold，但 235B、BS=256 的完整收益仍混合了树构造、调度和 packing。

## 4. 跨论文系统判断

1. **算法指标必须和 serving 指标分开。** accepted length、NED、FID 或准确率不会自动转成吞吐；ECHO、DODO、SelfJudge 与 MTP 都显示调度、cache、batch 和额外 verifier 开销可以改变最终排序。
2. **动态性需要 kernel-compatible 边界。** OnlineSpec 更新模型、MTP 动态选择 chunk、ECHO 动态树预算都会引入控制面成本；只有把动态决策压到稀疏 gate、固定窗口或 pack 阶段，才更可能保留 accelerator 利用率。
3. **缺少 dtype/bandwidth/尾延迟仍是共同缺口。** 多数论文报告 GPU 型号或吞吐，却没有 bytes moved、有效带宽、p95/p99、host-device 开销和 NPU fallback，因此 infra 结论应保持条件化。
4. **venue 与论文质量是独立维度。** 本题单混合 confirmed ICML、workshop、preprint 与未解析条目；目录收录只表示“被要求分析”，不表示接收或 endorsement。

## 5. 建议阅读顺序

1. 生成统一：XDLM → LatentLM → DODO。
2. 多模态参数效率：LiME → Dual-Latent（摘要级）。
3. 解码加速：SelfJudge → MTP → OnlineSpec → ECHO。
4. 最后阅读 SplAttN、Flex-Forcing 与 OmniFit 的 blocked 文档，理解当前证据缺口，而不是把缺口当负面实验结论。
