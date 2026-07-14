from pathlib import Path


def test_baseline_comparison_report_preserves_baseline_a_when_present() -> None:
    path = Path("outputs/reports/baseline_comparison_report.md")
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    assert "Baseline A" in text
    assert "Baseline E" in text
