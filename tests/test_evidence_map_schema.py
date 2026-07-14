from pathlib import Path

from rag_eval_gov.config.schemas import ANSWERABLE_QUESTION_TYPES
from rag_eval_gov.evaluation.evidence_map import load_evidence_map
from rag_eval_gov.evaluation.question_bank import load_question_bank

ROOT = Path(__file__).resolve().parents[1]


def test_answerable_questions_have_evidence() -> None:
    questions = load_question_bank(ROOT / "data/evaluation/question_bank.csv")
    evidence = load_evidence_map(ROOT / "data/evaluation/evidence_map.csv")
    answerable_ids = {
        question.question_id
        for question in questions
        if question.question_type in ANSWERABLE_QUESTION_TYPES
    }
    evidence_ids = {row.question_id for row in evidence}
    assert answerable_ids <= evidence_ids


def test_refusal_questions_have_no_evidence() -> None:
    questions = load_question_bank(ROOT / "data/evaluation/question_bank.csv")
    evidence = load_evidence_map(ROOT / "data/evaluation/evidence_map.csv")
    refusal_ids = {
        question.question_id for question in questions if question.question_type == "refusal"
    }
    evidence_ids = {row.question_id for row in evidence}
    assert refusal_ids.isdisjoint(evidence_ids)
