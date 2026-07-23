#!/usr/bin/env python3
"""Validate a research domain using a resolved skill-owned organization profile."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

from resolve_organization import resolve

LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")


def git_tracked(repo: Path, path: Path) -> bool:
    rel = path.resolve().relative_to(repo.resolve())
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(rel)],
        cwd=repo,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def document_files(domain: Path, organization: dict) -> tuple[list[Path], dict[str, list[Path]]]:
    by_type: dict[str, list[Path]] = {}
    entry = domain / organization["domain_entry"]
    files = [entry] if entry.exists() else []
    for doc_type, relative in organization["document_paths"].items():
        root = domain / relative
        by_type[doc_type] = sorted(root.rglob("*.md")) if root.exists() else []
        files.extend(by_type[doc_type])
    return files, by_type


def parse_target(source: Path, raw: str) -> Path | None:
    raw = raw.strip().split("#", 1)[0]
    if not raw or raw.startswith(("http://", "https://", "mailto:", "#")):
        return None
    return (source.parent / raw).resolve()


def validate(repo: Path, domain: Path, resolution: dict) -> dict:
    organization = resolution["organization"]
    config = organization["validation"]
    errors: list[dict] = []
    warnings: list[dict] = [{"code": "organization-resolution-warning", "message": w} for w in resolution["warnings"]]
    inbound: dict[Path, set[Path]] = defaultdict(set)
    referenced_assets: set[Path] = set()
    files, by_type = document_files(domain, organization)
    entry = (domain / organization["domain_entry"]).resolve()
    assets_root = (domain / organization["asset_paths"]["root"]).resolve()

    domain_rel = str(domain.relative_to(repo))
    patterns = resolution["repository"].get("domain_patterns", [])
    if patterns and not any(fnmatch.fnmatch(domain_rel, pattern) for pattern in patterns):
        errors.append({"code": "domain-outside-repository-profile", "domain": domain_rel, "patterns": patterns})
    if not entry.exists():
        errors.append({"code": "missing-domain-entry", "path": str(entry)})

    for source in files:
        text = source.read_text(encoding="utf-8")
        for token in organization["formal_forbidden_patterns"]:
            if token in text:
                errors.append({"code": "forbidden-reference", "path": str(source), "token": token})
        for raw in LINK_RE.findall(text):
            target = parse_target(source, raw)
            if target is None:
                continue
            if config["require_relative_links"] and Path(raw.split("#", 1)[0]).is_absolute():
                errors.append({"code": "absolute-local-link", "path": str(source), "target": raw})
                continue
            if not under(target, repo):
                errors.append({"code": "outside-repository-link", "path": str(source), "target": raw})
                continue
            if not target.exists():
                errors.append({"code": "broken-relative-link", "path": str(source), "target": raw})
                continue
            inbound[target].add(source.resolve())
            if under(target, assets_root) and target.is_file():
                referenced_assets.add(target)
                if config["require_git_tracked_assets"] and not git_tracked(repo, target):
                    errors.append({"code": "untracked-formal-asset", "path": str(source), "target": str(target.relative_to(repo))})
        # Evidence inventories may record assets as inline-code paths rather than links.
        for raw in INLINE_CODE_RE.findall(text):
            candidate = raw.split(";", 1)[0].strip()
            target = (source.parent / candidate).resolve()
            if target.exists() and target.is_file() and under(target, assets_root):
                referenced_assets.add(target)

    if config["check_orphan_documents"]:
        for doc_type in organization["relationships"]["domain_entry_indexes"]:
            for document in by_type.get(doc_type, []):
                if entry not in inbound.get(document.resolve(), set()):
                    errors.append({"code": "document-missing-domain-entry-inbound", "doc_type": doc_type, "path": str(document.relative_to(repo))})

        any_parent_types = organization["relationships"]["paper_backlinks_to_any"]
        all_parent_types = organization["relationships"]["paper_backlinks_to_all"]
        for paper in by_type.get("paper", []):
            sources = inbound.get(paper.resolve(), set())
            for required in all_parent_types:
                if required == "domain-entry" and entry not in sources:
                    errors.append({"code": "paper-missing-required-backlink", "required": required, "path": str(paper.relative_to(repo))})
                elif required in organization["document_paths"]:
                    root = (domain / organization["document_paths"][required]).resolve()
                    if not any(under(source, root) for source in sources):
                        errors.append({"code": "paper-missing-required-backlink", "required": required, "path": str(paper.relative_to(repo))})
            accepted_roots = [(domain / organization["document_paths"][kind]).resolve() for kind in any_parent_types if kind in organization["document_paths"]]
            if accepted_roots and not any(any(under(source, root) for root in accepted_roots) for source in sources):
                errors.append({"code": "paper-missing-parent-backlink", "required_any": any_parent_types, "path": str(paper.relative_to(repo))})

    if assets_root.exists():
        for asset in sorted(p for p in assets_root.rglob("*") if p.is_file()):
            if config["check_orphan_assets"] and asset.resolve() not in referenced_assets:
                warnings.append({"code": "orphan-formal-asset", "path": str(asset.relative_to(repo))})
            if config["require_git_tracked_assets"] and not git_tracked(repo, asset):
                severity = errors if asset.resolve() in referenced_assets else warnings
                severity.append({"code": "untracked-formal-asset", "path": str(asset.relative_to(repo))})

    return {
        "validation_schema_version": "2.0.0",
        "repository_root": str(repo.resolve()),
        "domain": domain_rel,
        "organization": organization,
        "organization_provenance": resolution["provenance"],
        "status": "passed" if not errors else "failed",
        "checked_markdown": len(files),
        "referenced_assets": len(referenced_assets),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--profile", help="Explicit repository profile; otherwise use discovery")
    parser.add_argument("--resolved-output", help="Optional resolved-organization JSON output")
    parser.add_argument("--output", help="Optional validation JSON output under the configured process root")
    args = parser.parse_args()
    repo = Path(args.repo_root).resolve()
    domain = (repo / args.domain).resolve()
    if not domain.exists():
        raise SystemExit(f"domain does not exist: {domain}")
    resolution = resolve(repo, domain, args.profile)
    if args.resolved_output:
        target = Path(args.resolved_output)
        target = target if target.is_absolute() else repo / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(resolution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = validate(repo, domain, resolution)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        output = Path(args.output)
        output = output if output.is_absolute() else repo / output
        process_root = (repo / resolution["organization"]["process_root"]).resolve()
        if not under(output, process_root):
            raise SystemExit(f"--output must be under configured process root: {process_root}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
