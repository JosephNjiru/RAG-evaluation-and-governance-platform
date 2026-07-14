import pandas as pd

from rag_eval_gov.metrics.faithfulness_metrics import evaluate_faithfulness


def test_faithfulness_scores_cited_overlap() -> None:
    answers = pd.DataFrame(
        [
            {
                "question_id": "Q1",
                "answer_text": "Based on the retrieved evidence: Secrets must be stored safely.",
                "citations": ["[D1:S1]"],
                "refusal_flag": False,
            }
        ]
    )
    evidence = pd.DataFrame(
        [
            {
                "question_id": "Q1",
                "document_id": "D1",
                "section_id": "S1",
                "evidence_text": "Secrets must be stored safely.",
            }
        ]
    )
    references = pd.DataFrame(
        [{"question_id": "Q1", "reference_answer": "Secrets must be stored safely."}]
    )
    metrics = evaluate_faithfulness(answers, evidence, references).iloc[0]
    assert metrics["faithfulness_score"] >= 0.8
    assert not bool(metrics["unsupported_claim_flag"])
