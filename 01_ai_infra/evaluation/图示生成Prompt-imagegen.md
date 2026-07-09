# 图示生成Prompt-imagegen

## 资料边界

- 用途：保存可复用的 image generation prompt，用于 AI Infra 评测类图示。
- 本地资产：当前目录不保存生成图；如后续沉淀成正式图片，需要在 README 的资产说明中登记。
- 使用建议：优先用 Mermaid 表达确定性结构，位图只用于分享、汇报或封面风格材料。

这份笔记不包含具体项目实现，只保存后续可复用的位图示意图 prompt。

说明：

- 当前知识库里的结构图优先用 Mermaid，因为这类维度分解图更适合确定性表达。
- 如果后续需要更适合分享、汇报或封面风格的位图示意图，可以直接复用下面的 prompt。

## Prompt 1：Kernel 评估维度分解图

```text
Use case: scientific-educational
Asset type: knowledge base illustration for LLM kernel evaluation
Primary request: create a clean technical infographic that explains how kernel performance evaluation is decomposed into FLOPs, DRAM bytes, operational intensity, compute roof, bandwidth roof, runtime overhead, and stage-level total time
Scene/backdrop: minimal light background with subtle grid, no photoreal scene
Subject: a central kernel-analysis pipeline diagram with arrows and labeled modules
Style/medium: polished scientific infographic, publication-friendly, flat 2.5D technical illustration
Composition/framing: landscape, left-to-right flow, large readable labels, enough whitespace, one main pipeline with two example side callouts
Lighting/mood: neutral, precise, analytical
Color palette: slate blue, teal, amber, graphite, off-white
Materials/textures: crisp vector-like surfaces rendered as high-quality bitmap, no painterly texture
Text (verbatim): "Kernel Description", "FLOPs", "DRAM Bytes", "Operational Intensity", "Compute Roof", "Bandwidth Roof", "Launch/Sync Overhead", "Stage Time", "GEMM Example", "LayerNorm Example"
Constraints: scientifically clean, no extra decorative objects, no logos, no watermark, no fake equations, all labels must be spelled correctly and readable
Avoid: hand-drawn style, messy poster layout, purple-heavy palette, clutter, tiny text, pseudo-code blocks
```

## Prompt 2：系统性能评测维度分解图

```text
Use case: scientific-educational
Asset type: knowledge base illustration for LLM serving evaluation
Primary request: create a clean technical infographic that decomposes LLM serving performance evaluation into workload definition, queueing, prefill, decode, network synchronization, postprocess, latency metrics, throughput metrics, and SLO-constrained goodput
Scene/backdrop: minimal neutral background with faint metric-grid texture
Subject: a layered serving pipeline diagram with one request timeline and one metrics panel
Style/medium: modern systems-performance infographic, presentation-ready, crisp bitmap
Composition/framing: wide 16:9 layout, central timeline, metric panels on the right, dimension tags on the left
Lighting/mood: calm, precise, engineering-focused
Color palette: deep navy, cyan, signal orange, moss green, warm gray
Materials/textures: smooth infographic surfaces, sharp lines, high text legibility
Text (verbatim): "Workload", "Queue", "Prefill", "Decode", "Network/Sync", "Postprocess", "TTFT", "TPOT", "ITL", "E2EL", "Throughput", "Goodput", "SLO"
Constraints: clear hierarchy, readable labels, no logos, no watermark, no mock UI chrome, no fake benchmark numbers
Avoid: futuristic cityscape, dashboard clutter, irrelevant server-room photography, glossy 3D excess, tiny labels
```

## Prompt 3：Kernel 与系统评测的关系图

```text
Use case: scientific-educational
Asset type: overview illustration for knowledge base section divider
Primary request: create a high-level conceptual illustration showing the relationship between kernel-level upper-bound modeling and system-level end-to-end serving evaluation for large language models
Scene/backdrop: abstract technical background, subtle layered grid and data-flow lines
Subject: left side shows kernel roofline style blocks, right side shows end-to-end request pipeline, center shows how micro-level cost feeds macro-level latency and throughput
Style/medium: elegant educational concept art, still rigorous and uncluttered
Composition/framing: panoramic horizontal layout, strong left-right contrast, one clear center bridge
Lighting/mood: thoughtful, analytical, not dramatic
Color palette: steel blue, muted teal, amber highlight, neutral gray
Text (verbatim): "Kernel Upper Bound", "Memory vs Compute", "Request Timeline", "Latency", "Throughput", "Goodput"
Constraints: clean typography, correct spelling, no logos, no watermark, not too abstract to read
Avoid: sci-fi scenes, random chips, exaggerated neon glow, unreadable labels
```
