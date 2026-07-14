from pathlib import Path

import pandas as pd

from scripts.evaluate_rag_outputs import evaluate_rag_outputs

ROOT = Path(__file__).resolve().parents[1]


def test_stage3_evaluation_pipeline_generates_outputs() -> None:
    summary = evaluate_rag_outputs(ROOT)
    results_path = ROOT / "outputs/evaluation/rag_evaluation_results.parquet"
    summary_path = ROOT / "outputs/evaluation/rag_evaluation_summary.csv"
    assert summary["questions"] == 60
    assert results_path.exists()
    assert summary_path.exists()
    results = pd.read_parquet(results_path)
    summary_rows = pd.read_csv(summary_path)
    assert len(results) == 60
    assert "rubric_scores" in results.columns
    factual = summary_rows[summary_rows["question_type"] == "factual"].iloc[0]
    adversarial = summary_rows[summary_rows["question_type"] == "adversarial"].iloc[0]
    assert factual["refusal_correct_rate"] == 1.0
    assert pd.isna(adversarial["retrieval_hit_rate"])
