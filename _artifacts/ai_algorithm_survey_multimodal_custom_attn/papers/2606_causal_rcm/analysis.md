# Causal-rCM 精读

## 证据与机制
PDF §B（`extracted_text/paper.txt:176`）和官方代码共同表明：teacher-forcing 将 clean/noisy blocks packed 到一次前向；`M_TF` 仅允许 noisy block 看历史 clean blocks 与自身 noisy tokens。该非三角 mask 同时进入 primal 和 JVP，故不能用“先跑 attention、再对输出补 mask”替代。

## Mask 到 kernel
- 表达：`BlockPattern` + `AttnMaskSpec`，而不是 `[L,L]` dense tensor。
- lowering：`rcm/utils/blockmask.py:72,146,197` 以 block metadata 构造 FlexAttention `BlockMask`；源码说明 fallback 对齐到 128 的 block。
- kernel：`rcm/utils/flash_attention_jvp_triton.py` 是 JVP 专用路径；README 指向 `RCM_FLEX_BACKEND=flash|auto|triton`。mask 的可见性在 tile/块层由元数据和 kernel 路径处理。
- runtime：同一 `BlockPattern` 驱动 packed training、replay 和 KV-cache inference；不是 host 侧生成完整 mask 再拷贝。

## Infra 判断
这是真正的“在线/结构化表达”实例：元数据规模随 block 数增长，避免 `O(L^2)` bool/bias；但可见块不规则时仍可能受 gather、padding 和 CP 负载不均约束。论文的 10x 收敛声明属于训练配方 + JVP 联合收益，不能归因给 kernel 单独贡献。

## 代码证据
官方 commit `ed3cb14dd936f92cdc9f9381af7369991509b41f`；公开评审未检索到，状态为 technical report。
