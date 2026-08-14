---
tags:
  - topic
  - collection/parallel-partitioning
  - domain/ai-infra
  - method/fsdp2
document_type: topic
domain: parallelism
canonical: true
---

# FSDP2 `fully_shard` 为什么必须 bottom-up

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[README](../README.md)
> - 上位汇总：[并行切分方法体系](../surveys/parallel-partitioning-taxonomy.md)
> - 相关概念：[多轴组合与设备网格](composition-and-device-mesh.md)
> - 相关 Paper：无（这是框架实现机制，不是单篇论文复述）
> - 证据资产：无

## 结论先行

`fully_shard` 的 bottom-up 不是因为“只有从叶子向根才能算出 shard size”，而是因为一次 `fully_shard(module)` 调用同时定义了一个**通信与生命周期分组**。调用时，FSDP2 把 `module.parameters()` 中尚未被子模块分组占用的参数收进当前组；因此必须先给子模块分组，再给父模块分组。这样每个 Transformer block 可以有自己的 all-gather / reduce-scatter 窗口，父模块最后只接管仍未分组的 embedding、norm、head 等参数。

如果先对根模块调用，根会递归看到几乎全部参数并把它们收进一个大组。之后对子模块调用时，参数已经属于已有组，子模块无法再形成独立通信组；结果是“看起来仍然 fully sharded”，但失去逐层释放、通信/计算重叠和较低峰值显存这些 FSDP2 composable API 的主要收益。

## 1. 先区分两个容易混淆的“分片”

这里的“分片”有两层含义：

1. **持久所有权**：每个原始参数在计算间以 DTensor 保存，默认 placement 是 `Shard(0)`，每个 rank 只持有参数第 0 维的一段；梯度和 optimizer state 也按同一数据并行组分片。
2. **通信分组**：多个参数可以合并到一个 `FSDPParamGroup`，以一次 all-gather 得到本组的完整参数，并以一次 reduce-scatter 归约本组梯度。

bottom-up 约束的是第二层。它不会改变“参数沿哪一维切”这个数学选择，而是决定哪些参数共享一次通信和同一个 unshard/reshard 生命周期。

### Symbol Table

| 符号 | 含义 |
|---|---|
| $p$ | FSDP 数据并行通信组中的 rank 数 |
| $G_i$ | 第 $i$ 个 `fully_shard` 调用建立的参数通信组 |
| $P_i$ | 组 $G_i$ 中参数的全局大小（MiB） |
| $P_r$ | 根组中剩余参数的全局大小（MiB） |
| $r$ | 当前观察的 rank；它持有每个参数 shard 的 owner-local 部分 |

下文沿用这些符号；“完整参数”表示一次 forward/backward 计算窗口内的 unsharded 临时 Tensor，“持久 shard”表示计算间保留的 DTensor。

## 2. 调用顺序如何决定参数归属

典型写法是：

```python
for block in model.blocks:
    fully_shard(block, mesh=mesh)
fully_shard(model, mesh=mesh)
```

假设 `model` 含两个 block，以及一个不属于任何 block 的 `lm_head`：

| 调用 | 本次可见但尚未归组的参数 | 新建通信组 |
|---|---|---|
| `fully_shard(block_0)` | `block_0` 的参数 | `G_0` |
| `fully_shard(block_1)` | `block_1` 的参数 | `G_1` |
| `fully_shard(model)` | `lm_head`、以及其他未被子模块占用的参数 | `G_root` |

这里的 `module.parameters()` 是递归枚举；“尚未归组”是关键条件。子模块先调用后，父模块再次枚举时仍能看到完整模块树，却会跳过已归属于 `G_0/G_1` 的参数。这使父级调用可以覆盖剩余参数，同时不吞掉子级分组。

反过来执行 `fully_shard(model)` 再执行 `fully_shard(block_0)`，根调用会先把 `block_0`、`block_1` 和 `lm_head` 一起放进一个组。此时后续 block 调用没有可重新分组的参数，无法把已经建立的根组拆开。bottom-up 因而是一个**不可逆的分组声明顺序**。

## 3. 为什么分组粒度会影响显存与通信

### 3.1 正向与反向的生命周期

对组 $G_i$，FSDP2 在正向前 all-gather 参数 shard，得到本组的临时完整参数；正向后按 `reshard_after_forward` 释放完整参数。若释放，反向开始前还要再次 all-gather；反向结束后 reduce-scatter 梯度，并恢复持久的 DTensor shard。

公式解释：$G_i$ 表示一次通信的参数组；正向 all-gather 的发送者是数据并行组内所有 rank，接收者也是所有 rank，结果是每个 rank 都有本组完整参数；reduce-scatter 的输入是各 rank 的本地梯度贡献，按元素求和后每个 rank 只保留自己负责的梯度 shard。该生命周期回答“完整参数在什么时候占用显存，以及梯度何时回到 owner”这两个工程问题。

### 3.2 一个数值例子

设有 $p=4$ 个 rank，两个 block 各含 $P_i=16$ MiB 参数，root 还有 $P_r=8$ MiB 的 head 参数。按 block bottom-up 分组时，每个 rank 的持久参数 shard 约为 $(16+16+8)/4=10$ MiB；但正向执行 block 0 时只需要额外 materialize 16 MiB 的完整参数，随后可释放，再处理 block 1。若根先调用，单个组包含 40 MiB 参数，根组的 unshard 峰值约为 40 MiB，无法利用 block 边界释放。

公式解释：持久 shard 大小是全局参数总量除以 $p$；临时完整参数峰值由“同时处于 unshard 窗口的组”决定，而不是由平均 shard 大小决定。这个例子说明 bottom-up 通过缩小通信组降低 peak memory，代价是增加组级 collective 的启动次数。

### 3.3 通信与重叠的取舍

组越小，单次 all-gather/reduce-scatter payload 越小，当前层计算更容易覆盖通信，且峰值 buffer 更低；但 collective 启动次数增加，短层或跨节点场景可能被 latency 主导。组越大则相反：启动次数少、带宽利用可能更好，但完整参数驻留时间更长，也更难和层内计算重叠。

因此 bottom-up 并不等于“每个叶子模块都必须独立一组”。实际边界应放在有足够计算量、参数复用关系清楚且 forward 顺序稳定的模块上；对很小的 norm、bias 或 head，可以让它们随父组一起通信。

## 4. 与模块执行树的因果关系

FSDP2 通过模块 forward/backward hooks 驱动组的 unshard、reshard 和梯度归约。子模块组先建立后，运行时可以在进入 `block_i` 时只激活 `G_i`，离开后释放其完整参数；根组负责未分组的参数和 forward-root 的迭代边界。这个关系有三个直接后果：

- **峰值显存**：不需要让整个模型同时处于 unsharded 状态。
- **通信/计算重叠**：下一个 block 的 all-gather 可以在当前 block 计算期间预取，具体是否重叠取决于 runtime 调度与硬件拓扑。
- **优化器语义**：optimizer 看到的是持久 DTensor 参数及其 owner-local state；bottom-up 不改变 optimizer 的数学更新，只改变参数何时临时 materialize。

这也解释了为什么把 checkpoint、bottom-up 配置或 mesh 初始化画进每一步训练回路是错误的：它们是 setup/边界操作；每步主链应是 `pre-forward all-gather -> FWD -> reshard -> backward all-gather（若需要） -> BWD -> reduce-scatter -> optimizer`。

## 5. 什么时候不应机械套用

- **根模块只有一组参数**：若模型很小，根调用本身足够，bottom-up 不会凭空带来收益。
- **参数共享**：同一个 `Parameter` 被多个模块引用时，应确认它归属哪个组，必要时使用 `ignored_params` 或显式分组；不能假设共享参数会自动得到两个独立 shard。
- **非标准 forward 顺序**：条件分支、chunked loss 或只调用部分模块时，要确保组的 hook 生命周期与实际调用顺序一致；对一次迭代多次独立调用的组，reduce-scatter 可能按调用次数发生。
- **不规则切分轴**：`shard_placement_fn` 可以改 placement 或 mesh，但它改变的是 ownership 规则，不会取消“每个 `fully_shard` 调用形成通信组”的约束。

## 6. 证据与源码边界

本节依据 [PyTorch `fully_shard` API 文档](https://pytorch.org/docs/stable/distributed.fsdp.fully_shard.html) 与 PyTorch `v2.13.0` [源码快照](https://github.com/pytorch/pytorch/tree/cf30153c4c131c8164ee7798e5022d810682e2cb)（commit `cf30153c4c131c8164ee7798e5022d810682e2cb`）的 `torch/distributed/fsdp/_fully_shard/_fully_shard.py` 中 `fully_shard` 文档与 `torch/distributed/fsdp/_fully_shard/_fsdp_param_group.py` 的参数组运行时；官方 API 文档说明了正向/反向 all-gather、reshard 和 reduce-scatter 的生命周期。源码能证明“参数如何归组、hook 如何触发 collective”，不能单独证明某个硬件上的吞吐提升；“bottom-up 降低峰值但增加启动次数”是基于该生命周期的 analysis-derived 推论。

### 训练 / prefill / decode 边界

- **训练**：上述 bottom-up 分组和 forward/backward 生命周期是直接适用的场景；optimizer 在持久 shard 上更新。
- **Prefill**：`fully_shard` 仍可在每层 forward 前 gather、之后 reshard，但 token 维度更大，all-gather 与 GEMM 的重叠条件要单独测量；KV cache 不由该 API 自动分片。
- **Decode**：单步 token 很少，组级 all-gather 更容易落入 critical path；bottom-up 仍能降低常驻参数，但不保证单请求延迟下降，需把 cache ownership、动态 batching 和通信频率单独建模。
