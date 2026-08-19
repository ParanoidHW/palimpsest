---
tags:
  - survey
  - collection/llm-foundations
  - domain/model-systems
  - status/deep-review
  - topic/long-context
  - method/hybrid-linear-attention
document_type: survey
domain: llm_foundations
collection: LLM Foundations
review_status: accepted-with-limitations
canonical: true
---

# Linear Attention Transformer 演化

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[LLM Foundations README](../README.md)
> - 证据索引：[Linear attention evidence](../evidence/linear-attention-transformer-evidence.md)
> - 相关 Paper：[Linear Transformer](../papers/linear-transformer.md) · [RetNet](../papers/retnet.md) · [Mamba](../papers/mamba.md) · [Mamba-2 / SSD](../papers/mamba-2-structured-state-space-duality.md) · [GLA](../papers/gated-linear-attention.md) · [DeltaNet](../papers/deltanet.md) · [Gated DeltaNet](../papers/gated-deltanet.md) · [Kimi Linear](../papers/kimi-linear.md) · [Kimi K3](../papers/kimi-k3.md)

## 修订信息

- 当前版本：`2.0.0`
- 当前修订：`rev-linear-attn-20260814`
- 检索截止：`2026-08-14`
- 模式：`hybrid`（方法谱系与系统采用分开计数）

| Revision | Version | Type | Supersedes | 变更与结论影响 |
|---|---:|---|---|---|
| `rev-linear-attention-transformer-initial-20260814` | `1.0.0` | `initial` | none | 旧稿仅能交付 blocked 六篇导航与 Kimi/Qwen 系统摘要。 |
| `rev-linear-attn-20260814` | `2.0.0` | `mixed/content-and-evidence-update` | revision `rev-linear-attention-transformer-initial-20260814`, manifest `7fb480d1291acbf16876b3e71a94adda22814fc26bd82024f528b5db90a2af56` | 扩展至 2026，加入 SSD、KDA、Mamba-3、Gated DeltaNet-2 与系统/kernel/serving 约束；未通过原文和视觉验收的方法不晋升为 canonical Paper。 |

## 一句话结论

线性注意力没有收敛到单一算子，而是收敛到一个系统组合：多数层用固定大小、可遗忘且可纠错写入的状态降低 KV/HBM 流量，少量 full attention 层恢复精确 token-to-token 检索，再用 chunk/scan/WY/DPLR kernel、prefix cache 和 serving backend 把理论 $O(N)$ 变成可测的端到端收益。

## 范围、计数与证据边界

方法 lane 选取 10 个演化节点：Linear Transformer、RetNet、Mamba、Mamba-2/SSD、GLA、DeltaNet、Gated DeltaNet、Kimi Linear/KDA、Mamba-3、Gated DeltaNet-2。2026 年 *Linear Attention Architectures: Mechanisms, Trade-offs, and Cross-Layer Routing* 只作 benchmark/taxonomy 计数，不冒充方法贡献。Qwen3-Next 与 Kimi K3 属于 system-adoption lane，不计入方法论文数量。

证据等级如下：`Paper` 指论文公式/正文/实验；`Code` 指官方或固定实现 locator；`Model` 指官方 model card/config；`Runtime` 指 Transformers、vLLM、SGLang、FLA 等后端入口；`Synthesis` 指跨论文推断。截至本次修订，[Linear Transformer](../papers/linear-transformer.md)、[RetNet](../papers/retnet.md)、[Mamba](../papers/mamba.md)、[Mamba-2 / SSD](../papers/mamba-2-structured-state-space-duality.md)、[GLA](../papers/gated-linear-attention.md)、[DeltaNet](../papers/deltanet.md)、[Gated DeltaNet](../papers/gated-deltanet.md) 与 [Kimi Linear](../papers/kimi-linear.md) 已完成 PDF/source、代码、原图和 schema/semantic 验收；其余方法仍是带限制的机制导航。详细来源与阻断见 [Evidence](../evidence/linear-attention-transformer-evidence.md)。

## 统一术语与符号

| 名称 | 本文中的精确定义 | 不等同于 |
|---|---|---|
| Linear attention | 通过 feature map 和结合律，把历史键值累积成固定状态 | 所有线性时间序列模型 |
| Retention | 在矩阵状态上加入位置衰减，并支持 parallel/recurrent/chunkwise 等价执行 | 一般 softmax attention |
| Selective SSM | 输入依赖地控制状态转移、步长或读写；Mamba 属于这一支 | 严格的 feature-map linear attention |
| SSD | 结构化状态空间与 attention 表示之间的 duality 及块算法 | “SSM 与 attention 完全相同” |
| Delta rule | 擦除当前 key 对应的旧预测，再写入新 value 的误差 | 只做累加的 outer-product memory |
| KDA | Kimi Delta Attention：细粒度 bounded decay 加 delta 写入 | Kimi 的全部模型收益 |
| Full-attention anchor | hybrid 中少量精确注意力层，用于补偿固定状态的检索损失 | 免费的质量恢复；它仍有二次成本 |

统一记号：$S_t$ 是矩阵状态，$q_t,k_t,v_t$ 是当前 query/key/value，$φ$ 是 feature map，$Λ_t$ 是逐输入衰减或门控，$N$ 是序列长度。不同论文中的 $A$、$Δ$、$Λ$ 或 $g$ 含义不同，本文不会把它们强行视为同一参数。

## 从“关联重排”到“有选择地擦写”

Linear Transformer 的核心重排可写为：

$$
S_t=S_{t-1}+φ(k_t)v_t^T, z_t=z_{t-1}+φ(k_t), y_t=\frac{φ(q_t)^TS_t}{φ(q_t)^Tz_t}.
$$

它回答“如何不显式保存 $N\times N$ 注意力矩阵”。$S_t$ 保存历史 key/value 的外积和，$z_t$ 负责归一化，query 只读取固定状态。收益是序列维线性；代价是多个历史 token 被压入同一有限状态，精确检索和冲突更新可能失败。

RetNet 将更新改成带衰减的 $S_t=γS_{t-1}+k_tv_t^T$，把“永不遗忘”改成“随距离减弱”。[GLA](../papers/gated-linear-attention.md) 进一步让门控依赖输入，解决不同内容需要不同记忆时间的问题；其统一 TikZ 图显式展示 key-wise gate、矩阵状态形状、训练分块与固定状态解码。[DeltaNet](../papers/deltanet.md) 则把新写入变为：

$$
δ_t=v_t-S_{t-1}^Tk_t, S_t=S_{t-1}+β_tk_tδ_t^T,
$$

即先计算旧状态对当前 key 的预测误差，再写入纠正量。这比盲目累加更接近 erase-then-write，但仍受状态维度和 key 冲突约束。其 canonical Paper 的统一 TikZ 图把 token 级 read-error-write、固定状态 decode 与训练期 WY/UT chunk 边界放在同一视图；论文 kernel speedup 不能外推为端到端模型吞吐。[Gated DeltaNet](../papers/gated-deltanet.md) 把标量衰减门与 delta 写入结合，在同一固定状态里区分“全局清除”和“当前 key 定向修改”。[Kimi Linear](../papers/kimi-linear.md) 再把 decay 细化到 key 通道，并用受约束 DPLR 降低 chunk kernel 工作；2025 报告中的 gate 不含后来 Kimi K3 使用的 lower bound，两者必须分开归因。

Mamba/Mamba-2 的递推外形与上述状态模型相似，但语义属于 selective SSM：输入控制状态转移/离散化参数，并依赖 selective scan 或 SSD 块算法。把它们纳入谱系有助于比较 kernel 和状态机制，把它们直接称为 linear attention 则会掩盖理论差异。

## 2020-2026 谱系

| 年份 | 工作 | 它解决的具体问题 | 核心变化 | 训练/推理形态 | 主要限制 |
|---:|---|---|---|---|---|
| 2020 | Linear Transformer | softmax attention 的二次序列成本 | feature-map 外积前缀状态 | parallel train / recurrent decode | 固定状态与归一化限制 |
| 2023 | RetNet | 并行训练与递推推理统一 | decayed retention | parallel / recurrent / chunkwise | 长程精确信息可能衰减 |
| 2023 | Mamba | SSM 缺少内容选择，scan 不适配 GPU | selective SSM + hardware-aware scan | fused scan / recurrent | 非严格 linear attention；kernel 依赖强 |
| 2023-24 | [GLA](../papers/gated-linear-attention.md) | 固定遗忘不足、chunk I/O 高 | input-dependent gate + FlashLinearAttention | chunkwise matrix kernel | 状态矩阵读写仍昂贵；组件级归因不完整 |
| 2024 | Mamba-2/SSD | SSM 与矩阵硬件映射不佳 | SSM-attention duality + block algorithm | Tensor-Core-friendly blocks | duality 不保证同等表达力 |
| 2024 | [DeltaNet](../papers/deltanet.md) | 新旧键值冲突 | delta erase-then-write + WY/UT | parallel chunks / recurrent | 仍有有限状态冲突 |
| 2024-25 | [Gated DeltaNet](../papers/gated-deltanet.md) | gate 和 delta 各自不完整 | scalar decay gate + delta write | WY/UT chunks / recurrent decode | hybrid 组件收益与训练配方混杂；公开评审正文不可得 |
| 2025 | Kimi Linear/KDA | 长上下文质量、KV cache 与吞吐同时受限 | bounded decay + delta；KDA/MLA hybrid | FlashKDA/KCP + prefix cache | 公开 matched ablation 不完整 |
| 2026 | Mamba-3 | 状态表达与多输入多输出能力 | complex-valued/MIMO state | 新 kernel 路径 | 版本与部署证据仍在演化 |
| 2026 | Gated DeltaNet-2 | erase/write 耦合 | 分离擦除与写入控制 | chunk/runtime 路径待核验 | 缺稳定同预算比较 |

谱系关系不是一条直线：Mamba-1/2/3 是 selective SSM 分支；GLA -> DeltaNet -> Gated DeltaNet -> Gated DeltaNet-2 是矩阵状态的 gate/erase/write 分支；KDA 吸收 delta 写入和细粒度 decay，并在 Kimi K3 中与 MLA 混合。Mamba-2 的 SSD 是两支之间的重要表示/实现桥梁，但不能抹掉它们的状态语义差异。

## 系统采用：Qwen3-Next 与 Kimi K3

### Qwen3-Next

官方 model card/config 显示 Qwen3-Next-80B-A3B 使用 48 层，以四层为周期安排 `3 Gated DeltaNet + 1 Gated Attention`。linear branch 配置为 16 个 QK heads、32 个 V heads、128 维 head、4-token causal convolution；原生 context 为 262,144，YaRN 路径扩展到 1M。实现线索分布在官方配置、FLA/causal-conv1d 依赖，以及 Transformers、vLLM、SGLang 的模型与 backend 路径。

这里能建立的是“原生采用与实现 locator”，不能把 Qwen3-Next 的整体质量或吞吐提升归因给 Gated DeltaNet：MoE、数据、训练 token、量化、batching、kernel 和 scheduler 都是混杂变量。

### Kimi K3

[Kimi K3](../papers/kimi-k3.md) 使用 69 层 KDA 与 24 层 Gated MLA。KDA 采用 bounded log-decay 和 delta-rule 状态更新，系统侧还包括 FlashKDA、Kimi Delta Attention 的 chunkwise parallel kernel（KCP）与双粒度 prefix cache。原论文结构、decay、训练重叠和 prefix-cache 图表均由 canonical Paper 持有，Survey 仅链接、不复制资产。

两套系统共同指向 hybrid：多数线性状态层节省 KV/HBM 流量，周期性 full-attention/MLA 层承担精确检索锚点。区别在于状态结构、层比例、kernel 与 cache 设计，不能只用“3:1”或“69:24”比较优劣。

## Kernel、硬件与 serving 约束

- `scan` 适合 selective SSM 的依赖链；`chunkwise/WY/DPLR` 把时间依赖重组为块矩阵乘，才能更充分使用 Tensor Core。
- 理论固定状态减少随 $N$ 增长的 KV cache，但每 token 仍要读写 $S_t$。当状态矩阵大、复用差或未融合时，瓶颈可能从容量转成 HBM 带宽。
- 端到端有效带宽应按 $B_{eff}=bytes\ moved/runtime$ 估算，利用率为 $B_{eff}/B_{peak}$。没有 bytes/runtime telemetry 时，不应从 $O(N)$ 推导实际吞吐。
- bf16/fp16/fp8 的状态存储、累加精度、layout transform 和 causal-conv fusion 会改变数值稳定性与可达带宽；论文速度不可脱离 dtype 和硬件复现。
- 多卡训练还要处理 chunk 边界状态、tensor/sequence parallel 通信和计算-通信重叠；固定状态并不自动消除跨 rank 通信。
- serving 需要 backend 实现 recurrent state、hybrid 层 KV、continuous batching、prefix cache 和 checkpoint/config 兼容。native adoption、optional official backend、third-party integration 必须分开计数。
- GPU/NPU 的算子库、片上 SRAM、DMA、图编译和 fallback 路径不同；CUDA kernel 的优势不能直接外推到 NPU。

## 同预算证据与归因边界

公平比较至少锁定参数量、训练数据与 token、上下文分布、优化器、精度、batch、硬件和 serving backend。当前公开结果常同时改变 architecture、data、kernel、cache 和 scheduler；因此“模型整体胜出”最多支持系统组合有效，不能单独证明某个 gate、delta rule 或 hybrid 比例造成全部收益。

可信的组件归因需要 matched ablation：只替换 gate、写入规则、full-attention 周期或 kernel，并同时报告质量、训练吞吐、decode latency、峰值内存和有效带宽。缺少这种证据时，本文只写“机制可解释”或“系统采用”，不写“已证明最优”。

## 当前共识、争议与下一步

**共识**：可遗忘的固定状态能显著改变长上下文内存增长；delta erase/write 比单纯累加更能处理冲突；少量 full attention 往往是精确检索锚点；块算法和 kernel fusion 决定理论复杂度能否转化为系统收益。

**争议**：Mamba 应否被纳入 linear attention 名称；KDA、Mamba-3 与 Gated DeltaNet-2 是否存在真正同预算比较；状态容量、跨层路由和 full-attention 周期应固定还是输入依赖；低精度和 NPU 上的稳定性、带宽利用率及多租户 prefix cache 仍缺公开证据。

**下一步**：建立状态容量/检索误差的可解释指标；发布固定数据与 backend 的 matched ablation；联合优化 hybrid 层路由、prefix cache 和 scheduler；为 GPU/NPU 提供可复现的 fused erase-write/scan；把 runtime telemetry 与模型质量一起报告。

## 结论

2020-2026 的主线不是“用一个线性算子取代 attention”，而是把历史压缩、遗忘、冲突擦写、精确检索和硬件执行拆成可组合部件。Linear Transformer 给出固定状态起点；RetNet/GLA 引入衰减；DeltaNet 系列处理写入冲突；Mamba/SSD 推动选择性状态和块硬件算法；KDA 与 Qwen3-Next/Kimi K3 的 hybrid 部署把方法问题变成 kernel、cache 和 serving 的联合设计问题。

本版是机制与系统导航；当前已有 Linear Transformer、RetNet、Mamba、Mamba-2/SSD、Kimi K3 五个相关 canonical Paper 链接，其余方法不冒充已验收证据。后续只有在 PDF/source、两类原论文视觉、代码 commit 与 schema/semantic checks 全部通过后，才能把对应条目升级为 canonical Paper，并同步覆盖矩阵。
