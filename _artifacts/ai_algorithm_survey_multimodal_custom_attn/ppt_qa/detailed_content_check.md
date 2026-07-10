<!-- Slide number: 1 -->
多模态稀疏 Attention
与定制 Mask Kernel
从论文图示、核心机制到 mask lowering、kernel metadata 与 host-device 数据流

high-resolution VLM token selection
理解

two-way stream lowering / special causal
统一

window, CSR, router, temporal reuse
生成
10 篇代表工作 | 原论文图已嵌入 | 代码证据与推断严格区分
01

<!-- Slide number: 2 -->
如何读本报告：一张图必须落到一个可执行对象
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

任务与 token 拓扑
可见性语义
lowering
kernel 与 runtime
->
->
->
text / patch / frame / action / chunk
causal / local / anchor / read-only
varlen call / BlockMask / CSR / pack
tile traversal / plan / KV / CP
每篇均回答：解决什么问题？图中 token/block 是什么？mask 怎样表示？kernel 到底跳过了什么？哪部分只有论文证据？

读图规则
论文图说明算法语义；源码路径说明 runtime 真正接收什么；性能图只能支持其报告设置，不能自动归因给单个 kernel。
02

<!-- Slide number: 3 -->
领域图谱：mask 不再只是一个 score bias
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

Causal-rCM / Cosmos 3
block schedule, stream split
BlockMask / varlen calls
规则型

LVSA
CSR indptr + indices
FlashInfer planning
索引型

VMoBA / TSA / VLM FlexAttn
index set + compact QKV
FlashAttention varlen
选择型

FrameDiT
frame-level matrix representation
不生成 token-pair mask
替代型
系统趋势：将“可见性”保留为规则、索引或紧凑序列，直到 kernel plan；禁止在模型脚本侧先 materialize L x L。
03

<!-- Slide number: 4 -->
理解侧：FlexAttention VLM 的高分辨率 token selection
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

解决的问题

![fig2_hierarchical_vlm_selection_caption.png](Picture4.jpg)
所有 high-resolution patch 与文本一起全注意力，分辨率升高时 decoder 成本失控。

图中机制
低分辨率/文本先给全局语义；attention map 选出高分辨率区域 token，再进 hierarchical self-attention。

实现 / kernel 含义
selected indices -> gather high-res feature -> compact attention。具体 CUDA backend 本次未逐行核验，不能把方法名等同 PyTorch FlexAttention。
04
Paper Fig.2, arXiv:2407.20228; official UMass repository

<!-- Slide number: 5 -->
统一模型：Cosmos 3 将混合 mask 降低为两个 varlen 调用
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![two_way_attention_infra.png](Picture4.jpg)
解决的问题
reasoner 必须 causal 且不受 noisy generator 污染；generator 又必须读同样本 reasoner + 自身 token。

图中机制
reasoner: causal self-attention；generator: bidirectional attention over [reasoner, generator]。按 sample 打包，避免跨样本 read。

实现 / kernel 含义
先 semantic lowering 为 causal/full 两次调用。论文材料报告相对 FlexAttention baseline 的 Nano training throughput +22%，Hopper FA3、GB200 NATTEN/CUTLASS。
05
Cosmos 3 local source: two-way attention infrastructure

<!-- Slide number: 6 -->
流式世界模型：Causal-rCM 的 special causal mask
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![fig3_causal_training_paradigms_caption.png](Picture4.jpg)

解决的问题
AR diffusion 的 TF 需要 clean history + noisy target；SF 又需 self-generated rollout 与 KV cache。普通三角 causal mask 不够。

图中机制
图中 TF / DF / SF 区分 clean、noisy、self-generated history；noisy block 只读允许的 clean history 与自身 block。

实现 / kernel 含义
BlockPattern + AttnMaskSpec -> Flex BlockMask / range metadata；同一 mask 进入 primal 和 JVP Triton kernel。Magi backward 限制需单独核验。
06
Causal-rCM Fig.3; code commit ed3cb14

<!-- Slide number: 7 -->
长视频：LVSA 用 window + rotating anchors 保持稀疏预算
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![fig1_expanded_window_caption.png](Picture4.jpg)

解决的问题
固定 window 会漏长程依赖；window 与 global anchor 重叠又浪费固定 attention budget。

图中机制
expanded local window 与 periodic global frames 构成 A(t)=G union W(t)，每个 query frame 近似保持相同 attended set 大小。

实现 / kernel 含义
frame-block CSR int32 indptr/indices；FlashInfer BlockSparseAttentionWrapper 跳过未列 tile。CPU planner 留 metadata 在 host，并非 GPU kernel 直接读 CPU RAM。
07
LVSA Fig.1; code commit 1ebcc92

<!-- Slide number: 8 -->
学习式 block router：VMoBA 的 partition -> select -> varlen
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

解决的问题

![fig2_vmoba_pipeline_caption.png](Picture4.jpg)
一维均匀 MoBA block 与视频 temporal/spatial/3D 邻域不匹配；固定 top-k 也浪费异质 head 预算。

图中机制
recurrent 1D/2D/3D partition，mean key 产生 block score；global/threshold selection 后仅在选中 blocks attention。

实现 / kernel 含义
GPU gate + topk/threshold -> nonzero -> gather QKV -> cu_seqlens -> FlashAttention varlen。控制面为 gate/sort/pack/LSE，不传 CSR 或 pair-mask。
08
VMoBA Fig.2; code commit 48aaccd

<!-- Slide number: 9 -->
动态控制面：HASTE 的 mask reuse 与 head-wise calibration
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![fig4_tmr_ebc_framework_caption.png](Picture4.jpg)
解决的问题
Video DiT 要多 step denoise；逐 head、逐 step 重算 sparse mask 可能吃掉 attention 节省，统一 threshold 又不公平。

图中机制
TMR 用 Q/K drift 判断每个 head 复用还是刷新 cached descriptor；EBC 用离线 error curve 分配 head-specific threshold。

实现 / kernel 含义
应缓存 sparse descriptor，而非 N x N mask。官方代码未取得，CSR/BlockMask/host-device placement 不可断言；机制与结果为 PDF-only。
09
HASTE Fig.4, arXiv:2605.14513

<!-- Slide number: 10 -->
Training-free 视频：Sparse VideoGen 的 spatial / temporal head dispatch
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![fig4_svg_workflow_caption.png](Picture4.jpg)
解决的问题
Video DiT 3D full attention 成为主成本；直接移植 LLM mask 会丢 temporal dependency。

图中机制
sampled rows 对 spatial / temporal / full attention 做 MSE 近似，按 head dispatch 到专用 pattern。

实现 / kernel 含义
关键不只是找 pattern：temporal slash 必须 layout transform 才能有 coalesced tile access。论文称 Triton/FlashInfer prototype，具体 metadata 本次未有源码核验。
10
Sparse VideoGen Fig.4, arXiv:2502.01776

<!-- Slide number: 11 -->
Token Sparse Attention：保留 selector 灵活性，复用成熟 kernel
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![fig3_compress_attention_scatter_caption.png](Picture4.jpg)
解决的问题
block sparse 粒度高效但 token importance 随 layer/head 变化；永久 drop token 会妨碍后续层重新选择。

图中机制
per-head select token subset；compress Q/K/V；在 compact tensors attention；scatter output back 后叠加 residual。

实现 / kernel 含义
kernel 只见连续 compact QKV，可复用 FlashAttention；真实成本为 selector + gather/contiguous + scatter。实现细节为 PDF-only。
11
Token Sparse Attention Fig.3, arXiv:2602.03216

<!-- Slide number: 12 -->
长上下文桥接：MInference 的 pattern-aware index 与 kernel dispatch
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![fig3_sparse_patterns_caption.png](Picture4.jpg)
解决的问题
prefill attention 延迟主导；固定 top-k index 跨 prompt recall 显著下降。

图中机制
离线给 head 选 A-shape / vertical-slash / block-sparse family；在线建立具体 ranges/columns/blocks。

实现 / kernel 含义
pattern-specific index 交给 PIT/Triton/FlashAttention 类 kernel。迁移到 video 必须改为双向时空 pattern，并处理每 step 的 planner 成本。
12
MInference Fig.3, NeurIPS 2024 Spotlight

<!-- Slide number: 13 -->
架构替代：FrameDiT 以 matrix attention 改变 temporal topology
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

解决的问题

![fig1_matrix_attention_architecture_caption.png](Picture4.jpg)
full 3D attention 表达强但昂贵；local factorized attention 便宜却错过大运动。

图中机制
以 frame matrix 为对象做 temporal Matrix Attention，Global-Local hybrid 保留局部路径，不再构造原 token-pair temporal mask。

实现 / kernel 含义
公开代码仍把 2D mask 转为 -10000 dense bias 并 broadcast；论文算法收益不自动等于 custom sparse kernel。
13
FrameDiT Fig.1, CVPR 2026 Findings; code commit 359bd12

<!-- Slide number: 14 -->
两条“真正下沉到 runtime”的路径：规则与 CSR
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

![table1_fig4_scaling_caption.png](Picture6.jpg)

![fig4_recipe_comparison_caption.png](Picture4.jpg)

Causal-rCM：规则型
LVSA：索引型
BlockPattern 让 kernel/BlockMask 按 block id 判定 visibility；同一规则覆盖 TF、JVP、cache。
CSR 与 compact layout 交给 FlashInfer planning；图表说明长 horizon/80GB 情况，但不可跨模型横比。
14
Causal-rCM Fig.4; LVSA Table 1 + Fig.4

<!-- Slide number: 15 -->
定制 mask 的四种表达：什么能真正跳过 tile？
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

Rule / BlockMask
CSR / page table
Selected segments
Dense bias
block id, window, stream, offset
indptr, indices, page id
indices, cu_seqlens, compact QKV
bool / -inf score bias
Causal-rCM
LVSA
VMoBA / TSA / VLM
FrameDiT public code
kernel/compiler 可判定 tile
scheduler 只遍历 nnz block
标准 varlen kernel
通常不跳 tile
成本：规则须 block-aligned
成本：plan / locality
成本：pack/unpack
成本：L² / dense work
15
Cross-paper implementation synthesis

<!-- Slide number: 16 -->
长序列 host-device 数据流：传 metadata，不传 dense pair mask
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

CPU static planner
GPU dynamic selector
Plan / pack
Attention kernel
->
->
->
geometry / cache
CSR int32
Q/K drift / top-k
indices
page plan / compact QKV
cu_seqlens
only nnz tiles /
compact sequence

允许
禁止
静态 window/anchor：CPU 一次性 CSR、pinned metadata、FlashInfer plan；每 request 的 page list 也可由 host scheduler 供给。
CPU 生成 L x L bool/fp16 mask 再拷 GPU。64K 单 bool mask 已 4GiB；per-step top-k CPU 往返还会同步 pipeline。
16
Direct code evidence: LVSA sparse_attention.py:275-304, 598-607

<!-- Slide number: 17 -->
建议的实现边界：先 lowering，再选 kernel
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

MaskSemantics: stream partition + temporal geometry + dynamic source

A. rectangles
B. regular graph
C. explicit graph
D. dynamic selection
split into causal/full varlen calls
BlockMask / predicate
CSR/page metadata + plan
gather + compact varlen
build_attention_plan(spec, qkv_layout, device) -> Plan
attention_run(q, k, v, Plan) -> out

评测公式
Ttotal = Tselect + Tmetadata + TH2D/plan + Tpack + Tattn + Tunpack。只报 attention FLOPs 会遗漏控制面和数据搬运。
17

<!-- Slide number: 18 -->
结论：让 mask 的语义在正确层级消失或变小
图文精读版 | 2026-07-10 | NVIDIA CUDA 重点

能拆就拆
双流 / 矩形可见性 -> causal/full varlen calls
1

需稀疏就索引化
window/anchor -> CSR / BlockMask / page table
2

需动态就紧凑化
router/selector -> GPU indices + compact QKV
3

控制面也是性能
planner、H2D、top-k、pack/unpack 必须和 attention 同测
4
完整图文精读、PDF/source、代码 commit、图清单与 QA：_artifacts/ai_algorithm_survey_multimodal_custom_attn
18
