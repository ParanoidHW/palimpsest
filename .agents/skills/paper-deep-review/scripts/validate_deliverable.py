#!/usr/bin/env python3
"""Validate one paper-deep-review manifest and deterministic local invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import jsonschema


def sha256_path(path: Path) -> str:
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    if path.is_dir():
        digest = hashlib.sha256()
        for child in sorted(item for item in path.rglob("*") if item.is_file()):
            relative = child.relative_to(path).as_posix().encode()
            digest.update(relative)
            digest.update(b"\0")
            digest.update(hashlib.sha256(child.read_bytes()).hexdigest().encode())
            digest.update(b"\0")
        return digest.hexdigest()
    raise FileNotFoundError(path)


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest.resolve()
    skill_root = Path(__file__).resolve().parent.parent
    schema_path = (args.schema or skill_root / "references/deliverable-schema.json").resolve()
    root = manifest_path.parent
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "$"
        errors.append(f"schema:{location}: {error.message}")

    artifacts = manifest.get("artifacts", {})
    for name, artifact in artifacts.items():
        if not isinstance(artifact, dict) or artifact.get("status") != "present":
            continue
        relative = Path(artifact["path"])
        add(errors, not relative.is_absolute() and ".." not in relative.parts,
            f"artifact:{name}: path must stay inside the review folder")
        target = root / relative
        if not target.exists():
            errors.append(f"artifact:{name}: missing {relative.as_posix()}")
            continue
        actual = sha256_path(target)
        add(errors, actual == artifact.get("sha256"),
            f"artifact:{name}: sha256 mismatch for {relative.as_posix()}")

    analysis_path = root / "analysis.md"
    analysis = analysis_path.read_text(encoding="utf-8") if analysis_path.exists() else ""
    add(errors, bool(analysis), "analysis.md is missing or empty")

    authorship = manifest.get("paper", {}).get("authorship_and_affiliations", {})
    institutional_authors = authorship.get("institutional_authors", [])
    ordered_authors = authorship.get("ordered_authors", [])
    first_authors = authorship.get("first_authors", [])
    corresponding_authors = authorship.get("corresponding_authors", [])
    mapped_people = first_authors + corresponding_authors
    if authorship.get("author_identity_status") == "verified":
        first_names = [entry.get("name") for entry in first_authors]
        add(errors, bool(ordered_authors), "authorship: verified identity requires ordered authors")
        add(errors, bool(first_names), "authorship: verified identity requires first-author mapping")
        if ordered_authors:
            add(errors, ordered_authors[0] in first_names,
                "authorship: first listed author is absent from first-author mappings")
        for entry in mapped_people:
            add(errors, entry.get("name") in ordered_authors,
                f"authorship: mapped author {entry.get('name')!r} absent from ordered author list")
    if authorship.get("author_identity_status") == "institutional":
        add(errors, bool(institutional_authors),
            "authorship: institution-authored work requires institutional authors")
        add(errors, not ordered_authors and not mapped_people,
            "authorship: institution-authored work must not contain personal-author mappings")
        add(errors, authorship.get("corresponding_author_designation_status") == "not-applicable",
            "authorship: institution-authored work must mark correspondence not applicable")
        add(errors, not authorship.get("other_author_affiliations", []),
            "authorship: institution-authored work must not use remaining-person affiliations")
    if authorship.get("corresponding_author_designation_status") == "verified":
        add(errors, bool(corresponding_authors),
            "authorship: verified corresponding-author designation requires a mapping")
    for entry in mapped_people:
        name = entry.get("name", "")
        add(errors, name in analysis,
            f"authorship: mapped author {name!r} not found in analysis.md")
        add(errors, entry.get("role_basis", "") in analysis,
            f"authorship: role basis for {name!r} not found in analysis.md")
        for affiliation in entry.get("affiliations", []):
            add(errors, affiliation in analysis,
                f"authorship: affiliation {affiliation!r} for {name!r} not found in analysis.md")
        for evidence in entry.get("evidence", []):
            add(errors, evidence in analysis,
                f"authorship: evidence {evidence!r} for {name!r} not found in analysis.md")
    for affiliation in authorship.get("other_author_affiliations", []):
        add(errors, affiliation in analysis,
            f"authorship: remaining-author affiliation {affiliation!r} not found in analysis.md")
    for institution in institutional_authors:
        add(errors, institution in analysis,
            f"authorship: institutional author {institution!r} not found in analysis.md")
    for evidence in authorship.get("evidence", []):
        add(errors, evidence in analysis,
            f"authorship: global evidence {evidence!r} not found in analysis.md")

    for group_name in ("revision_info", "terminology_and_symbols"):
        group = manifest.get(group_name, {})
        heading = group.get("section_heading", "")
        add(errors, heading in analysis, f"{group_name}: section heading not found in analysis.md")

    quality = manifest.get("explanation_quality", {})
    formula_group = quality.get("formula_explanations", {})
    formulas = formula_group.get("entries", [])
    formula_ids = [entry.get("formula_id") for entry in formulas]
    add(errors, len(formula_ids) == len(set(formula_ids)),
        "explanation_quality: duplicate formula_id")
    known_symbols = {
        entry.get("symbol")
        for entry in manifest.get("terminology_and_symbols", {}).get("symbols", [])
    }
    for entry in formulas:
        add(errors, entry.get("purpose", "") in analysis,
            f"formula:{entry.get('formula_id')}: purpose text not found in analysis.md")
        for variable in entry.get("variable_roles", []):
            add(errors, variable.get("symbol") in known_symbols,
                f"formula:{entry.get('formula_id')}: symbol {variable.get('symbol')!r} absent from symbol table")

    jargon = quality.get("jargon_audit", {})
    add(errors, not jargon.get("unexplained_terms"),
        "jargon_audit: unexplained_terms must be empty")
    known_terms = {
        entry.get("term")
        for entry in manifest.get("terminology_and_symbols", {}).get("terms", [])
    }
    for entry in jargon.get("retained_terms", []):
        add(errors, entry.get("term") in known_terms or entry.get("term") in analysis,
            f"jargon_audit: retained term {entry.get('term')!r} is not traceable")

    prior = quality.get("prior_solution_explanation", {})
    heading = prior.get("section_heading", "")
    add(errors, heading in analysis,
        "prior_solution_explanation: section heading not found in analysis.md")
    for index, failure in enumerate(prior.get("failure_modes", []), start=1):
        add(errors, failure.get("concrete_scenario", "") in analysis,
            f"prior_solution_explanation: scenario {index} not found in analysis.md")
        add(errors, failure.get("why_simple_fix_fails", "") in analysis,
            f"prior_solution_explanation: simple-fix explanation {index} not found in analysis.md")

    overview = quality.get("algorithm_overview", {})
    if overview.get("status") == "present":
        relative = Path(overview.get("artifact_path", ""))
        add(errors, not relative.is_absolute() and ".." not in relative.parts,
            "algorithm_overview: artifact path must stay inside the review folder")
        add(errors, (root / relative).is_file(),
            f"algorithm_overview: missing {relative.as_posix()}")
        add(errors, relative.as_posix() in analysis,
            "algorithm_overview: image is not linked from analysis.md")

    visual = manifest.get("visual_evidence", {})
    expected_total = visual.get("mechanism_count", 0) + visual.get("result_or_system_count", 0)
    add(errors, expected_total == visual.get("counted_total"),
        "visual_evidence: counted_total does not equal category sum")

    checklist_artifact = artifacts.get("review_checklist")
    if isinstance(checklist_artifact, dict) and checklist_artifact.get("status") == "present":
        checklist_path = root / checklist_artifact["path"]
        if checklist_path.is_file():
            checklist = checklist_path.read_text(encoding="utf-8")
            add(errors, re.search(r"- \\[pending\\]", checklist) is None,
                "review_checklist.md still contains pending items")

    if manifest.get("completion_status") == "complete":
        checks = manifest.get("semantic_validation", {}).get("checks", {})
        add(errors, all(checks.values()),
            "complete delivery has one or more false semantic_validation checks")

    result = {
        "validator": "paper-deep-review/scripts/validate_deliverable.py",
        "manifest": str(manifest_path),
        "schema": str(schema_path),
        "status": "passed" if not errors else "failed",
        "checked_artifacts": sum(
            1 for value in artifacts.values()
            if isinstance(value, dict) and value.get("status") == "present"
        ),
        "checked_formulas": len(formulas),
        "checked_prior_failure_modes": len(prior.get("failure_modes", [])),
        "errors": errors,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
