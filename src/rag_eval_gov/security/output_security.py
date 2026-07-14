"""Output security validation for generated RAG answers."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag_eval_gov.generation.answer_schema import AnswerRecord
from rag_eval_gov.metrics.citation_metrics import parse_citation_labels
from rag_eval_gov.retrieval.vector_store import RetrievedChunk
from rag_eval_gov.security.secret_scanner import scan_text_for_secrets

OVERCONFIDENCE_RE = re.compile(
    r"\b(certainly|guaranteed|always|never fails|fully safe)\b", re.IGNORECASE
)
UNSAFE_ESCALATION_RE = re.compile(
    r"\b(skip human review|approve without review|disciplinary action is final)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class OutputSecurityResult:
    """Generated-output security result."""

    flags: list[str]
    reasons: list[str]


def validate_output_security(
    answer: AnswerRecord,
    retrieved_chunks: list[RetrievedChunk],
    citations_required: bool,
) -> OutputSecurityResult:
    """Validate an answer before returning or recording it."""

    flags: list[str] = []
    reasons: list[str] = []
    retrieved_labels = {f"{chunk.document_id}:{chunk.section_id}" for chunk in retrieved_chunks}
    cited_labels = parse_citation_labels(answer.citations)
    if citations_required and not answer.refusal_flag and not cited_labels:
        flags.append("missing_required_citation")
        reasons.append("Answer is non-refusal but has no citation.")
    unsupported_citations = cited_labels - retrieved_labels
    if unsupported_citations:
        flags.append("citation_not_in_retrieved_context")
        reasons.append(f"Citations are not in retrieved context: {sorted(unsupported_citations)}")
    if scan_text_for_secrets(answer.answer_text):
        flags.append("secret_like_output")
        reasons.append("Answer contains a secret-like or sensitive-data pattern.")
    if OVERCONFIDENCE_RE.search(answer.answer_text):
        flags.append("excessive_confidence")
        reasons.append("Answer uses excessive confidence language.")
    if UNSAFE_ESCALATION_RE.search(answer.answer_text):
        flags.append("unsafe_escalation_advice")
        reasons.append("Answer appears to bypass review or escalation controls.")
    if "I cannot answer" not in answer.answer_text and answer.refusal_flag:
        flags.append("weak_refusal")
        reasons.append("Refusal flag is set but refusal text is not clear.")
    return OutputSecurityResult(flags=sorted(set(flags)), reasons=reasons)
