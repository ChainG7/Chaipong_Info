#!/usr/bin/env python3
"""Validate the knowledge-base metadata and local Markdown links."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID_STATUSES = {"verified", "reviewed", "draft", "archived"}
REQUIRED_METADATA = {
    "document_id",
    "title",
    "category",
    "status",
    "evidence_level",
    "owner",
    "technical_reviewer",
    "last_reviewed",
    "source_url",
    "source_accessed",
}
REQUIRED_COLUMNS = {
    "document_id",
    "slug",
    "english_name",
    "thai_name",
    "category",
    "status",
    "evidence_level",
    "file_path",
    "source_url",
    "source_accessed",
}
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError("unterminated YAML front matter") from exc
    result: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def validate_products(errors: list[str]) -> dict[str, Path]:
    records: dict[str, Path] = {}
    for path in sorted((ROOT / "products").glob("*/*.md")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            meta = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        missing = sorted(REQUIRED_METADATA - meta.keys())
        if missing:
            errors.append(f"{rel}: missing metadata: {', '.join(missing)}")
        status = meta.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{rel}: invalid status {status!r}")
        document_id = meta.get("document_id", "")
        if document_id in records:
            errors.append(f"{rel}: duplicate document_id {document_id}")
        elif document_id:
            records[document_id] = path
        if status == "verified":
            reviewer = meta.get("technical_reviewer", "")
            if not reviewer or reviewer.lower().startswith("pending"):
                errors.append(f"{rel}: verified record requires a named reviewer")
            if meta.get("evidence_level") != "verified":
                errors.append(f"{rel}: verified status requires verified evidence_level")
    return records


def validate_index(records: dict[str, Path], errors: list[str]) -> None:
    index_path = ROOT / "data" / "products.csv"
    with index_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            errors.append(f"data/products.csv: missing columns: {', '.join(missing)}")
        rows = list(reader)
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    for line_number, row in enumerate(rows, start=2):
        document_id = row.get("document_id", "")
        slug = row.get("slug", "")
        if document_id in seen_ids:
            errors.append(f"data/products.csv:{line_number}: duplicate document_id")
        if slug in seen_slugs:
            errors.append(f"data/products.csv:{line_number}: duplicate slug")
        seen_ids.add(document_id)
        seen_slugs.add(slug)
        target = ROOT / row.get("file_path", "")
        if not target.is_file():
            errors.append(f"data/products.csv:{line_number}: missing file {target}")
        elif records.get(document_id) != target:
            errors.append(
                f"data/products.csv:{line_number}: document_id/file mismatch"
            )
    missing_from_index = sorted(set(records) - seen_ids)
    if missing_from_index:
        errors.append(
            "data/products.csv: product records absent from index: "
            + ", ".join(missing_from_index)
        )


def validate_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            decoded = target.replace("%20", " ")
            resolved = (path.parent / decoded).resolve()
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT).as_posix()}: broken link {raw_target}"
                )


def main() -> int:
    errors: list[str] = []
    records = validate_products(errors)
    validate_index(records, errors)
    validate_links(errors)
    if errors:
        print("Content validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Content validation passed: {len(records)} product records and local links checked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
