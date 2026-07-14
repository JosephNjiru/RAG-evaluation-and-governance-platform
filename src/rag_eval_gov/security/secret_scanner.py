"""Lightweight local secret scanner."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "api_key_assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|credential)\s*=\s*['\"][^'\"]{8,}['\"]"
    ),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[a-z0-9._\-]{16,}"),
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "phone_number": re.compile(r"\b(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})\b"),
}
IGNORED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "data/index"}
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".toml",
    ".csv",
    ".json",
    ".jsonl",
    ".example",
}


@dataclass(frozen=True)
class SecretFinding:
    """One scanner finding."""

    path: str
    finding_type: str
    line_number: int
    excerpt: str


def scan_text_for_secrets(text: str, path: str = "<memory>") -> list[SecretFinding]:
    """Scan text and return likely secret or sensitive-data findings."""

    findings: list[SecretFinding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for finding_type, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append(
                    SecretFinding(
                        path=path,
                        finding_type=finding_type,
                        line_number=line_number,
                        excerpt=_redact(line),
                    )
                )
    return findings


def scan_paths_for_secrets(root: Path, include_outputs: bool = True) -> list[SecretFinding]:
    """Scan public text-like files for likely secrets."""

    findings: list[SecretFinding] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if not include_outputs and relative.parts and relative.parts[0] == "outputs":
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            ".env",
            ".env.example",
            "Dockerfile",
        }:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        findings.extend(scan_text_for_secrets(text, str(relative)))
    return findings


def _redact(text: str) -> str:
    if len(text) <= 18:
        return "[redacted]"
    return f"{text[:8]}...[redacted]...{text[-4:]}"
