# DME 图表证据清单

| Paper | 对象 | 来源页 | 完整 caption | 正式资产 | bbox/分辨率 | 用途与 QA |
|---|---|---:|---|---|---|---|
| douyin-multimodal-embedding | Figure 1 | 2 | Performance Comparison. Overall and per-domain (Image, Video, VisDoc) results on MMEB-v2. | `../assets/papers/douyin-multimodal-embedding/fig-performance.png` | 2769x1183，trim bbox=(21,31,2769,1183)，16px 安全边距 | 主结果；逐图检查通过 |
| douyin-multimodal-embedding | Figure 2 | 3 | Comparison with prior works. Contrastive, CoT-based and DME embedding pipelines. | `../assets/papers/douyin-multimodal-embedding/fig-compare.png` | 1843x512，trim bbox=(262,346,1843,512)，16px 安全边距 | 动机对比；逐图检查通过 |
| douyin-multimodal-embedding | Figure 3 | 7 | Overview of the DME two-stage training pipeline. | `../assets/papers/douyin-multimodal-embedding/fig-pipeline.png` | 1349x313，trim bbox=(512,460,1349,313)，16px 安全边距 | 算法总览；逐图检查通过 |
| douyin-multimodal-embedding | Figure 4 | 8 | Stage 2: Semantic Sufficiency Learning. | `../assets/papers/douyin-multimodal-embedding/fig-pipeline-stage2.png` | 1679x777，trim bbox=(352,277,1679,777)，16px 安全边距 | Stage 2 机制；逐图检查通过 |
| douyin-multimodal-embedding | Figure 5 | 16 | Effect of batch size on contrastive training. | `../assets/papers/douyin-multimodal-embedding/fig-batch_size_scaling.png` | 2133x1299，trim bbox=(0,105,2133,1299)，16px 安全边距 | 训练参数分析；逐图检查通过 |
| douyin-multimodal-embedding | Figure 6 | 28 | Reconstruction visualization on image and visual-document inputs. | `../assets/papers/douyin-multimodal-embedding/fig-generate_1.png` | 1156x1365，trim bbox=(151,8,1156,1365)，16px 安全边距 | 表示完整性；逐图检查通过 |
| douyin-multimodal-embedding | Figure 7 | 29 | Reconstruction visualization on video inputs. | `../assets/papers/douyin-multimodal-embedding/fig-generate_2.png` | 1153x1357，trim bbox=(123,13,1153,1357)，16px 安全边距 | 表示完整性；逐图检查通过 |
| douyin-multimodal-embedding | Figure 8 | 30 | Reconstruction visualization on video moment-retrieval inputs. | `../assets/papers/douyin-multimodal-embedding/fig-generate_3.png` | 1153x1358，trim bbox=(119,13,1153,1358)，16px 安全边距 | 时刻检索示例；逐图检查通过 |

图像来自 arXiv:2608.02148v3 源码中的原始图，已转为 PNG，并按非白色内容紧裁剪后保留 16px 安全边距；bbox 以原始 PNG 左上角为坐标原点。源码图本身不含论文 caption，完整 caption 在本清单与 Paper 正文中保留。
