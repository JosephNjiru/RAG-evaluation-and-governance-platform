import pandas as pd

from rag_eval_gov.metrics.retrieval_metrics import evaluate_retrieval


def test_retrieval_metrics_match_expected_sections() -> None:
    questions = pd.DataFrame([{"question_id": "Q1", "question_type": "factual"}])
    evidence = pd.DataFrame([{"question_id": "Q1", "document_id": "D1", "section_id": "S1"}])
    retrieved = pd.DataFrame(
        [
            {"query_id": "Q1", "document_id": "D1", "section_id": "S1", "rank": 1},
            {"query_id": "Q1", "document_id": "D2", "section_id": "S2", "rank": 2},
        ]
    )
    metrics = evaluate_retrieval(questions, evidence, retrieved, k=2).iloc[0]
    assert metrics["retrieval_precision_at_k"] == 0.5
    assert metrics["retrieval_recall_at_k"] == 1.0
    assert bool(metrics["hit_rate"])
