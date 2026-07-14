from pathlib import Path

from rag_eval_gov.evaluation.question_bank import load_question_bank
from rag_eval_gov.generation.mock_generator import MockAnswerGenerator
from rag_eval_gov.ingestion.chunker import chunk_documents
from rag_eval_gov.ingestion.document_loader import load_markdown_documents
from rag_eval_gov.retrieval.vector_store import LocalVectorStore

ROOT = Path(__file__).resolve().parents[1]


def test_mock_generator_refuses_unsupported_question() -> None:
    questions = load_question_bank(ROOT / "data/evaluation/question_bank.csv")
    refusal = next(question for question in questions if question.question_id == "QR-001")
    answer = MockAnswerGenerator().generate(refusal, [])
    assert answer.refusal_flag is True
    assert answer.citations == []
    assert answer.requires_human_review is True


def test_mock_generator_cites_answerable_question() -> None:
    questions = load_question_bank(ROOT / "data/evaluation/question_bank.csv")
    question = next(item for item in questions if item.question_id == "QF-007")
    store = LocalVectorStore.build(
        chunk_documents(load_markdown_documents(ROOT / "data/corpus/source_documents"))
    )
    retrieved = store.search(question.question_id, question.question_text, top_k=3)
    answer = MockAnswerGenerator().generate(question, retrieved)
    assert answer.refusal_flag is False
    assert answer.citations
    assert "[DOC-003:SEC-PROC-001]" in answer.citations
