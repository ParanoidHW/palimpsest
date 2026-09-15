#!/usr/bin/env python3
"""Mutation tests for paper-deep-review global-completeness gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_validator(validator: Path, manifest: Path, canonical: Path) -> dict:
    process = subprocess.run(
        [str(validator), str(manifest), "--canonical-paper", str(canonical)],
        check=False,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


def refresh_hash(manifest_path: Path, artifact: str) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    relative = manifest["artifacts"][artifact]["path"]
    manifest["artifacts"][artifact]["sha256"] = sha256(manifest_path.parent / relative)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def expect_failure(result: dict, fragment: str, case: str) -> None:
    errors = result.get("errors", [])
    if result.get("status") != "failed" or not any(fragment in item for item in errors):
        raise AssertionError(f"{case}: expected {fragment!r}, got {errors}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("canonical", type=Path)
    args = parser.parse_args()

    manifest = args.manifest.resolve()
    canonical = args.canonical.resolve()
    validator = Path(__file__).resolve().parents[1] / "scripts/validate_deliverable.py"

    baseline = run_validator(validator, manifest, canonical)
    if baseline.get("status") != "passed":
        raise AssertionError(f"baseline fixture must pass: {baseline.get('errors')}")

    cases: list[str] = []
    with tempfile.TemporaryDirectory(prefix="paper-review-strict-") as temp:
        temp_root = Path(temp)

        def fresh(name: str) -> tuple[Path, Path]:
            case_root = temp_root / name
            shutil.copytree(manifest.parent, case_root / "review")
            shutil.copy2(canonical, case_root / "canonical.md")
            return case_root / "review/deliverable_manifest.json", case_root / "canonical.md"

        case_manifest, case_canonical = fresh("short-checklist")
        checklist = case_manifest.parent / "review_checklist.md"
        checklist.write_text("# Review checklist\n\n- [done] W1 Folder: exists.\n", encoding="utf-8")
        refresh_hash(case_manifest, "review_checklist")
        expect_failure(run_validator(validator, case_manifest, case_canonical), "checklist item sequence", "short-checklist")
        cases.append("short-checklist")

        case_manifest, case_canonical = fresh("missing-section")
        analysis = case_manifest.parent / "analysis.md"
        analysis.write_text(
            analysis.read_text(encoding="utf-8").replace("## 8. Infra 需求分析", "## 8. Infrastructure"),
            encoding="utf-8",
        )
        refresh_hash(case_manifest, "analysis")
        expect_failure(run_validator(validator, case_manifest, case_canonical), "required heading", "missing-section")
        cases.append("missing-section")

        case_manifest, case_canonical = fresh("underreported-formula")
        data = json.loads(case_manifest.read_text(encoding="utf-8"))
        data["explanation_quality"]["formula_explanations"]["entries"].pop()
        case_manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        expect_failure(run_validator(validator, case_manifest, case_canonical), "manifest formula entries", "underreported-formula")
        cases.append("underreported-formula")

        case_manifest, case_canonical = fresh("incomplete-formula-card")
        analysis = case_manifest.parent / "analysis.md"
        analysis.write_text(
            analysis.read_text(encoding="utf-8").replace("**怎么读？**", "**阅读。**", 1),
            encoding="utf-8",
        )
        refresh_hash(case_manifest, "analysis")
        expect_failure(run_validator(validator, case_manifest, case_canonical), "formula-card label", "incomplete-formula-card")
        cases.append("incomplete-formula-card")

        case_manifest, case_canonical = fresh("orphan-image-reference")
        image = next(
            path for path in (case_manifest.parent / "figures").rglob("*.png")
            if path.name != "contact-sheet.png"
        )
        image.unlink()
        expect_failure(run_validator(validator, case_manifest, case_canonical), "process PNG set differ", "orphan-image-reference")
        cases.append("orphan-image-reference")

        case_manifest, case_canonical = fresh("inventory-only-image")
        inventory = case_manifest.parent / "figure_inventory.md"
        inventory.write_text(inventory.read_text(encoding="utf-8") + "\n`unused-evidence.png`\n", encoding="utf-8")
        refresh_hash(case_manifest, "figure_inventory")
        expect_failure(run_validator(validator, case_manifest, case_canonical), "inventory PNG set", "inventory-only-image")
        cases.append("inventory-only-image")

        case_manifest, case_canonical = fresh("canonical-drift")
        case_canonical.write_text(
            case_canonical.read_text(encoding="utf-8").replace("## 9. 开源代码对照", "## 9. Code"),
            encoding="utf-8",
        )
        expect_failure(run_validator(validator, case_manifest, case_canonical), "canonical Paper does not contain", "canonical-drift")
        cases.append("canonical-drift")

    print(json.dumps({"status": "passed", "negative_cases": cases}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
