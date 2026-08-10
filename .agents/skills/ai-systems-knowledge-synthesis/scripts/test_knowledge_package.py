#!/usr/bin/env python3
"""Deterministic smoke and negative tests for the knowledge-package tools."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


initializer = load_module("knowledge_initializer", SCRIPT_DIR / "init_knowledge_workspace.py")
validator = load_module("knowledge_validator", SCRIPT_DIR / "validate_knowledge_package.py")


METHOD_TEMPLATE = """# {title}

## Plain-Language Summary

{summary}

## Symbol Table

| Symbol | Plain-language meaning | Shape or value domain | Lifecycle or owner |
| --- | --- | --- | --- |
| W | Global weight tensor | [8, 16] | Split across four ranks |
| p | Number of participating ranks | Positive integer; here p = 4 | Fixed for this walkthrough |

## Problem And Failure Without It

One device cannot retain the full state; without partitioning, a 64 GiB state exceeds a 24 GiB device.

## Global State And Partition Axis

The global tensor has shape [8, 16] and is split along its second axis over four ranks.

## Tensor Walkthrough

Before partition, tensor W has shape [8, 16]. With four ranks, rank 0 owns columns 0 through 3 and each rank has shape [8, 4]. The local operator maps shape [2, 8] to shape [2, 4]. The all-gather collective sends each rank's shape [2, 4] output to every rank and concatenates columns into shape [2, 16]. This is correct because the column slices are disjoint and cover the global output.

## Lifecycle Differences

### Training Forward

Forward computes the local projection and gathers the output.

### Training Backward And Optimizer

Backward returns the matching gradient slice; the optimizer updates local parameter ownership.

### Prefill

Prefill applies the same weight layout to a batch containing many prompt tokens.

### Decode

Decode applies it to one new token per active request, so the collective repeats more frequently.

## Cost And Buffer Lifetime

Persistent weight memory falls by four. The gathered output is temporary until its consumer finishes.

## Composition And Failure Conditions

The hidden dimension must divide by four; shape [8, 15] is invalid for equal shards.

## Evidence Boundary

The implementation mapping uses [[source:src-megatron]] and [[trace:trace-megatron-training]].
"""

FRAMEWORK_TEMPLATE = """# {name}

## Version Boundary

- Repository: https://example.com/{repo}
- Commit: {commit}
- Version/tag context: test fixture
- Scope exclusions: kernels outside this repository

## Plain-Language Architecture

The launcher creates rank groups, the runtime selects local weight slices, and the model runner executes them.

## User Configuration

The parallel-size key chooses how many ranks share one global weight.

## Implementation Trace

The complete mapping is [[trace:{trace}]]. Each hop explains how state changes.

## Process Groups And Tensor Layout

Ranks in one group own disjoint columns and concatenate local outputs.

## Model Rewrite And Runtime

The runtime replaces a full linear layer with a layer that retains one column slice.

## Training State

Parameters and gradients remain sharded; optimizer state is local where training applies.

## Serving State

The key-value cache (KV) is populated during prefill and read plus appended during decode; training-only profiles mark it not applicable.

## Paper Correspondence And Engineering Differences

The implementation preserves the partition equation while adding buffer scheduling.

## Evidence Boundary

The source claim uses [[source:{source}]].
"""


class KnowledgePackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.workspace = initializer.initialize("parallelism-smoke", self.base)
        self.populate_valid(self.workspace)
        report = validator.validate(self.workspace, update_manifest=True)
        self.assertEqual([], report.errors, "fixture must be valid: " + " | ".join(report.errors))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def populate_valid(self, root: Path) -> None:
        (root / "synthesis.md").write_text(
            """# Parallelism Knowledge Synthesis

## Revision And Scope
This initial revision covers training, prefill, and decode.
## Problem Space
Model state and activations can exceed one device.
## Method System
Methods partition distinct tensor axes or state ownership.
## How Methods Compose
Independent mesh axes can compose when shapes are divisible.
## Training, Prefill, And Decode
Training stores gradients and optimizer state. Prefill writes cache for many tokens. Decode reads and appends cache for new tokens.
## Cross-Framework Implementation Findings
Framework names differ while tensor semantics can match.
## Engineering Conclusions
Choose the partition axis from the dominant memory and communication constraint.
## Evidence Boundaries And Open Questions
Source claims are pinned; performance remains unmeasured.
""",
            encoding="utf-8",
        )
        (root / "crosswalk.md").write_text(
            """# Method-To-Framework Crosswalk

## Semantic Baseline
A method is defined by state ownership and the operation that restores global meaning.
## Method Mappings
| Method semantic | Framework/config | Entry API | Runtime/module | Collective behavior | Tensor layout | Phase | Trace ID |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Column partition | Megatron/tensor size | initialize | parallel linear | concatenate local columns | [8, 4] per rank | training | [[trace:trace-megatron-training]] |
## Semantic Differences
Serving runtimes add scheduling and cache ownership to the weight partition.
## Composition And Incompatibilities
Uneven hidden dimensions cannot use equal column shards.
## Evidence Boundary
Mappings use pinned source records.
""",
            encoding="utf-8",
        )
        (root / "glossary.md").write_text(
            """# Glossary

## Terms

### Tensor parallelism
- Abbreviation: TP
- Aliases: tensor model parallelism
- Plain explanation: Several devices each compute one slice of a large tensor operation.
- Strict definition: A global tensor is partitioned across a process group and communication restores global operator semantics.
- Commonly confused with: data parallelism, which replicates model computation.
- Sources: src-megatron
""",
            encoding="utf-8",
        )
        (root / "methods" / "tensor-parallel.md").write_text(
            METHOD_TEMPLATE.format(
                title="Tensor Parallel (TP)",
                summary="Tensor parallelism (Tensor Parallel, TP) lets several devices each compute a slice of one large matrix operation.",
            ),
            encoding="utf-8",
        )
        (root / "methods" / "zero.md").write_text(
            METHOD_TEMPLATE.format(
                title="Zero Redundancy Optimizer",
                summary="Zero Redundancy Optimizer stores one ownership shard of training state on each rank instead of keeping every copy.",
            ),
            encoding="utf-8",
        )

        commit = "a" * 40
        profiles = (
            ("megatron", "Megatron Core", "src-megatron", "trace-megatron-training"),
            ("deepspeed", "DeepSpeed", "src-deepspeed", "trace-deepspeed-training"),
            ("vllm", "vLLM", "src-vllm", "trace-vllm-decode"),
        )
        for filename, name, source, trace in profiles:
            (root / "frameworks" / f"{filename}.md").write_text(
                FRAMEWORK_TEMPLATE.format(
                    name=name, repo=filename, commit=commit, trace=trace, source=source
                ),
                encoding="utf-8",
            )

        sources = [
            {
                "id": source,
                "type": "pinned-source",
                "title": name,
                "url": f"https://example.com/{filename}/tree/{commit}",
                "repository": f"example/{filename}",
                "commit": commit,
                "accessed": "2026-08-02",
            }
            for filename, name, source, _ in profiles
        ]
        (root / "sources.jsonl").write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in sources), encoding="utf-8"
        )

        def hop(symbol: str, behavior: str) -> dict[str, str]:
            return {"path": "runtime/example.py", "symbol": symbol, "lines": "10-20", "behavior": behavior}

        traces = []
        for filename, _, source, trace_id in profiles:
            phase = "decode" if filename == "vllm" else "training"
            traces.append(
                {
                    "id": trace_id,
                    "framework": filename,
                    "method": "tensor-parallel",
                    "source_id": source,
                    "phase": phase,
                    "config": hop("parallel_size", "Reads the requested group size and selects participating ranks."),
                    "entry_api": hop("initialize", "Creates the distributed context and passes the group to the runtime."),
                    "runtime": hop("ParallelLinear", "Keeps one weight-column slice and computes its local output values."),
                    "collective": hop("all_gather", "Sends every local output slice to all ranks and concatenates columns."),
                    "tensor_layout": hop("Shard(1)", "Records that each rank owns one disjoint slice of the second axis."),
                }
            )
        (root / "implementation-traces.jsonl").write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in traces), encoding="utf-8"
        )

    def clone(self, name: str) -> Path:
        target = self.base / name
        shutil.copytree(self.workspace, target)
        return target

    def assert_error_contains(self, root: Path, needle: str, refresh: bool = False) -> None:
        report = validator.validate(root, update_manifest=refresh)
        self.assertTrue(any(needle in error for error in report.errors), report.errors)

    def test_valid_smoke_package(self) -> None:
        report = validator.validate(self.workspace)
        self.assertEqual([], report.errors)
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "validate_knowledge_package.py"), str(self.workspace)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        validation = json.loads((self.workspace / "validation.json").read_text(encoding="utf-8"))
        self.assertEqual("pass", validation["status"])

    def test_missing_source_field(self) -> None:
        root = self.clone("missing-field")
        rows = (root / "sources.jsonl").read_text(encoding="utf-8").splitlines()
        row = json.loads(rows[0]); row.pop("title"); rows[0] = json.dumps(row)
        (root / "sources.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
        self.assert_error_contains(root, "missing fields", refresh=True)

    def test_duplicate_id(self) -> None:
        root = self.clone("duplicate")
        line = (root / "sources.jsonl").read_text(encoding="utf-8").splitlines()[0]
        with (root / "sources.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        self.assert_error_contains(root, "duplicate id", refresh=True)

    def test_unpinned_commit(self) -> None:
        root = self.clone("commit")
        text = (root / "sources.jsonl").read_text(encoding="utf-8").replace("a" * 40, "main")
        (root / "sources.jsonl").write_text(text, encoding="utf-8")
        self.assert_error_contains(root, "full lowercase SHA", refresh=True)

    def test_broken_reference(self) -> None:
        root = self.clone("reference")
        with (root / "synthesis.md").open("a", encoding="utf-8") as handle:
            handle.write("\nUnknown evidence [[source:missing-source]].\n")
        self.assert_error_contains(root, "broken source reference", refresh=True)

    def test_incorrect_hash(self) -> None:
        root = self.clone("hash")
        with (root / "synthesis.md").open("a", encoding="utf-8") as handle:
            handle.write("\nChanged after hashing.\n")
        self.assert_error_contains(root, "hash mismatch")

    def test_unexplained_abbreviation(self) -> None:
        root = self.clone("acronym")
        with (root / "synthesis.md").open("a", encoding="utf-8") as handle:
            handle.write("\nXYZ changes the runtime.\n")
        self.assert_error_contains(root, "unexplained abbreviation", refresh=True)

    def test_missing_tensor_walkthrough(self) -> None:
        root = self.clone("walkthrough")
        path = root / "methods" / "tensor-parallel.md"
        text = path.read_text(encoding="utf-8").replace("shape [8, 16]", "a large shape").replace("shape [8, 4]", "a local shape").replace("shape [2, 8]", "an input shape").replace("shape [2, 4]", "an output shape").replace("shape [2, 16]", "a restored shape")
        path.write_text(text, encoding="utf-8")
        self.assert_error_contains(root, "numeric global and rank-local shapes", refresh=True)

    def test_missing_symbol_table(self) -> None:
        root = self.clone("symbol-table")
        path = root / "methods" / "tensor-parallel.md"
        text = path.read_text(encoding="utf-8")
        start = text.index("## Symbol Table")
        end = text.index("## Problem And Failure Without It")
        path.write_text(text[:start] + text[end:], encoding="utf-8")
        self.assert_error_contains(root, "missing sections: Symbol Table", refresh=True)

    def test_formula_without_explanation(self) -> None:
        root = self.clone("formula")
        with (root / "synthesis.md").open("a", encoding="utf-8") as handle:
            handle.write("\n$$\ny = x + 1\n$$\nThis sentence does not explain symbols.\n")
        self.assert_error_contains(root, "formula lacks", refresh=True)

    def test_symbol_only_behavior(self) -> None:
        root = self.clone("behavior")
        rows = [json.loads(line) for line in (root / "implementation-traces.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["runtime"]["behavior"] = rows[0]["runtime"]["symbol"]
        (root / "implementation-traces.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )
        self.assert_error_contains(root, "behavior must explain", refresh=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
