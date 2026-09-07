# RL 期间的 drafter 联合适配

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[README](../README.md)
> - 上位汇总：[Foundations and trends](../surveys/foundations-and-trends.md)
> - 证据资产：无
> - 相关文档：[RL drafter co-training evidence](../evidence/rl-drafter-cotraining.md)

## 资料边界

本文讨论一种训练组织方式：目标模型在做强化学习（RL）后训练时，同时在线更新、蒸馏或从当前目标模型重新构造 speculative decoding 的 drafter。它不等同于“用 drafter loss 反向更新目标模型”。除非特别说明，本文假设 target 仍是 rollout 的最终 verifier，draft-and-verify 保持目标策略的采样分布。

证据标签约定：`[论文实证]` 是来源明确报告的实验或系统行为；`[综合推论]` 是基于多个来源和机制的归纳；`[待验证]` 是合理但当前来源没有完成因果消融的假设。逐条来源见 [证据清单](../evidence/rl-drafter-cotraining.md)。

## 1. 先区分三种“联合训练”

| 组织方式 | drafter 如何变化 | 主要风险 | 不能直接推出什么 |
|---|---|---|---|
| 在线蒸馏 | 用当前 target 的 token、logits 或 hidden states 更新独立 drafter | policy 和特征空间持续变化 | 不能推出 target 精度提高 |
| 空泡训练 | 在长尾 rollout 的空闲 GPU 上抢占式更新 drafter | 更新被中断、版本延迟 | 不能把“几乎无额外占用”当成所有硬件都成立 |
| 当前 target 自构造 | 每个 step 从最新 target 生成量化或跳层 self-drafter | 构造/量化本身有成本 | 不能推出独立 drafter 一定不如 self-drafter |

`P1` 使用前两种思路，`P3` 使用第三种思路；`P2` 则把 online adaptation 作为 RL rollout 系统的可选路径。这里的分类是为了澄清接口，不是声称三篇论文实现相同算法。

## 2. 收益排序：wall-clock 是主收益，接收长度是中间机制

### 2.1 论文直接报告的结果

- **[论文实证] 训练耗时/rollout 吞吐**：`P1` 报告端到端 RL 训练加速超过 1.7x；`P2` 报告 rollout generation 获得 1.5--1.8x 加速、整体 RL step 最多 1.41x；`P3` 报告 rollout latency 最多降低 19.6%、端到端 latency 最多降低 12.7%。这些数字来自不同模型、硬件、batch 和 baseline，不能直接排序。
- **[论文实证] 主模型质量**：`P1` 报告保持 model accuracy，`P2` 报告 validation accuracy 不变，`P3` 报告 preserving final model quality。它们支持“加速不牺牲质量”的系统结论，不支持“drafter 联合训练提高 target 的 intrinsic accuracy”。
- **[论文实证] drafter 可复用**：`P1` 报告训练过程产生的 drafter 可作为部署副产品；这说明联合适配可以避免完全独立的 drafter 训练阶段，但没有证明其最终 drafter 一定优于充分离线蒸馏。

### 2.2 机制推论

**[综合推论] 接收长度是加速的中间变量。** 目标策略由 $p_{\theta_t}$ 变成 $p_{\theta_{t+1}}$ 时，冻结 drafter $q_{\phi_0}$ 逐渐失配。在线更新得到 $q_{\phi_t}$，通常有助于维持 token agreement，从而延长首个 rejection 之前的连续 prefix。真正决定 wall-clock 的仍是：

$$
T_{round}=T_{draft}+T_{verify}+T_{pack}+T_{sync}+T_{update}.
$$

公式解释：$T_{draft}$ 是 drafter 生成候选的时间，$T_{verify}$ 是 target 并行验证的时间，$T_{pack}$ 是候选打包和 mask/KV 准备，$T_{sync}$ 是权重或版本同步，$T_{update}$ 是 drafter 更新成本。接收长度提高只有在减少的 target decode 时间超过新增成本时才转化为端到端收益。

**[综合推论] “同等质量的更短时间”比“同样时间的更高精度”更稳妥。** 标准 verifier-exact speculative decoding 不改变 rollout 的目标分布，因此在相同 RL steps 和样本量下，主模型精度预期基本不变；在固定 wall-clock 下因为完成了更多 rollout/update，最终质量可能更高，但这是吞吐带来的间接收益。

**[待验证] 充分的离线蒸馏可能追平最终接收长度。** 在线适配的独特价值是训练期间持续可用和省掉独立蒸馏阶段，而不是保证最终冻结 drafter 在离线 benchmark 上更强。需要在相同 drafter 参数量、数据量和训练 FLOPs 下做最终 checkpoint 对比。

## 3. hidden-state 漂移与训练稳定性

### 3.1 为什么 hidden state 比 token 分布更棘手

如果 drafter 依赖 target hidden states，则训练关系可写为：

$$
h_t=H_{\theta_t}(x),\qquad f_{\phi}(h_t)\approx y_t.
$$

公式解释：$H_{\theta_t}$ 是第 $t$ 个 RL policy snapshot 的 target 表征，$h_t$ 是输入前缀的 hidden state，$f_{\phi}$ 是 drafter，$y_t$ 是下一位置的 hidden state、logits 或 token 监督。RL 更新 $\theta_t$ 后，监督输入的坐标系也变化，不只是标签分布变化。

**[综合推论]** 如果 buffer 混用多个 policy 版本的 hidden states，同一个 drafter 会同时拟合多个表示坐标系。可能出现 drafter loss 下降但当前 policy 的 acceptance length 不升、更新后短暂变好又随 policy 更新下降，以及为兼容历史表示而牺牲当前表示。

### 3.2 对主模型 RL 的影响边界

- **[综合推论] stop-gradient 情形**：若 draft loss 不回传 target backbone，漂移主要损害 drafter 的收敛和加速稳定性；target 仍由自己的 RL loss 更新，最坏结果通常是加速消失，而不是 target 质量直接崩溃。
- **[综合推论] 共享 backbone 情形**：若 draft loss 与 RL loss 共同更新 target 表征，则

$$
\nabla_\theta L=\nabla_\theta L_{RL}+\lambda\nabla_\theta L_{draft}.
$$

公式解释：$L_{RL}$ 是策略优化损失，$L_{draft}$ 是草稿预测或蒸馏损失，$\lambda$ 是辅助损失权重。此时表征漂移和辅助梯度相互耦合，可能产生梯度冲突、KL 波动或 reward 收敛变差；这是机制风险，不是 `P1`--`P3` 已共同实证的结果。

### 3.3 稳定化建议与证据等级

| 建议 | 判断 | 原因 |
|---|---|---|
| rollout 内冻结 target snapshot，step 边界再切换 | [综合推论] | 把持续漂移切成分段平稳问题 |
| hidden state、label、logits 来自同一 snapshot | [综合推论] | 避免输入/监督跨版本错配 |
| buffer 按 policy version 限制窗口并衰减旧样本 | [待验证] | 可减少 stale features，但需要版本跨度消融 |
| drafter 更新对 target 使用 stop-gradient | [综合推论] | 隔离 drafter 不稳定性与 RL policy 梯度 |
| 使用当前 target 自构造或周期性重构 drafter | [论文实证 + 综合推论] | `P3` 直接采用 target-induced drafter；版本错配解释属于推论 |
| 用 acceptance length、rollout latency 和 time-to-quality 共同调度 | [综合推论] | 单看 loss 或 acceptance 不能覆盖系统成本 |

## 4. 应该如何做公平评测

至少需要四组对照：

1. RL target + 固定 drafter；
2. RL target + 在线 token/logit 蒸馏 drafter；
3. RL target + hidden-state drafter，区分新鲜 buffer 与跨版本 replay；
4. RL 结束后对最终 target 做相同预算的离线 drafter 训练。

每组同时报告 acceptance rate、accepted length、draft/verify/update latency、RL step time、总 GPU-hours、达到固定 reward 的 wall-clock，以及最终 reward/accuracy。若共享 backbone，还要报告 KL、梯度范数和 reward 曲线；否则无法判断“精度变化”来自 drafter 辅助梯度还是 rollout 吞吐。

## 5. 结论与证据标签

1. **[论文实证]** 现有工作最稳固的收益是 RL rollout 和端到端 wall-clock 加速，同时保持主模型质量。
2. **[综合推论]** 接收长度提升是在线适配发挥作用的主要中间机制，但不是最终评价指标。
3. **[综合推论]** hidden-state 漂移会使跨版本 replay 变成移动坐标系上的非平稳监督；梯度隔离和版本一致性是设计要点。
4. **[待验证]** 联合适配是否在固定 GPU-hours 下带来更高最终精度，以及它是否优于同预算离线蒸馏，当前不能从 `P1`--`P3` 的结果推出。

详细来源和每条 claim 的边界见 [RL drafter co-training evidence](../evidence/rl-drafter-cotraining.md)。
