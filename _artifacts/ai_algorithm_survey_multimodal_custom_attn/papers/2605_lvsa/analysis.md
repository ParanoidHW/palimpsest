# LVSA 精读

## 机制
论文定义 window + rotating global anchors 的时空 block-sparse pattern；PDF 称 LVSA-FI 相对 dense attention 最多 3.17x，且 dense 在最长序列可能 OOM（`paper.txt:30-32,424-447`）。这针对长视频的固定窗口长程伪影，而非一般 top-k。

## Mask 到 kernel
- 表达：frame-block CSR，`indptr:int32[M+1]` 与 `indices:int32[nnz]`。
- 生成：`lvsa/sparse_attention.py:277-303,662-707` 在 Python planner 依据几何 pattern 构造 CSR；它不是完整 `[L,L]` mask。
- 传递：源码 `:601-603` 明确 `fi_indptr/fi_indices` 在构建时不先移至 GPU；由 `build_bsa_mask_compact` 与 FlashInfer planning pass 消费。这是本调研发现的直接“CPU 构造 metadata -> runtime planning”证据，而非 CPU 传 dense mask。
- 执行：FlashInfer `BlockSparseAttentionWrapper` 跳过未列出的 frame blocks；QK/softmax/AV 仅遍历 CSR-listed tile。

## 限制
该 pattern 静态且结构化，metadata 为 `O(nnz_blocks)`，不是 `O(L^2)`；但 planner、CSR 拷贝和不连续 KV 访问会在短序列或低稀疏度时吞噬收益。官方代码存在 vLLM-omni/Cosmos hook，说明该路线可进入统一多模态 serving。

代码 commit：`1ebcc92e13d353cbc685eb8bf435e47dd5dfa062`。
