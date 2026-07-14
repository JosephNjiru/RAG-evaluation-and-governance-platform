"""Security checks for untrusted retrieved context."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag_eval_gov.retrieval.vector_store import RetrievedChunk

CONTEXT_INJECTION_RE = re.compile(
    r"ignore (previous|system|developer|policy) instructions|"
    r"reveal (the )?(system prompt|secret|token|password)|"
    r"do not mention human review|"
    r"approve the answer",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ContextSecurityResult:
    """Retrieved-context security result."""

    flags: list[str]
    flagged_context_ids: list[str]
    reasons: list[str]


def assess_retrieved_context(chunks: list[RetrievedChunk]) -> ContextSecurityResult:
    """Treat retrieved evidence as untrusted and flag suspicious instructions."""

    flags: list[str] = []
    flagged_ids: list[str] = []
    reasons: list[str] = []
    for chunk in chunks:
        if CONTEXT_INJECTION_RE.search(chunk.text):
            flags.append("indirect_prompt_injection")
            flagged_ids.append(chunk.chunk_id)
            reasons.append(f"Retrieved chunk {chunk.chunk_id} contains instruction-like text.")
    return ContextSecurityResult(
        flags=sorted(set(flags)),
        flagged_context_ids=flagged_ids,
        reasons=reasons,
    )
