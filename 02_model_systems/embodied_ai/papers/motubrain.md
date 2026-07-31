---
tags:
  - paper
  - collection/embodied-ai
  - domain/model-systems
  - status/deep-review
  - topic/world-action-models
  - method/unified-video-action-modeling
document_type: paper
domain: embodied_ai
collection: Embodied AI
review_status: deep-review
canonical: true
---

# MotuBrain: An Advanced World Action Model for Robot Control 精读分析

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[具身智能模型演进、Infra 与端云协同](../surveys/embodied-ai-evolution-infra.md)
> - 证据资产：`../assets/papers/motubrain/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md) · [Paper index](../evidence/paper-index.md)

> 资料状态：官方 arXiv PDF 与 LaTeX source 可用；官方 GitHub 仓库可用但为 documentation-only；未发现公开 OpenReview；三张内嵌证据均为 200 DPI PDF 单对象裁剪并包含完整 caption。canonical Paper 仅作为只读迁移线索，本审阅以重新获取的官方证据为准。

## 修订信息

- 当前修订 ID：`rev-motubrain-obsidian-properties-20260731`
- 当前文档版本：`1.0.2`
- 当前修订时间：`2026-07-31T10:00:00+08:00`
- 替代版本：`rev-motubrain-affiliation-backfill-20260730` / `1.0.1`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rev-motubrain-20260725-initial` | `1.0.0` | `2026-07-25T18:20:00+08:00` | `delegated-paper-review-agent` | `initial` | `none` | `none` | 重新获取 PDF/source/repo，审计机制、实验、系统与证据边界 | non-ICML Paper 交付完整性修复 | 本文各分析章节与 [Figure inventory](../evidence/figure-inventory.md) | official PDF/source；repo commit `a845f4b…` | 建立首个满足当前规范的正式版本 |
| `rev-motubrain-affiliation-backfill-20260730` | `1.0.1` | `2026-07-30T23:30:00+08:00` | `/root` | `metadata-update` | `rev-motubrain-20260725-initial` / `1.0.0` | 无 | 补充作者—机构元数据与角色证据边界 | 统一回填 affiliation 交付字段 | `作者与机构` | 论文 PDF 标题页、机构编号与角色脚注 | none：不改变方法、实验与归因结论 |
| `rev-motubrain-obsidian-properties-20260731` | `1.0.2` | `2026-07-31T10:00:00+08:00` | `/root` | `metadata-update` | `rev-motubrain-affiliation-backfill-20260730` / `1.0.1` | 无 | 增加 Obsidian YAML Properties 与层级标签 | 全量 canonical Paper 标签补齐 | 文件头 YAML frontmatter | 已验证的 ICML 2026 标签 schema；仓库覆盖矩阵 | none：不改变论文分析与证据结论 |

## 0. 资料与配图索引

- 论文：[arXiv:2506.05118](https://arxiv.org/abs/2506.05118) 官方 PDF/source。
- 官方仓库：[Motubrain](https://github.com/Motif-Technologies/Motubrain)，核验 commit `a845f4b93f430c578398bc65b1614b79f17088cd`。
- 公开评审：未发现可核验的官方 OpenReview forum、review、meta-review、decision 或 rebuttal。
- 视觉证据：Figure 1、Table 2、Table 3；bbox/caption/QA 见 [Figure inventory](../evidence/figure-inventory.md)。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| WAM | 同一生成模型联合建模未来视频与动作 | World Action Model | 不等于串联 VGM+IDM | Introduction；Table 1 |
| UniDiffuser | 视频、动作各有独立 timestep 的联合连续生成 formulation | unified video-action formulation | 不等于共享单一噪声时刻 | Method §2.1 |
| three-stream MoT | text/video/action 各自 FFN/表示流，并在部分层联合注意力 | Mixture-of-Transformers | 不等于专家路由 MoE | Figure 1；Method §2.1 |
| H-bridge | 中间 50% 层做 video-action-text joint attention，首尾各 25% 解耦 | HBridge | 不等于 V2A 非对称 mask | Method §2.1；Figure 1 |
| relative-EEF | 以末端执行器相对变化表达跨 embodiment 动作 | shared action representation | 不是固定机器人关节绝对坐标 | Method §2.1 |
| Non-AR / AR | 全窗口联合去噪 / chunk-block-causal 顺序 rollout | post-training modes | 不是相同计算图只改采样温度 | Method §2.3；Figure 2 |
| V2A-style | action 可 attend video/text，而 video 不 attend action；采样后缀可冻结 video | asymmetric dependency/action-only suffix | action-only 不等于无视觉输入 | Method §2.3–2.4；Eq. 9 |
| DiT cache | 速度场相邻相似度过阈值时复用并跳过后续 DiT evaluation | inference cache | 不等于 KV cache；后者用于 V2A 固定上下文 | Method §2.4；Eqs. 7–8 |
| EWMScore | WorldArena 16 个归一化指标的算术均值并缩放到 $[0,100]$ | embodied world-model score | 不等于控制成功率 | Experiment §3.2；Table 5 |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/索引 | 单位/取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|
| $z_v^{(t)},z_a^{(t)}$ | denoising step $t$ 的 video/action latent | author-defined | per sampling step | latent tensor | Eq. 9 | $t$ 是采样步，不是机器人时间 |
| $N$ | joint denoising prefix 结束步 | author-defined | per request | 未报告整数 | Eq. 9 | 不是 Transformer 层数 |
| $\Phi_{\mathrm{joint}},\Phi_{\mathrm{act}}$ | joint 与 action-only 更新算子 | analysis-normalized from author equation | per step | operator | Method §2.4 | 论文没有公开实现 |
| $v_t$ | 第 $t$ 个 denoising step 的 predicted velocity | author-defined | per step | latent velocity | Eqs. 7–8 | 不等于机器人关节速度 |
| $s_t,\gamma,k$ | 相邻速度余弦相似度、阈值、复用跨度 | author-defined | cache decision | $s_t\in[-1,1]$；$\gamma,k$ 未报告 | Eqs. 7–8 | 无 sensitivity/hit-rate |
| $H,s,\delta,\Delta t,d$ | action horizon、已执行步数、推理延迟、控制周期、延迟步数 | author-defined | per chunk/request | steps, seconds | Eqs. 10–12 | $0.09$ s 未证明包含完整网络/控制边界 |
| $\rho_i,g(\rho_i),w_i,L$ | fusion 进度、衰减函数、旧 chunk 权重、融合窗终点 | author-defined | per action index | normalized/unitless; steps | Eqs. 13–15 | 无 ablation 或部署值 |
| $L_i,r_i$ | 第 $i$ 行累计 stack latency 与相邻条件增益 $L_{i-1}/L_i$ | analysis-derived | Table 2 row | seconds, ratio | 本分析 §5.4 | $r_i$ 非独立贡献 |
| $B_{\mathrm{eff}},U_B$ | 有效带宽与峰值利用率 | analysis-derived | runtime | bytes/s, ratio | 本分析 §8.4 | 缺 bytes/peak，不能数值化 |

## 1. 论文基本信息

### 作者与机构

- 署名类型：机构署名（标题下未列个人作者）。
- 署名机构：Motubrain Team。
- 第一作者、共同第一作者、通讯作者：不适用。
- 对应依据：论文 PDF 标题页、作者机构编号与角色脚注（核验日期：2026-07-30）。


- 领域：具身智能、world model、机器人控制与生成模型 serving。
- 核心问题：如何同时保留视频模型的时序动力学先验、统一 policy/world-model 功能，并把联合视频—动作去噪降到闭环控制可用延迟。
- 目标：一个模型支持 policy、world prediction、video generation、IDM 与联合生成；跨多视角/embodiment；部署达到论文环境中的 11 Hz。
- 约束：arXiv technical report；模型规模与硬件/负载细节缺失；官方 repo 无实现/配置/checkpoint。

## 2. 研究动机与问题—方案闭环

### 2.1 出发点与背景痛点

作者明确指出，主流 VLA 从静态 image-text 预训练获得强语义，但对接触、物体运动和动作后果等细粒度 dynamics 建模不足。视频生成模型拥有时序先验，然而“先生成视频、再由 IDM 反推动作”的串联方案会把视频误差传给动作，而且双阶段推理昂贵。统一 WAM 又引入另一约束：高维视频 latent 与动作 latent 多步联合去噪，naive baseline 在 Table 2 为 4.90 s，无法支持高频操控。

### 2.2 现有方案为何不够

失败不是笼统的“效果低”：静态 VLA 的训练分布弱化 dynamics；VGM+IDM 的分解形成级联误差和双阶段 latency；固定摄像机/action 坐标妨碍跨 embodiment；joint WAM 的重复 video branch、solver steps、launch 和 memory traffic 使 runtime 成为绑定约束。简单只删视频生成虽快，却可能破坏训练时联合依赖；MotuBrain 因而用 V2A 非对称依赖在训练语义与部署图之间搭桥。

### 2.3 目标问题与成功标准

核心研究问题是：能否在同一模型中对齐 world prediction 与 control，同时把 policy inference 降到实时请求频率？成功标准包括 RoboTwin success、WorldArena EWMScore、少量同 embodiment trajectory 的适配，以及 Table 2 latency/frequency。论文不解决已证明的完整 cloud-to-robot SLA、一般 open-world robustness 或 hardware-portable speedup。

### 2.4 方案如何改变关键变量

| 原始问题/失败模式 | 根因/约束 | 方案 | 改变的变量/行为 | 机制 | 预期指标 | 证据 | 判断 |
|---|---|---|---|---|---|---|---|
| 静态 VLA dynamics 弱、VGM+IDM 级联 | 表征与目标割裂 | UniDiffuser joint video-action | 共享 backbone/联合 conditional distributions | world 与 action 互为上下文 | success + world score | Tables 1,3,5 | partially-supported；完整系统证据，formulation 未独立 ablate |
| 多视角/跨机器人格式固定 | 坐标与 camera layout 不统一 | multiview 3D RoPE + relative-EEF | view offset 与动作坐标 | 减少 layout/embodiment 特定绑定 | transfer/generalization | Method §2.1；现实实验 | plausible；无独立消融 |
| 短窗与长时 rollout 冲突 | factorization 不同 | Non-AR/AR post-training | attention mask 与 chunk sequence | 高频短窗或 block-causal 长时 | RoboTwin/long-horizon | Table 3；现实实验 | partial；AR 对比含多变量 |
| joint denoising 4.90 s | steps、launch、GEMM/traffic、video suffix 重复 | 30 steps + compile + FP8 + cache + V2A | forward 次数、dtype、graph、输出工作 | 顺序累积减少冗余 | latency/frequency | Table 2 | runtime supported；独立性/质量边界不足 |
| 云推理与 action chunk 边界抖动 | 请求延迟和 chunk 不连续 | RTC-inspired fusion | 冻结 prefix、overlap weight | 旧/新 chunk 平滑交接 | boundary stability | Eqs. 10–15 | plausible；无 fusion-off trace/ablation |

### 2.5 因果链与证据闭环

作者的闭环是：静态语义先验不足以表达 dynamics，串联 world/action 又级联且慢；因此统一多模态生成目标与表示，让视频先验进入 policy，再用 AR/Non-AR 匹配任务时域，最后通过 runtime stack 删除重复采样、低效图和不必要视频后缀。Table 3/5 支持完整系统在指定 benchmark 的质量，Table 2 直接支持固定顺序 stack 的累计 4.90→0.09 s；但“每个架构组件提高 accuracy”“优化 essentially lossless”“11 Hz 等于整机控制频率”均未闭环。剩余边界是组件消融、质量—速度曲线、硬件/负载与网络/controller telemetry。

## 3. 核心贡献

1. 统一视频—动作生成并扩展为 text/video/action three-stream MoT，支持五类 conditional inference（Method §2.1；Table 1）。
2. H-bridge、multiview 3D RoPE 与 relative-EEF 面向跨模态成本、多相机布局和跨 embodiment 表示（Figure 1）。
3. Non-AR/AR post-training 与 V2A-style dependency 把统一训练模型连接到 action-only 部署图（Method §2.3–2.4）。
4. 系统栈报告 54.4× 累计加速和 11.11 Hz（Table 2）。
5. RoboTwin 95.8/96.1 与 WorldArena 63.77 展示 action/world 双侧能力，但跨论文公平性和复现证据有限（Tables 3,5）。

## 4. 研究方法

### 4.1 架构

![Figure 1: MotuBrain architecture with full caption](../assets/papers/motubrain/fig1-architecture-caption.png)

Figure 1 直接显示三个 stream、各自 FFN/QKV 以及中间 joint attention；它不显示 V2A action-only suffix 的实际删图或 runtime cache。

### 4.2 组件设计动机矩阵

| 设计项 | why 状态 | 证据 | 具体问题 | 因果机制 | 替代/权衡 | 验证 | 判断 |
|---|---|---|---|---|---|---|---|
| UniDiffuser joint objective | author-stated | §2.1/Table 1 | VGM+IDM 级联/功能割裂 | 独立 timestep 下共享表示与条件分布 | 模块化两阶段更易诊断但更慢 | full-system Tables 3/5 | plausible/partial |
| independent text stream | author-stated | §2.1/Fig.1 | language-action coupling 弱 | text hidden states 进入 attention | 外部 embedding 更便宜 | 无独立消融 | unverified |
| H-bridge | author-stated | §2.1/Fig.1 | full joint attention 成本/干扰 | 仅中间 50% joint | full joint 更强交互；解耦更便宜 | Table 3 命名行低 0.5/0.7 点且定义不充分 | efficiency plausible, accuracy unsupported |
| multiview 3D RoPE | author-stated | §2.1 | camera 数/布局变化 | view-dependent offsets | calibration-aware geometry 更显式但复杂 | 无独立消融 | plausible |
| relative-EEF | author-stated | §2.1 | embodiment action 坐标不同 | 相对末端位姿统一语义 | joint-space 可直接执行但难迁移 | 现实适配 aggregate | partial/confounded |
| AR/Non-AR masks | author-stated | §2.3/Fig.2 | 短窗效率与长时因果 rollout | full-window vs block-causal chunks | 单一模式更简单 | Table 3 AR full +3.9/+3.8 points | direct configuration, mechanism confounded |
| V2A action-only suffix | author-stated | §2.3–2.4/Eq.9 | 重复高维 video denoising | freeze video, reuse video/text KV | full joint 保留视频预测 | Table 2 0.20→0.09 s | runtime partial；质量未量化 |
| 30 steps/compile/FP8/cache | author-stated | §2.4/Table 2 | repeated forward、launch、traffic | 少 forward、fusion/graph、低精度、复用 velocity | 更激进压缩有精度风险 | cumulative ladder | conditional runtime supported |
| async fusion | author-stated | §2.4.2/Eqs.10–15 | network delay/chunk discontinuity | frozen prefix + decayed overlap | 同步等待降低频率 | 无开关消融/trace | unverified |

### 4.3 关键公式

V2A sampling 的审阅归一化表达为：

$$
(z_v^{(t+1)},z_a^{(t+1)})=
\begin{cases}
\Phi_{\mathrm{joint}}(z_v^{(t)},z_a^{(t)}), & t<N,\\
(z_v^{(N)},\Phi_{\mathrm{act}}(z_a^{(t)};z_v^{(N)})), & t\ge N.
\end{cases}
$$

Cache 判据：

$$
s_t=\frac{\langle v_t,v_{t-1}\rangle}{\lVert v_t\rVert_2\lVert v_{t-1}\rVert_2},
\qquad s_t>\gamma\Rightarrow \hat v_{t+j}\approx v_t,\;j=1,\ldots,k.
$$

异步 delay：

$$
d=\left\lceil\frac{\delta}{\Delta t}\right\rceil.
$$

$N,\gamma,k,H,\Delta t$ 的部署值未报告，故无法推出 FLOPs、cache hit rate 或真实 overlap。

### 4.4 数据与训练边界

RoboTwin 采用 clean 2,500 demonstrations（50/task）与 randomized 25,000（500/task），视频 5 Hz、动作 10 Hz。预训练数据组成与两阶段策略由 source 描述，但模型规模、完整 budget、optimizer/硬件和可执行配置未公开。现实适配报告 50–100 条同 embodiment trajectory；这些是作者设置，不等同于公开可复现数据。

## 5. 关键结果与证据

### 5.1 RoboTwin

![Table 3: RoboTwin 2.0 results with full caption](../assets/papers/motubrain/table3-robotwin-results-caption.png)

完整 MotuBrain 报告 95.8 clean / 96.1 randomized。AR full 相对 Non-AR full 为 +3.9/+3.8 个百分点；AR full 相对 w/o pretrain 为 +4.3/+4.8；Non-AR full 相对 Non-AR w/o pretrain 为 +2.3/+2.8。HBridge 命名行反而比相邻 Non-AR w/o pretrain 低 0.5/0.7，且论文未证明这两行唯一变量，不能宣称 H-bridge 提升 accuracy。

### 5.2 Runtime ladder

![Table 2: cumulative inference speedup with full caption](../assets/papers/motubrain/table2-inference-speed-caption.png)

Table 2 每行包含前序优化；相邻条件增益不是独立贡献：

| 新增项 | latency | cumulative | 本分析条件比 |
|---|---:|---:|---:|
| baseline 50 steps | 4.90 s | 1.00× | — |
| 30-step noise sampling | 2.90 s | 1.69× | $4.90/2.90=1.690$ |
| `torch.compile` | 0.98 s | 5.00× | $2.90/0.98=2.959$ |
| FP8 | 0.88 s | 5.57× | $0.98/0.88=1.114$ |
| DiT cache | 0.20 s | 24.5× | $0.88/0.20=4.400$ |
| V2A action-only | 0.09 s | 54.4× | $0.20/0.09=2.222$ |

乘积约 54.44，仅是 telescoping ratio。无 factorial/remove-one、顺序交换、重复次数或方差。

### 5.3 技术 claim 证据矩阵

| claim | 证据 | 分类 | 结论 |
|---|---|---|---|
| unified WAM 同时改善 policy/world modeling | Tables 3,5 跨论文 comparison | indirect/confounded | 完整系统强，formulation 贡献未隔离 |
| pretraining 改善 RoboTwin | Table 3 matched naming rows | direct replacement | 支持总体 pretraining，不隔离数据阶段 |
| AR 改善 policy | Table 3 AR vs Non-AR | direct multi-change | 支持配置，mask/factorization/window 混杂 |
| H-bridge 平衡质量/效率 | Fig.1 + ambiguous Table 3 row | mechanism/unsupported gain | efficiency 动机合理；accuracy 正收益不成立 |
| 30 steps lossless | Table 2 latency + prose | runtime direct, quality missing | speed 支持；sub-percent 未量化 |
| compile/FP8/cache/V2A 加速 | Table 2 cumulative rows | direct conditional runtime | 仅固定 stack/未披露环境成立 |
| RTC fusion 稳定波动 | Eqs.10–15 + aggregate demos | plausible/no direct control | 需 fusion-off 和 jitter trace |
| WorldArena leader | Table 5, EWMScore 63.77 | direct reported table | 对所列 entries 成立；README 64.87 冲突 |

### 5.4 收益归因

30 steps 减少 nominal DiT evaluations 40%；compile 主要减少 dispatch/launch 和中间 materialization；FP8 降 eligible linear traffic/GEMM 时间；cache 通过跳过 forward 降 realized FLOPs；V2A 则减少 suffix video branch 与未来视频输出工作。后四者有顺序交互，不能把累计 ratio 当可乘的独立模块效应。0.09 s 更安全地解释为论文 Non-AR model inference request latency，而不是包含 VAE、网络、queue、controller dispatch 的机器人闭环 SLA。

### 5.5 WorldArena 与现实任务

Table 5 报 EWMScore 63.77，相对第二高 ABot-PW 62.63 为 +1.14，相对 Wan2.6 59.80 为 +3.97。跨模型训练数据、参数量和预算不透明。现实任务报告 33/124/138 s 的长时执行及 50–100 trajectory adaptation，但缺 matched baseline、置信区间和 failure telemetry，因此只支持窄场景作者报告。

## 6. Related Work

| 类别 | 机制 | 优点 | 局限 | 与本文关系 |
|---|---|---|---|---|
| VLA | image/language→action | 语义先验与成熟 policy 路径 | dynamics 弱 | MotuBrain 注入视频时序先验 |
| VGM+IDM | video rollout 后反推动作 | 复用视频模型 | 级联误差/两阶段成本 | MotuBrain 联合建模 |
| Motus/prior WAM | joint video-action | world/policy 对齐 | joint denoising 贵 | MotuBrain 扩展表示和 serving |
| Fast WAM/RTC-style | cache、chunk、融合 | 面向 realtime | 对阈值/硬件/telemetry 敏感 | MotuBrain 组合为累计 stack |

比较公平性限制：Tables 3/5 可核对作者报告的相对位置，不能把跨论文差值全归因于 MotuBrain formulation。

## 7. OpenReview 交叉核验

未发现公开 OpenReview forum、review、meta-review、decision 或 rebuttal；详见 公开评审核验记录。因此本分析不引用 reviewer 意见。复现性、消融和 deployment concerns 是基于 paper/source/repo 的审阅判断。

## 8. Infra 需求分析

### 8.1 算力与显存

方向上，step reduction/cache 降 DiT forward 次数，V2A 降 suffix video branch，compile/FP8 改善每次 forward。模型参数量、token shapes、$H/N$、cache hit rate 未给，不能数值估 FLOPs。显存至少包括 weights、video/action activations、固定 video/text per-layer KV 与 action state；缺 shape/dtype coverage，不能给可信 GB。

### 8.2 数据类型

| 对象 | 格式 | 阶段 | 硬件依赖 | 影响 | 证据 |
|---|---|---|---|---|---|
| eligible linear weights | `float8_e4m3fn`, per-tensor scale | inference | FP8 GPU；dim multiple of 16 | weight traffic/GEMM time 降 | §2.4.1；无 code |
| eligible activations | dynamic FP8 | inference | `torch._scaled_mm` | traffic/compute 降，有 quant overhead | §2.4.1 |
| fallback/output | original dtype 未命名 | inference | unspecified | precision fallback | paper prose only |

### 8.3 带宽与互联

$$
B_{\mathrm{eff}}=\frac{\mathrm{BytesMoved}}{\mathrm{RuntimeSeconds}},
\qquad U_B=\frac{B_{\mathrm{eff}}}{B_{\mathrm{peak}}}.
$$

论文未给 BytesMoved、GPU SKU/peak bandwidth 或 profiler，故不能报告 GB/s/%。FP8/cache/V2A 应减少 traffic，compile 可能通过 fusion 减少中间 tensor；这些是机制推断。论文只声称 single GPU，没有 all-reduce/all-to-all；PCIe/NVLink/RDMA 也未报告。

### 8.4 CPU/GPU/NPU 异构

| 阶段 | CPU/robot | GPU | 移动/同步 | 边界 |
|---|---|---|---|---|
| observation/request | 图像与请求 | 等待输入 | robot/network→cloud | encode/RTT/queue 未量化 |
| inference | Python/runtime orchestration | compiled DiT/FP8/cache/V2A | host dispatch + kernels | CPU overhead是否计入不清 |
| execution | controller 执行 current chunk | 异步 next chunk | cloud→robot actions | control Hz/jitter 未给 |
| fusion | delay queue/frozen prefix | 可参与 denoise | old/new chunk overlap | 无 trace/ablation |

NPU、DMA/pinned memory、async copy 与 fallback 均未报告。

### 8.5 Serving/自定义算子

论文提 `torch.compile`、CUDA-graph-friendly execution、`torch._scaled_mm`、DiT cache、V2A KV reuse 和异步 chunk queue；repo 无 serving path，无法验证 warmup、graph breaks、cache invalidation、batching、scheduler 或失败回退。

## 9. 开源代码与 checkpoint

- repo：[Motubrain](https://github.com/Motif-Technologies/Motubrain)；核验 commit `a845f4b93f430c578398bc65b1614b79f17088cd`。
- `README.md`、PDF、license、logos、scaling images 之外无代码。

| 论文机制 | 本地证据 | 一致性 |
|---|---|---|
| architecture/runtime/data pipeline | 无 `.py`/config/environment | 未开源，paper-only |
| benchmark tables | `official repository: README.md` | 大体一致；WorldArena prose 64.87 与 paper/table 63.77 冲突 |
| checkpoint/weights | 无链接/metadata/config | unavailable；参数/架构 flags 不推断 |

## 10. 优点、局限与改进

优点：Table 2 给出清晰累计 latency ladder；V2A 依赖方向足以判断删掉与保留的计算；Table 3 同时暴露 pretraining、AR/Non-AR 与 HBridge 命名变体，允许谨慎归因。

局限：硬件 SKU、batch/horizon/views/resolution、timing protocol 与 full-loop boundary 缺失；speed stack 非 factorial；“lossless”无数值表；H-bridge/text/multiview/relative-EEF/fusion 缺独立消融；repo documentation-only；现实实验窄且无 matched control；无公开 peer review。

最小改进：固定硬件与 shape 报 warm/cold median/P95；五项优化做 remove-one/顺序交换；公开 $\gamma,k,N$ sweep、cache hit rate 与 quality-speed curve；发布最小 inference config/checkpoint/profiler；RTC 做 fusion-off jitter/task ablation。

## 11. 研究启发

- WAM serving 可按“少 solver step、少 branch/output、少 bytes、少 launch”拆分，比单一 50× 口号更可迁移。
- action-only 的实质不是丢弃视觉，而是把动态视频生成变成固定视觉上下文 KV reuse。
- 云端 chunk policy 应将 P95 delay、boundary jerk、task success 与 model latency 联合评估。

## 12. 待验证清单

1. Table 2 的 GPU SKU、batch、views/resolution、$H,N,\gamma,k$ 是什么？
2. 0.09 s 是否包含 VAE、CPU preprocessing、网络、fusion 与 controller dispatch？
3. compile 行是否混入 pure-PyTorch rewrite/CUDA graph？
4. 每项优化的独立质量差、计时方差和顺序交互是什么？
5. HBridge 表行唯一变量为何，为什么分数较低？
6. WorldArena 63.77 与 README prose 64.87 的版本来源是什么？
7. 何时发布实现、配置、checkpoint 与 profiler？

## 13. 一句话总结

MotuBrain 把统一视频—动作 WAM 与部署栈结合，在论文未披露的单 GPU 环境将 Non-AR inference 从 4.90 s 累计降到 0.09 s；核心不确定性是组件独立贡献、质量无损、完整闭环边界和可复现实现均尚未被公开证据闭环。
