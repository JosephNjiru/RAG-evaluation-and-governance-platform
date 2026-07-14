from pathlib import Path

import pandas as pd


def test_retrieval_ablation_outputs_have_required_baselines() -> None:
    path = Path("outputs/evaluation/retrieval_ablation_by_question_type.csv")
    if not path.exists():
        return
    summary = pd.read_csv(path)
    assert {
        "baseline_a_tfidf",
        "baseline_b_metadata_weighted_tfidf",
        "baseline_c_bm25",
        "baseline_d_hybrid",
        "baseline_e_decomposition_diversified",
    }.issubset(set(summary["retrieval_method"]))
