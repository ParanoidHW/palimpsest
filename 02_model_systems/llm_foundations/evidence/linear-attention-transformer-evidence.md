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
review_status: blocked
canonical: true
---

# Linear Attention Transformer 证据索引

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[LLM Foundations README](../README.md)
> - 上位汇总：[Linear Attention Transformer 演化](../surveys/linear-attention-transformer-evolution.md)

## 方法 Paper

| Work | Source | Review status |
|---|---|---|
| Linear Transformer | [arXiv 2006.16236](https://arxiv.org/abs/2006.16236) | blocked PDF/source in isolated review |
| RetNet | [arXiv 2307.08621](https://arxiv.org/abs/2307.08621) | blocked PDF/source in isolated review |
| Mamba | [arXiv 2312.00752](https://arxiv.org/abs/2312.00752) | abstract accessible; PDF/source blocked |
| GLA | [arXiv 2312.06635](https://arxiv.org/abs/2312.06635) | abstract accessible; PDF/source blocked |
| DeltaNet | [arXiv 2406.06484](https://arxiv.org/abs/2406.06484) | blocked PDF/source in isolated review |
| Gated Delta Networks | [arXiv 2412.06464](https://arxiv.org/abs/2412.06464) | blocked PDF/source in isolated review |

## 系统采用

- Qwen3-Next official [model card](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) and [config](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct/raw/main/config.json): 3 Gated DeltaNet : 1 Gated Attention, 48 layers, 256K native context.
- Kimi K3: reuse [canonical Paper](../papers/kimi-k3.md) and [figure inventory](figure-inventory.md), covering KDA bounded decay, FlashKDA/KCP, prefix cache and original visuals.

原论文新裁剪资产数量为 0；不能用生成图或摘要替代缺失的 mechanism/result crop。
