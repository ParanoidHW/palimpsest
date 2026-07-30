# Video Generation Sparse Attention Claim Matrix

> [!info] 文档关系
> - [Survey](../surveys/video-generation-sparse-attention.md)
> - [Selection](video-generation-sparse-attention-selection.md)

| Claim | 直接证据 | 判断 | 限制 |
|---|---|---|---|
| 规则 3D tile 可把视频局部性转成稳定的可执行稀疏布局 | STA kernel 表与 E2E 表 | supported | kernel optimum 依赖硬件/shape |
| antidiagonal score 可减少完整 block scoring | XAttention 方法与 operator benchmark | partially supported | 无一般近似误差界 |
| coarse-to-fine selector 可参与预训练并降低训练 FLOPs | VSA scaling、kernel 图 | supported in reported scale | discrete Top-K membership 不可微 |
| 动态训练稀疏需要重做负载与通信分配 | DSV HCP/SCP 与 throughput | supported | 未独立 GPU 复现 |
| semantic permutation 提高连续 block density | SVG2 Figure 5/7 | supported | code-level mechanism 未审计 |
| mask/LSE/centroid 复用可摊销在线 selector | AdaSpa、SVG2、Jenga | supported by reported ablations | refresh 安全边界不统一 |
| pattern-aware reorder 同时有利于稀疏与低比特量化 | PARO matched table/latency figure | partially supported | 官方代码未发布，公式存在方向歧义 |
| Monarch 因子是 block mask 之外的可执行结构化替代 | VMonarch Figure 2/5 | supported at operator level | E2E 与 source/code 证据有限 |
| 路由器可在 full/sliding/coreset 间选分支 | VORTA Figure 6/Table 1 | supported | 与 cache/distillation 组合结果需拆账 |
| Jenga 8.83× 可归给 AttenCarve | Jenga Table 1 | rejected | AttenCarve-only 为 2.17×；8.83× 属于完整 Jenga-Flash |
| RainFusion2.0 是 RainFusion v1 的直接机制替代 | 两篇方法对比 | partially supported | v2 明确扩展目标，但 selector 结构已显著改变 |
| 单篇 operator speedup 可直接比较 | 跨论文证据 | rejected | shape、hardware、baseline、计时层级不同 |

## Promotion verdict

- `accepted`：证据链和实现/来源核验完整，可作为较强事实依据。
- `accepted-with-limitations`：可进入综合，但实现、硬件或公开评审缺口必须伴随结论。
- `rejected`：仅指未冻结的代理尝试，不否定后续 fresh remediation 的论文结论。
