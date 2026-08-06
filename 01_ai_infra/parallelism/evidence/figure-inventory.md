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

以下 11 张 PNG 全部由 [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) 独占，使用 TikZ 排版；除 Ring/CP 为收紧画幅后的 `2100×1125` 外，其余以 `2400×1350` 输出。它们是 analysis-derived 教学整理图，不是原论文 Figure/Table，不计入论文视觉证据数量。DP、ZeRO-1/2/3、TP、EP、PP、Megatron-SP、Ulysses 与 Ring/CP 的可编辑源码作为[独立辅佐材料](../supplements/parallel-partitioning-diagram-sources/README.md)维护；PDF、过程渲染、contact sheet 与像素检查仍只保留在 process workspace。

2026-08-05 的 `1.10.3` 修订刷新 Megatron-SP、Ulysses 与 Ring/CP：SP/Ulysses 对齐层级操作粒度、residual 路径和 $N/D/H$ 符号，Ulysses 直接突出 sequence shard → head shard → sequence shard 的两次 A2A ownership 转换；Ring 将 rank-local attention 作为主链，把邻居 P2P 放在 KV 输入旁并显式连接，使用 $\sigma_j$ 表示逐块合并状态，同时把画幅收紧为 `2100×1125`。三张图均删除制作过程式标题和核心区域中的冗长解释，并由独立 subagent 对最终原分辨率 raster 与全部 QA crops 复审通过。2026-08-04 的 `1.10.2` 修订把 PP 时间轴明确为 GPipe 全前向/全反向排程，以 BWD 约为 FWD 两倍的时间粒度重画连续计算块，并加入常见训练实现中的跨 stage global-norm barrier 与对齐 optimizer step；同时删除过密的通用本地状态更新链。`1.10.1` 修订纠正 PP 的 backward 拓扑：loss 仅进入最后一个 stage，activation gradient 再按 stage 3 → 2 → 1 → 0 逐边界 P2P 返回；同时显式增加各 stage 本地 weight、gradient、optimizer state 与 update 的交互链。`1.10.0` 修订把 PP、SP、Ulysses、Ring/CP 与 CFGP 补齐到同一 semantic visual grammar：蓝色只表示 tensor/weight，绿色只表示 model compute，橙色表示 collective/P2P，紫色表示 rank-local persistent state，灰色表示 runtime action。PP 分开表示 stage 参数 ownership、单个 micro-batch 的 forward/backward P2P 与 fill-drain 时间轴；SP 显式展示 AG/RS 两侧的 activation ownership 生命周期；Ulysses 保留 sender chunk、receiver concat 与双向 layout transpose；Ring/CP 把固定 $Q$、轮转 KV、online-softmax state、环形 P2P 和 causal imbalance 分层；CFGP 分开显示并行 branches、复制模型状态、branch-output exchange 和 guidance combine。五张图均参数化 world size $p$ 与 illustrated rank $r$，并移除会把 rank 颜色误当节点类型、让箭头穿过状态框或让节点超出画布的旧表达。`1.9.0` 修订统一普通 DP、ZeRO-1/2/3、TP 与 EP 的 tensor-flow 视觉语法：保留输入、输出、当前 micro-batch、ownership 和持久状态等有独立语义的框；其余中间 tensor 改为主箭头附近的蓝色标注，并让细引线与主 flow 保持间距。ZeRO 图保留有助于表达顺序执行的 $m_k$，且 all-gather 输出到计算使用单根完整橙色箭头，避免拼接成多色箭头。TP/EP 按 pre-norm layer 粒度展开，`Norm` 不绑定具体归一化实现；residual shortcut 用独立蓝色虚线，TP 以纵/横条纹区分 column/row split 并显式展示本 rank weight shard，EP 采用单向处理链和 expert ownership 条带。`1.8.0` 将普通 DP 与 ZeRO-1/2/3 更新为框架中立的方法机制图：sampler 与 async release 使用独立 runtime-action 语义；weight、gradient 与 optimizer state 显式展示 ownership；ZeRO-2 删除 bucket 等实现优化；ZeRO-3 用 `MODEL LAYERS × L` 标出 layer-local 重复范围，并把 temporary BF16 weight、FWD/BWD 输入依赖和异步 release 侧支画入 workflow。原理图的可见区域不再包含 framework、commit、配置或源码符号。`1.7.0` 修订用每 rank 单条时间线替换 `1.6.0` 的并列支路，使 micro-batch 顺序由箭头拓扑显式表达。`1.6.0` 曾显式列出 $m_1$、$m_2$、$m_K$ 及累计状态，但并列布局容易被误读为同一 rank 内并发，现已替换。`1.5.0` 将 ZeRO-1 修正为 gradient reduce-scatter、owner-local update 和 parameter all-gather。`1.4.0` 修订把 DP/ZeRO 汇总图拆成普通 DP、ZeRO-1、ZeRO-2、ZeRO-3 四张 workflow。2026-08-02 的 `1.3.0` 修订把原 SVG 重绘为 TikZ。`1.2.0` 参考的 [Colossal-AI Parallelism](https://colossalai.org/docs/concepts/paradigms_of_parallelism) 只作为视觉组织参考；tensor 关系、成本注释和边界条件来自本领域 canonical Paper/Topic/Evidence 的综合分析。

| Owner | Asset | 用途 | 分辨率 | 声明 | QA |
|---|---|---|---|---|---|
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [普通 DP](../assets/surveys/parallel-partitioning-taxonomy/dp-training-workflow.png) | 顺序执行 $K$ 个 micro-batches；显式 `m_1 → current m_k → model FWD` dequeue 链；箭头标注 BF16 activation、FP32 gradient contribution 与 accumulation；单次 gradient all-reduce 后执行 replicated optimizer update | `2400×1350` | 教学整理图 / 非论文证据 | passed：独立 subagent 原分辨率 full/main/footer crops 复审；current $m_k$、顺序回接、dtype/micro-batch/collective/ownership、箭头端点与图例 QA，2026-08-05 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [ZeRO-1](../assets/surveys/parallel-partitioning-taxonomy/zero1-training-workflow.png) | 保留当前 $m_k$；完整 local FP32 gradient accumulation、gradient reduce-scatter、owner-local optimizer、BF16 parameter all-gather | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、tensor callout、框架中立可见内容、owner/RS/AG 语义 QA，2026-08-04 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [ZeRO-2](../assets/surveys/parallel-partitioning-taxonomy/zero2-training-workflow.png) | 保留当前 $m_k$；每个 micro-batch 的 FP32 gradient reduce-scatter、owner-shard accumulation、owner-local optimizer 与 BF16 parameter all-gather | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、无 bucket 实现细节、分支箭头/tensor callout/ownership/collective 语义 QA，2026-08-04 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [ZeRO-3](../assets/surveys/parallel-partitioning-taxonomy/zero3-training-workflow.png) | `MODEL LAYERS × L`、temporary BF16 weight callout、FWD/BWD 输入依赖、异步 release 侧支、gradient reduce-scatter 与 shard-local optimizer | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、无文字覆盖、单根 all-gather 输入箭头、lifecycle/ownership/collective 频率 QA，2026-08-04 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [TP](../assets/surveys/parallel-partitioning-taxonomy/tensor-parallel-block.png) | pre-norm attention/FFN layer；$[B,S,H]$ tensor flow；column/row 条纹、rank-local weight ownership、partial all-reduce、residual shortcuts 与 panel 内 $X_{attn}[B,S,H]$ callout | `2400×1350` | 教学整理图 / 非论文证据 | passed：独立 subagent 原分辨率 full/main/footer crops 复审；$N/D/H$、weight shard/shape/collective、callout 归属、shortcut 分离、箭头端点与图例 QA，2026-08-05 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [PP](../assets/surveys/parallel-partitioning-taxonomy/pipeline-parallel-schedule.png) | stage ownership、loss 从末级启动并逐边界返回的 activation-gradient P2P、GPipe 全前向/全反向时间轴、global-norm barrier 与对齐 optimizer step | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、loss → stage 3 → 2 → 1 → 0 backward 拓扑、FWD/BWD 时间粒度、global-norm barrier、P2P/ownership/bubble 语义 QA，2026-08-04 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [EP](../assets/surveys/parallel-partitioning-taxonomy/expert-parallel-routing.png) | pre-norm MoE layer 单向执行链；箭头标注 token layout；A2A dispatch/return、local expert FFN、residual shortcut 与 expert weight ownership | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX、原分辨率逐图检查、flow 顺序、tensor callout 间距、shortcut/ownership/A2A 语义 QA，2026-08-04 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Megatron SP](../assets/surveys/parallel-partitioning-taxonomy/megatron-sequence-parallel.png) | pre-norm attention/FFN 主链；AG/RS 切换 $S/p\leftrightarrow S$ activation ownership；TP partial、独立 output projection 与两条 residual shortcut | `2400×1350` | 教学整理图 / 非论文证据 | passed：独立 subagent 原分辨率全图与 main/ownership/footer crops 复审；标题、$N/D/H$、weight shard、AG/RS、residual 与箭头端点 QA，2026-08-05 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Ulysses](../assets/surveys/parallel-partitioning-taxonomy/ulysses-layout-transpose.png) | sequence shard → head shard → sequence shard；两次 A2A、local attention、独立 output projection、$X_{attn,r}$ 与两条 residual shortcut | `2400×1350` | 教学整理图 / 非论文证据 | passed：独立 subagent 原分辨率全图与 main/layout/footer crops 复审；标题、$N/D/H$、no-sum A2A、shape、箭头端点与文本归属 QA，2026-08-05 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [Ring/CP](../assets/surveys/parallel-partitioning-taxonomy/ring-context-parallel.png) | rank $r$ 固定 $Q_r$；当前 $K_j,V_j$ 驱动 block attention；$\sigma_j$ 逐块合并；邻居 P2P 轮换 KV | `2100×1125` | 教学整理图 / 非论文证据 | passed：独立 subagent 原分辨率全图与 compute/P2P/state/footer crops 复审；通信 sender/receiver、非零 shaft、KV shape、文本归属、居中与留白 QA，2026-08-05 |
| [并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md) | [CFGP](../assets/surveys/parallel-partitioning-taxonomy/cfg-branch-parallel.png) | peer-ranks 视角下，$r_0$/$r_1$ 分别执行 conditional/unconditional forward；两份输出经 all-gather 后做 guidance combine，沿 $x_tightarrow x_{t-1}$ 进入下一 denoising step；图内显式解释 $x_t,t,c/emptyset,epsilon_c/epsilon_u,w,P,mathcal C_c/mathcal C_u$ | `2400×1350` | 教学整理图 / 非论文证据 | passed：LuaLaTeX；独立 subagent `ring_visual_qa` 按 status request `4-1de79469377b` 检查 full frame 与 5 个原始像素 crops，`verify` 通过；all-gather 载荷/收发、branch 对称性、ownership、迭代回边、箭头端点、孤立文本、行距与居中 QA，2026-08-06 |
