import pandas as pd

from rag_eval_gov.metrics.citation_metrics import evaluate_citations


def test_citation_metrics_check_support_against_evidence_map() -> None:
    answers = pd.DataFrame([{"question_id": "Q1", "citations": ["[D1:S1]", "[D2:S2]"]}])
    evidence = pd.DataFrame([{"question_id": "Q1", "document_id": "D1", "section_id": "S1"}])
    metrics = evaluate_citations(answers, evidence).iloc[0]
    assert metrics["citation_precision"] == 0.5
    assert metrics["citation_recall"] == 1.0
    assert metrics["unsupported_citation_count"] == 1
