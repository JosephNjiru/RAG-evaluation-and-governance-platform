from scripts.generate_publication_figures import generate_publication_figures


def test_publication_figure_generation_runs() -> None:
    outputs = generate_publication_figures()
    assert outputs
    assert any(path.name == "figure_05_factual_vs_multihop.png" for path in outputs)
