# Token Sparse Attention 精读

论文（ICML 2026）先对每 head 选择 token 子集、压缩 Q/K/V，再在紧凑张量上调用标准/稀疏 attention kernel，最后恢复输出（`paper.txt:14-23,148-160`）。其贡献是将 token-granularity selector 与 block/dense kernel 解耦，避免要求 kernel 原生支持任意 token predicate。

代价从 dense mask 内存转为 selector、gather/scatter、重排和恢复；紧凑 QKV 仍需要连续 layout 才能获得 FlashAttention 级吞吐。未获得官方实现，故对具体索引格式、CPU/GPU placement 和 kernel 细节标为未核验。
