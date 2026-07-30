# Video Generation Sparse Attention Selection

> [!info] 文档关系
> - 领域入口：[README](../README.md)
> - 专题 Survey：[Video generation sparse attention](../surveys/video-generation-sparse-attention.md)

## 纳入规则

- 必须直接改变视频生成 Attention 的 mask、selector、layout、kernel、量化或分布式执行；
- 端到端 pipeline 只有在能独立分析 Attention 贡献时纳入；
- 已有 canonical Paper 优先 link-only，不复制正文或资产；
- 15 篇新增工作均完成独立 `paper-deep-review`、PDF 核验、两类视觉证据与 manifest 验证。

## 结果

| 优先级 | 工作 | 处理 | Canonical owner | 角色 |
|---|---|---|---|---|
| P0 | CalibAtt | 新建精读 | custom_attn | 离线校准/编译 |
| P0 | Sliding Tile Attention | 新建精读 | custom_attn | 规则 tile 基线 |
| P0 | XAttention | 新建精读 | custom_attn | 在线 antidiagonal selector |
| P0 | VSA | 新建精读 | custom_attn | 可训练 coarse-to-fine selector |
| P0 | DSV | 新建精读 | custom_attn | 稀疏训练与 context parallelism |
| P0 | FPSAttention | 新建精读 | custom_attn | FP8 + sparse kernel |
| P1 | Sparse VideoGen2 | 新建精读、跨域链接 | multimodal_generation | semantic permutation pipeline |
| P1 | SpargeAttn | 新建精读 | custom_attn | 通用 online filtering |
| P1 | AdaSpa | 新建精读 | custom_attn | online search + step reuse |
| P1 | PAROAttention | 新建精读 | custom_attn | reorder + INT8/INT4 |
| P1 | VMonarch | 新建精读 | custom_attn | structured matrix |
| P1 | VORTA | 新建精读 | custom_attn | routed sparse variants |
| P2 | Jenga / TokenCarve | 单一 canonical 精读、跨域链接 | multimodal_generation | attention + full pipeline |
| P2 | RainFusion | 新建精读 | custom_attn | spatial/temporal/text pattern |
| P2 | RainFusion2.0 | 新建精读 | custom_attn | block mean/permutation/sink |
| anchor | Sparse VideoGen | link-only | multimodal_generation | 方法族锚点 |

## 去重与边界

- Jenga 与 TokenCarve 是同一工作，只登记 `jenga`。
- RainFusion 与 RainFusion2.0 是两个版本，后者以 `extends` 关系连接前者。
- XAttention、AdaSpa、PAROAttention 虽在既有 HASTE/LVSA 中出现过比较，过去没有 canonical Paper，因此本次不是重复创建。
- 生成模型本体与多种优化组合由 `multimodal_generation` 拥有；Attention primitive 和系统执行由 `custom_attn` 拥有。
