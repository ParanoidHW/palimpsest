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

SCOPES = {"full", "delta"}
CHANGE_CLASSES = {"text", "crop", "geometry", "semantic"}
DEFAULT_LEASE_SECONDS = 10 * 60


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


def parse_regions(values: list[str], option: str) -> list[str]:
    regions: list[str] = []
    for value in values:
        for region in value.split(","):
            region = region.strip()
            if not region:
                continue
            if region not in CROP_REGIONS:
                raise ValueError(f"invalid {option} region: {region}")
            if region not in regions:
                regions.append(region)
    return regions


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def lease_valid(review: dict[str, Any], at: dt.datetime | None = None) -> bool:
    expires = parse_time(review.get("lease_expires_at"))
    return expires is not None and expires > (at or dt.datetime.now(dt.timezone.utc))


def expires_at(seconds: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=seconds)).isoformat(
        timespec="seconds"
    )


def effective_scope(request_data: dict[str, Any]) -> str:
    return request_data.get("scope", "full")


def state_history(state: dict[str, Any]) -> list[dict[str, Any]]:
    history = state.get("history", [])
    return history if isinstance(history, list) else []


def baseline_candidates(state: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = [state, *reversed(state_history(state))]
    return [
        item
        for item in candidates
        if item.get("status") == "passed"
        and effective_scope(item.get("request", {})) == "full"
    ]


def find_request(state: dict[str, Any], request_id: str) -> dict[str, Any] | None:
    for item in [state, *state_history(state)]:
        if item.get("request_id") == request_id:
            return item
    return None


def review_regions(request_data: dict[str, Any]) -> list[str]:
    affected = request_data.get("affected_regions", [])
    neighbors = request_data.get("neighbor_regions", [])
    if effective_scope(request_data) == "delta":
        return list(dict.fromkeys([*affected, *neighbors]))
    return [item.get("region", "other") for item in request_data.get("crops", [])]


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
    affected_regions = parse_regions(args.affected_region, "affected")
    neighbor_regions = parse_regions(args.neighbor_region, "neighbor")
    crop_paths = [item["path"] for item in crops]
    crop_hashes = [item["sha256"] for item in crops]
    if len(crop_paths) != len(set(crop_paths)):
        raise ValueError("crop paths must be unique")
    if len(crop_hashes) != len(set(crop_hashes)):
        raise ValueError("crop contents must be distinct")
    if any(item["sha256"] == render["sha256"] for item in crops):
        raise ValueError("a crop is byte-identical to the full render")
    scope = args.scope
    escalated = False
    if args.change_class in {"geometry", "semantic"} and scope == "delta":
        scope, escalated = "full", True
    if scope == "delta" and not affected_regions:
        raise ValueError("delta request requires at least one affected region")
    declared = set(affected_regions) | set(neighbor_regions)
    supplied = {item["region"] for item in crops}
    if scope == "delta" and not declared.issubset(supplied):
        raise ValueError(f"delta crops missing declared regions: {', '.join(sorted(declared - supplied))}")
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
            "scope": scope,
            "base_request_id": args.base_request_id,
            "change_class": args.change_class,
            "affected_regions": affected_regions,
            "neighbor_regions": neighbor_regions,
            "escalated_to_full": escalated,
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
            "review_scope": None,
            "checked_regions": [],
            "escalated_to_full": escalated,
            "lease_expires_at": None,
            "last_heartbeat_at": None,
        },
        "history": [],
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
            if scope == "delta":
                candidates = baseline_candidates(previous)
                if not candidates:
                    raise ValueError("delta request requires a passed full baseline")
                selected = args.base_request_id or candidates[0]["request_id"]
                baseline = find_request(previous, selected)
                if not baseline or baseline.get("status") != "passed" or effective_scope(baseline.get("request", {})) != "full":
                    raise ValueError("base request must be a passed full request")
                base_request = baseline["request"]
                base_contract = base_request.get("contract")
                current_contract = state["request"].get("contract")
                if (
                    base_request.get("source", {}).get("sha256") != source["sha256"]
                    or (base_contract or {}).get("sha256") != (current_contract or {}).get("sha256")
                ):
                    state["request"]["scope"] = "full"
                    state["request"]["escalated_to_full"] = True
                    state["review"]["escalated_to_full"] = True
                    scope = "full"
                state["request"]["base_request_id"] = selected
            state["history"] = [*state_history(previous), {k: v for k, v in previous.items() if k != "history"}]
        elif scope == "delta":
            raise ValueError("first request must use full scope")
        atomic_write(status_path, state)
    print(request_id)
    return 0


def claim(args: argparse.Namespace) -> int:
    if args.lease_seconds <= 0:
        raise ValueError("lease-seconds must be positive")
    status_path = Path(args.status_file)
    with locked(status_path):
        state = load(status_path)
        require_request(state, args.request_id)
        if state["status"] not in {"pending", "reviewing"}:
            raise ValueError(f"cannot claim status {state['status']}")
        existing = state["review"]["reviewer"]
        if existing not in {None, args.reviewer} and lease_valid(state["review"]):
            raise ValueError(f"already claimed by {existing}")
        state["status"] = "reviewing"
        state["updated_at"] = now()
        state["review"]["reviewer"] = args.reviewer
        state["review"]["reviewer_role"] = "independent-qa-subagent"
        if existing != args.reviewer or not state["review"].get("claimed_at"):
            state["review"]["claimed_at"] = state["updated_at"]
        state["review"]["last_heartbeat_at"] = state["updated_at"]
        state["review"]["lease_expires_at"] = expires_at(args.lease_seconds)
        atomic_write(status_path, state)
    return 0


def heartbeat(args: argparse.Namespace) -> int:
    if args.lease_seconds <= 0:
        raise ValueError("lease-seconds must be positive")
    status_path = Path(args.status_file)
    with locked(status_path):
        state = load(status_path)
        require_request(state, args.request_id)
        if state["status"] != "reviewing" or state["review"]["reviewer"] != args.reviewer:
            raise ValueError("reviewer does not own a reviewing request")
        if not lease_valid(state["review"]):
            raise ValueError("reviewer lease expired; reclaim the request")
        state["updated_at"] = now()
        state["review"]["last_heartbeat_at"] = state["updated_at"]
        state["review"]["lease_expires_at"] = expires_at(args.lease_seconds)
        atomic_write(status_path, state)
    return 0


def reclaim(args: argparse.Namespace) -> int:
    status_path = Path(args.status_file)
    with locked(status_path):
        state = load(status_path)
        require_request(state, args.request_id)
        if state["status"] != "reviewing" or lease_valid(state["review"]):
            raise ValueError("request has an active lease or is not reviewing")
        state["status"] = "pending"
        state["updated_at"] = now()
        for key, value in (("reviewer", None), ("reviewer_role", None), ("claimed_at", None), ("lease_expires_at", None), ("last_heartbeat_at", None)):
            state["review"][key] = value
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
        # Legacy status files predate scoped QA and bound the updater hash.  Keep
        # their source/render/crop integrity checks intact while allowing the
        # coordinator itself to evolve without invalidating historical passes.
        legacy_tool = item is state["request"].get("qa_tool") and "scope" not in state["request"]
        if not legacy_tool and sha256(path) != item["sha256"]:
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
        if state["review"].get("lease_expires_at") and not lease_valid(state["review"]):
            raise ValueError("reviewer lease expired; reclaim the request")
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
        state["review"]["review_scope"] = effective_scope(state["request"])
        state["review"]["checked_regions"] = review_regions(state["request"])
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
        (args.required_scope == "delta" or effective_scope(state["request"]) == "full", "full scope is required"),
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
        (review.get("review_scope", effective_scope(state["request"])) == effective_scope(state["request"]), "review scope does not match request"),
        (set(review.get("checked_regions", review_regions(state["request"]))) >= set(review_regions(state["request"])), "not all declared regions were checked"),
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
                "review_scope": effective_scope(state["request"]),
            },
            indent=2,
        )
    )
    return 0


def show(args: argparse.Namespace) -> int:
    state = load(Path(args.status_file))
    expires = parse_time(state.get("review", {}).get("lease_expires_at"))
    if expires is not None:
        remaining = max(0, int((expires - dt.datetime.now(dt.timezone.utc)).total_seconds()))
        state["review"]["lease_remaining_seconds"] = remaining
        state["review"]["lease_state"] = "active" if remaining else "expired"
    print(json.dumps(state, ensure_ascii=False, indent=2))
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
    create.add_argument("--scope", choices=sorted(SCOPES), default="full")
    create.add_argument("--base-request-id")
    create.add_argument("--change-class", choices=sorted(CHANGE_CLASSES), default="text")
    create.add_argument("--affected-region", action="append", default=[])
    create.add_argument("--neighbor-region", action="append", default=[])
    create.set_defaults(run=request)

    take = commands.add_parser("claim")
    take.add_argument("--status-file", required=True)
    take.add_argument("--request-id", required=True)
    take.add_argument("--reviewer", required=True)
    take.add_argument("--lease-seconds", type=int, default=DEFAULT_LEASE_SECONDS)
    take.set_defaults(run=claim)

    renew = commands.add_parser("heartbeat", aliases=["renew"])
    renew.add_argument("--status-file", required=True)
    renew.add_argument("--request-id", required=True)
    renew.add_argument("--reviewer", required=True)
    renew.add_argument("--lease-seconds", type=int, default=DEFAULT_LEASE_SECONDS)
    renew.set_defaults(run=heartbeat)

    recover = commands.add_parser("reclaim")
    recover.add_argument("--status-file", required=True)
    recover.add_argument("--request-id", required=True)
    recover.set_defaults(run=reclaim)

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
    check.add_argument("--required-scope", choices=sorted(SCOPES), default="delta")
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
