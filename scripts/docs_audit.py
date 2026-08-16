"""Validate AiBoi Markdown metadata, links, and AI-index hygiene."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RAW_SOURCE = DOCS / "00-master" / "source-original-agrofence-v1.2.md"
REQUIRED = (
    "title",
    "type",
    "status",
    "owner",
    "canonical",
    "ai_index",
    "last_verified",
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"')
    return metadata, text[end + 5 :]


def audit() -> list[str]:
    errors: list[str] = []
    indexed_bodies: defaultdict[str, list[Path]] = defaultdict(list)

    for path in sorted(DOCS.rglob("*.md")):
        if path == RAW_SOURCE:
            continue
        text = path.read_text(encoding="utf-8-sig")
        metadata, body = parse_front_matter(text)
        relative = path.relative_to(ROOT)

        missing = [field for field in REQUIRED if not metadata.get(field)]
        if missing:
            errors.append(f"{relative}: missing metadata: {', '.join(missing)}")
            continue

        indexed = metadata["ai_index"].lower() == "true"
        if indexed and metadata["canonical"].lower() != "true":
            errors.append(f"{relative}: non-canonical document cannot be AI-indexed")
        if indexed and "data:image/" in body:
            errors.append(f"{relative}: embedded image data is forbidden in AI-indexed content")
        if indexed and "Definir o tratamento de **" in body:
            errors.append(f"{relative}: generic generated content cannot be AI-indexed")
        if indexed and len(body.split()) > 3000:
            errors.append(f"{relative}: AI-indexed page exceeds 3000 words")

        for target in LINK_RE.findall(body):
            clean_target = target.split("#", 1)[0]
            if not clean_target or re.match(r"^(https?:|mailto:)", clean_target):
                continue
            resolved = (path.parent / clean_target).resolve()
            if not resolved.exists():
                errors.append(f"{relative}: broken link: {target}")

        if indexed:
            normalized = re.sub(r"\s+", " ", body).strip().lower()
            indexed_bodies[normalized].append(relative)

    for duplicates in indexed_bodies.values():
        if len(duplicates) > 1:
            joined = ", ".join(str(path) for path in duplicates)
            errors.append(f"duplicate AI-indexed content: {joined}")

    llms = ROOT / "llms.txt"
    if not llms.exists():
        errors.append("llms.txt: missing AI entry point")
    else:
        for target in LINK_RE.findall(llms.read_text(encoding="utf-8-sig")):
            clean_target = target.split("#", 1)[0]
            if clean_target and not (ROOT / clean_target).exists():
                errors.append(f"llms.txt: broken link: {target}")

    return errors


if __name__ == "__main__":
    failures = audit()
    if failures:
        print("Documentation audit failed:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("Documentation audit passed.")
