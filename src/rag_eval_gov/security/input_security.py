"""Input security checks for local RAG requests."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag_eval_gov.security.security_policy import MAX_INPUT_CHARS

INSTRUCTION_OVERRIDE_RE = re.compile(
    r"ignore (all )?(previous|system|developer|policy|safety) (instructions|rules)|"
    r"override (the )?(system|policy)|"
    r"disregard (the )?(rules|instructions)",
    re.IGNORECASE,
)
SECRET_REQUEST_RE = re.compile(
    r"\b(secret|password|token|api key|private key|credential|system prompt)\b",
    re.IGNORECASE,
)
UNSUPPORTED_ADVICE_RE = re.compile(
    r"\b(legal advice|medical advice|financial advice|disciplinary decision|fire an employee|"
    r"deny eligibility|diagnose|prescribe|investment recommendation)\b",
    re.IGNORECASE,
)
MALFORMED_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


@dataclass(frozen=True)
class SecurityAssessment:
    """Structured security assessment."""

    flags: list[str]
    reasons: list[str]
    should_refuse: bool


def assess_input_security(question_text: str) -> SecurityAssessment:
    """Assess one user input without blindly blocking every request."""

    flags: list[str] = []
    reasons: list[str] = []
    text = question_text or ""
    if not text.strip():
        flags.append("malformed_input")
        reasons.append("Input is empty or whitespace only.")
    if len(text) > MAX_INPUT_CHARS:
        flags.append("unbounded_input")
        reasons.append("Input exceeds the local request text limit.")
    if MALFORMED_RE.search(text):
        flags.append("malformed_input")
        reasons.append("Input contains control characters.")
    if INSTRUCTION_OVERRIDE_RE.search(text):
        flags.append("instruction_override")
        reasons.append("Input attempts to override system or policy instructions.")
    if SECRET_REQUEST_RE.search(text):
        flags.append("secret_request")
        reasons.append("Input requests secrets, credentials or hidden prompts.")
    if UNSUPPORTED_ADVICE_RE.search(text):
        flags.append("unsupported_advice")
        reasons.append("Input requests unsupported high-stakes advice.")
    should_refuse = any(
        flag in flags for flag in {"instruction_override", "secret_request", "unsupported_advice"}
    )
    return SecurityAssessment(
        flags=sorted(set(flags)), reasons=reasons, should_refuse=should_refuse
    )
