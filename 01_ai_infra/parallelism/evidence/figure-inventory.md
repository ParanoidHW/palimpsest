---
tags:
  - evidence
  - collection/parallel-partitioning
  - domain/ai-infra
document_type: evidence
domain: parallelism
canonical: true
---

# Figure Inventory

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 上位 Survey：[并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md)
> - 原论文资产由对应 canonical Paper 独占；教学整理图由对应 Survey 独占。

所有图于 2026-07-31 完成 contact-sheet 初筛和单图原分辨率 QA。每个 crop 只含一个编号对象与完整 caption，bbox 坐标基于对应 PDF 页面渲染，格式为 `(x,y,width,height)`。

| Owner | Object | Type | PDF page | Source page | Bbox | Formal asset | QA |
|---|---|---|---:|---|---|---|---|
| [Megatron-LM](../papers/megatron-lm.md) | Figure 3 | mechanism | 4 | 1870×2420 | `(932,191,750,873)` | [asset](../assets/papers/megatron-lm/fig3_tensor_parallel_blocks_caption.png) | passed |
| [Megatron-LM](../papers/megatron-lm.md) | Figure 5 | result/system | 6 | 1870×2420 | `(925,575,757,385)` | [asset](../assets/papers/megatron-lm/fig5_weak_scaling_efficiency_caption.png) | passed |
| [GPipe](../papers/gpipe.md) | Figure 2 | mechanism | 3 | 1700×2200 | `(280,180,1140,700)` | [asset](../assets/papers/gpipe/fig2_pipeline_mechanism_caption.png) | passed |
| [GPipe](../papers/gpipe.md) | Table 2 | result/system | 5 | 1700×2200 | `(835,190,585,455)` | [asset](../assets/papers/gpipe/table2_throughput_caption.png) | passed |
| [ZeRO](../papers/zero.md) | Figure 1 | mechanism | 3 | 1700×2200 | `(260,280,1180,720)` | [asset](../assets/papers/zero/fig1-zero-dp-memory-stages-caption.png) | passed |
| [ZeRO](../papers/zero.md) | Figure 2 | result/system | 4 | 1700×2200 | `(260,266,1179,612)` | [asset](../assets/papers/zero/fig2-throughput-speedup-caption.png) | passed after tight-crop revision |
| [GShard](../papers/gshard.md) | Figure 3 | mechanism | 5 | 1530×1980 | `(260,168,1010,816)` | [asset](../assets/papers/gshard/fig3_moe_device_placement_caption.png) | passed |
| [GShard](../papers/gshard.md) | Figure 8 | result/system | 21 | 1530×1980 | `(260,194,1020,544)` | [asset](../assets/papers/gshard/fig8_runtime_roofline_caption.png) | passed |
| [Ulysses](../papers/deepspeed-ulysses.md) | Figure 2 | mechanism | 4 | 1700×2200 | `(330,1370,1050,550)` | [asset](../assets/papers/deepspeed-ulysses/fig2-ulysses-design-caption.png) | passed |
| [Ulysses](../papers/deepspeed-ulysses.md) | Figure 3 | result/system | 6 | 1700×2200 | `(200,650,1320,930)` | [asset](../assets/papers/deepspeed-ulysses/fig3-scaling-caption.png) | passed |
| [Ring Attention](../papers/ring-attention.md) | Figure 2 | mechanism | 4 | 2040×2640 | `(352,225,1338,1735)` | [asset](../assets/papers/ring-attention/fig2-ring-attention-mechanism-caption.png) | passed |
| [Ring Attention](../papers/ring-attention.md) | Table 3 | result/system | 7 | 2040×2640 | `(348,213,1346,1232)` | [asset](../assets/papers/ring-attention/table3-max-context-caption.png) | passed |

## QA corrections

- Megatron Figure 3/5：扩边以恢复完整 caption。
- GPipe：Figure 2 与 Table 2 均保留全部 panel/rows。
- ZeRO Figure 2：父级 QA 拒绝顶部约 211 px 无意义白边，修订为四侧各 20 px 安全边距。
- GShard Figure 8：首版 caption 右侧截断后重裁。
- Ulysses、Ring：labels、legend、caption 与全部 rows 在原分辨率可读。

## Survey 教学整理图

以下 SVG 全部由 [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) 独占，固定 `viewBox="0 0 1600 900"`，可编辑、无 `foreignObject`。它们是 analysis-derived 教学整理图，不是原论文 Figure/Table，不计入论文视觉证据数量。过程渲染、contact sheet 与像素检查保留在 process workspace。

| Owner | Asset | 用途 | viewBox | 声明 | QA |
|---|---|---|---|---|---|
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [DP/ZeRO](../assets/surveys/parallel-partitioning-taxonomy/dp-zero-state-lifecycle.svg) | batch shard、gradient reduce、ZeRO 1/2/3 生命周期与 gather 峰值 | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed：XML、原尺寸渲染、逐图与像素 QA，2026-08-02 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [TP](../assets/surveys/parallel-partitioning-taxonomy/tensor-parallel-block.svg) | column → local nonlinearity/head → row → reduce | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed：XML、原尺寸渲染、逐图与像素 QA，2026-08-02 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [PP](../assets/surveys/parallel-partitioning-taxonomy/pipeline-parallel-schedule.svg) | layer stages、micro-batch FWD/BWD P2P 与 bubble | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed：XML、原尺寸渲染、逐图与像素 QA，2026-08-02 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [EP](../assets/surveys/parallel-partitioning-taxonomy/expert-parallel-routing.svg) | token route、A2A dispatch/combine、hot rank | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed after text-bound revision，2026-08-02 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Megatron SP](../assets/surveys/parallel-partitioning-taxonomy/megatron-sequence-parallel.svg) | non-attention activation sequence shard 与 TP 边界 | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed：XML、原尺寸渲染、逐图与像素 QA，2026-08-02 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Ulysses](../assets/surveys/parallel-partitioning-taxonomy/ulysses-layout-transpose.svg) | sequence/head layout transpose 与两次 A2A | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed：XML、原尺寸渲染、逐图与像素 QA，2026-08-02 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Ring/CP](../assets/surveys/parallel-partitioning-taxonomy/ring-context-parallel.svg) | local Q、rotating KV、online softmax 与 causal imbalance | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed after footer-overlap revision，2026-08-02 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [CFGP](../assets/surveys/parallel-partitioning-taxonomy/cfg-branch-parallel.svg) | branch dispatch、local execution、guidance combine 与复制状态 | `0 0 1600 900` | 教学整理图 / 非论文证据 | passed：XML、原尺寸渲染、逐图与像素 QA，2026-08-02 |
