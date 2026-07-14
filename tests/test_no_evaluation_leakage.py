from pathlib import Path

from rag_eval_gov.config.schemas import QuestionRecord
from rag_eval_gov.generation.mock_generator import MockAnswerGenerator
from rag_eval_gov.retrieval.vector_store import RetrievedChunk


def test_retrieval_and_generation_do_not_import_evidence_map() -> None:
    scanned_dirs = [Path("src/rag_eval_gov/retrieval"), Path("src/rag_eval_gov/generation")]
    offending: list[str] = []
    for directory in scanned_dirs:
        for path in directory.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if "evidence_map" in text or "EvidenceMap" in text:
                offending.append(str(path))
    assert offending == []


def test_generation_runs_without_loading_evidence_map_csv() -> None:
    question = QuestionRecord(
        question_id="Q",
        question_text="What review is required?",
        question_type="factual",
        risk_level="medium",
        expected_answer_type="supported_answer",
        requires_human_review=False,
        expected_source_documents="DOC-1",
        notes="test",
    )
    chunk = RetrievedChunk(
        query_id="Q",
        chunk_id="DOC-1:S1:001",
        document_id="DOC-1",
        section_id="S1",
        rank=1,
        score=1.0,
        text="Human review is required.",
        metadata={},
    )
    answer = MockAnswerGenerator().generate(question, [chunk])
    assert answer.citations == ["[DOC-1:S1]"]
