#!/usr/bin/env python3
"""Create an isolated AI systems knowledge workspace from bundled templates."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "assets" / "templates"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="stable kebab-case topic slug")
    parser.add_argument(
        "--process-root",
        type=Path,
        default=Path("_artifacts"),
        help="process-artifact root (default: ./_artifacts)",
    )
    return parser


def initialize(slug: str, process_root: Path) -> Path:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug must be lowercase kebab-case")

    workspace = process_root / f"ai_systems_knowledge_{slug}"
    if workspace.exists():
        raise FileExistsError(f"refusing to overwrite existing workspace: {workspace}")

    (workspace / "methods").mkdir(parents=True)
    (workspace / "frameworks").mkdir()
    for source, target in (
        ("synthesis.md", "synthesis.md"),
        ("crosswalk.md", "crosswalk.md"),
        ("glossary.md", "glossary.md"),
    ):
        shutil.copyfile(TEMPLATES / source, workspace / target)

    (workspace / "implementation-traces.jsonl").write_text("", encoding="utf-8")
    (workspace / "sources.jsonl").write_text("", encoding="utf-8")
    (workspace / "execution_checklist.md").write_text(
        """# Execution Checklist

Allowed states: `pending`, `done`, `blocked`, `skipped-with-reason`.

- [pending] Phase 1: scope and canonical reuse check
- [pending] Phase 2: evidence registration
- [pending] Phase 3: method modeling and tensor walkthroughs
- [pending] Phase 4: pinned framework implementation traces
- [pending] Phase 5: cross-framework synthesis
- [pending] Phase 6: machine validation
- [pending] Human readability rubric
- [pending] Publication decision and publisher validation when applicable
""",
        encoding="utf-8",
    )
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    manifest = {
        "schema_version": 1,
        "slug": slug,
        "revision": "initial",
        "generated_at": now,
        "files": {},
        "validation": {"status": "draft", "validated_at": None},
    }
    (workspace / "knowledge-package.json").write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
    )
    (workspace / "validation.json").write_text(
        json.dumps(
            {"status": "not-run", "errors": [], "warnings": [], "validated_at": None},
            ensure_ascii=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return workspace


def main() -> int:
    args = build_parser().parse_args()
    try:
        workspace = initialize(args.slug, args.process_root)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}")
        return 2
    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
