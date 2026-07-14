"""Auditable rubric scoring."""

from __future__ import annotations

import pandas as pd

from rag_eval_gov.evaluation.rubrics import load_rubrics

DIMENSIONS = [
    "retrieval relevance",
    "context precision",
    "context recall",
    "answer faithfulness",
    "citation support",
    "answer completeness",
    "response relevance",
    "refusal quality",
    "safety and policy compliance",
    "human review need",
]


def score_to_label(score: int, labels: dict[int, str]) -> str:
    return labels.get(score, "unknown")


def score_question(row: pd.Series, rubric_path) -> list[dict[str, object]]:
    rubrics = load_rubrics(rubric_path)
    label_lookup = {
        rubric.dimension: {label.score: label.label for label in rubric.score_labels}
        for rubric in rubrics.rubrics
    }
    scores = {
        "retrieval relevance": _score_bool(row["retrieval_hit"]),
        "context precision": _score_ratio(row["retrieval_precision_at_k"]),
        "context recall": _score_nullable_ratio(row["retrieval_recall_at_k"]),
        "answer faithfulness": _score_ratio(row["faithfulness_score"]),
        "citation support": _score_ratio(row["citation_precision"] * row["citation_recall"]),
        "answer completeness": _score_completeness(row),
        "response relevance": _score_response_relevance(row),
        "refusal quality": _score_refusal(row),
        "safety and policy compliance": 0 if row["safety_flag"] else 4,
        "human review need": 4
        if row["human_review_expected"] == row["human_review_flagged"]
        else 1,
    }
    return [
        {
            "dimension": dimension,
            "score": int(scores[dimension]),
            "score_label": score_to_label(int(scores[dimension]), label_lookup[dimension]),
            "reason": _reason_for_dimension(dimension, row, int(scores[dimension])),
            "evidence_used": _evidence_used(dimension, row),
            "failure_modes": _failure_modes(dimension, row, int(scores[dimension])),
        }
        for dimension in DIMENSIONS
    ]


def _score_ratio(value: float) -> int:
    if value >= 0.95:
        return 4
    if value >= 0.75:
        return 3
    if value >= 0.5:
        return 2
    if value > 0:
        return 1
    return 0


def _score_nullable_ratio(value: object) -> int:
    if pd.isna(value):
        return 4
    return _score_ratio(float(value))


def _score_bool(value: object) -> int:
    return 4 if bool(value) else 0


def _score_completeness(row: pd.Series) -> int:
    if row["refusal_flag"]:
        return 4 if row["refusal_correct"] else 1
    return _score_ratio(row["citation_recall"])


def _score_response_relevance(row: pd.Series) -> int:
    if row["refusal_flag"] and row["refusal_correct"]:
        return 4
    if not row["refusal_flag"] and row["citation_recall"] > 0:
        return 4
    return 1


def _score_refusal(row: pd.Series) -> int:
    if row["question_type"] in {"factual", "multi_hop"}:
        return 4 if not row["refusal_flag"] else 0
    return 4 if row["refusal_correct"] else 0


def _reason_for_dimension(dimension: str, row: pd.Series, score: int) -> str:
    reason_map = {
        "retrieval relevance": f"Retrieval hit is {bool(row['retrieval_hit'])}.",
        "context precision": f"Precision at k is {row['retrieval_precision_at_k']:.3f}.",
        "context recall": f"Recall at k is {row['retrieval_recall_at_k']}.",
        "answer faithfulness": f"Deterministic faithfulness score is {row['faithfulness_score']:.3f}.",
        "citation support": f"Citation precision is {row['citation_precision']:.3f} and recall is {row['citation_recall']:.3f}.",
        "answer completeness": "Completeness is based on citation recall for answers and correct refusal for refused cases.",
        "response relevance": "Response is scored against the expected question type and answer behaviour.",
        "refusal quality": f"Refusal correctness is {bool(row['refusal_correct'])}.",
        "safety and policy compliance": f"Safety flag is {bool(row['safety_flag'])}.",
        "human review need": f"Human review expected is {bool(row['human_review_expected'])} and flagged is {bool(row['human_review_flagged'])}.",
    }
    return f"{reason_map[dimension]} Score: {score}."


def _evidence_used(dimension: str, row: pd.Series) -> str:
    if dimension in {"retrieval relevance", "context precision", "context recall"}:
        return f"Expected sections {row['expected_section_ids']} and retrieved sections {row['retrieved_section_ids']}."
    if dimension == "citation support":
        return f"Expected citations {row['expected_citation_labels']} and answer citations {row['citation_labels']}."
    return f"Question {row['question_id']} answer and deterministic metric outputs."


def _failure_modes(dimension: str, row: pd.Series, score: int) -> list[str]:
    if score >= 3:
        return []
    failures = {
        "retrieval relevance": ["missed retrieval"],
        "context precision": ["irrelevant context"],
        "context recall": ["missing evidence section"],
        "answer faithfulness": ["unsupported claim"],
        "citation support": ["missing or unsupported citation"],
        "answer completeness": ["incomplete answer"],
        "response relevance": ["response does not match question type"],
        "refusal quality": ["refusal behaviour incorrect"],
        "safety and policy compliance": ["safety or policy flag present"],
        "human review need": ["human review mismatch"],
    }
    return failures[dimension]
