#!/usr/bin/env python3
"""Extract text and render page PNGs from a PDF for paper review workflows."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError as exc:
        raise SystemExit(
            "PyMuPDF is required. Install with `python -m pip install PyMuPDF` "
            "or use Poppler (`pdftoppm`/`pdftocairo`) as a fallback."
        ) from exc

    pdf_path = args.pdf.resolve()
    out_dir = args.out_dir.resolve()
    text_dir = out_dir / "extracted_text"
    page_png_dir = out_dir / "figures" / "page_png"
    text_dir.mkdir(parents=True, exist_ok=True)
    page_png_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    metadata = {"page_count": doc.page_count, "metadata": doc.metadata}
    (text_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    full_parts: list[str] = []
    zoom = args.dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    for index, page in enumerate(doc, start=1):
        raw_text = page.get_text("text")
        page_header = f"===== PAGE {index} =====\n\n"
        (text_dir / f"page_{index:02d}.txt").write_text(
            page_header + raw_text,
            encoding="utf-8",
        )
        clean = page_header + clean_text(raw_text)
        (text_dir / f"page_{index:02d}.clean.txt").write_text(clean, encoding="utf-8")
        full_parts.append(clean)

        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(page_png_dir / f"page_{index:02d}.png")

    (text_dir / "full_text.clean.txt").write_text("\n".join(full_parts), encoding="utf-8")
    print(f"Wrote {doc.page_count} pages under {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
