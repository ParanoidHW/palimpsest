# 示意图文本描述：Diffusion 多模态生成、统一理解生成与 AI Infra 趋势

## 图意概述

这是一张自上而下的技术演进示意图，标题为“Diffusion 多模态生成、统一理解生成与 AI Infra 趋势”，副标题为“从算法趋势到负载、运行时、Kernel、内存互连与硬件”。图的主线展示：算法侧的多模态统一生成发展，如何逐步改变计算负载，并进一步提出运行时调度、可编程 Kernel、内存与互连、以及硬件协同的系统需求。

## 整体版式

- 白色背景，深蓝色细边框、箭头与强调文字；正文以黑色为主。
- 左侧约四分之三宽度为六个纵向堆叠的圆角矩形模块，每个模块左上角有深蓝底白字的编号方块（1 至 6）。
- 每个模块有各自独立的小logo
- 相邻模块之间由居中的蓝色向下箭头连接，箭头上方或附近依次标注“导致”“要求”“落到”“依赖”“映射到”。

## 六层链路

### 1. 算法&场景趋势

首层包含五个并列小框：

1. 多轮对话与编辑：VLM + Diffusion协同，多阶段分离部署，kvcache复用
2. MoT架构：AR Reasoner + Diffusion Generator，独立权重但共同attention
3. World-action-model：根据输入动作实时流式生成视频，用于具身智能场景生成数据
4. 音画同步：同时生成音频和视频，两者是时间同步的

模块底部总结为：“高质量单图与短视频已具备产品成熟度，但长视频叙事、稳定物理交互、低延迟双向音视频和实时世界模型仍处于快速迭代期。未来应用重心将从一次性 prompt-to-content 转向多轮编辑、可控代理创作、音画同步、交互仿真和具身数据生成”。

### 2. 工作负载变化

第二层包含五个小框，描述由算法带来的计算和数据访问特征：

1. 长序列压力来源：重复 denoise step = prefill-like 大矩阵计算
2. AR KV 与 Diffusion Feature 并存，多轮编辑与复用
3. VAE / Codec 成为独立负载
4. Diffusion feature cache引入多级缓存
5. 实时流式生成要求低时延

### 3. Serving / Runtime 要求

第三层有六个小框：

1. Phase-aware Scheduler / Prefill-Decode-Diffusion
2. AR 阶段与生成阶段切换
3. Resolution / Frame / Step Bucketing
4. Deadline-aware Stream Queue
5. Feature Cache 准入 / 淘汰
6. Topology-aware Parallelism

底部说明：“不能只扩展 token scheduler”。

### 4. 关键 Kernel

第四层有五个小框：

1. Varlen / Full / Causal / Two-way / Flex Attention
2. Block Sparse / Window / Selected Global
3. Custom Mask Lowering / General Mask Repr.
4. Sparse Attention Workload Balance
5. FP8 / MxFP8 / MxFP4 / HiF4 Attention

### 5. 内存与互连

第五层包含五个小框：

1. HBM 容量与带宽
2. 多级 Cache：HBM / CPU / NVMe
3. Feature Prefetch
4. NVLink / RDMA
5. One-sided Communication
