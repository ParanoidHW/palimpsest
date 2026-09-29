# DPara Figure Inventory

论文：*When Parallel Drafter Meets Parallel Speculative Decoding*，arXiv:2609.27396v1。坐标为 1700×2200 PNG 像素，bbox 为 `(x,y,width,height)`；所有对象均由 PDF 页渲染后紧裁剪，保留完整 caption。contact-sheet 初筛和逐图 100% 原分辨率检查：2026-09-29，结果均通过。

| Object | PDF page | Source dimensions | Crop bbox | Caption | Process crop | Formal asset | Supporting claim/section | QA |
|---|---:|---|---|---|---|---|---|---|
| Figure 1 | 1 | 1700×2200 | (250,1110,1280,610) | Performance of DPara and other baselines on Qwen3-14B... | `../assets/papers/dpara/fig1-performance-caption.png` | `../assets/papers/dpara/fig1-performance-caption.png` | 主结果与吞吐-延迟折中，§5.1 | pass |
| Figure 2 | 2 | 1700×2200 | (250,180,1280,560) | SSD drafts and verifies a batch of requests together... | `../assets/papers/dpara/fig2-ssd-fallback-caption.png` | `../assets/papers/dpara/fig2-ssd-fallback-caption.png` | 现有方案失败场景，§2.1–2.2 | pass |
| Figure 3 | 3 | 1700×2200 | (250,160,1280,700) | Scheduling of drafting and verification across speculative decoding paradigms... | `../assets/papers/dpara/fig3-schedules-caption.png` | `../assets/papers/dpara/fig3-schedules-caption.png` | 调度总览，§4.1 | pass |
| Figure 4 | 4 | 1700×2200 | (250,150,1280,700) | One decoding step of DPara... | `../assets/papers/dpara/fig4-dpara-step-caption.png` | `../assets/papers/dpara/fig4-dpara-step-caption.png` | 单轮机制，§0.2、§4.3 | pass |
| Figure 5 | 5 | 1700×2200 | (760,1260,620,500) | Input regimes of DFlash and M-DFlash... | `../assets/papers/dpara/fig5-multiple-anchor-caption.png` | `../assets/papers/dpara/fig5-multiple-anchor-caption.png` | 多锚点输入动机，§4.2 | pass |
| Figure 6 | 6 | 1700×2200 | (700,430,700,680) | M-DFlash attention mask for d=3... | `../assets/papers/dpara/fig6-mask-caption.png` | `../assets/papers/dpara/fig6-mask-caption.png` | 树状 mask，§4.3 | pass |
| Table 1 | 7 | 1700×2200 | (200,120,1450,620) | DPara against parallel and serial speculative decoding baselines... | `../assets/papers/dpara/table1-main-results-caption.png` | `../assets/papers/dpara/table1-main-results-caption.png` | 主结果，§5.1 | pass |
| Figure 7 | 8 | 1700×2200 | (200,950,1450,560) | Left: anatomy of one speculation round... | `../assets/papers/dpara/fig7-latency-resource-caption.png` | `../assets/papers/dpara/fig7-latency-resource-caption.png` | 延迟与异构部署，§8 | pass |
| Table 2 | 8 | 1700×2200 | (760,90,720,700) | Batched inference on Qwen3-8B/14B... | `../assets/papers/dpara/table2-batched-caption.png` | `../assets/papers/dpara/table2-batched-caption.png` | batch 结果，§5.1 | pass |
| Figure 8 | 9 | 1700×2200 | (200,120,1450,650) | Left: Qwen3-8B speedup... Right: acceptance length gains... | `../assets/papers/dpara/fig8-ablation-caption.png` | `../assets/papers/dpara/fig8-ablation-caption.png` | 消融与资源折中，§5.2 | pass |
| Figure 10 | 13 | 1700×2200 | (200,80,1450,600) | Fraction of speculation steps in which SSD falls back... | `../assets/papers/dpara/fig10-fallback-rate-caption.png` | `../assets/papers/dpara/fig10-fallback-rate-caption.png` | 回退率机制证据，§2.2、§5.3 | pass |

Figure 9（Appendix A）只重复 batch latency 趋势，未嵌入正文；Table 3（sampling）在正文以完整关键数字和文字重述，避免复制冗余 crop。两项均非遗漏，理由是正文已有相邻数字证据。
