"""Deterministic query decomposition for likely multi-evidence questions."""

from __future__ import annotations

import re

from rag_eval_gov.retrieval.question_intent import QuestionIntent, detect_question_intent

SPLIT_PATTERNS = [
    r"\s+and\s+",
    r"\s+compare\s+",
    r"\s+while\s+",
    r"\s+but\s+",
]


def decompose_query(question_text: str) -> list[str]:
    """Split a question into retrieval sub-queries using text-only rules."""

    intent = detect_question_intent(question_text)
    if intent != QuestionIntent.LIKELY_MULTI_HOP:
        return [question_text]

    cleaned = question_text.strip().rstrip("?")
    parts = [cleaned]
    for pattern in SPLIT_PATTERNS:
        next_parts: list[str] = []
        for part in parts:
            next_parts.extend(re.split(pattern, part, flags=re.IGNORECASE))
        parts = next_parts

    normalised = [_normalise_part(part) for part in parts if _normalise_part(part)]
    if len(normalised) < 2:
        return [question_text]
    return normalised[:4]


def _normalise_part(part: str) -> str:
    part = re.sub(r"^(what|which|how|when|where|why)\s+", "", part.strip(), flags=re.IGNORECASE)
    part = re.sub(r"\s+", " ", part)
    return part
