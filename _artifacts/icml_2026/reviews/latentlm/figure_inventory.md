# LatentLM Figure Inventory

论文：*Multimodal Latent Language Modeling with Next-Token Diffusion*，arXiv:2412.08635v1。页面渲染由 `paper.pdf` 以 180 DPI 生成，源页均为 `1530 x 1980` 像素；bbox 坐标系以左上角为原点，格式为 `(x, y, width, height)`。

| Row | Object | PDF page | Source dimensions | Crop bbox | Complete caption | Local path | Linked claim | Report section | Source URL | QA |
|---|---|---:|---|---|---|---|---|---|---|---|
| FI-1 | Figure 2 | 3 | 1530 x 1980 | `(240, 110, 1060, 710)` | “Figure 2: LatentLM unifies the modeling of continuous and discrete data. We introduce σ-VAE (Section 2.3) to represent continuous data as latent vectors. We perform next-token diffusion (Section 2.1) to autoregressively predict the latent vectors one by one. The diffusion head generates vectors by conditioning on the output states of Transformer. The predicted vectors can be decoded to produce the final outputs.” | `figures/crops/fig2_latentlm_architecture_caption.png` | 共享 causal Transformer 以 LM head 处理离散 token、以 diffusion head 处理连续 latent token | `analysis.md` 3.3 | https://arxiv.org/pdf/2412.08635v1 | passed: contact-sheet triage 2026-07-16；100% individual inspection 2026-07-16；单一编号对象、caption 完整、无章节标题/正文/页码、轴/标注可读，边界紧凑 |
| FI-2 | Figure 7 | 9 | 1530 x 1980 | `(240, 100, 1060, 570)` | “Figure 7: We compare the inference throughput of Diffusion Transformer (DiT) and LatentLM in the settings of different model size and batch size. ‘GQA’ stands for group-query attention.” | `figures/crops/fig7_inference_throughput_caption.png` | 单 H100、20 diffusion steps 下随模型与 batch 扩展的吞吐趋势；GQA 是额外 runtime/architecture 因素 | `analysis.md` 4.1 与 7.6 | https://arxiv.org/pdf/2412.08635v1 | passed: contact-sheet triage 2026-07-16；100% individual inspection 2026-07-16；单一编号对象、caption 完整、无后续正文/页码、曲线/legend/轴标签可读，边界紧凑 |

`figures/contact-sheet.png` 仅用于批量初筛；上表两张 counted crop 均已分别以原始分辨率打开检查。源 LaTeX 中也有独立图像资产，但正式 counted visual 使用 PDF crop，以保证编号与完整 caption 同框。
