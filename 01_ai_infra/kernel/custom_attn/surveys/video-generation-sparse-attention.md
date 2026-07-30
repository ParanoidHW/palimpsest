# 视频生成稀疏 Attention：从 Mask 控制面到可执行 Kernel

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[Custom Attention README](../README.md)
> - 上位综述：[Multimodal custom attention](multimodal-custom-attention.md)
> - 跨域模型入口：[Multimodal Generation](../../../../02_model_systems/multimodal_generation/README.md)
> - 选篇与证据：[Selection](../evidence/video-generation-sparse-attention-selection.md) · [Claim matrix](../evidence/video-generation-sparse-attention-claims.md) · [Figure inventory](../evidence/figure-inventory.md)

## 修订信息

- 当前版本：`1.0.0`
- 修订 ID：`rev-video-generation-sparse-attention-20260730`
- 范围：15 篇新增独立精读，Sparse VideoGen 1 作为既有 canonical 谱系锚点。

## 1. 结论先行

视频生成稀疏 Attention 不是单一“删掉低分 token”的算法，而是一条六段式系统链：

1. **mask 来源**：离线校准、规则模板、在线近似、可训练 selector 或路由器；
2. **descriptor/layout**：块索引、3D tile、重排后的连续区间、Monarch 因子或多分支模板；
3. **kernel**：必须让未选块不进入 QK、softmax、PV，而非只在 dense score 上乘零；
4. **control-plane reuse**：复用 mask、centroid、LSE、排列或阈值，避免 selector 抵消稀疏收益；
5. **quantization**：FP8/INT8/INT4 只有与 block layout、缩放和累加路径共同设计才可归因；
6. **distributed/runtime**：训练场景还要处理 head/block 稀疏异质性造成的负载和通信不均。

因此，最可靠的比较单位不是论文声称的“sparsity”，而是：

$$
\text{E2E gain}
=
\text{skipped attention work}
-
\text{selection/reorder/reuse overhead}
-
\text{非 attention 瓶颈}
.
$$

同一保留率可能对应完全不同的可执行性；同一 operator speedup 也不能直接外推到整条生成 pipeline。

## 2. 方法坐标系

### 时间线

- **2025 Q1**：STA、DSV、SpargeAttn、AdaSpa 把规则 tile、训练稀疏、online filtering 与 step reuse 分别建立为独立路线。
- **2025 Q2**：XAttention、VSA、VORTA、Jenga、RainFusion、SVG2、FPSAttention、PAROAttention 集中探索动态 selector、重排、路由、量化与 pipeline 组合。
- **2025 Q4–2026 Q1**：RainFusion2.0、VMonarch、CalibAtt 把重点推进到 NPU 规则块、结构化矩阵与 calibration/compile。
- **方法族锚点**：Sparse VideoGen 1 作为既有 canonical 分析，不重复精读；SVG2 在其上增加 semantic permutation 与 centroid cache。

| 路线 | Mask 来源 | Descriptor / layout | 实际执行 | 控制面复用 | 主要边界 |
|---|---|---|---|---|---|
| [CalibAtt](../papers/calibatt.md) | 离线 calibration，把块分为静态与输入相关集合 | 编译期静态块 + runtime 动态块 | 静态路径预编译，动态块按输入补充 | calibration 结果跨请求复用 | 代码/source 未核验；收益依赖校准分布 |
| [Sliding Tile Attention](../papers/sliding-tile-attention.md) | 规则 3D sliding tile | 连续规则 tile | 专用 tile kernel 跳过窗口外块 | pattern 固定，无在线 selector | 规则性强但适应性有限；kernel 证据强于跨模型结论 |
| [XAttention](../papers/xattention.md) | antidiagonal proxy + dynamic top blocks | block index | selection 后 sparse QK/PV | warmup 后启用；未形成通用 refresh 协议 | proxy 无一般误差界；13.5× 为 operator 级 |
| [VSA](../papers/vsa.md) | coarse attention 产生 row-wise Top-K cube | 3D cube 连续化，细粒度分支仅算选中 cube pair | coarse dense + fine block sparse | 训练/retrofit 学得 selector 与 gate | 离散 Top-K membership 不可微；retrofit 非 training-free |
| [DSV](../papers/dsv.md) | 低秩 Q/K predictor 预测 critical KV | query group + critical KV index | fused estimate/Top-K 与 sparse training kernel | predictor 低频更新 | 稀疏异质性引出 HCP/SCP 负载与通信问题 |
| [FPSAttention](../papers/fpsattention.md) | step-aware 粒度与稀疏/量化联合策略 | 3D block | fused quantized sparse kernel | 去噪阶段共享策略 | source/code 未核验；Hopper/精度格式边界重要 |
| [Sparse VideoGen2](../../../../02_model_systems/multimodal_generation/papers/sparse-videogen2.md) | centroid 近似 + Top-p | semantic permutation 后连续 cluster | dynamic sparse kernel | centroid cache 降低 k-means 开销 | permutation、selector、kernel 收益不能混为一项 |
| [SpargeAttn](../papers/spargeattn.md) | online block prediction + online softmax masking | block mask，warp 内继续判断 PV skip | 可接 FA2/Sage 等后端 | 无离线训练；每次在线判断 | kernel speed 随稀疏率上升，不等同视频 E2E |
| [AdaSpa](../papers/adaspa.md) | warmup precise search + LSE-cached refresh | head-adaptive hierarchical blocks | fused online search 与 block sparse attention | mask/LSE 跨若干 step 复用 | search 间隔与 stale mask 是质量—开销核心 |
| [PAROAttention](../papers/paroattention.md) | 离线 pattern-aware permutation + block mask | 重排后规则块 | sparse QK/PV 与 INT8/INT4 block quant | 后半程共享 mask；排列离线决定 | 论文公式存在符号方向歧义；官方代码未发布 |
| [VMonarch](../papers/vmonarch.md) | 在线迭代更新 Monarch 因子 | 时空结构化 $L,R$ 因子 | 两次较小结构化乘法 | 因子在线更新；首帧重算稳定 | 不是显式 block mask；operator 与 E2E 需分开 |
| [VORTA](../papers/vorta.md) | 条件 embedding 驱动 router | full/sliding/coreset 分支 | 只执行被选 attention branch | router 在 pattern detection 后固定使用 | 需要 router 训练/蒸馏；组合加速含 cache/distillation |
| [Jenga](../../../../02_model_systems/multimodal_generation/papers/jenga.md) | AttenCarve one-shot block mask | 3D latent block + space-filling layout | block-wise attention kernel | mask 一次生成；pipeline 另有 ProRes/timestep skip | 8.83× 属于完整 pipeline，不是 AttenCarve 单项 |
| [RainFusion](../papers/rainfusion.md) | ARM 在线识别 spatial/temporal/textual head | 三类预定义 pattern mask | pattern-specific FlashAttention 路径 | 论文未充分披露 refresh/cache | 无代码；棋盘布局和 ARM overhead 不透明 |
| [RainFusion2.0](../papers/rainfusion-2.md) | block mean + Top-N，显式 first-frame sink | 3D permutation 后规则 block | NPU block-wise sparse path | permutation/sink 静态；动态 Q/K score 应重算 | 只报告单 NPU E2E；动态 mask 刷新协议未披露 |

## 3. Mask 来源：越动态不一定越快

### 3.1 离线、规则与输入相关

- **离线/规则**：CalibAtt 与 STA 把更多工作移到编译或固定布局，selector 开销低，适合结构稳定、硬件编译链明确的部署。
- **在线近似**：XAttention、SVG2、SpargeAttn、AdaSpa、RainFusion 系列通过 pooled score、centroid、LSE 或 pattern classifier 适应输入，但必须证明 selector 没有吃掉省下的矩阵乘。
- **可训练**：VSA、DSV、VORTA 把 selector/predictor/router 纳入训练或微调，能学习动态结构，却不再是零准备成本的 drop-in。
- **结构化替代**：VMonarch 不直接生成离散 mask，而是用可执行的结构化矩阵逼近 full attention；它应与低秩/结构化 operator 比较，而非简单按“保留块比例”排序。

### 3.2 失败模式

动态 selector 常见三类失败：

1. 用完整 $QK^\top$ 才知道哪些块可删，选择成本与 dense attention 同阶；
2. selector 粒度过细，生成不规则索引和 gather/scatter，算术减少但带宽与 launch 增加；
3. mask 在去噪步间变化不大，却每步重算，control plane 成为新瓶颈。

SVG2 的 centroid cache、AdaSpa 的 LSE cache、Jenga 的 one-shot mask 和 HASTE 的 mask reuse 都是在解决第 3 类问题。

## 4. Descriptor 与 layout：稀疏率必须落成可调度对象

硬件友好的共同点是把稀疏决策压缩成少量规则对象：

- STA/VSA/FPSAttention：3D token 先重排为连续 cube/tile；
- SVG2/PARO/RainFusion2：先 permutation，再让语义或局部块在地址上连续；
- XAttention/SpargeAttn/AdaSpa/DSV：保留每个 query block/group 的 KV block index；
- VORTA：descriptor 是分支 ID；
- VMonarch：descriptor 是结构化因子而非布尔 mask。

Permutation 不是免费的。可信结果应计入重排、逆重排、索引构造和 cache 维护；若排列只在 DiT 首尾执行，才有机会被多层、多步摊薄。

## 5. Kernel：什么计算真的被跳过

“应用 mask”至少有四种不同含义：

1. dense score 后置零：几乎不省 QK；
2. QK 跳块、softmax/PV 仍处理大量空块：收益有限；
3. QK 与 PV 都按 block index 跳过：形成真正 sparse attention；
4. selection、quantization、softmax state 与 sparse matmul 融合：减少中间写回与 launch。

STA、XAttention、VSA、DSV、FPSAttention、SpargeAttn 与 PAROAttention都强调第 3–4 类路径，但证据强度不同：有代码或 artifact 的 DSV/XAttention 更适合做实现依据；只有论文图的 FPSAttention、RainFusion 系列应按 paper-reported 处理。

## 6. Control-plane reuse

| 可复用对象 | 代表方法 | 安全边界 |
|---|---|---|
| 静态 block/编译计划 | CalibAtt、STA | 输入分布变化时静态覆盖可能失效 |
| centroid / permutation | SVG2、PARO、RainFusion2 | 聚类或语义布局变化时需刷新 |
| mask | AdaSpa、Jenga、HASTE | stale mask 会漏掉新出现的高质量块 |
| LSE / softmax summary | AdaSpa | 只能作为 search proxy，不能直接替代当前 attention |
| router/pattern choice | VORTA、RainFusion | 需要说明按 head/layer/step 的刷新粒度 |
| structured factors | VMonarch | 迭代更新稳定性与首帧温度异常需单独处理 |

最值得保留的工程原则是：**把 mask 预测视为控制面，把 QK/softmax/PV 视为数据面，分别计时、缓存和验证。**

## 7. Quantization 与稀疏的耦合

FPSAttention 和 PAROAttention 说明，量化不是可随意叠加的独立开关：

- block layout 决定 scale 粒度、访存连续性与 tensor-core tile；
- QK、P、V 的误差敏感性不同，INT4/INT8/FP8 配置不可只报一个“bit width”；
- 稀疏后剩余块可能更重要，量化误差与 selection error 会耦合；
- fused kernel 的收益必须用 matched sparse-only、quant-only、sparse+quant 消融归因。

PAROAttention 提供了较清楚的 matched 表格，但官方代码尚未公开；FPSAttention 的论文结果显示协同收益，source/kernel 细节仍需保守使用。

## 8. 训练与分布式系统

DSV 把问题从单卡推理推进到训练：不同 head/block 的稀疏度不同，使传统 context parallelism 出现两种浪费：

- head context parallelism：不同 GPU 的有效块数量不均，最慢 rank 决定 step；
- sequence context parallelism：全量 gather KV，传输大量最终不会被访问的块。

其 hybrid HCP/SCP 和 selective gather 表明，训练稀疏 Attention 的优化目标不是单一 kernel latency，而是

$$
\max_r \left(T_{\text{compute},r}+T_{\text{comm},r}\right),
$$

必须围绕最慢 rank 的负载与通信联合设计。VSA 的可训练 sparsity 则证明 selector 可进入预训练/retrofit，但 discrete Top-K membership 本身并不会因“端到端训练”自动变为可微。

## 9. 证据解读

### 9.1 不可直接横比的数字

- operator speedup、attention-module speedup、DiT time 与整条视频生成 latency；
- FLOP density、block density、token density 与真正 executed tile 数；
- 480p/720p、不同帧数、不同 GPU/NPU、不同 baseline kernel；
- training-free plugin 与需要训练/微调的 selector/router；
- sparse-only 与叠加 cache、timestep skip、progressive resolution、distillation 的 pipeline。

### 9.2 当前最稳健的结论

1. **规则 tile 是下限基座**：STA 提供了易编译、易测的规则稀疏基线。
2. **动态方法的主战场是 selector amortization**：SVG2、AdaSpa、HASTE、Jenga 都通过复用降低控制面成本。
3. **重排把语义稀疏转成硬件稀疏**：SVG2、PARO、RainFusion2 的关键不是“更稀”，而是让保留块连续。
4. **量化需要 matched ablation**：只有稀疏/量化单项和组合都报告，才能判断协同而非混淆。
5. **训练需要负载与通信重新分配**：DSV 的系统证据不能从单卡推理 kernel 外推得到。
6. **端到端 pipeline 必须拆账**：Jenga 的 8.83× 不能归给 AttenCarve；VORTA 与 cache/distillation 的组合结果同理。

## 10. 采用建议

- **先选 descriptor，再选 selector**：现有 kernel 若只支持规则 tile，优先 STA/重排路线；不要先设计 token-level mask 再期待 kernel 自动高效。
- **建立四级 benchmark**：selector、sparse operator、DiT block、完整生成 pipeline。
- **强制记录硬件与形状**：GPU/NPU、dtype、head dim、序列长度、block size、稀疏率与 warmup。
- **为 reuse 设计刷新协议**：定义缓存对象、作用域、刷新信号、最大陈旧时间和 fallback。
- **把质量验证对齐 dense reference**：同时报告输出指标与 dense-reference PSNR/SSIM/LPIPS，避免随机采样掩盖误差。
- **组合优化逐项消融**：sparse、quant、cache、step skip、resolution schedule 分别测量。

## 11. 谱系与跨域链接

- [Sparse VideoGen](../../../../02_model_systems/multimodal_generation/papers/sparse-videogen.md) 是既有方法族锚点；[Sparse VideoGen2](../../../../02_model_systems/multimodal_generation/papers/sparse-videogen2.md) 以 semantic permutation 与 centroid cache 扩展。
- [RainFusion2.0](../papers/rainfusion-2.md) extends [RainFusion](../papers/rainfusion.md)：从三类 head pattern 的 ARM 路由转向 block-mean/Top-N、3D permutation 与 first-frame sink。
- [Jenga](../../../../02_model_systems/multimodal_generation/papers/jenga.md) 的 canonical owner 位于完整生成 pipeline domain；本 Survey 只解释其 attention primitive 与归因边界。
- HASTE、LVSA 与本专题方法的控制面比较见 [Multimodal custom attention](multimodal-custom-attention.md)。

## 12. 仍待验证的问题

1. 同一模型、同一 kernel、同一 sparsity/质量预算下，STA、XAttention、VSA、SVG2、AdaSpa 的严格 matched comparison；
2. permutation 与 inverse permutation 在长序列、多层、多步中的真实摊销；
3. selector 的 tail latency、临时显存与 CPU/GPU 同步；
4. INT4/FP8 sparse attention 的误差传播与跨 GPU 复现；
5. dynamic sparsity 下 context parallelism 的在线负载预测；
6. GPU 论文结果迁移到 NPU/其他 accelerator 的 descriptor 与 kernel 可移植性。
