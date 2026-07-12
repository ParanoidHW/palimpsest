# SwiftFusion：面向分布式 DiT 推理的拓扑感知序列并行
> [!info] 文档关系
> - 文档类型：Paper
> - 领域入口：[README](../README.md)
> - 上位汇总：[Diffusion 多模态生成与 AI Infra](../surveys/multimodal-diffusion-infra.md)
> - 证据资产：`../assets/papers/swiftfusion/`
> - 相关文档：[Figure inventory](../evidence/figure-inventory.md)

## 修订信息

- 当前文档版本：`1.0.0`
- 当前修订 ID：`rev-001`

| 修订 ID | 版本 | 时间 | 修订者 | 类型 | 前序 | 变更位置 | 原因/证据 | 对结论影响 |
|---|---|---|---|---|---|---|---|---|
| `rev-001` | `1.0.0` | 2026-07-12T00:00:00+08:00 | `review_swiftfusion` | `initial` | 无 | 全文及本地证据 | 初始交付；基于 arXiv PDF 与源码 | 建立初始结论，无前序修订 |

## 资料与图表清单

| 资料 | 状态 | 用途 |
|---|---|---|
| [arXiv:2601.20273](https://arxiv.org/abs/2601.20273) | 核验 PDF SHA-256 `130f6eab...4b0114` | 14 页主证据 |
| arXiv e-print | 核验归档 SHA-256 `c899e79c...23e4a` | 精确公式、caption、实验宏与伪代码 |
| `extracted_pdf/extracted_text/` | 已提取 | 全文检索；skill PyMuPDF helper，因环境无 `pdftotext` |
| 官方代码 | 不可用 | 任务包未提供，论文未给 repository；实现声明只能核至伪代码/源码文字 |
| OpenReview | 不适用/未发现 | 论文标注 ACM CAIS 2026；任务包无 OpenReview URL；检索工具失败，不能分析公开评审 |

![Figure 6：Torus Attention 分阶段通信调度（原论文图，含完整 caption）](../assets/papers/swiftfusion/fig6-torus-scheduling.png)

![Figure 10：SwiftFusion 逐组件消融（原论文图，含完整 caption）](../assets/papers/swiftfusion/fig10-ablation-caption.png)

## 结论先行

SwiftFusion 的核心并非“更快的 attention 数学”，而是把两层网络拓扑、attention 分片方向和通信语义联合调度：跨机使用通信量随机器数下降的 Ulysses 维度，机内使用通信量较高但可流水的 Ring 维度；随后以 Torus Attention 把跨机 all-to-all 拆成 Pull Q、Pull KV、Push O 阶段，并以 NVSHMEM one-sided push/pull 减少每步 sender-receiver 配对同步。

论文在 4 台 AWS `p4de.24xlarge`（每台 8 x A100 40 GiB、NVSwitch、EFA 最高 400 Gbps）上，相对 USP 报告平均 `1.35x`、最高 `1.77x` 的最优配置单步延迟加速。这个数字是系统整体相对 USP 的匹配工作负载比较，不是 Torus 或 one-sided 单组件的独立收益。Figure 10 的逐步消融显示组件效果强烈依赖工作负载：长序列视频更受益于 Torus；较短图像序列中，Torus+NCCL 可无收益甚至回退，而 one-sided 实现恢复收益。因此“所有组件总是各自加速”不成立，“组合在测试集上达到最佳整体表现”才受证据支持。

## 术语与符号

### 术语表

| 术语 | 来源/别名 | 本文特定含义 | 范围 | 来源 | 歧义/限制 |
|---|---|---|---|---|---|
| TAS | author-defined, topology-aware scheduling | 跨机映射 Ulysses、机内映射 Ring 的 2D mesh 调度 | attention serving runtime | §4.2，Appendix C | 不是自动 topology search；规则主要由 `gcd(NM,H)` 决定 |
| Torus Attention | author-defined, Torus | 将跨机 Ulysses all-to-all 分成 Pull Q / Pull KV / Push O，利用 stationary chunk 先算后传 | 跨机 attention | §4.3、Figure 6 | “Torus”描述调度形态，不等同通用 torus network |
| one-sided communication | author-defined | NVSHMEM remote put/get 与显式 barrier/stream ordering | serving/runtime | §4.4、Appendix B | 仍有层首/层末跨机全局同步，不是无同步 |
| stationary elements | author-defined | all-to-all 前后归属当前 rank 不变的 head partition | Torus breakdown | §4.3、Figure 6a | 仅在论文给定布局变换下成立 |
| matched speedup | analysis-derived | 同一 workload/hardware 下相对 USP 的延迟比；最优配置图允许各方法选自身最优配置 | evaluation | §5、Figure 7/10 | 不等于同一并行配置；Figure 8 才覆盖若干相同配置 |
| synchronization | stage-qualified | NCCL Ring 每步配对同步；NVSHMEM 方案保留 process-group barrier 与 layer boundary barrier-all | communication runtime | §3、§4.4、Appendix B | 论文“two inter-machine synchronizations”不应解读为全程序仅两次 |

### 符号表

| 符号 | 来源 | 含义 | 单位/范围 | 来源 | 歧义 |
|---|---|---|---|---|---|
| $B,L,H,D$ | author-defined | batch、全局 sequence length、head 数、每 head 维度 | 正整数 | §2.2 | $L$ 在单 GPU 与全局布局间需看上下文 |
| $N,M$ | author-defined | GPU 机器数、每机 GPU 数 | 正整数 | §4.2、Appendix C | 实验为 $N\le4,M=8$ |
| $P_u,P_r$ | author-defined | Ulysses 与 Ring 并行度，$P_uP_r=NM$ | 正整数 | §4.2 | $P_u$ 受 $H$ 整除约束 |
| $T_{l,h}$ | author-defined | tensor $T$ 的 sequence partition $l$ 与 head partition $h$ | tensor slice | §4.3 | 仅 Torus 调度记号 |
| $V_{USP},V_{SFU}$ | author-defined | 每 GPU 跨机通信元素数 | elements/GPU | Appendix C | 不含协议、同步与链路争用字节开销 |
| $s$ | analysis-derived | 每元素字节数 | bytes/element | 本文推导 | 论文未明确实验 dtype，不能代入固定值 |
| $\eta$ | analysis-derived | 有效链路利用率 | $0<\eta\le1$ | 本文推导 | 论文未报告，无法数值验证 |

## 方法与设计理由

### 设计理由矩阵

| 核心设计 | 理由状态/来源 | 具体问题 | 因果机制 | 替代/代价 | 验证证据 |
|---|---|---|---|---|---|
| TAS 反转 USP 的跨机/机内映射 | author-stated，§3/§4.2 | USP 跨机 Ring 每 GPU 通信量不随机器数下降 | 令低容量跨机链路承担 Ulysses 的 $O(1/N)$ 每 GPU 流量，Ring 留在 NVSwitch | 两机时 Ulysses 流量优势消失且不能重叠；$P_u$ 受 head 数约束 | Appendix C 解析式；Figure 10 TAS matched step；两机反例明确报告 |
| $P_u=\gcd(NM,H)$，$P_r=NM/P_u$ | author-stated，§4.2 | 最大化 Ulysses 使用且保持 head divisibility | 选择最大合法 Ulysses degree 降低跨机 Ring 部分 | 不是基于实测带宽/拥塞的 cost model；当 $N\nmid P_u$ 只给概念扩展 | 解析通信量证明；无独立 scheduler ablation |
| Torus stationary-first 分块 | author-stated，§4.3 | 跨机 Ulysses 原子 all-to-all 无法与 attention 重叠 | 先算不移动 chunk，同时传下一 chunk，形成流水 | 额外 chunk bookkeeping、分片 kernel、尾部不可隐藏区 | Figure 6 机制；Figure 10 视频 workload 有直接增益，图像 workload 否定普适增益 |
| Pull Q -> Pull KV -> Push O 排序 | author-stated，§4.3 | 四次 all-to-all 生命周期不同，KV 流量为 Q 的两倍 | 先传 Q 以尽早创造计算窗口，随后用已收 Q 掩蔽 KV，最后本地 $O_{t,t}$ 掩蔽 remote O push | 依赖计算窗口足够长；最后 Pull KV stage 无通信可重叠 | Figure 6/算法伪代码；无顺序替换消融 |
| NVSHMEM one-sided unified runtime | author-stated，§4.4/Appendix B | NCCL send/recv 每步双方同步且通信 kernel 占 SM | remote put/get 解耦配对，独立 streams 排序；Ring 用 pull，Ulysses/Torus 用 scatter-push/gather-pull | 程序员承担一致性；仍需 barrier；依赖 NVSHMEM/EFA/GPU direct | Figure 10 增量 one-sided；无公开代码，无法核实实现细节 |
| fused multi-Q/multi-KV CUDA kernel | author-stated，Appendix A | 分块 attention 与 merge 多 kernel launch/全局内存开销 | 单 kernel 维护 online softmax $m,l,O$ 并融合多块 | Ampere PTX/CuTe 特化；可移植性未经代码验证 | Figure 12 与 FA2 normalized microbenchmark；未嵌入，文本证据；无端到端独立消融 |

### 拓扑感知 SP

Ring Attention 每 GPU 近似传输 $2BLHD$ 个元素，不随 $P$ 增大而下降；Ulysses 的四次 all-to-all 近似为 $4BLHD/P$，但并行度受 $H$ 限制且原子 all-to-all 不重叠。SwiftFusion 将 $NM$ 个 GPU 组织为 $P_u\times P_r$ mesh。理想情形 $H=N$ 时取 $P_u=N,P_r=M$，Ulysses 完全跨机、Ring 完全机内。一般规则取：

$$P_u=\gcd(NM,H),\qquad P_r=\frac{NM}{P_u}.$$

Appendix C 对 $P_u\ge N$ 给出的 SwiftFusion 每 GPU 跨机元素数为：

$$V_{SFU}=4\frac{N-1}{N}\frac{BLHD}{N},$$

而 USP 在 $P_r\ge N$ 时为：

$$V_{USP}=2(N-1)\frac{BLHD}{N}.$$

两者比值为 $V_{USP}/V_{SFU}=N/2$。这是流量模型，不是延迟加速定律；它忽略 all-to-all 启动延迟、有效带宽、拓扑争用和 overlap。论文也观测到 $N=2$ 时 TAS 比 USP 更慢，恰好说明相等流量下 USP 的 Ring overlap 更有利。

### Torus Attention

Figure 6a 的关键观察是 all-to-all 变换中当前 rank 对应的 head slice 不移动。Torus 不等待完整 collective，而把执行拆为：

1. `Pull Q`：共 $N$ stage；计算当前可用 $Q$ 与本地 $KV$，并发拉取下一 Q chunk；最后一 stage 预取首个 KV。
2. `Pull KV`：共 $N-1$ stage；用已收 Q 对新 KV 计算并 online merge；最后一 stage 只有计算，形成不可隐藏尾部。
3. `Push O`：传出已完成的 remote output，同时计算本地保留的 $O_{t,t}$。

Figure 6b 支持调度可行性，但不证明所有通信都被隐藏。可隐藏条件可写成分析推导：

$$T_{stage}\approx \max(T_{compute},T_{comm})+T_{sync/residual},$$

仅当 $T_{compute}\ge T_{comm}$ 且 stream/NIC 并发成立时，主体通信可被遮蔽。Figure 10 中短图像序列的 Torus+NCCL 无增益，是这个条件的直接反例。

### One-sided communication 与同步边界

Appendix B 指定 NVSHMEM API：`nvshmemx_putmem_on_stream`、`nvshmemx_getmem_on_stream`、group barrier 与 barrier-all；默认 stream 计算，另设 `stream_ring` 和 `stream_other`。Ring 通信在独立 ring stream，其他通信在 another stream。算法在 layer 开始/结束有 `BarrierAll`，并在机内 process group 使用 barrier。因此准确表述是“把 Ring 每 step 的跨机双边配对同步压缩为层边界同步，并保留必要组内一致性”，不是彻底取消同步。

## 技术主张证据矩阵

| 主张 | 证据 | 分类 | 判断 |
|---|---|---|---|
| TAS 降低多机跨机流量 | Appendix C 解析式与 lemma | direct/theoretical | 在给定 $2\le M\le P_u\le N$ 条件下成立；延迟仍依赖拓扑 |
| TAS 优于 USP | Figure 7/8/10 | direct, matched workload | $N>2$ 支持；$N=2$ 明确不成立 |
| Torus 隐藏 all-to-all | Figure 6 + Figure 10 视频增量 | direct mechanism + workload-dependent experiment | 支持长序列；没有 overlap timeline/utilization 数值 |
| one-sided 降同步/SM contention | 伪代码、Figure 10 incremental step | confounded/direct incremental | 端到端增量可见，但同步与 SM contention 未分别隔离 |
| 整体平均 1.35x、最高 1.77x | `a-auto-experiments.tex`、§5.2 Figure 7 | direct reported | 相对 USP、各自最优配置；不能分配给单组件 |
| 其他相同配置平均 1.61x、最高 3.11x | Figure 8、实验宏 | direct reported | 覆盖所列 3/4 机配置，不代表任意拓扑 |
| 无额外内存消耗 | Figure 7 memory + one-copy-buffer argument | indirect | “不高于 USP”仅在测试配置；未给逐 buffer 字节核算 |
| fused kernel 近 FA2 性能 | Figure 12 | direct microbenchmark | 单 QKV；不能证明多 chunk 情形同样 negligible |
| 可扩展至非 Ampere/非整除布局 | 论文文字 | missing | 无代码/实验，未验证 |

## 匹配消融与收益归因

Figure 10 在同一 workload 和机器数中逐步加入 TAS、Torus、one-sided，是最接近因果归因的证据。五组数值为：

| Workload | TAS/USP | +Torus/USP | +one-sided/USP | 可归因结论 |
|---|---:|---:|---:|---|
| Flux 3072, M=3 | 1.11x | 1.01x | 1.11x | Torus+NCCL 回退约 9.0%；one-sided 恢复 |
| Flux 3072, M=4 | 1.64x | 1.06x | 1.77x | TAS 主收益；Torus 单独大幅回退，one-sided 组合最高 |
| Flux 4096, M=4 | 1.62x | 1.49x | 1.61x | Torus 未超过 TAS；one-sided 恢复至接近 TAS |
| CogVideoX 20s, M=3 | 1.08x | 1.26x | 1.22x | Torus 直接增益；one-sided 在该点略回退 |
| CogVideoX 40s, M=3 | 1.06x | 1.16x | 1.17x | Torus 主增量；one-sided 边际增益 |

表中“组件增量”是从图上相对 USP 的 speedup 粗算，speedup 不能线性相减。其可靠结论是方向与 workload dependence，而不是把整体 `1.35x` 分摊成固定百分比。论文所称三项“均需要”只在“跨测试 workload 获得最佳组合覆盖”意义成立；单个 workload 上 Figure 10 有 one-sided 或 Torus 不改善的反例。

## 基础设施与互连要求

### 硬件与软件事实

- 论文报告：4 x AWS `p4de.24xlarge`，每机 8 x NVIDIA A100 40 GiB，机内 NVSwitch，跨机 EFA 最高 400 Gbps。
- 软件：driver 570.172.08、CUDA 12.8、PyTorch 2.8、NCCL 2.27.3、NVSHMEM 3.4.5。
- workload：Flux 12B，3072/4096 图像；CogVideoX 5B，20/40 秒 768x1360；均 24 heads，head dimension 分别 128/64。
- dtype：论文未明确报告。任何通信字节数必须保留 $s$，不能擅自假设 bf16/fp16。

### 带宽与通信量推导

当 $P_u\ge N$，每 GPU 理想跨机字节数：

$$Bytes_{SFU}=s\cdot4\frac{N-1}{N^2}BLHD.$$

若跨机阶段耗时为 $T_c$，有效带宽与利用率为：

$$BW_{eff}=\frac{Bytes_{SFU}}{T_c},\qquad \eta=\frac{BW_{eff}}{BW_{peak}}.$$

论文未报告 $T_c$ 的字节级测量、NIC 聚合口径或 $\eta$，所以无法从“400 Gbps”验证链路利用率。部署必须满足：(1) GPU-direct EFA/IB RDMA；(2) 多 GPU 到 NIC 的稳定并发；(3) NVSwitch 机内 Ring 带宽显著高于跨机；(4) NVSHMEM symmetric heap/remote addressing；(5) CUDA stream 与 NIC progress 可并发。若 PCIe/NIC oversubscription 或 GPUDirect 关闭，Torus overlap 与 TAS 映射都可能失效。

### NIC/GPU 同步与调度要求

- GPU rank 必须有一致的 3D `(t,u,r)` 映射，且 $P_uP_r=NM$；错误 rank placement 会让“机内 Ring”跨机。
- Ulysses 要求 $H\bmod P_u=0$；论文的 gcd 规则是 legality heuristic，不是动态带宽 optimizer。
- 至少三个 CUDA streams（default compute、ring、other），依赖 stream-ordered NVSHMEM put/get/barrier。
- layer boundary `BarrierAll` 是 correctness 边界；机内 Ulysses/Ring 仍需 process-group barrier 或 event wait。
- NIC 需要在 GPU kernel 运行时推进 RDMA，否则所谓 overlap 退化为串行。
- custom kernel 使用 Ampere `mma.sync.aligned.m16n8k16` 与 `ldmatrix...x4`；迁移至 Hopper/NPU 需要重写/重调 tile 与 online-softmax merge。

### 内存、数据类型与异构性

伪代码最多为 Q/K/V/O 各保留一个额外 buffer，加上 online softmax 的 $m,l$。粗略额外 tensor storage 为：

$$M_{buffer}\approx4sBLHD + M_{m,l},$$

但局部 shard 与 layout 细节决定每 GPU 实际值，论文没有完整公式。CPU 只承担启动/调度角色，核心路径假定同构 NVIDIA GPU；没有 NPU、CPU fallback 或 mixed accelerator 实验。数据格式未报告，也没有量化、FP8、压缩通信证据。

## 相关工作定位

| 方法组 | 机制差异 | SwiftFusion 优势 | 公平性/限制 |
|---|---|---|---|
| Ring/Ulysses/USP | 固定 collective 或 USP 跨机 Ring | topology reversal + chunked overlap | 实验只直接比较 USP；未展示所有独立实现基线 |
| DistriFusion/PipeFusion | 借 diffusion temporal redundancy，可能有近似误差 | SwiftFusion 保持 exact attention 语义 | 未做端到端质量/延迟同表比较 |
| ScaleFusion | spatial-temporal attention 专用 all-to-all overlap | SwiftFusion 面向 general attention | 论文定性比较，缺直接实验 |
| DeepEP/Flux/Comet | LLM MoE/GEMM 通信融合 | 针对 attention 生命周期设计 | 领域与 operator 不同，不宜用绝对速度横比 |
| Triton-Distributed/TileLink/Mercury | compiler-driven overlap | SwiftFusion 提供手工专用 schedule | 无 compiler baseline，维护/可移植代价未量化 |

## Evidence loop

1. **问题**：USP 在多机下跨机 Ring 每 GPU 流量近常数，NCCL 配对同步形成 bubble（§3，Figure 3/4）。
2. **机制**：TAS 把低流量 Ulysses 放跨机；Torus 利用 stationary chunk 形成阶段流水；NVSHMEM 降低 per-step pairing（§4，Figure 6，Algorithm 1）。
3. **测量**：A100/NVSwitch/EFA 上与 USP 比较，Figure 7/8 报 overall speedup，Figure 10 逐步消融。
4. **结论**：测试拓扑上整体更快，视频长序列更能显示 Torus 增益。
5. **限制回扣**：两机 TAS 变慢、短图像 Torus+NCCL 回退；无公开代码、dtype、有效带宽和 overlap timeline，因此可泛化范围仅到相似同构 NVIDIA/EFA 拓扑与所测序列区间。

## 局限与待验证问题

- 无官方代码/commit 可检查，NVSHMEM API、barrier placement、buffer lifetime 与 kernel 实现仅由论文伪代码支持。
- 没有跨 topology（IB vs EFA、不同 NIC 数、Hopper）实验，也没有 NIC/GPU timeline 或有效带宽利用率。
- 最优配置比较允许方法各选配置；Figure 8 才是配置层面的补充，但覆盖仍有限。
- Figure 10 是累加式消融，没有“只 one-sided”“不同 Torus stage order”“NCCL 与 NVSHMEM microbenchmark”完全析因设计。
- 论文没有明确 dtype、随机性/重复次数、误差条，也未报告生成质量回归；exact attention 机制暗示质量等价，但仍缺数值校验。
- $N\nmid P_u$、head 数较少、非 Ampere、混合 GPU/NPU、NIC oversubscription 下如何 rank-map 与退化，均待验证。

## 研究启发

最可迁移的思想是用“通信量随并行度的缩放律”而不是 collective 名称来映射层级拓扑，并进一步寻找 collective 前后不移动的数据块作为计算启动点。工程上下一步应建立带 $BW_{intra}$、$BW_{inter}$、启动延迟、head divisibility、kernel occupancy 与 overlap efficiency 的 cost model，让 $P_u,P_r$ 与 stage chunk size 从静态 gcd 规则升级为实测自适应选择。
