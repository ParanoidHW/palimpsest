# RL 期间 drafter 联合适配的证据清单

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Foundations and trends](../surveys/foundations-and-trends.md)
> - 证据资产：无
> - 相关文档：[RL drafter co-training](../topics/rl-drafter-cotraining.md)

## 资料边界

本清单只记录 RL 后训练期间持续更新或重新构造 drafter 的公开证据，以及由这些证据支持的工程判断。它不把讨论中的机制推论伪装成论文结果，也不声称三篇论文构成同一实验协议。

访问日期：2026-09-07。论文版本以链接页面当前可见版本为准；数字只在论文明确报告的设置内成立。

## 来源登记

| ID | 来源 | 类型 | 论文直接报告的内容 |
|---|---|---|---|
| `P1` | [Taming the Long-Tail: Efficient Reasoning RL Training with Adaptive Drafter](https://arxiv.org/abs/2511.16665)（arXiv:2511.16665，ASPLOS 2026） | paper | Adaptive Drafter 在长尾 rollout 的空闲 GPU 上持续训练；论文摘要报告端到端 RL 训练加速超过 1.7x、保持模型精度，并得到可用于部署的 drafter。正文说明 Online DataBuffer 缓存 rollout 的 hidden states 与 input embeddings。 |
| `P2` | [Accelerating RL Post-Training Rollouts via System-Integrated Speculative Decoding](https://arxiv.org/abs/2604.26779)（arXiv:2604.26779） | paper | 在 NeMo-RL/vLLM 的 8B reasoning workload 上，rollout generation 获得 1.5--1.8x 加速，整体 RL step 最多 1.41x，validation accuracy 不变；系统支持 learner/rollout 权重同步和可选 online draft adaptation。 |
| `P3` | [EfficientRollout: System-Aware Self-Speculative Decoding for RL Rollouts](https://arxiv.org/abs/2606.18967)（arXiv:2606.18967） | paper | 每个训练 step 从当前 target 构造量化 self-drafter，避免独立 drafter 预训练和 online adaptation；论文报告 rollout latency 最多降低 19.6%、端到端 latency 最多降低 12.7%，并保持最终模型质量。 |
| `A1` | 本次讨论的机制综合 | analysis-derived | hidden-state 版本漂移、旧特征 replay、梯度隔离、buffer 新鲜度和 time-to-quality 的因果解释；不属于任何单篇论文的直接实验结论。 |

## 逐条证据边界

| Claim ID | 结论 | 证据类别 | 支撑来源/限定 |
|---|---|---|---|
| `C1` | RL 期间目标 policy 持续变化会使固定 drafter 逐步失配，这是在线适配的直接动机。 | paper | `P1` 明确讨论 evolving target model；`P3` 明确把 evolving policy 列为固定 drafter 的问题。 |
| `C2` | 在线或自适应 drafter 可以提高 rollout 吞吐，并降低端到端 RL wall-clock。 | paper | `P1`、`P2`、`P3` 分别报告了各自设置下的 speedup；不能把数字横向当作统一基准。 |
| `C3` | 这些工作把保持主模型质量作为约束或结果，而不是把 drafter loss 当作提高主模型精度的主要来源。 | paper + analysis-derived | `P1`、`P2`、`P3` 报告 accuracy/quality preserved；“不是主要来源”是对其系统目标和实验设计的归纳。 |
| `C4` | hidden states 与 token/logit 分布都会漂移；混用不同 policy snapshot 的 hidden states 会让 drafter 同时拟合多个表示坐标系。 | analysis-derived | `A1`；三篇来源说明 evolving policy 或 hidden-state buffer，但没有共同的跨版本表征漂移消融。 |
| `C5` | 如果 draft loss 不向 target backbone 反传，漂移主要损害 drafter 收敛和加速稳定性；如果共享 backbone 并反传，则会额外引入 RL/draft 梯度冲突风险。 | analysis-derived | `A1`；这是基于计算图和优化目标的机制推论，不应写成已被 `P1`--`P3` 证明的实验事实。 |
| `C6` | self-drafter 或周期性从当前 target 重构 drafter，是降低 hidden-state 版本错配的一条路线，但可能增加重构/量化开销。 | paper + analysis-derived | `P3` 直接报告 target-induced quantized drafter；“降低版本错配、增加重构开销”是机制解释，后半句需在具体系统测量。 |
| `C7` | acceptance length 是中间指标，最终应以 rollout throughput、RL step time、time-to-quality 和 GPU-hours 评价。 | analysis-derived | 由 speculative decoding 成本模型与 `P1`--`P3` 的端到端报告综合得到；不是单篇论文的统一定理。 |

## 尚未被这些来源充分验证的问题

- hidden-state buffer 的最大版本跨度、清理策略和采样权重对 acceptance length 的因果影响。
- `stop_gradient`、EMA/lagged teacher、低学习率和共享 backbone 之间的独立消融。
- 在相同 GPU-hours 而不是相同 RL steps 下，联合 drafter 是否提高最终 reward 或验证集精度。
- 在线 drafter 更新的额外显存、同步、抢占和通信成本是否被 rollout 节省完全覆盖。
- 高并发、长尾 batch 和不同温度下的 hidden-state 漂移速度与 acceptance degradation 曲线。

## 使用规则

Survey 可以引用 `C1`--`C3` 作为论文报告结果；`C4`--`C7` 必须明确标为“综合推论”或“待验证假设”。任何新增数字必须回到来源论文的具体版本和实验设置，不得从本清单推导出跨论文排行榜。
