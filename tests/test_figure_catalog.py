from scripts.generate_figure_catalog import generate_figure_catalog


def test_figure_catalog_lists_required_figures() -> None:
    path = generate_figure_catalog()
    text = path.read_text(encoding="utf-8")
    assert "Figure 1" in text
    assert "Figure 16" in text
    assert "Visual abstract" in text
