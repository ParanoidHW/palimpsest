<!-- Slide number: 1 -->
多模态稀疏 Attention
与定制 Mask Kernel

规则
BlockMask / predicate

索引
CSR / page table
从 mask 语义、稀疏表征到 kernel / planner / KV runtime 的实现趋势

打包
selector -> varlen
内核设计评审版 | 9 篇深读 | CUDA 重点
01

<!-- Slide number: 2 -->
核心判断：不要把可见性先展开成 L x L 张量
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn
完整 dense mask 既浪费内存，也不保证跳过 QK/softmax/AV tile。正确的系统边界是：语义 lowering -> 稀疏 metadata / compact QKV -> kernel plan -> attention run。

01
02
03
能拆矩形
结构化图
动态选择
多次 causal/full varlen 调用
CSR / BlockMask / page table
indices + pack + varlen attention
结论：稀疏的单位应该是 kernel 能跳过的 tile、page 或 compact segment，而非抽象的 0/1 score bias。
02

<!-- Slide number: 3 -->
时间线：从 kernel-aware pattern 到多模态 runtime
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn
2024
2025
2025
2026
2026
MInference
Sparse VideoGen
VMoBA
HASTE / LVSA
Causal-rCM / Cosmos 3

per-head dynamic pattern
spatial / temporal heads
block router + varlen
reuse / CSR + FlashInfer
custom JVP / two-way lowering
2026 的变化不只在更稀疏，而在把动态 mask 的 planner 成本、训练 JVP 和 serving KV 纳入算子接口。
03

<!-- Slide number: 4 -->
多模态 mask：组合可见性，而非单一 causal
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn

block-causal
local + anchor
Token stream
历史 chunk 可读；未来 chunk 禁止。
局部时空窗口加 global/keyframe bridge。

reasoner / text / state

video / audio / action

read-only boundary
within-chunk bidirectional
reasoner 不被 noisy generator 反向污染。
diffusion chunk 内保留去噪互动。

noisy diffusion chunk

keyframe / reference
可见性条件若在 block/tile 层可判定，就传 rule / metadata；若不可判定，先 lowering 或 selector。
04

<!-- Slide number: 5 -->
四种实现路径：kernel 看到的不是同一个“mask”
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn

规则 / BlockMask
CSR / block plan
selector / pack
dense bias fallback
Causal-rCM
FlexAttention
LVSA
FlashInfer
VMoBA
Token Sparse
FrameDiT 公开代码
SDPA/Diffusers
block schedule + predicate
可跳过 block
indptr + indices
plan 后遍历 nnz tile
indices + cu_seqlens
compact QKV
bool/bias broadcast
通常仍遍历 dense tile
审查点：metadata 的大小是否为 O(nnz_blocks)？kernel grid 是否真的只遍历非零 tile？
05

<!-- Slide number: 6 -->
LVSA：CPU 保留 CSR metadata，FlashInfer 消费计划
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn

geometry
window + rotating anchors
CPU CSR
int32 indptr / indices
FlashInfer plan
block traversal
GPU run
skip unlisted tile
->
->
->
源码证据：`ring_block_frame_csr` 返回 int32 CSR；`ensure_device()` 刻意不移动 fi_indptr / fi_indices，由 host builder 与 FlashInfer planning pass 消费。

为何这比 dense mask 可扩展
metadata 从 O(L^2) 改为 O(nnz_blocks + n_rows)，但需计入 planner、CSR 复制与非连续 KV 访存。
06

<!-- Slide number: 7 -->
Causal-rCM：custom mask 是 JVP operator contract
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn

BlockPattern + AttnMaskSpec
Flex BlockMask / JVP Triton
Packed stream
frame-token geometry、chunk、sliding window、sink、offset；不是 L x L 张量。
同一 teacher-forcing mask 进入 primal 与 JVP；错误的后处理 mask 不等价。

clean block 0

clean block 1

KV cache + CP

noisy block 0
同一模式覆盖 packed training、replay、inference；对齐和负载均衡仍是成本。

noisy block 1
把“mask 支持”当作 forward-only feature 会漏掉 backward/JVP、cache 与 sequence parallel 的系统合同。
07

<!-- Slide number: 8 -->
统一模型：先进行语义 lowering，再考虑 sparse kernel
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn

Cosmos 3 two-way flat attention
通用 FlexAttention
一个混合 mask

semantic
lowering
reasoner causal varlen call
正确但 kernel 对双流结构不透明
可能做 padding-equivalent work

generator full varlen call
本地论文材料：相对 FlexAttention baseline，Nano 训练吞吐 +22%。
08

<!-- Slide number: 9 -->
长序列：CPU 可以规划稀疏，但不能输出 dense mask
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn
场景
生成位置
传递对象
执行要点

静态几何
CPU 初始化 / cache
CSR / page table
异步 H2D 或 runtime plan

每请求 KV 选择
GPU selector 为主
selected pages / indptr
paged attention

每 step 小变化
reuse + delta
cached metadata
减少 planner 次数

每 token top-k
GPU
indices + compact QKV
避免 PCIe 往返
禁止路径：CPU 生成 [L,L] bool/fp16 mask 再拷 GPU。它具有 O(L²) 内存、PCIe 传输与同步三重成本。
09

<!-- Slide number: 10 -->
实现建议：接口、指标与质量守护
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn

接口
性能模型
正确性
MaskSpec(kind, geometry, dynamic, storage)
plan(spec, layout, device) -> Plan
run(q,k,v,Plan) -> o
T = T_select + T_pack + T_plan + T_attn + T_unpack
测有效带宽、tile occupancy、nnz 曲线。
dense reference、JVP/backward、chunk 边界、cache reuse；不要只验证 forward。

视频
motion / identity / loop
跨模态
audio-action sync / grounding
服务
TTFT / TPOT / mixed batch
10

<!-- Slide number: 11 -->
最终建议：让 mask 的语义在正确层级消失或变小
2026-07-10 | NVIDIA CUDA | 证据包：_artifacts/ai_algorithm_survey_multimodal_custom_attn

能拆就拆
双流/矩形可见性 -> causal/full varlen calls
1

需稀疏就索引化
window/anchor -> CSR / BlockMask / page table
2

需动态就打包
router/selector -> GPU indices + compact QKV
3

把控制面纳入 KPI
planner、H2D、top-k、pack/unpack 与 attention 同测
4
最终文件：01_ai_infra/kernel/custom_attn/ 多模态稀疏Attention与定制Mask_Kernel调研.md / .pptx
11
