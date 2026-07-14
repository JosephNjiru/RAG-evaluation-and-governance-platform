"""Package the Stage 3 evaluation dashboard for static serving."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_dashboard(root: Path = ROOT) -> Path:
    """Copy the generated Stage 3 dashboard into the dashboard folder."""

    source = root / "outputs/reports/rag_evaluation_dashboard.html"
    if not source.exists():
        from scripts.build_evaluation_dashboard import build_evaluation_dashboard

        build_evaluation_dashboard(root)
    target = root / "dashboard/index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return target


def main() -> None:
    target = build_dashboard()
    print(f"Dashboard packaged: {target}")


if __name__ == "__main__":
    main()
