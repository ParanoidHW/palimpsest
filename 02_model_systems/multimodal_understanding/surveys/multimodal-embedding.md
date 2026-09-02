# 多模态嵌入方法综述

> [!info] 文档关系
> - 文档类型：Survey
> - 领域入口：[README](../README.md)
> - 上位汇总：无
> - 证据资产：[Evidence](../evidence/figure-inventory.md)

多模态嵌入将文本、图像、视频或视觉文档编码为可检索向量。DME 的核心路线是“先用大规模对比学习获得覆盖，再用证据定位与跨条件重建补足细粒度语义”，详见 [DME Paper](../papers/douyin-multimodal-embedding.md#核心机制)。该方法的工业价值在于保持双编码器和离线索引接口；其证据边界是消融为累计配方，未完全隔离每个子损失的独立贡献。
