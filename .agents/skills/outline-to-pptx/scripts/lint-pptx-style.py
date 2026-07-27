#!/usr/bin/env python3
"""Lint a generated PPTX against an outline-to-pptx style profile."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
CJK_RE = re.compile(r"[\u3400-\u9fff]")


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def run_color(run_props: ET.Element) -> str | None:
    node = run_props.find("a:solidFill/a:srgbClr", NS)
    return node.get("val") if node is not None else None


def run_font(run_props: ET.Element, key: str) -> str | None:
    node = run_props.find(f"a:{key}", NS)
    return node.get("typeface") if node is not None else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument(
        "--style",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "references" / "academic-light.style.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    style = json.loads(args.style.read_text(encoding="utf-8"))
    allowed_sizes = set(style["typography"]["sizes_pt"].values())
    max_sizes = style["typography"]["max_distinct_sizes_per_slide"]
    critical = style["palette"]["critical_red"]
    canvas = style["palette"]["canvas"]
    zh_fonts = {style["fonts"]["zh_primary"], *style["fonts"]["fallback"]}
    en_fonts = {style["fonts"]["en_primary"], *style["fonts"]["fallback"]}

    errors: list[str] = []
    warnings: list[str] = []
    slide_reports = []

    with zipfile.ZipFile(args.pptx) as archive:
        slide_names = sorted(
            (
                name
                for name in archive.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            ),
            key=slide_number,
        )
        for slide_name in slide_names:
            number = slide_number(slide_name)
            root = ET.fromstring(archive.read(slide_name))
            sizes: set[int] = set()
            fonts: set[str] = set()

            background = root.find(".//p:bgPr/a:solidFill/a:srgbClr", NS)
            background_color = background.get("val") if background is not None else None
            if style["canvas"]["light_background_required"] and background_color != canvas:
                errors.append(
                    f"slide {number}: background {background_color!r} does not match light canvas {canvas}"
                )

            for run in root.findall(".//a:r", NS):
                text_node = run.find("a:t", NS)
                props = run.find("a:rPr", NS)
                if text_node is None or props is None:
                    continue
                text = text_node.text or ""
                size_raw = props.get("sz")
                if size_raw:
                    size = int(size_raw) // 100
                    sizes.add(size)
                    if size not in allowed_sizes:
                        errors.append(f"slide {number}: text {text!r} uses undeclared size {size} pt")

                latin_font = run_font(props, "latin")
                east_asian_font = run_font(props, "ea")
                if latin_font:
                    fonts.add(latin_font)
                if east_asian_font:
                    fonts.add(east_asian_font)
                if CJK_RE.search(text):
                    effective = east_asian_font or latin_font
                    if effective and effective not in zh_fonts:
                        errors.append(
                            f"slide {number}: Chinese text {text!r} uses {effective!r}, expected {sorted(zh_fonts)}"
                        )
                elif text.strip():
                    effective = latin_font or east_asian_font
                    if effective and effective not in en_fonts:
                        errors.append(
                            f"slide {number}: English text {text!r} uses {effective!r}, expected {sorted(en_fonts)}"
                        )

                color = run_color(props)
                if color == critical and props.get("b") not in {"1", "true"}:
                    errors.append(f"slide {number}: critical-red text {text!r} is not bold")

            if len(sizes) > max_sizes:
                errors.append(f"slide {number}: uses {len(sizes)} font sizes {sorted(sizes)}, maximum is {max_sizes}")
            if not sizes:
                warnings.append(f"slide {number}: no explicit text sizes found")
            slide_reports.append(
                {
                    "slide": number,
                    "background": background_color,
                    "font_sizes_pt": sorted(sizes),
                    "fonts": sorted(fonts),
                }
            )

    report = {
        "status": "failed" if errors else "passed",
        "pptx": str(args.pptx),
        "style": style["id"],
        "slides": slide_reports,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
