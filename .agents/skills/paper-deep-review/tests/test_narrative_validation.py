#!/usr/bin/env python3
"""Small behavioral checks for the v1.8 traceability validator."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_deliverable.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(manifest: Path) -> dict:
    proc = subprocess.run(["python3", str(VALIDATOR), str(manifest)], capture_output=True, text=True)
    return json.loads(proc.stdout)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="narrative-review-") as temp:
        root = Path(temp)
        (root / "fig.png").write_bytes(b"fake figure content")
        claim = "The extra verification path raises accepted tokens under this load."
        support = "The measured gain uses the same target and a tuned baseline."
        analysis = (
            "---\ntags:\n  - paper\n  - collection/test\n  - domain/test\n  - status/deep-review\n  - topic/test\n  - method/test\n---\n\n"
            "# Why this system slows down\n\nReview revision rev-test-1, version 1.0.0. Author Ada Example is first author at Example University (paper title block).\n\n"
            "The old path rereads model weights for a short accepted prefix. (§1)\n\n"
            "## Following a different path\n\n" + claim + " (§3, Figure 1)\n\n"
            "$$\nS=\\tau/c\n$$\n\nThe equation divides accepted tokens by relative step cost.\n\n"
            "![Figure 1](fig.png)\n\n" + support + "\n\n"
            "## Reading the result\n\nThe reported speedup compares the tested system with stock. (§5, Table 1)\n"
        )
        (root / "analysis.md").write_text(analysis)
        (root / "paper.txt").write_text(
            "Paper text, §1: The old path rereads model weights for only a short accepted prefix. "
            "§3, Figure 1: More verification paths can raise the number of accepted tokens. "
            "§5, Table 1: We compare the tested system against a tuned stock baseline.\n"
        )
        (root / "inventory.md").write_text("Figure 1 | fig.png | caption and QA checked\n")
        rev = "rev-test-1"
        review = (
            "# Narrative review\n\n"
            "- Reviewer and role: Reader, independent reviewer\n"
            "- Reviewed at: 2026-11-18T12:00:00+08:00\n"
            "- Source version: v1\n"
            f"- Report revision and hash: {rev}; {sha(root / 'analysis.md')}\n\n"
            "## Reading path\n\n"
            "1. problem → §1: repeated weights explain initial cost.\n"
            "2. mechanism → §3: more paths raise accepted tokens.\n"
            "3. result → §5: stock is the gain denominator.\n\n"
            "## Findings and disposition\n\n"
            "| Location | Finding | Action | Status |\n|---|---|---|---|\n"
            "| result | The reader could identify stock as the comparison denominator and follow the figure to the accepted-token claim | No edit needed after the source cross-check | resolved |\n\n"
            "## Judgment\n\nAn unfamiliar technical reader can retell the causal thread from repeated weight reads through extra verification paths to the measured stock comparison; the equation and figure have nearby interpretations.\n\n"
            "Reading verdict: ready — The tested passages connect the cost, mechanism and stock denominator without an unresolved gap.\n"
        )
        (root / "review.md").write_text(review)
        manifest = {
            "schema_version": "1.8.0", "deliverable_type": "paper-deep-review", "invocation_mode": "delegated",
            "paper": {"paper_key": "test-paper", "title": "Test Paper", "source_version": "v1", "paper_url": "https://example.org/paper", "tags": ["paper", "collection/test", "domain/test", "status/deep-review", "topic/test", "method/test"], "authorship_and_affiliations": {"identity_status": "personal", "ordered_authors": ["Ada Example"], "first_authors": ["Ada Example"], "corresponding_authors": [], "role_affiliations": [{"name": "Ada Example", "role": "first", "affiliations": ["Example University"], "evidence": "paper title block"}], "institutions": ["Example University"], "evidence": "paper title block"}},
            "revision": {"id": rev, "document_version": "1.0.0", "revised_at": "2026-11-18T12:00:00+08:00", "supersedes_manifest_sha256": None},
            "artifacts": {name: {"path": path, "sha256": sha(root / path)} for name, path in {
                "analysis": "analysis.md", "paper_source": "paper.txt", "figure_inventory": "inventory.md", "reading_review": "review.md"
            }.items()},
            "source_map": [
                {"report_excerpt": "The old path rereads model weights for a short accepted prefix.", "source_refs": ["§1"], "source_excerpt": "The old path rereads model weights for only a short accepted prefix.", "evidence_kind": "paper-stated"},
                {"report_excerpt": claim, "source_refs": ["§3", "Figure 1"], "source_excerpt": "More verification paths can raise the number of accepted tokens.", "evidence_kind": "measured"},
                {"report_excerpt": "The reported speedup compares the tested system with stock.", "source_refs": ["§5", "Table 1"], "source_excerpt": "We compare the tested system against a tuned stock baseline.", "evidence_kind": "measured"}
            ],
            "limitations": [], "publication": {"canonical_owner": "test", "canonical_path": "test/papers/test-paper.md", "promotion_plan_path": None},
            "visuals": [{"object_id": "Figure 1", "path": "fig.png", "supports_excerpt": support}]
        }
        path = root / "deliverable_manifest.json"
        path.write_text(json.dumps(manifest, ensure_ascii=False))
        result = run(path)
        assert result["status"] == "passed", result["errors"]
        assert result["qualitative_reading"] == "recorded-not-machine-scored"

        manifest["source_map"][0]["source_excerpt"] = "The source never made this claim about the model at all."
        path.write_text(json.dumps(manifest, ensure_ascii=False))
        result = run(path)
        assert result["status"] == "failed" and any("cited source excerpt absent" in e for e in result["errors"])
        manifest["source_map"][0]["source_excerpt"] = "The old path rereads model weights for only a short accepted prefix."
        path.write_text(json.dumps(manifest, ensure_ascii=False))

        (root / "fig.png").unlink()
        result = run(path)
        assert result["status"] == "failed" and any("missing relative image" in e for e in result["errors"])
        (root / "fig.png").write_bytes(b"fake figure content")

        (root / "review.md").write_text("# Narrative review\n")
        manifest["artifacts"]["reading_review"]["sha256"] = sha(root / "review.md")
        path.write_text(json.dumps(manifest, ensure_ascii=False))
        result = run(path)
        assert result["status"] == "failed" and any("reading_review:" in e for e in result["errors"])
    print("narrative validator positive and negative checks passed")


if __name__ == "__main__":
    main()
