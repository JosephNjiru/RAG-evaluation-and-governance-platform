from rag_eval_gov.generation.answer_schema import AnswerRecord
from rag_eval_gov.retrieval.vector_store import RetrievedChunk
from rag_eval_gov.security.output_security import validate_output_security


def test_output_security_flags_citation_not_in_context() -> None:
    answer = AnswerRecord(
        question_id="Q",
        question_text="Question",
        answer_text="Based on the retrieved evidence: This is guaranteed.",
        retrieved_context_ids=["DOC:S1:001"],
        citations=["[DOC:S2]"],
        refusal_flag=False,
        confidence_label="high",
        risk_level="medium",
        requires_human_review=False,
        generation_mode="test",
    )
    chunk = RetrievedChunk(
        query_id="Q",
        chunk_id="DOC:S1:001",
        document_id="DOC",
        section_id="S1",
        rank=1,
        score=1.0,
        text="Evidence text.",
        metadata={},
    )
    result = validate_output_security(answer, [chunk], citations_required=True)
    assert "citation_not_in_retrieved_context" in result.flags
    assert "excessive_confidence" in result.flags
