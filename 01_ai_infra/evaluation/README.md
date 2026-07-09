# 大模型评估

本目录只归档通用、可复用、可核查的大模型评估知识，不归档某个具体项目的实现细节。

## 整理原则

- 优先记录定义、方法、指标边界和常见误区。
- 对变化快的内容，优先记录“怎么评”，不记录“谁最好”。
- 能追溯到一手来源的内容才写成结论；工程近似会明确标注。
- 把“能力评测”和“系统性能评测”分开，避免把 benchmark 分数和服务体验混为一谈。
- 公式优先用 LaTeX，结构图优先用 Mermaid；这类知识图更适合确定性表达，不依赖生成式位图。

## 当前笔记

- [能力评测-维度与常用基准](能力评测-维度与常用基准.md)
- [评测设计-复现污染与裁判偏差](评测设计-复现污染与裁判偏差.md)
- [部署能力评测-内存算力带宽与通信](../performance_modeling/部署能力评测-内存算力带宽与通信.md)
- [系统性能评测-延迟吞吐与Roofline](../performance_modeling/系统性能评测-延迟吞吐与Roofline.md)
- [kernel开销计算逻辑](../performance_modeling/kernel开销计算逻辑.md)
- [图示生成Prompt-imagegen](图示生成Prompt-imagegen.md)

## 一页判断

- 单一 benchmark 不能代表模型总体能力。HELM 明确把评测拆成多场景、多指标，而不是只看准确率。
- 对可验证任务，优先使用客观评分；对开放式任务，再考虑偏好评测或 LLM-as-a-judge。
- 多项选择题、答案提取规则、选项顺序这类细节，会实质影响排行榜结果。
- 公开 benchmark 需要默认存在污染风险；污染检测也不能只靠 n-gram 匹配。
- 对 infra 来说，先问“这套硬件能不能高效部署这个模型”，再问“部署后服务指标如何”。

## 核心来源

- HELM: https://arxiv.org/abs/2211.09110
- MMLU: https://arxiv.org/abs/2009.03300
- GSM8K: https://arxiv.org/abs/2110.14168
- IFEval: https://arxiv.org/abs/2311.07911
- MT-Bench / LLM-as-a-Judge: https://arxiv.org/abs/2306.05685
- Chatbot Arena: https://arxiv.org/abs/2403.04132
- Length-Controlled AlpacaEval: https://arxiv.org/abs/2404.04475
- Benchmark contamination: https://arxiv.org/abs/2401.06059
- Rephrased contamination / stronger decontamination: https://arxiv.org/abs/2311.04850
- Benchmark sensitivity: https://arxiv.org/abs/2402.01781
- LiveBench: https://arxiv.org/abs/2406.19314
- vLLM benchmark metrics: https://docs.vllm.ai/en/stable/api/vllm/benchmarks/serve/
- MLPerf Inference policies: https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc
- Roofline: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.pdf
