---
tags:
  - paper
  - collection/speculative-decoding
  - domain/model-systems
  - status/deep-review
  - topic/workload-aware-speculative-decoding
  - method/hybrid-parallel-drafting
document_type: paper
domain: 02_model_systems/speculative_decoding
collection: speculative-decoding
review_status: deep-review
canonical: true
---

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 父级 Survey：[Evolution](../surveys/evolution.md)
> - 正式资产：`../assets/papers/angelspec/`
> - 证据清单：[Figure inventory](../evidence/figure-inventory.md)


# AngelSpec: Towards Real-World High Performance Inference with Speculative Decoding 精读分析

AngelSpec 不是单一 drafter，而是把投机解码拆成“按负载选择训练对象、用 DFly 提高长块候选质量、用 D-cut 按运行时成本分配验证预算”三层。论文最有价值的地方是承认一种 drafter 无法同时统治开放对话与代码/数学；最大不确定性则是 D-cut 尚未随仓库开源，且 Hy3 与生产流量结果无法由外部复现。

> 资料状态：已核验 arXiv:2607.25852v2 PDF、LaTeX source、官方仓库 commit `d3412bed231025ea85d35dbf5e0af44f1ac62a5b`、四个带完整 caption 的 PDF crop。未发现公开 OpenReview forum；匿名 API 查询返回 403。

## 修订信息

- 当前文档版本：`1.0.0`
- 当前修订 ID：`rev-angelspec-20260804-initial`
- 当前修订时间：`2026-08-04T21:30:00+08:00`
- 替代版本：无（initial）

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rev-angelspec-20260804-initial` | `1.0.0` | `2026-08-04T21:30:00+08:00` | Codex | initial | 无 | 无 | 建立 PDF/source/code/视觉证据完整精读 | 用户要求分析 AngelSpec | `analysis.md`、`figure_inventory.md`、代码快照 | arXiv v2、官方仓库与逐图 QA | material |

## 0. 资料与配图索引

- 论文：arXiv:2607.25852v2；官方代码 commit：`d3412bed231025ea85d35dbf5e0af44f1ac62a5b`
- 视觉证据：[Figure inventory](../evidence/figure-inventory.md)
- 方法图：`../assets/papers/angelspec/dfly-overview.png`、`../assets/papers/angelspec/dcut-overview.png`
- 系统与结果：`../assets/papers/angelspec/framework-overview.png`、`../assets/papers/angelspec/throughput-table7.png`
- AI 生成图：未生成。论文 Figure 6 已覆盖输入、控制面、Mooncake 数据面、训练 ranks 与评估回路。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| MTP drafter | 复用 target 隐状态、embedding 与 LM head，并递归调用一个共享 MTP block 的短候选生成器 | multi-token prediction | 不是一次并行生成整块；推理时仍逐深度递归 | Section 2；`angelspec/models/mtp.py` |
| TTT | 训练时让后续 MTP 深度吃前一深度自己的预测，以逼近推理时状态分布 | Training-Time Test | 不是测试时更新 target 权重 | Section 2.2 |
| DFly | DFlash 共享非线性 FC context、每 draft layer 的 target-layer fusion residual，以及 predecessor-conditioned hidden correction 的并行 drafter | DFlareV2 | 不是 DSpark；仓库测试明确不带 Markov/confidence head | Section 3；`models/draft/dfly.py` |
| hidden correction | 用前一 draft token embedding 修正当前位置 parallel hidden state 的轻量 SwiGLU residual | predecessor-conditioned AR head | backbone 仍一次并行；只在输出头加入前驱条件 | Eq. 13；`HiddenStatesCorrection` |
| D-cut | 把 batch 内验证位置看成共享预算，按 prefix-survival score 和启动时 profile 的成本选择保留比例 | dynamic verification budgeting | 不改变 drafter 权重；不是每请求独立固定截断 | Section 4 |
| accepted length | 每次 target 验证后实际提交的 token 数，通常含 bonus token | committed length / MAL（上下文中） | 不是单位置接受率，也不是吞吐 | Tables 3-7 |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/索引 | 单位/取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|
| $D$ | MTP logical depths；在 D-cut 章节又表示每请求 draft token 数 | author-defined | per training/inference setup | positive integer | Sections 2, 4 | 两章同符号不同对象，需按阶段读 |
| $h^{(k)}$ | 共享 MTP block 在逻辑深度 $k$ 的 hidden state | author-defined | per depth/token | vector | Eq. 1-2 | 不是 target 的第 $k$ 层 hidden state |
| $W_{\mathrm{fuse}}$ | 每个 DFly draft layer 对选定 target layers 的可学习融合 logits | author-defined | draft layer x target layer | scalar matrix | Eq. 11；code `layer_fusion_weights` | softmax 后才是权重 |
| $c_{i,t}$ | 请求 $i$ 在 draft 位置 $t$ 的 token confidence | author-defined | per request/position | $[0,1]$ | Eq. 20 | 论文未证明它是校准后的真实接受概率 |
| $s_{i,k}$ | 前 $k$ 个位置全部存活的估计分数 | author-defined | per request/prefix | $[0,1]$ | Eq. 20 | 是 confidence product，不是真实 survival probability |
| $K_\rho(B)$ | batch size $B$、比例 $\rho$ 下的验证位置预算 | author-defined | per batch | token positions | Eq. 22 | 至少为 $B$，保留每请求 bonus slot |
| $U(B,\rho)$ | 该预算下估计的 batch token progress | author-defined | per batch/ratio | tokens per step | Eq. 23 | 是期望进展估计，不是实测吞吐 |
| $C(B,\rho)$ | 启动 profile 得到的整轮延迟 | author-defined | per hardware/batch/ratio | seconds | Eq. 24 | 硬件与软件版本相关，不能跨部署复用 |

## 0.2 原论文算法/系统总览

![AngelSpec framework overview](../assets/papers/angelspec/framework-overview.png)

> 原论文 Figure 6。灰色部分来自 TorchSpec 基础：推理 engine 生成 target hidden states，经 Mooncake RDMA/TCP 送到训练 ranks；绿色部分是 AngelSpec 增量：Hy target plugin、MTP+TTT、DFly family、可组合目标与实时接受率评估。

## 1. 论文基本信息

- 标题：*AngelSpec: Towards Real-World High Performance Inference with Speculative Decoding*
- 版本：arXiv:2607.25852v2，2026-07-29 更新
- 完整作者列表：Hong Liu, Rui Cen, Junhan Shi, Guangshuo Qin, Jiebin Zhang, Tianyu Liu, Runzhi Fan, Guoliang Zhao, Ruobing Xie, Kai Zhang, Song Liu, Guanghua Yu, Jianchen Zhu
- 第一作者/共同一作及机构：Hong Liu；身份依据 `first listed`；Tencent Inc.；证据 `paper source main.tex author block`
- 通讯作者及机构：Guanghua Yu；身份依据 `superscript * and *Corresponding author legend`；Tencent Inc.；证据 `paper source main.tex author block`
- 其余作者涉及机构：Tencent Inc.
- 作者核验：论文未标 equal contribution，因此只把首位作者视为第一作者。
- 核心问题：真实 workload 异质性下，如何同时提高 drafter 质量、训练可扩展性和高并发验证效率。

## 2. 研究动机与问题—方案闭环

### 2.1 出发点与背景痛点

作者明确指出，开放对话、代码和数学的条件熵与续写结构不同。高熵对话有许多语义可接受的分支，但 target 只采样其中一条，长 block 很快失配；代码与数学受语法、标识符和推导约束，较长前缀更可预测。把全部数据平均混合并训练一个“万能 drafter”，会在短 horizon 的稳定性与长 block 的并行摊销之间折中，却不一定在任何域达到最好。

此外，accepted length 不是部署目标本身。每个保留位置仍要由 target 验证；并发升高后，大块验证会占满 target 计算，即使 drafter 很快也可能降低吞吐。论文因此把成功标准从单一 MAL 扩展为不同域、并发和硬件上的 end-to-end tok/s。

### 2.2 现有方案为何不够

| 现有方案 | 可观察失败 | 具体场景 | 来源 | 根因 | 为什么简单修补仍不够 | 证据 |
|---|---|---|---|---|---|---|
| 一个 drafter + 均匀数据混合 | chat 与 code/math 不能同时拿到最佳 accepted length | 论文 Hy3 结果中 MTP-3 在 MT-Bench 更强，而 DFly-8 在结构化任务更强；强行只部署 DFly 会牺牲 chat | paper-provided | workload 条件熵与可预测跨度不同 | 只调 block size 仍用同一表示和数据分布，不能同时解决域差异 | Intro；Table 7 |
| DFlash position-wise parallel block | 后缀缺少已选前驱 token 条件，接受率随位置衰减 | 本文构造的说明例，不是论文实验：第 2 位在“for”路径下选“i”，第 3 位却采用另一分支的边际高频 token，组合后语法不一致 | reviewer-created | 各位置看到 accepted context，却看不到本 block 已选路径 | 单纯加深 backbone 不注入 realized predecessor；更长 block 反而放大缺口 | Section 3.2；Table 4 |
| 固定每请求验证深度 | 高并发时大量低置信 suffix 占 target slots | live traffic c64：DFly 848 tok/s，D-cut 981 tok/s，而 MAL 仅从 2.50 降到 2.43 | paper-provided | verification cost 随 batch/hardware/CUDA graph 路径变化，并且请求间 useful depth 不同 | 统一缩短会同时裁掉高置信请求；只看 confidence 又忽略硬件成本拐点 | Section 4；Figure 4 |

### 2.3 目标与成功标准

- draft quality：不同 workload 上提高 mean accepted length。
- serving：并发 4-64 的平均 tok/s 优于 AR、MTP 与 DFlash。
- training：支持大 MoE target hidden-state 流、MTP on-policy rollout、128k 长上下文、packing 和实时 acceptance evaluation。
- 正确性：保留 token 仍由 target 原始验证；论文将 deterministic draft + target-only verification 的 D-cut 路径表述为分布保持。

### 2.4 核心方案如何解决并优化问题

| 问题 | 方案 | 改变的变量/行为 | 机制 | 预期指标 | 证据 | 判断 |
|---|---|---|---|---|---|---|
| workload 异质 | 对话数据训练 MTP；代码/数学数据强化 DFly | drafter structure 与训练分布按域分工 | 短 horizon 避免 chat 过度投机；长 block 利用结构化续写 | MAL、tok/s | Intro；Tables 3,7 | partially-supported：只展示有限域与 target |
| DFlash target conditioning 与块内依赖弱 | hybrid FC + layer-specific fusion + hidden correction | 每层 target view、前驱条件 | 保留并行 backbone，再轻量修正路径一致性 | suffix acceptance/MAL | Table 4 cumulative ablation | supported，但组件消融是累积式 |
| 固定验证预算浪费 | D-cut top-K prefix scores + profiled cost | 每请求 keep depth、全局 ratio | 把 target slots 给高预期收益 prefix，并按 $U/C$ 选形状 | high-load tok/s | live traffic Figure 4 | paper-supported；代码未开源 |
| target 与 training 抢 GPU/数据流 | TorchSpec/Mooncake 解耦 + FSDP2/USP | 资源配比、数据驻留与序列切分 | inference/training 独立扩展，避免磁盘中转 | train throughput/context | Section 6/code | implementation-supported；论文少量量化 |

### 2.5 完整因果链与证据边界

真实流量异质且验证成本随负载变化，导致统一 drafter 与固定深度无法同时优化 chat、结构化生成和高并发。AngelSpec 先把结构/数据按 workload 分工，再用 DFly 提升 block 的 target feature 利用与前驱一致性，最后用 D-cut 把验证位置按预测收益和 profile 成本重分配。Table 4 直接支持 DFly 累积组件带来的 MAL 增益，Table 7 支持完整 DFly 在给定 Hy3/H20 设置下的吞吐优势，live traffic 支持 D-cut 高负载收益。

边界是：架构与数据在 Table 4 中按累积顺序加入，不能把最终收益完全独立归因；D-cut confidence calibration、profile 迁移和实现均未公开；Hy3、生产流量和 H20 环境不可外部检查。

## 3. 核心贡献

1. 将 workload heterogeneity 明确纳入 drafter 结构与数据选择，而非只报告混合平均分。
2. DFly 用共享非线性 target context + per-layer fusion + predecessor correction 组合 parallel drafting 与路径条件。
3. D-cut 将 batched verification 视为共享资源，以期望进展/实测成本选择预算。
4. 发布统一的 torch-native 训练框架，代码覆盖 DFly、MTP/TTT、DFlash/DFlare/DSpark/Eagle3、packing、FSDP2 和多 backend。

## 4. 研究方法

### 4.1 方法总览

训练阶段：target engine 生成 hidden states；Mooncake 把 tensor 流给训练 ranks；按 workload 训练 MTP 或 DFly；评估 server 周期性加载 checkpoint 做真实 speculative decoding。推理阶段：MTP 对短 horizon 逐深度 draft；DFly 一次 parallel backbone 产生 block hidden states，再用 predecessor-conditioned head 修正 logits；D-cut 在 batch 层裁剪验证 prefix；target 最终验证并提交 token。

### 4.2 组件级设计动机

| 设计 | why 状态 | 针对问题 | 因果机制 | 权衡 | 验证 | 判断 |
|---|---|---|---|---|---|---|
| MTP TTT shared-depth rollout | author-stated | teacher forcing 与递归 draft 状态错配 | 后深度吃自生成 token/KV，学习从早期误差恢复 | 多深度 activation/logit 显存增加 | Table 1/2 loss与接受率 | supported |
| hybrid target conditioning | author-stated | DFlash shared feature 不分层；DFlare scalar fusion 表达弱 | FC 捕获跨层非线性交互，fusion residual 给每 draft layer 特化 view | 要求 target/draft hidden size 一致；额外参数 | Table 4 backbone row | partially-supported |
| hidden correction | author-stated | parallel marginal 不条件于 realized predecessor | previous embedding + current hidden 的 zero-init SwiGLU residual | 引入顺序 head 和采样开销 | Table 4 head rows；modular profile | supported |
| code/math data expansion | author-stated | uniform data 低估结构化续写 | target-regenerated domain examples 改变 proposal distribution | MT-Bench 轻微下降，需多 drafter routing | Table 4 final row | supported for measured domains |
| D-cut | author-stated | batch 内验证 slot 浪费 | prefix product 排序保持连续 prefix；$U/C$ 选 budget | confidence miscalibration、profile stale、selector overhead | live traffic only | partially-supported |
| disaggregated training | author-stated | target inference 与 draft training 资源耦合 | metadata/control 与 tensor/data 分离，经 Mooncake 流式传输 | 增加网络、Ray、buffer lifecycle 运维复杂度 | code + Section 6 | implementation-supported |

### 4.3 DFly 架构

![DFly architecture](../assets/papers/angelspec/dfly-overview.png)

![D-cut overview](../assets/papers/angelspec/dcut-overview.png)

代码与图一致：`DFlyDraftModel` 先用 `context_proj` 对多 target layers 拼接后做共享 FC，再用 `layer_fusion_weights` 的 softmax 加权和作为 residual；`HiddenStatesCorrection` 把当前位置 hidden 与前一 token embedding 分别 RMSNorm、拼接进 SwiGLU，并将 output projection 零初始化，所以初始行为退化为无 correction 的 backbone。

### 4.4 关键公式

#### F1：DFly 每层 target context

$$
g_t^{(i)}=\operatorname{RMSNorm}\left(c_t+\sum_{j=1}^{T}\alpha_j^{(i)}h_t^{(j)}\right),
\quad \alpha^{(i)}=\operatorname{softmax}(W_{\mathrm{fuse},i,:}).
$$

**这条公式在算什么？** 它为第 $i$ 个 draft layer 生成既共享又分层特化的 target 条件。

**怎么读？** 所有 draft layers 先共享一个跨层 FC context $c_t$，再各自添加对 target layers 的不同加权 view。

**输入与输出。** 输入是 target hidden states $h_t^{(j)}$ 和共享 context；输出是该 draft layer 的条件 $g_t^{(i)}$。

**变量在这里各做什么？** $W_{\mathrm{fuse}}$ 产生每层权重；$T$ 是选取的 target layer 数；$i$ 索引 draft layer。

**直觉。** 共享 FC 保留跨层非线性交互，residual 权重让浅/深 draft layer 偏向不同 target 深度。

**边界。** 代码要求 target hidden size 等于 draft hidden size；Table 4 只给累计消融。

**小例子。** 本文构造：若浅层 draft 更依赖 target 浅层局部模式，其 $\alpha^{(i)}$ 可偏向较浅层，而深层仍共享 $c_t$ 的全局语义。

#### F2：D-cut prefix survival 与吞吐选择

$$
s_{i,k}=\prod_{t=1}^{k}c_{i,t},\qquad
\rho^*=\arg\max_{\rho\in\{0.25,0.5,0.75,1\}}\frac{U(B,\rho)}{C(B,\rho)}.
$$

**这条公式在算什么？** 先估计某请求前 $k$ 个 draft 全部有用的概率，再选择预计单位时间提交 token 最多的 batch 预算。

**怎么读？** 深位置只有在前面都存活时才有价值；全局 ratio 由预计收益除以实测 step cost 决定。

**输入与输出。** 输入是 confidence、batch size、候选 ratio 与启动 profile；输出是 $\rho^*$ 和每请求连续 keep depth。

**变量在这里各做什么？** $c_{i,t}$ 是位置置信度；$s_{i,k}$ 是 prefix score；$U$ 汇总预计 token progress；$C$ 是整轮秒数。

**直觉。** 高并发下若深位置显著增加 target 延迟，分母上升会推动更小 ratio；轻载时可保留长 draft。

**边界。** confidence product 假定这些分数足以近似 prefix survival；profile 对当前硬件/图捕获有效；实现未开源。

**小例子。** 本文构造：两请求第二位置 confidence 分别 0.9 和 0.2，有限 slot 应优先给前者，而不是统一保留两位。

## 5. 关键结论与证据矩阵

![Hy3 throughput results](../assets/papers/angelspec/throughput-table7.png)

| 技术点 | 声称收益 | 对应证据 | 控制情况 | 结论 |
|---|---|---|---|---|
| MTP TTT + rollout | 改善后深度接受 | MTP ablation Tables 1-2 | architecture/data fixed | 直接支持组合目标；各 loss 贡献有限 |
| DFly backbone | 平均 MAL 3.77 -> 4.40 | Table 4 | cumulative first step | 直接 replacement baseline |
| Markov/hidden correction | 4.40 -> 4.56/4.60 | Table 4 | same backbone | direct；hidden 仅比 Markov +0.04 average |
| code/math data | 4.60 -> 4.75，MT-Bench 3.06 -> 3.02 | Table 4 | added last | direct but specialization trade-off |
| complete DFly | Hy3 MAL 4.79 vs DFlash 3.69（+29.8%） | Table 3 | MTP data differs; DFlash/DFly domain-strengthened | 整体支持，跨范式不完全同数据 |
| serving throughput | DFly average speedup 1.98x-2.40x over AR, 10.5%-11.8% over DFlash | Table 7, 8x H20 TP=8 | same table/protocol | direct in reported setup |
| D-cut live traffic | c64 +15.7% throughput，MAL -2.8% | Figure 4 | production replay; no public trace/code | correlation/official report only |

收益归因必须分层：DFly 的 MAL 增益来自模型/数据；Table 7 的 tok/s 还包含 target verification、batching 和 engine；D-cut 改的是 verification shape，不改变 candidate set 的原始质量。不能把 D-cut 吞吐收益说成 drafter 接受率提升。

## 6. Related Work 对比

| 路线 | 核心 | 优点 | 局限 | AngelSpec 关系 |
|---|---|---|---|---|
| EAGLE/MTP | target feature + AR draft | 高接受、短 horizon 稳定 | draft 随深度串行 | AngelSpec 保留为 chat drafter |
| DFlash | 一次 parallel block | draft latency 低 | suffix dependency 弱 | DFly 继承 backbone 并修正 conditioning |
| DSpark/TreeFlash | parallel backbone + causal head | 改善块内路径 | head/runtime 更复杂 | hidden correction 同类，但 DFly backbone 不等于 DSpark |
| request-local adaptive depth | confidence/policy 调每请求长度 | 避免局部浪费 | 忽略 batch 共享 target 容量 | D-cut 做跨请求全局预算 |
| TorchSpec | 解耦 hidden-state generation/training | 系统扩展性 | 本身不决定最优 drafter | AngelSpec 在其上扩展 MTP/DFly/评估 |

## 7. OpenReview 交叉核验

未发现公开 OpenReview 评审。`openreview_reviews.md` 记录了检索位置与 HTTP 403 限制；本分析没有使用匿名 reviewer 意见。

## 8. Infra 需求分析

- 训练控制面：Ray inference controller 与 training controller 只传 samples/metadata/Mooncake keys。
- 数据面：target hidden tensors 经 Mooncake RDMA/TCP；GPU Direct 可绕 CPU staging，TCP fallback 会提高 CPU/内存带宽压力。
- 训练并行：FSDP2 支持 `REPLICATE`/`FULL_SHARD`；MTP 长序列使用 Ulysses，并为深度 shift 保留 $D$-token halo。
- 数据类型：默认训练配置/代码以 bf16 参数为主，FSDP reduce 可 fp32/bf16；input IDs 为整数；论文未报告 D-cut confidence 与 profile table 的具体精度。
- serving：Hy3-295B-A21B 使用 TP=8、8x H20。D-cut 依赖离散 verification shapes 与 CUDA graph capture；论文承认当前仅 piecewise capture，selector 仍在 critical path。

隐藏状态通信量可写为：

$$
\mathrm{Bytes}=N\,L\,T\,H\,b,
\qquad \mathrm{EffectiveBandwidth}=\frac{\mathrm{Bytes}}{t},
\qquad \eta=\frac{\mathrm{EffectiveBandwidth}}{\mathrm{PeakBandwidth}}.
$$

其中 $N$ 是 batch 样本数，$L$ 是 token 数，$T$ 是 target layer 数，$H$ 是 hidden width，$b$ 是每元素字节数。论文/仓库未给 transfer runtime，所以无法计算有效带宽利用率；只声称 RDMA/TCP 与预注册 buffer 可减少复制。

## 9. 开源代码对照

- commit：`d3412bed231025ea85d35dbf5e0af44f1ac62a5b`
- DFly：`angelspec/models/draft/dfly.py`、`angelspec/models/dfly.py`、`angelspec/training/dfly_trainer.py`
- MTP/TTT：`angelspec/models/mtp.py`、`angelspec/models/draft/mtp.py`、`angelspec/training/mtp_trainer.py`
- packing/隔离：`angelspec/data/`、`tests/test_packing_safety.py`
- backend/Mooncake：`angelspec/inference/engine/`、`angelspec/transfer/mooncake/`
- D-cut：仓库全局检索无实现；论文只引用 companion paper，故 serving selector 不可由此快照复现。

测试：`pytest tests/test_dfly.py tests/test_packing_safety.py` 在 collection 阶段因当前 Transformers/`PreTrainedModel` 与 ABC 的 metaclass conflict 失败，未进入模型断言。这是环境兼容性阻塞，不足以判定仓库测试本身失败。

## 10. 优点与局限

### 优点

- 把“哪种 workload 用哪种 drafter”从经验选择提升为系统设计变量。
- 组件与系统指标分开：MAL、component latency、end-to-end throughput、live traffic 都有对应位置。
- 代码的 DFly 结构、zero-init correction、FSDP2、packing 和 backend 路径可定位。

### 局限

- D-cut 未随仓库发布；线上流量、profile table 和调度代码不可复现。
- Table 4 是 cumulative ablation，backbone/head/data 不是完整 factorial design。
- Hy3 主结果依赖私有 target、数据生成与硬件环境；论文 Conclusion 还出现 `A20B`，而正文/表格为 `A21B`，应视为编辑错误。
- workload routing 的实际策略没有给出：论文证明两类 drafter 互补，但没有展示在线 router 的准确性、切换成本与混合流量资源占用。
- 测试未在当前环境跑通；checkpoint metadata 未逐个下载核验。

## 11. 研究启发

1. 把 speculative decoding 优化目标写成 workload-conditioned policy，而非固定 architecture leaderboard。
2. 将 candidate quality、verification shape、runtime cost model 分开消融，避免 MAL 代理吞吐。
3. 后续最小实验应公开 D-cut implementation、confidence calibration curve、profile stale sensitivity，以及 MTP/DFly 在线 routing。

## 12. 待验证清单

1. $c_{i,t}$ 在不同域、温度与模型版本上是否校准？
2. D-cut profile 在 CUDA/driver/engine 更新后多久失效？
3. DFly hidden correction 的 +0.04 average 是否覆盖所有并发下的 sampler overhead？
4. 统一部署两套 drafter 的显存与调度成本是否抵消 workload specialization 收益？
5. 分布保持声明在随机 drafter/temperature sampling 路径是否仍成立？

## 13. 一句话总结

AngelSpec 的核心不是“又一个更强 drafter”，而是将 drafter 结构、训练数据和 batched verification budget 按 workload 与运行时分工；DFly 的公开证据较扎实，D-cut 的生产收益则仍受未开源实现和私有流量限制。
