"""Simple claim-level support screening."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag_eval_gov.metrics.faithfulness_metrics import overlap_score

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class ClaimSupportResult:
    """Claim support screening result."""

    claims: list[str]
    weakly_supported_claims: list[str]
    unsupported_claim_count: int
    min_support_score: float


def check_claim_support(
    answer_text: str, cited_evidence_text: str, threshold: float = 0.35
) -> ClaimSupportResult:
    """Flag answer claims with weak lexical support in cited evidence."""

    answer_body = answer_text.removeprefix("Based on the retrieved evidence: ").strip()
    claims = [claim.strip() for claim in SENTENCE_SPLIT_RE.split(answer_body) if claim.strip()]
    scores = [overlap_score(claim, cited_evidence_text) for claim in claims]
    weak_claims = [claim for claim, score in zip(claims, scores, strict=False) if score < threshold]
    return ClaimSupportResult(
        claims=claims,
        weakly_supported_claims=weak_claims,
        unsupported_claim_count=len(weak_claims),
        min_support_score=min(scores) if scores else 0.0,
    )
