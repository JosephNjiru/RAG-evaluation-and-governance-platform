"""Check local Markdown links for missing files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def markdown_files(root: Path) -> list[Path]:
    """Return Markdown files outside local dependency and cache folders."""

    ignored_parts = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
    return [
        path
        for path in root.rglob("*.md")
        if not ignored_parts.intersection(path.relative_to(root).parts)
    ]


def check_markdown_links(root: Path = ROOT) -> list[str]:
    """Return local Markdown links that do not resolve."""

    failures: list[str] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if (
                target.startswith(("http://", "https://", "mailto:"))
                or target.startswith("#")
                or target == ""
            ):
                continue
            target_path = target.split("#", 1)[0]
            if target_path == "":
                continue
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                failures.append(f"{path.relative_to(root)} links outside repo: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{path.relative_to(root)} has missing link: {target}")
    return failures


def main() -> None:
    failures = check_markdown_links()
    if failures:
        print("Markdown link check failed.")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Markdown link check passed.")


if __name__ == "__main__":
    main()
