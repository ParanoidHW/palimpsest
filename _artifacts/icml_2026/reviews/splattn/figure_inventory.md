# SplAttN Figure Inventory

论文标题：SplAttN: Bridging 2D and 3D with Gaussian Soft Splatting and Attention for Point Cloud Completion。主 PDF `paper.pdf` 下载中断（868,352 bytes，`pdfinfo` 报 trailer/xref 缺失），因此无法进行 PDF 页码、源页面尺寸、bbox 和原分辨率裁剪 QA。ar5iv HTML 已保存并含图/表的完整 caption；代码仓库含 `overview.png`，但该图没有论文 caption，故不计为合格 crop，也不生成 contact sheet。

| Object | Source | Caption/evidence | Crop | QA |
|---|---|---|---|---|
| Figure 1 (mechanism) | ar5iv HTML `#S1.F1`, PDF page unavailable | “The overall architecture of our proposed SplAttN.” HTML also describes GS-Bridge, local encoder, global-local decoder. | not produced | blocked: primary PDF invalid; no page dimensions/bbox |
| Table 8 (system) | ar5iv HTML `#A5.T8`, PDF page unavailable | “Computational cost comparison. CD-Avg is reported from Table 1. Params, MACs, latency, and GPU memory are measured on a single NVIDIA RTX 3090 over the PCN test set with batch size 1.” | not produced | blocked: primary PDF invalid; no page dimensions/bbox |

替代视觉证据：代码 `code/SplAttN/overview.png`（无 caption，仅用于核对仓库结构，未嵌入分析）；HTML figure IDs、caption 和公式均记录于 `extracted_text/ar5iv.html` 与 `paper.txt`。
