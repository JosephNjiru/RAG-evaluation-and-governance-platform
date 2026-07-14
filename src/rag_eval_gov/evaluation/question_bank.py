"""Question bank loading and validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from rag_eval_gov.config.schemas import QuestionRecord


def load_question_bank(path: Path) -> list[QuestionRecord]:
    records = pd.read_csv(path).fillna("").to_dict(orient="records")
    return [QuestionRecord.model_validate(record) for record in records]


def question_counts_by_type(records: list[QuestionRecord]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        counts[record.question_type] = counts.get(record.question_type, 0) + 1
    return counts
