from pathlib import Path

from rag_eval_gov.evaluation.question_bank import load_question_bank
from rag_eval_gov.generation.prompt_builder import build_prompt
from rag_eval_gov.ingestion.chunker import chunk_documents
from rag_eval_gov.ingestion.document_loader import load_markdown_documents
from rag_eval_gov.retrieval.vector_store import LocalVectorStore

ROOT = Path(__file__).resolve().parents[1]


def test_prompt_builder_separates_question_and_evidence() -> None:
    question = load_question_bank(ROOT / "data/evaluation/question_bank.csv")[0]
    store = LocalVectorStore.build(
        chunk_documents(load_markdown_documents(ROOT / "data/corpus/source_documents"))
    )
    retrieved = store.search(question.question_id, question.question_text, top_k=2)
    prompt = build_prompt(question, retrieved)
    assert "Trusted system instructions:" in prompt
    assert "User question:" in prompt
    assert "Untrusted retrieved evidence:" in prompt
    assert "Required answer format:" in prompt
