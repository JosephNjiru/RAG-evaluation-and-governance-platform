"""Question intent signals inferred from question text."""

from __future__ import annotations

import re
from enum import StrEnum


class QuestionIntent(StrEnum):
    """Retrieval-aid labels inferred without ground-truth question type."""

    FACTUAL = "factual"
    LIKELY_MULTI_HOP = "likely_multi_hop"
    AMBIGUOUS = "ambiguous"
    ADVERSARIAL_SIGNAL = "adversarial_signal"
    UNSUPPORTED_OR_EXTERNAL_SIGNAL = "unsupported_or_external_signal"


MULTI_HOP_PATTERNS = [
    r"\band\b",
    r"\bboth\b",
    r"\bcompare\b",
    r"\brelationship\b",
    r"\baffect\b",
    r"\bcontrols?\b.*\breviewer\b",
    r"\bprocess\b.*\bexception\b",
    r"\bpolicy\b.*\bgovernance\b",
]
ADVERSARIAL_PATTERNS = [
    r"ignore (the )?(instructions|rules|policy)",
    r"override",
    r"system prompt",
    r"do not mention",
    r"quoted instruction",
]
UNSUPPORTED_PATTERNS = [
    r"\bexternal\b",
    r"\breal[- ]time\b",
    r"\bcurrent market\b",
    r"\bprivate key\b",
    r"\bcredential\b",
]
AMBIGUOUS_PATTERNS = [
    r"\bthat\b",
    r"\bthis\b",
    r"\bthe policy\b$",
    r"\bthe system\b$",
]


def detect_question_intent(question_text: str) -> QuestionIntent:
    """Infer retrieval intent from text only."""

    text = question_text.lower()
    if _matches(text, ADVERSARIAL_PATTERNS):
        return QuestionIntent.ADVERSARIAL_SIGNAL
    if _matches(text, UNSUPPORTED_PATTERNS):
        return QuestionIntent.UNSUPPORTED_OR_EXTERNAL_SIGNAL
    if _matches(text, MULTI_HOP_PATTERNS):
        return QuestionIntent.LIKELY_MULTI_HOP
    if len(re.findall(r"\w+", text)) <= 4 or _matches(text, AMBIGUOUS_PATTERNS):
        return QuestionIntent.AMBIGUOUS
    return QuestionIntent.FACTUAL


def _matches(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)
