import pandas as pd


def test_challenge_set_has_required_question_types() -> None:
    questions = pd.read_csv("data/evaluation/challenge_questions.csv")
    assert len(questions) >= 15
    assert (questions["question_type"] == "multi_hop").sum() >= 5
    assert (questions["question_type"] == "adversarial").sum() >= 2
    assert (questions["question_type"] == "refusal").sum() >= 2
