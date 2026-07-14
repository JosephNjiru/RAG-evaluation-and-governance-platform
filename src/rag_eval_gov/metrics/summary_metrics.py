"""Summary helpers for Stage 3 outputs."""

from __future__ import annotations

import pandas as pd


def build_summary_table(results: pd.DataFrame) -> pd.DataFrame:
    rows = [_summary_row("overall", results)]
    for question_type, group in results.groupby("question_type"):
        rows.append(_summary_row(question_type, group))
    return pd.DataFrame(rows)


def _summary_row(question_type: str, frame: pd.DataFrame) -> dict[str, object]:
    answerable = frame[frame["expected_section_ids"].map(len) > 0]
    return {
        "question_type": question_type,
        "questions": len(frame),
        "overall_pass_rate": frame["overall_pass"].mean(),
        "retrieval_hit_rate": _mean_or_none(answerable, "retrieval_hit"),
        "mean_retrieval_precision": _mean_or_none(answerable, "retrieval_precision_at_k"),
        "mean_retrieval_recall": _mean_or_none(answerable, "retrieval_recall_at_k"),
        "mean_reciprocal_rank": _mean_or_none(answerable, "mean_reciprocal_rank"),
        "mean_citation_precision": frame["citation_precision"].mean(),
        "mean_citation_recall": frame["citation_recall"].mean(),
        "mean_faithfulness": frame["faithfulness_score"].mean(),
        "refusal_correct_rate": frame["refusal_correct"].mean(),
        "safety_flag_rate": frame["safety_flag"].mean(),
        "human_review_match_rate": frame["human_review_match"].mean(),
    }


def _mean_or_none(frame: pd.DataFrame, column: str) -> float | None:
    if frame.empty:
        return None
    return float(frame[column].mean())
