# MInference 1.0 精读：把动态稀疏 mask 编译成 pattern-specific index 与 Triton FlashAttention 遍历

## 来源与图示索引

- 论文：*MInference 1.0: Accelerating Pre-filling for Long-context LLMs via Dynamic Sparse Attention*，本地 `paper.pdf` 共 27 页。论文给出实现细节，但当前 artifacts 未有官方仓库快照，故不能把论文伪码当作已代码审计的 API。
- 推荐嵌入图：**Fig. 3（PDF p. 3）** 展示 A-shape / Vertical-Slash / Block-Sparse 三族 pattern；**Fig. 4（p. 4）** 展示三条推理路径；**Algorithms 2/3（p. 5）** 是在线 index approximation；**Fig. 7 + Appendix C.4（p. 20）** 是混合块/列格式和 kernel traversal；**Fig. 10（p. 22）** 给出 index build 在总时延中的占比。

## 问题、范围与核心结论

MInference 面向的是 **causal LLM prefill**，不是 video diffusion 的双向 attention。它要解决的是：长 prompt 的 attention 矩阵很稀疏，但 exact nonzero location 随请求改变，静态 index 会破坏检索/理解；而每行 arbitrary top-k 的元数据和 irregular gather 又难以高效执行。

它将每个 head 先离线归为三类，并把在线动态 mask 约束到对 GPU 友好的结构：

1. **A-shape**：固定 global tokens + local window，几乎无需动态 index。
2. **Vertical-Slash (VS)**：动态重要列（vertical）+ 斜线/range（slash），需要“混合 block 与 column”的 index。
3. **Block-Sparse (BS)**：使用 pooled Q/K 估计的 top-K dense blocks。

本工作的关键价值不只是“先选 mask 再调 FlashAttention”：它公开说明了 **mask 应如何从概念性可见性变成 kernel 可遍历的两级 metadata**，并且明确避免 materialize dense causal mask。

## 符号与离线 pattern 选择

| 符号 | 含义 | 证据 |
|---|---|---|
| \(S,d_h\) | sequence length、head dimension | PDF p. 4-6 |
| \(M_{i,j}\in\{0,1\}\) | 概念性 dynamic sparse attention mask | p. 4, Eq. (1) |
| \(k_v,k_s\) | VS 的 vertical/slash top-K 数 | p. 5, Algorithm 2 |
| \(k_b\) | Block-Sparse 的 top-K block 数 | p. 5, Algorithm 3 |
| `last_q` | 用于 VS pattern approximation 的末尾 query 行数，实验取 64 | p. 5-6 |
| `block_size` \(B\) | BS pooling/block granularity，实验取 64 | p. 5-6 |

概念上，论文写作 \(A(M)=\operatorname{Softmax}(QK^\top/\sqrt d-c(1-M))\)，但这只是说明被遮蔽项软最大后近零（p. 4, Eq. (1)）。真实系统不应构造其中的 \(S\times S\) \(M\)：Appendix C.3 明确说为降低中间变量，删除 attention mask tensor，在 kernel 内实现 causal logic（p. 19）。

离线阶段的 **kernel-aware optimal pattern search** 先让不同候选在“实际 kernel FLOPs”而非概念 pair 数上对齐，再在 reference example 上比较稀疏输出对 dense 输出的误差，选每个 head 的 pattern 与参数（p. 5, Algorithm 1）。论文的实现配置为 1 个 30K KV-retrieval sample、A100 上约 15 分钟搜索，搜索空间见 Table 7（p. 19）。这是一种模型配置期的参数选择，和每个 request 的 online index build 是两个不同层次。

## 在线 mask/index 的构造

### A-shape

固定 global tokens 与 local window，pattern 是静态的，因此无需动态 mask construction（p. 6）。这可由 kernel 的 causal/local predicate 直接判断，metadata 最小。

### Vertical-Slash：从 recent queries 到混合 range + column index

对末 `last_q=64` 条 query 与所有 K 计算近似 \(\hat A_b\)，沿 vertical、slash 方向分别聚合，取 \(i_v,i_s\)，再调用 `sparseformat(i_v,i_s)`（PDF p. 5, Algorithm 2）。实现不是把每个 selected pair 存成 COO：

- slash line 以 \(64\times64\) blocks 表示；
- vertical line 以 \(1\times64\) columns 表示；
- 对每个 query-block row，vertical point 与基于 row 推出的 slash range 做 two-way merge；输出是 **merged block ranges + separate column indexes**，build 复杂度 \(O(k_v+k_s)\)（Appendix C.4.2, p. 20）。

随后 VS sparse FlashAttention 是混合 kernel：thread block 先遍历 block indexes，再将 column indexes 按 block size 分组、用 PIT（Permutation Invariant Transformation）加载到 dense compute block（p. 20）。这就是“稀疏表达”与“kernel 内定制化表达”同时存在的例子：外部 metadata 有 range/column index，kernel 将不规则列临时打包为 Tensor Core 可计算片段。

### Block-Sparse：池化近似到 top-K block list

以 `block_size=64` 对 Q/K mean-pool 成 \(\hat Q,\hat K\)，计算 block-level approximate score，取 top-K blocks \(i_b\)，调用 `sparseformat(i_b)`，再只在 selected blocks 做 QK、online softmax、AV（Algorithm 3，p. 5-6）。

Appendix C.4.1（p. 20）给出实际 kernel 形态：基于 Triton FlashAttention v2，每个 thread block 将 selected block index 作为额外输入，逐行循环 top-K blocks；这使 latency 近似和 block 数线性相关。它与先 materialize `M`、再由通用 dense attention 读 mask 完全不同。

## 完整的数据流与 memory 答案

```text
offline (per model/head): kernel-aware pattern/config search

prefill (per request, device):
  Q/K/V
  -> A-shape: direct static traversal
     VS: last-Q x all-K -> iv/is -> ranges + column indexes -> hybrid sparse FA
     BS: pooled Q/K -> top-K block index -> Triton block-sparse FA
  -> online softmax/AV -> O
```

| 用户问题 | MInference 的明确答案 |
|---|---|
| custom mask 是稀疏表达还是 kernel predicate？ | 三种都有：A-shape 接近在线 predicate；BS 是 selected-block index；VS 是 range/block index + column index，再由 kernel 做 PIT packing。|
| 是否先生成完整 mask 放到 device？ | 否。概念公式有 \(M\)，实现删掉 dense attention mask，causal 判断进 kernel（p. 19）。|
| index 在哪里生成？ | 论文称 VS 有 custom sparse index kernel，kernel 实现以 Triton/PIT 为基础（p. 19-20），因此 index build 是 GPU system path 的一部分。BS pooling/top-K 的具体 launch 融合未给代码。|
| host CPU 预生成/读取？ | 未报告。request-dependent Q/K 使核心 index 天然应 device-side；但论文没有 host/pinned-memory path，不能编造 CPU streaming 方案。|
| 很长序列 metadata 会不会失控？ | 实验报告 LLaMA-3-8B、1M context 的 sparse indexing memory 小于 160 MB（Fig. 10 讨论，p. 22），远小于 dense \(S^2\) mask；该数字不含所有模型 runtime 内存。|

在 1M context 下，论文还发现 dynamic approximation/index build 分别约占 VS 5%-15%、BS 25% 的总时间，BS 主要受 mean-pooling + block-level matmul 影响（p. 22）。这直接回答“不是 kernel online 生成怎么办”：即便在 device 上生成稀疏 index，也有实质控制面成本，必须把它计入 end-to-end，而不是只报 sparse QK kernel。

## 具体 kernel 与基础设施证据

- 论文实现使用 bf16、单张 NVIDIA A100，基于 PyTorch + FlashAttention + Triton + dynamic sparse compiler PIT（p. 6, p. 19）。
- 为跑 1M prompt，作者按 head split attention、按 sequence split MLP，并只保留最后 token 的 LM head；这些不是 sparse mask 本身，但会影响端到端时延归因（p. 19）。
- Fig. 10（p. 22）报告 1M 下 Block-Sparse kernel 的单 kernel speedup 高于 VS/A-shape；它不是三者质量等价的证明。Appendix 的 ablation 还指出 kernel 限制使“only vertical/slash”仍需保留另一类 top-1（p. 22）。

## 技术主张证据矩阵

| 主张 | 直接证据 | 判读 |
|---|---|---|
| 静态 index 会损害动态任务 | Table 2/4 的 `Ours w/ static`；Fig. 2c / p. 8 的文字归因 | 有任务结果，但 static 具体配置可能影响幅度 |
| 三类结构覆盖比统一 top-k 更适合 kernel | Fig. 3（p. 3）pattern recall 与实际 kernel FLOPs；Algorithm 1 | 是结合模型/搜索样本的经验性结论 |
| 真实 VS/BS metadata 可被高效遍历 | Appendix C.4（p. 20）给出 block/range/column 格式和 traversal | 没有源码，无法独立验证 occupancy、register、coalescing |
| long context 才能摊销 planner | Limitations（p. 18）：10K index 时间从约 5% 升到 30%；Fig. 10（p. 22） | 强边界条件，不能只引用 1M speedup |
| 模式可用于多模态/双向 attention | Appendix G 仅观察 BERT/T5/VLM 也有类似 pattern（p. 23+） | 不是完整 VLM kernel/quality benchmark，不能直接宣称可迁移 |

## 局限与对多模态 custom attention 的启示

- **因果语义不可直接移植。** VS 的 `last_q`、causal predicate、slash 方向均依赖 LLM prefill；Video DiT 或 encoder attention 需要重定义 query/key blocks 和双向可见性。
- **模型配置依赖。** 离线只用一个 30K synthetic sample 搜索，配置跨 LLaMA 262K/1M 复用；对跨模态 token 布局、长视频或统一模型应重新验证，不应把 head 分类冻结为 universal truth。
- **无官方代码核验。** 虽论文罕见地说明 metadata 和 kernel，但 `sparseformat` 的 buffer layout、index dtype、workspace、stream overlap、实际 Triton 源码版本仍未知。
- **可借鉴的设计模式。** 对任意长序列，优先把 mask 编译为 row-local block ranges / compact columns，并让 kernel 做 online causal/predicate 与 tile traversal；绝不上传完整 dense mask。对于 metadata 太复杂的 token-level选择，Token Sparse Attention 那种先 compact QKV 再调用 dense FA 往往更稳健。
