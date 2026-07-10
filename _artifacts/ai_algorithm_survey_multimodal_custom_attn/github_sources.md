# GitHub / 框架来源

访问日期：2026-07-10。stars/forks 为 GitHub API 快照，易变。

| 来源 | 角色 | 信号/核验 |
|---|---|---|
| `NVlabs/rcm` | Causal-rCM 官方实现 | 750 stars / 27 forks；commit `ed3cb14`；`rcm/utils/blockmask.py`、`flash_attention_jvp_triton.py`。 |
| `JiusiServe/LongVideoSparseAttention` | LVSA 官方实现 | commit `1ebcc92`；`lvsa/sparse_attention.py` 生成 int32 CSR，交给 FlashInfer `BlockSparseAttentionWrapper`。 |
| `KlingAIResearch/VMoBA` | VMoBA 官方实现 | 64 stars / 4 forks；commit `48aaccd`；`src/vmoba.py` 用选择 mask 打包变长序列，再调用 FlashAttention varlen。 |
| `minhkhoale/FrameDiT` | FrameDiT 官方实现 | 3 stars / 0 forks；commit `359bd12`；公开代码主要复用 Diffusers attention，mask 转为 bias。 |
| `pytorch/pytorch` | PyTorch FlexAttention 上游 | `torch/nn/attention/flex_attention.py` GitHub SHA `c051c529`；API 用 `score_mod` / `BlockMask`，不是预先 materialize `[Lq,Lk]` 的唯一方式。 |
| `flashinfer-ai/flashinfer` | block/paged attention runtime | 5,930 stars / 1,134 forks；适合 CSR/indptr、page/block metadata 与 plan/run 分离。 |
| `Dao-AILab/flash-attention` | dense / varlen 与定制衍生 kernel 基线 | 24,404 stars / 2,896 forks；注意标准 FlashAttention 不等于通用任意稀疏 mask。 |
| `UMass-Embodied-AGI/FlexAttention` | ECCV 2024 VLM 方法仓库 | 49 stars / 6 forks；作为高分辨率 VLM 稀疏/灵活 attention 的桥接来源。 |

## 结论

GitHub 搜索结果中大量“multimodal sparse attention”命中为非官方 demo，未作为证据。核心结论只依赖上述上游或论文作者组织仓库及论文 PDF。
