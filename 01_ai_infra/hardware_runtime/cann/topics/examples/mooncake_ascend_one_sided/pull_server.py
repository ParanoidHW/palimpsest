#!/usr/bin/env python3
"""Prepare and expose a dict of NPU tensors for a one-sided READ client."""

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
    parser.add_argument("--control-port", type=int, default=15556)
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
    device = f"npu:{args.device}"
    tensors = {
        "key_cache": torch.arange(args.rows * args.cols, dtype=torch.float16, device=device)
        .reshape(args.rows, args.cols)
        .add_(1000),
        "value_cache": torch.arange(args.rows * args.cols, dtype=torch.float16, device=device)
        .reshape(args.rows, args.cols)
        .add_(2000),
        "block_table": torch.arange(args.rows * 8, dtype=torch.int32, device=device).reshape(
            args.rows, 8
        ),
    }
    # Make the prepared payload visible to the transport before publishing it.
    torch.npu.synchronize()

    engine = TransferEngine()
    ret = engine.initialize(args.advertise_host, "P2PHANDSHAKE", args.protocol, "")
    if ret != 0:
        raise RuntimeError(f"TransferEngine.initialize failed: {ret}")

    remote_buffers = []
    listener = None
    try:
        for name, tensor in tensors.items():
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

        session_id = f"{args.advertise_host}:{engine.get_rpc_port()}"
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((args.control_bind, args.control_port))
        listener.listen(1)
        print(f"pull_server_session_id={session_id}", flush=True)
        print(f"prepared_buffers={[item['name'] for item in remote_buffers]}", flush=True)
        print(f"waiting_for_pull_client={args.control_port}", flush=True)
        conn, peer = listener.accept()
        with conn:
            send_json_line(
                conn,
                {"operation": "read", "session_id": session_id, "buffers": remote_buffers},
            )
            if recv_line(conn) != b"DONE":
                raise RuntimeError("client did not acknowledge READ completion")
        print(f"pull_completed_by={peer[0]}", flush=True)
    finally:
        if listener is not None:
            listener.close()
        for item in remote_buffers:
            ret = engine.unregister_memory(item["ptr"])
            if ret != 0:
                raise RuntimeError(f"unregister_memory failed for {item['name']}: {ret}")


if __name__ == "__main__":
    main()
