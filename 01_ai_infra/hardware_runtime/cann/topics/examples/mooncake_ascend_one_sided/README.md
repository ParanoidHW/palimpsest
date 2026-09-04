# Mooncake Ascend 单边 Tensor 字典传输样例

这组样例演示一个最小的两进程流程：server 持有并注册由多个 Ascend NPU tensor 组成的 Python `dict`，client 创建同构的本地 `dict`，通过 Mooncake Transfer Engine 的批量单边 `WRITE` 将所有 tensor 写入 server 的远端 buffer。控制面使用一个普通 TCP socket 只交换 `session_id`、每个 tensor 的远端地址、长度、shape、dtype 和名称；实际 payload 不经过这个 socket。

默认字典包含三个键：`key_cache`、`value_cache` 和 `block_table`，分别模拟 KV Cache 的 K/V 张量和块表。每个 tensor 单独注册，但 client 用 `batch_transfer_sync_write` 一次提交多个非连续 buffer。

## 前置条件

- 两端均为可用的 Ascend NPU 环境，并已加载 CANN、`torch_npu` 和 Mooncake Ascend NPU Python 包。
- Mooncake 已按 Ascend Direct Transport 构建（`-DUSE_ASCEND_DIRECT=ON`），并安装对应的 Python wheel；当前文档推荐 Ascend NPU 使用 `mooncake-transfer-engine-npu`。
- 两端网络可互相访问控制端口和 Mooncake Transfer Engine 的 RPC 端口；`--advertise-host`/`--local-host` 必须是对端可达的本机 IP 或 DNS 名称，不能使用 `0.0.0.0`。
- `protocol=ascend` 是 Mooncake Python/配置层的 Ascend transport 名称；如果目标发行版提供的绑定要求其他名称，可通过 `--protocol` 覆盖，并以该版本的 transport 注册名为准。

## 运行

先在目标端启动 server：

```bash
export MC_HOST_IP=10.0.0.2
export HCCL_INTRA_ROCE_ENABLE=1  # 可选：要求走适用的 RDMA/RoCE 路径
python server.py --advertise-host "$MC_HOST_IP" --device 0 --rows 1024 --cols 4096
```

再在发起端启动 client：

```bash
export MC_HOST_IP=10.0.0.3
export HCCL_INTRA_ROCE_ENABLE=1
python client.py --server-host 10.0.0.2 --local-host "$MC_HOST_IP" --device 0
```

server 输出的 `previews` 应包含三个键，并分别出现 `[0.0, 1.0, ...]` 一类的前几个元素（浮点类型下可能显示等价的 dtype 表示）。未设置 `HCCL_INTRA_ROCE_ENABLE=1` 时，具体链路由 Ascend Direct Transport 根据平台和配置选择，常见路径包括 HCCS。

## Server 预置数据，Client 拉取

这条路径使用独立的 `pull_server.py` 和 `pull_client.py`：server 先构造并注册带数据的 `dict`，client 通过控制面获得远端描述，分配本地空字典，然后发起批量单边 `READ`。

先启动准备数据的 server：

```bash
export MC_HOST_IP=10.0.0.2
export HCCL_INTRA_ROCE_ENABLE=1
python pull_server.py --advertise-host "$MC_HOST_IP" --device 0 --rows 1024 --cols 4096
```

再启动拉取数据的 client：

```bash
export MC_HOST_IP=10.0.0.3
export HCCL_INTRA_ROCE_ENABLE=1
python pull_client.py --server-host 10.0.0.2 --local-host "$MC_HOST_IP" --device 0
```

此时数据方向是：

```text
server 的已注册 key_cache/value_cache/block_table
        -- batch_transfer_sync_read -->
client 的本地目标 key_cache/value_cache/block_table
```

`READ` 的发起者是 client，`buffer` 参数指向 client 本地目标，`peer_buffer_addresses` 指向 server 已注册的远端地址。server 不需要为这个请求调用 `receive`，但必须在 client 返回 `DONE` 前保持字典 tensor 和注册状态有效。

## 读语义和 KV Cache 改造

样例只演示 client 对字典中的多个 tensor 发起批量 `WRITE`。若改为 client 从 server 拉取 KV Cache，应为 client 先按远端元数据分配并注册本地目标字典，再调用：

```python
ret = engine.batch_transfer_sync_read(
    str(remote["session_id"]),  # server session
    [item["ptr"] for item in local_buffers],
    [item["ptr"] for item in remote["buffers"]],
    [item["length"] for item in remote["buffers"]],
)
```

生产 KV Cache 传输还需要在控制面增加请求 ID、字典 key 到 cache block 的映射、版本/校验信息、ready 通知和超时回收；不能把裸指针和长度直接当作对象一致性协议。每个 `register_memory` 返回成功后都必须保持对应 tensor 存活，直到该批传输完成并完成 `unregister_memory`。

## 证据边界

Python 方法名和参数依据 Mooncake Transfer Engine Python API；Ascend Direct 的构建选项、`ascend` transport、HCCS/RDMA 选择和 ADXL 适配边界依据 Mooncake 官方文档。该样例未在当前环境连接真实 NPU，运行前需按目标 Mooncake/CANN/HDK 版本校正包版本、设备可见性和 transport 注册名。
