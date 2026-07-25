# Dual-Latent Memory Routing for Vision-Language Reasoning 受限证据审计

> [!info] 文档关系
> - 文档类型：Paper（原投稿索引证据已恢复；final PDF/源码/评审仍受阻）
> - 领域入口：[README](../README.md)
> - 上位汇总：[ICML 2026 selected papers](../surveys/icml-2026-selected-papers.md)
> - 证据资产：无（本次无合格图表资产）
> - 相关文档：[Paper index](../evidence/paper-index.md)

> 资料状态：ICML 2026 官方页面与 OpenReview `SFWWUr9V7c` 已确认身份、作者、摘要和 Spotlight 状态；搜索索引还恢复了 anonymous original submission 的 Sections 4.1–4.3、核心公式与 Tables 1–4 文本。2026-07-25 再次尝试 attachment、`/pdf?id=`、API2 attachment 与文本代理，仍遭 403/challenge，声称的 GitHub 仓库也保持 404。因此本文可审计原投稿的方法与表格转录，但不能声称核验了 accepted final PDF、图像、代码或公开评审。

## 修订信息

- 当前文档版本：`1.2.0`
- 当前修订 ID：`rev-dlmr-indexed-body-promotion-20260725`
- 当前修订时间：`2026-07-25T23:55:00+08:00`
- 替代版本：`rev-dlmr-problem-solution-20260725` / `1.1.0`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rev-initial-20260716` | `1.0.0` | `2026-07-16T19:16:43+08:00` | `review_dual_latent` | `initial` | 无 | 无 | 建立官方摘要级 blocked 交付 | 精确 PDF 在受控恢复后仍不可得 | 本文证据边界各节 | ICML poster 63955 | material：不能验证论文技术与实验结论 |
| `rev-source-recovery-20260724` | `1.0.1` | `2026-07-24T22:45:00+08:00` | `/root` | `evidence-update` | `rev-initial-20260716` / `1.0.0` | 无 | 定位精确 OpenReview 身份并重试 PDF/API/代码 | 刷新上次缺失源文件 | 来源与阻塞边界 | OpenReview `SFWWUr9V7c`；ICML poster `63955`；GitHub API | minor：身份/venue 更强，技术结论仍 blocked |
| `rev-dlmr-problem-solution-20260725` | `1.1.0` | `2026-07-25T10:05:32+08:00` | `/root` | `content-update` | `rev-source-recovery-20260724` / `1.0.1` / `7706f839b1418a54fe51e366f454636e630d3f58c853ff2530ea18ccbbc7a16b` | 无 | 新增摘要级论文动机与问题—方案闭环，并显式保留不可验证边界 | 统一回写既有 Paper 报告 | `研究动机与问题—方案闭环` | ICML 官方摘要与既有 blocked 证据 | minor：技术结论仍 blocked |
| `rev-dlmr-indexed-body-promotion-20260725` | `1.2.0` | `2026-07-25T23:55:00+08:00` | `/root` | `evidence-promotion` | `rev-dlmr-problem-solution-20260725` / `1.1.0` | 无 | 将已冻结但未提升的原投稿索引方法、公式、Tables 1–4 与收益归因同步到 canonical Paper，并记录新一轮官方端点恢复失败 | 修复 canonical Paper 与现有过程证据不一致 | 术语符号、方法、公式、关键结果、claim matrix、Infra 与状态声明 | OpenReview original-submission 搜索索引；ICML poster `63955`；2026-07-25 恢复日志 | material：从摘要级升级为原投稿文本级；final/视觉/代码仍受限 |

## 0. 资料与配图索引

- 官方论文页：<https://icml.cc/virtual/2026/poster/63955>
- 官方页面：[ICML 2026 poster 63955](https://icml.cc/virtual/2026/poster/63955)。
- OpenReview：[forum `SFWWUr9V7c`](https://openreview.net/forum?id=SFWWUr9V7c)；搜索索引与 ICML 页面身份一致。
- 原投稿正文：OpenReview attachment 的搜索索引已恢复 Sections 4.1–4.3、公式与 Tables 1–4 文本；这是索引转录，不等于本地 PDF 或 accepted final。
- PDF：直接 attachment、`/pdf?id=`、API2 attachment 与文本代理在 2026-07-25 重试仍返回 challenge/403，未取得可验证文件。
- LaTeX/source：不可得。
- 开源代码：声称的 `https://github.com/Hunter-Wrynn/DLMR` 在 2026-07-24 返回 404/API Not Found，不能作为实现证据。
- 图表：0；`visual-evidence-skip`。未取得可验证 final PDF，未创建空白占位资产或生成图替代论文证据。
- AI 生成分析示意图：跳过。父契约确认已安装 CLI 只有 `generate`/`edit`，不具备技能强制要求的 required document-input path 文档输入路径。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| DLMR | 在冻结 MLLM 上增加双 latent bank、injector 与动态 router | Dual-Latent Memory Routing | 不等于 ICML 2026 的另一篇 *Dual Latent Memory for Visual Multi-agent System* | 原投稿索引 Abstract/§4 |
| visual latent memory | 输入无关、跨样本共享的可学习 bank $Z^{(v)}$，经 injector 上下文化为视觉证据 token | visual memory | 不是每样本图像 KV cache；名称本身不能证明语义纯度 | 原投稿索引 §4.1 |
| reasoning latent memory | 输入无关的可学习 bank $Z^{(r)}$，目标是保存中间结论与约束 | reasoning memory | 不是显式 scratchpad 文本 | 原投稿索引 §4.1 |
| memory injector | 将当前上下文与选定 bank 的前 $k$ 个 latent 映射为 step-specific memory tokens 的 LoRA 化副本 | $g_\phi$ | 不负责选择 memory 类型/预算 | 原投稿索引 Eq. 5–7 |
| eligible step | prefix 命中 delimiter pattern 且未超过 $N_{\max}$ 时允许路由的 decoding step | routed insertion point | router 并非在每个 token 都决定是否注入 | 原投稿索引 §4.2 |
| routing action | 在 eligible step 选择 memory 类型与注入预算的离散动作 $(s_t,k_t)$ | route | 训练 sampling、推理 greedy | 原投稿索引 Eq. 8–9 |
| three-stage training | latent bank 预热；injector+memory 训练；router GRPO | 三阶段训练 | backbone 始终冻结，三阶段并非同时端到端更新 | 原投稿索引 §4.3 |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/取值 | 来源 | 边界 |
|---|---|---|---|---|---|
| $Z^{(s)}$ | 第 $s$ 类共享 latent bank | author-defined | $\mathbb R^{M_s\times d}$，$s\in\{v,r\}$ | 原投稿索引 Eq. 4 | $M_s,d$ 数值未恢复 |
| $E_t$ | step $t$ 的 image+text-prefix embeddings | author-defined | $\mathbb R^{L_t\times d}$ | Eq. 5 | 不是 KV cache |
| $g_\phi$ | memory injector | author-defined | Stage 2/推理 | Eq. 5–7 | 具体 LoRA rank 未核验 |
| $M_t$ | 当次生成的 memory tokens | author-defined | $\mathbb R^{k\times d}$ | Eq. 5/7/9 | 不等于 bank size $M_s$ |
| $a_t=(s_t,k_t)$ | eligible step 的路由动作 | author-defined | $s_t\in\{v,r\}$，$k_t\in\mathcal K_+$ | Eq. 8–9 | “when” 先受 delimiter gate 限制 |
| $\pi_\psi$ | router policy | author-defined | 训练 sampling、推理 greedy | Eq. 8–9/12 | policy 结构仅有索引文字 |
| $R_{\rm task},R_{\rm eff}$ | 正确性与效率 reward | author-defined | Stage 3 | Eq. 12 | $R_{\rm eff}$ 仅对正确答案计入；精确式未恢复 |
| $\lambda_{\rm eff},\beta$ | efficiency reward 与 KL 权重 | author-defined | scalar | Eq. 12 | 无 sensitivity |

## 1. 论文基本信息

- 标题：**Dual-Latent Memory Routing for Vision-Language Reasoning**
- 作者：Hao-Xuan Ma、Jin-Fei Qi、YiCheng Xiao、Han-Jia Ye。
- Venue：ICML 2026；官方站将其列入 Spotlight Posters 搜索结果，poster ID 为 `63955`。
- 官方页面发布时间字段：2026-05-05；页面修改时间字段：2026-06-19。
- 研究领域：多模态大语言模型、视觉语言推理、长程推理记忆。
- 摘要声称的问题：生成变长时，单一增长上下文会丢失早期视觉证据和中间约束。
- 证据边界：搜索索引可审计 anonymous original submission 的方法段、公式结构与 Tables 1–4；accepted final PDF、appendix 图像、代码、公开评审和版本差异仍不可得。

## 1.1 研究动机与问题—方案闭环

### 1.1.1 出发点与背景痛点

作者把出发点放在长程视觉语言推理：随着生成序列增长，模型既要持续引用早期图像证据，又要保留已经形成的中间结论与约束；把这两类信息都留在单一增长上下文中，会出现遗忘和冗余解码。该痛点发生在长回答的推理阶段，而不是视觉编码精度或基础模型预训练阶段。原投稿索引支持这一问题设定和后续双 bank 设计，但没有恢复失败频率、attention 诊断或 accepted-final 版本。

### 1.1.2 现有方案为何不够

原投稿把失败模式归纳为早期视觉 grounding 和中间 reasoning state 随上下文增长而丢失。作者隐含的根因是两类信息的生命周期与调用需求不同，却共享同一上下文表示和复用方式。索引还显示作者将方法与 CoT/CCoT、SFT/GRPO/Visual-RFT、RCTS-RAG、单一 latent memory 和固定预算注入比较；但 bibliography 与完整 related-work 论证不可得，不能据此判定覆盖完整。

### 1.1.3 计划解决的问题与成功标准

- 核心问题：如何在冻结 base MLLM 的条件下，分别保存并按需复用视觉证据与推理状态。
- 约束：新增可训练参数应较少，长生成不能靠无界扩大上下文解决。
- 可量化成功标准：一般与推理 benchmark 相对相同 post-training 范式提升；dual bank、trainable injector 和 adaptive budget 在对应替换消融中优于对照；在准确率不降的前提下降低注入/生成 token。
- 证据边界：索引恢复了表格均值和部分 token 数，但没有方差、完整训练预算、硬件或 accepted-final 表格，因此只能做原投稿文本级验收。

### 1.1.4 核心方案如何解决并优化问题

| 原始问题/失败模式 | 根因或约束 | 对应设计 | 改变的变量/系统行为 | 作用机制 | 预期优化 | 证据与判断 |
|---|---|---|---|---|---|---|
| 早期视觉证据与中间约束混存 | 两类信息的生命周期与调用需求不同 | 双 latent bank $Z^{(v)},Z^{(r)}$ | 将共享容量拆成两个参数子空间 | injector 按当前 prefix 将静态 latent 上下文化 | 减少跨类型干扰 | shared 47.53 → dual 53.84；MathVision 26.68 → 35.32，direct replacement；语义纯度仍 indirect |
| 静态 latent 与当前问题不对齐 | bank 输入无关 | trainable injector $g_\phi$ | 生成 step-specific $M_t$ | latent 与 $E_t$ 联合上下文化 | 提高可用性 | frozen 50.44 → trainable 53.84，direct ablation |
| 不同推理状态需要不同容量 | 固定 $k$ 可能浪费或不足 | eligibility gate + router $a_t=(s_t,k_t)$ | 只在结构边界选择类型和预算 | 对 eligible subset 做离散路由 | accuracy–token frontier | adaptive 53.84/677 tokens；优于固定 $k=8$ 的 52.71/732，replacement evidence |
| 不希望重训基础模型 | 参数和训练预算约束 | frozen base + three-stage training | 依次学习 bank、injector、router | 分离表征学习、上下文化与 cost-aware 决策 | 参数效率、训练稳定性 | 训练结构有索引公式；参数量、稳定性和等容量公平性 unverified |

### 1.1.5 完整因果链与证据闭环

当前链条是：长程视觉语言生成需要持续调用视觉证据和中间约束 → 单一增长上下文出现遗忘与冗余复用 → 双 bank 提供分离容量 → injector 将共享 latent 变成当前 step 的 memory token → eligibility gate 限制决策位置，router 选择类型与预算 → 三阶段训练依次学习分离、上下文化和 cost-aware routing。Tables 2–4 对 dual bank、injector 和 adaptive budget 给出替换证据，因此“组件有用”已形成局部闭环；bank 的视觉/推理语义纯度、delimiter 选择、各 loss 项和 wall-clock 收益仍没有直接证据。

## 2. 原投稿索引可确认的贡献声明

以下由原投稿搜索索引支持，但不等于 accepted final 已核验：

1. 为 MLLM 引入 visual memory 与 reasoning memory 两类潜在记忆。
2. 用 router 在推理时动态选择记忆类型和复用量。
3. 冻结 base MLLM，以 bank 预热、injector/memory 训练、router GRPO 三阶段训练新增机制。
4. Tables 1–3 报告两个 backbone 上的主结果以及 dual bank、injector 替换消融。
5. Table 4 报告 adaptive route 相对固定 $k$ 的 accuracy–token 对照。

索引没有恢复完整参数清单、方差、seed、硬件、延迟或 final revision，因此性能数字是“原投稿表格转录”，不是可复现实验结论。

## 3. 研究方法：设计动机与证据边界

### 3.1 架构与推理路径

1. 学习两个输入无关的全局 bank $Z^{(v)}$ 与 $Z^{(r)}$。
2. 生成 prefix 命中 delimiter 且注入次数未超过 $N_{\max}$ 时，进入 eligible step。
3. router policy $\pi_\psi$ 根据当前 hidden state 选择 $a_t=(s_t,k_t)$；训练时 sampling，推理时 greedy。
4. injector $g_\phi$ 将当前 embeddings $E_t$ 与选定 bank 的前 $k_t$ 个 latent 联合上下文化为 $M_t$。
5. 把 $M_t$ 加入上下文，继续由冻结 backbone 解码。

因此“router 决定何时注入”需要限定：真正的候选时刻先由手工 eligibility gate 决定，router 只在 eligible subset 内选择类型和预算。

### 3.2 设计动机矩阵

| 设计项 | why 状态 | 原文证据 | 针对的具体问题 | 摘要声称的因果机制 | 替代方案/权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|---|
| dual latent banks | author-stated | Eq. 4；disentanglement ablation | 单一 buffer 的类型干扰 | 两个参数子空间提供专化容量 | 单 bank 更简单；显式 scratchpad 更可解释但更长 | shared 47.53 vs dual 53.84 | supported for separation；语义纯度 indirect |
| LoRA replica injector | partly author-stated | Eq. 5–7；Table 2 | 静态 latent 不适配当前 prefix | 生成 context-specific $M_t$ | cross-attention 更轻；完整副本可能更贵 | frozen 50.44 vs trainable 53.84 | injector need supported；replica choice unisolated |
| delimiter eligibility + $N_{\max}$ | author-stated | §4.2 | 每 token 路由开销与无界注入 | 限制动作位置和最坏注入次数 | learned trigger 更灵活；固定规则可漏掉有效时刻 | 无 trigger/sensitivity ablation | plausible, unverified |
| discrete type+budget router | author-stated | Eq. 8–9；Table 4 | 固定容量不适应状态变化 | 选择 $(s_t,k_t)$ | continuous mixture 可微但可能总激活 | adaptive 53.84/677 vs fixed $k=8$ 52.71/732 | supported against tested fixed budgets |
| Stage 1 alignment/separation | author-stated | Eq. 10 | bank 可能 collapse | branch alignment + cross-branch separation | orthogonality/contrastive loss；过强分离可能损伤共享信息 | dual-vs-shared 间接支持，无 loss-term ablation | indirect/confounded |
| Stage 2 mixed route training | author-stated | Eq. 11 | injector 只适配单一 budget/type | 覆盖多种 route condition | curriculum 更稳但覆盖慢 | 无单项消融 | unverified |
| Stage 3 cost-aware GRPO | author-stated | Eq. 12 | 只优化准确率可能过度注入 | 正确性 reward + correctness-gated efficiency reward + KL | constrained RL；可能 reward hacking | Table 4 是整体证据，无 reward-term ablation | partially supported |
| frozen backbone | author-stated | Abstract/§4.3 | 控制训练成本和能力漂移 | 仅更新 memory-related parameters | 全参/adapter 可能更强 | 无参数清单或等容量对照 | quantitatively unverified |

### 3.3 关键公式

索引恢复的核心结构式为：

$$
Z^{(s)}\in\mathbb{R}^{M_s\times d},\qquad
M_t=g_\phi\!\left(E_t,Z^{(s)}_{1:k},k\right)\in\mathbb{R}^{k\times d}.
$$

$$
a_t=(s_t,k_t),\qquad s_t\in\{v,r\},\quad k_t\in\mathcal K_+.
$$

router 的 Stage 3 目标结构为：

$$
\max_\psi\ \mathbb E_{\tau\sim\pi_\psi}
\left[R_{\rm task}(\tau)+\lambda_{\rm eff}R_{\rm eff}(\tau)\right]
-\beta\,{\rm KL}\!\left(\pi_\psi\Vert\pi_{\rm ref}\right).
$$

Eq. 10–11 的索引抽取存在排版丢失风险，因此只采用其结构含义，不声称逐字符复原。

### 3.4 训练与部署缺口

索引报告 Qwen2.5-VL-7B 与 InternVL-3-8B，Stage 2 有 SFT/GRPO 版本，并提到选定 benchmark 与 OpenMMReasoner。样本量、数据泄漏检查、chat template、GRPO group size、LoRA rank、optimizer、epoch、seed/方差、GPU、precision 与 final revision 均未核验。

## 4. 技术声明证据矩阵与收益归因

| 技术声明 | 声称效果 | 可得实验/消融 | 对照是否受控 | 数值变化 | 证据强度 | 结论 |
|---|---|---|---|---|---|---|
| Qwen general：SFT → DLMR-SFT | general avg 提升 | indexed Table 1 | 完整方法对照，训练预算未核验 | 65.62 → 71.45（+5.83） | confounded complete-method | 原投稿表支持，复现性 unverified |
| Qwen reasoning：GRPO → DLMR-RL | reasoning avg 提升 | indexed Table 1 | 完整方法对照 | 50.29 → 56.45（+6.16） | confounded complete-method | 原投稿表支持 |
| InternVL general：SFT → DLMR-SFT | general avg 提升 | indexed Table 1 | 完整方法对照 | 73.37 → 79.25（+5.88） | confounded complete-method | 原投稿表支持 |
| InternVL reasoning：GRPO → DLMR-RL | reasoning avg 提升 | indexed Table 1 | 完整方法对照 | 54.33 → 63.08（+8.75） | confounded complete-method | 原投稿表支持 |
| dual 而非 shared bank | 减少类型干扰 | indexed Table 3 | matched replacement（按索引） | 47.53 → 53.84；MathVision 26.68 → 35.32 | direct ablation | separation supported；语义专化 indirect |
| trainable injector | context-specific latent | indexed Table 2 | frozen vs trainable | 50.44 → 53.84 | direct ablation | injector 学习必要性 supported |
| adaptive route/budget | accuracy–token frontier | indexed Table 4 | fixed $k=4,8,16$ | adaptive 53.84/677；$k=8$ 52.71/732 | replacement baseline | 对已测试 fixed budgets supported |
| Stage 1/2 loss 各项 | 分离与接口鲁棒性 | 无单项消融 | none | 未报告 | unverified | 不能隔离 |
| token efficiency → runtime | 系统加速 | 无 wall-clock/throughput | none | 未报告 | unverified | token 数不能替代 latency |

以上 delta 不能相加，因为并非同一 factorial design。完整方法主表还混合训练目标、额外参数和数据预算，不能归因给单一组件。

## 5. Related Work 对比

索引主文出现的比较组包括 CoT/CCoT prompting、SFT/GRPO/Visual-RFT、RCTS-RAG、单一 latent memory 与 fixed-budget injection。DLMR 的区别在于参数化共享 latent、双 bank 分工和状态依赖预算；外部检索更显式但有检索/上下文化开销，单 bank 与 fixed budget 更简单但缺少分工或自适应。由于 bibliography 不可得，不能审计是否遗漏更近工作。

## 6. OpenReview 公开评审 × 论文内容交叉核验

已定位精确 forum `SFWWUr9V7c`，但 OpenReview 页面/API/attachment 在本轮环境均返回 challenge 403。reviews、meta-review、decision、rebuttal 和 discussion 仍不可得，因此不能进行评审交叉核验。

## 7. Infra 需求分析

### 7.1 可确认事实

原投稿索引确认 7B/8B frozen backbone、LoRA 化 injector 副本、双 bank 和 router。每次 injector 仍可能处理约 $L_t+k$ 的序列；若运行完整层栈，成本可能显著高于 router head。无代码不能判断它是否缓存、裁剪层数或复用 KV。

一次注入的 embedding payload 约为：

$$
\mathrm{Bytes}_{\rm embed}=kdb.
$$

若注入 token 保存到每层 KV cache，额外 KV 量近似为：

$$
\mathrm{Bytes}_{\rm KV/injection}\approx 2Lkn_{\rm kv}d_hb.
$$

所有维度和实际 dtype 均未知，不能给出可信 GB 数。

### 7.2 不可验证项

- 算力：无法估算训练/推理 FLOPs。
- 显存与存储：无法估算 memory、activation 或 KV cache 字节数。
- Data types：fp32/fp16/bf16/fp8/int8 等均未报告。
- 带宽利用率：没有 bytes moved、runtime 或 peak bandwidth，不能计算有效带宽与利用率。
- 互联：PCIe/NVLink/RDMA/all-reduce/all-to-all 使用情况未知。
- CPU/GPU/NPU 异构：预处理、host-device transfer、kernel、DMA、异步 overlap 与 fallback path 均未知。
- Serving/runtime：batching、scheduler、cache layout、CUDA graph 和自定义算子均未知。

因此不能把摘要的 token-efficiency 声明等价为 latency、throughput、显存或带宽收益。

## 8. 开源代码与配置对照

官方 ICML 页没有可访问的代码快照；搜索结果所指向的 `Hunter-Wrynn/DLMR` 当前返回 404/API Not Found。没有可核验的 commit、架构、loss、data pipeline、evaluation、serving、checkpoint 或 config。任何实现级解释均应标记为未验证。

## 9. 优点、局限与可改进之处

### 摘要层面的潜在优点

- 将视觉证据与推理约束分离，目标问题明确。
- 冻结 base MLLM 的参数效率方向具有工程吸引力。
- 摘要至少声明关注 router 可解释性和 token efficiency，而非只报 accuracy。

### 当前交付的实质局限

- 没有 accepted final PDF/appendix，无法确认索引转录与最终版本是否一致。
- 没有图表，无法核对 mechanism 与主结果。
- 没有代码/config/checkpoint，无法区分论文概念与实现行为。
- 没有公开评审证据，无法判断 novelty、baseline 公平性和 rebuttal 解决情况。
- 参数量、方差、完整训练预算与 wall-clock 未恢复，不能把原投稿表格复述为可复现事实。

### 最小解除阻塞条件

取得与 poster `63955` 精确对应的 accepted final PDF（最好含 appendix），或由作者/ICML 提供正式 PDF URL；随后核对 revision 差异，执行图表裁剪与逐图 QA，并补齐公开评审、代码、参数量、方差和 runtime 证据。

## 10. 研究启发

在后续取得正文后，最值得检验的不是“双记忆”命名本身，而是三类最小对照：单 visual memory、单 reasoning memory、双 memory 但固定路由。只有与完整动态 router 的 matched ablation 才能隔离双记忆分工与路由学习的贡献。另需把 token 数减少与实际 wall-clock latency、HBM 流量和 serving throughput 分开测量。

## 11. 解读问题/待验证清单

1. $M_s,d,N_{\max}$、delimiter 集和 LoRA rank 的精确值是什么？
2. accepted final 是否修改了 Eq. 10–12、Tables 1–4 或数据配置？
3. “少量参数”具体是多少，是否与 LoRA/adapter 等容量匹配 baseline 公平比较？
4. 数据样本量、泄漏检查、prompt、GRPO 配置、seed 和方差是什么？
5. 是否有单 visual、单 reasoning、learned trigger 和 loss-term 消融？
6. 路由可解释性是否有定量指标，而非仅案例可视化？
7. token efficiency 是否转化为 latency/throughput 收益，还是被 injector/router 开销抵消？
8. reasoning memory 写入错误时，是否会造成持续错误放大？

## 12. 一句话总结

DLMR 已从摘要级 block 恢复到原投稿方法、公式和 Tables 1–4 可审计：dual bank、trainable injector 与 adaptive budget 均有局部替换证据；但 accepted final、视觉、代码、公开评审和 runtime 仍受限，不能把索引转录升级为最终版可复现结论。
