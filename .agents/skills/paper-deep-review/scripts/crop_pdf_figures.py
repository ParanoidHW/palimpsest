#!/usr/bin/env python3
"""Batch crop paper figures from rendered page PNGs and create a contact sheet.

Crop spec JSON example:
{
  "page_dir": "figures/page_png",
  "crop_dir": "figures/crops",
  "crops": [
    {"name": "fig1_architecture.png", "page": 5, "box": [135, 145, 1075, 985]},
    {"name": "table1_main_results.png", "page": "page_11.png", "box": [100, 85, 1120, 615]}
  ]
}

Coordinates are pixel coordinates in the rendered page PNG: [left, top, right, bottom].
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def page_filename(page: int | str) -> str:
    if isinstance(page, int):
        return f"page_{page:02d}.png"
    if page.isdigit():
        return f"page_{int(page):02d}.png"
    return page


def crop_from_spec(spec_path: Path) -> list[Path]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base_dir = spec_path.parent
    page_dir = (base_dir / spec.get("page_dir", "figures/page_png")).resolve()
    crop_dir = (base_dir / spec.get("crop_dir", "figures/crops")).resolve()
    crop_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    for item in spec["crops"]:
        name = item["name"]
        page_path = page_dir / page_filename(item["page"])
        if not page_path.exists():
            raise FileNotFoundError(page_path)
        box = tuple(int(x) for x in item["box"])
        if len(box) != 4:
            raise ValueError(f"{name}: box must be [left, top, right, bottom]")
        image = Image.open(page_path)
        crop = image.crop(box)
        out_path = crop_dir / name
        crop.save(out_path)
        outputs.append(out_path)
        print(f"{out_path} {crop.size}")
    return outputs


def make_contact_sheet(image_paths: list[Path], out_path: Path, thumb_size=(560, 360)) -> None:
    if not image_paths:
        return
    cells: list[Image.Image] = []
    cell_w, cell_h = 600, 430
    for path in image_paths:
        image = Image.open(path).convert("RGB")
        original_size = image.size
        image.thumbnail(thumb_size)
        canvas = Image.new("RGB", (cell_w, cell_h), "white")
        canvas.paste(image, ((cell_w - image.width) // 2, 20))
        draw = ImageDraw.Draw(canvas)
        draw.text((12, cell_h - 30), f"{path.name} {original_size}", fill="black")
        cells.append(canvas)

    cols = 2
    rows = (len(cells) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    for idx, cell in enumerate(cells):
        sheet.paste(cell, ((idx % cols) * cell_w, (idx // cols) * cell_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)
    print(f"contact_sheet {out_path} {sheet.size}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path, help="JSON crop spec")
    parser.add_argument("--sheet", type=Path, default=None, help="Optional contact sheet output")
    args = parser.parse_args()

    outputs = crop_from_spec(args.spec.resolve())
    if args.sheet is not None:
        make_contact_sheet(outputs, args.sheet.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
