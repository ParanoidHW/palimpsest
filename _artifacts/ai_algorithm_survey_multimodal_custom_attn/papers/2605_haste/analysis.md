# HASTE 精读

PDF 将问题定位为“在线 top-p mask 预测成本”而不是稀疏计算本身（`paper.txt:19-24,113-130`）。方法用 Temporal Mask Reuse，按 head 和 denoising step 用 query-key drift 决定复用或刷新稀疏 mask，并按 head 分配预算。

表达层面是动态 sparse pattern；本次未得到官方实现，无法确认它最终使用 CSR、BlockMask 还是 kernel 内 predicate。因此不能断言其 metadata 所在 device。可确定的系统结论是：视频 diffusion 的 mask planner 调用次数也乘以 denoising steps；跨 step 复用是降低控制面而非改变单次 QK 的方法。

公开评审/官方代码未检索到；关键收益仅以论文为准。
