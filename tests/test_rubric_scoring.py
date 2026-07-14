from pathlib import Path

import pandas as pd

from rag_eval_gov.metrics.rubric_scoring import score_question

ROOT = Path(__file__).resolve().parents[1]


def test_rubric_scoring_returns_dimension_specific_reasons() -> None:
    row = pd.Series(
        {
            "question_id": "Q1",
            "question_type": "factual",
            "retrieval_hit": True,
            "retrieval_precision_at_k": 0.8,
            "retrieval_recall_at_k": 1.0,
            "faithfulness_score": 1.0,
            "citation_precision": 1.0,
            "citation_recall": 1.0,
            "refusal_flag": False,
            "refusal_correct": False,
            "safety_flag": False,
            "human_review_expected": False,
            "human_review_flagged": False,
            "expected_section_ids": ["D1:S1"],
            "retrieved_section_ids": ["D1:S1"],
            "expected_citation_labels": ["D1:S1"],
            "citation_labels": ["D1:S1"],
        }
    )
    scores = score_question(row, ROOT / "configs/evaluation_rubrics.yaml")
    assert len(scores) == 10
    reasons = {item["dimension"]: item["reason"] for item in scores}
    assert reasons["context precision"] != reasons["citation support"]
