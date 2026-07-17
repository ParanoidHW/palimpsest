from pathlib import Path
import re
import subprocess
import sys


ROOT = Path("02_model_systems/ICML/2026")
DOCS = list(ROOT.rglob("*.md"))
ASSETS = [path for path in (ROOT / "assets").rglob("*") if path.is_file()]
ERRORS = []
HEADING_CACHE = {}


def anchors(path):
    if path not in HEADING_CACHE:
        seen = {}
        values = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
            if not match:
                continue
            text = re.sub(r"<[^>]+>", "", match.group(1)).strip().lower()
            slug = re.sub(r"[^\w\- \u4e00-\u9fff]", "", text, flags=re.UNICODE)
            slug = re.sub(r"\s+", "-", slug)
            duplicate = seen.get(slug, 0)
            seen[slug] = duplicate + 1
            values.add(slug if duplicate == 0 else f"{slug}-{duplicate}")
        HEADING_CACHE[path] = values
    return HEADING_CACHE[path]


link_pattern = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
for doc in DOCS:
    content = doc.read_text(encoding="utf-8")
    for banned in (
        "_artifacts",
        "/mnt/d/",
        "file://",
        "page_png",
        "figures/crops",
        "contact-sheet",
    ):
        if banned in content:
            ERRORS.append(f"forbidden {banned}: {doc}")

    for raw_target in link_pattern.findall(content):
        target = raw_target.strip().split()[0].strip("<>")
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("#"):
            if target[1:] not in anchors(doc):
                ERRORS.append(f"bad anchor {doc}: {target}")
            continue
        path_part, _, anchor = target.partition("#")
        resolved = (doc.parent / path_part).resolve()
        if not resolved.exists():
            ERRORS.append(f"missing target {doc}: {target}")
        elif anchor and resolved.suffix.lower() == ".md" and anchor not in anchors(resolved):
            ERRORS.append(f"bad target anchor {doc}: {target}")

all_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)
for asset in ASSETS:
    candidates = (asset.name, asset.relative_to(ROOT).as_posix())
    if not any(candidate in all_text for candidate in candidates):
        ERRORS.append(f"orphan asset: {asset}")

papers = list((ROOT / "papers").glob("*.md"))
for paper in papers:
    content = paper.read_text(encoding="utf-8")
    if "../README.md" not in content or "../surveys/icml-2026-selected-papers.md" not in content:
        ERRORS.append(f"missing backlinks: {paper}")

tracked = set(subprocess.check_output(["git", "ls-files"], text=True).splitlines())
for path in DOCS + ASSETS:
    if path.as_posix() not in tracked:
        ERRORS.append(f"untracked formal file: {path}")

if ERRORS:
    print("\n".join(ERRORS))
    sys.exit(1)

print(
    f"FORMAL_VALIDATION_PASS docs={len(DOCS)} "
    f"assets={len(ASSETS)} papers={len(papers)}"
)
