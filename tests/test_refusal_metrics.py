import pandas as pd

from rag_eval_gov.metrics.refusal_metrics import evaluate_refusals, refusal_summary


def test_refusal_metrics_distinguish_false_and_correct_refusals() -> None:
    answers = pd.DataFrame(
        [
            {
                "question_id": "Q1",
                "answer_text": "I cannot answer from the corpus evidence.",
                "refusal_flag": True,
            },
            {
                "question_id": "Q2",
                "answer_text": "Supported answer.",
                "refusal_flag": False,
            },
            {
                "question_id": "Q3",
                "answer_text": "I cannot answer from the corpus evidence.",
                "refusal_flag": True,
            },
        ]
    )
    questions = pd.DataFrame(
        [
            {"question_id": "Q1", "question_type": "refusal", "expected_answer_type": "refusal"},
            {
                "question_id": "Q2",
                "question_type": "factual",
                "expected_answer_type": "supported_answer",
            },
            {
                "question_id": "Q3",
                "question_type": "factual",
                "expected_answer_type": "supported_answer",
            },
        ]
    )
    metrics = evaluate_refusals(answers, questions)
    summary = refusal_summary(metrics)
    assert bool(metrics.loc[metrics["question_id"] == "Q1", "correct_refusal"].iloc[0])
    assert bool(metrics.loc[metrics["question_id"] == "Q2", "correct_refusal"].iloc[0])
    assert bool(metrics.loc[metrics["question_id"] == "Q3", "false_refusal"].iloc[0])
    assert summary["refusal_precision"] == 0.5
