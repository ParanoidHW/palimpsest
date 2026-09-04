#!/usr/bin/env python3
"""Pull a dict of NPU tensors with Mooncake's one-sided READ operation."""

from __future__ import annotations

import argparse
import json
import os
import socket

import torch
import torch_npu  # noqa: F401  # Registers the NPU backend.
from mooncake.engine import TransferEngine


def recv_json_line(sock: socket.socket) -> dict[str, object]:
    data = bytearray()
    while b"\n" not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise RuntimeError("server closed control connection")
        data.extend(chunk)
    return json.loads(bytes(data).split(b"\n", 1)[0].decode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--server-host", required=True)
    parser.add_argument("--control-port", type=int, default=15556)
    parser.add_argument("--local-host", default=os.getenv("MC_HOST_IP"))
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--protocol", default=os.getenv("MOONCAKE_PROTOCOL", "ascend"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.local_host:
        raise SystemExit("--local-host or MC_HOST_IP is required")

    with socket.create_connection((args.server_host, args.control_port)) as control:
        remote = recv_json_line(control)
        if remote.get("operation") != "read":
            raise RuntimeError(f"unexpected operation: {remote.get('operation')}")

        dtype_by_name = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
            "int32": torch.int32,
        }
        torch.npu.set_device(args.device)
        device = f"npu:{args.device}"
        local_tensors = {}
        local_buffers = []
        for item in remote["buffers"]:
            name = str(item["name"])
            shape = tuple(int(x) for x in item["shape"])
            dtype = dtype_by_name[str(item["dtype"])]
            tensor = torch.empty(shape, dtype=dtype, device=device)
            local_tensors[name] = tensor
            length = tensor.numel() * tensor.element_size()
            remote_length = int(item["length"])
            if length != remote_length:
                raise ValueError(f"metadata size mismatch for {name}")
            local_buffers.append(
                {
                    "name": name,
                    "ptr": tensor.data_ptr(),
                    "length": length,
                    "remote_ptr": int(item["ptr"]),
                }
            )

        engine = TransferEngine()
        ret = engine.initialize(args.local_host, "P2PHANDSHAKE", args.protocol, "")
        if ret != 0:
            raise RuntimeError(f"TransferEngine.initialize failed: {ret}")
        for item in local_buffers:
            ret = engine.register_memory(item["ptr"], item["length"])
            if ret != 0:
                raise RuntimeError(f"register_memory failed for {item['name']}: {ret}")

        try:
            ret = engine.batch_transfer_sync_read(
                str(remote["session_id"]),
                [item["ptr"] for item in local_buffers],
                [item["remote_ptr"] for item in local_buffers],
                [item["length"] for item in local_buffers],
            )
            if ret < 0:
                raise RuntimeError(f"batch_transfer_sync_read failed: {ret}")
            torch.npu.synchronize()
            previews = {name: tensor.flatten()[:4].cpu().tolist() for name, tensor in local_tensors.items()}
            control.sendall(b"DONE\n")
            print(
                f"pull_ok tensors={list(local_tensors)} "
                f"bytes={sum(item['length'] for item in local_buffers)} previews={previews}"
            )
        finally:
            for item in local_buffers:
                ret = engine.unregister_memory(item["ptr"])
                if ret != 0:
                    raise RuntimeError(f"unregister_memory failed for {item['name']}: {ret}")


if __name__ == "__main__":
    main()
