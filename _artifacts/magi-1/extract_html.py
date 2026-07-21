from pathlib import Path

from bs4 import BeautifulSoup


html_path = Path("_artifacts/magi-1/paper.html")
soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

for figure in soup.select("figure"):
    caption = figure.find("figcaption")
    image = figure.find("img")
    caption_text = " ".join(caption.get_text(" ", strip=True).split()) if caption else ""
    if caption_text:
        print(
            figure.get("id"),
            image.get("src") if image else "-",
            caption_text,
            sep="\t",
        )
