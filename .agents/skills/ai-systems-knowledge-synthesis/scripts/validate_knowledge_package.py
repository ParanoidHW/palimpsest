#!/usr/bin/env python3
"""Validate an AI systems knowledge package and emit validation.json."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_FILES = {
    "synthesis.md",
    "crosswalk.md",
    "implementation-traces.jsonl",
    "sources.jsonl",
    "glossary.md",
    "knowledge-package.json",
    "execution_checklist.md",
    "validation.json",
}
METHOD_SECTIONS = {
    "Plain-Language Summary",
    "Symbol Table",
    "Problem And Failure Without It",
    "Global State And Partition Axis",
    "Tensor Walkthrough",
    "Lifecycle Differences",
    "Cost And Buffer Lifetime",
    "Composition And Failure Conditions",
    "Evidence Boundary",
}
FRAMEWORK_SECTIONS = {
    "Version Boundary",
    "Plain-Language Architecture",
    "User Configuration",
    "Implementation Trace",
    "Process Groups And Tensor Layout",
    "Model Rewrite And Runtime",
    "Training State",
    "Serving State",
    "Paper Correspondence And Engineering Differences",
    "Evidence Boundary",
}
SYNTHESIS_SECTIONS = {
    "Revision And Scope",
    "Problem Space",
    "Method System",
    "How Methods Compose",
    "Training, Prefill, And Decode",
    "Cross-Framework Implementation Findings",
    "Engineering Conclusions",
    "Evidence Boundaries And Open Questions",
}
CROSSWALK_SECTIONS = {
    "Semantic Baseline",
    "Method Mappings",
    "Semantic Differences",
    "Composition And Incompatibilities",
    "Evidence Boundary",
}
HOPS = ("config", "entry_api", "runtime", "collective", "tensor_layout")
SOURCE_TYPES = {"paper", "official-doc", "pinned-source", "measurement", "analysis-derived"}
BUILTIN_ACRONYMS = {"AI", "API", "ASCII", "CPU", "CUDA", "GPU", "HTTP", "HTTPS", "ID", "JSON", "JSONL", "NVME", "SHA", "URL"}
SOURCE_REF_RE = re.compile(r"\[\[source:([A-Za-z0-9._-]+)\]\]")
TRACE_REF_RE = re.compile(r"\[\[trace:([A-Za-z0-9._-]+)\]\]")
ACRONYM_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z][A-Z0-9]{1,7})(?![A-Za-z0-9])")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_json(path: Path, report: Report) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.error(f"{path.name}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        report.error(f"{path.name}: root must be an object")
        return {}
    return value


def read_jsonl(path: Path, report: Report) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        report.error(f"{path.name}: cannot read: {exc}")
        return rows
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            report.error(f"{path.name}:{number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(row, dict):
            report.error(f"{path.name}:{number}: row must be an object")
            continue
        row["__line__"] = number
        rows.append(row)
    return rows


def headings(text: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^##+\s+(.+?)\s*$", text, re.MULTILINE)}


def check_sections(path: Path, required: set[str], report: Report) -> str:
    text = path.read_text(encoding="utf-8")
    missing = sorted(required - headings(text))
    if missing:
        report.error(f"{path.relative_to(path.parents[1])}: missing sections: {', '.join(missing)}")
    return text


def validate_sources(rows: list[dict[str, Any]], report: Report) -> set[str]:
    ids: set[str] = set()
    for row in rows:
        line = row.pop("__line__", "?")
        missing = [key for key in ("id", "type", "title", "url", "accessed") if not row.get(key)]
        if missing:
            report.error(f"sources.jsonl:{line}: missing fields: {', '.join(missing)}")
        source_id = row.get("id")
        if source_id in ids:
            report.error(f"sources.jsonl:{line}: duplicate id {source_id}")
        elif isinstance(source_id, str):
            ids.add(source_id)
        if row.get("type") not in SOURCE_TYPES:
            report.error(f"sources.jsonl:{line}: unsupported type {row.get('type')!r}")
        if row.get("type") == "pinned-source":
            if not row.get("repository"):
                report.error(f"sources.jsonl:{line}: pinned-source requires repository")
            if not re.fullmatch(r"[0-9a-f]{40}", str(row.get("commit", ""))):
                report.error(f"sources.jsonl:{line}: pinned-source commit must be a full lowercase SHA")
    return ids


def validate_traces(
    rows: list[dict[str, Any]], source_ids: set[str], source_types: dict[str, str], report: Report
) -> set[str]:
    ids: set[str] = set()
    for row in rows:
        line = row.pop("__line__", "?")
        missing = [key for key in ("id", "framework", "method", "source_id", "phase") if not row.get(key)]
        if missing:
            report.error(f"implementation-traces.jsonl:{line}: missing fields: {', '.join(missing)}")
        trace_id = row.get("id")
        if trace_id in ids:
            report.error(f"implementation-traces.jsonl:{line}: duplicate id {trace_id}")
        elif isinstance(trace_id, str):
            ids.add(trace_id)
        if row.get("source_id") not in source_ids:
            report.error(f"implementation-traces.jsonl:{line}: unknown source_id {row.get('source_id')!r}")
        elif source_types.get(str(row.get("source_id"))) != "pinned-source":
            report.error(
                f"implementation-traces.jsonl:{line}: implementation trace source must be pinned-source"
            )
        if row.get("phase") not in {"training", "prefill", "decode"}:
            report.error(f"implementation-traces.jsonl:{line}: phase must be training, prefill, or decode")
        for hop_name in HOPS:
            hop = row.get(hop_name)
            if not isinstance(hop, dict):
                report.error(f"implementation-traces.jsonl:{line}: missing hop {hop_name}")
                continue
            absent = [key for key in ("path", "symbol", "lines", "behavior") if not hop.get(key)]
            if absent:
                report.error(f"implementation-traces.jsonl:{line}:{hop_name}: missing {', '.join(absent)}")
            behavior = str(hop.get("behavior", "")).strip()
            symbol = str(hop.get("symbol", "")).strip()
            if len(behavior) < 20 or behavior == symbol or re.fullmatch(r"[A-Za-z0-9_:.()/-]+", behavior):
                report.error(f"implementation-traces.jsonl:{line}:{hop_name}: behavior must explain the hop, not only name code")
    return ids


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`]*`", "", text)


def check_formula_explanations(path: Path, text: str, report: Report) -> None:
    lines = text.splitlines()
    in_formula = False
    for index, line in enumerate(lines):
        if line.strip() == "$$":
            if not in_formula:
                in_formula = True
                continue
            in_formula = False
            next_text = next((candidate.strip() for candidate in lines[index + 1 :] if candidate.strip()), "")
            if not (next_text.startswith("公式解释：") or next_text.lower().startswith("formula explanation:")):
                report.error(f"{path.name}:{index + 1}: displayed formula lacks a following natural-language explanation")
    if in_formula:
        report.error(f"{path.name}: unclosed displayed formula")


def acronym_is_defined(text: str, acronym: str, start: int) -> bool:
    prefix = text[max(0, start - 240) : start + len(acronym) + 2]
    patterns = (
        rf"\([A-Za-z][^()]{{2,180}}(?:,\s*|\s+){re.escape(acronym)}\)",
        rf"（[^（）]{{2,180}}(?:,|，)\s*{re.escape(acronym)}）",
        rf"[A-Za-z][A-Za-z -]{{2,120}}\s*\({re.escape(acronym)}\)",
        rf"Abbreviation:\s*{re.escape(acronym)}(?:\s|$)",
    )
    return any(re.search(pattern, prefix) for pattern in patterns)


def check_readability(path: Path, text: str, report: Report) -> None:
    cleaned = strip_code(text)
    check_formula_explanations(path, cleaned, report)
    seen: set[str] = set()
    for match in ACRONYM_RE.finditer(cleaned):
        acronym = match.group(1)
        if acronym in BUILTIN_ACRONYMS or acronym in seen:
            continue
        seen.add(acronym)
        if not acronym_is_defined(cleaned, acronym, match.start()):
            report.error(f"{path.name}: unexplained abbreviation at first use: {acronym}")
    for number, line in enumerate(cleaned.splitlines(), 1):
        if len(line) > 220 and not line.lstrip().startswith(("|", "http")):
            report.warn(f"{path.name}:{number}: long line may hide a dense causal explanation")
        terms = ACRONYM_RE.findall(line)
        if len(terms) >= 5:
            report.warn(f"{path.name}:{number}: high abbreviation density requires human review")


def check_method(path: Path, report: Report) -> None:
    text = check_sections(path, METHOD_SECTIONS, report)
    match = re.search(r"^## Tensor Walkthrough\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    section = match.group(1) if match else ""
    numeric_shapes = re.findall(r"(?:shape|形状)[^\n]{0,30}(?:\d+\s*[,x×]\s*\d+|\[[0-9, x×]+\])", section, re.IGNORECASE)
    if len(numeric_shapes) < 2:
        report.error(f"{path.name}: Tensor Walkthrough requires numeric global and rank-local shapes")
    if not re.search(r"collective|集合通信|all[-_ ]?(?:reduce|gather|to[-_ ]all)|reduce[-_ ]scatter", section, re.IGNORECASE):
        report.error(f"{path.name}: Tensor Walkthrough must explain a collective")
    check_readability(path, text, report)


def collect_markdown(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def check_references(markdown: list[Path], source_ids: set[str], trace_ids: set[str], report: Report) -> None:
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        for source_id in SOURCE_REF_RE.findall(text):
            if source_id not in source_ids:
                report.error(f"{path.name}: broken source reference {source_id}")
        for trace_id in TRACE_REF_RE.findall(text):
            if trace_id not in trace_ids:
                report.error(f"{path.name}: broken trace reference {trace_id}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_files(root: Path) -> list[Path]:
    excluded = {"knowledge-package.json", "validation.json"}
    return sorted(
        path for path in root.rglob("*") if path.is_file() and path.name not in excluded
    )


def refresh_manifest(root: Path, manifest: dict[str, Any]) -> None:
    manifest["files"] = {
        path.relative_to(root).as_posix(): sha256(path) for path in package_files(root)
    }


def validate_manifest(root: Path, manifest: dict[str, Any], report: Report) -> None:
    missing = [key for key in ("schema_version", "slug", "revision", "generated_at", "files", "validation") if key not in manifest]
    if missing:
        report.error(f"knowledge-package.json: missing fields: {', '.join(missing)}")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        report.error("knowledge-package.json: files must contain output hashes")
        return
    actual_paths = {path.relative_to(root).as_posix() for path in package_files(root)}
    if set(files) != actual_paths:
        missing_hashes = sorted(actual_paths - set(files))
        stale_hashes = sorted(set(files) - actual_paths)
        if missing_hashes:
            report.error(f"knowledge-package.json: missing hashes: {', '.join(missing_hashes)}")
        if stale_hashes:
            report.error(f"knowledge-package.json: hashes reference missing files: {', '.join(stale_hashes)}")
    for relative, expected in files.items():
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            report.error(f"knowledge-package.json: unsafe file path {relative}")
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", str(expected)):
            report.error(f"knowledge-package.json: invalid SHA-256 for {relative}")
            continue
        path = root / relative
        if path.is_file() and sha256(path) != expected:
            report.error(f"knowledge-package.json: hash mismatch for {relative}")


def validate(root: Path, update_manifest: bool = False) -> Report:
    report = Report()
    if not root.is_dir():
        report.error(f"workspace does not exist: {root}")
        return report
    present = {path.name for path in root.iterdir() if path.is_file()}
    for name in sorted(REQUIRED_FILES - present):
        report.error(f"missing required file: {name}")
    for directory in ("methods", "frameworks"):
        if not (root / directory).is_dir():
            report.error(f"missing required directory: {directory}")
    if report.errors:
        return report

    manifest = read_json(root / "knowledge-package.json", report)
    if update_manifest and manifest:
        refresh_manifest(root, manifest)
        (root / "knowledge-package.json").write_text(
            json.dumps(manifest, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
        )

    source_rows = read_jsonl(root / "sources.jsonl", report)
    trace_rows = read_jsonl(root / "implementation-traces.jsonl", report)
    source_ids = validate_sources(source_rows, report)
    source_types = {
        str(row.get("id")): str(row.get("type")) for row in source_rows if row.get("id")
    }
    trace_ids = validate_traces(trace_rows, source_ids, source_types, report)

    check_sections(root / "synthesis.md", SYNTHESIS_SECTIONS, report)
    check_sections(root / "crosswalk.md", CROSSWALK_SECTIONS, report)
    glossary = (root / "glossary.md").read_text(encoding="utf-8")
    if "Terms" not in headings(glossary):
        report.error("glossary.md: missing Terms section")

    method_files = sorted((root / "methods").glob("*.md"))
    framework_files = sorted((root / "frameworks").glob("*.md"))
    if not method_files:
        report.error("methods/: at least one method card is required")
    if not framework_files:
        report.error("frameworks/: at least one framework profile is required")
    for path in method_files:
        check_method(path, report)
    for path in framework_files:
        text = check_sections(path, FRAMEWORK_SECTIONS, report)
        if not re.search(r"\b[0-9a-f]{40}\b", text):
            report.error(f"{path.name}: Version Boundary requires a full commit SHA")
        check_readability(path, text, report)

    markdown = collect_markdown(root)
    for path in markdown:
        if path not in method_files and path not in framework_files:
            check_readability(path, path.read_text(encoding="utf-8"), report)
    check_references(markdown, source_ids, trace_ids, report)
    validate_manifest(root, manifest, report)
    return report


def write_results(root: Path, report: Report, update_manifest: bool) -> None:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    status = "pass" if not report.errors else "fail"
    result = {"status": status, "errors": report.errors, "warnings": report.warnings, "validated_at": now}
    if root.is_dir():
        (root / "validation.json").write_text(
            json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
        )
        if update_manifest and (root / "knowledge-package.json").is_file():
            manifest = json.loads((root / "knowledge-package.json").read_text(encoding="utf-8"))
            manifest["validation"] = {"status": status, "validated_at": now}
            (root / "knowledge-package.json").write_text(
                json.dumps(manifest, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--update-manifest", action="store_true", help="refresh hashes before validation")
    args = parser.parse_args()
    report = validate(args.workspace, args.update_manifest)
    write_results(args.workspace, report, args.update_manifest)
    for error in report.errors:
        print(f"ERROR: {error}")
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    print(f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
