"""Build the static Stage 3 evaluation dashboard."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag_eval_gov.reports.dashboard import build_dashboard_html
from scripts.evaluate_rag_outputs import evaluate_rag_outputs


def build_evaluation_dashboard(root: Path = ROOT) -> Path:
    results_path = root / "outputs/evaluation/rag_evaluation_results.parquet"
    summary_path = root / "outputs/evaluation/rag_evaluation_summary.csv"
    if not results_path.exists() or not summary_path.exists():
        evaluate_rag_outputs(root)
    results = pd.read_parquet(results_path)
    summary = pd.read_csv(summary_path)
    dashboard_path = root / "outputs/reports/rag_evaluation_dashboard.html"
    dashboard_path.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html = build_dashboard_html(results, summary)
    dashboard_path.write_text(dashboard_html, encoding="utf-8")
    packaged_path = root / "dashboard/index.html"
    packaged_path.parent.mkdir(parents=True, exist_ok=True)
    packaged_path.write_text(dashboard_html, encoding="utf-8")
    return dashboard_path


def main() -> None:
    dashboard_path = build_evaluation_dashboard()
    print(f"Dashboard written: {dashboard_path}")


if __name__ == "__main__":
    main()
