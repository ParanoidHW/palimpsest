# OmniFit: Bridging Modalities via Layer-Adaptive Token Compression for Omnimodal Large Language Models

> [!info] 文档关系
> - 文档类型：Paper（final PDF 深度审阅）
> - 领域入口：[README](../README.md)
> - 上位汇总：[ICML 2026 selected papers](../surveys/icml-2026-selected-papers.md)
> - 证据清单：[Figure inventory](../evidence/figure-inventory.md#omnifit)
> - 正式资产：[assets/papers/omnifit-layer-compression](../assets/papers/omnifit-layer-compression/)

> 证据状态：已逐页核验用户提供的 22 页 ICML 2026 final PDF，并对 4 个原论文图表完成 contact sheet 初筛和原分辨率逐图 QA。源码、官方代码与 OpenReview 公开评审仍不可得。

## 修订信息

- 当前文档版本：`1.4.0`
- 当前修订 ID：`rev-omnifit-final-pdf-promotion-20260727`
- 当前修订时间：`2026-07-27T16:00:00+08:00`
- 替代版本：`rev-omnifit-abstract-promotion-20260725` / `1.3.0`

本次用 final PDF 将文档从摘要级提升为全文证据级，新增公式、算法、主表、消融、H800 延迟/显存证据和 4 个正式图表资产。

| 修订 ID | 版本 | 时间 | 类型 | 替代修订 | 摘要 | 结论影响 |
|---|---|---|---|---|---|---|
| `rev-omnifit-initial` | `1.0.0` | 2026-07-17 | initial | 无 | 建立 blocked 交付 | material |
| `rev-omnifit-openreview-refresh` | `1.1.0` | 2026-07-24 | evidence-update | `rev-omnifit-initial` | 恢复 OpenReview/ICML 身份 | material |
| `rev-omnifit-problem-solution-20260725` | `1.2.0` | 2026-07-25 | content-update | `rev-omnifit-openreview-refresh` | 建立题名级问题—方案边界 | minor |
| `rev-omnifit-abstract-promotion-20260725` | `1.3.0` | 2026-07-25 | evidence-promotion | `rev-omnifit-problem-solution-20260725` | 提升官方摘要、LAHP/ARTS 与 headline claims | material |
| `rev-omnifit-final-pdf-promotion-20260727` | `1.4.0` | 2026-07-27 | evidence-promotion | `rev-omnifit-abstract-promotion-20260725` | 提升 final PDF、公式、算法、系统结果与 4 个 QA 资产 | material |

## 1. 核心判断

OmniFit 要解决多模态模型视觉/音频 token 过多带来的 attention、activation 与 KV-cache 开销。论文观察到：深层冗余更高；浅层信息损失会向后传播；不同层的 modality preference 不同；依赖完整 attention map 的 saliency 又与 FlashAttention 路径不兼容。

方法以 LAHP 规划“每层保留多少”，以 modality preference 规划“各模态各保留多少”，再以 ARTS 决定“具体保留哪些 token”。完整方法的质量、TTFT/TPOT 与显存证据较强；但代码缺失，且 Table 5 不是完整 factorial design，因此不能把全部收益精确拆给每一个子项。

![OmniFit 总览：离线 profiling 与在线 layer-wise token selection。](../assets/papers/omnifit-layer-compression/fig6-omnifit-overview-caption.png)

## 2. 术语与符号

| 术语/符号 | 含义 | 来源与边界 |
|---|---|---|
| LAHP | Layer-Adaptive Heterogeneity Profiling | §4.1；training-free 仍包含离线 calibration |
| modality preference | 以 token 数归一后的逐层模态 attention density | Eq. 6；依赖模型和输入分布 |
| ARTS | Alignment-Rectified Token Selection | §4.2 |
| DPC-KNN anchors | 从当前样本的 encoder 输出 $H_0$ 选出的代表性 anchors | Algorithm 2；“pre-computed”指进入各层前按样本计算，不是全局常量 |
| $k_{\rm eff}^{(l)}$ | 第 $l$ 层累计能量超过 $\delta$ 的最小有效秩 | Eq. 3 |
| $r^{(l)}$、$\Psi(l)$ | 第 $l$ 层 retention ratio 与累计信息代理 | Eq. 4 |
| $\rho_m^{(l)}$ | 第 $l$ 层对模态 $m$ 的 preference | Eq. 6–7 |
| $S_i$ | token $i$ 的 norm + 正 cross-modal anchor similarity 分数 | Eq. 8 |

## 3. 问题—方案—证据闭环

| 失败/约束 | 设计与改变 | 预期优化 | 证据 | 判断 |
|---|---|---|---|---|
| Uniform ratio 忽略逐层冗余 | 有效秩驱动的 LAHP | 保护浅层、利用深层冗余 | Eq. 3–5、Table 5 | composite evidence |
| 模态重要性随层变化 | $\rho_m^{(l)}$ 分配 vision/audio 预算并保留文本 | 保留跨模态证据 | Eq. 6–7、Table 5 | partially supported |
| attention-map saliency 成本高 | ARTS anchors + 一次性 score | 兼容高效 attention 路径 | Eq. 8、Table 5 | supported |
| 压缩开销可能吞噬收益 | offline profiling / online execution 解耦 | 取得真实延迟与显存收益 | Figure 8、Table 4 | reported setup supported |

因果链是：层/模态异质性 → 按层/模态规划 retention → 以 cross-modal anchor 选择 token → 后续层 attention/KV token 减少 → 质量保持同时降低 TTFT、TPOT 与显存。整体判断为 **partially supported**：完整方法证据强，但每个 planner 子项和 merge 操作未全部隔离。

## 4. 方法重构

Eq. 3 对每层表示做 SVD，取累计能量超过 $\delta$ 的最小 $k_{\rm eff}^{(l)}$。Eq. 4 令

$$
\Psi(l)=\prod_{i\le l}\frac{k_{\rm eff}^{(i)}}{d},\qquad
r^{(l)}=\xi\frac{\mu\Psi(l)}{\overline{\Psi}},
$$

Eq. 5 在 $C(n)=c_1n+c_2n^2$ 预算下求 $\xi$。Eq. 6–7 用逐层 modality preference 分配 vision/audio 的剩余预算，并保留 text。DPC-KNN 在 encoder 后选 32 个 anchors；Eq. 8 以 token norm 与对侧模态 anchor 的正相似度构成 $S_i$。score 只算一次，各层按计划 top-$k$，其余 token 合并。

默认校准使用 AVQA 与 Ola 的 1024 样本，$\delta=0.9$、$\lambda=1.5$、DPC-KNN $K=5$、anchors $M=32$。

## 5. 质量、消融与归因

![Qwen2.5-Omni-3B 主结果。](../assets/papers/omnifit-layer-compression/table1-main-results-caption.png)

- 40% token：平均相对性能 99.94%。
- 30% token：99.32%。
- 20% token：98.68%，高于 OmniZip 94.41%。
- 20% 跨模型：Qwen-7B 97.28%、OmniVinci 95.87%、Qwen-Omni-30B 93.46%。

![组件消融。](../assets/papers/omnifit-layer-compression/table5-component-ablation-caption.png)

Table 5 的五列结果：

- RandomDrop：`50.1 / 20.9 / 40.9 / 59.4 / 55.7`
- RandomDrop + LAHP：`55.3 / 30.1 / 51.5 / 65.5 / 63.9`
- ARTS：`55.4 / 28.6 / 48.5 / 61.8 / 60.1`
- ARTS + TRP：`58.9 / 36.5 / 55.4 / 67.7 / 67.0`
- ARTS + LAHP：`62.0 / 45.1 / 59.8 / 68.0 / 67.2`

这些行分别支持 selector 与 planner 的价值，但不是全 factorial：MPP/TRP、merge、effective-rank schedule 的每一项不能被独立精确归因。

## 6. Infra 与部署证据

离线 calibration 复杂度约为 $O(N_{\rm calib}L(Nd^2+N^2))$，跨推理摊销。在线 score 为 $O(NMd)$（$M$ 小且固定），逐层选择近似线性；attention 二次项降到约 $O((r_lN)^2d)$，KV memory 与 $\sum_l r_lNd$ 成正比。

![单 H800 上的 TTFT/TPOT 结果。](../assets/papers/omnifit-layer-compression/fig8-inference-speed-caption.png)

- 同等精度设置下，7B/30B 的最大 TTFT speedup 为 2.20×/2.31×，TPOT 为 1.20×/1.39×。
- Appendix 的 7B 精确点：length 2048 时 TTFT 855 ms → 387 ms；batch 32 时 TPOT 32.5 ms → 27.0 ms。
- Table 4：Qwen-7B 35.7 GB → 14.5 GB（约 2.5×）；30B full model OOM，OmniFit 为 70.2 GB。
- 8×H800 calibration：7B 小于 30 分钟，30B 约 58.6 分钟；appendix 的 256 样本单卡小于 5 分钟是更小 calibration 配置，不能混为同一成本。

论文未报告带宽计数器、互联影响、p95/p99、NPU 路径或 host overhead，不能把单 H800 结果无条件外推到所有 serving 栈。

## 7. Related Work、代码与评审边界

OmniFit 相对 uniform pruning 使用逐层预算，相对 attention-map pruning 使用 FlashAttention-compatible proxy，相对 learned compressor 不更新模型参数。与 OmniZip/Echoing Pixels 的主表对比支持质量优势，但实现成熟度、baseline 覆盖与硬件优化并未完全统一。

未找到可核验的官方 repository、commit、checkpoint 或 config，因此压缩插入层、position remapping、merge kernel、dynamic shape 和 KV invalidation 都保持 `unverified`。OpenReview forum 返回 challenge，reviews、rebuttal 与 discussion 不可得。

## 8. 局限与待验证项

- 缺少源码、代码、配置与 checkpoint。
- 组件消融并非完整 factorial design。
- analytical cost model 对不同 accelerator/kernel 的适配范围未充分验证。
- calibration 数据迁移、长上下文、batch 内不同 retention 和 tail latency 仍需更多证据。
- final PDF、正式图表、主结果与 H800 系统数字已核验；上述缺口主要限制复现与跨系统外推。
