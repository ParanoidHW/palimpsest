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

以下 11 张 PNG 全部由 [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) 独占，使用 TikZ 排版并以 `2400×1350` 输出。它们是 analysis-derived 教学整理图，不是原论文 Figure/Table，不计入论文视觉证据数量。TikZ 源码、PDF、过程渲染、contact sheet 与像素检查保留在 process workspace。

2026-08-03 的 `1.6.0` 修订把普通 DP 与 ZeRO-1 的 $m_1$、$m_2$、$m_K$ 分别画成独立的 `FWD -> BWD -> g_{r,k}` 路径，并用 $G_r^{[0]}$、$G_r^{[1]}$、$G_r^{[2]}$、$G_r^{[K]}$ 显式展示每次 backward 后的累计状态；所有 dataflow 改为 lane 内水平箭头，移除把 updated weight 误接到 micro-batch 输入的回环。`1.5.0` 修订参考用户提供稿的 rank lane 与 feedback loop 视觉语法重绘普通 DP 和 ZeRO-1，补入 $K$ 个 micro-batches 的本地梯度累积，并依据 Megatron Core 固定 commit `b19b1f47cf7e289607f3be480c5f06c6ada25b16` 将 ZeRO-1 修正为 gradient reduce-scatter、owner-local update 和 parameter all-gather。`1.4.0` 修订把 DP/ZeRO 汇总图拆成普通 DP、ZeRO-1、ZeRO-2、ZeRO-3 四张 workflow，固定 BF16 compute 与 FP32 gradient/optimizer 的示例 dtype，显式展示 forward、backward、optimizer、collective payload、owner 和 buffer 生命周期。2026-08-02 的 `1.3.0` 修订把原 SVG 重绘为 TikZ，并将各图统一为“全局 tensor/state -> rank-local ownership 与具体 shape -> local operator -> collective/P2P 的发送者、接收者和合并规则 -> 恢复语义”。`1.2.0` 参考的 [Colossal-AI Parallelism](https://colossalai.org/docs/concepts/paradigms_of_parallelism) 仍只作为视觉组织参考；tensor 关系、成本注释和边界条件来自本领域 canonical Paper/Topic/Evidence 的综合分析，没有复制网页图片，也不把这些整理图作为外部证据。

| Owner | Asset | 用途 | 分辨率 | 声明 | QA |
|---|---|---|---|---|---|
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [普通 DP](../assets/surveys/parallel-partitioning-taxonomy/dp-training-workflow.png) | $K$ 个 micro-batches、BF16 compute、FP32 gradient accumulation、单次 gradient all-reduce、replicated Adam update | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、文字/箭头/dtype/micro-batch/collective 语义 QA，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [ZeRO-1](../assets/surveys/parallel-partitioning-taxonomy/zero1-training-workflow.png) | $K$ 个 micro-batches、完整 local FP32 gradient buffer、gradient reduce-scatter、owner-local Adam、BF16 parameter all-gather | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、文字/箭头/dtype/owner/RS/AG 语义 QA，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [ZeRO-2](../assets/surveys/parallel-partitioning-taxonomy/zero2-training-workflow.png) | FP32 gradient reduce-scatter、owner-local Adam、BF16 parameter all-gather 与 bucket 峰值 | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、文字/箭头/dtype/chunk/collective 语义 QA，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [ZeRO-3](../assets/surveys/parallel-partitioning-taxonomy/zero3-training-workflow.png) | layer-wise BF16 parameter gather、forward/backward buffer 生命周期、FP32 gradient reduce-scatter 与 shard-local optimizer | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、文字/箭头/dtype/lifecycle/collective 语义 QA，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [TP](../assets/surveys/parallel-partitioning-taxonomy/tensor-parallel-block.png) | column-sharded weight -> local GeLU -> row-sharded weight -> partial sum all-reduce | `2400×1350` | 教学整理图 / 非论文证据 | passed after 11-page renumber：原分辨率逐图检查，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [PP](../assets/surveys/parallel-partitioning-taxonomy/pipeline-parallel-schedule.png) | layer ownership、micro-batch activation/gradient P2P 与 fill-drain bubble | `2400×1350` | 教学整理图 / 非论文证据 | passed after 11-page renumber：原分辨率逐图检查，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [EP](../assets/surveys/parallel-partitioning-taxonomy/expert-parallel-routing.png) | token row permutation、variable local shape、A2A dispatch/combine 与 hot rank | `2400×1350` | 教学整理图 / 非论文证据 | passed after 11-page renumber：原分辨率逐图检查，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Megatron SP](../assets/surveys/parallel-partitioning-taxonomy/megatron-sequence-parallel.png) | sequence-sharded non-TP activation、all-gather、TP linear 与 reduce-scatter | `2400×1350` | 教学整理图 / 非论文证据 | passed after 11-page renumber：原分辨率逐图检查，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Ulysses](../assets/surveys/parallel-partitioning-taxonomy/ulysses-layout-transpose.png) | sequence/head ownership transpose、sender chunks、receiver concat 与两次 A2A | `2400×1350` | 教学整理图 / 非论文证据 | passed after 11-page renumber：原分辨率逐图检查，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Ring/CP](../assets/surveys/parallel-partitioning-taxonomy/ring-context-parallel.png) | local Q ownership、rotating KV payload、block attention、online softmax 与 causal imbalance | `2400×1350` | 教学整理图 / 非论文证据 | passed after 11-page renumber：原分辨率逐图检查，2026-08-03 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [CFGP](../assets/surveys/parallel-partitioning-taxonomy/cfg-branch-parallel.png) | condition-axis shard、branch-local output exchange、guidance combine 与复制状态 | `2400×1350` | 教学整理图 / 非论文证据 | passed after 11-page renumber：原分辨率逐图检查，2026-08-03 |
