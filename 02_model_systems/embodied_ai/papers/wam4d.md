# WAM4D

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[具身智能模型演进、Infra 与端云协同](../surveys/embodied-ai-evolution-infra.md)
> - 证据资产：`../assets/papers/wam4d/`
> - 相关文档：[论文索引](../evidence/paper-index.md)、[图表清单](../evidence/figure-inventory.md)

论文：[arXiv:2606.14048](https://arxiv.org/abs/2606.14048)。论文作者给出 [myendless1/wam4d](https://github.com/myendless1/wam4d) 仓库入口，但本次未获得可固定的实现 commit；PDF、提取文本与图表审计过程保留于审计区。

## 论文资料

- 领域：具身 AI、world action model、机器人操作、4D 几何建模。
- 论文：Ying Li 等，*WAM4D: Fast 4D World Action Model via Spatial Register Tokens*，arXiv:2606.14048v3，2026-07-07 online / PDF 标注 2026-07-08；arXiv-only。
- 核心问题：2D/latent WAM 的视频外观可能物理合理但几何和接触不一致；显式 dense 4D 解码又会拖慢动作生成。
- 目标：用训练时几何监督塑造 action 所用的历史视频特征，部署时保持轻量 observation-to-action 路径。
- 关键假设：未来深度能由历史视频特征通过 registers 读取；因果可见性可阻止未来泄漏；几何 branch 可完全去除而保留策略收益。

## 核心机制与贡献

1. spatial registers：以未来时间 × 三视图 mosaic 网格复制出的 960 个查询读取历史视频特征，连接预训练几何先验与 WAM hidden state（Eq. (6)-(8)，Fig. 2）。
2. causal mixture attention：future action 只能看历史视频、历史动作和自身加噪 action；register 只能看 register 和历史视频（§3.3、Fig. 2），避免 geometry/future-video shortcut。
3. trainable pretrained DA3 head + SmoothL1 depth loss：在共享 video-action backbone 上增加几何监督（Eq. (9)-(10)、Table 8）。
4. 训练/部署解耦：部署去掉 registers、DepthBlocks、投影层和 geometric head，仅保留 video-action action generation（§3.3、Algorithm 1、§4.7）。
5. 评测覆盖 RoboTwin 2.0、AstriBot S1 四类真实操作和 10-task ablations；报告 SR、视频/深度/点云质量、latency 和 VRAM（Tables 1-9）。

## 方法与实现

### 3.1 问题到方案的逻辑链

2D rollout 隐藏接触几何 -> dense 4D inference 成本高 -> registers 只在训练时从 history video 查询 future depth -> depth loss 更新共享特征 -> causal MoT 阻止 future tokens 反向泄漏 -> inference 删除 geometry branch，保留 action-only path。

### 3.2 设计动机与具体问题映射

| 设计项 | why 状态/来源 | 针对的具体问题 | 因果机制 | 替代方案/权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|
| spatial registers 读取 history video | author-stated（§1、§3.2） | dense 4D inference 慢；2D latent 缺少接触/遮挡几何 | query 只读取 history features，深度误差反传到 action 所用特征 | 直接预测 RGB-D/未来 VAE depth；register 额外训练算力和激活 | Table 7 interface 对比；Table 6/8 geometry metrics | 部分支持：几何质量改善，训练成本未量化 |
| causal mixture visibility | author-stated（§3.3） | future video/geometry 可能形成 non-causal shortcut | action queries 禁止 future video/register；register 不进入 policy path | bidirectional register visibility；更密集全注意力会增加信息/算力 | Table 7 bidirectional 行是 confounded（层位也改变）；无独立 mask-only ablation | 部分支持/未完全隔离 |
| SmoothL1 future-depth loss | author-stated（§3.4） | action-only supervision 对空间结构弱 | 有效像素平均的深度误差塑造 shared video hidden | 其他 depth loss 或无深度；没有 loss-type sweep | No-depth vs register rows；Table 8 | 部分支持，不能分离 loss 类型贡献 |
| trainable pretrained DA3 head | author-stated（§4.4.3） | 普通 depth head 不能提供强几何先验；fixed head 不能适配 | 预训练初始化提供 prior，继续训练适配机器人域 | random-init / fixed-pretrained | Table 8：Train. DA3 80.1/75.4 clean/random SR，geometry 指标最佳 | 直接支持相对两种 head 设置 |
| middle register layers 12/14/16/18 | author-stated + inferred（§4.4.2） | 早层/晚层在视觉去噪与几何抽象间有冲突 | 中间层在视觉结构和几何抽象间平衡 | shallow/deep/uniform/bidirectional | Table 7；middle 的 AbsRel 0.053、F-score 0.685、F-score-T 0.825，控制 SR 75.2 | 部分支持；多指标 trade-off，不是单一最佳 |
| three-view mosaic/register grid | author-stated geometry alignment（§3.2、§3.5） | 多相机特征与深度像素需要空间对应 | 32x32 输入 cell 对齐到 12x10 grid，每 8 future frames 共 960 registers | 直接用全局 latent 或单视角 query；register 数量增加训练显存 | §3.5 的结构说明；无 grid-size sweep | 机制合理但未独立验证 |
| deployment branch removal + KV cache | author-stated（§3.3、Algorithm 1、§4.7） | 几何解码拖慢 causal action | 删除 R/DepthBlocks/$P_g$/$G_\phi$，仅编码 observation queue、更新 video/action KV cache | 保留 geometry 做 closed-loop rollout；会更重但可输出 depth | Table 9 absolute latency/VRAM；无 branch on/off matched pair | latency 结果支持部署可行性，不支持因果加速量 |

### 3.3 模型/系统架构

![Figure 2 WAM4D architecture and causal visibility pattern](../assets/papers/wam4d/fig2-wam4d-architecture-causal-visibility-caption.png)

Fig. 2 的左侧把 history RGB/actions 输入 30 层 video-action MoT；register 支路在若干层读取 history video，经四个 DepthBlocks 和预训练几何头得到 future depth。右侧的 VA self-attention 使 future action 只能看历史视频/历史动作/自身 action noise；Depth cross-attention 使 geometry query 读取合法历史上下文。图示是机制证据，不等价于实现了稀疏或融合 attention kernel。

### 3.4 训练/推理边界：哪些张量和算子留下

| 对象 | 训练 | 默认 inference | 证据/判断 |
|---|---|---|---|
| learnable spatial register grid $R^\star$、复制后的 $R_t^0$、960 register tokens | 存在，按未来时间和 mosaic 坐标复制 | 移除，不进入 action KV cache | §3.2、§3.5、§4.7（直接） |
| DepthBlock 1-4，层 12/14/16/18 cross-attention | 存在，Q=register，K/V=register+history video | 移除 | Eq. (7)、Fig. 2、§4.7（直接） |
| 四个 linear adapters $P_g$ 与 DA3-GIANT-1.1 DualDPT head $G_\phi$ | 存在；最终 head 为 trainable pretrained | 移除 | Eq. (8)、Table 8、§4.7（直接） |
| future depth $\hat D$、$\mathcal L_{depth}$、pseudo-depth target | 训练监督和反传 | 不生成、不缓存 | Eq. (9)-(10)、Algorithm 1（直接） |
| shared video-action MoT 参数（含被深度损失塑形后的 history features） | 更新 | 保留 | §1、§3.2（直接）；“几何先验以权重形式留下”是跨段落推导 |
| VAE、history RGB latent、history-action embedding、future action denoising、action head、text cross-attention、KV cache | 存在 | 保留 | §3.5、Algorithm 1（直接） |
| future video flow path | 训练有未来 video noise 和 $ℒ_{video}$ | Algorithm 1 只写 action prediction；部署 geometry branch 明确移除 | 部署是否仍运行 video generation 未被代码核验；不得把未报告路径当作事实 |

因此，“4D”是训练期几何塑形和可选 qualitative rollout 能力，不是部署时持久的 dense 4D tensor。推理端留下的是被 geometry loss 影响过的 video-action 参数和普通 observation/action cache；这是由 §1、§3.3 和 §4.7 共同推出的 derived interpretation。

### 3.5 关键公式

主干 token 序列和 register 更新为：

$$X_t^{(0)}=[Z_t^{hist},\tilde Z_t^{fut},A_t^{hist},\tilde A_t^{fut}],\qquad
R_t^{\ell+1}=\operatorname{DepthBlock}_\ell(Q=R_t^\ell,K,V=[R_t^\ell,Z_t^{hist,\ell}]).$$

深度读出和目标为：

$$G_t=P_g(\{R_t^{\ell+1}\}_{\ell\in\mathcal L_r}),\qquad \hat D_t^{fut}=G_\phi(G_t),$$

$$\mathcal L_{depth}=\frac{1}{\sum_{\tau\in T_t}|\Omega_\tau|}\sum_{\tau\in T_t}\sum_{p\in\Omega_\tau}
\operatorname{SmoothL1}(\hat D_{\tau,p},D_{\tau,p}),$$

$$\mathcal L=\mathcal L_{video}+\lambda_{act}\mathcal L_{action}+\lambda_{depth}\mathcal L_{depth},\qquad \lambda_{act}=\lambda_{depth}=1.$$

这些公式直接说明 depth loss 的梯度路径；它们不提供 FLOPs、带宽或训练 wall-clock。

### 3.6 训练/实验/部署设计

- 数据：RoboTwin 2.0 每任务 50 clean、500 randomized trajectories；真实 AstriBot S1 四任务各 100 demonstrations，10 physical rollouts/task。真实和 RoboTwin depth 均通过 offline Depth Anything 3 pseudo-depth pipeline 获得。
- 输入：三视图（head + 两 wrist）mosaic；main 256x320、wrist 128x160；VAE stride 16 + 2x2 latent grouping 对应 32x32 register cell；最多 17 帧，8 future video/depth frames；action chunk 32，16-D absolute end-effector action。
- 训练：LingBot-VA 初始化、Wan2.2 VAE、AdamW、$2\times10^{-5}/N$ 学习率（$N$ 为 machine 数）、10 warmup、clip 2.0、bf16 参数；main 50k steps、ablation 10k steps。机器型号/数量、batch、训练时间、峰值训练显存未报告。
- 部署：单步维护 observation queue 和 executed-action history；VAE 编码后替换 video KV cache，action KV cache 追加历史，10 action denoising steps，执行 action chunk；每 4 actions 采集一个 observation。

## 关键实验与证据

### 4.1 主结果

Table 1：WAM4D clean 93.8%、randomized 89.9%、平均 91.8%；Fast-WAM 为 91.9/91.8/91.8，LingBot-VA 为 92.9/91.6/92.3。WAM4D 在 clean 比 Fast-WAM 高 1.9 个百分点，在 randomized 低 1.9 个百分点，平均相同；不能据此说 action quality 全面领先。

Table 2：AstriBot 四任务 sub-action 平均 WAM4D 0.90，优于 π0.5 0.74、LingBot-VA 0.84、Fast-WAM 0.80；每任务仅 10 rollouts，是真实机器人支持性证据而非大样本统计验证。

### 4.2 消融和机制证据

![Table 7 register interface, placement, and visibility ablation](../assets/papers/wam4d/table7-register-interface-placement-visibility-caption.png)

Table 7 在固定 depth head、10-task split 下比较接口/层位/可见性。No depth clean SR 71.7；middle registers 75.2，AbsRel 0.053、$\delta_1$ 0.945、CD1 0.0108、F-score 0.685、F-score-T 0.825；bidirectional SR 76.6 最高，但几何指标较 middle 多数下降，且其层位也改为 6/12/18/24，因此 visibility-only 因果效果未被完全隔离。VAE depth head 的几何指标弱于 register 变体，支持 register interface 选择，但同时改变了 head/interface。

Table 8：trainable pretrained DA3 比 random-init/fixed-pretrained 在 10-task split 上获得最佳 selected metrics（clean SR 80.1、FVD 164.5、AbsRel 0.049、F-score-T 0.848），但这是 head 初始化与可训练性组合的直接对比，不拆分两者各自贡献。

### 4.3 技术点证据矩阵

| 技术点 | 声称收益 | 证据 | 是否受控 | 分类 | 结论 |
|---|---|---|---|---|---|
| geometry branch / spatial registers | 几何一致性和 action features | Table 7、Table 6 No-depth vs register；Fig. 5 attention | 大体 matched；接口/层位会共同变化 | direct ablation + mechanism visualization | 部分支持 |
| causal visibility 防 future shortcut | 因果 action generation | Fig. 2、§3.3；Table 7 bidirectional | visibility 行同时改层位 | confounded/indirect | 机制明确，隔离证据不足 |
| middle insertion layers | geometry/control balance | Table 7 shallow/middle/deep/uniform | 固定 head、数据和预算；多指标 trade-off | replacement baseline | 部分支持 |
| pretrained trainable DA3 | 强几何先验和适配 | Table 8 | random/fixed/pretrained 设置直接对照 | direct ablation | 支持，但未拆 init 与 finetune |
| deployment geometry removal | 低 inference cost | Algorithm 1、Table 9 | 没有同一模型 geometry on/off pair | direct deployment measurement, causal effect missing | absolute cost 有证据；加速归因未隔离 |
| training efficiency | 轻量/快速总体训练 | 50k/10k budgets、Table 6 params | 无 wall-clock/FLOPs/train-memory | missing | 不可建立 |

### 4.4 四个核验问题的结论

1. **训练-only geometry 与 inference tensors：明确。** 训练有 $R$、DepthBlocks、$P_g$、$G_\phi$、depth targets/loss；部署删除它们。保留的是共享 video-action backbone 的权重、VAE、history video/action tokens、future action denoising 和 KV cache。不存在论文证据表明部署保留显式 depth tensor。
2. **Causal mixture attention 的 operator/memory 后果：机制级明确，kernel 级未知。** mask 限定信息流，训练额外运行 register-to-history cross-attention（960 queries、4 blocks）和 DA3 head；推理删除该分支，减少 branch 的参数/激活/KV。因果 mask 本身不自动等价于 block-sparse/fused kernel，源码不可用所以不能声称算子复杂度或带宽利用率变化。
3. **4D consistency 是否单独建立：部分建立。** Table 6-8 的 AbsRel、$\delta$、Chamfer、F-score、F-score-T 和 Fig. 6 qualitative rollout 直接评估几何/时序点云质量；但这些结果来自可保留 geometry branch 的分析路径，部署 action-only policy 的“4D consistency”没有单独测试。
4. **action、训练开销、deployment latency 是否分别建立：** action quality 有 full-suite、real-robot 和 matched 10-task ablations；training overhead 只有参数量结构差异（default 5.690B vs no-depth 5.089B，+0.601B、约 +11.8%）和训练 step budget，缺 wall-clock/FLOPs/peak train memory；deployment latency/VRAM 有 Table 1/9 单 A800 测量，但没有同一 WAM4D geometry on/off 配对，因此不能把 525.43 ms 的差异全部归因于删除 geometry branch。

### 4.5 收益来源归因

| 组件/变化 | 对比基线 | 指标变化 | 影响路径 | 证据强度 |
|---|---|---|---|---|
| trainable pretrained DA3 + registers | No depth（Table 6） | clean SR 71.7 -> 80.1；random SR 69.1 -> 75.4；F-score-T 0.685 -> 0.848 | geometry feature shaping + head adaptation | direct but bundled |
| middle placement | shallow/deep/uniform | middle AbsRel 0.053、F-score 0.685、F-score-T 0.825；shallow RGB metrics better | geometry/control vs denoising trade-off | matched replacement baseline |
| bidirectional register visibility | default middle unidirectional | SR 76.6 vs 75.2，但 F-score 0.579 vs 0.685 | register->VA information and changed insertion layers | confounded; rough comparison only |
| geometry removal at serving | WAM4D 525.43 ms / 9.71 GiB vs Fast-WAM 425.53 ms / 11.55 GiB | WAM4D +23.48% latency, -15.93% VRAM | full model/runtime differences, not only geometry branch | direct system table; causal attribution missing |

## 5. Related Work 对比

| 类别 | 方法核心 | 本文差异 | 公平性/局限 |
|---|---|---|---|
| 2D WAM | LingBot-VA、Fast-WAM、Motus 联合视频/动作或 latent imagination | WAM4D 增加 training-only geometry prior；部署 action-only | Table 1 统一 denoising setting，但部分 baseline 数字来自既有报告（Table 3 caption） |
| 显式 4D world model | TesserAct、Kinema4D、X-WAM 生成/拼接 geometry 或 RGB-D future | WAM4D 不把 dense geometry 作为部署目标 | Fig. 1 是概念对比，不是同预算实验 |
| geometric foundation | DA3/Dust3R/VGGT 类 depth/point prior | 作为 teacher/head，经 registers 反向塑造 WAM features | DA3 pseudo-depth 数据管线和 head 训练状态影响结果 |
| spatial VLA | SpatialVLA、PointVLA、GeoVLA 等把 geometry 注入直接 policy | WAM4D 预测 future video+action，并用 geometry 作为辅助监督 | 任务、数据和模型范式不同，不能直接横比 |

## 6. OpenReview 公开评审 × 论文内容交叉核验

未发现该 arXiv-only 条目的公开 OpenReview 页面；任务包也给出 `openreview_url: unknown`。因此没有 reviewer claim、decision 或 rebuttal 可交叉核验。此项为 not-applicable，不代表未来转投版本没有评审。

## Infra 与部署

### 7.1 算力和参数

Paper-reported：5.690B default transformer parameters（Table 6），no-depth 5.089B；default geometry training 还包括 DA3 head、4 DepthBlocks、adapters。训练 50k main / 10k ablation steps，bf16 parameters，AdamW；设备与 step time 未报告。

Derived：参数差 $0.601$B，约 $(5.690-5.089)/5.089=11.8\%$。这只是模型规模差异，不是训练 FLOPs 或时间差；DA3 head 参数是否计入 “Transformer Params” 也未澄清。

### 7.2 显存与存储

Table 9 single A800 80GB inference：WAM4D 9.71 GiB、Fast-WAM 11.55 GiB、LingBot-VA 12.97 GiB。WAM4D 比 Fast-WAM 少 1.84 GiB（15.93%），比 LingBot-VA 少 3.26 GiB（25.13%）。训练 register activations、DA3 activations、optimizer states 的峰值显存没有报告；960 registers 只给出 token 数，hidden width、dtype/layout 未给出，无法可靠换算 bytes。

### 7.3 Data Types / 数值格式

| 对象 | 格式 | 阶段 | 硬件依赖 | 影响 | 证据 |
|---|---|---|---|---|---|
| model parameters | bf16 | training | accelerator support implied, exact kernel unknown | 可能降低 memory/compute，但数值收益未测 | §3.5 |
| VAE/latent/depth/attention activations | 未报告 | train/infer | unknown | 不能据此估算 bandwidth 或 cache bytes | §3.5/Algorithm 1 |
| actions | normalized float range [-1,1] | train/infer | none stated | 16-D action representation | §3.5 |
| depth targets | DA3 pseudo-depth / real depth annotations | training | offline preprocessing | geometry supervision only; no deployment tensor | §4.1 |

### 7.4 带宽、互联与高效利用

论文没有 bytes moved、runtime breakdown、peak/achieved HBM bandwidth、PCIe/NVLink/RDMA 统计。可写出的结构公式仅为：

$$\text{register activation bytes}\approx N_R\times d\times b\times n_{layers},\quad N_R=960,$$

其中 hidden width $d$、每元素字节数 $b$、保存的 activation 层数均未报告，所以不能给出数值 bandwidth/utilization。训练为 multi-machine（学习率除以 $N$），但 all-reduce、通信拓扑、overlap、CPU staging 和 kernel fusion 未说明。部署 KV-cache 替换是论文报告的逻辑操作，不等于已测得的 memory bandwidth 优化。

### 7.5 CPU/GPU/NPU 异构执行

latency/VRAM 仅在单 A800 80GB GPU 上报告；没有 NPU、CPU/GPU 分工、DMA、pinned memory、异步 copy、fallback 或 scheduler telemetry。VAE 编码、动作 cache 更新和物理机器人 I/O 在算法上必需，但具体落在哪个处理器及是否 overlap 均未知。不能将单 GPU 数字外推到异构部署。

### 7.6 调度/Serving/自定义算子

Algorithm 1 明确了 observation queue、video/action KV cache、10 action denoising steps 和每 4 actions 采样一次 observation；未给 batching、CUDA graph、custom attention kernel、quantization、request scheduler 或 multi-stream。Causal mask 的 operator 级实现需源码确认。

## 代码状态与实现核验

- 仓库：PDF 作者块中的 `https://github.com/myendless1/wam4d`。
- commit：unavailable；未 clone/访问（source 429 后按要求 local-only）。
- 结论：论文级实现路径可以列出 `DepthBlock`、`DA3-GIANT-1.1 DualDPT`、`KV-cache` 等概念，但不能声称对应代码文件、kernel、checkpoint 或 release。任何“默认代码实现”的推断均不采用。

## 局限与证据边界

### 优点

- 清楚把 geometry supervision 与 deployment geometry tensor 分开；§3.3/§4.7 对移除边界明确。
- 表 7/8 同时报告 SR、视频、深度和点云指标，避免只以 depth loss 宣称 manipulation 改善。
- Table 9 提供 A800 latency/VRAM 的可复核系统锚点；Table 2 提供真实机器人长时序任务的支持性证据。

### 局限

- 没有 geometry branch on/off 的同模型 latency、FLOPs、训练 wall-clock、训练显存或带宽 breakdown，因而“fast”主要是部署配置的绝对结果和 WAM 间比较。
- Table 7 bidirectional 对照同时改变 register 层位；causal mask 的独立因果作用未被完全隔离。
- 4D consistency 指标来自 geometry-enabled analysis path；action-only deployment 的空间一致性没有单独 telemetry。
- 10-task ablation 与真实任务样本有限；部分 baseline 结果来自既有报告，且训练数据/预算复现实况需代码核验。
- 长 autoregressive rollout 无显式 long-term object memory，遮挡后可能出现 identity-inconsistent completion（Fig. 7；§4.6）。
- TeX source、官方代码、权重和配置未核验，复现路径不完整。

## 研究启发

- 用严格的 same-backbone branch on/off 实验分别测训练 FLOPs、peak memory、latency、action SR 和 geometry metrics。
- 固定 register 层位，只切换 visibility mask，隔离 causal mixture attention 的贡献。
- 报告 inference geometry-on qualitative/geometry telemetry 与 action-only control 的关系，避免把 training readout 的 4D 能力外推为 deployment 4D state。
- 开源 attention mask、register grid、DA3 adapter、KV-cache 和训练配置，并提供 commit-pinned checkpoint。
- 在遮挡长时序加入 object memory/scene-state tracking，验证是否改进 Fig. 7 failure 而不恢复 dense geometry deployment。

## 待验证问题

1. default Train. DA3 的 5.690B 参数是否包含 geometric head；参数表的容量变化需 checkpoint/config 核验。
2. geometry branch on/off 是否在同一 WAM4D backbone、同 batch、同 denoising steps 下测过训练和推理开销？
3. Table 7 bidirectional 结果中，成功率提升来自 visibility 还是层位变化？
4. causal mask 是否由 dense masked attention、block-sparse kernel 还是其他实现执行？
5. action-only deployment 是否仍运行 future-video flow path，还是只运行 action denoising？论文 Algorithm 1 偏向后者，但代码不可核验。
6. pseudo-depth 的 DA3 误差、深度尺度和真实传感器标定如何影响 AbsRel/point-cloud metrics？
7. RoboTwin baseline 是否真正使用同一重采样数据、训练步数、相机和模型容量？
8. 4D rollout 的 geometry quality 与 closed-loop action success 是否存在可测的样本级相关性？

## 一句话总结

WAM4D 的关键桥接是训练时用 spatial registers 和 causal visibility 将 DA3 几何先验压入 video-action backbone，部署时完全移除 geometry branch；论文对几何/动作质量和部署绝对成本有证据，但没有隔离训练开销，也没有证明 branch removal 本身造成了多少 latency/memory 收益。
