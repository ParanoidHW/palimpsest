#!/usr/bin/env python3
"""Resolve the built-in research organization with an optional repository profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from copy import deepcopy
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REFS = SKILL_DIR / "references"
DEFAULT_PROFILE = REFS / "default-profile.json"
ORGANIZATION_SCHEMA = REFS / "organization-schema.json"
REPOSITORY_PROFILE_SCHEMA = REFS / "repository-profile-schema.json"
UNION_LIST_PATHS = {
    "process_only_kinds",
    "formal_forbidden_patterns",
    "relationships.domain_entry_indexes",
    "relationships.survey_links_to",
    "relationships.paper_backlinks_to_any",
    "relationships.paper_backlinks_to_all",
}
NON_WEAKENABLE_FLAGS = {
    "validation.require_relative_links",
    "validation.require_git_tracked_assets",
    "validation.check_orphan_documents",
    "validation.check_orphan_assets",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_json(instance: dict, schema_path: Path, label: str) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise RuntimeError("jsonschema is required to validate research knowledge profiles") from exc
    errors = sorted(Draft202012Validator(load_json(schema_path)).iter_errors(instance), key=lambda e: list(e.absolute_path))
    if errors:
        detail = "; ".join(f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors)
        raise ValueError(f"invalid {label}: {detail}")


def find_repository_profile(repo: Path, start: Path, explicit: str | None) -> Path | None:
    if explicit:
        candidate = Path(explicit)
        return (candidate if candidate.is_absolute() else repo / candidate).resolve()
    env_profile = os.environ.get("RESEARCH_KB_PROFILE")
    if env_profile:
        candidate = Path(env_profile)
        return (candidate if candidate.is_absolute() else repo / candidate).resolve()
    cursor = start.resolve()
    if cursor.is_file():
        cursor = cursor.parent
    profile_names = ("research-knowledge.profile.json", ".research-knowledge.json")
    while True:
        for name in profile_names:
            candidate = cursor / name
            if candidate.exists():
                return candidate
        if cursor == repo or cursor.parent == cursor or repo not in cursor.parents:
            break
        cursor = cursor.parent
    for name in profile_names:
        candidate = repo / name
        if candidate.exists():
            return candidate
    return None


def deep_merge(base: dict, overlay: dict, prefix: str = "") -> dict:
    out = deepcopy(base)
    for key, value in overlay.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value, path)
        elif isinstance(value, list) and path in UNION_LIST_PATHS:
            out[key] = list(dict.fromkeys([*out.get(key, []), *value]))
        else:
            if path in NON_WEAKENABLE_FLAGS and out.get(key) is True and value is False:
                raise ValueError(f"repository profile cannot weaken built-in invariant: {path}")
            out[key] = deepcopy(value)
    return out


def resolve(repo: Path, start: Path, explicit_profile: str | None = None) -> dict:
    default = load_json(DEFAULT_PROFILE)
    validate_json(default, ORGANIZATION_SCHEMA, "built-in organization")
    profile_path = find_repository_profile(repo, start, explicit_profile)
    profile = None
    warnings: list[str] = []
    resolved = deepcopy(default)
    if profile_path:
        if not profile_path.exists():
            raise FileNotFoundError(f"repository profile does not exist: {profile_path}")
        profile = load_json(profile_path)
        validate_json(profile, REPOSITORY_PROFILE_SCHEMA, "repository profile")
        resolved = deep_merge(resolved, profile.get("overrides", {}))
        resolved["profile_id"] = profile["profile_id"]
    validate_json(resolved, ORGANIZATION_SCHEMA, "resolved organization")

    policy_documents = []
    for raw in (profile or {}).get("policy_documents", []):
        path = (repo / raw).resolve()
        exists = path.exists()
        if not exists:
            warnings.append(f"policy document does not exist: {raw}")
        policy_documents.append({"path": raw, "exists": exists, "sha256": sha256(path) if exists and path.is_file() else None})

    return {
        "resolution_schema_version": "1.0.0",
        "organization": resolved,
        "provenance": {
            "organization_schema": str(ORGANIZATION_SCHEMA),
            "organization_schema_sha256": sha256(ORGANIZATION_SCHEMA),
            "default_profile": str(DEFAULT_PROFILE),
            "default_profile_sha256": sha256(DEFAULT_PROFILE),
            "repository_profile": str(profile_path) if profile_path else None,
            "repository_profile_sha256": sha256(profile_path) if profile_path else None,
            "policy_documents": policy_documents,
        },
        "repository": {
            "profile_id": (profile or {}).get("profile_id"),
            "domain_patterns": (profile or {}).get("domain_patterns", []),
        },
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--start", default=".", help="Domain or path used for nearest-profile discovery")
    parser.add_argument("--profile", help="Explicit repository profile; overrides discovery")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()
    repo = Path(args.repo_root).resolve()
    start = (repo / args.start).resolve()
    result = resolve(repo, start, args.profile)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        output = Path(args.output)
        output = output if output.is_absolute() else repo / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
