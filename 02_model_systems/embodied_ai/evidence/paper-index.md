# 具身智能锚点论文索引

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位汇总：[具身智能模型演进、Infra 与端云协同](../surveys/embodied-ai-evolution-infra.md)
> - 证据资产：见各 Paper 的 `../assets/papers/<paper-slug>/`
> - 相关文档：[图表清单](figure-inventory.md)

本索引记录 12 篇锚点的稳定元数据与验收边界。代码“可用”只表示本次能够定位到指定 commit 或公开入口，不表示训练、评测和部署能在当前环境复现。

| Paper | 年份与状态 | 在谱系中的角色 | 论文与代码 | 代码可用性 | 验收结论与主要限制 |
| --- | --- | --- | --- | --- | --- |
| [ACT](../papers/act.md) | RSS 2023 | 低成本双臂操作；chunk/ensemble 基线 | [arXiv](https://arxiv.org/abs/2304.13705)；[ACT](https://github.com/tonyzhaozh/act/tree/742c753c0d4a5d87076c8f69e5628c79a8cc5488)；[ALOHA](https://github.com/tonyzhaozh/aloha/tree/06369f03cd8e0a47e16d3a90167853fd33af7557) | 两个固定 commit 已核验 | chunk/CVAE 消融强；50 Hz 策略端到端 timing 未报告。 |
| [Diffusion Policy](../papers/diffusion-policy.md) | RSS 2023；arXiv v5 | 连续多峰动作与 receding horizon | [arXiv](https://arxiv.org/abs/2303.04137)；[code](https://github.com/real-stanford/diffusion_policy/tree/5ba07ac6661db573af695b419a7947ecb704690f) | 固定 commit 已核验 | 多阶段任务证据强；真实任务的 8/10/16 去噪步配置不可混为单一 SLA。 |
| [RT-2](../papers/rt-2.md) | 2023 技术报告 | web-VLM 到 action token 的桥梁 | [arXiv](https://arxiv.org/abs/2307.15818) | 未获得可固定的官方实现 | 机器人与 web 联合微调有直接实验；远程 serving 的网络与尾延迟未公开。 |
| [EmbodiedScan](../papers/embodiedscan.md) | CVPR 2024 | 具身多视图 RGB-D 数据和 3D 融合 | [arXiv](https://arxiv.org/abs/2312.16170)；[code](https://github.com/InternRobotics/EmbodiedScan/tree/fe26e4bc3f3fb706fd7e33788766f61f8857fc3c) | 固定 commit 已核验 | dense fusion 有直接消融；grounding evaluator 的 AP 语义存在实现级歧义。 |
| [Genie](../papers/genie.md) | ICML 2024 | 无标签视频的 latent action world model | [arXiv](https://arxiv.org/abs/2402.15391) | 主训练数据和权重未公开 | latent 可控生成有证据；约 1 FPS 生成不构成真实机器人闭环。 |
| [OpenVLA](../papers/openvla.md) | 2024 技术报告 | 开放 7B VLA、LoRA 与 int4 | [arXiv](https://arxiv.org/abs/2406.09246)；[code](https://github.com/openvla/openvla/tree/c8f03f48af692657d3060c19588038c7220e9af9) | 固定 commit、训练/推理入口和 checkpoint 已核验 | 量化与微调证据直接；边缘 NPU/高频闭环未测。 |
| [VLFM](../papers/vlfm.md) | ICRA 2024 | VLM value map 与 frontier 导航 | [arXiv](https://arxiv.org/abs/2312.03275)；[code](https://github.com/rai-opensource/vlfm/tree/584ed56008754fde7997d904983607def8328322) | 固定 commit 已核验 | value-update 消融直接；无模块 profiler、功耗或异步调度实验。 |
| [Cosmos World Foundation Model Platform](../papers/cosmos-world-foundation-model.md) | 2025 arXiv 技术报告 | Physical AI 数据、tokenizer 与视频生成平台 | [arXiv](https://arxiv.org/abs/2501.03575)；[tokenizer](https://github.com/NVIDIA/Cosmos-Tokenizer/tree/3584ae752ce8ebdbe06a420bf60d7513c0e878cc) | tokenizer 固定 commit 已核验；Cosmos 主仓版本漂移 | 训练并行和 AR latency 有直接表格；非在线机器人控制证据。 |
| [NaVILA](../papers/navila.md) | RSS 2025 | 语言中层 action 与腿式低层策略 | [arXiv](https://arxiv.org/abs/2412.04453) | NaVILA、legged-loco、NaVILA-Bench 的固定 commit 已核验 | W4A16 单样本测量直接；实机低层频率、网络和 command-to-motion latency 未公开。 |
| [VGGT](../papers/vggt.md) | CVPR 2025 | 多视图几何 foundation backbone | [arXiv](https://arxiv.org/abs/2503.11651)；[code](https://github.com/facebookresearch/vggt/tree/a288dd0f14786c93483e45524328726ab7b1b4ce) | 固定 commit 已核验 | H100 帧数/显存测量直接；并非动作策略或闭环定位器。 |
| [MotuBrain](../papers/motubrain.md) | 2026 arXiv v3 | 统一视频-动作模型和 action-only 优化 | [arXiv](https://arxiv.org/abs/2604.27792)；[repository](https://github.com/shengshu-ai/Motubrain/tree/b2b08f7504337c0d1faf840de8233c76b45ede39) | 仓库固定 commit 为 documentation-only | 累积优化表有直接证据；硬件 SKU、模型规模、cache 与端到端 protocol 缺失。 |
| [WAM4D](../papers/wam4d.md) | 2026 arXiv v3 | spatial register 与训练期 4D 几何监督 | [arXiv](https://arxiv.org/abs/2606.14048)；[repository entry](https://github.com/myendless1/wam4d) | 未获得可固定实现 commit | 质量/绝对延迟表存在；没有 geometry branch on/off 的匹配延迟消融。 |
