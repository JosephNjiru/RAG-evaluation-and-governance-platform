from rag_eval_gov.metrics.claim_support import check_claim_support


def test_claim_support_flags_unsupported_claims() -> None:
    result = check_claim_support(
        "Human review is required. The system is externally certified.",
        "Human review is required for high-risk outputs.",
        threshold=0.35,
    )
    assert result.unsupported_claim_count >= 1
