# LongLive-2.0 Figure Inventory

所有 12 个编号 Figure 均来自 LaTeX 源码中的单一对象；先以 220 dpi 渲染，再执行内容紧裁剪和 16 px 安全边距。`bbox` 以裁剪后 PNG 左上角为 `(0,0)`，尺寸见文件。

| Paper | Object | PDF page | Source | Crop / dimensions | Complete caption | Usage | QA |
|---|---|---:|---|---|---|---|---|
| longlive-2-0 | Figure 1 | 1 | `teaser.pdf` | `fig1-teaser.png`; `(0,0,8765,1300)` | LongLive 2.0 supports NVFP4-based multi-shot long-video generation for both training and inference. | teaser、质量/速度/显存 | 原分辨率通过 |
| longlive-2-0 | Figure 2 | 2 | `fig1-overall.pdf` | `fig2-overview.png`; `(0,0,2283,633)` | Overview of the LongLive-2.0 Framework. | 总体训练/推理边界 | 原分辨率通过 |
| longlive-2-0 | Figure 3 | 3 | `fig3-training-pipeline-v7.pdf` | `fig3-training-infra.png`; `(0,0,2445,1246)` | Overview of the Training Infrastructure. | Balanced SP | 原分辨率通过 |
| longlive-2-0 | Figure 4 | 4 | `Fig-clean-pipeline.pdf` | `fig4-clean-pipeline.png`; `(0,0,2932,893)` | Clean Pipeline for AR Video Generation. | 训练流程简化 | 原分辨率通过 |
| longlive-2-0 | Figure 5 | 5 | `nvfp4_dmd.pdf` | `fig5-dmd-training.png`; `(0,0,556,488)` | NVFP4 DMD training infrastructure. | DMD 低精度训练 | 原分辨率通过 |
| longlive-2-0 | Figure 6 | 7 | `inference_all.pdf` | `fig6-inference.png`; `(0,0,961,475)` | NVFP4 inference infrastructure. | W4A4、KV、异步解码 | 原分辨率通过 |
| longlive-2-0 | Figure 7 | 6 | `shot-level-sink.pdf` | `fig7-sink.png`; `(0,0,638,497)` | Multi-shot Attention Sink for streaming multi-shot inference. | 双层 sink | 原分辨率通过 |
| longlive-2-0 | Figure 8 | 15 | `sp_1.pdf` + `sp_2.pdf` | `fig8-sp-scaling.png`; `(0,0,1946,590)` 合并双 panel | Iteration speed and peak memory for SP, TP, DP in interactive AR training. | SP/TP/DP 扩展性 | 原分辨率通过 |
| longlive-2-0 | Figure 9 | 16 | `sp_inference.pdf` | `fig9-sp-inference.png`; `(0,0,1405,719)` | Sequence Parallelism (SP) Inference. | 非 Blackwell SP 推理 | 原分辨率通过 |
| longlive-2-0 | Figure 10 | 17 | `shot-level-sink-ablation.pdf` | `fig10-sink-ablation.png`; `(0,0,7092,2380)` | Visual ablation of the multi-shot attention sink. | 漂移机制消融 | 原分辨率通过 |
| longlive-2-0 | Figure 11 | 18 | `ptq_nvfp4.pdf` | `fig11-ptq.png`; `(0,0,2490,1168)` | Comparison of PTQ and Pre-trained NVFP4. | PTQ 质量边界 | 原分辨率通过 |
| longlive-2-0 | Figure 12 | 19 | `DMD_comparison.png` | `fig12-dmd-comparison.png`; `(0,0,2524,677)` | Comparison of two DMD fine-tuning strategies. | DMD 策略选择 | 原分辨率通过 |

正式资产均位于 `../assets/papers/longlive-2-0/`，每个对象在 Paper 正文有一处图片引用和邻近解释。Table 1–7 不使用截图，完整决策相关字段在 Paper 的“关键结果”章节以 Markdown 表重建。
