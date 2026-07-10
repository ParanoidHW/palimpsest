# Diffusion World Models

本目录保存 2025-09 之后 diffusion/flow 在常规多模态生成、具身世界模型和扩散语言模型/投机草稿方向的综述笔记。

## 阅读顺序

1. [diffusion技术总览](diffusion技术总览.md)：先看三条路线的总览、交付覆盖和 AI Infra 共性需求。
2. [常规多模态生成_diffusion最新进展](常规多模态生成_diffusion最新进展.md)：看图像、视频、音视频、统一理解生成和后训练路线。
3. [具身智能_diffusion最新进展](具身智能_diffusion最新进展.md)：看 world model、VLA diffusion action head、跨 embodiment 和控制 runtime。
4. [扩散语言模型_投机草稿_diffusion最新进展](扩散语言模型_投机草稿_diffusion最新进展.md)：看 dLLM serving、diffusion draft 和 speculative decoding 交叉方向。

## 资产说明

- 正式正文只使用四张 SVG 总览图：`diffusion_overall_2026_map.svg`、`multimodal_2026_diffusion_map.svg`、`embodied_world_2026_diffusion_map.svg`、`language_dllm_draft_2026_map.svg`。
- 生成过程中的 banner、direct 和 trend PNG 中间图已确认零引用并移出正式目录。

## 维护规则

- 时间窗口按当前综述固定为 2025-09-01 之后。
- 新增论文时优先写清子领域、机构、技术族、系统价值信号和本地 deep-review 位置。
- 结论需要回到模型结构、数据管线、后训练、候选验证、cache/runtime 和硬件约束。
