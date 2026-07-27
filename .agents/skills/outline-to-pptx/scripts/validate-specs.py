#!/usr/bin/env python3
"""Validate outline-to-pptx style profiles and deck plans."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(instance: dict, schema: dict, label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label}:{location}: {error.message}")
    return errors


def slide_text(slide: dict) -> str:
    chunks = [slide["title"], slide["header"]]
    for message in slide["messages"]:
        chunks.extend(
            value
            for key in ("message", "detail", "annotation")
            if (value := message.get(key))
        )
    for placeholder in slide.get("placeholders", []):
        chunks.append(placeholder["label"])
        chunks.extend(placeholder["fields"])
    visual = slide.get("visual", {})
    chunks.extend(value for key in ("caption", "alt") if (value := visual.get(key)))
    return "\n".join(chunks)


def semantic_checks(style: dict, plan: dict) -> list[str]:
    errors: list[str] = []
    if plan["style_profile"] != style["id"]:
        errors.append(
            f"plan.style_profile={plan['style_profile']!r} does not match style.id={style['id']!r}"
        )

    size_values = list(style["typography"]["sizes_pt"].values())
    if len(set(size_values)) > style["typography"]["max_distinct_sizes_per_slide"]:
        errors.append("style typography defines more distinct sizes than allowed")
    if style["typography"]["sizes_pt"]["body"] < style["typography"]["body_min_pt"]:
        errors.append("style body size is below body_min_pt")
    if style["canvas"]["light_background_required"] and style["canvas"]["dark_slides_allowed"]:
        errors.append("light-background profile cannot enable dark slides")

    sections = {section["id"] for section in plan["sections"]}
    slide_ids: set[str] = set()
    for index, slide in enumerate(plan["slides"], start=1):
        prefix = f"slide[{index}] {slide['id']!r}"
        if slide["id"] in slide_ids:
            errors.append(f"{prefix}: duplicate slide id")
        slide_ids.add(slide["id"])
        if slide["section"] not in sections:
            errors.append(f"{prefix}: unknown section {slide['section']!r}")
        if len(slide["title"]) > style["content"]["max_title_chars"]:
            errors.append(f"{prefix}: title exceeds style max_title_chars")
        if len(slide["messages"]) > style["content"]["max_message_groups_per_slide"]:
            errors.append(f"{prefix}: too many message groups")
        if len(slide["critical_emphasis"]) > style["emphasis"]["max_fragments_per_slide"]:
            errors.append(f"{prefix}: too many critical-emphasis fragments")
        if len(set(slide["font_size_tokens_used"])) > style["typography"]["max_distinct_sizes_per_slide"]:
            errors.append(f"{prefix}: too many font-size tokens")
        content = slide_text(slide)
        for phrase in slide["critical_emphasis"]:
            if phrase not in content:
                errors.append(f"{prefix}: emphasized phrase {phrase!r} is not present in slide content")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--style-schema", type=Path)
    parser.add_argument("--plan-schema", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    reference_dir = script_dir.parent / "references"
    style_schema_path = args.style_schema or reference_dir / "style-profile.schema.json"
    plan_schema_path = args.plan_schema or reference_dir / "deck-plan.schema.json"

    style = load_json(args.style)
    plan = load_json(args.plan)
    errors = []
    errors.extend(validate_schema(style, load_json(style_schema_path), "style"))
    errors.extend(validate_schema(plan, load_json(plan_schema_path), "plan"))
    if not errors:
        errors.extend(semantic_checks(style, plan))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": "passed",
                "style": style["id"],
                "slides": len(plan["slides"]),
                "max_message_groups_per_slide": style["content"]["max_message_groups_per_slide"],
                "max_distinct_sizes_per_slide": style["typography"]["max_distinct_sizes_per_slide"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
