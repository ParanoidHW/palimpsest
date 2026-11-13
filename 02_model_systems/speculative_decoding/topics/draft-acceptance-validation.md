---
document_type: topic
domain: model-systems
collection: speculative-decoding
tags: [topic, collection/speculative-decoding, topic/draft-model-training, topic/acceptance-validation]
review_status: research-note
canonical: true
---

# 投机草稿模型的训练时接受率验证与监测

> [!info] 文档关系
> - 文档类型：Topic / 工程研究笔记
> - 领域入口：[Speculative Decoding README](../README.md)
> - 相关总览：[投机草稿模型：从训推对齐到在线训练的技术思考](speculative-drafter-stack.md)
> - 训练数据生命周期：[Speculator training data lifecycle](speculator-training-data-lifecycle.md)
> - 相关论文：[DFlash](../papers/dflash.md)、[DSpark](../papers/dspark.md)、[DPara](../papers/dpara.md)

## 1. 问题结论

草稿模型没有一个可以直接类比量化 PTQ PPL 的单一标量。原因是接受率不是草稿模型的独立属性，而是由以下因素共同决定：

```text
acceptance
= f(draft distribution, target distribution,
    prefix distribution, decoding protocol,
    draft length, target/draft implementation, serving system)
```

因此，训练时最有价值的替代方案不是继续寻找一个“草稿模型 PPL”，而是建立一个**目标模型条件下的、on-policy sampled-prefix 的离线验证闭环**：

```text
真实 prompt 分布
  -> target on-policy rollout / target-generated prefix
  -> draft 自己连续生成 speculative window
  -> target logits 离线验证
  -> AR_k / survival curve / EAL / first rejection
  -> calibration、分布偏移和成本监控
  -> 少量候选进入真实 serving 实测
```

这能显著减少完整部署测试数量，但不能完全取代最终 serving 测试，因为 draft latency、KV cache、调度、continuous batching、kernel 和负载会改变最终 tokens/s。

## 2. 为什么普通验证集会虚高

### 2.1 Teacher-forcing 与真实 draft rollout 不同

普通验证通常把数据集真值前缀直接喂给 draft：

```text
reference prefix -> draft prediction
```

真实投机推理则是：

```text
accepted prefix
  -> draft token_1
  -> draft token_2 conditioned on draft token_1
  -> ...
  -> target verifies the whole speculative window
```

第一个 draft token 偏离 target 后，后续 token 的 prefix 也会偏离。于是 teacher-forced token agreement 不能代表连续 accepted prefix。已有训练感知工作也明确区分训练 batch acceptance 与跨任务最终 Spec-Bench 表现：训练 batch 直接来自训练分布，不能自动外推到其他任务。[5]

### 2.2 独立位置准确率不能代表连续接受长度

投机验证在第一个 rejection 后丢弃后续位置。因此真正关心的是：

```text
P(L >= 1), P(L >= 2), ..., P(L >= gamma)
```

而不是只看所有 proposed token 的总体 accepted/drafted 比例。两个模型可能拥有相近的平均 token agreement，但一个模型在第 1 个位置频繁失败，另一个模型在第 4 个位置才失败；它们的 EAL、target 调用次数和实际收益会明显不同。

### 2.3 解码协议会改变指标含义

至少要分开评估：

- greedy draft + greedy target；
- stochastic draft + rejection sampling；
- target/draft 的 temperature、top-k、top-p；
- thinking / non-thinking；
- speculative length `gamma`；
- target 是否量化；
- tokenizer、BOS/EOS、chat template 和 bonus token 处理。

greedy 接受关注 top-1 一致性；sampling/rejection sampling 关注 target 与 draft 分布的 overlap。不能用 greedy acceptance 直接推断 sampling acceptance，也不能用采样 acceptance 直接推断线上 greedy speedup。[1]

## 3. 训练时应使用的核心指标

### 3.1 Conditional Acceptance Rate

设一轮最多 draft `gamma` 个 token，第 `k` 个位置的条件接受率为：
$$
AR_k = P(\text{token } k\text{ accepted}\mid L\ge k-1)
$$

用它计算 accepted draft token 的期望长度：

$$
E[A] = \sum_{k=1}^{\gamma} P(L\ge k)
     = \sum_{k=1}^{\gamma}\prod_{j=1}^{k} AR_j
$$

如果框架在整段 draft 都通过时额外提交一个 target token，则：

$$
E[C] = 1 + E[A]
$$

SPEED-Bench 和 NVIDIA NeMo 的评测定义都强调 acceptance length、acceptance rate 和 per-position/conditional acceptance 的区别。[1][2]

训练日志至少应该包含：

```text
AR_1 ... AR_gamma
P(L>=1) ... P(L>=gamma)
EAL / accepted draft tokens
MAT（必须明确是否包含 bonus token）
first_rejection_position
```

### 3.2 Greedy 的离线 EAL

greedy 验证可以对 draft 和 target 的 top-1 结果做逐位置比较：

$$
a_k = 1[\arg\max q_k = \arg\max p_k]
$$

但是 `q_k` 必须在 draft 自己生成的 prefix 上计算，而不是在 reference prefix 上计算。对一批 target-generated prefix，可以在不启动完整 serving engine 的情况下，批量完成 draft rollout 和 target verification。

### 3.3 Sampling 的分布 overlap

对于标准 rejection sampling，给定 prefix 后的单位置接受概率可表示为：

$$
a_k = \sum_v \min(p_k(v),q_k(v))
    = 1 - TV(p_k,q_k)
$$

窗口级 EAL 还要乘以前面位置的 survival probability：

$$
E[A] = \sum_{k=1}^{\gamma}
E\left[\prod_{j=1}^{k}a_j\right]
$$

因此 sampling 评估应同时记录：

```text
TV overlap
JS divergence
KL（辅助，不作为最终 acceptance 指标）
top-k overlap
AR_k / EAL
```

KL/PPL 仍可作为分布拟合的辅助指标，但在 draft 容量受限时，最小化 KL 不保证最大化连续 acceptance。Acceptance-Aware Training、LK Losses 和后续 REAL/D-REAL 类工作都转向直接优化 EAL 或 acceptance-aware objective。[3][4]

## 4. 推荐的 sampled-prefix 验证集

### 4.1 数据构造

不要只从人工答案或静态文本截取 prefix。推荐构建三层验证集：

1. **Target-trajectory set**：从真实 prompt 分布出发，用冻结 target 按线上配置生成 response，并从生成轨迹抽取 prefix。
2. **Draft-rollout set**：从上述 prefix 出发，让每个候选 draft 自己生成 $\gamma$ 个 token，再由 target 离线验证。
3. **Shift set**：用尚未参与训练的真实业务 prompt、长上下文、代码、数学、工具调用、RAG、JSON 和 thinking/non-thinking 场景构成。

每个样本应记录：

```text
prompt_id / domain / conversation_id
 target checkpoint hash
 tokenizer / chat-template hash
 target decoding config
 prefix length / response position
 draft checkpoint hash
 gamma / seed
 draft tokens and logits（或必要的 top-k 信息）
 target logits / verification result
 accepted_mask / survival_mask
 first_rejection_position
```

### 4.2 关键原则

- target prefix 与 draft-induced prefix 分开标记，不能混称为 on-policy；
- 每个 checkpoint 使用相同 prompt、相同 target rollout 和相同随机种子，支持 counterfactual 比较；
- 训练、calibration 和 shift 三套数据必须分开；
- 按 chat/code/math/RAG/tool-call/long-context 分桶；
- 按 response 前段、中段、尾段以及 first rejection position 分桶；
- 固定 tokenizer、template、temperature、top-p、stop condition、bonus token 和 `gamma`；
- 对 target/draft forward parity、权重转换、dtype、TP/EP、padding 和 batch shape 做独立检查。

这类 counterfactual 评估的价值在于：在同一 target trajectory 上比较多个 drafter，减少由于不同 target rollout 和不同 prompt 子集造成的噪声。[6]

## 5. 训练期间的监测信号

### 5.1 三套 acceptance 曲线

同时维护：

```text
A_train       = 训练 batch 的 on-policy acceptance
A_calib       = 独立 target-trajectory calibration acceptance
A_shift       = 模拟真实业务分布的 acceptance
```

并计算：

$$
\Delta_{generalization}=A_{train}-A_{calib}
$$

$$
\Delta_{distribution}=A_{calib}-A_{shift}
$$

如果 `A_train` 上升而 `A_calib` 不升，优先怀疑训练分布过拟合或 prefix 构造不一致；如果 `A_calib` 上升而 `A_shift` 下降，优先怀疑业务分布偏移。

### 5.2 Survival curve 与 first rejection

推荐将 `P(L>=k)` 作为主图，而不是只画平均 acceptance：

```text
x = draft position k
 y = P(L >= k)
```

同时画 `first_rejection_position` 的分布。对于窗口长度 `gamma=7`，至少保留：

```text
AR_1 ... AR_7
P(L>=1) ... P(L>=7)
mean / p50 / p90 EAL
first rejection histogram
```

### 5.3 Confidence-acceptance calibration

草稿模型过度自信时，平均 confidence 可能上涨，但实际 acceptance 下降。将 draft confidence 分桶，记录：

```text
confidence bin
mean confidence
actual acceptance
high-confidence rejection rate
ECE / Brier score
Pearson / Spearman(confidence, acceptance)
```

对于 tree speculative decoding，已有工作专门研究 confidence 与 acceptance 的对应关系，并提出 token-level/path-level calibration；这类指标适合做训练时 early warning，而不是只看平均置信度。[7]

### 5.4 成本与收益联合监测

接受长度不是最终目标。每个 checkpoint 同步记录：

```text
draft latency
 target verification latency
pack/tree/KV/scheduler overhead
target calls per output token
offline goodput estimate
真实 serving tokens/s（少量候选）
```

Goodput 工作指出，接受率高并不保证高负载下加速；speculation 的额外 draft、verify 和调度成本可能抵消 acceptance 收益。[8]

## 6. 不启动完整部署框架的分级验证方案

### Phase A：纯离线快速筛选

只使用批量 target logits 和 draft logits，不启动 continuous batching 或真实服务端：

1. 固定 target-generated prefix；
2. draft 自回归生成 `gamma` 个 token；
3. target 对 draft prefix 做 batched verification；
4. 计算 `AR_k`、survival curve、EAL、first rejection；
5. 对 sampling 计算 TV overlap；
6. 记录 confidence calibration 和 train/calibration gap。

适合每个训练 checkpoint 做，目标是淘汰明显不合格 checkpoint。

### Phase B：轻量 target-verification benchmark

对 Phase A 入选 checkpoint：

- 500～2,000 个真实 prompt；
- 固定 target、draft、tokenizer、template、seed 和 `gamma`；
- 只做离线 batched target verification；
- 按业务桶、response position 和 thinking 模式报告结果；
- 用 bootstrap 置信区间比较两个 checkpoint 的 EAL 差异。

### Phase C：少量真实 serving 实测

只对 Pareto 前沿候选进入框架测试：

- batch size 1 / 8 / 32；
- 单请求 latency、TPOT、P99；
- continuous batching；
- KV cache rollback/append；
- CUDA graph、kernel fusion、通信和 target quantization；
- draft 与 target 的真实并行/异步关系。

Phase A/B 估计算法层 acceptance，Phase C 验证系统层收益，二者不应混为一个指标。

## 7. Checkpoint 淘汰规则

建议采用多指标门槛，而不是“验证集 acceptance 最大”：

```text
保留 checkpoint，当且仅当：

1. calibration EAL 高于当前 best 或处于统计上不劣；
2. AR_1 不下降；
3. 主要 draft positions 的 P(L>=k) 不出现明显退化；
4. train -> calibration gap 在阈值内；
5. high-confidence rejection rate 不上升；
6. chat/code/math/long-context 等主要业务桶不出现系统性退化；
7. draft latency 增量没有抵消 EAL 增益。
```

建议将 checkpoint 选择画成 Pareto front：

```text
x = draft cost / latency
y = EAL 或 offline goodput
颜色 = calibration gap / task bucket
```

不要将以下指标当作最终筛选标准：

- 只看 teacher-forced PPL；
- 只看 KL/CE；
- 只看 overall accepted/drafted；
- 只看 synthetic prompt；
- 只看单一任务的平均 EAL；
- 只看 draft confidence；
- 只看单请求的 theoretical speedup。

## 8. 与现有项目笔记的关系

当前项目已经记录了训推 parity、sampled-prefix、QA regen、chat-template、feature freshness 和真实 rollout 的要求。[投机草稿模型技术栈与思考](speculative-drafter-stack.md) 中的 P0/B0/B9/B12/B15 应作为本验证方案的工程前置条件：

- `B0`：锁定 baseline 和双指标；
- `B9`：fixed feature 与 online feature 对照；
- `B12`：离线与真实 rollout 对照；
- `B15`：chat-template/token parity；
- 再进入 acceptance-aware loss、confidence calibration 和 draft-induced supervision。

本笔记新增的重点是把“接受率验证”从一个模糊的验证集数字，拆成**目标条件、前缀分布、连续存活、校准、分布偏移和系统成本**六条可监测链路。

## 9. 仍需实测确认的边界

- 离线 batched verification 与具体推理框架在 logits、采样和 cache 状态上的一致程度；
- 不同 `gamma` 下，AR 曲线是否能稳定预测真实 EAL；
- target 量化、distributed logits 和 kernel 差异对 acceptance 的影响；
- `A_calib -> A_shift -> serving tokens/s` 的跨业务相关性；
- confidence calibration 是否能可靠支持动态 verify；
- 离线 EAL 提升多少才足以覆盖 draft/verify/scheduler 的额外成本。

所以最终结论不是“离线指标可以替代部署”，而是：

> **离线 on-policy EAL 可以作为高性价比的 checkpoint 筛选器；真实 serving 测试负责校准离线指标到端到端收益的映射。**

## Sources

[1] [SPEED-Bench: A Unified and Diverse Benchmark for Speculative Decoding](https://arxiv.org/html/2604.09557v2)

[2] [NVIDIA NeMo Speculative Decoding Evaluation](https://nvidia-nemo.github.io/Skills/evaluation/speculative-decoding/)

[3] [Acceptance-Aware Draft Model Training for Speculative Decoding](https://arxiv.org/html/2609.24150)

[4] [LK Losses: Direct Acceptance Rate Optimization for Speculative Decoding](https://arxiv.org/html/2602.23881v2)

[5] [Draft, Verify, and Improve: Toward Training-Aware Speculative Decoding](https://arxiv.org/abs/2510.05421)

[6] [Not-a-Bandit: Provably No-Regret Drafter Selection in Speculative Decoding for LLMs](https://arxiv.org/html/2510.20064)

[7] [Calibrated Tree-Structured Speculative Decoding](https://aclanthology.org/2026.emnlp-main.80.pdf)

[8] [Optimizing Speculative Decoding for Serving Large Language Models Using Goodput](https://arxiv.org/pdf/2406.14066v2.pdf)
