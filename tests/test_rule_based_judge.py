from pathlib import Path

import pandas as pd

from rag_eval_gov.judging.rule_based_judge import evaluate_questions

ROOT = Path(__file__).resolve().parents[1]


def test_rule_based_judge_produces_auditable_record() -> None:
    question_bank = pd.DataFrame(
        [
            {
                "question_id": "Q1",
                "question_text": "What is supported?",
                "question_type": "factual",
                "risk_level": "low",
                "expected_answer_type": "supported_answer",
                "requires_human_review": False,
                "expected_source_documents": "D1",
                "notes": "",
            }
        ]
    )
    references = pd.DataFrame([{"question_id": "Q1", "reference_answer": "Supported text."}])
    evidence = pd.DataFrame(
        [
            {
                "question_id": "Q1",
                "document_id": "D1",
                "section_id": "S1",
                "evidence_text": "Supported text.",
            }
        ]
    )
    answers = pd.DataFrame(
        [
            {
                "question_id": "Q1",
                "question_text": "What is supported?",
                "risk_level": "low",
                "answer_text": "Based on the retrieved evidence: Supported text.",
                "citations": ["[D1:S1]"],
                "refusal_flag": False,
                "requires_human_review": False,
            }
        ]
    )
    retrieval = pd.DataFrame(
        [{"query_id": "Q1", "document_id": "D1", "section_id": "S1", "rank": 1}]
    )
    results = evaluate_questions(
        question_bank,
        references,
        evidence,
        answers,
        retrieval,
        ROOT / "configs/evaluation_rubrics.yaml",
    )
    record = results.iloc[0]
    assert record["question_id"] == "Q1"
    assert len(record["rubric_scores"]) == 10
    assert bool(record["overall_pass"])
