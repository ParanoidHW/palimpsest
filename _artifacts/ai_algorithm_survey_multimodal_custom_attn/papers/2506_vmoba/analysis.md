# VMoBA 精读

VMoBA 对视频 token 做 recurrent block partition，按 gate 选 global blocks，再用 FlashAttention 计算选中块（PDF `paper.txt:123-144,320-324`）。它是训练内生路由而不是固定 window。

官方代码 commit `48aaccd4f14c5adb7db961058bfbb2113e392003` 显示实现细节：`src/vmoba.py:617-675` 用 `topk`/threshold 产生 `gate_mask`，取 `nonzero` indices、把 Q/KV 打包为变长序列，并调 `_flash_attn_varlen_forward` / `flash_attn_varlen_func`（`:360-373,675-702`）。因此 mask 在模型脚本侧短暂以 dense bool gate 存在，但不把完整 token-token matrix 传入 FlashAttention；稀疏性由 gather + varlen segment 表达。

长序列风险是 `topk/sort/nonzero` 与 pack/unpack 可能成为控制面瓶颈；它适用于选择足够粗的 block，而非每 token 独立随机选择。
