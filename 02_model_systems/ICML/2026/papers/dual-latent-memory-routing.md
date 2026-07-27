# Dual-Latent Memory Routing for Vision-Language Reasoning 精读分析

> [!info] 文档关系
> - 文档类型：Paper（final PDF 深度审阅）
> - 领域入口：[README](../README.md)
> - 上位汇总：[ICML 2026 selected papers](../surveys/icml-2026-selected-papers.md)
> - 证据资产：[assets/papers/dual-latent-memory-routing](../assets/papers/dual-latent-memory-routing/)
> - 相关文档：[Paper index](../evidence/paper-index.md)，[Figure inventory](../evidence/figure-inventory.md#dual-latent-memory-routing)

> 资料状态：已逐页核验 17 页 ICML 2026 / PMLR 306 final PDF。3 个正式图表均来自 200 DPI PDF crop，保留完整 caption 并通过 contact sheet 与原分辨率逐图 QA。LaTeX/source、可用官方代码及 OpenReview 公开评审仍不可得。

## 修订信息

- 当前文档版本：`1.4.0`
- 当前修订 ID：`rev-dlmr-schema-projection-20260727`
- 当前修订时间：`2026-07-27T22:00:00+08:00`
- 替代版本：`rev-dlmr-final-pdf-promotion-20260727` / `1.3.0`

| 修订 ID | 版本 | 时间 | 类型 | 替代修订 | 摘要 | 结论影响 |
|---|---|---|---|---|---|---|
| `rev-initial-20260716` | `1.0.0` | 2026-07-16 | initial | 无 | 建立官方摘要级 blocked 交付 | material |
| `rev-source-recovery-20260724` | `1.0.1` | 2026-07-24 | evidence-update | `rev-initial-20260716` | 确认 OpenReview/ICML 身份，代码仍 404 | minor |
| `rev-dlmr-problem-solution-20260725` | `1.1.0` | 2026-07-25 | content-update | `rev-source-recovery-20260724` | 新增摘要级问题—方案闭环 | minor |
| `rev-dlmr-indexed-body-promotion-20260725` | `1.2.0` | 2026-07-25 | evidence-promotion | `rev-dlmr-problem-solution-20260725` | 提升原投稿索引方法、公式与 Tables 1–4 | material |
| `rev-dlmr-final-pdf-promotion-20260727` | `1.3.0` | 2026-07-27 | evidence-promotion | `rev-dlmr-indexed-body-promotion-20260725` | 提升 final PDF、appendix 与 3 个 QA 资产 | material |
| `rev-dlmr-schema-projection-20260727` | `1.4.0` | 2026-07-27 | mixed | `rev-dlmr-final-pdf-promotion-20260727` | 补齐标准 claim/evidence/rationale/Infra 结构与语义边界 | material：不改变论文数字，修正交付完整性 |

## 0. 资料与配图索引

- 官方页面：<https://icml.cc/virtual/2026/poster/63955>
- OpenReview：<https://openreview.net/forum?id=SFWWUr9V7c>；公开 reviews/decision/rebuttal 因 challenge 不可读。
- LaTeX/source：不可得。
- 代码：论文命名的 `Hunter-Wrynn/DLMR` 仓库返回 404，无 commit/config/checkpoint。
- Figure 2：[DLMR overview](../assets/papers/dual-latent-memory-routing/fig2-dlmr-overview-caption.png)。
- Table 1：[main results](../assets/papers/dual-latent-memory-routing/table1-main-results-caption.png)。
- Figure 3：[disentanglement ablation](../assets/papers/dual-latent-memory-routing/fig3-disentanglement-ablation-caption.png)。
- AI 生成分析图：未提升；文档输入生成能力不可用，未用生成图替代论文证据。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据 |
|---|---|---|---|---|
| DLMR | 冻结 MLLM 外接双 latent memory、injector 与 router | Dual-Latent Memory Routing | 不等于同名多智能体 memory 工作 | Abstract、§4、Figure 2 |
| visual latent memory | 输入无关、跨样本共享、面向视觉证据的 $Z^{(v)}$ | visual memory | 不是每样本 image KV cache；语义纯度未被直接 probing | §4.1、Eq. 4 |
| reasoning latent memory | 面向中间结论与约束的 $Z^{(r)}$ | reasoning memory | 不是显式文本 CoT | §4.1、Eq. 4 |
| memory injector | 将 prefix 与 latent 上下文化为 $M_t$ 的 LoRA 化副本 | $g_\phi$ | 不选择 route | Eq. 5–7 |
| eligible step | delimiter 命中且未超过 $N_{\max}$ 的候选注入位置 | routing opportunity | router 只在此子集内动作 | §4.2 |
| routing action | memory type、budget 或 null action | $a_t=(s_t,k_t)$ | 训练 sampling、推理 greedy | Eq. 8–9 |
| cross-negative learning | 用另一 memory 分支作负例，鼓励分工 | cross-negative loss | 不是普通跨样本 negatives | Eq. 10 |
| cost-aware GRPO | task、正确性条件下 efficiency 与 KL 的 router 优化 | router RL | 不更新 frozen backbone | Eq. 12 |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/单位 | 来源 | 易混点 |
|---|---|---|---|---|---|
| $I,x,y$ | 图像、文本输入、输出序列 | author-defined | per instance | Eq. 1 | $x$ 不含 $y_{<t}$ |
| $M_\theta$ | frozen base MLLM | author-defined | global model | §3 | 与 $M_t$ 不同 |
| $L_v,L,n_t$ | 视觉 token、prompt、当前可见长度 | author-defined | token count | Eq. 2–3 | $n_t=L_v+L+t-1$ |
| $\alpha_{t,i},z_{t,i},A_t^{\rm img}$ | attention weight/logit/视觉总 mass | author-defined | per step/head abstraction | Eq. 2–3 | $O(L_v/n_t)$ 是条件近似 |
| $Z^{(s)}$ | 类型 $s$ 的 latent bank | author-defined | $\mathbb R^{M_s\times d}$ | Eq. 4 | $M_s$ 不是注入数 |
| $E_t,L_t$ | 当前 multimodal embeddings/长度 | author-defined | $\mathbb R^{L_t\times d}$ | Eq. 5 | 不是 KV cache |
| $k,\mathcal K_+$ | 注入 budget/候选集合 | author-defined | token count | §4.1–4.2 | null action 独立 |
| $g_\phi,M_t$ | injector 与 contextualized memory tokens | author-defined | model / $\mathbb R^{k_t\times d}$ | Eq. 5–7 | $M_t$ 不是模型 |
| $a_t,\pi_\psi$ | route action 与 policy | author-defined | eligible step | Eq. 8–9 | gate 先决定 eligibility |
| $R_{\rm task},R_{\rm eff},\lambda_{\rm eff},\beta$ | task/efficiency rewards 与权重 | author-defined | scalar | Eq. 12 | reward 子项未隔离 |
| $\mathrm{Bytes}_{\rm KV}$ | 注入引起的 cache bytes 推导 | analysis-derived | bytes | §8.2 | 需 heads/dtype 才能数值化 |

## 0.2 AI 生成算法分析示意图

未生成。所需的 Markdown document-input 路径不可用；保留论文 Figure 2 作为机制证据，不以生成图替代。

## 1. 论文基本信息

- 领域：多模态大语言模型、长程视觉语言推理、latent memory、参数高效后训练。
- 核心问题：输出变长后，固定视觉前缀和中间约束在 monolithic context 中更难被再次调用。
- 研究目标：冻结 base MLLM，以分角色、按需注入的连续 memory 提升 general/reasoning，并控制 token/延迟。
- 关键假设：attention 不会无限向早期视觉 token 尖化；共享 latent 可形成角色分工；delimiter 是有效结构边界；新增模块足够轻量。
- 模型：Qwen2.5-VL-7B、InternVL3-8B。

## 2. 研究动机与问题—方案闭环

### 2.1 出发点与背景痛点

作者把问题明确放在长程生成阶段：图像只在固定前缀出现，而模型持续产生文本；越到后面，越需要重新访问早期 visual grounding 与已经形成的 constraints。Eq. 3 给出解释：若 attention logits 不随长度越来越尖，固定视觉 token 的总 attention mass 近似按 $O(L_v/n_t)$ 衰减。这是机制近似，不是所有层/头的无条件定理。

### 2.2 现有方案为何不够

CoT/SFT/GRPO/RAG 能改变提示、模型能力或外部知识，但没有同时显式处理两项变量：视觉证据与推理状态角色不同；不同 reasoning state 需要不同 memory 类型和容量。单 bank 可能干扰，固定 $k$ 可能不足或浪费。

### 2.3 论文计划解决的问题与成功标准

- 核心问题：冻结 MLLM 时，如何分别保存并按当前状态复用视觉证据和 reasoning constraints。
- 成功标准：主表提升；dual 优于 shared；trainable injector 优于 frozen；adaptive 优于 fixed-$k$ frontier；wall-clock 不被新增模块吞噬。
- 约束：delimiter eligibility、$N_{\max}$、frozen backbone。
- 不解决：外部知识检索、显式可读 scratchpad、通用 serving SLA。

### 2.4 核心方案如何解决并优化问题

| 失败/约束 | 对应设计 | 改变的变量/行为 | 作用机制 | 预期指标 | 证据 | 判断 |
|---|---|---|---|---|---|---|
| 视觉证据随长上下文稀释 | visual bank | 增加可重注入视觉状态 | 压缩并重访早期证据 | reasoning/general | Eq. 3–4、Table 1 | partial：未单独隔离 visual bank |
| 视觉/推理信息互相干扰 | dual $Z^{(v)},Z^{(r)}$ | 拆分参数容量 | alignment/cross-negative/separation | reasoning/overall | Figure 3 | performance supported；语义间接 |
| 静态 latent 不适配 prefix | trainable injector | 生成 step-specific $M_t$ | 联合上下文化 $E_t$ 与 latent | reasoning avg | Table 2 | supported |
| 每 token 路由/无界注入 | delimiter + $N_{\max}$ | 限定时机与次数 | 缩小动作空间 | worst-case overhead | §4.2 | plausible，未消融 |
| fixed budget 不适应状态 | type-budget router | 选择 $s_t,k_t$/null | 状态依赖 role/capacity | accuracy/token | Table 4 | supported |
| correctness-only 会过注入 | cost-aware GRPO | reward 加 efficiency/KL | 正确前提下降低使用 | token/latency | Eq. 12、Table 4/A1 | partially supported |
| 联合训练目标混杂 | three stages | 分离 bank/interface/policy 更新 | 分阶段优化 | stability/quality | Eq. 10–12 | plausible，未替换验证 |

### 2.5 完整因果链与证据闭环

长生成需要持续访问视觉证据与中间约束 → 单一 context 可能 attention dilution 且角色混存 → dual banks 改变可用状态容量 → injector 改变 latent 与 prefix 的条件关系 → gate/router 改变注入时机、类型和 token 数 → 预期改善质量与 accuracy–cost frontier → Table 1、Figure 3、Tables 2/4、Appendix A1 分别测完整质量、分离、接口、预算和部分延迟。

- 直接：dual/shared、trainable/frozen injector、adaptive/fixed budget、两个 backbone 主结果。
- 间接/混杂：latent 语义纯度、Stage 1 loss、cost reward 子项、three-stage necessity。
- 未验证：delimiter/$N_{\max}$ sensitivity、代码一致性、production serving。

## 3. 核心贡献与创新点

1. 双角色 latent memory：解决 visual/reasoning state 混存；Figure 3。
2. prefix-conditioned memory interface：解决 input-agnostic latent 不适配；Table 2。
3. 受限 type-budget routing：解决 fixed budget；Table 4。
4. 三阶段 cost-aware training：分离表征、接口和 control；Eq. 10–12，但子项未全部隔离。
5. 跨 backbone 质量和部分 wall-clock 证据；Table 1、Appendix A1。

## 4. 研究方法

### 4.1 方法总览

输入 $I,x$，frozen $M_\theta$ autoregressively 生成 $y$。训练依次学习 banks、injector、router。推理时 gate 先确定候选位置，router 选择 type/budget/null，injector 生成 $M_t$ 并加入上下文，再由 base model 解码。

### 4.2 组件级设计动机与具体问题映射

| 设计 | why 状态/证据 | 具体问题 | 因果机制 | 替代/权衡 | 验证 | 判断 |
|---|---|---|---|---|---|---|
| frozen backbone | author-stated，Abstract/§3 | 参数/能力漂移 | 只更新 memory-side | full/adapter tuning 更强但贵 | 无等容量对照 | unverified quantitatively |
| dual banks | author-stated，Eq. 4 | role interference | 分参数子空间 | shared 简单 | Figure 3 | supported for performance |
| alignment loss | author-stated，Eq. 10 | latent-target 不对齐 | 拉近表示 | reconstruction/distillation | 无 | unverified |
| cross-negative | author-stated，Eq. 10 | 两 bank 相似 | 另一分支作负例 | cross-sample negatives | 无 | unverified |
| separation loss | author-stated，Eq. 10 | branch collapse | 增加分支距离 | orthogonality | Figure 3 间接 | confounded |
| LoRA injector replica | author-stated，Eq. 5–7 | 静态 latent | base-like contextualization | cross-attention 更轻 | Table 2 | injector supported；replica 未隔离 |
| Stage-2 random routes | inferred，Figure 2/§4.3 | interface route coverage | 暴露多种组合 | curriculum/on-policy | 无 | plausible |
| delimiter | author-stated，§4.2 | per-token route | 限制候选点 | learned trigger | 无 | unverified |
| $N_{\max}$ | author-stated，§4.2 | 无界次数 | 硬上限 | soft budget | 无 | unverified |
| type-budget-null router | author-stated，Eq. 8–9 | fixed capacity | 按 state 选 role/capacity | continuous mixture | Table 4 | supported |
| cost-aware GRPO | author-stated，Eq. 12 | over-injection | task+efficiency+KL | constrained RL | Table 4/A1 间接 | partially supported |

### 4.3 模型/系统架构

![Figure 2. DLMR 总体架构、三阶段训练与推理路由。](../assets/papers/dual-latent-memory-routing/fig2-dlmr-overview-caption.png)

Figure 2 显示 delimiter 位于 router 前，因此“router 决定何时”应限定为“在规则允许的位置选择是否及如何注入”。

### 4.4 关键公式

$$
P(y\mid I,x)=\prod_{t=1}^{T}P(y_t\mid I,x,y_{<t}),
$$

$$
A_t^{\mathrm{img}}
=\sum_{i\in V}\alpha_{t,i}
\approx O\!\left(\frac{L_v}{n_t}\right)
\xrightarrow[t\to\infty]{}0,
$$

$$
Z^{(s)}\in\mathbb R^{M_s\times d},\quad
M_t=g_\phi(E_t,Z^{(s)}_{1:k},k)\in\mathbb R^{k\times d},
$$

$$
a_t=(s_t,k_t),\qquad
\max_\psi\;
\mathbb E_{\tau\sim\pi_\psi}
[R_{\rm task}+\lambda_{\rm eff}R_{\rm eff}]
-\beta\,\mathrm{KL}(\pi_\psi\Vert\pi_{\rm ref}).
$$

### 4.5 训练/实验/部署设计

- 数据：所选 benchmark training split；无 training split 者仅评估；加入 OpenMMReasoner。
- Stage 1：alignment、cross-negative、separation。
- Stage 2：SFT/GRPO 变体训练 memory/injector。
- Stage 3：cost-aware GRPO 训练 router。
- Baselines：CoT、CCoT、SFT、GRPO、Visual-RFT、RCTS-RAG。
- 缺口：训练 token/预算、LoRA rank、loss weights、seed/方差、GPU/precision、chat template、代码/config。

## 5. 关键结论

### 5.1 主结果

![Table 1. 两个 backbone 上的主结果。](../assets/papers/dual-latent-memory-routing/table1-main-results-caption.png)

- Qwen SFT general：65.62 → 71.45，绝对 +5.83，相对约 +8.9%。
- Qwen GRPO reasoning：50.29 → 56.45，绝对 +6.16，相对约 +12.2%。
- InternVL SFT general：73.37 → 79.25，绝对 +5.88，相对约 +8.0%。
- InternVL GRPO reasoning：54.33 → 63.08，绝对 +8.75，相对约 +16.1%。

主表是 bundled complete-method evidence，不能归因给单一组件。

### 5.2 消融和机制证据

![Figure 3. shared 与 dual memory 的分离消融。](../assets/papers/dual-latent-memory-routing/fig3-disentanglement-ablation-caption.png)

| 技术点 | 声称效果 | 实验 | 控制 | 指标变化 | 证据强度 | 结论 |
|---|---|---|---|---|---|---|
| dual vs shared | 减少干扰 | Figure 3 | matched replacement | overall 52.05→59.73；reasoning 46.61→53.84 | direct | performance supported，语义 indirect |
| trainable injector | prefix adaptation | Table 2 | frozen vs trainable | 50.44→53.84 | direct | supported |
| adaptive route | accuracy/token | Table 4 | fixed $k=4,8,16$ | adaptive 53.84/677；$k=8$ 52.71/732 | replacement | supported |
| alignment/cross-negative | 表征/分离 | 无单项 | none | 无 | none | unverified |
| separation loss | 防 collapse | Figure 3 整体 | confounded | 无 loss delta | indirect | partial |
| delimiter/$N_{\max}$ | 控制触发/次数 | 无 | none | 无 | none | unverified |
| cost reward | 控制 token | Table 4/A1 整体 | confounded | mixed | indirect | partial |
| frozen 参数效率 | 少量新增参数 | paper claim | unknown | 无完整 compute-normalized 表 | none | unverified |
| runtime | token→wall-clock | Table A1 | reported setup | Qwen reasoning 14.0s→11.5s；InternVL general 3.5s→3.7s | direct system | mixed |

### 5.3 是否验证了假设

| 假设 | 证据 | 结论 |
|---|---|---|
| 分离 memory 减少干扰 | Figure 3 | accuracy 支持；语义纯度间接 |
| latent 需上下文化 | Table 2 | 支持 |
| adaptive 优于 fixed | Table 4 | 对测试过的 $k$ 支持 |
| cost reward 有系统收益 | Table 4/A1 | 部分支持、不同路径不一致 |
| three-stage 优于 joint | 无 | 未验证 |

### 5.4 收益来源归因

| 变化 | 基线 | 指标 | 影响路径 | 证据 |
|---|---|---|---|---|
| shared→dual | Figure 3 | overall +7.68 | representation→quality | matched |
| frozen→trainable injector | Table 2 | +3.40 | interface→quality | matched |
| fixed $k=8$→adaptive | Table 4 | +1.13、-55 tokens | routing→quality/token | replacement |
| base→full DLMR | Table 1 | +5.83 至 +8.75 | bundled→quality | confounded |
| base→DLMR runtime | Table A1 | -2.5s 至 +0.2s | token/overhead→latency | setup-specific |

不同实验不是 factorial design，delta 不可相加。

## 6. Related Work 对比

| 类别 | 核心 | 优点 | 局限 | 与本文关系 |
|---|---|---|---|---|
| CoT/CCoT | 文本推理 | 无新模块 | 更长 context | DLMR 用 continuous state |
| SFT/GRPO/RFT | 更新能力/policy | 直接提升任务 | 不显式分状态 | DLMR 可叠加 |
| RAG | 外部检索 | 补外部证据 | corpus/query overhead | DLMR 是内部 memory |
| single latent | 单 bank | 简单 | 角色混合 | Figure 3 |
| fixed injection | 固定 $k$ | 可预测 | 不适应状态 | Table 4 |

## 7. OpenReview 公开评审 × 论文内容交叉核验

- 访问日期：2026-07-27。
- forum/API：anti-bot challenge。
- decision/meta-review/rebuttal：不可得。

因此不能构造 reviewer concern 表或判断 final revision 如何响应评审。该分支是 `blocked`，不是 `passed`。

## 8. Infra 需求分析

### 8.1 算力

$$
\Delta\mathrm{FLOPs}_{\rm attn}\propto(2nk_t+k_t^2)d.
$$

injector 可能运行 LoRA 化模型副本；无代码/profiler 不能数值化。

### 8.2 显存与存储

$$
\mathrm{Bytes}_{\rm KV/injection}
\approx2L_{\rm layer}k_tn_{\rm kv}d_hb.
$$

双 bank 参数约 $(M_v+M_r)d$ elements；injector/router 参数未知。

### 8.3 Data Types / 数值格式

weights、activations、latent、KV、router 的实际 dtype 均未充分报告；不能假定 bf16/fp16/fp8/量化路径。

### 8.4 带宽、互联与高效利用

$$
\mathrm{BytesMoved}\gtrsim k_tdb+
2L_{\rm layer}k_tn_{\rm kv}d_hb,\quad
\mathrm{EffectiveBandwidth}=\frac{\mathrm{BytesMoved}}{t}.
$$

无 bytes、peak bandwidth、timeline，不能算利用率或判断 NVLink/RDMA。

### 8.5 CPU/GPU/NPU 异构执行

未报告 host-device transfer、CPU preprocessing、NPU path、DMA、pinned memory、fallback 或 overlap；异构行为未验证。

### 8.6 调度/Serving/自定义算子

动态 $k_t$ 和不等注入次数可能破坏 batch shape、CUDA graph 和 KV allocator。论文无 continuous batching、paged KV、custom kernel、throughput/p95/p99。

## 9. 开源代码对照

仓库返回 404，无 commit、config、checkpoint 或本地 snapshot。dual banks、injector、gate/router、loss/GRPO、serving 均不能做代码一致性核验。

## 10. 优点与局限

### 优点

- paper-level problem、机制与三类替换消融有清晰局部闭环。
- 不只报告完整方法，还隔离 dual、injector、adaptive budget。
- Appendix 给出部分 wall-clock。

### 局限

- loss、delimiter、$N_{\max}$、staged recipe、reward terms 未 factorially ablate。
- semantic specialization 缺直接 probing。
- 无代码/config/checkpoint/reviews。
- runtime 设置有限，且存在轻微变慢路径。

### 可改进之处

补 loss/trigger/budget 独立消融、等参数 shared/dual、latent probing、代码/config/checkpoint，以及 throughput/tail-latency/KV telemetry。

## 11. 研究启发

- 分角色长期状态 + 小 policy 控制访问。
- 学习式 eligibility、连续 mixture、按请求硬预算。
- 最小复现应先闭环 Figure 3、Table 2、Table 4，再测长度—attention—route—latency。

## 12. 解读问题/待验证清单

1. Eq. 3 在真实层/头上与错误的因果关系有多强？
2. dual 提升是否只是容量增加，shared 是否等参数？
3. alignment/cross-negative/separation 各自贡献多少？
4. delimiter 与 $N_{\max}$ 如何跨回答格式泛化？
5. injector replica 的 rank、层数、KV 与 FLOPs 是多少？
6. Stage 2 random routes 是否匹配推理分布？
7. reward 子项分别影响 accuracy/token/latency 多少？
8. 主表是否同数据、同训练 token、同搜索预算？
9. Appendix latency 是否包含 encoder/injector/sync/warmup？
10. 动态 route 对 continuous batching 和 tail latency 有何影响？
11. 代码和公开评审何时可用？

## 13. 一句话总结

DLMR 用双 latent memory、上下文化 injector 和受约束的 type-budget router，为长程视觉语言推理建立了较完整的“状态分离—按需复用—质量/成本”链条；最大不确定性是角色语义、训练子项和真实 serving 行为仍缺代码与独立消融验证。
