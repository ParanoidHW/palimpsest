#!/usr/bin/env python3
"""Validate v1.8 narrative review structure without scoring prose quality."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import jsonschema


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(manifest_path: Path, schema_path: Path, canonical_paper: Path | None = None) -> dict:
    errors: list[str] = []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for issue in jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).iter_errors(manifest):
        errors.append(f"schema:{'.'.join(map(str, issue.path)) or '$'}: {issue.message}")

    root = manifest_path.parent
    loaded: dict[str, str] = {}
    for name, entry in manifest.get("artifacts", {}).items():
        rel = Path(entry.get("path", ""))
        if rel.is_absolute() or ".." in rel.parts or not rel.parts:
            errors.append(f"artifact:{name}: path must stay inside review folder")
            continue
        path = root / rel
        if not path.is_file():
            errors.append(f"artifact:{name}: missing {rel}")
            continue
        if digest(path) != entry.get("sha256"):
            errors.append(f"artifact:{name}: sha256 mismatch")
        if path.suffix in {".md", ".txt"}:
            loaded[name] = path.read_text(encoding="utf-8")

    analysis = loaded.get("analysis", "")
    inventory = loaded.get("figure_inventory", "")
    review = loaded.get("reading_review", "")
    revision = manifest.get("revision", {})
    authorship = manifest.get("paper", {}).get("authorship_and_affiliations", {})
    if authorship.get("identity_status") == "personal":
        authors = authorship.get("ordered_authors", [])
        if not authors or not authorship.get("first_authors") or not set(authorship.get("first_authors", [])).issubset(authors):
            errors.append("authorship: missing or inconsistent first-author mapping")
        mappings = authorship.get("role_affiliations", [])
        mapped_names = {entry.get("name") for entry in mappings}
        if not set(authorship.get("first_authors", []) + authorship.get("corresponding_authors", [])).issubset(mapped_names):
            errors.append("authorship: first/corresponding author affiliation mapping incomplete")
        for entry in mappings:
            if entry.get("name") not in authors:
                errors.append("authorship: mapped person absent from ordered author list")
            for value in entry.get("affiliations", []) + [entry.get("evidence", "")]:
                if value not in analysis:
                    errors.append(f"authorship: mapping evidence {value!r} absent from report")
    for name in authorship.get("ordered_authors", []) + authorship.get("first_authors", []) + authorship.get("corresponding_authors", []):
        if name not in analysis:
            errors.append(f"authorship: {name!r} absent from report")
    if authorship.get("evidence", "") not in analysis:
        errors.append("authorship: source evidence absent from report")
    publication = manifest.get("publication", {})
    canonical_rel = Path(publication.get("canonical_path", ""))
    if canonical_rel.is_absolute() or ".." in canonical_rel.parts:
        errors.append("publication: canonical path must be repository-relative")
    if manifest.get("invocation_mode") == "standalone" and not publication.get("promotion_plan_path"):
        errors.append("publication: standalone review requires promotion plan path")

    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", analysis, re.S)
    tags = re.findall(r"(?m)^\s+-\s+([^\s]+)\s*$", frontmatter.group(1)) if frontmatter else []
    expected_tags = manifest.get("paper", {}).get("tags", [])
    if sorted(tags) != sorted(expected_tags):
        errors.append("paper: frontmatter tags differ from manifest")
    dimensions = ("paper", "collection/", "domain/", "status/deep-review", "topic/", "method/")
    if len(tags) != 6 or any(sum(t == d if d in {"paper", "status/deep-review"} else t.startswith(d) for t in tags) != 1 for d in dimensions):
        errors.append("paper: six required tag dimensions are incomplete")
    if revision.get("id", "") not in analysis or revision.get("document_version", "") not in analysis:
        errors.append("revision: id/version not present in analysis")

    if len(re.findall(r"(?m)^#{1,3} .+$", analysis)) < 3:
        errors.append("analysis: fewer than three substantive headings")
    if "<!--" in analysis or re.search(r"\b(?:TODO|FIXME|pending)\b", analysis, re.I):
        errors.append("analysis: contains unfinished markup")
    blocks = re.findall(r"(?ms)^\$\$\s*\n(.*?)\n\$\$\s*$", analysis)
    if analysis.count("$$") != 2 * len(blocks):
        errors.append("analysis: unmatched or malformed display math")
    for index, block in enumerate(blocks, 1):
        offset = analysis.find(block)
        nearby = analysis[max(0, offset - 500):offset] + analysis[offset + len(block):offset + len(block) + 500]
        if len(re.sub(r"[^\u4e00-\u9fffA-Za-z]", "", nearby)) < 35:
            errors.append(f"analysis: formula {index} lacks nearby explanatory prose")

    for index, item in enumerate(manifest.get("source_map", []), 1):
        excerpt = item.get("report_excerpt", "")
        if excerpt not in analysis:
            errors.append(f"source_map:{index}: report excerpt absent from analysis")
        source_excerpt = item.get("source_excerpt", "")
        source = loaded.get("paper_source", "")
        normalize = lambda value: re.sub(r"\s+", " ", value).strip()
        if source_excerpt and normalize(source_excerpt) not in normalize(source):
            errors.append(f"source_map:{index}: cited source excerpt absent from locked source")
        for ref in item.get("source_refs", []):
            excerpt_at = analysis.find(excerpt)
            neighborhood = analysis[max(0, excerpt_at - 500):excerpt_at + len(excerpt) + 500] if excerpt_at >= 0 else ""
            if ref not in neighborhood:
                errors.append(f"source_map:{index}: source reference {ref!r} absent near claim")

    actual_images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", analysis)
    declared = manifest.get("visuals", [])
    declared_paths = [item.get("path", "") for item in declared]
    if sorted(actual_images) != sorted(declared_paths):
        errors.append("visuals: manifest image paths differ from analysis image links")
    if len(declared_paths) != len(set(declared_paths)):
        errors.append("visuals: duplicate image path")
    analysis_path = root / manifest.get("artifacts", {}).get("analysis", {}).get("path", "analysis.md")
    for item in declared:
        rel = Path(item.get("path", ""))
        if rel.is_absolute() or not (analysis_path.parent / rel).is_file():
            errors.append(f"visuals: missing relative image {rel}")
        if item.get("object_id", "") not in inventory or rel.name not in inventory:
            errors.append(f"visuals: {rel.name} absent from figure inventory")
        if item.get("supports_excerpt", "") not in analysis:
            errors.append(f"visuals: supporting excerpt absent for {rel.name}")

    for label in ("Reviewer and role:", "Reviewed at:", "Source version:",
                  "Report revision and hash:", "## Reading path", "## Findings and disposition", "## Judgment"):
        if label not in review:
            errors.append(f"reading_review: missing {label}")
    if len(re.findall(r"(?m)^\d+\. .+→.+", review)) < 3:
        errors.append("reading_review: fewer than three source-to-report reading checks")
    findings = re.search(r"(?ms)^## Findings and disposition\s*\n(.*?)(?=^## |\Z)", review)
    if not findings or len(findings.group(1).strip()) < 60:
        errors.append("reading_review: concrete finding/disposition or checked passages missing")
    elif re.search(r"(?im)^\|[^\n]*\|\s*open\s*\|\s*$", findings.group(1)):
        errors.append("reading_review: unresolved open finding")
    judgment = re.search(r"(?ms)^## Judgment\s*\n(.*?)(?=^## |\Z)", review)
    if not judgment or len(judgment.group(1).strip()) < 60:
        errors.append("reading_review: reasoned judgment missing")
    verdict = re.search(r"(?im)^Reading verdict:\s*(ready|revise)\s*[-—]\s*(.{20,})$", review)
    if not verdict or verdict.group(1).lower() != "ready":
        errors.append("reading_review: explicit ready verdict with reason missing")
    for value in (revision.get("id", ""), manifest.get("paper", {}).get("source_version", ""),
                  manifest.get("artifacts", {}).get("analysis", {}).get("sha256", "")):
        if value and value not in review:
            errors.append(f"reading_review: revision/source/hash not bound: {value}")
    if re.search(r"<[^>]+>|\bTODO\b|\bFIXME\b", review):
        errors.append("reading_review: placeholder remains")

    if canonical_paper is not None:
        if not canonical_paper.is_file():
            errors.append("canonical: Paper does not exist")
        elif canonical_paper.read_text(encoding="utf-8") != analysis:
            errors.append("canonical: Paper text differs from audited analysis")

    return {
        "schema_version": manifest.get("schema_version"),
        "validator": "paper-deep-review/scripts/validate_narrative.py",
        "status": "passed" if not errors else "failed",
        "scope": "deterministic structure and traceability; no automated readability judgment",
        "qualitative_reading": "recorded-not-machine-scored" if review and not any(e.startswith("reading_review:") for e in errors) else "unverified",
        "checked_claims": len(manifest.get("source_map", [])),
        "checked_visuals": len(declared),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--canonical-paper", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    schema = args.schema or Path(__file__).resolve().parents[1] / "references/deliverable-schema.json"
    result = check(args.manifest.resolve(), schema.resolve(), args.canonical_paper)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
