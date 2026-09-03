# LongLive-2.0 Figure Inventory

| Paper | Object | PDF page | Source / crop bbox | Caption | Local path | Linked claim | QA |
|---|---|---:|---|---|---|---|---|
| longlive-2-0 | Figure 1 | 1 | `fig1-overall.pdf`; vector export, full object | LongLive 2.0 supports NVFP4-based multi-shot long-video generation for both training and inference. | `../assets/papers/longlive-2-0/fig1-overall.png` | overall quality/speed/memory | contact-sheet passed; individual 100% passed |
| longlive-2-0 | Figure 3 | 3 | `fig3-training-pipeline-v7.pdf`; vector export, full object | Overview of training infrastructure: traditional SP, Balanced SP and NVFP4. | `../assets/papers/longlive-2-0/fig3-training-pipeline.png` | Balanced SP rationale | contact-sheet passed; individual 100% passed |
| longlive-2-0 | Figure 6 | 7 | `inference_all.pdf`; vector export, full object | NVFP4 inference infrastructure with W4A4, KV cache and asynchronous decoding. | `../assets/papers/longlive-2-0/fig6-inference.png` | inference path | contact-sheet passed; individual 100% passed |
| longlive-2-0 | Figure 7 | 6 | `shot-level-sink.pdf`; vector export, full object | Multi-shot attention sink for streaming. | `../assets/papers/longlive-2-0/fig7-sink.png` | global/shot sink mechanism | contact-sheet passed; individual 100% passed |
| longlive-2-0 | Figure 11 | 18 | `ptq_nvfp4.pdf`; vector export, full object | Comparison of PTQ and pre-trained NVFP4; pre-trained NVFP4 preserves clearer facial details. | `../assets/papers/longlive-2-0/fig11-ptq.png` | quantization evidence | contact-sheet passed; individual 100% passed |

Tables 1–5 are reproduced in `analysis.md` as complete decision-relevant Markdown values (source pages 4, 6–8); Appendix Figures 8–10 and Tables 6–7 are cited where needed but not duplicated as assets because they repeat the progressive/system evidence or are qualitative supplements. The original TeX vector exports are single numbered objects with captions; no page render is used as a formal asset.

Process crop names retained for audit linkage: `fig3-training-pipeline-v7.png`, `inference_all.png`, `ptq_nvfp4.png`, `shot-level-sink.png`. They correspond one-to-one to the formal Figure 3, Figure 6, Figure 11 and Figure 7 exports above.
