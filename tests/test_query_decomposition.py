from rag_eval_gov.retrieval.query_decomposition import decompose_query


def test_decompose_query_splits_multi_part_question() -> None:
    parts = decompose_query("What controls and who reviews high-risk answers?")
    assert len(parts) >= 2
    assert any("controls" in part for part in parts)
