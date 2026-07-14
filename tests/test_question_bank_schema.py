from pathlib import Path

from rag_eval_gov.evaluation.question_bank import load_question_bank, question_counts_by_type

ROOT = Path(__file__).resolve().parents[1]


def test_question_bank_schema_and_counts() -> None:
    records = load_question_bank(ROOT / "data/evaluation/question_bank.csv")
    counts = question_counts_by_type(records)
    assert len(records) >= 60
    assert counts["factual"] >= 20
    assert counts["multi_hop"] >= 10
    assert counts["ambiguous"] >= 10
    assert counts["refusal"] >= 10
    assert counts["adversarial"] >= 10


def test_question_ids_are_unique() -> None:
    records = load_question_bank(ROOT / "data/evaluation/question_bank.csv")
    ids = [record.question_id for record in records]
    assert len(ids) == len(set(ids))
