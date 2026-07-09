# Performance Modeling

本目录保存 AI Infra 里的性能建模笔记，覆盖从单 kernel 上界到部署可行性、在线服务 QoS 的分层判断。

## 阅读顺序

1. [Roofline模型](Roofline模型.md)：先理解算力屋顶、带宽屋顶和 ridge point。
2. [kernel开销计算逻辑](kernel开销计算逻辑.md)：把 Roofline 落到单 kernel 的 FLOPs、Bytes 和 overhead 估算。
3. [部署能力评测-内存算力带宽与通信](部署能力评测-内存算力带宽与通信.md)：把模型、硬件和并行策略映射成容量、计算、访存与通信约束。
4. [系统性能评测-延迟吞吐与Roofline](系统性能评测-延迟吞吐与Roofline.md)：在模型可部署之后评估 TTFT、TPOT、吞吐和 goodput。

## 资产说明

本目录当前不保存图片资产；结构化图示使用 Mermaid，外部公式和来源统一写入各笔记的“来源”小节。

## 维护规则

- 先区分 kernel 上界、部署可行性和线上服务 QoS，不把三类指标混报。
- 所有估算公式需要明确是理论上界、工程近似还是 benchmark 校准值。
- 与能力评测交叉时，回到 [evaluation](../evaluation/) 区分 benchmark 分数和服务体验。
