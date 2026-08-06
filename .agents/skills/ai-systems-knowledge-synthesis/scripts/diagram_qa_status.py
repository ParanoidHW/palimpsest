#!/usr/bin/env python3
"""Coordinate diagram QA through a hash-bound, atomically updated status file."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Iterator


CHECKLIST = [
    "full-frame-original-resolution",
    "all-crops-original-pixels",
    "arrow-endpoints",
    "nonzero-communication-shaft",
    "isolated-text",
    "line-spacing-baseline",
    "semantic-grouping",
    "composition-centering",
    "one-sided-whitespace",
    "stale-crop",
]

CROP_REGIONS = {
    "main-flow",
    "communication",
    "cross-rank-return",
    "ownership-time",
    "legend-footer",
    "other",
}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact(path: str) -> dict[str, str]:
    resolved = Path(path)
    if not resolved.is_file():
        raise ValueError(f"artifact does not exist: {path}")
    return {"path": path, "sha256": sha256(resolved)}


def crop_artifact(value: str) -> dict[str, str]:
    if "=" not in value:
        raise ValueError("crop must use REGION=PATH")
    region, path = value.split("=", 1)
    if region not in CROP_REGIONS:
        raise ValueError(f"invalid crop region: {region}")
    item = artifact(path)
    item["region"] = region
    return item


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)


@contextlib.contextmanager
def locked(status_path: Path) -> Iterator[None]:
    lock_path = status_path.with_suffix(status_path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def require_request(state: dict[str, Any], request_id: str) -> None:
    if state.get("request_id") != request_id:
        raise ValueError(
            f"stale request: expected {state.get('request_id')}, received {request_id}"
        )


def request(args: argparse.Namespace) -> int:
    if args.round < 1:
        raise ValueError("round must be at least 1")
    if re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.diagram_id) is None:
        raise ValueError("diagram ID must be lowercase kebab-case")
    status_path = Path(args.status_file)
    render = artifact(args.render)
    source = artifact(args.source)
    crops = [crop_artifact(value) for value in args.crop]
    crop_paths = [item["path"] for item in crops]
    crop_hashes = [item["sha256"] for item in crops]
    if len(crop_paths) != len(set(crop_paths)):
        raise ValueError("crop paths must be unique")
    if len(crop_hashes) != len(set(crop_hashes)):
        raise ValueError("crop contents must be distinct")
    if any(item["sha256"] == render["sha256"] for item in crops):
        raise ValueError("a crop is byte-identical to the full render")
    request_id = f"{args.round}-{render['sha256'][:12]}"
    timestamp = now()
    state = {
        "schema_version": 1,
        "diagram_id": args.diagram_id,
        "request_id": request_id,
        "review_round": args.round,
        "status": "pending",
        "updated_at": timestamp,
        "request": {
            "requested_at": timestamp,
            "requested_by": "main-agent",
            "qa_tool": artifact(str(Path(__file__).resolve())),
            "source": source,
            "render": render,
            "crops": crops,
            "contract": artifact(args.contract) if args.contract else None,
            "checklist": CHECKLIST,
        },
        "review": {
            "reviewer": None,
            "reviewer_role": None,
            "claimed_at": None,
            "completed_at": None,
            "verdict": None,
            "reviewed_request_id": None,
            "reviewed_render_sha256": None,
            "reviewed_crops": [],
            "findings": [],
            "summary": "",
        },
    }
    with locked(status_path):
        if status_path.exists():
            previous = load(status_path)
            if previous["diagram_id"] != args.diagram_id:
                raise ValueError("diagram ID cannot change within one status file")
            if args.round <= previous["review_round"]:
                raise ValueError(
                    f"round must increase beyond {previous['review_round']}"
                )
        atomic_write(status_path, state)
    print(request_id)
    return 0


def claim(args: argparse.Namespace) -> int:
    status_path = Path(args.status_file)
    with locked(status_path):
        state = load(status_path)
        require_request(state, args.request_id)
        if state["status"] not in {"pending", "reviewing"}:
            raise ValueError(f"cannot claim status {state['status']}")
        existing = state["review"]["reviewer"]
        if existing not in {None, args.reviewer}:
            raise ValueError(f"already claimed by {existing}")
        state["status"] = "reviewing"
        state["updated_at"] = now()
        state["review"]["reviewer"] = args.reviewer
        state["review"]["reviewer_role"] = "independent-qa-subagent"
        state["review"]["claimed_at"] = state["updated_at"]
        atomic_write(status_path, state)
    return 0


def read_findings(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return []
    with Path(path).open("r", encoding="utf-8") as handle:
        findings = json.load(handle)
    if not isinstance(findings, list):
        raise ValueError("findings file must contain a JSON array")
    required = {"severity", "region", "description", "resolved"}
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != required:
            raise ValueError(f"invalid finding: {finding!r}")
        if finding["severity"] not in {"blocker", "major", "minor", "note"}:
            raise ValueError(f"invalid severity: {finding['severity']}")
        if not isinstance(finding["resolved"], bool):
            raise ValueError("finding resolved must be boolean")
    return findings


def current_artifacts_match(state: dict[str, Any]) -> tuple[bool, str]:
    requested = [
        state["request"]["qa_tool"],
        state["request"]["source"],
        state["request"]["render"],
    ]
    requested.extend(state["request"]["crops"])
    if state["request"]["contract"] is not None:
        requested.append(state["request"]["contract"])
    for item in requested:
        path = Path(item["path"])
        if not path.is_file():
            return False, f"missing artifact: {item['path']}"
        if sha256(path) != item["sha256"]:
            return False, f"artifact changed after request: {item['path']}"
    return True, ""


def complete(args: argparse.Namespace) -> int:
    status_path = Path(args.status_file)
    findings = read_findings(args.findings_file)
    with locked(status_path):
        state = load(status_path)
        require_request(state, args.request_id)
        if state["status"] != "reviewing":
            raise ValueError(f"cannot complete status {state['status']}")
        if state["review"]["reviewer"] != args.reviewer:
            raise ValueError("reviewer does not own this request")
        matches, reason = current_artifacts_match(state)
        verdict = args.verdict if matches else "error"
        if verdict == "passed" and any(not item["resolved"] for item in findings):
            raise ValueError("passed verdict cannot contain unresolved findings")
        timestamp = now()
        state["status"] = verdict
        state["updated_at"] = timestamp
        state["review"]["completed_at"] = timestamp
        state["review"]["verdict"] = verdict
        state["review"]["reviewed_request_id"] = args.request_id
        state["review"]["reviewed_render_sha256"] = state["request"]["render"]["sha256"]
        state["review"]["reviewed_crops"] = state["request"]["crops"]
        state["review"]["findings"] = findings
        state["review"]["summary"] = reason or args.summary
        atomic_write(status_path, state)
    if verdict == "error":
        print(reason, file=sys.stderr)
        return 2
    return 0


def verify(args: argparse.Namespace) -> int:
    status_path = Path(args.status_file)
    with locked(status_path):
        state = load(status_path)
        require_request(state, args.request_id)
        matches, reason = current_artifacts_match(state)
    review = state["review"]
    checks = [
        (matches, reason),
        (state["status"] == "passed", f"status is {state['status']}"),
        (review["verdict"] == "passed", f"verdict is {review['verdict']}"),
        (
            review["reviewer_role"] == "independent-qa-subagent",
            "reviewer role is not independent-qa-subagent",
        ),
        (
            review["reviewed_request_id"] == state["request_id"],
            "reviewed request ID does not match",
        ),
        (
            review["reviewed_render_sha256"] == state["request"]["render"]["sha256"],
            "reviewed render hash does not match",
        ),
        (
            review["reviewed_crops"] == state["request"]["crops"],
            "reviewed crop set does not match",
        ),
        (
            not any(not item["resolved"] for item in review["findings"]),
            "unresolved findings remain",
        ),
    ]
    failures = [message for passed, message in checks if not passed]
    if failures:
        print(json.dumps({"passed": False, "failures": failures}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "passed": True,
                "diagram_id": state["diagram_id"],
                "request_id": state["request_id"],
                "render_sha256": state["request"]["render"]["sha256"],
                "reviewer": review["reviewer"],
                "completed_at": review["completed_at"],
            },
            indent=2,
        )
    )
    return 0


def show(args: argparse.Namespace) -> int:
    print(json.dumps(load(Path(args.status_file)), ensure_ascii=False, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    create = commands.add_parser("request")
    create.add_argument("--status-file", required=True)
    create.add_argument("--diagram-id", required=True)
    create.add_argument("--round", type=int, required=True)
    create.add_argument("--source", required=True)
    create.add_argument("--render", required=True)
    create.add_argument(
        "--crop",
        action="append",
        required=True,
        metavar="REGION=PATH",
        help="tag each distinct original-pixel crop with its review region",
    )
    create.add_argument("--contract")
    create.set_defaults(run=request)

    take = commands.add_parser("claim")
    take.add_argument("--status-file", required=True)
    take.add_argument("--request-id", required=True)
    take.add_argument("--reviewer", required=True)
    take.set_defaults(run=claim)

    finish = commands.add_parser("complete")
    finish.add_argument("--status-file", required=True)
    finish.add_argument("--request-id", required=True)
    finish.add_argument("--reviewer", required=True)
    finish.add_argument(
        "--verdict", choices=["passed", "changes-requested", "error"], required=True
    )
    finish.add_argument("--findings-file")
    finish.add_argument("--summary", default="")
    finish.set_defaults(run=complete)

    check = commands.add_parser("verify")
    check.add_argument("--status-file", required=True)
    check.add_argument("--request-id", required=True)
    check.set_defaults(run=verify)

    display = commands.add_parser("show")
    display.add_argument("--status-file", required=True)
    display.set_defaults(run=show)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.run(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
