#!/usr/bin/env python3
"""Validate one research-knowledge domain against the project publication contract."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

FORMAL_DIRS = {"surveys", "papers", "topics", "evidence", "supplements"}
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
ASSET_PATH_RE = re.compile(r"(?:\.\./)+assets/[A-Za-z0-9_./-]+")
FORBIDDEN = ("_artifacts", "file://", "page_png", "page-render", "page_render")


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


def markdown_files(domain: Path) -> list[Path]:
    files = [domain / "README.md"] if (domain / "README.md").exists() else []
    for folder in FORMAL_DIRS:
        root = domain / folder
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return files


def parse_target(source: Path, raw: str) -> Path | None:
    raw = raw.strip().split("#", 1)[0]
    if not raw or raw.startswith(("http://", "https://", "mailto:", "#")):
        return None
    return (source.parent / raw).resolve()


def validate(repo: Path, domain: Path) -> dict:
    errors: list[dict] = []
    warnings: list[dict] = []
    inbound: dict[Path, set[Path]] = defaultdict(set)
    referenced_assets: set[Path] = set()
    files = markdown_files(domain)

    if not (domain / "README.md").exists():
        errors.append({"code": "missing-readme", "path": str(domain / "README.md")})

    for source in files:
        text = source.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:
                errors.append({"code": "forbidden-reference", "path": str(source), "token": token})
        for raw in LINK_RE.findall(text):
            target = parse_target(source, raw)
            if target is None:
                continue
            if target.is_absolute() and repo.resolve() not in target.parents and target != repo.resolve():
                errors.append({"code": "outside-repository-link", "path": str(source), "target": raw})
                continue
            if not target.exists():
                errors.append({"code": "broken-relative-link", "path": str(source), "target": raw})
                continue
            inbound[target].add(source.resolve())
            if "assets" in target.parts:
                referenced_assets.add(target)
                if not git_tracked(repo, target):
                    errors.append({"code": "untracked-formal-asset", "path": str(source), "target": str(target.relative_to(repo))})
        # Figure inventories often record canonical assets as inline-code paths.
        for raw in ASSET_PATH_RE.findall(text):
            target = (source.parent / raw).resolve()
            if target.exists() and target.is_file():
                referenced_assets.add(target)

    readme = (domain / "README.md").resolve()
    for paper in sorted((domain / "papers").glob("*.md")) if (domain / "papers").exists() else []:
        sources = inbound.get(paper.resolve(), set())
        if readme not in sources:
            errors.append({"code": "paper-missing-readme-inbound", "path": str(paper.relative_to(repo))})
        parent_sources = [p for p in sources if "surveys" in p.parts or "evidence" in p.parts]
        if not parent_sources:
            errors.append({"code": "paper-missing-survey-or-index-inbound", "path": str(paper.relative_to(repo))})

    assets_root = domain / "assets"
    if assets_root.exists():
        for asset in sorted(p for p in assets_root.rglob("*") if p.is_file()):
            if asset.resolve() not in referenced_assets:
                warnings.append({"code": "orphan-formal-asset", "path": str(asset.relative_to(repo))})
            if asset.resolve() not in referenced_assets and not git_tracked(repo, asset):
                warnings.append({"code": "untracked-formal-asset-unreferenced", "path": str(asset.relative_to(repo))})

    return {
        "schema_version": "1.0.0",
        "repository_root": str(repo.resolve()),
        "domain": str(domain.relative_to(repo)),
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
    parser.add_argument("--output", help="Optional JSON output path under _artifacts")
    args = parser.parse_args()
    repo = Path(args.repo_root).resolve()
    domain = (repo / args.domain).resolve()
    if not domain.exists():
        raise SystemExit(f"domain does not exist: {domain}")
    result = validate(repo, domain)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        output = (repo / args.output).resolve()
        if "_artifacts" not in output.parts:
            raise SystemExit("--output must be under _artifacts")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
