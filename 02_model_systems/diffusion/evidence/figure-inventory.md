# Diffusion Figure Inventory

## Nemotron-Labs-Diffusion

| Object | Source | Caption（完整转述） | Crop / usage | QA |
|---|---|---|---|---|
| Figure 1 | PDF p.1，`1654×2339` @ 200 DPI；bbox xyxy `(170,1160,1490,1735)` | 三种模式示意；NVIDIA H100 batch 1 的精度—吞吐折中；以及 GB200 上 Linear/Quadratic self-speculation 与 AR、Eagle3 的 per-user throughput 折中。 | [asset](../assets/papers/nemotron-labs-diffusion/fig1-tri-mode-tradeoff-caption.png)；支撑[研究问题](../papers/nemotron-labs-diffusion.md#1-研究问题与核心判断)。 | passed：单一 Figure 1、完整 caption、`1320×575` 原分辨率 QA。 |
| Table 1 | PDF p.4，`1654×2339` @ 200 DPI；bbox xyxy `(170,205,1490,470)` | 25B continuous-pretraining tokens 上各训练技术的累积消融，含五种配方与六个 benchmark、平均分。 | [asset](../assets/papers/nemotron-labs-diffusion/table1-training-ablation-caption.png)；支撑[训练消融](../papers/nemotron-labs-diffusion.md#41-训练消融)。 | passed：单一 Table 1、完整标题/行列、无相邻正文，`1320×265` 原分辨率 QA。 |
| Figure 5 | PDF p.7，`1654×2339` @ 200 DPI；bbox xyxy `(170,185,1490,735)` | AR、diffusion 与 linear self-speculation 三种推理路径；quadratic 路径另见原文 Figure 12。 | [asset](../assets/papers/nemotron-labs-diffusion/fig5-tri-mode-inference-caption.png)；支撑[三种推理路径](../papers/nemotron-labs-diffusion.md#32-三种推理路径)。 | passed：单一 Figure 5、完整 caption、`1320×550` 原分辨率 QA。 |
| Figure 9 | PDF p.14，`1654×2339` @ 200 DPI；bbox xyxy `(170,1700,1490,2115)` | RTX Pro 6000、GB200 和 DGX Spark 上不同系统的 per-user throughput trade-off。 | [asset](../assets/papers/nemotron-labs-diffusion/fig9-throughput-hardware-caption.png)；支撑[系统吞吐](../papers/nemotron-labs-diffusion.md#43-系统吞吐)。 | passed：单一 Figure 9、完整 caption、`1320×415` 原分辨率 QA。 |

