# 原论文图清单与 QA

所有文件均为论文 PDF 页面的裁剪，保留图号和完整 caption；`Cosmos 3` 图来自同一工作本地源码/论文资产。裁剪路径与最终知识库 `assets/papers/` 内容一致。

| 工作 | 图 | 用途 | 裁剪资产 | 正文使用 |
|---|---|---|---|---|
| FlexAttention VLM | Fig.2 | 高分辨率 token selection + hierarchical attention | `papers/2407_flexattention_vlm/figures/crops/fig2_hierarchical_vlm_selection_caption.png` | 理解侧机制 |
| Causal-rCM | Fig.3 | TF / DF / SF mask 与 KV rollout | `papers/2606_causal_rcm/figures/crops/fig3_causal_training_paradigms_caption.png` | special causal mask |
| Causal-rCM | Fig.4 | recipe 对比 | `papers/2606_causal_rcm/figures/crops/fig4_recipe_comparison_caption.png` | 算法闭环 |
| LVSA | Fig.1 | basic / expanded window | `papers/2605_lvsa/figures/crops/fig1_expanded_window_caption.png` | structured sparse mask |
| LVSA | Fig.4/Table 1 | 80GB 长视频 wall-time / OOM | `papers/2605_lvsa/figures/crops/table1_fig4_scaling_caption.png` | 性能证据 |
| VMoBA | Fig.2 | partition -> select -> sparse attention | `papers/2506_vmoba/figures/crops/fig2_vmoba_pipeline_caption.png` | selector + varlen packing |
| HASTE | Fig.4 | TMR / EBC | `papers/2605_haste/figures/crops/fig4_tmr_ebc_framework_caption.png` | dynamic mask control plane |
| Token Sparse Attention | Fig.3 | compress QKV -> attention -> scatter | `papers/2602_token_sparse_attention/figures/crops/fig3_compress_attention_scatter_caption.png` | kernel reuse |
| Sparse VideoGen | Fig.4 | spatial/temporal head online profiling | `papers/2502_sparse_videogen/figures/crops/fig4_svg_workflow_caption.png` | head dispatch |
| MInference | Fig.3 | A-shape / vertical-slash / block sparse pattern | `papers/2407_minference/figures/crops/fig3_sparse_patterns_caption.png` | long-context bridge |
| FrameDiT | Fig.1 | matrix attention 结构替代 | `papers/2603_framedit/figures/crops/fig1_matrix_attention_architecture_caption.png` | architecture alternative |
| Cosmos 3 | two-way attention infra | reasoner/generator lowering | `01_ai_infra/kernel/custom_attn/assets/papers/2606_cosmos3/two_way_attention_infra.png` | unified model |

## QA

- 逐张在渲染 PNG 上人工检查了图体、legend/axis 与完整 caption。
- 原论文图用于机制和证据，报告中不将 AI 生成图替换为论文事实图。
- 个别工作没有可审计官方 kernel 代码时，图只支持论文级机制，不被用于证明某个具体 runtime 或 host-device placement。
