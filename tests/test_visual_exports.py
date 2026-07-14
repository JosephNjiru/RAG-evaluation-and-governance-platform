from pathlib import Path


def test_key_visual_exports_exist_when_generated() -> None:
    required = [
        Path("figures/export/journal/figure_01_system_architecture.svg"),
        Path("figures/export/journal/figure_04_baseline_comparison.pdf"),
        Path("figures/export/slides/slide_results_summary.png"),
        Path("figures/export/web/visual_abstract_landscape.png"),
    ]
    missing = [path for path in required if not path.exists()]
    assert missing == []

    stale_text = "44 tests passed"
    text_files = [
        Path("README.md"),
        Path("docs/research-audit-trail.md"),
        Path("scripts/generate_slide_figures.py"),
    ]
    offenders = [
        path
        for path in text_files
        if path.exists() and stale_text in path.read_text(encoding="utf-8")
    ]
    assert offenders == []
