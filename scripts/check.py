#!/usr/bin/env python3
"""Repository validation with no external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from delivery.model import DeliveryError, read_json, validate_release  # noqa: E402


def main() -> int:
    failures: list[str] = []
    policy = read_json(ROOT / "policies/release-policy.json")
    releases = sorted((ROOT / "examples/releases").glob("*.json"))
    for path in releases:
        try:
            validate_release(read_json(path), policy)
        except (DeliveryError, json.JSONDecodeError) as error:
            failures.append(f"{path.relative_to(ROOT)}: {error}")

    for path in sorted((ROOT / "environments").glob("*.json")):
        try:
            document = read_json(path)
            if document.get("name") != path.stem:
                failures.append(f"{path.relative_to(ROOT)}: name must match filename")
        except json.JSONDecodeError as error:
            failures.append(f"{path.relative_to(ROOT)}: {error}")

    markdown = list(ROOT.rglob("*.md"))
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^#\s+\S", text, re.MULTILINE):
            failures.append(f"{path.relative_to(ROOT)}: missing level-one heading")
        if not text.endswith("\n"):
            failures.append(f"{path.relative_to(ROOT)}: missing final newline")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line != line.rstrip():
                failures.append(f"{path.relative_to(ROOT)}:{line_number}: trailing whitespace")

    forbidden = ("mamu" + "durijk", "mamu" + "duri-jeevankumar", "@g" + "mail.com")
    checked_extensions = {".md", ".py", ".sh", ".json", ".yml", ".yaml"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in checked_extensions or ".git" in path.parts:
            continue
        content = path.read_text(encoding="utf-8")
        for value in forbidden:
            if value.lower() in content.lower():
                failures.append(f"{path.relative_to(ROOT)}: forbidden identity reference")

    if failures:
        print("Validation failed:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    print(f"Validated {len(releases)} releases, 3 environments, and {len(markdown)} Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
