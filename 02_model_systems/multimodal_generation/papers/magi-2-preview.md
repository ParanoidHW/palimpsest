---
tags:
  - paper
  - collection/multimodal-generation
  - domain/model-systems
  - status/deep-review
  - topic/audio-video-generation
  - method/multi-head-latent-moe
---

# MAGI-2 Preview: Scaling Video Generation Models Efficiently 深度评审

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 模型多模态演进调研](../surveys/diffusion-evolution.md)
> - 证据资产：`../assets/papers/magi-2-preview/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

> 资料状态：本文评审 Sand.ai 于 2026-08-05 发布的官方技术报告网页。官方网页受 WAF 阻断，未获得可归档 PDF 或完整 HTML；作者声明主要来自官方页面的搜索索引片段，架构、配置与推理路径由官方代码提交 `f68a0f9bbccbea56e0177a9bd912abc3b18ffe61` 交叉核验。报告未公开完整训练代码、训练集群规模、训练成本、质量主表或受控消融，因此训练收益与扩展效率均按证据边界表述。

## 修订信息

- 当前文档版本：`1.2.0`
- 当前修订 ID：`rev-magi-2-preview-scope-cleanup-20260922`
- 当前修订时间：`2026-09-22T00:00:00+08:00`
- 替代版本：`rev-magi-2-preview-code-audit-20260920` / `1.1.0`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 变更摘要 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|
| `rev-magi-2-preview-initial-20260920` | `1.0.0` | `2026-09-20T20:12:06+08:00` | Hermes Agent | initial | 无 | 建立官方技术报告、固定代码提交、模型配置和训练 Infra 的证据化解读 | 官方报告索引片段、官方代码与配置、知识库整理图 | material |
| `rev-magi-2-preview-code-audit-20260920` | `1.1.0` | `2026-09-20T20:50:16+08:00` | Hermes Agent | evidence-update | `rev-magi-2-preview-initial-20260920` / `1.0.0` / `41e6d57b4c8e3abf6244cc3cd00530380d5d367231e4ab8506c083e168a82af5` | 补充参数量复算、head padding、CP/EP rank 复用、Refiner 视频-only 路径与确定性开关边界 | 独立代码审计与固定提交源码 | minor |
| `rev-magi-2-preview-scope-cleanup-20260922` | `1.2.0` | `2026-09-22T00:00:00+08:00` | Codex | editorial-cleanup | `rev-magi-2-preview-code-audit-20260920` / `1.1.0` | 移除特定硬件合作语境及其整理图，保留通用系统分析 | 用户指定范围清理 | minor |

## 0. 资料与配图索引

| 对象 | 状态 | 位置 / 版本 | 用途 |
|---|---|---|---|
| 官方技术报告 | 可检索、正文直连受限 | [Sand.ai 技术报告网页](https://sand.ai/blog/magi-2-preview)，2026-08-05 | 作者动机、Head Parallel、MagiMoE、MagiMuon 与数据方法声明 |
| 官方代码 | 已固定 | [SandAI-org/MAGI-2-preview](https://github.com/SandAI-org/MAGI-2-preview/commit/f68a0f9bbccbea56e0177a9bd912abc3b18ffe61) | 模型结构、路由、EP/CP、内核、offload 与 checkpoint 分片 |
| 模型权重 | 公开但未下载 | [sand-ai/MAGI-2-preview](https://huggingface.co/sand-ai/MAGI-2-preview) | 官方 README 报告总量约 307 GB；本次未下载逐 tensor 审计 |
| OpenReview | 未发现 | 不适用 | 无公开评审、decision 或 rebuttal 可交叉核验 |
| 原报告 Figure/Table | 无可接受资产 | WAF 阻断；第三方网页图片不是报告图，已拒绝提升 | 不以第三方卡片冒充论文证据 |

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| Multi-Head LatentMoE | 把 3072 维隐藏状态拆成 12 个 256 维 latent head，每个 head 独立路由到自己的专家池 | 多头潜变量 MoE | 不是 Attention 的 query head；这里是 FFN 路由子空间 | 官方报告 §2.1；`configs/magi2_preview.json` |
| Ultra-Fine-Grained MoE | 每个 head 有 256 个窄专家，每个 token 在每个 head 选择 6 个专家 | 超细粒度 MoE | 不是全模型只有 256 个专家；每个稀疏层共有 12×256 个 head-local expert unit | 官方报告 §2.2；模型配置 |
| Head Parallel | 先按 head 维做固定形状跨 rank 分发，再在 head owner 内执行动态路由 | HP | 不是按动态 token-to-expert 数量做跨节点 All-to-All | 官方报告 §2.1/§3.1；`ep_dispatch` |
| MagiMoE | 从路由、排序、Gather/Scatter、专家 FFN 到加权合并的一体化执行路径 | MoE runtime | 不只是一个 Grouped GEMM | 官方报告 §3.2；`flash_mh_moe/*` |
| MagiMuon | 保留 `head × expert` 小矩阵批次结构并分布执行 Muon 正交化的优化器设计 | 无 | 不等于所有参数都用 Muon；报告称部分参数仍用 Adam 类更新 | 官方报告 §3.3；训练代码未公开 |
| MagiAttention | 面向超长上下文和异构 mask 的分布式 Attention 栈 | 无 | 不是本报告新提出的稀疏路由算法；它解决 Attention/CP 轴 | 官方仓库 Dockerfile 与配置；MAGI-1 canonical 报告 |
| auxiliary-loss-free expert bias | 用每个专家的偏置调节 Top-K 选择，不向主训练目标额外加入负载均衡损失 | 无辅助损失偏置 | 偏置用于选择，最终路由概率仍取未加偏置的 router score | 官方报告 §3.2；`route.py:52-58,135-143` |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域 | 单位/取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|
| $N$ | 序列 token 数 | author-defined | 单次层计算 | tokens | 官方报告公式 | 视频 token 很长，但官方未公开训练长度分布 |
| $H$ | 完整隐藏维 | author-defined/code-defined | 每 token | 3072 | 报告；配置 | 不等于 head 数 |
| $M$ | latent head 数 | author-defined/code-defined | 每个 MoE 层 | 12 | 报告；`num_heads` | 不等于 Attention query head 数 |
| $H_{head}$ | 每个 latent head 的维度 | author-defined/code-defined | 每个 head | 256 | $H/M$；代码 | 配置中的 Attention `head_dim=128` 是另一对象 |
| $E$ | 每个 latent head 的专家数 | analysis-derived/code-defined | 每个 MoE 层、每个 head | 256 | `num_experts` | 全层 expert unit 数为 $ME=3072$ |
| $K$ | 每个 head 激活的专家数 | code-defined | 每 token、每 head | 6 | `top_k` | 全 token 每层共激活 $MK=72$ 个 expert unit |
| $P_{total}$ | 模型总参数 | author-defined | 全模型 | 约 114B | 官方报告 | 含哪些辅助组件未给完整逐项分解 |
| $P_{active}$ | 每 token 激活参数 | author-defined | 每 token | 约 6B | 官方报告 | 不等于端到端 FLOPs，也不包含 Attention 成本的简单等价物 |
| $P_{FFN}$ | Dense FFN 参数规模 | author-defined | 每层/模型 | parameters | 官方报告公式 | 只用于主导 FFN 计算量级 |
| $BytesMoved$ | 通信路径实际搬运字节数 | analysis-derived | 每次通信/每层 | bytes | 本文带宽核算 | 报告未公开数值 |
| $RuntimeSeconds$ | 对应通信路径耗时 | analysis-derived | 每次通信/每层 | seconds | 本文带宽核算 | 需用 trace 实测 |
| $BW_{peak}$ | 互联理论峰值带宽 | analysis-derived | 某条链路 | bytes/s | 硬件规格 | 不等于应用有效带宽 |

## 1. 论文基本信息

- 标题：*MAGI-2 Preview: Scaling Video Generation Models Efficiently*
- 资料类型：官方技术报告网页，不是 arXiv 论文
- 发布时间：2026-08-05
- 署名类型：机构署名
- 署名机构：Sand.ai
- 署名依据：Official Sand.ai report page title and official GitHub README。
- 个人作者、共同一作、通讯作者及个人机构：不适用；官方网页标题块未提供个人作者列表
- 研究领域：统一音视频生成、稀疏 MoE、大规模训练系统
- 核心问题：如何在视频长序列和重复去噪计算下，把模型总容量扩展到 100B 级，同时避免每 token 计算、动态通信和训练状态显存同步增长。
- 研究目标：让模型容量、训练系统和数据复杂度一起扩展；Preview 版本用于验证这条路线，而不是提供完整 scaling law 或受控结论。

## 2. 研究动机与问题—方案闭环

### 2.1 出发点与背景痛点

**具体场景（依据官方报告重构，不是论文逐字实验）**：一批音视频样本被编码成很长的时空 token 序列，模型在多个去噪步中反复执行 Transformer。若把 100B 参数全部做成 Dense FFN，每个 token 都要调用全部 FFN 参数，参数、梯度、优化器状态和激活显存同时增长；如果改用普通 token-choice MoE，动态 Top-K 路由又直接决定跨设备发送量，某些 rank 收到更多 token，产生慢 rank、通信尾部和局部峰值显存。成功方案必须保留大容量与动态专家选择，但把跨节点通信变成可预测形状，并把细粒度专家的排序、访存和优化器开销控制住。

报告将问题拆成三条相互依赖的主线：可扩展模型结构、可扩展训练系统和可扩展数据。本文重点审计前两条，因为它们直接决定大规模异构集群的训练系统设计。

### 2.2 现有方案为何不够

长视频去噪反复调用全部 Dense FFN 参数，使参数、梯度、优化器状态和主计算同步增长。只做参数分片会增加通信和同步，不能降低每 token 主计算。

数千个 head-local 小矩阵被人工拼接后，无法逐矩阵匹配正交化和跨 rank 均衡。常规 data parallel 只复制或切分状态，不会自动恢复逐小矩阵更新语义。

| 现有方案/做法 | 可观察失败 | 根因 | 为什么简单修补不够 | 证据 |
|---|---|---|---|---|
| 继续加宽 Dense FFN 或增加层数 | 每 token 计算、训练状态和显存一起增长 | 所有 token 激活全部参数 | 只做参数分片会增加通信和同步，不能降低每 token 主计算 | 官方报告开篇与 §2 |
| 普通动态 token-to-expert All-to-All | 慢 rank、气泡、接收缓冲区不均，甚至局部 OOM | 路由结果直接决定跨设备 token 数和 buffer shape | 提高网络带宽不能消除动态不均衡与 host metadata 同步 | 官方报告 §3；Head Parallel 公式 |
| 通用 Grouped GEMM MoE runtime | 3072 个窄专家使排序、launch 和中间张量成本占比升高 | 每专家 token 少、矩阵小且形状不规则 | 只换一个 GEMM kernel 没有消除路由、重排、Gather/Scatter 和 merge 开销 | 官方报告 §3.2；官方 Triton 路径 |
| 把所有专家矩阵拼成一个大矩阵做优化 | 优化器忽略 `head × expert` 的天然小矩阵结构，计算分配不均 | 参数几何结构被人工拼接 | 常规 data parallel 无法自动匹配各类参数的更新几何 | 官方报告 §3.3 |

场景一：长视频 token 经 Top-K 后，各 rank 收到不同数量 token，最快 rank 等待最慢 rank。只提升网络带宽不能消除数据相关不均衡和 host metadata 同步。

场景二：每层 3072 个窄专家单元各自只接收少量 token，矩阵小且形状不规则。只换 GEMM kernel 没有消除路由、重排、Gather/Scatter 和 merge。

### 2.3 论文计划解决的问题与成功标准

- 核心问题：以稀疏激活维持约 6B/token 的参数调用，同时训练约 114B 总容量模型。
- 适用场景：长序列统一音视频生成；报告与代码的 Preview 版本固定生成 10 秒音视频。
- 必须满足：路由可学习、跨节点通信规则化、细粒度专家执行高效、训练状态可分片、数值稳定。
- 报告给出的成功信号：模型和权重已公开，40 层中 36 层为 Multi-Head MoE，官方推理代码可在 8 张 Hopper GPU 上运行。
- 尚未给出的成功证据：完整训练吞吐、MFU、扩展曲线、与普通 MoE/Dense 的 matched ablation、训练成本与质量—算力曲线。

### 2.4 核心方案如何解决并优化问题

| 原始问题 | 对应方案 | 改变的变量/行为 | 作用机制 | 预期指标 | 判断 |
|---|---|---|---|---|---|
| Dense 容量与每 token 计算绑定 | Multi-Head LatentMoE | 每个 head 只激活 Top-6/256 experts | 总容量与激活容量解耦 | active params、每步 FLOPs | 架构存在有代码支持；收益缺受控实验 |
| 动态路由决定跨设备流量 | Head Parallel | 跨 rank 先按 head 固定分发 | 动态 Top-K 留在 head owner 本地，通信 shape 可预分配 | 通信尾部、buffer 峰值、扩展效率 | 机制与代码直接支持；训练收益未公开 |
| 窄专家执行开销过高 | MagiMoE | 路由、排序、Gather/Scatter、FFN、merge 协同 | 减少中间物化、launch 与访存 | kernel 时间、HBM 流量 | 推理代码直接支持；反向路径未公开 |
| 专家状态无法常驻单卡 | 层次化 HP + 全分片 | 激活跨节点，专家状态节点内按层 materialize/reshard | 匹配两级网络带宽 | 峰值显存、状态通信 | 报告声明；训练实现未公开 |
| 小矩阵优化器计算分散 | MagiMuon | 按 `head × expert` 保持矩阵批次 | 独立正交化并跨 rank 均衡矩阵批次 | optimizer step time、稳定性 | 报告声明；代码与消融缺失 |
| 长序列 Attention 成本 | MagiAttention + CP | token 序列按 CP/Ulysses 分片 | Attention 与 MoE 形成多轴组合 | attention 时间、显存、scale-out | 推理依赖存在；联合训练结果缺失 |

### 2.5 完整因果链与证据闭环

视频长序列让 Dense 扩模的计算和状态成本迅速增长；普通 MoE 虽减少激活参数，却把数据相关路由直接暴露为跨设备不规则通信。MAGI-2 先把隐藏状态拆成独立 latent head，使跨设备边界由动态 token copy 改成固定 head slice；再在 head owner 内完成 Top-K 路由和窄专家计算，并用 MagiMoE 融合完整执行路径；训练侧再用状态分片和 MagiMuon 处理专家 bank 与小矩阵优化器负载。官方代码直接验证模型配置、head dispatch、per-head routing、专家权重分片和融合推理 kernel；但完整训练栈、反向 kernel、MagiMuon 实现、训练效率和质量消融均未公开，因此闭环只能判为**机制部分有证据，训练收益尚未充分验证**。

## 3. 核心贡献与创新点

1. **100B 级统一音视频 MoE**：官方声明约 114B 总参数、约 6B/token 激活，统一处理文本、视频和音频。
2. **Multi-Head LatentMoE**：在 12 个 256 维子空间内独立路由，每层形成 3072 个 head-local expert unit，每 token 激活 72 个。
3. **Hierarchical Head Parallel**：把跨节点通信与动态路由解耦，并把专家状态分片映射到节点内高带宽互联。
4. **MagiMoE 执行栈**：联合优化 FP32 路由、稳定排序、Gather/Scatter、BF16 窄专家 FFN 和输出合并。
5. **MagiMuon**：按 `head × expert` 的矩阵批次组织优化器，而不是将所有专家拼成一个人工大矩阵。

## 4. 研究方法

### 4.1 方法总览

一个样本进入模型后，文本、视频和音频 token 被拼成统一序列。稀疏层先把 3072 维隐藏状态视为 12 个 256 维 latent head；Head Parallel 按 head 做固定形状 All-to-All，使每个 rank 获得完整序列上的一部分 head；每个本地 head 独立计算 256 个 expert score，并选择 Top-6；MagiMoE 把选中 token 排成 expert-wise 紧凑布局，执行窄专家 SwiGLU7，再按路由权重合并输出并逆向分发回原 rank。Attention 则使用 CP/Ulysses 与 MagiAttention 路径处理长序列。

### 4.2 组件级设计动机与具体问题映射

**Multi-Head LatentMoE。** 如果整个 3072 维 token 只选择少数大专家，专家粒度仍粗，增加总容量容易同步增加单专家计算。拆成 12 个 256 维路由子空间后，每个 head 可以选择不同专家组合，条件容量更细；代价是专家单元数量变成每层 3072 个，通用小矩阵 runtime 的固定开销更明显。

**Head Parallel。** 普通 MoE 先路由再跨设备发送 token，通信量和 buffer shape 随 batch 路由变化。Head Parallel 先按 head 固定切分，跨 rank 只移动规则 head slice，再本地路由。它把不规则性从网络边界移到本地执行，但并没有消除本地专家负载不均和专家 bank 显存问题。

**MagiMoE。** 窄专家下只优化 GEMM 不够，因为排序、Gather/Scatter、kernel launch 和中间张量也可能成为主成本。官方实现将路由结果转换为稳定排序的 CSR-like offsets，并用 Triton kernel 读取专家权重、融合 gate/up 和 SwiGLU7，再进行加权 scatter-back。公开代码只含推理 forward，不能证明训练 backward 的效率声明。

**MagiMuon。** 报告认为 head-local 专家权重天然是一批小矩阵，Muon 正交化应逐矩阵执行并把矩阵批次分配到不同 rank。其动机合理，但训练优化器代码和收敛消融未公开，现阶段只能作为待验证训练设计。

| 设计项 | 论文是否明确说明 why | 具体问题 | 机制 | 权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|
| Multi-Head LatentMoE | author-stated | 大容量与 active compute 绑定 | 独立 head 路由细化条件容量 | 更多小专家与路由元数据 | 配置、权重结构、推理代码 | 部分支持 |
| Head Parallel | author-stated | 动态 All-to-All 不规则 | 固定 head slice 跨 rank，路由本地化 | head 数须适配 EP；本地仍不均衡 | 通信公式、`ep_dispatch` | 机制支持 |
| MagiMoE | author-stated | 小专家固定开销高 | 融合路由到 merge 的完整路径 | 定制 kernel、硬件相关 | Triton forward 代码 | 推理支持，训练未验证 |
| auxiliary-loss-free bias | author-stated | 路由负载不均 | 偏置影响 Top-K 选择，不改变最终概率来源 | 需异步统计和 EMA 对齐 | `route.py`、checkpoint EMA | 实现支持，训练效果未验证 |
| MagiMuon | author-stated | 小矩阵优化器结构不匹配 | 逐小矩阵正交化、批次分布 | 系统复杂、收敛需验证 | 报告索引片段 | 未充分验证 |
| MagiAttention | inferred/复用 | 长视频 Attention 成本高 | CP/Ulysses 与异构 mask runtime | 与 EP/HP 组合复杂 | Docker/config/代码依赖 | 推理依赖支持 |

### 4.3 模型/系统架构

官方配置给出的 Preview backbone 为 40 层、hidden size 3072、Attention head dimension 128、24 query groups；第 2–37 层共 36 层使用 MoE，首尾四层保持 Dense。每个 MoE 层含 12 个 latent head、每 head 256 experts、Top-6，专家中间维 1280；另有共享专家和模态特定共享专家路径。模型还开启 attention gating、1 个 attention sink token 和 4-stream mHC。

按代码参数形状复算，Preview Transformer core 约 113.48B，每 token 涉及的 core 权重约 5.60B，和官方 114B/6B 的四舍五入口径一致。这个口径不含约 6.06B 的 Refiner、Qwen3.5-27B 文本编码器和 VAE。

Refiner 是独立的 30 层、hidden size 4096 模型，所有层采用局部 window attention；公开推理先以 100 denoising steps 生成 512×896 preview，再以 5 steps refiner 生成 1088×1920 latent/video。发布配置的 `audio_noise_scale=-1` 会移除 Refiner 的 audio token，因此第二阶段只精炼视频，最终音频沿用 Preview 产生的 latent。

### 4.4 关键公式

报告用简化式表达 Dense 与 MoE 的 FFN 主计算：

$$
F_{dense}\propto N P_{FFN},\qquad
F_{MoE}\propto N P_{active},\qquad
P_{active}\ll P_{total}.
$$

**这条公式在算什么？** 比较 Dense FFN 与稀疏 MoE 的每 token 主计算。

**怎么读？** Dense 每个 token 调用全部 FFN 参数，MoE 只调用路由选中的活跃专家参数。

**输入与输出。** 输入是 token 数 $N$、Dense FFN 参数规模 $P_{FFN}$ 或活跃参数 $P_{active}$；输出是主导 FFN 计算量的比例关系。

**变量在这里各做什么？** $N$ 决定处理多少 token；$P_{active}$ 决定每 token 实际进入多少专家权重；$P_{total}$ 表示可存储的总容量。

**直觉。** 增加未激活专家可以扩大容量而不按相同比例增加单 token FFN 计算。

**边界。** 这不是端到端 FLOPs 公式；Attention、路由、排序、通信、共享专家和 VAE 均未计入。

**小例子。** MAGI-2 每层有 $12\times256=3072$ 个 head-local expert unit，每 token 激活 $12\times6=72$ 个；这说明激活单元比例低，但不等价于全模型只做 $72/3072$ 的计算。

Head Parallel 的主导通信量被报告简化为：

$$
C_{HP}\propto N M H_{head}=NH.
$$

**这条公式在算什么？** 估算 Head Parallel 固定 head 切分的主导通信元素量。

**怎么读？** 把完整隐藏状态按 $M$ 个 head 分发一次，总元素数仍约等于 $N\times H$，不会再乘每 head 的 Top-$K$。

**输入与输出。** 输入是序列长度 $N$、head 数 $M$ 和每 head 维度 $H_{head}$；输出是通信元素量级。

**变量在这里各做什么？** $M H_{head}=H$；$K$ 不出现在公式中，因为动态专家选择发生在 head owner 本地。

**直觉。** 网络看到的是规则隐藏状态切片，而不是被 Top-K 复制后的动态 token 包。

**边界。** 该式没有计协议、拓扑、双向 dispatch/undispatch、反向梯度和 expert state materialization，也不证明实际链路利用率。

**小例子。** 代码中 `ep_dispatch` 将 `(S,H,D)` 变为 `(S×ep,H/ep,D)`，元素总数不变；随后才在本地形成 `[head, token, expert]` router logits。

### 4.5 训练/实验/部署设计

报告称数据方法从“过滤为中心”转向高吞吐数据生产与精确多模态标注，覆盖主体/场景、动作/交互、镜头/时间结构、对白/歌曲、环境声/音乐和屏幕文字。该方向与统一音视频 MoE 的专家专门化具有机制关联，但公开材料没有数据规模、去重策略、版权范围或数据消融，不能证明数据方法对具体能力的因果贡献。

官方仓库是推理代码，不含完整训练 loop。README 要求 8 张 NVIDIA Hopper GPU；Docker 固定 FlashAttention Hopper backend、MagiAttention `2c641357...`、MagiCompiler `5950612...`，并使用 NCCL。Preview/refiner 默认 roundtrip offload，是因为 1080p 路径中二者无法同时与 activation 驻留一张 80 GB 卡。

## 5. 关键结论

### 5.1 主结果

- 官方声明模型总参数约 114B、每 token 激活约 6B。
- Preview backbone 配置为 40 层，36 层 Multi-Head MoE，12 latent heads、256 experts/head、Top-6。
- 每个稀疏层共有 3072 个 head-local expert unit，每 token 激活 72 个。
- 路由 logits 与 expert bias 使用 FP32；专家权重与主计算配置为 BF16。
- `ep_dispatch`/`ep_undispatch` 使用固定形状 `all_to_all_single`，先按 head 分发再本地路由。
- checkpoint 中 `(head, expert)` 维专家权重按 EP rank 切片读取，其他权重复制。
- 官方公开路径是 8×Hopper 的两阶段推理，不是完整训练复现。

### 5.2 消融和机制证据

| 技术点 | 声称收益 | 公开证据 | 对照性 | 结论 |
|---|---|---|---|---|
| 114B/6B sparse scaling | 大容量、低 active compute | 官方声明、配置与权重目录 | 无 Dense matched baseline | 规模声明可接受，质量/成本归因不足 |
| Head Parallel | 固定通信 shape、避免 Top-K 放大跨节点流量 | 公式与 `ep_dispatch` | 无训练 trace/scale curve | 机制支持，实际收益未量化 |
| MagiMoE | 降低窄专家排序、launch 和访存成本 | 推理 Triton forward | 无通用 Grouped GEMM 对照 | 实现存在，速度归因未验证 |
| auxiliary-loss-free bias | 平衡专家负载且不污染主 loss | 路由与 EMA 代码 | 无训练负载曲线 | 实现支持，训练效果未验证 |
| MagiMuon | 匹配小矩阵几何并均衡 optimizer compute | 官方报告描述 | 训练代码/消融缺失 | 未充分验证 |
| 数据生产与精确标注 | 促进专家专门化和统一能力 | 官方方法描述 | 数据/模型变化捆绑 | 相关性判断，不能因果归因 |

### 5.3 是否验证了假设

报告本身将 MAGI-2 Preview 定位为中间研究版本，并明确表示更完整的 scaling curves、受控消融和能力边界仍是后续工作。因此，它较强地验证了“100B 级 Multi-Head MoE 可以形成公开权重和可运行推理栈”，但没有充分验证“每个系统组件分别带来多少训练效率或质量收益”。

### 5.4 收益来源归因

现有公开证据只能把收益定位到机制路径，不能完成数值分解：Head Parallel 负责规则化跨 rank 通信；MagiMoE 负责降低本地窄专家执行开销；MagiMuon 面向优化器矩阵批次；MagiAttention 面向长序列 Attention。报告没有在同模型、同数据、同硬件条件下逐项开关这些组件，因此任何训练吞吐或质量收益都不能单独归因给其中一项。

## 6. Related Work 对比

| 路线 | 核心机制 | 优点 | 局限 | 与 MAGI-2 的关系 |
|---|---|---|---|---|
| Dense Video DiT | 所有 token 激活全部 FFN | 执行规则、易优化 | 容量与计算/状态同步增长 | MAGI-2 用稀疏 FFN 解耦容量与 active compute |
| 普通 token-choice MoE | token 动态发送到专家 owner | 专家可跨设备分布 | 动态 All-to-All、不均衡 buffer | Head Parallel 改为先固定 head 分发 |
| Multi-Head Latent Attention/MoE | 在低维 head 子空间独立表达或路由 | 更细粒度条件容量 | 小矩阵执行复杂 | MAGI-2 将其扩到视频 114B 并做系统协同 |
| MAGI-1 + MagiAttention | chunkwise AR + 异构 mask CP | 超长视频和流式生成 | 主要是 Attention/serving 轴 | MAGI-2 保留长序列 Attention 基础设施，并新增 MoE/HP/optimizer 轴 |

## 7. OpenReview 公开评审 × 论文内容交叉核验

未发现 MAGI-2 Preview 对应的公开 OpenReview 页面、评审、decision 或 rebuttal。该材料是机构发布的技术报告，不能以同行评审结论补强其主张。

### 7.1 与论文证据一致的正向评价

不适用：没有公开 reviewer 正向评价。代码事实支持“结构和推理实现已公开”，但这不是同行评审意见。

### 7.2 经核验仍成立的主要担忧

完整训练代码、受控消融、扩展曲线和训练成本均未公开，这是当前最主要的证据缺口。

### 7.3 Rebuttal/Revision 是否真正解决问题

不适用：未发现 rebuttal、meta-review 或正式 revision 讨论。

### 7.4 对本文贡献、适用范围和潜在风险的影响

结论应限定为“公开架构和推理代码验证了 100B 级多头 MoE 的可实现性”；不能扩展为“已证明训练效率最优”或“114B 容量单独导致质量提升”。

## 8. Infra 需求分析

### 8.1 算力

核心算子不是一个大 FFN GEMM，而是大量 `256→1280→256` 的窄专家计算。每层 3072 个专家单元、每 token 激活 72 个，使 kernel 的 token grouping、tile occupancy、launch 数和 scatter merge 成为核心。面向其他加速器适配时，需要把完整链路视为一个优化对象：FP32 router score/Top-K、stable sort/offset、Gather、gate/up fusion、SwiGLU7、down projection、weighted scatter-back。

### 8.2 显存与存储

仅按 BF16 粗算 114B 参数需要约 228 GB；这与官方 preview transformer 约 228 GB 的磁盘规模数量级一致，但磁盘 safetensors 大小不等于训练 HBM。训练还需梯度、主权重和优化器状态。若以 BF16 参数/梯度和 FP32 两份 Adam state 作说明例，未分片状态可达约 $2+2+8=12$ bytes/parameter，即约 1.37 TB，尚未计 activation、临时 buffer 与 allocator 碎片。MagiMuon 的实际状态格式未公开，不能沿用该估算作为其真实占用。

### 8.3 Data Types / 数值格式

| 对象 | 格式 | 阶段 | 作用 | 证据 |
|---|---|---|---|---|
| router logits / expert bias | FP32 | 推理；报告称训练同样重视稳定性 | 降低 Top-K 与 bias 更新的数值误差 | `magi2_preview.py:2590-2600`、`route.py` |
| expert weights / activation | BF16 | Preview 主计算 | 降低 HBM 与矩阵计算成本 | config 与 Triton kernel |
| text/video/audio adapters | FP32 参数声明 | 推理模型构造 | 模态输入投影精度保守 | `PreAdapter` |
| Attention | FA3 Hopper path | 推理 | 高效长序列 Attention | Dockerfile 与 imports |

### 8.4 带宽、互联与高效利用

Head Parallel 的价值不是减少隐藏状态元素总数，而是让跨节点 send/recv count 与 head partition 静态确定。训练报告进一步把跨节点 head activation 交换放到 InfiniBand，把节点内专家参数/梯度/优化器状态 materialize/reshard 放到 NVLink。迁移到其他硬件时，应映射到实际节点内高带宽互联与节点间网络，而不能照搬特定互联名称；关键是分别测量固定 head activation 流量、按层专家状态流量和未隐藏通信占比。

公开材料没有通信 bytes、链路峰值、step trace 或 wall time，因此无法计算有效带宽：

$$
BW_{eff}=\frac{BytesMoved}{Runtime},\qquad U=\frac{BW_{eff}}{BW_{peak}}.
$$

**这条公式在算什么？** 计算通信路径的实际带宽和峰值利用率。

**怎么读？** 实际每秒传输量除以硬件峰值，得到有效利用比例。

**输入与输出。** 输入是 `BytesMoved`、`RuntimeSeconds` 和 $BW_{peak}$；输出是有效带宽 $BW_{eff}$ 与利用率 $U$。

**变量在这里各做什么？** `BytesMoved` 是真实搬运量；`RuntimeSeconds` 是对应耗时；$BW_{peak}$ 是硬件峰值；$BW_{eff}$ 和 $U$ 分别表示实际吞吐与峰值占比。

**直觉。** 同样的峰值链路，如果小包、同步或负载不均增加耗时，$BW_{eff}$ 和 $U$ 都会下降。

**边界。** MAGI-2 未公开 `BytesMoved` 与训练 runtime，本报告只把它列为后续实测必须补齐的测量项，不能给出数值结果。

**小例子。** 不适用：缺少训练通信 bytes 和 runtime，给出数值会误导。

### 8.5 CPU/GPU/NPU 异构执行

官方实现依赖 CPU 侧配置、checkpoint shard 并发读取、视频/audio 后处理和 ffmpeg；GPU 执行路由、Triton MoE、Attention 与 VAE。动态路由的核心路径尽量留在 device 上，避免 host metadata 同步。迁移到其他加速器时要确认 Top-K、stable sort、prefix offsets、动态 shape 编译和自定义算子不会回退到 Host。

### 8.6 调度/Serving/自定义算子

官方推理以 8 张 Hopper GPU、CP=8、EP=8 运行；两个轴复用同一组 8 ranks，不是 64 卡笛卡尔积，默认 DP=1。12 个 MoE head 在 EP=8 时被 padding 到 16，每 rank 持有 2 个 head，其中 rank 6、7 的 head 全为 dummy zero weights，形成通信和计算空洞。Preview 和 Refiner 采用 roundtrip offload 分阶段驻留，VAE 使用滑动窗口解码。迁移到其他加速器时需要重新实现 Head Parallel All-to-All、MoE 自定义算子、MagiAttention 后端、compile cache 与确定性 scatter，并在 CP×EP 组合下避免 collective 争用，同时针对 `head_count % EP != 0` 做并行度搜索或非均匀 head placement。

确定性路径也存在接口边界：`MAGI2_DETERMINISTIC=1` 会触发仓内 MoE 顺序 scatter 和 Preview FA3 确定性分支；单独传 `--deterministic` 没有设置该环境变量，因此两者并非完全等价。跨硬件正确性对齐应显式覆盖路由排序、scatter 累加次序和编译 autotune 开关。

## 9. 开源代码对照

- 仓库：[SandAI-org/MAGI-2-preview](https://github.com/SandAI-org/MAGI-2-preview)
- 固定提交：`f68a0f9bbccbea56e0177a9bd912abc3b18ffe61`
- 代码范围：推理；不含完整训练数据、training loop、MagiMuon 和生产调度栈

| 报告机制 | 代码位置 | 一致性判断 |
|---|---|---|
| 40层、36层 MoE、12 heads、256 experts/head、Top-6 | `configs/magi2_preview.json` | 一致 |
| per-head router logits `[H,S,E]` | `inference/model/magi2_preview.py::_route` | 一致 |
| 固定 head EP dispatch | `magi2_preview.py::ep_dispatch/ep_undispatch` | 一致；推理实现 |
| stable expert sort 与 offsets | `inference/flash_mh_moe/route.py::flash_mh_moe_global_sort` | 一致 |
| fused expert forward | `inference/flash_mh_moe/triton/mh_moe_fwd.py` | 一致；仅 forward |
| expert 权重按 `(head,expert)` 分片加载 | `inference/infra/checkpoint/magi2_checkpointing.py` | 一致 |
| auxiliary-loss-free bias EMA | `magi2_checkpointing.py::_apply_router_bias_ema` | 推理对齐存在；训练更新未开源 |
| MagiMuon | 未发现 | 未开源 |
| Hierarchical HP training | 未发现完整训练实现 | 报告声明，代码不足 |

### 9.1 开源权重/配置对照

| 权重/组件 | 公开状态 | 规模/结构 | 本次核验 |
|---|---|---|---|
| Preview transformer | 公开，约 228 GB | 40 层、36 MoE、hidden 3072；代码形状复算约 113.48B core | 配置和源码已核验；未下载权重逐 tensor 求和 |
| Refiner | 公开，约 14 GB | 30 层、hidden 4096、局部 window attention；复算约 6.06B | 配置已核验；默认只精炼视频 |
| Text encoder | 公开，约 56 GB | Qwen3.5-27B | README 路径已核验；权重未下载 |
| Video/Audio VAE | 公开 | Wan2.2 VAE、Stable Audio Open 1.0 | README 与配置已核验 |

## 10. 优点与局限

### 优点

- 架构、通信边界、kernel 和优化器围绕同一 `head × expert` 结构共同设计，系统逻辑一致。
- 官方配置和推理代码把关键形状、数据类型、路由和权重 ownership 暴露得较清楚。
- Preview 报告主动承认 scaling curve、消融和能力边界仍不完整，避免把中间版本包装成最终证明。

### 局限

1. 官方技术报告网页受 WAF 阻断，未获得完整可归档 PDF/HTML，原始 Figure/Table 无法做逐图 QA。
2. 开源仓库是推理代码，不能复现训练 throughput、反向 kernel、MagiMuon、优化器状态分片和收敛。
3. 未公开训练集群规模、训练 FLOPs、wall time、MFU、通信 trace、峰值显存或故障率。
4. 未提供 Dense、普通 MoE、Head Parallel、MagiMoE、MagiMuon 的 matched ablation。
5. 114B/6B 是官方声明；本次未下载约 307 GB 权重逐 tensor 复算。
6. 推理强依赖 Hopper、FA3、Triton、NCCL 和自研编译/Attention 栈，不能直接外推到其他硬件平台。

### 最小补实验

- 固定模型与数据，对比动态 token All-to-All、Head Parallel、层次化 HP 的 step time、P99 rank time、buffer 峰值和 OOM 率。
- 逐项拆分 routing、sort、Gather/Scatter、expert GEMM、merge，比较通用 Grouped GEMM 与 MagiMoE。
- 对比 Adam、Muon、MagiMuon 的收敛、optimizer step time、状态显存和矩阵批次负载。
- 在 CP×EP 组合下报告单机到多机 scaling curve、通信暴露和有效带宽。
- 给出 114B 与更小模型在同数据、同 active compute 下的质量—成本曲线。

### 可改进之处

优先公开完整训练配置、Head Parallel/MagiMoE/MagiMuon 的逐项受控实验，以及每层通信字节、rank P99、峰值显存、MFU 和收敛曲线；同时给出 active-parameter 的精确口径与 checkpoint tensor 统计脚本。

## 11. 研究启发

- MoE 的“路由轴”可以同时成为通信分区轴和优化器矩阵批次轴；结构选择应贯穿模型、runtime 与 optimizer。
- 对细粒度专家，系统瓶颈往往从大 GEMM 转向排序、内存搬运、launch、元数据和同步，单算子峰值不是充分指标。
- 长视频训练的 Attention 轴和 MoE 轴共享网络与 HBM，必须做组合调度和全链路 trace，不能分别看局部收益。

## 12. 解读问题/待验证清单

1. 官方 6B active parameters 是否包含共享专家、Attention 和 adapter，精确口径是什么？
2. 训练时 head 数不能整除 EP 时如何 padding，额外计算与收敛有何影响？
3. per-head expert bias 的更新公式、目标 load 和 EMA 系数是什么？
4. MagiMoE backward 如何控制 saved tensor 与原子 scatter 的确定性？
5. MagiMuon 的 momentum、正交化迭代和分布矩阵 batch 如何与 FSDP state ownership 组合？
6. HP、CP、DP、EP 的生产拓扑和 collective 优先级如何安排？
7. 114B 相对小模型的能力收益是否来自容量、数据、训练预算或统一音视频目标？

## 13. 一句话总结

MAGI-2 Preview 的关键不只是“114B MoE”，而是用 Multi-Head LatentMoE 把动态路由限制在 head owner 内，再以固定 Head Parallel 通信、融合窄专家 runtime 和结构感知优化器协同承接；这条系统路线有官方配置和推理代码支撑，但完整训练效率、质量收益和组件归因仍缺公开证据。

## 14. 冻结前发布审计

- Markdown 渲染器：Python Markdown 3.10.2，启用 `tables` 与 `fenced_code` 扩展。
- 渲染命令：`python -c 'markdown.markdown(..., extensions=["tables", "fenced_code"])'`，输出 `rendered-gfm.html`。
- 渲染结果：passed；11 张表、17 个二级标题、0 张图片均生成，table/code 标签成对闭合。
- Figure/Table 邻近性审计：无官方 Figure/Table；本 Paper 不再引用整理图。
- 临时标记扫描：clean；未发现 HTML 注释、TODO、FIXME、pending 或 debug 标记。
- 审计证据：`review_checklist.md` 与 `deliverable_manifest.json`。
