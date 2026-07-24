# Dual-Latent Memory Routing for Vision-Language Reasoning 精读分析

> 交付状态：**blocked**。ICML/OpenReview 身份与 Spotlight 状态已确认，搜索索引恢复了原投稿的部分方法、公式和表格文本；但 OpenReview 的 Cloudflare challenge 阻断了本地可读 PDF、公开评审与最终修订核验，代码链接当前返回 404。本文不把搜索索引转录伪装成 PDF、代码或最终版本复核。

## 修订信息

- 当前文档版本：`1.1.0`
- 当前修订 ID：`rev-refresh-r2-20260724`
- 当前修订时间：`2026-07-24T17:54:44+08:00`
- 替代版本：`rev-initial-20260716` / `1.0.0` / manifest SHA-256 `4371334aa259856f2ddafec22e9bead4ef3eb1bda1f1f8733c7887e2d7469c31`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rev-initial-20260716` | `1.0.0` | `2026-07-16T19:16:43+08:00` | `review_dual_latent` | `initial` | 无 | 无 | 建立官方摘要级 blocked 交付 | 精确 PDF 在受控恢复后仍不可得 | `analysis.md`; `figure_inventory.md`; `openreview_reviews.md` | ICML official poster 63955; `recovery/recovery_log.md` | material |
| `rev-refresh-r2-20260724` | `1.1.0` | `2026-07-24T17:54:44+08:00` | `dual_latent_refresh_r2` | `mixed` | tracked `rev-initial-20260716` / `1.0.0` / `4371334aa259856f2ddafec22e9bead4ef3eb1bda1f1f8733c7887e2d7469c31` | 无 | 新增搜索索引方法/实验转录、精确下载日志、代码 404 核验、设计动机与技术 claim 矩阵、infra 推导和公共评审状态；仍保持 blocked | 新发现的 OpenReview/ICML 页面显著扩展摘要级证据，但本地 PDF、最终修订、代码与评审正文仍不可得 | `analysis.md`; `extracted_text/search_index_evidence.md`; `retrieval/acquisition_log.md`; `figure_inventory.md`; `openreview_reviews.md` | task packet; indexed original-submission attachment; ICML poster page; bounded retrieval attempts | material |

## 0. 资料与配图索引

- 论文身份：OpenReview forum `SFWWUr9V7c`；ICML poster `63955`；ICML 2026 Spotlight。
- 原投稿：索引 URL `https://openreview.net/attachment?id=SFWWUr9V7c&name=originally_submitted_PDF`；本地 PDF **blocked**。
- 源码/LaTeX：任务包为 `unknown`，无公开 source URL；**blocked**。
- 开源代码：OpenReview 索引声称 `https://github.com/Hunter-Wrynn/DLMR`；clone 与 GitHub API 检查失败/404，**blocked**。
- 公开评审：Spotlight 决策层级已核验；reviews/meta-review/rebuttal/discussion 正文 **blocked**，见 `openreview_reviews.md`。
- 搜索索引转录：`extracted_text/search_index_evidence.md`。
- 采集日志：`retrieval/acquisition_log.md`。
- 图表：0 张；机制 visual 与结果 visual 都因无可读 PDF 而 blocked，见 `figure_inventory.md`。
- AI 生成分析示意图：`skipped-with-reason`。已安装的 OpenRouter ICU CLI 仅支持 `generate`/`edit`，不支持技能要求的 `responses-doc --input-file analysis.md`，因此未用 prompt-only 方式替代。
- 知识组织：本目录是 `_artifacts` process workspace；canonical Paper/Asset promotion 由父 survey agent 负责。本交付不修改任何正式/global 路径。

## 0.1 术语与符号解释

本章是本文唯一术语/符号定义入口。后文只引用这里的定义，不另建散落 glossary。来源均指向索引恢复的原投稿文本；未核验最终 PDF 时，所有定义保留版本限定。

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| DLMR | 在冻结 MLLM 上增加双 latent bank、injector 和动态 router 的方法 | Dual-Latent Memory Routing | 不是同名的 VLA/多智能体 dual-memory 工作 | indexed Abstract; indexed Section 4; `extracted_text/search_index_evidence.md` |
| visual latent-space memory | 输入无关、跨样本共享的可学习 latent bank \(Z^{(v)}\)，预期经 injector 上下文化为视觉证据 token | visual memory, \(Z^{(v)}\) | 不是每个样本的图像 KV cache，也不能由 bank 名称直接证明其只编码视觉信息 | indexed Section 4.1, Eq. 4–7 |
| reasoning latent-space memory | 输入无关、跨样本共享的可学习 latent bank \(Z^{(r)}\)，预期表征中间结论/约束 | reasoning memory, \(Z^{(r)}\) | 不是显式 scratchpad 文本；语义专化仍需机制证据 | indexed Section 4.1, Eq. 4–7 |
| memory injector | 将当前上下文和选中 latent bank 前 \(k\) 个向量映射为 \(k\) 个 step-specific memory tokens 的 LoRA 化副本模型 | injector, \(g_\phi\) | 不是 router；injector 负责内容上下文化，router 负责时机/类型/预算 | indexed Section 4.1, Eq. 5–7 |
| eligible step | 生成前缀以某个 delimiter pattern 结束、且未超过注入次数上限时允许路由的 decoding step | routed insertion point | 不是每个 token step；资格门控本身是手工规则，不是 router 学出的时机 | indexed Section 4.2 |
| routing action | 在 eligible step 选择 memory 类型和注入预算的离散动作 \((s_t,k_t)\) | route, \(a_t\) | 不包含无条件逐步注入；非 eligible step 确定性不注入 | indexed Eq. 8–9 |
| injection budget | 一次注入使用的 latent/token 数 \(k\)；示例集合为 \(\{4,8,16\}\) | latent token length, budget | 不等于总生成 token 数；总注入上界还取决于 \(N_{\max}\) | indexed Section 4.1–4.2 and Table 4 |
| three-stage training | Stage 1 latent bank 预热；Stage 2 injector+memory 训练；Stage 3 router GRPO | pre-warm / injector training / router learning | 不是三阶段都端到端更新；backbone 始终冻结，router 在 Stage 3 才训练 | indexed Section 4.3, Eq. 10–12 |
| token efficiency | 论文用生成 token 长度和注入预算的 accuracy–cost 关系描述效率 | reduced decoding tokens | 不等于 wall-clock latency、throughput、FLOPs 或 HBM traffic 改善 | indexed Table 4/Figure 4; no runtime artifact |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/索引 | 单位/取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|
| \(s\) | memory 类型 | author-defined | bank/route | \(v\) 或 \(r\) | indexed Eq. 4, 8 | \(v/r\) 是预期语义标签，不是已证明的纯语义分解 |
| \(Z^{(s)}\) | 第 \(s\) 类共享 latent bank | author-defined | 全局共享 | \(\mathbb R^{M_s\times d}\) | indexed Eq. 4 | 搜索索引未给 \(M_s,d\) 数值 |
| \(M_s\) | bank 中 latent 数 | author-defined | per bank | 正整数，值未知 | indexed Eq. 4 | 与 step-specific tokens \(M_t\) 名称接近 |
| \(d\) | backbone embedding width | author-defined | per token | 维度，值未知 | indexed Eq. 4–5 | 不等于 injector width \(d_w\) |
| \(E_t\) | step \(t\) 的 image+text-prefix embeddings | author-defined | per decoding step | \(\mathbb R^{L_t\times d}\) | indexed Eq. 5 | 是 embeddings，不是 KV cache |
| \(L_t\) | step \(t\) 上下文长度 | author-defined | per step | tokens | indexed Eq. 5–7 | 会随生成与注入增长 |
| \(k,k_t\) | 单次选择/注入的 latent token 数 | author-defined | per injection | \(\mathcal K_+\)，示例 \(\{4,8,16\}\) | indexed Eq. 5, 8–9 | Table 4 的 fixed \(k\) 与 router 的动态 \(k_t\) 要区分 |
| \(g_\phi\) | 参数为 \(\phi\) 的 memory injector | author-defined | Stage 2/推理 | function | indexed Eq. 5–7, 11 | 与冻结 backbone \(\theta\) 不同 |
| \(M_t\) | step \(t\) 生成的 memory tokens | author-defined | per injection | \(\mathbb R^{k\times d}\) | indexed Eq. 5, 7, 9 | 不等于 bank size \(M_s\) |
| \(\mathcal D\) | eligible delimiter pattern 集 | author-defined | decoding policy | 集合，内容未知 | indexed Section 4.2 | 手工 eligibility rule，未由 router 学习 |
| \(N_{\max}\) | 每样本 routed injection 上限 | author-defined | per sample | count，值未知 | indexed Section 4.2 | 不等于单次 budget \(k\) |
| \(a_t=(s_t,k_t)\) | eligible step 的离散路由动作 | author-defined | per eligible step | categorical action | indexed Eq. 8 | “when” 部分受 eligibility gate 预先限制 |
| \(\pi_\psi\) | 参数为 \(\psi\) 的 router policy | author-defined | Stage 3/推理 | action distribution | indexed Eq. 8–9, 12 | 推理使用 greedy，训练使用 sampling |
| \(t_v,t_r\) | 冻结 backbone 提供的视觉/推理 teacher pooled representations | author-defined | Stage 1 | vectors，维度未知 | indexed Stage 1 prose | 不是独立外部 teacher model |
| \(z_v,z_r\) | 注入 memory token 得到的 student pooled representations | author-defined | Stage 1 | vectors，维度未知 | indexed Eq. 10 prose | 与 latent bank \(Z^{(s)}\) 大写符号不同 |
| \(m\) | cross-teacher hinge margin | author-defined | Stage 1 | scalar，值未知 | indexed Eq. 10 | 超参数未恢复 |
| \(\lambda_{\rm neg},\lambda_{\rm sep}\) | cross-teacher 与 separation 权重 | author-defined | Stage 1 | scalar，值未知 | indexed Eq. 10 | 不能从公式判断稳定性 |
| \(\epsilon\) | specialization-preservation loss 权重 | author-defined | Stage 2 | scalar，值未知 | indexed Eq. 11 | 搜索抽取可能丢失字体/下标 |
| \(\tau\) | 带路由动作的 sampled decoding trajectory | author-defined | Stage 3 | trajectory | indexed Eq. 12 | 不是 temperature |
| \(R_{\rm task},R_{\rm eff}\) | 任务正确性与效率 reward | author-defined | Stage 3 | reward | indexed Eq. 12/Appendix-B prose | \(R_{\rm eff}\) 仅在答案正确时计入；精确公式未恢复 |
| \(\lambda_{\rm eff},\beta\) | 效率 reward 与 KL 权重 | author-defined | Stage 3 | scalar，值未知 | indexed Eq. 12 | 没有 sensitivity 证据 |
| \(\pi_{\rm ref}\) | 稳定 router 学习的固定参考 policy | author-defined | Stage 3 | policy | indexed Eq. 12 | checkpoint/初始化未知 |
| \(b\) | 每元素字节数 | analysis-derived | infra 推导 | bytes，例如 fp16/bf16 为 2；本文实际精度未知 | Section 7 derivation | 不是论文报告符号 |
| \(L,n_{\rm kv},d_h\) | decoder 层数、KV heads、head dimension | analysis-derived | KV 开销推导 | counts/dimension，值未知 | Section 7 derivation | 未从代码/config 核验 |

## 1. 论文基本信息

- 领域：多模态长链推理、latent memory、参数高效适配与动态路由。
- 核心问题：长生成中模型对早期图像证据的有效访问下降，并可能丢失中间约束。
- 目标：在冻结 7B/8B MLLM 上，用小型 memory-related 参数实现可选择的视觉/推理记忆复用。
- 已确认身份：Hao-Xuan Ma, Jin-Fei Qi, YiCheng Xiao, Han-Jia Ye；ICML 2026 Spotlight。
- 关键证据边界：方法/表格来自索引的 **original submission**；accepted final PDF 和修订差异未知。

## 2. 核心贡献与创新点

1. 把“视觉证据”和“中间推理约束”建模成两个共享 latent bank，并在需要时上下文化为 token；索引 Section 4/Eq. 4–7 支撑架构描述。
2. 用 delimiter eligibility + 离散 router 分离“哪些 step 可以注入”与“注入哪类/多少”；索引 Section 4.2/Eq. 8–9 支撑。
3. 用三阶段训练降低 joint optimization 难度：先形成分离 latent，再训练 injector，最后用 cost-aware GRPO 学 router；索引 Eq. 10–12 支撑。
4. 搜索索引中的 matched ablation 分别支持 dual-vs-shared memory、trainable-vs-frozen injector、adaptive-vs-fixed budgets；但代码、最终 PDF 与方差/seed 未核验。

## 3. 研究方法

### 3.1 问题到方案的逻辑链

单一增长上下文中视觉 attention/约束保持变弱  
\(\rightarrow\) 建立视觉与推理两个可复用 latent bank  
\(\rightarrow\) injector 按当前 prefix 将静态 bank 上下文化  
\(\rightarrow\) eligibility gate 限制可注入位置，router 决定类型与预算  
\(\rightarrow\) 用分阶段训练把表征分离、上下文化和 cost-aware 决策依次学习。

这条链条在概念上闭合，但只有组件替换消融；“视觉 bank 真的只保存视觉、推理 bank 真的只保存约束”的因果语义仍主要是间接证据。

### 3.2 设计动机与具体问题映射

| 设计项 | why 状态 | 原文证据 | 针对的具体问题 | 因果机制 | 替代方案/权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|---|
| dual latent banks | author-stated | Intro; Eq. 4; disentanglement ablation | 单一 buffer 混合视觉证据与推理约束，产生干扰 | 两个参数子空间提供专化容量，减少跨类型干扰 | 单 bank 更简单；显式 scratchpad 更可解释但更长 | shared 47.53 vs dual 53.84；MathVision +8.64 | supported for separation, not semantic purity |
| input-agnostic shared banks | inferred | Eq. 4/Section 4.1 明确结构，但未给 why | 避免每样本外部 memory store 与额外写入系统 | 学到可复用 latent slots，再由当前 context 上下文化 | per-example cache 更具体但存储/更新更重；共享 bank 可能模板化 | 无独立 ablation | plausible, unverified |
| LoRA replica injector | author-stated for parameter efficiency; architecture choice why partly inferred | Eq. 5–7 | 静态 latent 不能直接适配当前问题状态 | latent 对当前 context self-attend 后投影回 backbone space | cross-attention 小模块更轻；完整副本表达力强但计算更贵 | frozen 50.44 vs trainable 53.84 | injector need supported; replica choice unisolated |
| delimiter-based eligibility | author-stated for stability/control overhead | Section 4.2 | 每 token 路由开销大且动作空间不稳定 | 只在结构边界决策，减少路由次数 | learned trigger 更灵活；固定周期更简单 | 无 delimiter/trigger ablation | plausible, unverified |
| per-sample \(N_{\max}\) | author-stated for overhead control | Section 4.2 | 注入次数无界导致 latency/context 增长 | 硬上限约束最坏注入开销 | soft cost penalty 更自适应但无硬保证 | 未恢复 sensitivity | unverified |
| discrete type+budget router | author-stated | Eq. 8–9; Table 4 | 不同状态需要不同 memory 类型与容量 | 依据当前 hidden state选择 \((s_t,k_t)\) | 连续 mixture 可微但可能总激活；fixed budget 简单但浪费 | adaptive 53.84/677 tokens vs best fixed accuracy 52.71/732 | supported against tested fixed budgets |
| greedy inference | inferred (reproducibility explicitly stated) | Section 4.2 | sampling 引入部署方差 | 取最大概率动作保证确定性 | sampling/exploration 可能改善难例但不稳定 | 无 decoding-policy ablation | operationally motivated, quality trade-off unknown |
| Stage 1 dual-teacher alignment + separation | author-stated | Eq. 10 | 两个 bank 可能 collapse 成同一表示 | within-branch alignment + cross-branch negative/separation | orthogonality loss、contrastive loss；过强分离可能损伤共享信息 | dual-vs-shared 是间接证据；无 loss-term ablation | partially supported |
| Stage 2 mixed types/budgets | author-stated | Eq. 11 prose | injector 可能只适配单一 memory/budget | 训练时覆盖多种 route conditions，提高接口鲁棒性 | curriculum 或 exhaustive schedules；混合会增加训练方差 | 无 mixed-training ablation | plausible, unverified |
| Stage 3 correctness-gated efficiency GRPO | author-stated | Eq. 12; indexed Appendix-B prose | 仅优化准确率会过度注入，直接惩罚预算又可能牺牲正确性 | 只在答对时奖励小预算，先保正确再压成本 | constrained RL/Pareto optimization；reward hacking 风险 | Table 4 为整体 router 证据，无 reward-term ablation | partially supported |
| frozen backbone | author-stated for parameter efficiency | Abstract; Section 4.3 | 避免全参训练成本和能力漂移 | 只更新 memory-related parameters | adapters/full fine-tuning 可能更强但成本更高 | 与 SFT/GRPO baseline 的公平性需最终 appendix/code | plausible; capacity match unverified |

### 3.3 架构与推理阶段

1. **Memory construction（训练）**：学习两个全局 bank \(Z^{(v)},Z^{(r)}\)。
2. **Eligibility gating（推理）**：prefix 命中 delimiter 且注入计数未超 \(N_{\max}\) 才允许 route。
3. **Routing（推理）**：\(\pi_\psi\) 从最新 hidden state 选择 \(s_t,k_t\)。
4. **Injection（推理）**：\(g_\phi\) 把 bank 前 \(k_t\) 个 latent 与 \(E_t\) 联合上下文化为 \(M_t\)。
5. **Backbone decoding（推理）**：将 \(M_t\) 追加到上下文后继续由冻结 backbone 预测。

这里“router 决定 when”要加限定：真正的“何时”先被手工 eligibility gate 截断；router 只在 eligible subset 内行动。

### 3.4 关键公式

核心公式已在术语与符号章完整定义。索引恢复最关键的结构式与目标为：

$$
Z^{(s)}\in\mathbb{R}^{M_s\times d},\qquad
M_t=g_\phi(E_t,Z^{(s)}_{1:k},k)\in\mathbb{R}^{k\times d}.
$$

$$
a_t=(s_t,k_t),\qquad
s_t\in\{v,r\},\quad k_t\in\mathcal K_+.
$$

$$
\max_\psi\ \mathbb E_{\tau\sim\pi_\psi}
\left[R_{\rm task}(\tau)+\lambda_{\rm eff}R_{\rm eff}(\tau)\right]
-\beta\,{\rm KL}(\pi_\psi\Vert\pi_{\rm ref}).
$$

Eq. 10/11 的搜索抽取存在排版丢失风险，因此本报告只使用其结构含义，不声称逐字符复原。

### 3.5 训练/实验/部署事实与缺口

- 报告 backbones：Qwen2.5-VL-7B、InternVL-3-8B；搜索索引另暴露了小模型扩展表，但表号/型号行存在抽取错位，不纳入主要结论。
- 数据：有训练 split 的选定 benchmark + OpenMMReasoner；无训练 split 的 benchmark 只评估。
- Stage 2 有 SFT 和 GRPO 版本，主表分别与对应训练范式比较。
- 未核验：样本数、重复/泄漏检查、prompt/chat template、GRPO group size、reward 实现、LoRA rank、optimizer、epochs、seed/方差、GPU、precision、final revision。

## 4. 关键结论

### 4.1 主结果

| 对比 | 基线 | DLMR | 绝对变化 | 相对变化 | 证据等级 |
|---|---:|---:|---:|---:|---|
| Qwen 7B general avg: SFT → DLMR-SFT | 65.62 | 71.45 | +5.83 | +8.88% | indexed Table 1; complete-method, confounded |
| Qwen 7B reasoning avg: GRPO → DLMR-RL | 50.29 | 56.45 | +6.16 | +12.25% | indexed Table 1; complete-method, confounded |
| InternVL 8B general avg: SFT → DLMR-SFT | 73.37 | 79.25 | +5.88 | +8.01% | indexed Table 1; complete-method, confounded |
| InternVL 8B reasoning avg: GRPO → DLMR-RL | 54.33 | 63.08 | +8.75 | +16.11% | indexed Table 1; complete-method, confounded |

这些数字支持“完整 DLMR 版本在两个 backbone 上优于所列对应 post-training baseline”，但未核验 final PDF、代码、方差和训练预算，不能推出可复现效果。

### 4.2 技术 claim 证据矩阵

| 技术点 | 声称收益 | 对应证据 | 对照 | 指标变化 | 强度分类 | 结论 |
|---|---|---|---|---|---|---|
| dual 而非 shared bank | 减少视觉/推理干扰 | disentanglement ablation | matched replacement（按索引） | avg +6.31；MathVision +8.64 | direct ablation | separation supported；语义专化仅间接 |
| trainable injector | 把 latent 转成 context-aligned token | Table 2 | frozen vs trainable | avg +3.40 | direct ablation | injector 学习必要性 supported |
| adaptive route/budget | 更好 accuracy–token frontier | Table 4 | fixed \(k=4,8,16\) | vs \(k=8\): +1.13 acc, -55 tokens | replacement baseline | supported against tested fixed budgets |
| Stage 1 cross-teacher hinge | 防止错分支/坍缩 | 无单项 ablation | none | 无 | missing | unverified |
| Stage 1 separation term | 促使 bank 专化 | dual-vs-shared only bundles multiple effects | confounded | 无单项 delta | indirect/confounded | plausible, not isolated |
| Stage 2 mixed budgets/types | 提高 injector robustness | 无单项 ablation | none | 无 | missing | unverified |
| correctness-gated \(R_{\rm eff}\) | 在正确性前提下降低预算 | 完整 router vs fixed route | confounded | Table 4 overall | indirect/confounded | partially supported |
| delimiter eligibility | 控制稳定性和 overhead | 无 trigger ablation | none | 无 | missing | unverified |
| frozen backbone/parameter efficiency | 少量新增可训练参数 | 摘要 claim；无参数清单 | unknown | 无 | correlation/no local config | unverified quantitatively |
| reduced long-generation tokens | 降低冗余 decoding | Table 4 fixed-budget comparison | no vanilla token baseline in recovered evidence | router 677 vs fixed 732/765, but vs \(k=4\) 664 | partial | limited frontier claim supported；broad vanilla reduction unverified |
| state-dependent specialized roles | 可解释 route 与 memory 专化 | 摘要/索引称 appendix analysis | visual unavailable | 无可核验图 | missing visual | unverified |

### 4.3 假设核验

- “双 bank 比 shared bank 好”：有直接替换消融，支持。
- “bank 语义分别是视觉和推理”：没有可视化/最终 appendix，只有 loss 与性能间接支持。
- “learned injector 必须”：有 frozen-injector ablation，支持。
- “adaptive router 比 fixed budget 好”：对测试的三个 fixed budgets 支持；是否优于更强 continuous/gated baseline 未知。
- “更少 token 等于更快”：不成立。没有 wall-clock、throughput 或 kernel/serving 证据。

### 4.4 收益来源归因

| 组件 | 对比 | 变化 | 影响路径 | 证据强度 |
|---|---|---|---|---|
| dual bank | shared bank | +6.31 reasoning avg | 表征分离/干扰减少 | matched ablation；语义解释仍间接 |
| trainable injector | frozen injector | +3.40 reasoning avg | context-specific latent contextualization | matched ablation |
| adaptive router | best fixed-accuracy \(k=8\) | +1.13 acc, -55 tokens | state-dependent budget allocation | replacement baseline |
| RL variant | DLMR-SFT → DLMR-RL on Qwen reasoning | 53.84 → 56.45 (+2.61) | task/reward optimization | rough inferred; SFT/RL objectives differ |

最后一行只是表格桥接近似，不是论文正式方差分解。三项 ablation 的 delta 也不能相加，因为它们不是同一 factorial design。

## 5. Related Work 对比

| 类别 | 机制 | 优点 | 局限 | 与 DLMR 的关系 |
|---|---|---|---|---|
| CoT/CCoT prompting | 通过文本提示产生显式推理 | 无结构改造 | 上下文继续增长，视觉 revisit 不受结构保证 | DLMR 增加 latent memory 接口 |
| SFT/GRPO/Visual-RFT | 调整模型输出策略 | 可显著提高任务准确率 | 不显式分离视觉/推理 memory | DLMR 与相同范式组合；公平性依赖训练预算 |
| RCTS-RAG | 检索外部/历史内容回填 | 可访问显式证据 | 检索与上下文化开销，证据粒度不同 | DLMR 使用参数化共享 latent 而非外部库 |
| 单一 latent memory | 一个共享 latent buffer | 简单、参数少 | 不同语义可能互相干扰 | 直接 ablation 的替代对象 |
| fixed-budget injection | 每次固定注入 \(k\) | 预测性强、实现简单 | 不能按状态分配成本 | Table 4 的 router baseline |

没有本地 PDF bibliography，无法审计论文是否遗漏更近的 latent-memory/router 工作；Related Work 仅限索引主文已出现的比较组。

## 6. OpenReview 公开评审 × 论文内容交叉核验

- OpenReview：`https://openreview.net/forum?id=SFWWUr9V7c`
- 访问日期：2026-07-24
- decision：Spotlight 已由 forum search metadata 与 ICML official page 双源确认。
- meta-review/reviews/rebuttal/discussion：Cloudflare/API 403，正文和 note IDs 未取得。

| 来源 | claim/问题 | 关联证据 | 状态 | 本报告判断 |
|---|---|---|---|---|
| venue metadata | 接收为 ICML 2026 Spotlight | ICML poster 63955; forum metadata | resolved at tier level | 可引用接收层级，不可推断评审理由 |
| forum revision metadata | 2026-06-24 有修改 | forum search metadata；原投稿为 anonymous preliminary | unclear | 无 final PDF，不能判断是否实质修改 |
| OpenReview code field | 代码可在 GitHub 获得 | URL 当前 404；clone/API 均失败 | unresolved/contradicted by access | 不作为 reproducibility 正向证据 |

由于未取得任何 reviewer body，本报告不虚构“reviewer concerns”。当前主要担忧来自我们对 paper/search-index evidence 的独立检查：数据泄漏控制、训练预算公平性、组件 loss 消融、参数量、runtime 与 token/latency 区分、final revision 差异。

## 7. Infra 需求分析

### 7.1 算力

论文报告事实：7B/8B frozen backbone；injector 是 LoRA 化副本；router 重用 ongoing decoding 的 hidden state。  
推导：每次 injector 仍需处理长度约 \(L_t+k\) 的序列，若副本运行完整层栈，其成本可能远大于 router head；无代码不能判断是否缓存、裁剪层数或复用 KV。

### 7.2 显存与 cache

一次注入新增 embedding payload 约为

$$
\mathrm{Bytes}_{\rm embed}=kdb.
$$

若注入 token 被保存到每层 KV cache，额外 KV 量近似

$$
\mathrm{Bytes}_{\rm KV/injection}
\approx 2Lkn_{\rm kv}d_hb.
$$

每样本最坏注入 token 数受 \(N_{\max}k_{\max}\) 限制。所有维度与 \(b\) 的实际值未知，不能给出可信 GB 数。

### 7.3 Data Types

| 对象 | 格式 | 阶段 | 硬件依赖 | 影响 | 证据 |
|---|---|---|---|---|---|
| backbone/injector weights | 未报告/未核验 | train/infer | GPU/NPU 未知 | 无法估算显存与 tensor-core 路径 | no PDF appendix/code |
| latent banks | 未报告/未核验 | train/infer | 未知 | \(M_sd b\) bytes per bank | analysis derivation |
| injected KV | 未报告/未核验 | infer | decoder cache layout | 随 \(L,k,N_{\max}\) 增长 | analysis derivation |
| router logits/actions | 未报告/未核验 | infer | 小 head | 相对 backbone 可能较小 | indexed architecture only |

bf16/fp16/fp8/int8/int4、量化/反量化、accumulation precision、packing/layout transform 均无证据，不能推断。

### 7.4 带宽、互联与利用率

$$
\mathrm{EffectiveBandwidth}=\frac{\mathrm{BytesMoved}}{\mathrm{RuntimeSeconds}},\qquad
\mathrm{Utilization}=\frac{\mathrm{EffectiveBandwidth}}{\mathrm{PeakBandwidth}}.
$$

缺少 bytes/runtime/hardware，无法计算。潜在流量包括：latent bank 读取、injector 前向、memory token 写入 backbone KV、追加上下文后的 attention 读取。论文恢复证据只报告 token length，不报告 HBM、PCIe/NVLink、all-reduce 或 kernel fusion。

### 7.5 CPU/GPU/NPU 异构执行

| 阶段 | CPU | GPU/NPU | 数据移动/同步 | 证据 |
|---|---|---|---|---|
| preprocess | 未知 | 图像 encoder likely accelerator，但未核验 | 未知 | no code/config |
| decode eligibility | delimiter matching 可能在 host 或 device | 未知 | 若 host 判定可能引入同步 | analysis inference only |
| router/injector | 未知 | MLLM/LoRA 通常在 accelerator | hidden state → action → injector 可能产生 pipeline bubble | indexed method + inference |
| serving | 未报告 | 未报告 | batching、CUDA graph、KV allocator、fallback 均未知 | no runtime artifact |

### 7.6 Token efficiency 不等于系统效率

Table 4 仅给生成 token 数。DLMR 还引入 injector forward、路由动作和额外 memory tokens/KV；即使生成文本短，wall-clock 也可能更慢。没有 matched latency/throughput/energy，不能把 token reduction 归因成 serving speedup。

## 8. 开源代码对照

- 声称仓库：`https://github.com/Hunter-Wrynn/DLMR`
- 检查日期：2026-07-24
- 结果：clone 不可读，GitHub REST API 404，网页 fetch 404。
- commit：unavailable。

| 论文机制 | 本地路径/commit | 判断 |
|---|---|---|
| visual/reasoning banks | unavailable | 未核验 |
| injector LoRA replica | unavailable | 未核验 |
| delimiter eligibility / \(N_{\max}\) | unavailable | 未核验 |
| router action/budget | unavailable | 未核验 |
| Stage 1–3 losses | unavailable | 未核验 |
| evaluation/token counting | unavailable | 未核验 |

因此无法回答 task packet 的“trace implementations to concrete code paths and pinned commit”。OpenReview 的 code-available 字段当前是 stale/unfulfilled claim。

### 8.1 权重/Checkpoint

未发现可读取 checkpoint 或 model metadata。容量差异、LoRA rank、架构 flags 和 paper-specific configs 全部标为未验证。

## 9. 优点与局限

### 优点

- 问题—机制对应清晰：把视觉 recall 与约束保持分开建模。
- 三个关键组件至少各有一个替换/冻结类消融。
- Table 4 没有简单声称“更多注入总是更好”，而是呈现非单调 accuracy–token 关系。
- frozen backbone + small action space 具有工程吸引力。

### 局限

- **交付级硬阻塞**：无本地可读 PDF、无最终修订比对、无公开 review body、无代码/commit。
- 双 bank 的语义专化缺少可核验 visual/representation probe；性能 ablation 只证明分离有用。
- eligibility delimiter、\(N_{\max}\)、Stage 1 loss terms、mixed-budget curriculum、efficiency reward 均无独立 ablation。
- token efficiency 未与 wall-clock、吞吐、显存、功耗分离。
- 数据来自 benchmark training splits + OpenMMReasoner；无 final appendix/code，泄漏与数据重叠无法审计。
- 搜索索引可能丢失表号、公式排版、脚注与修订内容，所有数值需最终 PDF 二次核验。

### 可改进之处

1. 公开 immutable PDF、source、repo commit 和环境 lockfile。
2. 做 \(2\times2\times2\) 或 sequential matched ablation，避免把 memory/injector/router delta 相加。
3. 对 delimiter vs learned trigger、不同 \(N_{\max}\)、各 loss term 和 reward gate 做 sensitivity。
4. 报告 memory-role probe、route confusion matrix、per-step budget、正确/错误样本路由差异。
5. 报告 prefill/decode latency、tokens/s、peak memory、KV bytes、energy，并使用相同 serving engine/batch。

## 10. 显式证据闭环

| Claim | Mechanism | Measurement | Limitation reached |
|---|---|---|---|
| 双 bank 改善 reasoning | 分离视觉/推理 latent，降低干扰 | shared 47.53 → dual 53.84 | 不能证明语义纯度；final PDF/seed 未核验 |
| trainable injector 有效 | 将共享 latent 按当前 prefix 上下文化 | frozen 50.44 → trainable 53.84 | 未隔离“LoRA replica”相对其他 injector 设计 |
| adaptive router 改善 accuracy–token frontier | 按状态选预算 | vs fixed \(k=8\): +1.13 acc, -55 tokens | 不是 wall-clock 证据；eligibility/reward 未消融 |
| DLMR 在两个 backbone 提升 | frozen backbone + memory stack | Table 1 general/reasoning averages | 训练预算、数据重叠、最终版本和代码不可核验 |

证据链能到达“组件在索引报告的实验中有改进”，但在可复现性、最终版本、语义因果和系统收益处停止；因此 completion 必须 blocked。

## 11. 研究启发与待验证清单

- 将“可路由的 memory type”与“可路由的 budget”联合建模，是比单一 retrieval score 更有解释力的接口。
- eligibility gate 把难问题拆成规则触发 + policy 选择，但也可能漏掉非 delimiter 的关键状态。
- correctness-gated efficiency reward 是一种简单的 lexicographic bias，可扩展为 constrained RL/Pareto frontier。

待验证：

1. 最终 accepted PDF 相比 anonymous original submission 改了哪些方法、表格、代码链接？
2. \(Z^{(v)}\) 与 \(Z^{(r)}\) 是否在 representation probe 上真正专化，还是只形成两个容量池？
3. injector 是否每次运行完整 MLLM 副本？是否复用 context KV？
4. delimiter patterns \(\mathcal D\)、\(N_{\max}\)、LoRA rank、\(M_s\)、\(d_w\) 和所有 loss/reward 权重是多少？
5. Table 1 baseline 是否同数据、同 step、同 compute、同 reward 与同 prompt？
6. token reduction 是否抵消 injector/router 开销并产生真实 latency/throughput 改善？
7. OpenReview concerns、rebuttal 和 decision rationale 是否指出数据泄漏、novelty 或系统成本问题？
8. 公开代码何时恢复，能否固定 commit 并复现 table/token-count pipeline？

## 12. 一句话总结

DLMR 的“共享双 latent bank + 上下文化 injector + 离散类型/预算 router”设计有三类索引消融支撑，尤其 adaptive routing 展现了优于测试 fixed budgets 的 accuracy–token frontier；但由于最终 PDF、评审、代码与运行时证据均不可取得，本轮只能形成显著增强的 **blocked** 分析，不能作为已完成、可复现的单篇深审。
