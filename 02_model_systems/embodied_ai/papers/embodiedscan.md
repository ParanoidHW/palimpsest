# EmbodiedScan

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[具身智能模型演进、Infra 与端云协同](../surveys/embodied-ai-evolution-infra.md)
> - 证据资产：`../assets/papers/embodiedscan/`
> - 相关文档：[论文索引](../evidence/paper-index.md)、[图表清单](../evidence/figure-inventory.md)

论文：[arXiv:2312.16170](https://arxiv.org/abs/2312.16170)。代码核验固定于 [InternRobotics/EmbodiedScan](https://github.com/InternRobotics/EmbodiedScan/tree/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c) 的 `fe26e4bc3f3fb706fd7e33788766f61f8857fc3c`；过程材料保留于审计区。

## 论文资料

- 作者：Tai Wang 等；Shanghai AI Laboratory、SJTU、HKU、CUHK、Tsinghua。
- 发表：CVPR 2024，pp. 19757-19767；arXiv 2312.16170。
- 核心问题：如何从第一视角 RGB-D 序列建立可被语言定位的、场景级几何与语义 3D 表示。
- 数据规模（paper-reported）：5,185 scans、890k images、160k objects、762 box categories、970k prompts；occupancy benchmark 80 类。
- 关键假设：相机内外参可用；多视角可以转换到一个预先对齐地面/墙面的 global coordinate；训练/评测可通过有限视角采样近似探索过程。

## 核心机制与贡献

1. 将三套真实室内 RGB-D 数据统一为 ego-centric multi-view suite，并扩充 oriented box、occupancy 和 language annotation。规模由 Table 1 与 Sec. 3 直接记录，但 annotation quality 主要是流程说明，没有独立 inter-annotator agreement。
2. 提出 Embodied Perceptron：稀疏多层融合服务 detection/grounding，稠密 grid 融合服务 occupancy。Fig. 4、Sec. 4 与代码直接支持结构存在。
3. 建立 continuous、multi-view、monocular、grounding benchmark。Table 2-5 给主结果，Table 6-14/附录给设置与消融。
4. 关键收益不是都被同等验证：dense fusion 与 box decoder 有直接消融；VL fusion、contrastive loss、多尺度监督缺少逐组件 matched ablation。

## 方法与实现

### 3.1 问题到方案的逻辑链

真实 RGB-D/pose 异构 -> 统一帧采样与 global frame -> depth 转点并聚合 -> 2D ResNet 与 sparse MinkResNet 并行编码 -> 对 box/grounding 做层级对应的 sparse projection fusion，对 occupancy 做固定网格 dense fusion -> task-specific decoder -> AP/AR、mIoU 或 grounding success 评测。

### 3.2 模型与系统架构

![Figure 4: Embodied Perceptron](../assets/papers/embodiedscan/fig4-embodied-perceptron-caption.png)

Figure 4 直接显示三条输出路径。代码进一步确认 sparse fusion 并非简单 concatenate 原图：每层 voxel coordinate 乘 voxel size 回到物理坐标，投影至各视角同层 feature，`grid_sample` 后按有效视角平均，再以相同 coordinate map 拼回 Minkowski sparse tensor。Dense occupancy 则对 40x40x16 prior grid 投影图像 feature，同时把 MinkResNet 最后一层 densify，形成 256+512=768 channel volume。

### 3.3 设计动机与具体问题映射

| 设计项 | why 状态/来源 | 针对问题 | 因果机制 | 替代方案/权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|
| 复用三套真实 RGB-D 数据并统一格式 | author-stated；Sec. 3.1 | 单一 indoor dataset 场景/类别不足，渲染有 domain gap | 保留真实 first-person sensor stream，同时扩展场景覆盖 | 新采集更一致但成本高；复用带来传感器/采样异质性 | Table 1、Table 7、Table 8 | partially supported |
| SAM-assisted oriented box annotation | author-stated；Sec. 3.2、Fig. 3a | 原标注缺 orientation、小物体与长尾类别 | keyframe SAM mask 提供初始化，再由正交视图人工调整 | 全人工慢；SAM bias 与 QC 未量化 | Fig. 3、Fig. 6、数据统计 | plausible，缺质量受控实验 |
| global coordinate 对齐 | author-stated；Sec. 3.1 | 多视角聚合需要共同 reference，跨源分布不一致 | floor/wall 对齐降低 pose distribution variance | 在线 agent 未必有该先验；SLAM frame 更真实但噪声大 | 论文仅称 slight improvement，无数字 | unverified |
| 可变视角采样与有效视角平均 | author-stated；Sec. 4.1 | 输入顺序/数量变化 | 坐标投影后对有效视角 feature 求平均，保持 permutation invariance | attention/visibility weighting 更灵活但更耗算 | Fig. 7；code `point_fusion.py:257-309` | supported for sampled range；continuous 曲线受 GT 变化混杂 |
| isomorphic sparse multi-level fusion | author-stated；Sec. 4.1 | FPN/raw-image query 与 sparse levels 不一致，梯度不稳定 | 每个 voxel level 对应同尺度 2D feature，避免单尺度错配 | painting 简单；FPN fusion 显存更高 | Table 2 bridge baseline；附录报告约 25G vs 59G | partially supported，缺单独 level-matching 消融表 |
| dense grid fusion | author-stated；Sec. 4.1 | occupancy 需要细密、规则 3D prediction | 每个 grid point 投影到 2D FPN，并与 densified 3D feature concat | painting 丢失 dense information；coarse MinkUNet 分辨率不足 | Table 12 direct ablation | supported |
| sparse/dense task-specific decoder | author-stated；Sec. 4.2 | box 是 sparse instances，occupancy 是 dense field | 分别使用 FCAF-style sparse head 与 3D FPN multi-scale head | 更统一 decoder 可做 multi-task，但尚未探索 | task results；无统一 decoder 对照 | plausible |
| 6D rotation + weighted disentangled corner loss | author-stated；Sec. 4.2、Eq. 1-2 | Euler L1 难优化且 9-DoF box 参数耦合 | 用 corners 把 center/size/orientation 映射到几何误差，并分组监督 | 7-DoF IoU loss更贴 AP50 但近似且不可覆盖完整旋转 | Table 2、Table 13 | supported；最佳 AP25/AP50 方案并不完全一致 |
| occupancy 多尺度监督 | author-stated；Sec. 4.2、Appendix A.1 | 细粒度 occupancy 需要低层 detail | 3D FPN 三尺度输出，训练时逐级衰减权重 | 单尺度省算力；权重敏感性未给 | code/config 与总体结果，无独立消融 | unverified |
| VL transformer + contrastive alignment | author-stated；Sec. 4.1-4.2、Appendix Eq. 3-5 | prompt 与 sparse 3D object feature 需交互 | self-attention 建模空间关系，cross-attention/contrastive loss 对齐 token-object | detector proposals + late fusion 更模块化 | Table 5 仅整模型对比 | plausible but confounded |
| 复杂 prompt 拼接 | author-stated；Appendix B.3 | 密集同类对象使单关系 prompt 有歧义 | 拼接同一 target 的多条空间关系收缩候选集 | 可能引入语言模板偏差；人工自然语言更真实 | 论文无 matched ablation；README 后续结果不是 paper evidence | unverified |

### 3.4 关键公式

Box 解耦定位损失：

$$
L_{\mathbf c}=L_{CD}\left(\mathbf B(\mathbf c,\hat{\mathbf l},\hat{\mathbf\Theta}),\hat{\mathbf B}\right),
$$

$$
L_{loc}=0.2L_{\mathbf c}+0.2L_{\mathbf l}+0.2L_{\mathbf\Theta}+0.4L_{pred}.
$$

它把三个参数组分别替换为预测、其余保持真值，再叠加整体 box corner loss。Table 13 表明 weighted decoupling 的 mAP25 为 21.70，但 7-DoF IoU loss 的 mAP50 为 14.43，高于 weighted decoupling 的 12.53；因此“几何解耦最优”只对部分指标成立。

## 关键实验与证据

### 4.1 技术 claim 证据矩阵

| 技术 claim | 论文证据 | 控制情况 | 证据分类 | 结论 |
|---|---|---|---|---|
| RGB-D 优于单模态 | Table 2/3 的 camera/depth/RGB-D rows | 架构分支相近但 modality-specific behavior 不完全等价 | direct-to-partial | detection 中 depth 主导；occupancy 中 RGB 带来更大 semantic 增益 |
| sparse multi-level fusion 优于 painting | Table 2：painting AP25 15.10，Ours 16.85 | 在相同 dataset/task 的 bridge baseline 上比较，但完整 ours 可能含多处实现差异 | indirect/confounded | 支持总体方案，不完全隔离“同层匹配”单点因果 |
| dense fusion 设计有效 | Table 12：20.33/24.53/21.16/27.65 mIoU | 同一 RGB-D occupancy setting，替换 fusion/backbone choice | direct ablation | 强证据 |
| weighted corner decoder 改善 oriented detection | Table 2：FCAF3D 9.07 -> +decoder 14.80 AP25；Table 13 | bridge baseline + 细粒度 loss ablation | direct ablation | 强证据，但 AP50 偏好 IoU-like loss |
| 任意视角数量具有可扩展性 | Fig. 7 | multi-view inference/training曲线较直接；continuous GT 随视角变化 | direct + confounded | 20 views 后趋于饱和；“任意”仅是结构性质，不是无界成本 |
| 数据规模带来增益 | Table 14：ScanNet -> +3RScan -> +Matterport3D | 模型固定、训练数据递增，但域组成与样本数同时变化 | direct trend, scale/domain confounded | 增益存在；不能只归因样本数线性增长 |
| VL fusion/contrastive loss带来 grounding 增益 | Table 5 只比较完整方法与其他模型 | 架构、encoder、training recipe 同时变化 | confounded | 不能归因到单个 VL component |
| in-the-wild 泛化良好 | Appendix qualitative/video statement | 无定量、无 sensor/domain split、作者称 no cherry-picking 但不可审计 | indirect | 仅示例性证据 |

### 4.2 消融、机制证据与收益归因

![Table 12: dense fusion ablation](../assets/papers/embodiedscan/table12-dense-fusion-ablation-caption.png)

Table 12 是最干净的 model-design 证据：相对 painting，最终 dense fusion 从 20.33 提升到 27.65 mIoU，绝对 +7.32，约 +36.0% 相对提升；相对 MinkUNet 为 +3.12（+12.7%），相对 w/o FPN 为 +6.49（+30.7%）。这些数字支持“fine-grained point partition + FPN image feature + dense volume concat”整体，但表中没有完全正交的 factorial design，不能把 +7.32 独立分配给某一个子模块。

### 4.3 哪些结果隔离模型设计，哪些隔离数据规模

- 模型设计：Table 2 的 `FCAF3D -> +our decoder -> +painting -> Ours` 是固定 EmbodiedScan setting 的 bridge comparison；Table 12 固定 occupancy task 比较 dense fusion；Table 13 固定 detector 比较 loss 组合。这三组最适合回答设计贡献。
- 数据规模：Table 14 固定模型与验证集，逐步加入 ScanNet、3RScan、Matterport3D。它隔离的是“训练数据组合”而非模型设计；但 scan 数量与 domain diversity 同时变化，所以不是纯 sample-count experiment。
- 传感器：Table 2/3 的 RGB、Depth、RGB-D rows 主要隔离 modality；不能把它们直接当作 architecture ablation。

### 4.4 显式证据闭环

1. 问题：scene-level reconstructed point cloud benchmark 与真实 first-person RGB-D deployment 有输入鸿沟（Introduction）。
2. 假设：相机 pose/global frame 足以把多视角 depth 与 image feature 映射到共同 3D 表示（Sec. 3-4）。
3. 方法：multi-view aggregation + sparse/dense projection fusion（Fig. 4；代码路径见第 8 节）。
4. 测量：AP/AR、mIoU、view-count curve、fusion/decoder/data ablation（Tables 2-14）。
5. 结论：RGB-D fusion、oriented decoder 与更多真实数据均改善对应 benchmark。
6. 局限：global alignment 是额外先验；continuous GT 会随视角数量改变；代码提交与 paper-time split 不同；无 latency/bandwidth telemetry；因此不能把 benchmark gain 直接外推为在线 embodied system gain。

## 5. Related Work 对比

| 类别 | 代表方法/数据 | 机制/优点 | 局限 | 与本文关系/公平性 |
|---|---|---|---|---|
| indoor 3D datasets | ScanNet、3RScan、Matterport3D、ARKitScenes | 真实扫描、成熟 annotation | 类别/任务或 ego-centric setup 有限 | EmbodiedScan 复用前三者，因此不是完全独立新域；Table 1 的 annotation breadth 对比有效 |
| synthetic/mesh embodied data | HM3D、HSSD | 可交互、规模大 | mesh/render domain gap | 本文强调真实 RGB-D；Table 7 直接显示 render-to-real drop，但只在 ScanNet 子集 |
| sparse 3D detection | VoteNet、FCAF3D | point/voxel sparse efficiency | 原设定多为 axis/yaw-aligned、类别较少 | 本文改为 9-DoF 和 284 类；直接复用可能不公平，因此提供 decoder adaptation |
| occupancy | OccNet、SurroundOcc、TPVFormer | dense structured representation | 多来自 autonomous driving camera setup | 本文改为 indoor RGB-D grid；task/domain adaptation 同时变化，跨方法结果是 baseline 而非严格原论文复现 |
| 3D grounding | ScanRefer、BUTD-DETR、L3Det | text-object alignment | 常依赖 reconstructed scene/proposals、prompt 较简单 | 本文端到端多视角 RGB-D 更难；但 current code metric 与论文 AP 命名存在语义风险 |

## 6. OpenReview 公开评审交叉核验

任务包未提供 OpenReview URL；官方 CVF 页面仅链接论文与 supplement，没有 OpenReview。精确标题 OpenReview API 请求返回 403，故无法完成公开 review/meta-review/rebuttal cross-check。详见 `openreview_reviews.md`。本报告没有引用任何 reviewer opinion；该缺口不改变论文/代码证据判断，但不能断言不存在隐藏或未索引 forum。

## Infra 与部署

### 7.1 证据分级总览

| 级别 | 结论 | 证据 |
|---|---|---|
| 论文实测/报告 | sparse 最终方案约 25G 显存，保留 FPN/其他替代约 59G；detection/grounding train/test 20/50 views，occupancy 10/20；点数上限 100k；所有主实验以 8 GPUs 训练（grounding baselines 部分 4 GPUs） | Appendix A/C；configs |
| 公式推导 | 20/50 张 480x480 RGB 的 fp32 input 分别至少 52.73/131.84 MiB；occupancy 768x40x40x16 fp32 fused volume 约 75 MiB；20-view dense projection 临时 sampled feature 逻辑尺寸约 500 MiB | 论文 shape/channel + code tensor path，本节公式 |
| 工程推断 | 显存主导项不是 100k XYZ raw points，而是多视角 2D pyramid、projection sampled tensors、3D activations与反向图；CPU data pipeline 和 host-to-device 可能成为输入瓶颈；无 NPU path | 由 tensor shapes/code path 推断，未 profiler 测量 |

### 7.2 算力、显存与主要表示

图像输入下限：

$$
M_{img}=N_i\cdot3\cdot480\cdot480\cdot4\ \text{bytes}.
$$

得到 20 views 为 55,296,000 bytes（52.73 MiB），50 views 为 131.84 MiB，尚不含 feature/gradient。按 sparse ResNet 的通道 `{128,256,512,1024}` 和标准 `{120,60,30,15}` 空间层级推导，每 view 2D pyramid 约 13.18 MiB fp32，20/50 views 约 263.67/659.18 MiB。

Sparse projection 的 `grid_sample` 会先形成 `N_i x C_k x N_{V_k}` sampled tensor 再按 view 求和。若第一级 active voxels 接近 100k，上限级逻辑临时量为：

$$
20\cdot128\cdot100000\cdot4\approx976.56\ \text{MiB},
$$

50 views 时约 2.38 GiB。实际 $N_{V_k}$ 会因 1 cm voxelization 和层级下采样而变化；这是 shape-derived upper-bound，不是 profiler peak。

Occupancy 的 dense fused volume：

$$
M_{dense}=40\cdot40\cdot16\cdot(256+512)\cdot4=75\ \text{MiB}.
$$

20-view dense image projection 在求和前的逻辑 tensor 为 $20\cdot25600\cdot256\cdot4=500$ MiB；这解释了为什么 view count、FPN 与 dense volume 容易主导 memory。相对地，100k XYZ fp32 points 只有约 1.14 MiB，坐标/稀疏 activation 才是后续成本。

### 7.3 Data Types / 数值格式

| 对象 | 格式 | 阶段 | 证据/判断 |
|---|---|---|---|
| depth-derived points | float32 | load/preprocess | `loading.py:285-294` |
| images | 显式 cast 到 float32 | model preprocess | `data_preprocessor.py:249-264, 281-305` |
| box/eval tensors | float32 | evaluation | `euler_box3d.py:29-33` |
| default training | fp32 default；AMP 仅 CLI `--amp` opt-in | training | configs 使用 `OptimWrapper`；`tools/train.py:85-97` 才动态改为 `AmpOptimWrapper` |
| sparse indices/masks | integer/bool | voxel/eval | voxelization/evaluator code |

论文没有报告 fp16/bf16/fp8/int8、量化或 accumulation precision。不能把 AMP 可选支持当作论文实验使用事实。

### 7.4 带宽、互联与利用率

$$
\mathrm{EffectiveBandwidth}=\frac{\mathrm{BytesMoved}}{\mathrm{RuntimeSeconds}},\qquad
\mathrm{Utilization}=\frac{\mathrm{EffectiveBandwidth}}{\mathrm{PeakBandwidth}}.
$$

论文与代码日志没有 runtime、HBM bytes、PCIe/NVLink traffic 或 GPU 型号/peak bandwidth，故两者均不可实测。可以推断 projection 的 memory traffic 随 $O(N_i\sum_k N_{V_k}C_k)$ 增长；`grid_sample`、valid mask、跨视角求和和 sparse concat 是主要数据移动路径。8-GPU 训练暗示 distributed gradient synchronization，但未报告 interconnect、all-reduce volume、scaling efficiency 或 overlap，不能判断 NVLink/RDMA 利用率。

### 7.5 CPU/GPU/NPU 异构执行

- 代码直接证据：dataset workers 读取/resize RGB-D、采样 views、将 depth 转 points、用相机外参聚合到 global frame；GPU 执行 ResNet、MinkowskiEngine、projection sampling、3D heads。
- 工程推断：20-50 张图的 decode/resize 与 depth-to-point 会产生显著 CPU 与 host-device input pressure；但仓库没有 pinned-memory、async DMA 或 pipeline profiler 证据。
- NVIDIA/CUDA 依赖由 README、MinkowskiEngine、PyTorch3D 明确；无 NPU kernel、NPU fallback 或混合 CPU/GPU/NPU placement 路径。
- 自定义/编译依赖：MinkowskiEngine 与 PyTorch3D；voxelization 包含 extension binding。论文未给 kernel-level throughput。

## 代码状态与实现核验

统一 commit：`fe26e4bc3f3fb706fd7e33788766f61f8857fc3c`。

| 论文机制 | 本地路径与行 | 固定 commit URL | 核验结论 |
|---|---|---|---|
| view 采样/相机参数组织 | `code/EmbodiedScan/embodiedscan/datasets/transforms/multiview.py:28-109` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/datasets/transforms/multiview.py#L28 | random/ordered views 与 intrinsics/extrinsics 同步 |
| depth points 转 global frame | `.../multiview.py:113-169` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/datasets/transforms/multiview.py#L113 | 对外参线性求解后拼接 points |
| multi-view projection 与平均 | `code/EmbodiedScan/embodiedscan/models/layers/fusion_layers/point_fusion.py:208-311` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/models/layers/fusion_layers/point_fusion.py#L208 | `grid_sample` 后按有效 view 数平均 |
| sparse level-wise fusion | `code/EmbodiedScan/embodiedscan/models/detectors/sparse_featfusion_single_stage.py:86-221` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/models/detectors/sparse_featfusion_single_stage.py#L86 | voxelize -> MinkResNet -> same-level image projection -> sparse concat |
| dense occupancy fusion | `code/EmbodiedScan/embodiedscan/models/detectors/dense_fusion_occ.py:120-259` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/models/detectors/dense_fusion_occ.py#L120 | grid image volume + densified point volume -> 3D neck |
| grounding fusion | `code/EmbodiedScan/embodiedscan/models/detectors/sparse_featfusion_grounder.py:176-320` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/models/detectors/sparse_featfusion_grounder.py#L176 | 复用 sparse fusion，再送入 transformer decoder |
| detection evaluation | `code/EmbodiedScan/embodiedscan/eval/metrics/det_metric.py:36-99`、`indoor_eval.py:224-326` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/eval/metrics/det_metric.py#L36 | AP/AR at IoU 0.25/0.5，与论文定义一致 |
| occupancy evaluation | `code/EmbodiedScan/embodiedscan/eval/metrics/occupancy_metric.py:33-115` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/eval/metrics/occupancy_metric.py#L33 | per-class IoU；index 0 被实现为 occupied-vs-empty geometry IoU，printed mean 语义需谨慎 |
| grounding evaluation | `code/EmbodiedScan/embodiedscan/eval/metrics/grounding_metric.py:36-152` | https://github.com/InternRobotics/EmbodiedScan/blob/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c/embodiedscan/eval/metrics/grounding_metric.py#L36 | top-10 any-hit success，不是标准 PR-area AP；与论文命名有歧义 |

Checkpoint URL 可访问且约 991.44 MiB，但未下载；参数量与 checkpoint 内部 config 未验证。仓库没有独立 tests 目录，且本地没有数据、MinkowskiEngine runtime 或权重，因此未运行训练/评测复现。

## 局限与证据边界

### 优点

- 数据、任务与 baseline 形成较完整 3D perception suite，且论文提供比常见 benchmark paper 更丰富的 appendix ablation。
- 稀疏与稠密 representation 的职责划分合理，代码路径与 Fig. 4 基本一致。
- Table 12/13 与 Table 14 分别提供 model-design 和 data-composition 证据，便于避免混淆归因。

### 局限

- “continuous” 不是在线 recurrent/stateful perception；是不同 view prefix 的 batch 化评测。
- global floor/wall aligned coordinate 是部署时可能不存在的先验。
- 数据规模与 domain diversity 同时增长，不能证明严格线性 scaling law。
- VL fusion、contrastive loss、多尺度 occupancy supervision 缺少独立 ablation。
- current code 为 2025 commit，README 明示公开 split 与论文结果略有不同；不能保证逐数字复现。
- grounding/occupancy evaluator 的当前实现语义与论文表格名存在风险，需 paper-time commit/log 才能闭环。
- 无 GPU 型号、latency、throughput、power、HBM/PCIe/NVLink telemetry；所有带宽结论只能是 shape-derived 或 inferred。
- 无公开 OpenReview 交叉核验；checkpoint 未下载；未运行训练/评测。

### 待验证清单

1. paper-time evaluator 是否用标准 grounding AP，还是当前 top-10 any-hit success？
2. occupancy mIoU 是否包含 geometry IoU/empty 项，论文数字由哪个 exact commit 产生？
3. 在无 floor/wall alignment、仅 noisy online pose 的设置下性能下降多少？
4. 对 sparse fusion 做正交消融：same-level matching、FPN、view aggregation、channel reduction 各自贡献多少？
5. 用 profiler 分解 image pyramid、projection sampled tensor、Minkowski activations 与 3D dense volume 的 peak memory/latency。
6. complex prompt 拼接的收益来自 disambiguation 还是模板/数据量增加？

## 研究启发

1. **哪些 3D 表示和 sensor input 主导 memory/preprocessing？** 论文实测 sparse 最终方案约 25G，替代 fusion 约 59G；代码与 shape 推导表明多视角 480x480 RGB feature pyramid、跨视角 `grid_sample` 临时 tensor，以及 occupancy 的 768-channel dense volume 主导显存，100k XYZ raw points 本身仅约 1.14 MiB。CPU 侧主要是 20-50 帧 RGB-D decode/resize、depth-to-point、pose transform、global aggregation 和 resampling。Depth 对 detection 几何贡献更大，RGB 对 occupancy semantic 类别贡献更大。
2. **哪些 benchmark 结果把 model design 与 data scale 分开？** Table 2 bridge baseline、Table 12 dense-fusion ablation、Table 13 sparse-decoder loss ablation固定数据并改设计；Table 14 固定模型逐步加入 ScanNet/3RScan/Matterport3D，隔离训练数据组合。后者仍混合 sample count 与 domain diversity，不能称纯规模实验。
3. **哪些代码路径实现 point/voxel/image fusion 与 evaluation？** 数据入口是 `multiview.py:28-169`；投影/有效视角平均是 `point_fusion.py:208-311`；稀疏 detection/grounding 分别是 `sparse_featfusion_single_stage.py:86-221`、`sparse_featfusion_grounder.py:176-320`；dense occupancy 是 `dense_fusion_occ.py:120-259`；评测是 `det_metric.py` + `indoor_eval.py`、`occupancy_metric.py`、`grounding_metric.py`。所有路径均对应 commit `fe26e4bc...f8857fc3c`。

## 待验证问题

EmbodiedScan 的核心价值是把真实第一视角 RGB-D、丰富 3D annotation 与 sparse/dense/language benchmark 串成可运行 suite；最强证据来自 dense fusion、oriented decoder 与数据组合消融，而在线连续性、评测语义和系统效率仍缺 paper-time code 与 profiler 级闭环。
