# Diffusion

本目录保存 diffusion/flow 在常规多模态生成、具身世界模型和扩散语言模型/推测解码方向的综述与单篇精读。

## 阅读顺序

1. [diffusion技术总览](diffusion技术总览.md)：先看三条路线的总览、交付覆盖和 AI Infra 共性需求。
2. [常规多模态生成_diffusion最新进展](常规多模态生成_diffusion最新进展.md)：看图像、视频、音视频、统一理解生成和后训练路线。
3. [具身智能_diffusion最新进展](具身智能_diffusion最新进展.md)：看 world model、VLA diffusion action head、跨 embodiment 和控制 runtime。
4. [扩散语言模型与 Serving](surveys/language-diffusion-serving.md)：看 dLLM serving、diffusion draft 和 self-speculation；其中 [Nemotron-Labs-Diffusion](papers/nemotron-labs-diffusion.md) 按主要建模机制归入 diffusion。

## 资产说明

- 正式正文只使用四张 SVG 总览图：`diffusion_overall_2026_map.svg`、`multimodal_2026_diffusion_map.svg`、`embodied_world_2026_diffusion_map.svg`、`language_dllm_draft_2026_map.svg`。
- 可核验入口：[总体图](assets/diffusion_overall_2026_map.svg) · [多模态图](assets/multimodal_2026_diffusion_map.svg) · [具身/world 图](assets/embodied_world_2026_diffusion_map.svg) · [语言图](assets/language_dllm_draft_2026_map.svg)。
- 生成过程中的 banner、direct 和 trend PNG 中间图已确认零引用并移出正式目录。

## 证据索引

- [论文索引](evidence/paper-index.md)
- [图表清单](evidence/figure-inventory.md)

## 维护规则

- 时间窗口按当前综述固定为 2025-09-01 之后。
- 新增论文时优先写清子领域、机构、技术族、系统价值信号和 canonical Paper 位置。
- 结论需要回到模型结构、数据管线、后训练、候选验证、cache/runtime 和硬件约束。
