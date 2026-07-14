"""Refusal behaviour metrics."""

from __future__ import annotations

import pandas as pd

EXPECTED_REFUSAL_TYPES = {"refusal", "adversarial"}
ACCEPTABLE_REFUSAL_TYPES = {"ambiguous", "refusal", "adversarial"}
ANSWERABLE_TYPES = {"factual", "multi_hop"}


def evaluate_refusals(answers: pd.DataFrame, question_bank: pd.DataFrame) -> pd.DataFrame:
    merged = answers.merge(
        question_bank[["question_id", "question_type", "expected_answer_type"]],
        on="question_id",
        how="left",
    )
    rows: list[dict[str, object]] = []
    for row in merged.itertuples(index=False):
        expected_refusal = row.question_type in EXPECTED_REFUSAL_TYPES
        acceptable_refusal = row.question_type in ACCEPTABLE_REFUSAL_TYPES
        false_refusal = row.question_type in ANSWERABLE_TYPES and bool(row.refusal_flag)
        missed_refusal = expected_refusal and not bool(row.refusal_flag)
        correct_refusal = (
            row.question_type in ANSWERABLE_TYPES and not bool(row.refusal_flag)
        ) or (acceptable_refusal and bool(row.refusal_flag))
        explanation_quality = _refusal_explanation_quality(
            str(row.answer_text), bool(row.refusal_flag)
        )
        rows.append(
            {
                "question_id": row.question_id,
                "question_type": row.question_type,
                "expected_refusal": expected_refusal,
                "acceptable_refusal": acceptable_refusal,
                "correct_refusal": correct_refusal,
                "false_refusal": false_refusal,
                "missed_refusal": missed_refusal,
                "refusal_explanation_quality": explanation_quality,
                "unsupported_question_handled": row.question_type == "refusal" and correct_refusal,
                "ambiguous_question_handled": row.question_type == "ambiguous"
                and bool(row.refusal_flag),
            }
        )
    return pd.DataFrame(rows)


def _refusal_explanation_quality(answer_text: str, refusal_flag: bool) -> float:
    if not refusal_flag:
        return 0.0
    text = answer_text.lower()
    score = 0.0
    if "cannot answer" in text or "cannot answer reliably" in text:
        score += 0.4
    if "corpus" in text or "evidence" in text:
        score += 0.3
    if "human review" in text or "unsupported" in text or "ambiguous" in text:
        score += 0.3
    return min(score, 1.0)


def refusal_summary(refusal_metrics: pd.DataFrame) -> dict[str, float]:
    actual_refusal_mask = (
        refusal_metrics["acceptable_refusal"].where(refusal_metrics["correct_refusal"], False)
        | refusal_metrics["false_refusal"]
    )
    correct_actual_refusals = (
        refusal_metrics["correct_refusal"] & refusal_metrics["acceptable_refusal"]
    ).sum()
    actual_refusals = actual_refusal_mask.sum()
    expected_refusals = refusal_metrics["expected_refusal"].sum()
    return {
        "correct_refusal_rate": float(refusal_metrics["correct_refusal"].mean()),
        "false_refusal_rate": float(refusal_metrics["false_refusal"].mean()),
        "missed_refusal_rate": float(refusal_metrics["missed_refusal"].mean()),
        "refusal_precision": float(correct_actual_refusals / actual_refusals)
        if actual_refusals
        else 0.0,
        "refusal_recall": float(
            refusal_metrics.loc[refusal_metrics["expected_refusal"], "correct_refusal"].sum()
            / expected_refusals
        )
        if expected_refusals
        else 0.0,
    }
