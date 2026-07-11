# Kernel Agents 原论文图清单与 QA

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[Paper index](paper-index.md)
> - 证据资产：`../assets/papers/`
> - 相关文档：[Survey paper](../papers/towards-automated-kernel-generation.md)，[AscendKernelGen](../papers/ascend-kernel-gen.md)，[AscendCraft](../papers/ascend-craft.md)，[s1](../papers/s1-test-time-scaling.md)

以下 bbox 以 180 DPI PDF render 的像素坐标 `(x0,y0,x1,y1)` 记录；正式资产本身只保留单一编号对象及完整 caption。2026-07-11 对每张正式图片以原分辨率逐图检查，contact sheet 只用于初筛。

| Paper | Object | Source | Caption（完整中文转述） | Crop / bbox | Usage | QA |
|---|---|---|---|---|---|---|
| towards-automated-kernel-generation | Figure 1 | arXiv:2601.15727v3, PDF p.2 | 按时间和类别组织 LLM-driven kernel generation 的增长趋势及 LLM4Kernel、Agent4Kernel、Datasets、Benchmarks 分支。 | `../assets/papers/towards-automated-kernel-generation/fig1-field-map-caption.png`; `(80,20,1450,630)` on 1530x1980 | 领域版图，不作为性能排序 | pass；caption 完整、单一 Figure 1、边界可读 |
| towards-automated-kernel-generation | Table 2 | arXiv:2601.15727v3, PDF p.7 | 汇总 kernel generation/optimization benchmark 的时间、metrics、hardware 与 task 描述，并解释 metrics/hardware 缩写。 | `../assets/papers/towards-automated-kernel-generation/table2-benchmarks-caption.png`; `(75,70,1455,1180)` | benchmark taxonomy | pass；表体与完整 caption/脚注保留 |
| ascend-kernel-gen | Figure 1 | arXiv:2601.07160v2, PDF p.6 | AscendKernelGen 的数据构建、LLM training 与 hardware-grounded evaluation pipeline。 | `../assets/papers/ascend-kernel-gen/fig1-system-overview-caption.png`; `(80,650,1410,1730)` on 1489x2105 | 系统闭环 | pass；完整图体/caption，无相邻编号对象 |
| ascend-kernel-gen | Table 7 | arXiv:2601.07160v2, PDF p.18 | 在不同 sampling budget 下报告 NPUKernelBench 的 Compilation Rate、Execution Rate 与 generated kernel speedup。 | `../assets/papers/ascend-kernel-gen/table7-main-results-caption.png`; `(105,110,1385,730)` | 主结果与口径拆分 | pass；单一 Table 7、数值清晰、caption 完整 |
| ascend-craft | Figure 3 | arXiv:2601.22760v1, PDF p.6 | AscendCraft 两阶段框架：先按 DSL specification 与 category/shape examples 生成 DSL，再用 mapping rules 做 multi-pass transcompilation。 | `../assets/papers/ascend-craft/fig3-framework-caption.png`; `(100,100,1420,720)` on 1530x1980 | 方法机制 | pass；单一 Figure 3、caption 完整 |
| ascend-craft | Table 1 | arXiv:2601.22760v1, PDF p.8 | 按 operator category 报告 52 个 kernel 的 Comp@1 与 Pass@1，总计 98.1%/90.4%。 | `../assets/papers/ascend-craft/table1-correctness-caption.png`; `(110,120,720,590)` | correctness 主结果 | pass；单一 Table 1、caption 完整；保留原论文脚注标记 |
| s1-test-time-scaling | Figure 2 | arXiv:2501.19393v3, PDF p.3 | 左侧显示 s1K 的 1,000 个高质量、多样、困难问题，右侧显示 s1-32B 位于样本效率前沿。 | `../assets/papers/s1-test-time-scaling/fig2-data-efficiency-caption.png`; `(95,130,1425,800)` on 1530x1980 | 数据与样本效率 | pass；单一 Figure 2、caption 完整 |
| s1-test-time-scaling | Figure 4 | arXiv:2501.19393v3, PDF p.5 | 对比 budget forcing 的 sequential scaling 与 majority voting 的 parallel scaling，并给出各自 token/采样设置。 | `../assets/papers/s1-test-time-scaling/fig4-scaling-caption.png`; `(95,115,1425,765)` | scaling 证据与混杂边界 | pass；单一 Figure 4、caption 完整 |

## QA 结论

- 所有正式图都由官方 arXiv PDF 180 DPI render 裁得；render 与裁剪过程不进入正式知识链路。
- 旧的 `overview.png`、`agent4kernel-overview.png`、`llm4kernel-overview.png`、`quantitative-analysis.png` 没有完整 inventory/caption 或语义重复，不再被正式 Markdown 引用；后续应在确认 PPT/HTML 零引用后迁回 artifacts 或删除。
- 图表仅支撑其明确 caption 和论文上下文；Figure 1 时间线不证明性能演进，mHC 个案也未提升为正式总体结果图。
