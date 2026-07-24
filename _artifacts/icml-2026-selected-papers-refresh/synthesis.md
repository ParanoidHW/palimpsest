# ICML 2026 用户题单：模型系统与推理机制增量综述

## 修订信息

- 当前文档版本：`1.0.0`
- 当前修订 ID：`rev-icml2026-refresh-migration-20260724`
- 当前修订时间：`2026-07-24T22:30:00+08:00`
- 替代版本：`unresolved legacy survey delivery`

| 修订 ID | 文档版本 | 时间 | 修订者 | 类型 | 替代修订 | 迁移问题/解析 | 变更摘要 | 原因 | 影响位置 | 依据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rev-icml2026-refresh-migration-20260724` | `1.0.0` | `2026-07-24T22:30:00+08:00` | `/root` | migration | 旧正式 Survey 存在，但未恢复旧 process manifest | `migration-legacy-survey-manifest-missing-icml2026-001` unresolved；已检索 `_artifacts/icml_2026/`、正式 Survey 邻近目录及 manifest 文件名 | 对 12 篇既有题单进行增量检索，优先刷新缺失 PDF/source/code 的论文；重建可审计的 process delivery | 用户要求继续完善并刷新上次未取得源文件的论文 | 本文；paper/system DB；单篇刷新交付；正式知识库 | 2026-07-24 一手来源、fresh-agent handoff、正式目录现状 | material |

> 完成边界：旧 Survey 的 process manifest 无法恢复，因此本次根交付保持 `blocked`；这不否定已通过独立审计的单篇升级。被父级判为 rejected 的单篇交付不用于综合或正式提升。

## 1. 领域与检索范围

- 用户输入领域：`02_model_systems/ICML/2026` 既有 12 篇用户题单。
- 规范化分支：统一生成模型、多模态 token/memory 路由、视频扩散、speculative/MTP 解码、点云多模态补全。
- 检索日期：2026-07-24。
- 来源：arXiv/导出 source、ICML 官方页面/Downloads、OpenReview、作者/项目页、GitHub API、Semantic Scholar。
- 时间范围：以 2024–2026 的题单论文为主；不把目录视为 ICML 官方接收名单。
- 纳入标准：保留原 12 项；对本轮实际修订项要求精确身份、一手正文、fresh one-paper agent 和父级验收。
- 排除标准：同名但身份不符的论文、第三方实现、无法通过隔离/manifest/视觉 QA 的交付不得提升为正式结论。

检索查询、访问限制和 exact-title 恢复过程见 `search_log.md`；候选与系统实体分别见 `paper_db.jsonl`、`system_db.jsonl`。

## 2. AI 生成趋势与 Infra 示意图

未生成。环境存在 `OPENROUTER_ICU_API_KEY`，但已安装的 `$openrouter-icu-image` 只提供 `generate`/`edit`，没有本技能要求的 `responses-doc --input-file synthesis.md` 文档驱动入口；未用纯 prompt 图替代。

## 3. 术语与符号解释

### 3.1 术语表

| 术语 | 规范解释 | 定义性质 | 各论文用法 | 来源 | 易混点 |
|---|---|---|---|---|---|
| token efficiency | 达到相同任务目标时生成、验证或保留 token 的有效程度 | cross-paper synthesis | DLMR 指减少冗余 decoding；MTP/ECHO 指每轮接受更多 token | 各论文正文/摘要 | 不等于 wall-clock throughput |
| speculative decoding | draft 提案、target 验证并接受前缀的解码框架 | paper-stated | SelfJudge 放宽 verifier；OnlineSpec 在线更新 draft；ECHO 调度树预算 | 单篇 reviews | acceptance length 不自动等于服务吞吐 |
| soft splatting | 点对邻域像素的加权散射 | paper-stated | SplAttN 使用 Gaussian × inverse-depth 的有限窗口实现 | SplAttN §3/code | 不等于 3DGS alpha compositing |
| layer-adaptive compression | 随网络层改变 token 压缩策略 | paper-title/待正文核验 | OmniFit 标题与公开条目使用该概念 | OpenReview/ICML metadata | 不应由标题推断具体算法 |
| visual/reasoning memory | 分别保存视觉证据和中间推理约束的潜在状态 | paper-stated at abstract level | DLMR 摘要级机制 | ICML/OpenReview indexed abstract | memory shape、更新和路由粒度仍未知 |

### 3.2 符号表

| 符号 | 来源类型 | 论文 | 含义 | 作用域 | 取值 | 来源 | 易混点 |
|---|---|---|---|---|---|---|---|
| \(\sigma\) | paper-specific | SplAttN | Gaussian splat 带宽 | 每个投影 kernel | code 为 1.5 pixel | Eq. 3/7 与 fixed commit | kernel size 4 不等于 \(\sigma=4\) |
| \(\mathrm{CMIT}\) | paper-specific | SplAttN | channel entropy × spatial coverage | 一组视觉表示 | proxy | Appendix C/Figure 8 | 不是 bit/s |
| \(k\) | paper-specific | MTP Self-Distillation | 一次预测的 token span | training region/decoding step | 论文覆盖多种 span | MTP method/implementation | 与实际接受的动态 \(k'\) 区分 |
| \(\tau\) | paper-specific | SelfJudge/MTP | acceptability 或置信阈值 | 每次解码决策 | 按任务调节 | 单篇实验 | 不是 sampling temperature |

## 4. GitHub/awesome 资源

| 仓库 | URL | Stars/Forks（2026-07-24） | 更新线索 | 论文 | 可信度 |
|---|---|---:|---|---|---|
| SplAttN | https://github.com/zay002/SplAttN | 13/1 | pushed 2026-07-02；commit `0c279dd…` | SplAttN | 官方原生实现 |
| XDLM | https://github.com/MzeroMiko/XDLM | 27/1 | 活跃仓库 | XDLM | 官方原生实现 |
| OnlineSPEC | https://github.com/ZinYY/OnlineSPEC | 72/11 | 代码已发布 | OnlineSpec | 官方原生实现 |
| mtp-lm | https://github.com/jwkirchenbauer/mtp-lm | 39/8 | 本轮重新可访问 | MTP Self-Distillation | 官方实现，等待本轮 agent 最终核验 |
| DLMR | https://github.com/Hunter-Wrynn/DLMR | unavailable | API 404 | Dual-Latent | 声称链接当前不存在 |

## 5. 高热度/高价值信号

| 论文 | 引用信号 | GitHub 信号 | 价值判断 | 边界 |
|---|---|---|---|---|
| ECHO | Semantic Scholar 6，influential 2 | 代码未发布 | 高并发 speculative serving 新锚点 | 数字早期且易变 |
| MTP Self-Distillation | Semantic Scholar 4 | 39 stars / 8 forks | standalone MTP 部署路径 | venue 仍未独立确认 |
| SplAttN | 引用 API rate-limited | 13/1，含公开 checkpoint metadata | 点云 2D–3D 融合概念锚点 | 早期工作，不以 stars 代替质量 |

其余影响 API 多次 rate-limit；缺值保留为空，而非填零。详情见 `impact_signals.md`。

## 6. 候选论文概览

| 论文 | venue/status | 角色 | 本轮状态 | 原因 |
|---|---|---|---|---|
| SplAttN | ICML 2026 Spotlight | core refresh | accepted | 完整 PDF/source/code/checkpoint/visual 链闭环 |
| Dual-Latent Memory Routing | ICML 2026 Spotlight | core refresh | rejected delivery / source blocked | PDF/API 403，仓库 404，且共享工作区隔离审计失败 |
| Flex-Forcing | ICML 2026 Spotlight | core refresh | accepted-with-limitations | 完整 PDF/source 与视觉已恢复；未发布官方 code/checkpoint |
| OmniFit | ICML 2026 Spotlight | core refresh | rejected delivery / source blocked | 精确身份已定位；primary PDF/source/API/code 不可得 |
| MTP Self-Distillation | preprint / venue 未确认 | source refresh | accepted-with-limitations | 完整 source、官方 code commit 与 5 张视觉已核验 |
| 其余 7 篇 | confirmed/workshop/preprint 混合 | retained context | unchanged | 已有正式 review，本轮未重写 |

## 7. 组织/高校分布

作者归属只在一手 PDF/OpenReview 明示时记录；当前 DB 对未核验 affiliations 留空。题单同时包含公司研究团队、大学实验室与合作项目，因此不能从 GitHub owner 推断论文归属。

## 8. 入选论文时间线

| 年份 | 论文族 | 核心问题 | 设计动机 | 关键机制 | 系统权衡 |
|---|---|---|---|---|---|
| 2024 | LatentLM | 连续/离散模态统一 | 保留 causal 主干 | next-token diffusion head + σ-VAE | diffusion head 与 VAE 成本 |
| 2025 | SelfJudge | 严格验证损失可接受 token | 目标模型自监督 acceptability | learned verifier | 有损 quality-speed trade-off |
| 2026 | XDLM/DODO/Flex-Forcing | 双向与 AR/离散生成统一 | 按预算切换并行性 | kernel/block/flexible chunk | cache、同步与视频显存 |
| 2026 | MTP/OnlineSpec/ECHO | 解码加速落地 | 将动态决策放到可服务边界 | adaptive span、online update、global scheduling | control-plane 与 dense-kernel 利用率 |
| 2026 | LiME/DLMR/OmniFit/SplAttN | 多模态信息选择 | 避免复制、遗忘和稀疏对齐 | routed PEFT、dual memory、layer compression、soft splat | 路由/压缩损失与带宽 |

## 9. 方法谱系与关联

| 起点 | 后续 | 关系 | 继承 | 改动 | 证据 |
|---|---|---|---|---|---|
| strict speculative verification | SelfJudge | 放宽 | draft/target 两阶段 | 学习 acceptability | SelfJudge 正文 |
| per-request speculative tree | ECHO | 系统化 | draft tree + verification | 全 batch budget、flatten-and-pack | ECHO 正文/消融 |
| hard point projection | SplAttN | 替代 | 多视图 2D–3D fusion | finite Gaussian splat | SplAttN Table 4/code |
| full-sequence diffusion OCR | DODO | 修正 | masked diffusion | block training + exact cache | DODO Tables 2–3 |

不存在论文直接引用时只记机制谱系，不虚构 citation lineage。

## 10. 横向对比

| 方法族 | 为什么这样设计 | 具体问题 | 因果机制 | 替代/权衡 | 系统代价与局限 |
|---|---|---|---|---|---|
| routed multimodal modules | 不为每个任务/模态复制大模块 | 参数与信息选择 | 小 router/modulator 决定复用 | dense adapter 更简单 | 负载均衡、尾延迟常未报告 |
| memory-augmented reasoning | 单一增长上下文会遗忘 | 长生成视觉/约束保持 | 分离 memory 并按状态路由 | 原 token/KV 保留 | 正文缺失时无法估算容量与带宽 |
| adaptive decoding | 不同位置可安全接受的跨度不同 | 固定 chunk 浪费或掉点 | 阈值/反馈动态调整 | verifier 或固定 k | 控制开销会抵消吞吐 |
| batch-level speculative scheduling | 高并发下 request 独立扩展浪费预算 | verification budget 竞争 | 全局重分配并 pack dense batch | 固定树更易实现 | 调度和 packing 归因耦合 |
| soft 2D–3D bridge | hard projection 支持稀疏 | 点云视觉分支失效 | 邻域平滑扩大支持 | bilinear/learned renderer | 当前实现不是连续坐标 scatter |

## 11. 技术演进趋势

### 11.1–11.4 问题、动机、结构与监督

问题从“模型能否生成”转向“在给定步数、显存和服务负载下如何生成”。结构上，统一大模块逐渐转为小型 router、memory、head 或 bridge；监督从固定 ground-truth token 延伸到 target feedback、自蒸馏与反事实视觉移除。

### 11.5 推理、部署与系统代价

动态算法只有在控制面边界可编译、可 pack、可 cache 时才转化为硬件收益。ECHO 把动态性限制在 sparse gate/scheduler/packing，DODO 用 block-causal cache 保留精确复用，MTP 则需验证 confidence decision 的逐 token 开销。

### 11.6–11.8 评测、组织与热度

accepted length、CMIT、SCS、FID/NED 等代理指标不能替代 wall-clock、p95/p99、HBM bytes 和并发吞吐。当前论文较新，引用与 stars 主要用于定位工程采用，不用于质量排序。

## 12. 软硬件 Infra 需求维度

| 维度 | 需求/瓶颈 | 关联工作 | 趋势/证据 |
|---|---|---|---|
| Data types | 多数论文未完整报告 fp16/bf16/fp8 | 全题单 | 不能由 GPU 型号推断 dtype |
| runtime/serving | batching、verification、cache、packing | SelfJudge/MTP/OnlineSpec/ECHO/DODO | 算法跨度必须和服务吞吐分开 |
| kernel/operator | attention、scatter、kNN、custom cache | SplAttN/DODO/Flex-Forcing | 固定窗口和 block 边界更易映射 dense kernel |
| CPU/GPU/NPU | preprocessing、custom CUDA、fallback | SplAttN 等 | NPU/CPU fallback 多未实现 |
| 显存 | 视频时空激活、KV、树节点、点云中间点 | Flex-Forcing/ECHO/SplAttN | batch/序列/分辨率共同决定峰值 |
| 带宽/互联 | HBM、PCIe/NVLink、all-reduce | 全题单 | 缺 bytes moved 和有效带宽，不能报利用率 |
| 部署 | checkpoint、commit、配置、license | SplAttN/MTP | “仓库存在”不等于可复现闭环 |

## 13. 当前共识与分歧

- 共识：动态选择可减少无效计算，但必须保留 cache/packing/kernel 友好性。
- 共识：多模态增益必须用移除/替换/等预算对照，而非只看端到端分数。
- 分歧：应保留 lossless target verification，还是接受有损置信阈值以降低系统复杂度。
- 不可直接比较：venue、模型规模、数据、并发、硬件、dtype 和 latency 口径不同。

## 14. 后续研究方向

| 方向 | 动机 | 方法 | 风险 | 关联 |
|---|---|---|---|---|
| router-aware serving | 路由收益可能被尾延迟抵消 | batch-aware routing + load telemetry | 训练/部署分布漂移 | LiME/DLMR/ECHO |
| continuous-to-discrete implementation audit | 理论连续性与 scatter 实现不一致 | gradient test + subpixel kernel | kernel 复杂度上升 | SplAttN |
| confidence decision fusion | per-token 控制开销高 | fused kernel / block decision | 精度损失 | MTP/SelfJudge |
| source-complete reproducibility | 新论文 release 不完整 | immutable source+commit+checkpoint manifest | 存储与维护成本 | 全题单 |

## 15. 证据与局限性

- 论文正文结论只来自通过验收的 paper delivery 或既有正式 review。
- 代码结论必须固定 commit/path；第三方仓只作为 adoption 线索。
- Dual-Latent 的新 agent delivery 因隔离审计失败被拒绝；本文只保留父级独立核验的身份与访问障碍，不采用其技术分析。
- Flex-Forcing 与 MTP 已通过独立 clone/manifest/视觉验收；OmniFit 因 primary PDF/source 缺失按契约 rejected，只保留身份和阻塞元数据。
- OpenReview/ICML 某些页面受 Cloudflare 403；搜索索引可用于定位身份，但不能替代 PDF 内容。
- 旧 process manifest 缺失对应 migration issue `migration-legacy-survey-manifest-missing-icml2026-001`，使根交付不能标为 complete。
