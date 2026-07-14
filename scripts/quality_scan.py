"""Release quality scan for public project files."""

from __future__ import annotations

import re
from pathlib import Path

from rag_eval_gov.security.secret_scanner import scan_paths_for_secrets

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".toml",
    ".txt",
    ".example",
    ".mmd",
    ".dockerignore",
}
TEXT_NAMES = {"Dockerfile", "Makefile", ".gitignore", ".env.example", "docker-compose.yml"}
IGNORED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "htmlcov",
    "dist",
    "build",
    "data/index",
}

GLOBAL_PATTERNS = {
    "private planning language": re.compile(
        r"\b(ChatGPT|Codex conversation|planning chat|Stage [1-4] prompt)\b", re.IGNORECASE
    ),
    "inflated release claim": re.compile(r"production-ready", re.IGNORECASE),
    "unverified AWS deployment claim": re.compile(r"deployed to AWS", re.IGNORECASE),
    "unverified Azure deployment claim": re.compile(r"deployed to Azure", re.IGNORECASE),
    "company or hiring language": re.compile(
        r"\b(job opportunity|client project|future employer|recruiter-facing|hiring manager)\b",
        re.IGNORECASE,
    ),
    "secret-like assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|credential)\s*=\s*['\"][^'\"]{8,}['\"]"
    ),
}
STALE_TEST_RE = re.compile(r"\b(\d+)\s+passed\b", re.IGNORECASE)
EXPECTED_TEST_COUNT = 54


def text_files(root: Path) -> list[Path]:
    """Return public text-like files to scan."""

    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.as_posix() == "scripts/quality_scan.py":
            continue
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
            files.append(path)
    return files


def scan_quality(root: Path = ROOT) -> list[str]:
    """Return quality scan failures."""

    failures: list[str] = []
    for zip_path in root.rglob("*.zip"):
        if not any(part in IGNORED_PARTS for part in zip_path.relative_to(root).parts):
            failures.append(f"zip file should not be present: {zip_path.relative_to(root)}")

    for path in text_files(root):
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8", errors="ignore")
        scan_text = text
        if relative.as_posix() == "portfolio/release_checklist.md":
            scan_text = scan_text.replace("No `production-ready`.", "")
        for label, pattern in GLOBAL_PATTERNS.items():
            if pattern.search(scan_text):
                failures.append(f"{relative}: {label}")

        for match in STALE_TEST_RE.finditer(scan_text):
            count = int(match.group(1))
            if count != EXPECTED_TEST_COUNT:
                failures.append(f"{relative}: stale test-count claim {count} passed")

    failures.extend(_check_required_outputs(root))
    failures.extend(_check_evaluation_leakage(root))
    failures.extend(_check_baseline_preservation(root))
    failures.extend(_check_security_release_gates(root))
    return sorted(set(failures))


def _check_required_outputs(root: Path) -> list[str]:
    required = [
        root / "outputs/reports/reproducibility_manifest.json",
        root / "outputs/reports/challenge_set_report.md",
        root / "outputs/reports/baseline_comparison_report.md",
        root / "outputs/evaluation/run_manifest.csv",
        root / "outputs/reports/security_assurance_report.md",
        root / "governance/security_controls_matrix.md",
    ]
    return [
        f"missing required output: {path.relative_to(root)}"
        for path in required
        if not path.exists()
    ]


def _check_evaluation_leakage(root: Path) -> list[str]:
    failures: list[str] = []
    for folder in [root / "src/rag_eval_gov/retrieval", root / "src/rag_eval_gov/generation"]:
        for path in folder.rglob("*.py"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "evidence_map" in text or "EvidenceMap" in text:
                failures.append(
                    f"{path.relative_to(root)}: evidence map reference outside evaluation"
                )
    return failures


def _check_security_release_gates(root: Path) -> list[str]:
    failures: list[str] = []
    env_path = root / ".env"
    if env_path.exists():
        failures.append(".env file should not be prepared for release")
    api_path = root / "src/rag_eval_gov/api/main.py"
    if api_path.exists():
        api_text = api_path.read_text(encoding="utf-8", errors="ignore")
        if "debug=True" in api_text:
            failures.append("API debug mode is enabled")
        if 'allow_origins=["*"]' in api_text or "allow_origins=['*']" in api_text:
            failures.append("API uses unsafe CORS wildcard")
    output_findings = [
        finding
        for finding in scan_paths_for_secrets(root)
        if finding.path.startswith("outputs/")
        and not finding.path.endswith("security_events.jsonl")
        and not finding.path.endswith("reproducibility_manifest.json")
    ]
    for finding in output_findings[:20]:
        failures.append(
            f"secret-like value in output: {finding.path}:{finding.line_number}:{finding.finding_type}"
        )
    return failures


def _check_baseline_preservation(root: Path) -> list[str]:
    failures: list[str] = []
    readme = root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="ignore")
        if "Baseline A" not in text or "Baseline E" not in text:
            failures.append("README.md: baseline comparison labels are missing")
    report = root / "outputs/reports/baseline_comparison_report.md"
    if report.exists():
        text = report.read_text(encoding="utf-8", errors="ignore")
        if "Baseline A" not in text or "Baseline E" not in text:
            failures.append(
                "baseline comparison report does not preserve Baseline A and Baseline E"
            )
    gitignore = root / ".gitignore"
    if gitignore.exists() and ".venv/" not in gitignore.read_text(
        encoding="utf-8", errors="ignore"
    ):
        failures.append(".gitignore: .venv/ is not ignored")
    return failures


def main() -> None:
    failures = scan_quality()
    if failures:
        print("Quality scan failed.")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Quality scan passed.")


if __name__ == "__main__":
    main()
