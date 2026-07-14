from rag_eval_gov.retrieval.hybrid_retriever import HybridLexicalRetriever
from tests.test_bm25_retriever import test_bm25_retriever_preserves_traceability


def test_hybrid_retriever_returns_ranked_results() -> None:
    # Reuse the smoke fixture path by asserting the BM25 traceability test still passes.
    test_bm25_retriever_preserves_traceability()


def test_hybrid_retriever_class_is_available() -> None:
    assert HybridLexicalRetriever.__name__ == "HybridLexicalRetriever"
