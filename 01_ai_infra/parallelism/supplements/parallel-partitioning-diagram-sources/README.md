---
tags:
  - supplement
  - collection/parallel-partitioning
  - domain/ai-infra
document_type: supplement
domain: parallelism
canonical: false
---

# 并行切分示意图 TikZ/LaTeX 源码

> [!info] 文档关系
> - 文档类型：Supplement
> - 领域入口：[README](../../README.md)
> - 上位 Survey：[并行切分方法体系](../../surveys/parallel-partitioning-taxonomy.md)
> - 图表清单：[Figure Inventory](../../evidence/figure-inventory.md)
> - 正式资产：[`assets/surveys/parallel-partitioning-taxonomy/`](../../assets/surveys/parallel-partitioning-taxonomy/)

本目录保存已通过视觉 QA 的教学整理图的可编辑源码。每个 `.tex` 文件均包含完整 LaTeX 导言和 TikZ 图形定义，可独立编译；PNG 仍是 Survey 正式引用的展示资产，源码仅作为复现与后续维护的辅佐材料。

| 方法 | TikZ/LaTeX 源码 | 对应正式 PNG | 目标分辨率 |
|---|---|---|---|
| 普通 DP | [dp-training-workflow.tex](dp-training-workflow.tex) | [dp-training-workflow.png](../../assets/surveys/parallel-partitioning-taxonomy/dp-training-workflow.png) | `2400x1350` |
| ZeRO-1 / ZeRO-2 / ZeRO-3 | [zero-training-workflows.tex](zero-training-workflows.tex) | [zero1](../../assets/surveys/parallel-partitioning-taxonomy/zero1-training-workflow.png)、[zero2](../../assets/surveys/parallel-partitioning-taxonomy/zero2-training-workflow.png)、[zero3](../../assets/surveys/parallel-partitioning-taxonomy/zero3-training-workflow.png) | `2400x1350` |
| TP / EP | [layer-partitioning-review.tex](layer-partitioning-review.tex) | [TP](../../assets/surveys/parallel-partitioning-taxonomy/tensor-parallel-block.png)、[EP](../../assets/surveys/parallel-partitioning-taxonomy/expert-parallel-routing.png) | `2400x1350` |
| Pipeline Parallel / GPipe | [pipeline-parallel-schedule.tex](pipeline-parallel-schedule.tex) | [pipeline-parallel-schedule.png](../../assets/surveys/parallel-partitioning-taxonomy/pipeline-parallel-schedule.png) | `2400x1350` |
| Megatron Sequence Parallel | [megatron-sequence-parallel.tex](megatron-sequence-parallel.tex) | [megatron-sequence-parallel.png](../../assets/surveys/parallel-partitioning-taxonomy/megatron-sequence-parallel.png) | `2400x1350` |
| Ulysses | [ulysses-layout-transpose.tex](ulysses-layout-transpose.tex) | [ulysses-layout-transpose.png](../../assets/surveys/parallel-partitioning-taxonomy/ulysses-layout-transpose.png) | `2400x1350` |
| Ring / Context Parallel | [ring-context-parallel.tex](ring-context-parallel.tex) | [ring-context-parallel.png](../../assets/surveys/parallel-partitioning-taxonomy/ring-context-parallel.png) | `2100x1125` |
| CFGP | [cfg-branch-parallel.tex](cfg-branch-parallel.tex) | [cfg-branch-parallel.png](../../assets/surveys/parallel-partitioning-taxonomy/cfg-branch-parallel.png) | `2400x1350` |

## 构建

依赖 LuaLaTeX、TikZ 和 `Noto Sans CJK SC`。在本目录执行：

```bash
lualatex -interaction=nonstopmode -halt-on-error <diagram>.tex
pdftoppm -png -f 1 -l 1 -singlefile -scale-to-x <width> -scale-to-y <height> <diagram>.pdf <diagram>
```

中间 PDF、日志和复核 PNG 不应提交到本目录；它们仍属于过程产物。
