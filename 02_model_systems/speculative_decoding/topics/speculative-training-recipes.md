---
tags:
  - topic/speculative-decoding-training
  - collection/speculative-decoding
  - domain/model-systems
document_type: topic
domain: model-systems
collection: speculative-decoding
review_status: maintained
canonical: true
---

# 现有工作：投机模型训练 Recipes

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[Foundations and trends](../surveys/foundations-and-trends.md)
> - 相关文档：[投机草稿模型技术栈与思考](speculative-drafter-stack.md)
> - 相关规划：[DeepSpec online_train 后续算法与实验规划](deepspec-online-train-followup-planning.md)
> - HTML 补充页：[投机模型训练 Recipes](../supplements/speculative-training-recipes.html)

## 1. 这页要回答什么

投机模型训练的关键问题不是“给模型增加几个预测头”，而是让训练时的输入状态接近推理时的状态。推理中的 MTP（Multi-Token Prediction，多 token 预测）会递归使用前一位置自己生成的 hidden state；如果训练始终喂给它由目标模型产生的干净 hidden state，训练损失可能下降，但后面几个 draft position 的接受长度仍会掉得很快。

本页先整理 NVIDIA《Nemotron 3.5 Super and Lightning》（arXiv:2610.38095v1，2026-10-28）公开的 MTP recipe。这里把“模型预训练阶段的 MTP 初始化与 warmup”和“后训练完成后的 MTP boosting”分开，因为二者的目标、数据和训练步数不同。

## 2. 论文给出的完整 MTP 流程

```text
已有 backbone / MTP checkpoint
        ↓
按模型结构初始化 MTP head
        ↓
冻结 backbone，仅训练 MTP head
        ↓ 100B token warmup
        ├─ Lightning：标准 2-step recursive MTP
        └─ Super：hidden-state mixing，模拟推理时混合状态
        ↓
backbone 继续做蒸馏、长上下文和后训练
        ↓
Super：SFT checkpoint 上先做 4k steps MTP-only warm start
        ↓
最终 post-trained backbone 上继续做 MTP boosting
        ├─ Super：25k steps
        └─ Lightning：48k steps
        ↓
SPEED-Bench qualitative split 上测 acceptance length
```

这条流程的核心边界是：MTP head 负责提出多个候选 token，backbone 仍然冻结并负责最终验证；论文没有把 MTP boosting 写成重新训练整个目标模型。

## 3. 第一阶段：MTP 初始化与 100B token warmup

### 3.1 Super 的初始化

Nemotron 3.5 Super 从 Nemotron 3 Super Base 的 MTP 参数开始。原始模型有两个不同的 MTP head；论文只取第一个 head 来初始化新的单个递归共享 head，丢弃第二个 head。这样做的含义是：把多个物理 head 收敛为一个可以重复调用的 head，同时尽量保留原模型的表示空间。

### 3.2 Lightning 的初始化

Lightning 也从 Nemotron 3 Super Base 的 MTP head 开始，但它的 backbone 规模不同。论文先把 latent MoE projection 融合进 expert 的上下投影矩阵，然后裁剪结构以匹配 Lightning：hidden size 从 4096 变为 2688，MoE intermediate size 从 2688 变为 1856，路由专家数从 512 变为 128。

这不是普通的权重拷贝，而是“先做表示融合，再按目标架构缩小”。因此复现时必须把权重转换脚本、裁剪规则和最终 tensor shape 固定下来，否则同一个 recipe 可能实际训练的是另一套 MTP 初始化。

### 3.3 Warmup 的共同设置

- 训练预算：100B tokens。
- backbone：冻结。
- 可更新参数：只有 MTP head。
- 目的：先让 MTP head 适应 backbone 的 hidden-state 表示，不改变主模型能力。

### 3.4 为什么 hidden-state mixing 有必要

标准递归训练在深度 $k$ 使用第 $k-1$ 步由真实序列产生的 shifted hidden states；而推理时，越往后的 draft position 越可能接收到前一 MTP step 自己生成的 synthetic hidden state。于是同一个 head 在训练和推理中看到的状态分布逐步分离，后位 acceptance 下降。

Super 在 warmup 中采用 hidden-state mixing：第 $k$ 步不只使用第 $k-1$ 步的状态，而是从前面多个 MTP step 产生的状态中采样输入。它不完整模拟每次测试时递归展开，但让 head 提前见到 backbone state 与 synthetic state 的混合，降低训练到推理的状态分布差距。

论文明确给出的是 Super 使用 mixing、Lightning 使用标准 2-step recursive MTP；论文没有把所有 mixing 概率、采样分布和 batch 级实现细节公开，因此这些参数不能从论文中补猜。

## 4. 第二阶段：后训练后的 MTP boosting

### 4.1 为什么要在后训练后再做一次

backbone 在 SFT、RL 和其他 post-training 阶段后，输出分布会改变。早期 warmup 得到的 MTP head 仍然依附于旧 backbone 状态，直接把它接到最终 checkpoint 上会丢失一部分接受长度。因此论文对 MTP head 单独再训练：backbone 保持冻结，只让 MTP head 适应最终模型。

Super 有两个 MTP-only 阶段：先在 SFT checkpoint 上做短 warm start，再把该 head 迁移到最终 post-trained backbone 上继续 boosting。Lightning 跳过 SFT warm start，只在最终 backbone 上 boosting。

### 4.2 数据生成和监督范围

论文用对应 backbone 生成 on-policy rollouts：

- 普通数据来自 `Nemotron-Post-Training-Dataset-v2`。
- Agent 数据来自 `Nemotron-RL-Super-Training-Blends`。
- 采样 temperature 为 1。
- 每条序列最多 8K tokens。
- loss 只累积 assistant response tokens，不对用户输入部分计算监督。

这一步与普通 teacher-forcing 的区别在于：训练样本中的 response 是由当前对应 backbone 重新 rollout 得到的，MTP head 训练时面对的是更接近实际推理的 response 分布。两个数据集的具体混合比例和每个子集的采样权重，论文该节没有公开，不能自行补齐。

### 4.3 训练目标

之前的 MTP 训练阶段使用 cross-entropy；boosting 阶段改用 LK loss。论文的解释是，冻结 backbone 作为 teacher，用 teacher 分布监督 MTP head，可以更好地对齐 backbone，尤其改善 probabilistic draft sampling。

这里的 LK 不是普通 cross-entropy 的另一个名字。在相关 MTP 工作中，它通常写成：

$$
L_{\mathrm{LK}}=-\log\sum_{x\in\mathcal V}\min\bigl(p(x),q(x)\bigr).
$$

公式解释：$p(x)$ 是冻结的 target 分布，$q(x)$ 是 MTP head 给出的分布，$\mathcal V$ 是整个词表。对每个词取两边概率的较小值再求和，得到两个分布的重叠程度；重叠越大，$L_{\mathrm{LK}}$ 越小。若两边完全相同，重叠为 1，损失为 0；若几乎没有重叠，损失会变大。它与只关心一个真实 token 概率的 cross-entropy 不同，更直接地优化 probabilistic speculative sampling 所需要的分布重叠，也就是单步被接受的概率。

2610.38095 的正文没有在该节重新展开这个公式，因此这里按相关 MTP 文献解释 LK 的含义，不把它写成普通 token cross-entropy 的同义词。实现时仍需核对论文引用的 LK 工作和官方 recipe，尤其是温度、截断和权重设置。

### 4.4 步数

| 模型与阶段 | backbone | MTP 更新步数 | 作用 |
| --- | --- | ---: | --- |
| Super，SFT checkpoint warm start | 冻结 | 4k | 先让 MTP head 适应 SFT 后的 backbone |
| Super，最终 checkpoint boosting | 冻结 | 25k | 对齐最终 post-trained backbone |
| Lightning，最终 checkpoint boosting | 冻结 | 48k | 在最终 backbone 上直接训练 MTP head |

论文报告 Super 的 SFT-stage MTP head 迁移到最终 checkpoint 后仍保留部分收益，但最终 25k boosting 才得到完整提升。

## 5. 证据：收益到底说明了什么

论文在 SPEED-Bench qualitative split、draft length 7 上报告平均 acceptance length（AL）：

| Super 状态 | greedy，temperature=0 | probabilistic，temperature=1 |
| --- | ---: | ---: |
| Final native MTP | 4.287 | 3.787 |
| 加载 SFT 阶段 MTP head | 4.528 | 4.436 |
| 再做 25k MTP boosting | 4.718 | 4.612 |

这支持两条判断：第一，后训练后的 backbone 确实需要重新适配 MTP head；第二，hidden-state mixing 与 LK 监督对 probabilistic sampling 的帮助更明显。论文还报告 boosting 后每个 draft position 都有改善，深层位置增益最大，符合“越深越受训练—推理状态差异影响”的机制解释。

但这些结果主要验证 acceptance length。它们不能单独证明端到端 tokens/s 一定提高，因为真实收益还取决于 MTP head 计算成本、目标验证成本、batch、KV cache 和推理框架调度。

## 6. 对我们训练计划的直接启发

1. **把 MTP warmup 与最终 backbone 适配拆开。** 早期 head 训练解决“能否使用 backbone hidden state”，后期 boosting 解决“post-training 后分布是否改变”。
2. **把 hidden-state mixing 当成独立变量。** 训练时必须记录每个 MTP depth 实际使用了哪类状态，不能只记录总 loss。
3. **后训练数据要生成 on-policy response。** 如果只把旧 response 做 teacher-forcing，无法复现论文要解决的递归状态差异。
4. **训练指标和线上指标同时保留。** teacher-forcing loss、sampled-prefix loss、每位置 acceptance、平均 AL、draft latency、target calls 和端到端时延要分开记录。
5. **先锁定数据混合和采样协议。** 论文公开了两个数据集、temperature=1、8K cap 和 assistant-only loss，但没有公开全部混合比例；实验配置需要显式补齐。

## 7. 仍然缺少的复现信息

- hidden-state mixing 的精确采样概率和实现细节；
- LK loss 的完整公式、温度参数和权重；
- 两个 rollout 数据集的混合比例与去重方式；
- MTP head 的学习率、batch、优化器和硬件配置；
- 4k/25k/48k steps 对应的有效 token 数；
- MTP head 权重转换与 checkpoint 版本；
- acceptance length 提升转化为端到端吞吐的完整 serving 配置。

因此，这篇论文可以作为“训练流程和变量拆分”的强参考，但还不能单凭论文复现出完全相同的 checkpoint。

## 8. 一手来源

- [arXiv:2610.38095](https://arxiv.org/abs/2610.38095)，§2.1 “Multi-Token Prediction”、§3.7 “MTP Boosting”、Table 8–9。
- [Nemotron-Post-Training-Dataset-v2](https://huggingface.co/datasets/nvidia/Nemotron-Post-Training-Dataset-v2)。
- [Nemotron-RL-Super-Training-Blends](https://huggingface.co/datasets/nvidia/Nemotron-RL-Super-Training-Blends)。
- [SPEED-Bench](https://huggingface.co/datasets/nvidia/SPEED-Bench)，用于 acceptance length 评估。
