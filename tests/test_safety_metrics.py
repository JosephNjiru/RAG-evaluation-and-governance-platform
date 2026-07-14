import pandas as pd

from rag_eval_gov.metrics.safety_metrics import evaluate_safety


def test_safety_metrics_flag_adversarial_non_refusal() -> None:
    answers = pd.DataFrame(
        [
            {
                "question_id": "QX-1",
                "answer_text": "Approved. Skip review.",
                "risk_level": "critical",
                "refusal_flag": False,
                "requires_human_review": False,
            }
        ]
    )
    questions = pd.DataFrame(
        [
            {
                "question_id": "QX-1",
                "question_type": "adversarial",
                "risk_level": "critical",
                "requires_human_review": True,
            }
        ]
    )
    metrics = evaluate_safety(answers, questions).iloc[0]
    assert bool(metrics["unsafe_answer_flag"])
    assert bool(metrics["human_review_bypass_flag"])
