from pathlib import Path

from scripts.build_evaluation_dashboard import build_evaluation_dashboard

ROOT = Path(__file__).resolve().parents[1]


def test_stage3_dashboard_is_generated() -> None:
    dashboard_path = build_evaluation_dashboard(ROOT)
    html = dashboard_path.read_text(encoding="utf-8")
    assert "RAG evaluation dashboard" in html
    assert "Question-type breakdown" in html
    assert "Human review queue" in html
