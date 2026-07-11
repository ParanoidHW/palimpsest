# FlexAttention for Efficient High-Resolution Vision-Language Models 精读

> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Multimodal custom attention](../surveys/multimodal-custom-attention.md)
> - 证据资产：`../assets/papers/flexattention-vlm/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

来源：ECCV 2024；官方仓库 `UMass-Embodied-AGI/FlexAttention`；论文 [arXiv:2407.20228](https://arxiv.org/abs/2407.20228)。注意这篇论文的 `FlexAttention` 是模型方法名，不等于 PyTorch 同名算子 API。

## 问题与原始图

高分辨率 VLM 若把全部 high-resolution image tokens 拼接到 text/low-resolution token 后做全注意力，decoder 的成本随视觉 token 数二次增长。原论文 Fig.2（本地 `../assets/papers/flexattention-vlm/fig2_hierarchical_vlm_selection_caption.png`）给出两阶段结构：低分辨率图像和文本先提供全局上下文；每个 FlexAttention layer 再利用 input attention map 选择局部 high-resolution tokens。

## 核心机制

令低分辨率和文本 token 为 $H_L$，高分辨率候选为 $H_R$。前 $N_{SA}$ 层仅处理 $H_L$；随后层从上一层的 attention map 中根据最后生成 token 对视觉 token 的注意力选择 $S_l\subset H_R$，并对 $[H_L,S_l]$ 运行 hierarchical self-attention。selection 和 self-attention 每层交替，因此选择集合可以随问句与生成状态变化。

这不是把 dense attention 中若干 logits 置零：它在 attention 前缩短实际输入序列，表征更接近 `selected token indices + gathered high-res features`。因而最合适的 kernel 是对 compact/varlen QKV 的 dense attention，而不是把原 $H_R$ 长度的 `[L,L]` mask 传到 SDPA。

## 实现与边界

- 官方 README 说明项目为 LLaVA v1.5 7B 的高分辨率 VLM 实现，支持 TextVQA、V* Bench、MagnifierBench；本次未克隆全部训练依赖，kernel 具体实现没有按源码行核验。
- 论文 Fig.2/§4 显示 selection 来自上一层 attention map。若在训练或推理时先 materialize 全量 attention map 才 selection，首个 selection/每层 score 获取仍可能昂贵；论文的价值主要在不将全部 high-resolution feature 投入后续层。
- 与 Token Sparse Attention 的关系：两者都通过 `indices -> gather -> compact attention -> scatter/residual` 复用成熟 kernel；FlexAttention 的 selector 由视觉区域与文本生成 attention 引导，Token Sparse 则是 per-head general token selector。

## 证据矩阵

| 声称 | 证据 | 结论 |
|---|---|---|
| 动态选高分辨率视觉 token | Fig.2、PDF §4 | 直接机制证据 |
| 与低分辨率/文本 token 做 hierarchical attention | Fig.2 caption、PDF §4 | 直接机制证据 |
| 具体 CUDA/Triton/FlashAttention kernel | 本次未核验 | 不作实现归因 |
