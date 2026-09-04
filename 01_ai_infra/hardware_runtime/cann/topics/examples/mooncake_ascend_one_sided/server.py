#!/usr/bin/env python3
"""Receive a dict of NPU tensors through Mooncake Ascend Direct Transport.

The TCP socket in this sample is control-plane metadata exchange only. The
payload is transferred by Mooncake's one-sided WRITE operation.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
from typing import Any

import torch
import torch_npu  # noqa: F401  # Registers the NPU backend.
from mooncake.engine import TransferEngine


def recv_line(conn: socket.socket) -> bytes:
    data = bytearray()
    while b"\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            raise RuntimeError("control connection closed before DONE")
        data.extend(chunk)
    return bytes(data).split(b"\n", 1)[0]


def send_json_line(conn: socket.socket, value: dict[str, Any]) -> None:
    conn.sendall(json.dumps(value).encode("utf-8") + b"\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--advertise-host", default=os.getenv("MC_HOST_IP"))
    parser.add_argument("--control-bind", default="0.0.0.0")
    parser.add_argument("--control-port", type=int, default=15555)
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--rows", type=int, default=1024)
    parser.add_argument("--cols", type=int, default=4096)
    parser.add_argument("--protocol", default=os.getenv("MOONCAKE_PROTOCOL", "ascend"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.advertise_host:
        raise SystemExit("--advertise-host or MC_HOST_IP is required")

    torch.npu.set_device(args.device)
    dtype_by_name = {
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "float32": torch.float32,
        "int32": torch.int32,
    }
    tensor_specs = {
        "key_cache": ((args.rows, args.cols), "float16"),
        "value_cache": ((args.rows, args.cols), "float16"),
        "block_table": ((args.rows, 8), "int32"),
    }
    # Keep every tensor alive until the client has acknowledged completion.
    receive_tensors = {
        name: torch.zeros(
            shape, dtype=dtype_by_name[dtype_name], device=f"npu:{args.device}"
        )
        for name, (shape, dtype_name) in tensor_specs.items()
    }
    torch.npu.synchronize()

    engine = TransferEngine()
    local_host = args.advertise_host
    ret = engine.initialize(local_host, "P2PHANDSHAKE", args.protocol, "")
    if ret != 0:
        raise RuntimeError(f"TransferEngine.initialize failed: {ret}")

    remote_buffers = []
    try:
        for name, tensor in receive_tensors.items():
            ptr = tensor.data_ptr()
            length = tensor.numel() * tensor.element_size()
            ret = engine.register_memory(ptr, length)
            if ret != 0:
                raise RuntimeError(f"register_memory failed for {name}: {ret}")
            remote_buffers.append(
                {
                    "name": name,
                    "ptr": ptr,
                    "length": length,
                    "shape": list(tensor.shape),
                    "dtype": str(tensor.dtype).removeprefix("torch."),
                }
            )

        session_id = f"{local_host}:{engine.get_rpc_port()}"
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((args.control_bind, args.control_port))
        listener.listen(1)

        print(f"server_session_id={session_id}", flush=True)
        print(f"server_buffers={[item['name'] for item in remote_buffers]}", flush=True)
        print(f"waiting_for_client={args.control_port}", flush=True)
        try:
            conn, peer = listener.accept()
            with conn:
                send_json_line(conn, {"session_id": session_id, "buffers": remote_buffers})
                if recv_line(conn) != b"DONE":
                    raise RuntimeError("client did not acknowledge transfer")
            torch.npu.synchronize()
            previews = {
                name: tensor.flatten()[:4].cpu().tolist()
                for name, tensor in receive_tensors.items()
            }
            print(f"received_from={peer[0]} previews={previews}", flush=True)
        finally:
            listener.close()
    finally:
        for item in remote_buffers:
            ret = engine.unregister_memory(item["ptr"])
            if ret != 0:
                raise RuntimeError(f"unregister_memory failed for {item['name']}: {ret}")


if __name__ == "__main__":
    main()
