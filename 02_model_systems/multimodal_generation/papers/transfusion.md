# Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model 精读分析
> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 多模态生成与 AI Infra](../surveys/multimodal-diffusion-infra.md)
> - 证据资产：`../assets/papers/transfusion/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

> 资料状态：arXiv PDF 与完整 LaTeX source 已取得；正文图表为 PDF 3x 渲染后的紧裁剪。论文未给出官方代码地址，任务包也标记 code unknown；因此实现级结论仅限论文/LaTeX，不能当作代码核验。OpenReview 被 challenge verification 阻断，见 `openreview_reviews.md`。

## 修订信息

- 当前文档版本：`1.0.0`
- 当前修订 ID：`rev-initial-20260712-transfusion`
- 当前修订时间：`2026-07-12T17:44:02+08:00`
- 替代版本：无（initial delivery）

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rev-initial-20260712-transfusion` | `1.0.0` | `2026-07-12T17:44:02+08:00` | `review_transfusion` | initial | 无 | 无 | 首次建立论文、视觉、目标函数与 mixed-serving 审阅 | initial delivery | `analysis.md`; [Figure inventory](../evidence/figure-inventory.md); `openreview_reviews.md` | PDF、LaTeX source、任务包验证问题 | material |

## 0. 资料与配图索引

- 论文与 LaTeX：[arXiv:2408.11039](https://arxiv.org/abs/2408.11039)；核验 PDF SHA-256 `463f4af2...a69705d0`。
- 提取文本：`extracted_text/extracted_text/full_text.clean.txt`（PyMuPDF，23 页）。
- 机制图：Figure 4，`../assets/papers/transfusion/fig4-mixed-attention-mask.png`。
- 结果证据：Table 5 与 Table 8，见 `../assets/papers/transfusion/`；完整 bbox/QA 见 [Figure inventory](../evidence/figure-inventory.md)。
- OpenReview：公开页存在，但 API 与 forum 均被 challenge 阻断；证据见 `openreview_reviews.md`。
- 开源代码/权重：论文、arXiv metadata 与 source 未提供官方仓库或 checkpoint；未验证实现与数值格式。
- AI 生成分析示意图：未生成，原因见第 0.2 节。

## 0.1 术语与符号解释

### 0.1.1 术语表

| 术语 | 本文含义 | 别名 | 不等于/易混项 | 证据来源 |
|---|---|---|---|---|
| Transfusion sequence | 文字 token 与连续图像 patch vector 串接成一条序列；图像块由 BOI/EOI 包围 | mixed-modality sequence | 不是把图像量化为 LM vocabulary token | Sec. 3 Data Representation, arXiv source `03_method.tex` |
| Transfusion attention | 序列块之间保持 causal；同一图像的 patch 内部允许双向注意 | intra-image bidirectional attention | 不是整条序列全双向，也不是 serving 阶段的 cache policy | Sec. 3, Figure 4 |
| LM mode | 逐 token 自回归采样，直到采出 BOI | text decoding mode | 不等于训练期对整段 text 并行算交叉熵 | Sec. 3 Inference |
| diffusion mode | 在 BOI 后附加 n 个纯噪声 patch，迭代 T 次并原位覆写当前图像状态，完成后附 EOI | image decoding mode | 不保留每个历史 diffusion timestep 作为序列 token | Sec. 3 Inference |
| shared model / shared parameters | 同一 Llama-style transformer 主干处理两种模态 | unified transformer | 不等于所有参数共享：text embedding/head 与 image adapters 不共享 | Sec. 3 Model Architecture |
| joint objective | 同一训练 step 中把 text LM loss 与 image DDPM loss 相加 | multi-objective training | 不等于单一概率分布或同一归一化单位；由 lambda 平衡 | Eq. 3 |
| patch compression | 用 linear 或 U-Net down/up 将 k×k latent pixels 映射为一个 transformer vector | image token/patch count reduction | patch 是连续向量，不是 VQ code | Sec. 3; Table 6 |
| noisy-image conditioning | 位于图像之后的 token 在训练时看见 x_t，而非干净 x_0 | downstream conditioning on noisy image | 不等于 inference 最终 EOI 后只见干净解码图；论文未精确说明 cache 重算 | Sec. 3 footnote; Sec. 4.3.4 |
| parity FLOP ratio | 达到 Chameleon 7B 同等指标时，Transfusion 估计所需 FLOPs / Chameleon FLOPs | compute-efficiency proxy | 不是实测 serving latency 或吞吐 | Sec. 4.2, Table 3 |

### 0.1.2 符号表

| 符号 | 含义 | 性质 | 作用域/索引 | 单位/取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|
| `y_i`, `y_<i` | 第 i 个离散 token 及其前缀 | author-defined | text positions | vocabulary item / sequence | Sec. 2.1 | 图像 patch 不属于 y 的 closed vocabulary |
| `P_theta` | 共享参数 theta 下的 token 条件分布 | author-defined | per text token | probability | Eq. LM | theta 也服务 diffusion head，但分布头不同 |
| `x_0`, `x_t`, `x_T` | 干净图像 latent、t 时刻带噪 latent、纯噪声起点 | author-defined | per image / diffusion step | continuous tensor | Eqs. forward/DDPM; Sec. 3 | inference 中 x_t 原位覆写，不扩展为 T 个序列块 |
| `epsilon`, `epsilon_theta` | 注入噪声与模型预测噪声 | author-defined | per image patch/timestep | latent-space tensor | Eq. DDPM | 论文使用 epsilon-prediction，而非 x/v prediction |
| `t`, `T` | 当前 diffusion timestep 与总训练 schedule 长度 | author-defined | per image | integer；训练 1000，推理 250 steps | Sec. 2.2, Sec. 4.1 | 推理 250 并不意味着训练 T=250 |
| `beta_t`, `alpha_bar_t` | 前向噪声 schedule 与累计保真系数 | author-defined | per timestep | scalar | Eq. forward | 采用 cosine schedule |
| `c` | diffusion 条件上下文，如 caption prefix | author-defined | per image/request | transformer context | Sec. 2.2 | 可含早先图像/text；不是独立冻结 text encoder |
| `lambda` | DDPM loss 相对 LM loss 的平衡系数 | author-defined | global training hyperparameter | 5 | Eq. 3; Sec. 4.1 | 未报告系统调参或敏感性，不能视为自然单位转换 |
| `k` | image adapter 聚合的 k×k latent-pixel window 边长 | author-defined | per model variant | 1,2,4,8 | Sec. 3; Table 6 | transformer sequence 中每图 patch 数随 k 平方下降 |
| `n` | diffusion mode 附加的 image patch 数 | author-defined | per requested image size/compression | 16/64/256/1024 in experiments | Sec. 3 Inference; Table 6 | 与 text token count 不同但竞争同一 context length |
| `N`, `D` | 参数量与训练 token/patch 数 | author-defined | scaling experiment | parameters, elements | Sec. 4.2 | `6ND` 是理论 FLOP proxy，不含真实 kernel/attention shape |
| `B`, `L`, `d_h`, `b` | batch、context length、KV head dimension、bytes/element | analysis-derived | serving estimate | request, elements, dimensions, bytes | 第 7 节推导 | 论文未报告 GQA/MQA、dtype，故只给符号公式 |

## 0.2 AI 生成算法分析示意图

已按要求调用 `$openrouter-icu-image` 的 `responses-doc --input-file analysis.md`，显式使用 `1792x1008`、high、PNG。API 返回 HTTP 404：默认模型 `gpt-5.5-medium` 不受当前 account group 支持，request ID `a4f4776c-d323-4c93-8ae5-0a178098638a`。因此生成失败并跳过，不用其他图片替代论文证据。

## 1. 论文基本信息

- 论文：*Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model*，ICLR 2025，arXiv:2408.11039。
- 核心问题：一个 transformer 是否能在离散 text 上做 next-token prediction、在连续 image latent 上做 diffusion，并避免把图像量化为离散 code 的信息瓶颈。
- 范围：预训练从 0.16B 到 7B；主 controlled setting 为 0.5T text/image elements，增强模型为 7B transformer + 0.27B U-Net adapters、2T mixed elements。
- 关键边界：论文证明的是 recipe 的可行性与 scaling；未提供 serving latency、吞吐、KV-cache、kernel、dtype、scheduler 或代码证据。

## 2. 核心贡献与证据边界

1. **统一序列与共享主干**：BOI/EOI 将连续图像 patch 嵌入文字序列，一个 transformer 共享绝大多数参数；modality-specific input/output adapters 仍分离（Sec. 3）。
2. **按模态保留原生 objective**：text 用交叉熵，image 用 epsilon-prediction DDPM MSE，以 lambda=5 相加（Eq. 3）。这是共享参数的多任务目标，不是把 diffusion 改写成 AR。
3. **块状 attention mask**：跨元素保持 causal；同图 patch 内双向。Table 5 对 linear adapter 给出强直接消融，对 U-Net adapter 的增益很小，说明部分收益可由 U-Net 内部双向 mixing 替代。
4. **连续 patch + U-Net adapter 的压缩能力**：Table 6 表明 U-Net 在 16 patches/image 时仍保持 FID 16.1，但 linear 退化到 43.5；然而数据暴露量随 patch 压缩变化，机制与更多 image samples 有混杂。
5. **规模结果**：7.3B、2T model 报告 COCO FID 6.78、GenEval 0.63、Llama suite 66.1（Table 9）。跨论文数据、caption、参数和评测设置不完全匹配，不能作为纯 architecture ablation。

## 3. 研究方法

### 3.1 问题到方案的逻辑链

图像离散化造成量化瓶颈；独立 LLM + diffusion 又重复主干与条件编码。Transfusion 将 mixed samples 序列化，让 text 位置用 categorical loss、image block 用 continuous denoising loss；共享 transformer 学跨模态上下文，mask 同时维护 text causality 与 image spatial set-like interaction。

### 3.2 设计动机与具体问题映射

| 设计项 | why 状态/原文证据 | 具体问题 | 因果机制 | 替代与权衡 | 验证证据 | 判断 |
|---|---|---|---|---|---|---|
| 连续 VAE latent 而非 VQ token | author-stated, Sec. 4.1 Baseline | VQ quantization 信息瓶颈 | 保留连续 latent，以 MSE 学噪声而非 code classification | VQ 可直接用纯 LM 与成熟 AR serving | controlled Transfusion vs Chameleon，但 transformer stability 修改仍不同 | partially supported |
| BOI/EOI mixed sequence | author-stated, Sec. 3 Data Representation | 一个主干需要区分模态边界与切换生成模式 | marker 决定 adapter/loss/decoder state | 独立 cross-attention encoder-decoder 更易调度但不统一 | 可生成 text-image/image-text；无 marker ablation | plausible, not isolated |
| shared Llama-style transformer + modality adapters | author-stated, Sec. 3 Architecture | 避免为每种模态复制大主干 | 大部分参数共享，边缘投影适配离散/连续空间 | separate towers 可专门优化 kernel/容量 | scaling 与 7B results；无 matched shared-vs-separate capacity ablation | partially supported |
| causal-between-blocks + bidirectional-within-image mask | author-stated, Sec. 3 Attention | causal image rasterization阻断后部 patch 对前部 patch 的信息流 | 同图形成 dense block，前序上下文仍单向进入 | 全 causal 易 cache；全 bidirectional 会泄漏未来 text | Table 5 direct ablation | supported，且收益依 adapter 而异 |
| `L_LM + lambda L_DDPM` | author-stated, Sec. 3 Objective | 两模态输出空间/合适 likelihood 不同 | 共享 theta 接收两种梯度，head/objective 保留各自归纳偏置 | all-token LM、flow matching、动态 loss weighting | 与 Chameleon replacement baseline；lambda 无 sensitivity | partially supported |
| U-Net down/up image adapters | inferred + author hypotheses, Sec. 4.3.3 | 大 patch 压缩让 linear adapter 丢局部结构 | U-Net spatial inductive bias 与内部双向 attention 补足局部 mixing | linear 参数少、部署简单；U-Net 增 0.27B 参数/额外 kernels | Table 7 跨规模；非严格同参数 | partially supported |
| 图像前置时限制 t<=500 | author-stated, Sec. 4.3.4 | 后续 caption 在训练时可能只看到严重污染的 image | 限噪提高可恢复视觉条件 | clean-image auxiliary path / two-pass context refresh | Table 8 matched ablation | supported for CIDEr |
| 250-step diffusion inference + CFG | not-stated for exact choices; Sec. 4.1 | image quality/compute trade-off | iterative denoising；CFG 通常双倍 conditional/unconditional compute | DDIM/DPM/flow/consistency distillation | 无 step-count sensitivity；CFG 系数按实验改变 | unverified as optimal |

### 3.3 序列布局与混合 attention mask

![Figure 4 mixed attention mask](../assets/papers/transfusion/fig4-mixed-attention-mask.png)

对序列 `text prefix, BOI, image patches, EOI, later text`，可用块索引表达 mask：

$$
M_{ij}=1 \quad\text{iff}\quad j\le i\;\lor\;(i,j\in I_m),
$$

其中 `I_m` 是同一张图的 patch index set。于是：

- text token 只能看 prefix；
- image patch 能看更早 text/更早 images，并双向看本图所有 patch；
- 后续 text 能看整个更早图像块，但训练时看到的是带噪 `x_t`；
- 不同图片之间仍按序列因果关系，不能互相向未来泄漏。

这不是普通 causal KV-cache 的小改动：生成图像时，同图所有 query 每一步都依赖同图所有更新后的 key/value。跨图像前缀可缓存，但当前 image block 的 K/V 至少需要每个 diffusion step 更新；论文没有实现细节证明更激进的 cache reuse。

### 3.4 目标函数

$$
\mathcal{L}_{LM}=\mathbb{E}_{y_i}[-\log P_\theta(y_i|y_{<i})],
$$

$$
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,
\quad
\mathcal{L}_{DDPM}=\mathbb{E}\|\epsilon-\epsilon_\theta(x_t,t,c)\|_2^2,
$$

$$
\mathcal{L}_{Transfusion}=\mathcal{L}_{LM}+5\mathcal{L}_{DDPM}.
$$

LM loss 按 token 计算（BOI input 不算 loss），DDPM 按 image 计算。论文说“simply adding”，但这隐藏了归一化粒度：一个 image spanning n patches 产生 image-level loss，而 text 是 token-level loss；lambda=5 来自 preliminary experiments，未报告 sensitivity。因此“一个 objective”应准确写成“一个 scalar training objective 聚合两种不同统计单位的损失”。

### 3.5 训练与推理状态机

- 训练：4096-element sequence；batch 2M elements、250k steps（0.5T），或 4M、500k（2T）。text:image element ratio 1:1，不等于样本数 1:1；patch 越少，同样 element budget 可见更多图像。
- text inference：逐 token greedy；采到 BOI 后切换 image mode。
- image inference：附加 n 个 `x_T` patch，250 denoise steps（训练 schedule 1000）；每步以 `x_{t-1}` 原位覆盖 `x_t`；完成后附 EOI 返回 LM mode。
- CFG：controlled comparison coefficient 5，ablation coefficient 3，大模型按 benchmark 调参。标准 CFG 可能需要 conditional/unconditional 两路 forward，论文未报告 batching/fusion。

## 4. 关键结论与证据矩阵

### 4.1 技术 claim evidence matrix

| 技术点 | 声称收益 | 实验 | 控制情况 | 证据强度 | 结论 |
|---|---|---|---|---|---|
| continuous diffusion 优于 VQ image tokens | 更好 scaling/compute efficiency | Figure 5/Table 3 Transfusion vs Chameleon | 数据/compute/VAE 尽量匹配；transformer recipe 不完全相同 | replacement baseline, partially confounded | supported at recipe level，不是纯 loss isolation |
| intra-image bidirectional mask | 更强理解/生成 | Table 5 | 同 size/adapter/patch size matched | direct ablation | linear FID 61.3->20.3；U-Net FID 16.8->16.7 |
| U-Net adapter | 更好 image tasks 与强压缩 | Tables 6/7 | 参数增量与 data exposure 随 patch size/scale变化 | sensitivity/confounded | benefit clear，inductive-bias attribution partial |
| noise limiting for image->text | 提高 captioning | Table 8 | 同 model，limit on/off | direct ablation | CIDEr 25.4->29.4 (0.76B), 33.7->35.2 (7B) |
| lambda=5 | 平衡两目标 | preliminary experiments only | 未公开 | none | unverified sensitivity |
| 250 denoise steps | practical generation | main evaluation | 未做 step/latency curve | none | quality numbers成立；效率最优性未验证 |
| 16 patches lowers serving cost up to 64x | image sequence 1024->16 | Table 6 + token-count arithmetic | 未实测 latency；attention/CFG/adapter overhead omitted | indirect | sequence-work reduction plausible，64x end-to-end cost不成立为实测 |
| 7B/2T 与同级专用模型相当 | joint text+image quality | Table 9 | literature-reported heterogeneous settings | confounded cross-paper comparison | evidence of competitiveness, not architecture causality |

### 4.2 直接消融：mask 与噪声条件

![Table 5 attention ablation](../assets/papers/transfusion/table5-attention-ablation-caption.png)

Table 5 的关键交互：linear adapter 下，bidirectional mask 将 FID 从 61.3 降至 20.3（绝对 -41.0，约 -66.9%）；U-Net 下仅 16.8->16.7（-0.1，约 -0.6%）。这支持作者解释：U-Net 自身已有双向 attention，削弱 transformer mask 的边际贡献。不能把 linear 的巨大增益外推到最终 U-Net 7B serving model。

![Table 8 noise limit ablation](../assets/papers/transfusion/table8-noise-limit-caption.png)

Table 8 显示 mixed sequence 的一个真实冲突：diffusion 训练需要随机大噪声，但 image->text 需要可辨识视觉条件。限制 t<=500 后，0.76B CIDEr +4.0（+15.7%），7B +1.5（+4.5%），其他指标变化小。这是“按 sequence position/任务动态选择 diffusion corruption”的直接依据，而不是统一 objective 自动消除冲突。

### 4.3 收益归因

| 变化 | 指标变化 | 影响路径 | 归因强度 |
|---|---|---|---|
| causal -> intra-image bidirectional, linear | FID -41.0 | spatial information flow | matched direct |
| causal -> intra-image bidirectional, U-Net | FID -0.1, CIDEr +2.1 | transformer mask 与 U-Net mixing 重叠 | matched direct |
| noise cap, 0.76B | CIDEr +4.0 | cleaner image conditioning | matched direct |
| U-Net 2x2 vs linear 2x2, 7B | FID 18.6->16.0, CIDEr 27.2->33.7 | spatial adapter + 3.8% params | matched scale but capacity confounded |
| 1024->16 patches with U-Net, 0.76B | FID 21.0->16.1，text metrics下降 | shorter sequence + more images seen + adapter | multi-factor sensitivity, not clean attribution |
| 0.5T controlled -> 2T enhanced model | FID 16.0->6.78 cannot be directly computed as matched delta | more data, changed mixture, tuning, same broad recipe | confounded; do not attribute solely to architecture |

## 5. Related Work 对比

| 类别 | 机制 | 优点 | 局限 | 与本文关系 |
|---|---|---|---|---|
| Chameleon / discrete unified LM | VQ image codes + next-token LM | 单一 AR runtime、成熟 KV cache | quantization bottleneck、长 image token sequence、training instability modifications | 主要 controlled baseline |
| LLaVA/Flamingo-style understanding | pretrained LM + visual encoder/projection | 复用强组件 | 通常不原生生成图像 | Transfusion 从零训练并双向生成 |
| GILL/DreamLLM/tool/grafted diffusion | LM 调用或连接独立 diffusion | 模态专用能力强 | 多主干、条件接口与 serving 资源重复 | Transfusion 共享 transformer 主干 |
| 专用 latent diffusion | text encoder conditions denoiser | image generation成熟 | 不生成 text，通常需冻结 text encoder | Table 9 仅作异构 literature comparison |

公平性判断：Transfusion vs Chameleon 最接近 controlled，但 Chameleon 为稳定性改变 QK norm、post-norm、denominator loss 与 LR，故差异是 recipe bundle。Table 9 对 SD/Imagen 等的训练数据、synthetic captions、reranking、冻结 encoder 均不同，只能说明量级竞争力。

## 6. OpenReview 公开评审交叉核验

OpenReview forum 已知，但 2026-07-12 的 v1/v2 API 与 HTML 都返回 challenge verification；无法读取 review、meta-review、decision、rebuttal 或 discussion。详见 `openreview_reviews.md`。因此不存在可合法填入的 reviewer claim 表，也不把“ICLR 2025”反推为 reviewer 对 novelty/正确性的认可。

影响：PDF/source 足以核验方法与数字；但无法判断作者是否在 rebuttal 中补充 lambda sensitivity、代码承诺、baseline 公平性或 serving 细节。本报告将这些保持为未解决问题。

## 7. Infra 与 mixed serving  implications

### 7.1 计算形态：同权重，不同节拍

text decode 每次追加 1 token，典型是低 arithmetic intensity 的小 batch decode；image decode 每次同时更新 n 个 image queries，重复约 250 steps，且 CFG 可能双路 forward。两者共享 weights 适合权重驻留，但 shape 与 deadline 完全不同：

$$
C_{text}\approx m\,C_{step}(1,L),\quad
C_{image}\approx T_{infer}\,g\,C_{step}(n,L+n),
$$

其中 m 是生成 token 数，`T_infer=250`，`g` 约为 1 或 CFG 导致的 2 路系数（是否融合未知）。论文没有 latency，不能把 parity FLOP ratio 当 serving speedup。

### 7.2 KV-cache 与 block 更新

对 transformer 每层，缓存前缀 KV 的字节量可写为：

$$
S_{prefix}=2B L h_{kv}d_h b.
$$

AR text 每步只新增一个位置；当前 image block 在每次 diffusion step 的 hidden state 都变化，故其 KV 也变化：

$$
Traffic_{imageKV}\gtrsim 2B T_{infer} n h_{kv}d_h b.
$$

前缀 text/image history 可复用，当前 image block 不能按普通 append-only cache 原样复用。若完成图像后 EOI/later text 需要 clean final image 的 KV，runtime 还需确保 cache 对应最终 x_0，而非某个旧 x_t。论文未描述此 refresh，属于实现关键缺口。

### 7.3 batching 与 scheduler

推荐从机制推导出双队列/阶段感知调度，而非把所有 request 塞入一个 token batch：

| 阶段 | shape | cache 行为 | scheduler 需求 | 风险 |
|---|---|---|---|---|
| AR prefill | BxL | 建立 prefix KV | length bucketing | 长图像历史挤占 context/HBM |
| AR decode | Bx1 | append-only | continuous batching、低延迟 | 被大 image step 阻塞 |
| diffusion step | Bxn | current block overwrite/recompute | 按 n、t、CFG mode 分桶 | 250-step residency 与 head-of-line blocking |
| EOI transition | Bx1 | commit final image KV | cache consistency barrier | 旧 x_t KV 泄漏到 later text |

同一 GPU 可复用 7B weights，但在线服务更合理的是 time-sliced microbatch 或空间隔离：AR decode 保持短 quantum，diffusion 用较大矩阵提高利用率；按 SLO 动态给 diffusion steps 限额。跨模式动态 batching 只有当 kernel shape、mask 与 adapter path 兼容时才有价值。

### 7.4 patch compression 的真实系统意义

32x32 latent grid 对应 n=1024；k=2/4/8 对应 256/64/16。n 降 64x 会线性降低当前 image block KV/activation，且 image-image attention 项约按 n^2 降低；但端到端不会必然 64x，因为 transformer prefix、250 steps、CFG、U-Net adapter、VAE 编解码仍在。论文的“up to 64x serving costs”是 token-count proxy，没有 telemetry。

### 7.5 dtype、带宽、互联与异构

- 论文未报告 fp32/fp16/bf16/fp8、KV dtype、accumulation precision、quantization 或 custom kernel；任何具体数值格式均未验证。
- 7B weights 若以 b bytes/parameter 存储，单副本约 `7e9*b` bytes；U-Net 增 0.27B。bf16 的 14 GB 只是条件推导，不是 paper-reported deployment。
- 多 GPU 训练使用何种 TP/DP/FSDP、NVLink/RDMA、all-reduce volume 未报告，因此无法计算 effective bandwidth/utilization。
- CPU 可能负责 tokenizer、VAE I/O、image decode/postprocess 与 scheduler；GPU/NPU 执行 transformer/diffusion/U-Net，但论文没有 placement、DMA、pinned memory、async copy 或 NPU kernel 证据。
- 异构 accelerator 的困难在于 block mask、RoPE、U-Net adapters 与动态 mode switch 需要完整算子覆盖；fallback 到 CPU 会破坏 250-step latency。此为系统推断，非作者结论。

## 8. 开源代码与 checkpoint 对照

论文 source、arXiv metadata 与 task packet 均无官方 code URL；未发现论文声称公开 checkpoint。因此 code snapshot 和 checkpoint metadata 属于 unavailable/not applicable，而不是“README 未核验”。没有 commit 可引用，mask materialization、loss normalization、cache refresh、CFG fusion、dtype、parallelism 均不得声称已实现。

## 9. 优点、局限与 evidence loop

### 优点

- 统一 recipe 简洁，数学上明确保留两种模态合适的 objective。
- Table 5/8 给出与核心 mixed-sequence 机制直接相关的 matched ablation。
- controlled baseline 尽量匹配数据、compute、VAE，并公开 transformer recipe 差异。
- patch count 是连接算法与 serving 的清晰控制旋钮。

### 局限

- lambda=5、250 steps、loss normalization 与 mode sampling 缺 sensitivity。
- shared-vs-separate 主干没有同总参数/同 FLOPs的 matched ablation。
- 2T 主结果同时改变数据量、数据混合、adapter 与调参，架构/规模效应不可分。
- 无代码、dtype、kernel、KV-cache、throughput、latency、SLO 或 power 证据。
- OpenReview 评审/反驳受 challenge 阻断。

### Evidence loop

Claim（统一模型可同时做 AR text 与 diffusion image）-> mechanism（mixed sequence、block mask、双 objective、mode-switch inference）-> measurement（Tables 3/5/8/9）-> boundary（mask 仅在 matched Table 5 被隔离；大模型结果存在数据/配置混杂）-> implementation limitation（无代码与 serving telemetry）。因此可把 Transfusion 作为“统一 AR+diffusion recipe”的成立证据，但不能把它作为“统一 runtime 已实现高吞吐”的证据。

## 10. 研究启发

- 做 mode-aware serving benchmark：固定 7B weights，对 AR-only、diffusion-only、交错 text-image-text 三类 workload 分别测 TTFT、TPOT、image latency、HBM、cache rebuild 与公平调度。
- 用 clean-final-image KV commit 对比全 block recompute，验证 later-text correctness 与 latency。
- 在相同 image exposure 而非相同 element budget 下复做 patch-size ablation，拆开 compression 与更多数据样本效应。
- 对 lambda、noise cap、diffusion steps 做 Pareto surface，而非单点选择。
- 将 DDPM 换 flow matching/consistency objective，重点测 step count 是否改变 mixed scheduler 的可行性。

## 11. 待验证问题

1. DDPM loss 是对 patch、维度、image 如何 reduce 后再乘 lambda？
2. 多图 sequence 是否为每张图独立采 t，mask/kernel 如何表示多个 dense blocks？
3. diffusion 完成后，later text 使用最终 image block 的 KV 是否完整重算？
4. CFG conditional/unconditional passes 是否可共享 prefix KV、是否 fused batching？
5. 16-patch 模型的端到端 latency 是否真有接近 64x，还是仅 current block token work？
6. shared transformer 相对相同总参数的 separate LM+diffusion 是否节省吞吐/显存？
7. lambda 与 text:image element ratio 的联动是否导致梯度冲突或容量偏置？
8. OpenReview rebuttal 是否提供代码、额外消融或 baseline 公平性说明？

## 12. 一句话总结

Transfusion 的关键不是把图像“自回归化”，而是在同一因果 mixed sequence 和共享 transformer 上，为 text 保留 next-token loss、为 image block 保留双向 diffusion；论文证明了 recipe 与若干机制，但 mixed serving 的 batching、cache consistency 与 250-step 调度仍完全是待实现、待测量的系统问题。
