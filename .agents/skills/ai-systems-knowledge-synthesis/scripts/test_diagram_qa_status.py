#!/usr/bin/env python3
"""Regression tests for full/delta diagram QA coordination."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("diagram_qa_status.py")


class DiagramQaStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name, content in (("source", "source"), ("render", "render"), ("main", "main"), ("neighbor", "neighbor")):
            (self.root / name).write_text(content, encoding="utf-8")
        self.status = self.root / "status.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def invoke(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *args], check=check, capture_output=True, text=True)

    def request(self, round_: int, scope: str = "full", change: str = "text") -> str:
        args = ["request", "--status-file", str(self.status), "--diagram-id", "demo", "--round", str(round_), "--source", str(self.root / "source"), "--render", str(self.root / "render"), "--crop", f"main-flow={self.root / 'main'}", "--scope", scope, "--change-class", change]
        if scope == "delta":
            args += ["--affected-region", "main-flow", "--neighbor-region", "communication", "--crop", f"communication={self.root / 'neighbor'}"]
        return self.invoke(*args).stdout.strip()

    def pass_request(self, request_id: str, reviewer: str) -> None:
        self.invoke("claim", "--status-file", str(self.status), "--request-id", request_id, "--reviewer", reviewer)
        self.invoke("complete", "--status-file", str(self.status), "--request-id", request_id, "--reviewer", reviewer, "--verdict", "passed")

    def test_full_then_delta_and_release_gate(self) -> None:
        full = self.request(1)
        self.pass_request(full, "full-reviewer")
        delta = self.request(2, "delta")
        self.pass_request(delta, "delta-reviewer")
        self.assertEqual(0, self.invoke("verify", "--status-file", str(self.status), "--request-id", delta).returncode)
        self.assertNotEqual(0, self.invoke("verify", "--status-file", str(self.status), "--request-id", delta, "--required-scope", "full", check=False).returncode)

    def test_geometry_delta_escalates_to_full(self) -> None:
        full = self.request(1)
        self.pass_request(full, "reviewer")
        escalated = self.request(2, "delta", "geometry")
        state = json.loads(self.status.read_text(encoding="utf-8"))
        self.assertEqual("full", state["request"]["scope"])
        self.assertTrue(state["request"]["escalated_to_full"])
        self.pass_request(escalated, "reviewer-2")

    def test_lease_reclaim(self) -> None:
        request_id = self.request(1)
        self.invoke("claim", "--status-file", str(self.status), "--request-id", request_id, "--reviewer", "stale", "--lease-seconds", "1")
        time.sleep(1.2)
        self.invoke("reclaim", "--status-file", str(self.status), "--request-id", request_id)
        self.invoke("claim", "--status-file", str(self.status), "--request-id", request_id, "--reviewer", "recovered")


if __name__ == "__main__":
    unittest.main()
