# DFly2 Figure Inventory

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[Speculative Decoding README](../README.md)
> - 上位汇总：[Speculative Decoding evolution](../surveys/evolution.md)
> - 相关文档：[DFly2 Paper](../papers/dfly2.md)

Paper：*DFly2: Turbocharging Long-Context Speculative Decoding by Sharing the Target's Sparsity*，arXiv:2611.34776v1。四张正式图均为官方 PDF 单一编号对象裁剪，caption 包含于图内。原 PDF 页面均为 612×792 pt；最终裁剪按 3× 渲染。bbox 单位为 PDF point，顺序为左、上、右、下。

| 对象 | PDF 页 | 完整原 caption | bbox；最终尺寸 | 正式资产；用途 | QA |
| --- | --- | --- | --- | --- | --- |
| Figure 3 | p. 7；§3.3 | Top-k mass coverage on DS-V4.1-Flash. (a) Mean over slots and layers. Bands span context lengths. (b) Budget 512, own scale. The window stays at 0.13–0.17. (c) Budget 512, averaged as in (a). | (88,62,535,258)；1341×588 px | [fig3-caption.png](../assets/papers/dfly2/fig3-caption.png)；[覆盖率测量](../papers/dfly2.md#为什么上一轮的位置还能用于下一块) | 2026-11-27 原分辨率逐图通过：三面板、轴、完整 caption，无其他对象或周边正文。 |
| Figure 4 | p. 8；§3.3–4 | Overview of DFly2. Each of its three draft layers is paired with one of the target’s DSA layers and reads the KV that layer cached, at the positions its indexer selected. | (88,68,534,306)；1338×714 px | [fig4-caption.png](../assets/papers/dfly2/fig4-caption.png)；[方法](../papers/dfly2.md#草稿器实际借用了什么) | 2026-11-27 原分辨率逐图通过：层配对、图例、完整 caption，无邻近章节。 |
| Figure 5 | p. 9；§4 | (a) DFlash and DSpark build their own KV, while DFly2 reads the target’s KV at its top-k positions. (b) Only the latent KV and the selection pass at run time, so the drafter needs no indexer. | (88,64,534,287)；1338×669 px | [fig5-caption.png](../assets/papers/dfly2/fig5-caption.png)；[缓存来源](../papers/dfly2.md#草稿器实际借用了什么) | 2026-11-27 原分辨率逐图通过：两个面板、完整 caption，无其他编号对象。 |
| Figure 7 | p. 15；§5.3 | Throughput against per-user decode speed on DS-V4.1-Flash, greedy, one point per concurrency level. Labels give the concurrency and, in parentheses, the requests decoding. Dashed guides compare DFly2 with DSpark at equal per-user speed and at equal throughput. Throughput counts the whole deployment. | (88,68,536,272)；1344×612 px | [fig7-caption.png](../assets/papers/dfly2/fig7-caption.png)；[并发吞吐](../papers/dfly2.md#成本账缓存接受数与速度) | 2026-11-27 原分辨率逐图通过：三面板、图例、虚线说明、完整 caption，无相邻表格。 |

四张图已经先由 contact sheet 初筛，再单独检查原分辨率。PDF 与源码归档只在系统临时工作区；正式图是 PDF 裁剪，不冒充源码原图。Table 2–4、6–11 的关键数字在 Paper 正文重建，没有转存表格截图。
