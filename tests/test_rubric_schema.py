from pathlib import Path

from rag_eval_gov.evaluation.rubrics import load_rubrics

ROOT = Path(__file__).resolve().parents[1]


def test_required_rubrics_are_present() -> None:
    config = load_rubrics(ROOT / "configs/evaluation_rubrics.yaml")
    dimensions = {rubric.dimension for rubric in config.rubrics}
    assert "answer faithfulness" in dimensions
    assert "human review need" in dimensions
    assert len(dimensions) == 10
