---
tags:
  - evidence
  - collection/llm-foundations
  - domain/model-systems
  - status/deep-review
  - topic/long-context
  - method/hybrid-linear-attention
document_type: evidence
domain: llm_foundations
collection: LLM Foundations
review_status: accepted-with-limitations
canonical: true
---

# Linear Attention Transformer 证据索引

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[LLM Foundations README](../README.md)
> - 上位汇总：[Linear Attention Transformer 演化](../surveys/linear-attention-transformer-evolution.md)
> - 复用 Paper：[Kimi K3](../papers/kimi-k3.md)

## 版本与范围

- 当前证据版本：`2.4.0` / `rev-linear-attn-evidence-kimi-linear-20260819`
- 检索截止：`2026-08-14`
- Survey 模式：`hybrid`
- 分桶：10 个方法节点、1 个 benchmark/taxonomy、2 个 native-system adoption；backend/integration 不计为论文。
- 验收结论：Linear Transformer、RetNet、Mamba、Mamba-2/SSD、GLA、DeltaNet、Gated DeltaNet 与 Kimi Linear 已完成独立 PDF/source/代码/视觉/schema 验收并提升为 canonical Paper（accepted-with-limitations）；其余方法仍保留为导航记录。Kimi K3 继续 `link-only` 复用。

## 方法候选与证据状态

| Work | Stable identity | Role | Primary source | Code/kernel locator | Review verdict |
|---|---|---|---|---|---|
| Linear Transformer | arXiv `2006.16236` / ICML 2020 | seminal | [Linear Transformer Paper](../papers/linear-transformer.md) | official code pin recorded in canonical Paper | `accepted-with-limitations`; canonical |
| RetNet | arXiv `2307.08621` | bridge | [RetNet Paper](../papers/retnet.md) | official code pin recorded in canonical Paper | `accepted-with-limitations`; canonical technical report |
| Mamba | arXiv `2312.00752` / COLM 2024 | selective-SSM bridge | [arXiv](https://arxiv.org/abs/2312.00752) | [Mamba Paper](../papers/mamba.md); [state-spaces/mamba](https://github.com/state-spaces/mamba) | `accepted-with-limitations`; 明确非严格 linear attention |
| Mamba-2 / SSD | arXiv `2405.21060` / ICML 2024 | duality bridge | [Mamba-2 / SSD Paper](../papers/mamba-2-structured-state-space-duality.md) | [state-spaces/mamba](https://github.com/state-spaces/mamba) | `accepted-with-limitations`; canonical |
| Gated Linear Attention | arXiv `2312.06635` / ICML 2024 | core | [Gated Linear Attention Paper](../papers/gated-linear-attention.md) | [Flash Linear Attention](https://github.com/fla-org/flash-linear-attention) pinned in canonical Paper | `accepted-with-limitations`; canonical |
| DeltaNet | arXiv `2406.06484` / NeurIPS 2024 | core | [DeltaNet Paper](../papers/deltanet.md) | [Flash Linear Attention](https://github.com/fla-org/flash-linear-attention) pinned in canonical Paper | `accepted-with-limitations`; canonical |
| Gated DeltaNet | arXiv `2412.06464` / ICLR 2025 | core/adoption bridge | [Gated DeltaNet Paper](../papers/gated-deltanet.md) | official NVlabs and current FLA commits pinned in canonical Paper | `accepted-with-limitations`; canonical; OpenReview bodies unavailable |
| Kimi Linear / KDA | arXiv `2510.26692v2` / technical report | recent/method-system bridge | [Kimi Linear Paper](../papers/kimi-linear.md) | official project, paper-era FLA/vLLM and model commits pinned in canonical Paper | `accepted-with-limitations`; canonical; distinct from Kimi K3 |
| Mamba-3 | arXiv `2603.15569` | recent/selective-SSM | [arXiv](https://arxiv.org/abs/2603.15569) | [state-spaces/mamba](https://github.com/state-spaces/mamba) | stable locator verified; fresh review pending |
| Gated DeltaNet-2 | arXiv `2605.22791` | recent | [arXiv](https://arxiv.org/abs/2605.22791) | [NVlabs/GatedDeltaNet-2](https://github.com/NVlabs/GatedDeltaNet-2) | stable locator verified; fresh review pending |

2026 *Linear Attention Architectures: Mechanisms, Trade-offs, and Cross-Layer Routing* 单列 taxonomy/benchmark，稳定 locator 为 [arXiv:2607.07953](https://arxiv.org/abs/2607.07953)；其 benchmark 结论需独立精读后才进入综合，不计入 10 篇方法。

## System adoption database

### Qwen3-Next-80B-A3B

| Field | Value | Evidence class |
|---|---|---|
| Layer count | 48 | official config (`Model`) |
| Hybrid cadence | `3 Gated DeltaNet + 1 Gated Attention` | official model card/config (`Model`) |
| Linear QK/V heads | 16 / 32 | official config (`Model`) |
| Head dimension | 128 | official config (`Model`) |
| Causal convolution | kernel size 4 | official config (`Model`) |
| Native context | 262,144 | official config (`Model`) |
| Extended context | YaRN path to 1M | official model documentation (`Model`) |
| Kernel dependencies | FLA and causal-conv1d locators | official dependency/runtime evidence (`Code`) |
| Serving paths | Transformers, vLLM, SGLang implementation locators | backend evidence (`Runtime`); exact support tier must be checked per release |

Sources: official [model card](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct), raw [config](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct/raw/main/config.json), and [FLA](https://github.com/fla-org/flash-linear-attention). These establish configuration and integration paths, not a matched causal attribution of model quality.

### Kimi K3

Canonical owner: [Kimi K3 Paper](../papers/kimi-k3.md). Stable adopted facts include 69 KDA + 24 Gated MLA layers, bounded decay, delta-rule state update, FlashKDA/KCP, and dual-granularity prefix cache. Original-paper assets remain under `../assets/papers/kimi-k3/`; see the domain [Figure inventory](figure-inventory.md). No asset is copied for this Survey.

## Count buckets

| Bucket | Count | Included records |
|---|---:|---|
| Peer-reviewed method Papers accepted in this task | 6 | Linear Transformer (ICML 2020), GLA (ICML 2024), Mamba-2/SSD (ICML 2024), Mamba (COLM 2024), DeltaNet (NeurIPS 2024), Gated DeltaNet (ICLR 2025); all accepted-with-limitations |
| ArXiv technical-report Papers accepted in this task | 2 | RetNet、Kimi Linear；accepted-with-limitations |
| arXiv/technical-report method nodes used for navigation | 10 | table above |
| Benchmark/taxonomy records | 1 | arXiv `2607.07953`; independent review pending |
| Native-system adoption | 2 | Qwen3-Next, Kimi K3 |
| Optional official backends | not frozen | per-release Transformers/vLLM/SGLang checks required |
| Third-party integrations | not counted | discovery-only unless source and support tier are pinned |

## Visual inventory and QA

New original-paper crops promoted by this revision: `19` across Linear Transformer (4), RetNet (2), Mamba (3), Mamba-2/SSD (2), GLA (2), DeltaNet (2), Gated DeltaNet (2), and Kimi Linear (2); each canonical Paper embeds its owned assets. Each accepted method also owns or is passing the final gate for a unified TikZ architecture diagram with the same tensor/state/gate palette.

Reason for remaining candidates: a qualifying crop must contain one numbered object and complete caption, record PDF page/source dimensions/bbox, pass contact-sheet triage and individual 100% review, and be embedded with an evidence loop. Generated diagrams and README screenshots are not substitutes. Kimi K3 has existing QA-passed crops in the canonical [Figure inventory](figure-inventory.md).

## Claim-to-source matrix

| Survey claim | Source class | Strength | Attribution boundary |
|---|---|---|---|
| feature-map reordering yields fixed prefix state | Linear Transformer paper locator | paper-derived, visual not revalidated | no claim of softmax equivalence |
| RetNet supports parallel/recurrent/chunkwise forms | RetNet paper locator | paper-derived, visual not revalidated | kernel performance not remeasured |
| Mamba is selective SSM, not strict linear attention | paper/repository + taxonomy synthesis | strong boundary classification | similarity of recurrence is not identity |
| GLA uses input-dependent key-wise forgetting and a chunkwise training algorithm | [canonical GLA Paper](../papers/gated-linear-attention.md), original Figure 3/Figure 6, pinned FLA code | strong mechanism and scoped single-H100 system evidence | kernel tricks, normalization and output gate lack complete component-level causal isolation |
| DeltaNet uses erase-then-write correction and WY/UT chunk execution | [canonical DeltaNet Paper](../papers/deltanet.md), original Figure 2/Table 1, pinned FLA code | strong mechanism and scoped kernel evidence | component gain not isolated here; chunk speed is not end-to-end model speed |
| Gated DeltaNet combines scalar decay with delta-rule erase/write and a chunkwise training path | [canonical Gated DeltaNet Paper](../papers/gated-deltanet.md), original Figure 1/Figure 3, pinned NVlabs/FLA code | strong mechanism, matched model evidence and scoped single-H100 throughput | hybrid gains bundle SWA/Mamba2; decode latency and HBM counters are not reported |
| KDA combines channel-wise decay with delta correction and a constrained-DPLR chunk path | [canonical Kimi Linear Paper](../papers/kimi-linear.md), original Figure 2/Figure 7, pinned paper-era FLA/vLLM code | strong mechanism, whole-model matched-recipe evidence and scoped batch-one system evidence | Figure 7 gives about 2.2x TPOT at 1M and batch 1; 6.3x is a different batching/memory scenario; KDA-only attribution remains limited |
| Qwen3-Next has 3:1 hybrid cadence and listed dimensions | official model card/config | strong configuration evidence | model-wide gains remain confounded |
| Kimi K3 has 69 KDA + 24 Gated MLA and prefix-cache stack | canonical Paper and original visuals | strongest local evidence | training data/full production stack remain partly closed |

## Promotion gate

Each remaining candidate requires exactly one fresh `$paper-deep-review` run, unchanged task packet, readable PDF/source, code commit where available, two types of original visual or explicit skip evidence, 100% crop QA, valid paper manifest and deterministic parent verdict. Only then may it become `papers/<slug>.md`, acquire `assets/papers/<slug>/`, enter README, and increment the meta coverage matrix.
