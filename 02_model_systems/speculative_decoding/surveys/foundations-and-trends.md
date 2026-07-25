# 投机解码的基础合同与机制分类

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[README](../README.md)
> - 上位汇总：[Evolution](evolution.md)
> - 证据资产：无
> - 相关文档：[P-EAGLE](../papers/p-eagle.md)，[DFlash](../papers/dflash.md)，[D2SD](../papers/d2sd.md)，[JetSpec](../papers/jetspec.md)，[HyperDFlash](../papers/hyperdflash.md)，[DSpark](../papers/dspark.md)

## 修订信息

- 当前文档版本：`1.1.0`
- 当前修订 ID：`rev-spec-foundations-delivery-remediation-20260725`
- 当前修订时间：`2026-07-25T23:30:00+08:00`
- 替代版本：初始 foundations/trends 交付

| 修订 ID | 文档版本 | 时间 | 类型 | 变更摘要 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|
| `rev-spec-foundations-delivery-remediation-20260725` | `1.1.0` | `2026-07-25T23:30:00+08:00` | evidence-and-link remediation | 明确 correctness contract、accepted-length/成本模型、六篇 canonical Paper 证据入口与 lossy 边界 | canonical Paper reviews 与发布器校验 | minor；不改变 lossless 合同 |

## 资料边界与阅读分工

本文只回答三件事：什么叫 lossless speculative decoding；接受率、draft/verify 成本与 speedup 上限如何联系；token/tree/block/reasoning-level 方法分别改变哪个合同。时间顺序和 2023--2026 演进只在 [Evolution](evolution.md) 维护，本文不复制时间线。

经典一手来源采用 [Leviathan et al., ICML 2023](https://proceedings.mlr.press/v202/leviathan23a.html) 与 [Chen et al., 2023](https://arxiv.org/abs/2302.01318)；本地六篇工作通过具体章节承接机制、实验和 infra 证据。reasoning-level 论文若不保持 target token distribution，本文统一标为 lossy/proposal-and-verification，不借用“lossless”标签。

## 1. Lossless correctness contract

设 target model 的 next-token distribution 为 $p(x\mid h)$，drafter 为 $q(x\mid h)$，历史为 $h$。投机解码的正确性目标不是“草稿看起来合理”，而是最终提交 token 的边缘分布仍等于 $p$：

$$
P_{SD}(x\mid h)=p(x\mid h).
$$

一种标准接受-纠正规则是：先从 $q$ 采样候选 $x$，以

$$
a(x)=\min\left(1,\frac{p(x\mid h)}{q(x\mid h)}\right)
$$

接受；若拒绝，则从 residual distribution

$$
r(x\mid h)=\frac{[p(x\mid h)-q(x\mid h)]_+}{\sum_y[p(y\mid h)-q(y\mid h)]_+}
$$

采样 correction。于是接受分支贡献 $\min(p,q)$，拒绝分支补足 $p-q$ 的正部，合计恢复 $p$。greedy decoding 是该合同的退化情形：接受最长与 target argmax 一致的 prefix，并在首个 mismatch 用 target token 修正。

### 1.1 合同成立需要什么

- verifier 必须获得 target 对候选前缀各位置的 logits，且 tree/block attention 不得泄漏未来或兄弟分支。
- sampling temperature、top-k/top-p 和 logit transforms 必须在 draft、verify 与 correction 规则中一致处理；不能先截断分布再套原公式。
- 接受 token 的 KV state 必须与 target 对同一已提交序列的状态一致；draft-only state 不能污染 target cache。
- 浮点/kernel 差异可能使“理论同分布”出现实现偏差，尤其是 quantized target、distributed logits 和非确定 sampling。

### 1.2 什么不属于 lossless

- 用 reward model、embedding similarity 或 LLM judge 接受语义相近 reasoning step。
- 让小模型生成 CoT，仅在低置信时调用大模型。
- 为追求 final-answer accuracy/latency 而改变 target 的 token path 或采样分布。

这些方法可以有价值，但正确定位是 lossy reasoning acceleration。Evolution 的 [step-level correctness 分化](evolution.md#55-step-level--semantic-speculation-的最新分化) 讨论其时间线；本文只保留合同边界。

## 2. Acceptance、accepted length 与速度上限

若每轮 draft $\gamma$ 个 token，逐位置条件接受概率近似为 $\alpha$，忽略相关性，则一轮提交的期望 draft prefix 长度为

$$
E[A]=\sum_{i=1}^{\gamma}P(A\ge i)=\sum_{i=1}^{\gamma}\alpha^i
=\frac{\alpha(1-\alpha^\gamma)}{1-\alpha}.
$$

若 verifier 在全部 $\gamma$ 个 token 都接受时额外从 target 提交一个 token，则期望提交数为

$$
E[C]=1+E[A]=\frac{1-\alpha^{\gamma+1}}{1-\alpha}.
$$

这揭示两个上限：$\gamma$ 增大时 $E[C]$ 会在 $1/(1-\alpha)$ 附近饱和；accepted length 高不等于 speedup 高，因为 draft/tree construction 与 verify tensor shape 也增长。

更一般的单轮成本模型：

$$
T_{round}=T_{draft}(\gamma,B)+T_{pack/tree}(\gamma,B)+T_{verify}(N_v,B)
+T_{accept}+T_{KV}+T_{sched},
$$

$$
\mathrm{Speedup}\approx\frac{E[C]\,T_{AR-target}}{T_{round}}.
$$

$B$ 是 batch/load，$N_v$ 是 target 实际验证节点数。理想化上界假设 draft/pack/scheduler 免费且一次 target forward 与单 token 一样快，则 speedup 至多 $E[C]$；真实系统永远更低。JetSpec 明确展示 [tree budget 是负载相关旋钮](../papers/jetspec.md#47-serving-中-tree-budget-是负载相关旋钮)，D²SD 也在[关键结论](../papers/d2sd.md#5-关键结论)和[Infra 需求分析](../papers/d2sd.md#8-infra-需求分析)中说明更长 accepted prefix 可能被额外 draft/verify 成本抵消。

### 2.1 应同时报告的指标

| 指标 | 回答什么 | 常见误读 |
|---|---|---|
| acceptance rate | 每个 proposed token 被接受的概率 | 不等于一轮提交长度 |
| accepted length | 每轮接受的 draft token 数 | 不包含 correction/bonus token 时口径会不同 |
| draft latency | proposal 成本 | 不能只按 draft model 参数量估算 |
| verify latency | target 对 token/tree/block 的成本 | 节点数与 attention layout 很关键 |
| OTPS/throughput | 实际提交 output tokens/s | batch/load/backend 不同不可横比 |
| TTFT/TPOT/P99 | 用户体验与尾延迟 | 平均 speedup 可能掩盖尾部退化 |
| quality/distribution test | 是否保持合同 | final accuracy 相同不代表同分布 |

## 3. Mechanism taxonomy

### 3.1 Token-chain drafting

独立小 drafter 或 feature drafter 自回归产生 $\gamma$ 个 token，target 一次并行评分。优点是 contract 清晰、实现成熟；瓶颈是 drafter 自身仍串行，且 $\alpha^i$ 使长 prefix 概率衰减。EAGLE 类方法通过 target hidden states 提高 $q\approx p$，但仍有 sequential draft latency。

P-EAGLE 把 feature drafter 改成 parallel MTP：冻结 target，复用 hidden states，一次预测多个位置；其 mask precomputation 和 sequence partitioning 处理长上下文训练。具体机制见 [P-EAGLE 架构](../papers/p-eagle.md#41-架构)，接受与 vLLM OTPS 见 [Acceptance length](../papers/p-eagle.md#51-acceptance-length) 和 [OTPS](../papers/p-eagle.md#52-otps)。它改变的是 draft latency，不改变 target verify contract；已合并的 vLLM 支持属于论文后的 runtime 证据，不能替代训练代码。

### 3.2 Token-tree drafting

tree 一轮提供多条候选路径，target 用 tree-causal mask 评分全部节点，再提交最长 accepted path。它把预算从“加深一条链”改成“增加 breadth/depth”，提高覆盖率；代价是 $N_v$、tree KV/layout、packing 和 scheduler 成本。

JetSpec 的 causal-parallel head 在一个 forward 内为 depth 位置建立因果依赖，最强证据支持 rank-1 主干保真；off-argmax 分支仍共享深度 logits，不能概括为完整 branch conditioning。其 [方法与阶段边界](../papers/jetspec.md#6-方法重建与阶段边界)、[high-budget 主结果](../papers/jetspec.md#9-主结果高预算扩展) 与 [消融和收益归因](../papers/jetspec.md#10-消融技术点证据矩阵与收益归因) 说明：tree coverage 是主要来源，causal head 的直接优势是降低对深度损失权重的敏感性，不能把全部 speedup 归给 head。

### 3.3 Block / diffusion drafting

block drafter 一次或少数步并行预测一段 token，target 仍按 token contract 验证。DFlash 用 block diffusion 解决 sequential drafter；其[研究方法](../papers/dflash.md#4-研究方法)、[关键结论与 claim 证据矩阵](../papers/dflash.md#5-关键结论与技术-claim-证据矩阵)与[Infra 需求分析](../papers/dflash.md#8-infra-需求分析)展示算法和系统两侧。

DFlash 的局限是 block 内 prefix dependency 弱、首个 mismatch 后缀浪费。D²SD 用 confidence 定位潜在拒绝边界，再以 variable-prefix drafter 生成共享前缀分支；见 [D²SD 研究方法](../papers/d2sd.md#4-研究方法)与[关键结论](../papers/d2sd.md#5-关键结论)。

HyperDFlash 不是简单加深 vanilla DFlash，而是让 block drafter 的 hidden-state reducer 对齐 target 的 mHC 架构，并用 LM-head KL distillation 约束前两个位置；见 [关键公式](../papers/hyperdflash.md#44-关键公式)、[主结果](../papers/hyperdflash.md#51-主结果) 与 [收益归因](../papers/hyperdflash.md#54-收益来源归因)。matched six-step 对比支持完整 bundle 的优势，但组件消融缺失，因此“架构对齐 + distillation”只能作为组合机制解释，不能拆分量化。

DSpark 位于纯并行 block 与纯 AR draft 之间：semi-autoregressive groups 保留部分依赖，并用 confidence scheduling 动态决定何时 verify。其[研究方法](../papers/dspark.md#4-研究方法)、[关键结论与证据矩阵](../papers/dspark.md#5-关键结论与技术主张证据矩阵)与[Infra 需求分析](../papers/dspark.md#8-infra-需求分析)表明，动态 policy 必须与 load/scheduler 联合评估。

### 3.4 Reasoning-step / semantic proposals

对象从 token 变成自然语言 step/thought 后，验证器通常判断语义可接受、奖励或最终答案质量。它可跳过大量 target reasoning compute，但一般不满足 $P_{SD}=p$：step segmentation 不是稳定随机变量，semantic equivalence 也不等价于 target 自由生成的路径概率。

因此合理分类是：

| 系统 | target token distribution | 合同 | 合理指标 |
|---|---|---|---|
| token/token-tree/block SD | 可保持 | lossless acceptance/correction | distribution + OTPS |
| reward/semantic step acceptance | 通常改变 | lossy quality-cost | final accuracy、calibration、cost |
| small-large cascade/router | 通常改变 | selective escalation | target-call rate、quality、tail latency |

## 4. Draft/verify 成本按机制拆解

| 机制 | $T_{draft}$ | $N_v$ / verify | 主要额外成本 | 主要收益 |
|---|---|---|---|---|
| sequential token | $O(\gamma)$ forwards | chain length $\gamma$ | draft KV/cache | 高 $q/p$ 对齐 |
| parallel MTP | one/few forwards | chain positions | MTP heads、mask | 降 draft latency |
| tree | one/few forwards + construction | all tree nodes | score/top-k/pack/tree mask | candidate coverage |
| block diffusion | $S_d$ denoise steps | block tokens | diffusion states、context injection | block parallel proposal |
| confidence branch | base block + VP branches | cascade tree | confidence/top-k boundaries | 减少后缀浪费 |
| semi-AR scheduled | group forwards | adaptive | scheduler/control divergence | 质量-延迟自适应 |

真实比较必须使用 bridge baseline：同 target、同 tokenizer、同 prompt、同 sampling、同 verify backend、同 batch/load，再逐步替换 drafter、tree construction 与 runtime。否则算法接受率和 CUDA graph/attention kernel/调度收益会混在一起。

## 5. KV cache、attention 与 serving contract

### 5.1 Cache ownership

target cache 只应提交 accepted prefix。被拒绝 token/tree nodes 可以临时写入 staging KV，但必须 rollback/free；共享前缀可复用，兄弟分支不能互相可见。D2SD 的共享前缀树与 JetSpec 的 tree-causal mask都依赖这个不变量。

对 $L$ 层、$n_{kv}$ KV heads、head dimension $d_h$、每元素 $b$ bytes、已提交长度 $T$：

$$
M_{KV,target}=2L n_{kv}d_hTb.
$$

tree staging 近似再加 $2L n_{kv}d_hN_vb$，paged KV 可减少碎片但不消除 bytes。长 reasoning 输出使 HBM read 与 cache capacity成为主约束；draft model 小不代表整个 pipeline 不受 target KV bandwidth 限制。

### 5.2 Attention masks

- chain verify：causal prefix + draft block，通常可用标准 causal/paged attention。
- tree verify：节点只能读系统 prefix 与祖先，需要 tree mask或 ancestor indices；错误 mask 会破坏 lossless contract。
- diffusion/block draft：block 内 attention 由 drafter 训练定义；target verify仍必须遵守 token因果性。
- cascade tree：共享 prefix、不同 boundary/branch 需要稳定 node mapping 与 KV slot allocation。

相关实现需求见 [DFlash Infra 需求分析](../papers/dflash.md#8-infra-需求分析)、[JetSpec 调度/自定义算子](../papers/jetspec.md#64-调度serving自定义算子)、[DSpark Infra 需求分析](../papers/dspark.md#8-infra-需求分析)。

### 5.3 Continuous batching 与负载

不同 request 的 accepted length、tree size 与 verify cadence 不同，造成 iteration time divergence。静态最大 budget 在低并发可提高单请求 speedup，在高并发会扩大 verify batch、占用 KV blocks 并降低 batch capacity。故 scheduler 应把 tree/block budget 视为 load-aware policy，而不是模型常量。

端到端应报告：batch size/concurrency、prompt/output length distribution、TP degree、GPU、dtype、KV format、CUDA graphs、P50/P99、OTPS/TPOT、draft/verify breakdown 与 rejected-node memory。

## 6. Acceptance 与 speedup 的常见错误归因

- “accepted length 增加，所以更快”：忽略额外 branches/denoise/packing。
- “kernel 更快，所以接受率提高”：runtime kernel 不改变 candidate distribution 时不应影响 acceptance。
- “tree budget 更大，所以 coverage 更好”：若 score/conditioning 不一致，新增路径可能低质量且增加 verify。
- “最终 accuracy 相同，所以 lossless”：final-answer metric 不能检验 token distribution。
- “平均 speedup 高，所以 serving 更好”：高并发与 P99 可能退化。

六篇本地证据提供了互补反例：D2SD 展示 accepted length 与 speedup 解耦；JetSpec 展示 tree budget/load 交互；DFlash 展示 serving 高并发收益下降；DSpark 展示 confidence policy 需要 runtime support；P-EAGLE 展示 draft latency 也可成为上限；HyperDFlash 展示 drafter/target architecture mismatch 会限制 proposal quality。

## 7. 开放问题

### Lossless correctness

- quantized/distributed target 下如何测试 distribution equivalence，而不只比较 greedy output？
- top-p、temperature、repetition penalty、grammar constraint 与 tree verify 如何组合 residual correction？
- speculative tool use / structured output 的 side effects 如何回滚？

### Candidate generation

- 如何在固定 $T_{draft}+T_{verify}$ 下联合选择 depth、breadth、block size 与 denoise steps？
- confidence 是否校准到“首个 rejection boundary”，还是只相关于 marginal token accuracy？
- parallel head 如何保持 prefix conditioning，又不退回 sequential draft？

### KV 与 serving

- staging tree KV 如何与 paged attention、prefix cache、preemption 和 migration 协同？
- load-aware controller 如何避免 request 间不公平与 P99 放大？
- draft/target colocate、disaggregate 或跨 GPU/NPU 部署时，hidden state/logits/KV 传输何时抵消收益？

### Reasoning-level

- 如何定义可校准的 semantic acceptance risk，而非只用 judge preference？
- target 是否拥有最终裁决权，错误 step 能否恢复，是否报告 path divergence？
- lossy reasoning speedup 应如何同时报告答案质量、token/call cost 和安全失败？

## 8. 最小评测清单

1. 固定 target、sampling contract、backend、dtype、prompt/output 分布和 batch/load。
2. 分开测 draft、tree/pack、verify、accept、KV/scheduler latency。
3. 同时报 acceptance rate、accepted/committed length、OTPS、TPOT、P50/P99 和 peak KV。
4. lossless 方法做 distribution/seed 回归；lossy reasoning 方法明确 quality-cost contract。
5. 逐级 bridge baseline：AR target -> sequential SD -> parallel/block drafter -> tree/confidence -> runtime optimizations。
6. 对 budget 做 load sweep，不只报最佳离线点。

## 9. 与 Evolution 的双向导航

- 需要时间线：读 [Evolution 的 2022--2023 lossless 奠基](evolution.md#2-2022-2023token-级-lossless-speculative-decoding-奠基) 和 [2026 parallel/tree/block 主线](evolution.md#6-2026drafter-自身并行化block-diffusion-和-parallel-tree-成为前沿)。
- 需要合同/公式：留在本文 [lossless contract](#1-lossless-correctness-contract) 与 [speedup model](#2-acceptanceaccepted-length-与速度上限)。
- 需要单篇证据：按 [机制分类](#3-mechanism-taxonomy) 进入六篇 Paper 的 method/result/infra 章节。
