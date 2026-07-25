# 具身智能模型演进、Infra 与端云协同

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[README](../README.md)
> - 上位汇总：无
> - 证据资产：各论文的 `../assets/papers/<paper-slug>/`
> - 相关文档：[论文索引](../evidence/paper-index.md)、[图表清单](../evidence/figure-inventory.md)

这份调研把具身智能视为从传感器到执行器的实时系统，而不是把机器人上的视觉语言模型等同于中心侧多模态服务。覆盖 2023--2026 年的 12 篇锚点工作：3D 感知、操作、导航、VLA、world model 与 WAM 各两篇。所有具体数字、公式、图表与代码核验均回到对应 Paper；这里仅保留跨工作比较和工程判断。

## 修订信息

- 当前版本：`1.1.0`
- 修订日期：`2026-07-25`
- 资料范围：只综合本领域 README 已索引的 12 篇 canonical Paper，不新增 Survey 尚未覆盖的精读。
- 本轮修复：逐批把概括性旧锚点替换为 Paper 的动机闭环、方法、技术 claim 证据矩阵、Infra 与局限精确章节；同步代码、checkpoint 与 OpenReview 的当前可用边界。
- 结论边界：Survey 保留跨论文比较，不复制 Paper 全文；系统吞吐、离线生成、仿真成功率和闭环控制安全不得跨协议直接比较。

## 结论先行

1. **首要约束是 deadline 与状态连续性。** 低层控制通常要求 20--100 Hz，高层 VLA/WAM 更适合 1--10 Hz 的动作块；均值吞吐不能替代 p95 deadline、过期观测与 fallback 设计。RT-2 的远程 serving、NaVILA 的双频结构和 MotuBrain 的频率声明都必须在各自边界内阅读，见 [RT-2 的 Infra 分析](../papers/rt-2.md#8-infra-需求分析)、[NaVILA 的 Infra 需求分析](../papers/navila.md#8-infra-需求分析)、[MotuBrain 的 Infra 分析](../papers/motubrain.md#8-infra-需求分析)。
2. **3D/4D 与 world model 的瓶颈正转向显存、token/activation 带宽和互联。** VGGT 的帧数-显存测量、Cosmos 的长上下文并行以及 WAM4D 的训练期几何分支说明，这类模型不能按端侧 TOPS 单独估算，[VGGT 实验](../papers/vggt.md#关键实验与证据)、[Cosmos Infra](../papers/cosmos-world-foundation-model.md#8-infra-需求分析)、[WAM4D 部署](../papers/wam4d.md#infra-与部署)给出原始边界。
3. **action chunk、receding horizon、KV/feature cache 与 action-only 是把大模型接入控制环的共同接口。** ACT 和 Diffusion Policy 分别用 chunk/ensemble 与多步去噪处理操作；OpenVLA、RT-2 使用 action token；MotuBrain 把重复视频输出裁成 action suffix。它们并不消除视觉前缀和安全闭环成本，见 [ACT 研究方法](../papers/act.md#4-研究方法)、[Diffusion Policy 方法](../papers/diffusion-policy.md#4-研究方法)、[OpenVLA Infra](../papers/openvla.md#8-infra-需求分析)、[MotuBrain 研究方法](../papers/motubrain.md#4-研究方法)。
4. **量化主要节省权重/激活流量与显存，并不自动降低所有计算。** OpenVLA 的 int4 和 NaVILA 的 W4A16 都有直接的容量、延迟或成功率测量，但真实收益取决于 fusion、算子覆盖和 fallback，[OpenVLA 技术点证据矩阵](../papers/openvla.md#52-技术点证据矩阵)、[NaVILA 技术点证据矩阵](../papers/navila.md#52-技术点证据矩阵与消融机制证据)。
5. **“能生成未来”与“能安全控制”是两条证据链。** Genie 和 Cosmos 对 latent action、视频预测和数据生成有证据，但秒级视频生成不是在线伺服；WAM4D 的训练几何分支可移除，但缺少匹配的 on/off 延迟消融，[Genie 实验](../papers/genie.md#关键实验与证据)、[Cosmos 技术 claim 矩阵](../papers/cosmos-world-foundation-model.md#5-关键结论与技术-claim-证据矩阵)、[WAM4D 局限](../papers/wam4d.md#局限与证据边界)。

## 范围与比较规则

- 范围包括机械臂、双臂/移动操作、轮式/腿式导航与人形相关模型；驾驶和无人机仅作为相邻证据。
- 同一“Hz/FPS/actions per second/GPU latency”名称并不代表同一测量：输入分辨率、视图数、采样步数、action horizon、batch、网络与低层执行都可能不同。
- 本文将论文图表中的直接测量与基于 token shape、算子路径的工程推断分开；后者不冒充 profiler 结论。

## 技术谱系

### 3D 感知：从任务融合到多视图 token backbone

EmbodiedScan 将 RGB-D、文本、3D detection/grounding/occupancy 放入统一多视图 benchmark；稀疏与稠密融合分别服务不同输出。[研究方法](../papers/embodiedscan.md#4-研究方法)与[技术 claim 证据矩阵](../papers/embodiedscan.md#51-技术-claim-证据矩阵)说明多视图投影和 feature volume 是实际负担，同时 grounding evaluator 的 AP 语义仍有实现级边界。VGGT 进一步将相机、深度、点图和 tracking 压入 feed-forward transformer，frame/global alternating attention 仅降低全局注意力常数，并未消除随帧数增长的 activation，[方法](../papers/vggt.md#方法与实现)和[运行时实验](../papers/vggt.md#关键实验与证据)给出边界。

趋势是把 3D 从独立感知结果转成可对齐语言、动作与历史状态的 token 前缀；训练期的 4D 几何监督会增加显存和互联压力，而部署期通常尝试裁掉 decoder。

### 操作：平滑、长时域与多峰动作

[ACT](../papers/act.md#2-研究动机与问题方案闭环)以 CVAE、action chunk 与 temporal ensemble 降低决策频率并平滑执行。chunk 越长，GPU 调用越少，但观测越旧、纠错越慢；代码核验还表明当前无-TE 路径仍每控制步搬运四幅 float32 图像，不能把 forward 降频直接外推为 H2D 同比例下降，见[技术 claim 证据矩阵](../papers/act.md#52-技术-claim-证据矩阵消融和机制证据)。[Diffusion Policy](../papers/diffusion-policy.md#2-研究动机与问题方案闭环)将未来动作序列从噪声迭代还原，用多次 denoiser forward 表达多峰行为；其部署成本近似随采样步数增加，[技术点证据矩阵](../papers/diffusion-policy.md#52-技术点证据矩阵)和[部署分析](../papers/diffusion-policy.md#8-infra-需求分析)必须一起阅读。

两者共同指向“高层块状规划 + 低层连续控制”：一次视觉编码、短期动作缓存、replanning 与动作插值往往比只缩小网络更重要。

### 导航：模块化异构 pipeline 到双频控制

[VLFM](../papers/vlfm.md#核心机制与贡献)串联 VLM 分数、地图、frontier、检测和 PointNav；其工程瓶颈可能是同步 RPC、CPU map 更新、序列化和模型等待，而非单个 GPU kernel，[部署边界](../papers/vlfm.md#infra-与部署)没有 profiler 支撑，需保持推断性质。[NaVILA](../papers/navila.md#4-研究方法)显式把语言中层动作交给低层腿式策略执行；RTX 4090 单样本量化 latency 不能推成实机 50 Hz，[技术点证据矩阵](../papers/navila.md#52-技术点证据矩阵与消融机制证据)明确了这一界限。

稳定设计是语义决策与低层执行分频，并将地图、历史观测、失败恢复作为持续状态，而不是每次调用重新建立上下文。

### VLA：动作 token、开放模型与量化

[RT-2](../papers/rt-2.md#4-研究方法)把机器人动作表示进已有语言 token 空间，通过 web/robot 联合微调转移语义泛化；但[其 Infra 分析](../papers/rt-2.md#8-infra-需求分析)表明远程 serving 的网络、排队与尾延迟没有充分公开。[OpenVLA](../papers/openvla.md#4-研究方法)以开放 7B VLM、离散动作 token、LoRA 与 int4 把模型推向单卡部署，[其 Infra 章节](../papers/openvla.md#8-infra-需求分析)显示 batch-1 下视觉 prefill 偏 compute，而自回归动作 decode 更受权重/KV 带宽和 launch 约束。

下一层的竞争不只是更大的 VLM，而是可失效的 persistent memory、token budget、early exit 和与低层控制相容的 action chunk 接口。

### World model：从 latent interactive environment 到 Physical AI 平台

[Genie](../papers/genie.md#核心机制与贡献)在无动作标签视频中学习离散 latent action，并以 tokenizer 与 dynamics 组成可控生成环境；[其系统分析](../papers/genie.md#infra-与部署)表明长视频 token、迭代采样和训练规模更接近数据生成/交互平台。[Cosmos](../papers/cosmos-world-foundation-model.md#4-研究方法)进一步提供 curator、连续/离散 tokenizer、diffusion/AR WFM、后训练与 guardrail；[主结果与证据矩阵](../papers/cosmos-world-foundation-model.md#5-关键结论与技术-claim-证据矩阵)说明高质量生成不能直接进入在线伺服。

world model 的价值在于预测、数据闭环、候选分支与不确定性，而非自动构成安全 policy。内容 guardrail 也不能代替碰撞、力矩限制和急停。

### WAM：统一视频动作和 4D 几何的早期形态

[MotuBrain](../papers/motubrain.md#4-研究方法)统一视频、文本与动作流，累积使用步数缩减、compile、FP8、cache 与 action-only；其表格是按顺序堆叠的累计测量，单项增益不可相乘，[Infra 边界](../papers/motubrain.md#8-infra-需求分析)也未公开完整 runtime 条件。[WAM4D](../papers/wam4d.md#核心机制与贡献)以 spatial register 与因果可见性把训练期几何监督连到动作主干；默认推理移除几何 head，但 register attention 仍有 token 成本，[实验](../papers/wam4d.md#关键实验与证据)尚不能证明“几何收益零延迟”。

## 负载分解与部署

一个端到端链路可概括为：

`sensor capture -> decode/normalize -> 3D/4D preprocessing -> vision encoder -> multimodal fusion -> reasoning/world model -> action decode -> safety -> low-level policy -> actuator`

| 阶段 | 主要约束 | 设计要点 |
| --- | --- | --- |
| 传感器和预处理 | IO、CPU copy、同步、带宽 | DMA/zero-copy、时间戳、异步队列。 |
| 3D/4D | activation 容量、memory bandwidth、稀疏算子 | 复用投影和 feature，避免重复坐标变换。 |
| 视觉与融合 | prefill compute、batch-1 decode 带宽/launch | 固定 shape、量化、KV 与视觉 feature cache。 |
| diffusion/world decoder | 重复 denoise、attention、activation | step reduction、低精度、cache 与异步 pipeline。 |
| safety/低层控制 | 硬 deadline、确定性 | 独立 watchdog、限幅和 fallback，不依赖云端返回。 |

端侧 SoC 的 TOPS 只能描述部分算子峰值，无法替代内存容量、带宽、传感器 IO、软件栈和 tail latency。中心侧长上下文/视频训练可用 FSDP、TP、CP、HBM 与高速互联，而端侧更依赖 fused kernel、unified memory、zero-copy、固定 token budget 和轻量控制器。

## 端云协同

| 模式 | 适用任务 | 关键约束 |
| --- | --- | --- |
| 全端侧闭环 | 移动操作、弱网、安全敏感控制 | 量化、固定 shape、局部缓存、watchdog 与可执行 fallback。 |
| 边缘感知、云端规划 | 长时语义推理、全局路径/数据检索 | 上传状态摘要而非原始多相机流；测量 RTT、p95、掉线恢复。 |
| 云端 foundation、端侧 policy | 训练、蒸馏、LoRA、量化后执行 | 固定 action chunk/状态接口，低层 controller 独立。 |
| 异步/推测层级 | 候选未来、长时规划 | 处理 observation drift、动作过期与 branch consistency。 |

云端模型可预生成候选 future/action chunk，端侧依据最新传感器选择、修正或拒绝，安全控制持续本地运行。Genie、Cosmos 与 MotuBrain 可启发离线候选生成，但均未构成在线安全证据。

## 共识、分歧与趋势

当前共识是：多视图和长视频 token 会把显存/互联推到前台；分频和 action chunk 是实际部署接口；量化、缓存、编译与异步化是 batch-1 的必选项；world model 必须走向 action-conditioned、可验证和可恢复。

仍无定论的是统一视频-动作主干与模块化 pipeline 的取舍、训练期是否保留几何分支、连续或离散 tokenizer、扩散或自回归动作生成。未来重点会是按风险和观测新颖度自适应计算，端侧 memory/KV/feature cache 协同，低精度扩展到 activation/KV/通信，以及将 p95 deadline miss、掉线恢复、energy/task、collision/near-miss 与 safety override 纳入 benchmark。

## 证据边界

- 图表、论文版本、页码、caption、bbox 与逐图 QA 在 [图表清单](../evidence/figure-inventory.md)；每个数字均可回到单篇 Paper。
- compute/memory bound、端云 SLA 与趋势是工程推断，除非单篇明确报告 profiler 或端到端测量。
- 代码可用性、commit 与实现差异在 [论文索引](../evidence/paper-index.md) 和各 Paper 的“代码状态与实现核验”中记录；缺少实现的工作不应被视为可复现部署栈。
