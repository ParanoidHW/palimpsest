---
tags:
  - topic
  - domain/ai-infra
  - domain/hardware-runtime
  - topic/one-sided-communication
  - topic/llm-serving
document_type: topic
domain: hardware_runtime/cann
canonical: true
status: draft-for-iteration
last_reviewed: 2026-09-04
---

# 单边通信、Mooncake 与 Ascend ADXL/HIXL

> [!info] 文档关系
> - 文档类型：Topic
> - 领域入口：[CANN Hardware Runtime README](../README.md)
> - 相关主题：[通信原语与成本模型](../../../parallelism/topics/communication-primitives-and-cost-model.md)
> - 相关文档：[Mooncake Transfer Engine 文档](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/)、[昇腾 HIXL 单边通信应用开发](https://www.hiascend.com/document/detail/zh/canncommercial/900/programug/acldevg/aclcppdevg_000538.html)

本文解释三个层次：单边通信的通用语义、Mooncake 如何组织 KV Cache 数据搬运，以及 Ascend 的 ADXL/HIXL 如何提供底层能力。重点是数据面和生命周期，不把单边读写误解成集合通信或完整的缓存一致性协议。本文当前标记为 `draft-for-iteration`，便于继续补充目标 CANN/HDK 版本和实测结果。

## 1. 单边通信是什么

单边通信（one-sided communication）指：通信发起方提交一次远程读写后，目标进程不需要为每个请求显式调用匹配的接收函数。

基本流程是：

```text
目标端：分配并注册内存，公开地址范围和访问权限
        |
        | 控制面交换地址、句柄、权限等元数据
        v
发起端：提交 READ 或 WRITE
        |
        v
通信库/网卡直接搬运数据
        |
        v
发起端查询完成状态；目标端不必参与每次接收调用
```

- `READ`：从远端地址读取到本地地址。
- `WRITE`：把本地地址的数据写入远端地址。
- 远端内存必须提前注册，通信库需要知道地址、长度和访问权限。
- “单边”描述的是操作语义，不等于某一种链路。RDMA（Remote Direct Memory Access，远程直接内存访问）、HCCS（Huawei Cache Coherent System，昇腾互联链路）都可能成为底层路径。
- 单边通信不等于集合通信。一次 `WRITE` 不会自动完成 `all-reduce`、`all-gather` 或求和。

### 为什么需要它

双边消息通信通常要求发送端和接收端共同参与匹配。当 Decode 线程正在执行计算、调度或缓存管理时，接收调用可能成为额外同步点。单边通信把控制面（地址、权限、请求状态）和数据面（实际字节搬运）分开，目标可以继续计算或只处理完成通知。

这并不意味着“完全没有同步”：注册、建链、完成确认、数据一致性和释放顺序仍然必须由通信库或上层系统管理。

## 2. 一个具体的读写例子

设目标端保存一个形状为 `[8, 4096]`、数据类型为 `float16` 的 KV Cache（Key-Value Cache，键值缓存）对象。它的大小是 `8 × 4096 × 2 = 65536` 字节。

1. 目标端为这段 Device 内存调用注册接口，并设置允许远端访问的范围和权限。
2. 控制面把远端地址、长度和句柄交给发起端。
3. 发起端提交 `WRITE`，将本地 `[8, 4096]` 缓冲区写入目标端；或提交 `READ`，把目标端快照读回本地。
4. 发起端等待请求完成后，目标端的内容才可被上层当作“已到达”使用。

这里不需要 `all-reduce`，因为操作是一个发起方到一个目标地址的点对点数据搬运。如果两个发起方同时写同一远端地址，仍然会发生竞态；单边 `WRITE` 不自动提供原子累加或对象版本控制。

## 3. Mooncake 的分层结构

Mooncake 是面向大模型推理的分离式基础设施，核心场景是把 Prefill 和 Decode 拆到不同资源池，并把 KV Cache 放到可共享的设备内存、主机内存或存储池中。[Mooncake 论文](https://arxiv.org/abs/2407.00079)描述了这种 KV Cache-centric 架构和调度目标。

### Transfer Engine：字节搬运层

Transfer Engine（TE，传输引擎）是 Mooncake 的底层数据面：

- `Segment` 表示一组可访问地址范围；
- `Buffer` 表示某个设备上的连续内存区域；
- `BatchTransfer` 批量提交多个 `READ`/`WRITE` 请求；
- 根据内存位置、NUMA 拓扑和设备关系选择传输路径；
- 支持 TCP、RDMA、GPUDirect RDMA、NVMe-oF、NVLink，以及 Ascend 相关 transport；
- 可对大请求切片，利用多网卡并行，并在路径失败时重试。

Mooncake 文档将远端 DRAM/VRAM 的直接读写和多网卡拓扑选择放在 Transfer Engine 中，而不是放在上层模型代码里。[Transfer Engine 设计](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/)

### Mooncake Store：对象和缓存层

Mooncake Store 位于 TE 之上，负责：

- 用对象 key 管理 KV Cache 或模型权重；
- 决定对象放在哪个节点和哪个内存区域；
- 处理复制、淘汰和多级缓存；
- 对大对象进行切片和并行传输；
- 提供对象级写入提交和读取一致性语义。

因此可以按下面的方式区分：

```text
HIXL / ADXL       地址级单边读写
Mooncake TE       统一的数据搬运抽象
Mooncake Store    对象级 KV Cache 存储和生命周期
vLLM / SGLang     请求调度和模型推理逻辑
```

Store 的对象原子写、复制和淘汰不是裸 HIXL `TransferSync` 自动提供的能力。

## 4. Ascend HIXL 如何支持单边通信

HIXL（Huawei Xfer Library，昇腾单边通信库）是 CANN（Compute Architecture for Neural Networks，昇腾计算架构）提供的面向集群的点对点通信库。官方文档强调它支持单边零拷贝，并可在 Host 和 Device 内存之间使用 HCCS 或 RDMA 等链路。[HIXL 应用开发文档](https://www.hiascend.com/document/detail/zh/canncommercial/900/programug/acldevg/aclcppdevg_000538.html)

### 4.1 初始化和内存注册

```cpp
Hixl engine;
std::map<AscendString, AscendString> options;
engine.Initialize(local_engine, options);

MemDesc desc{};
desc.addr = reinterpret_cast<uintptr_t>(buffer);
desc.len = length;

MemHandle handle = nullptr;
engine.RegisterMem(desc, MEM_DEVICE, handle);
```

HIXL 支持 `MEM_DEVICE` 和 `MEM_HOST` 两类注册内存。注册的意义类似于 RDMA Memory Region：库建立访问映射和权限信息，远端只能访问已公开的区间。官方开发指南要求本地和远端内存在建链前完成注册，并要求解注册晚于所有在途操作。[HIXL 内存管理](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900beta2/commlib/hixlug/llmcdv2_42_29.html)

### 4.2 建链和同步读写

```cpp
engine.Connect(remote_engine);

TransferOpDesc op{
    local_addr,
    remote_addr,
    length
};

engine.TransferSync(remote_engine, READ, {op});
engine.TransferSync(remote_engine, WRITE, {op});
```

`READ` 表示“远端到本地”，`WRITE` 表示“本地到远端”。目标端不需要为每一个 `TransferSync` 调用匹配的接收函数，但目标内存必须仍处于注册和有效状态。

### 4.3 异步传输

支持的 CANN 版本和 Ascend 型号可以使用 `TransferAsync`：

```cpp
TransferReq req = nullptr;
engine.TransferAsync(remote_engine, WRITE, {op}, args, req);
```

调用方随后查询请求状态，直到 `COMPLETED` 或 `FAILED`。异步模式适合将传输和 Decode 的其他计算重叠，但并非所有型号都支持，超时处理通常需要断链并重新建链。[TransferAsync API](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900beta2/API/hixlapiref/llmcrv2_42_31.html)

### 4.4 资源释放顺序

推荐顺序是：

```text
等待传输完成
    -> Disconnect
    -> DeregisterMem
    -> 释放 Host/Device 内存
    -> Finalize
```

在传输未完成时解注册或释放内存，可能导致超时、失败或非法访问。

## 5. ADXL 与 HIXL 的关系

ADXL（Ascend Direct Xfer Library，旧版直接传输接口）和 HIXL 不应当视为两个完全独立的通信模型：

- ADXL 是较早的 Ascend Direct 能力或接口命名；CANN 9.2 文档已将相关 ADXL 接口标记为待废弃。
- HIXL 是当前公开的昇腾单边通信库接口，提供 `Initialize`、`RegisterMem`、`Connect`、`TransferSync`、`TransferAsync` 等 API。
- Mooncake 的 Ascend Direct Transport 文档仍描述为“基于 CANN ADXL 能力的适配层”，所以 Mooncake 内部适配层和用户侧 CANN 文档可能出现不同命名。[Mooncake Ascend Direct Transport](https://github.com/kvcache-ai/Mooncake/blob/main/docs/source/design/transfer-engine/ascend_direct_transport.md)

可以用下面的层次理解它们：

```text
Mooncake Transfer Engine
        |
        v
Ascend Direct Transport
        |
        v
CANN ADXL 兼容/底层能力
        |
        v
HIXL 的内存注册、建链和单边读写语义
        |
        v
HCCS / RDMA 等实际链路
```

新业务代码应优先依据目标 CANN 版本的 HIXL 文档和产品支持矩阵，而不是只依据旧 ADXL 名称判断能力。

## 6. Mooncake 如何接入 Ascend 单边通信

Mooncake 通过 Ascend Direct Transport，把自身的 `Segment`、`Buffer` 和批量请求映射到 Ascend 侧的内存注册、端点和读写操作。构建时启用：

```bash
-DUSE_ASCEND_DIRECT=ON
```

运行时的逻辑链条是：

```text
Mooncake Segment / Buffer
        |
        v
本地地址、远端地址、长度、READ/WRITE
        |
        v
Ascend Direct Transport
        |
        v
HIXL/ADXL 注册内存、建链、提交传输
        |
        v
HCCS 或 RDMA
```

常见配置包括：

- `ASCEND_USE_ASYNC_TRANSFER=1`：请求 HIXL 异步传输；默认是同步模式；
- `ASCEND_ENABLE_USE_FABRIC_MEM=1`：在支持的 A3/CANN/HDK 组合上启用 Fabric Memory 路径；
- `HCCL_INTRA_ROCE_ENABLE=1`：在适用的昇腾内部路径上选择 RDMA/RoCE；
- `ASCEND_CONNECT_TIMEOUT`：建链超时；
- `ASCEND_TRANSFER_TIMEOUT`：数据传输超时。

这些选项改变传输路径或执行方式，不会自动解决 KV Cache 的请求归属、版本、一致性或调度问题。Mooncake 当前 Ascend Direct Transport 的源码适配边界可固定到 [commit `0f422b960c0590808c9a8f7f9b85e558a27f754b`](https://github.com/kvcache-ai/Mooncake/tree/0f422b960c0590808c9a8f7f9b85e558a27f754b/mooncake-transfer-engine/src/transport/ascend_transport)。

## 7. PD 分离中的端到端例子

设 Prefill 节点生成 KV Cache，Decode 节点负责后续 token 生成。Decode 节点先注册一块 Device buffer，控制面交换对象 key、远端地址和长度，然后由数据面直接传输：

```text
Prefill 节点
  计算 KV Cache
       |
       | HIXL/Mooncake WRITE
       | HCCS 或 RDMA
       v
Decode 节点
  已注册 Device buffer
       |
       v
  Attention 读取 KV Cache
```

控制面回答“写到哪里、写多少、属于哪个请求”；单边数据面回答“如何搬运实际字节”；Mooncake Store 还可以在更高层负责对象放置、复制、淘汰和命中。Decode 不需要为每一次 KV Cache 写入执行匹配接收调用。

## 8. 成本、限制和排障边界

### 成本

- 内存注册需要页映射、权限密钥和对端元数据，不是零成本操作；
- 零拷贝可以减少 CPU staging 和额外 memcpy，但仍消耗 NIC、设备 DMA 队列和请求描述符；
- 小块请求过多时，启动延迟、建链和状态轮询可能超过有效 payload 时间；
- 多网卡并行能提高大对象吞吐，但也会引入拓扑选择、拥塞和故障重试。

### 常见失败条件

- 远端地址未注册，或访问越过注册区间；
- 权限不允许当前的 `READ`/`WRITE`；
- HCCS 所需的内存对齐不满足，例如部分 Device 内存需要按页表对齐；
- 双方设备上下文、CANN/HDK 版本或产品能力不匹配；
- 链路断开后仍复用旧句柄；
- 请求尚未完成就解注册或释放内存。

### 不能从接口直接推出的结论

不能仅凭“支持 HIXL”推断所有 Ascend 型号都拥有相同的异步语义、Fabric Memory 路径、HCCS 对齐要求或带宽。也不能把 Mooncake Store 的对象原子性归因给裸 HIXL。目标环境仍需按具体 CANN、HDK、芯片、拓扑和传输协议实测。

## 9. 证据与版本边界

- Mooncake 的 Segment、Buffer、BatchTransfer、多网卡和路径选择： [Transfer Engine 官方设计](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/)；
- Mooncake 的 KV Cache-centric 架构和 Store/TE 分层： [Mooncake Architecture](https://kvcache-ai.github.io/Mooncake/design/architecture.html) 与 [论文](https://arxiv.org/abs/2407.00079)；
- HIXL 的零拷贝定位、HCCS/RDMA 支持和 C++ 示例： [昇腾单边通信应用开发](https://www.hiascend.com/document/detail/zh/canncommercial/900/programug/acldevg/aclcppdevg_000538.html)；
- HIXL 的注册、建链、同步传输和资源约束： [HIXL 内存管理开发指南](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900beta2/commlib/hixlug/llmcdv2_42_29.html)；
- HIXL 异步传输支持： [TransferAsync API](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900beta2/API/hixlapiref/llmcrv2_42_31.html)；
- ADXL 的待废弃边界： [CANN 9.2 ADXL 接口文档](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920beta1/commlib/hixlug/docs/zh/api/cpp/deprecated_ADXL-interface.md)；
- Mooncake 的 Ascend Direct Transport 适配： [源码文档](https://github.com/kvcache-ai/Mooncake/blob/main/docs/source/design/transfer-engine/ascend_direct_transport.md) 和固定 commit `0f422b960c0590808c9a8f7f9b85e558a27f754b`。

本文中关于“控制面/数据面分离”、注册成本、竞态和集合通信边界的归纳属于跨来源分析，不是某个库对所有版本和硬件的性能保证。
