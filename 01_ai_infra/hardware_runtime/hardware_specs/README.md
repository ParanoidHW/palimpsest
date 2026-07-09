# Hardware Specs

本目录保存 GPU/NPU 规格对比表，用于部署可行性、Roofline 和互联瓶颈判断。

## 阅读顺序

1. [不同硬件的规格对比](不同硬件的规格对比.md)：按 architecture、memory、compute、interconnect、software、multimedia 和 deployment 维度横向比较。

## 维护规则

- 规格表属于工作笔记，不替代厂商 datasheet。
- 新增硬件时优先补齐显存容量、带宽、张量算力、互联、TDP 和典型部署形态。
- 与性能建模交叉使用时，优先回到 [Roofline模型](../../performance_modeling/Roofline模型.md) 和 [部署能力评测](../../performance_modeling/部署能力评测-内存算力带宽与通信.md)。
