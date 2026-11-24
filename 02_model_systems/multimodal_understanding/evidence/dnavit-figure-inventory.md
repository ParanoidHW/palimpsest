# dNaViT 图表证据清单

> [!info] 文档关系
> - 文档类型：Evidence
> - 领域入口：[README](../README.md)
> - 上位索引：[Paper Index](paper-index.md)
> - 跨域汇总：[Diffusion 多模态生成与 AI Infra](../../multimodal_generation/surveys/multimodal-diffusion-infra.md)
> - 相关文档：[dNaViT Paper](../papers/dnavit.md)

来源：arXiv:2611.12426v1，官方 32 页 PDF；PDF 页面坐标单位为 point，页面均为 612×792 pt。资产从原 PDF 以 2 倍采样裁剪。2026-11-24 先看六图 contact sheet，再逐张打开最终 PNG 原始分辨率检查单一编号、完整图注、文字与边界。bbox 以 PDF 左上为原点，格式为 `(x0,y0,x1,y1)`；图像四边安全余量约 6–16 px，图注与示意内部标签完整。

| Paper / Object | 来源、完整 caption 中文转述 | Crop、正式资产 | 用途、逐图 QA |
|---|---|---|---|
| dnavit / Figure 3 | v1 PDF p.5。dNaViT 总览：(a) 冻结的表征编码器支持任意分辨率；ResMod 在分组乘积量化前注入多层信息，共享离散码分别经 ViT 像素与语义解码器重建；(b) ResMod 融合中间特征并预测零初始化的缩放与平移残差；(c) 两分支分别用图像与特征重建损失优化。 | `(68,65,544,344)`；[fig3](../assets/papers/dnavit/fig3-architecture-caption.png)，952×558 px | [方法总览](../papers/dnavit.md#从具体任务看问题)；原分辨率 QA 通过 2026-11-24：图注完整，三个子图可读。 |
| dnavit / Figure 4 | v1 PDF p.7。视觉编码及多任务统一码：(a) 每个位置的调制特征按通道分成 $G$ 组，由各组码本量化为一组索引及向量；(b) 理解仅将索引经新建、与 LM 联训的组嵌入表送入 LM；(c) 重建将冻结码本的向量串接送入像素解码器；(d) 生成/编辑用 LM 的多子 token 头预测各位置多组索引，可选参考图条件，随后经同一冻结码本和像素解码器输出。 | `(68,68,544,360)`；[fig4](../assets/papers/dnavit/fig4-code-interface-caption.png)，952×584 px | [码本接口](../papers/dnavit.md#2-每个空间位置使用多个码本)；原分辨率 QA 通过 2026-11-24：四个子图与图注完整。 |
| dnavit / Figure 6 | v1 PDF p.10。码条件 Refiner：码向量通过全局上下文 token 和时间条件空间残差进入 flow 解码器；多步教师通过对抗监督蒸馏为一步学生。图中时间 $t$ 对应公式中的 $\tau$。G64 增大组数提高重建保真，G16 搭配一步 Refiner 保留保真并改善感知质量。 | `(68,65,544,388)`；[fig6](../assets/papers/dnavit/fig6-refiner-caption.png)，952×646 px | [额外解码器](../papers/dnavit.md#4-高保真解码器是额外组件)；原分辨率 QA 通过 2026-11-24：示例、图注、图例完整。 |
| dnavit / Figure 7 | v1 PDF p.11。三阶段训练：连续像素预训练、离散语义重建、联合重建；第二阶段停止码向量上的像素梯度，第三阶段打开该路径，冻结的第二阶段 ResMod 提供特征目标；火焰/雪花表示训练/冻结模块，紫色虚线表示固定目标。 | `(68,65,544,404)`；[fig7](../assets/papers/dnavit/fig7-training-caption.png)，952×678 px | [训练步骤](../papers/dnavit.md#3-双分支约束与三阶段训练)；原分辨率 QA 通过 2026-11-24：三阶段及图注完整。 |
| dnavit / Figure 8 | v1 PDF p.19。残差特征融合的像素和表征损失：较 SelfDistill，ResMod 后期像素 MSE 和表征余弦损失更低，说明视觉细节和语义表征的保留指标均改善。 | `(68,65,544,244)`；[fig8](../assets/papers/dnavit/fig8-resmod-loss-caption.png)，952×358 px | [机制对照](../papers/dnavit.md#实验告诉了我们什么)；原分辨率 QA 通过 2026-11-24：双图坐标、线条与图注完整。 |
| dnavit / Table 9 | v1 PDF p.19。连续与离散表征的视觉理解：连续特征比较有无 ResMod；计算八项基准平均分时，OCRBench 先除以 10。 | `(68,247,544,360)`；[table9](../assets/papers/dnavit/table9-continuous-discrete-caption.png)，952×226 px | [连续/离散对照](../papers/dnavit.md#实验告诉了我们什么)；原分辨率 QA 通过 2026-11-24：所有行列、注释与图注可读。 |

其余 Table 1–8 的决策相关行列数值在 Paper 正文转写，原 PDF 表格未裁成正式资产；Figure 5、Figure 9 为定性对比，Paper 对其限制做文字说明，本次不以其替代定量证据。Figure 1/2 属于高层概览和案例展示，Figure 3/4 提供更完整的算法路径。未引用的图表不计入已完成视觉 QA。
