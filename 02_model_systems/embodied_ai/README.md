# Embodied AI

本领域记录具身智能从多视图 3D 感知、操作与导航，到 VLA、world model 和 world action model 的演进，并以端侧 deadline、状态连续性、显存/带宽与端云协同作为共同的 AI Infra 视角。

## 阅读路径

1. 先读 [综合调研：具身智能模型演进、Infra 与端云协同](surveys/embodied-ai-evolution-infra.md)，建立方法谱系与工程判断。
2. 再按任务进入 [3D 感知](#3d-感知)、[操作](#操作)、[导航](#导航)、[VLA](#vla)、[world-model](#world-model) 或 [WAM](#wam) 的单篇精读。
3. 需要核验选篇、版本、图表页码、caption、裁剪和视觉 QA 时，查阅 [论文索引](evidence/paper-index.md) 与 [图表清单](evidence/figure-inventory.md)。

## 文档索引

| 类型 | 文档 | 说明 |
| --- | --- | --- |
| Survey | [具身智能模型演进、Infra 与端云协同](surveys/embodied-ai-evolution-infra.md) | 12 篇锚点论文的跨工作综合与部署判断。 |
| Evidence | [论文索引](evidence/paper-index.md) | 选篇角色、版本、代码与主要限制。 |
| Evidence | [图表清单](evidence/figure-inventory.md) | 30 个正式图/表资产的来源和 QA 记录。 |

### 3D 感知

- [EmbodiedScan](papers/embodiedscan.md)：面向具身场景的多视图 RGB-D 数据与 3D 融合。
- [VGGT](papers/vggt.md)：多视图几何 backbone 与帧数/显存边界。

### 操作

- [ACT](papers/act.md)：action chunk、temporal ensemble 与低成本双臂操作。
- [Diffusion Policy](papers/diffusion-policy.md)：条件扩散动作序列与 receding horizon。

### 导航

- [VLFM](papers/vlfm.md)：VLM value map、frontier 与异构导航管线。
- [NaVILA](papers/navila.md)：语言中层动作与腿式低层控制分频。

### VLA

- [RT-2](papers/rt-2.md)：web-VLM 与机器人动作 token 的联合微调。
- [OpenVLA](papers/openvla.md)：开放 7B VLA、LoRA 和量化部署。

### World Model

- [Genie](papers/genie.md)：无动作标签视频中的 latent action 与生成环境。
- [Cosmos World Foundation Model Platform](papers/cosmos-world-foundation-model.md)：Physical AI 数据、tokenizer 和视频生成平台。

### WAM

- [MotuBrain](papers/motubrain.md)：统一视频-动作主干与 action-only 优化。
- [WAM4D](papers/wam4d.md)：spatial register、因果可见性和训练期 4D 几何监督。

## 资产说明

原论文 Figure/Table 的唯一 canonical owner 位于 `assets/papers/<paper-slug>/`。PDF、源码、整页渲染、裁剪过程、contact sheet、日志和原始一次性交付均保留在审计区，不作为正式知识入口。
