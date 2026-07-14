"""Deterministic local answer generator for Stage 2."""

from __future__ import annotations

from rag_eval_gov.config.schemas import QuestionRecord
from rag_eval_gov.generation.answer_schema import AnswerRecord
from rag_eval_gov.generation.citation_formatter import citations_from_chunks, format_citations
from rag_eval_gov.retrieval.vector_store import RetrievedChunk

REFUSAL_TYPES = {"refusal", "adversarial"}
REVIEW_TYPES = {"ambiguous", "refusal", "adversarial", "multi_hop"}


class MockAnswerGenerator:
    """Controlled baseline that does not use external model calls."""

    generation_mode = "deterministic_mock"

    def generate(
        self,
        question: QuestionRecord,
        retrieved_chunks: list[RetrievedChunk],
    ) -> AnswerRecord:
        retrieved_ids = [chunk.chunk_id for chunk in retrieved_chunks]
        useful_chunks = [chunk for chunk in retrieved_chunks if chunk.score > 0]

        if self._should_refuse(question, useful_chunks):
            return AnswerRecord(
                question_id=question.question_id,
                question_text=question.question_text,
                answer_text=self._refusal_text(question),
                retrieved_context_ids=retrieved_ids,
                citations=[],
                refusal_flag=True,
                confidence_label="low",
                risk_level=question.risk_level,
                requires_human_review=True,
                generation_mode=self.generation_mode,
            )

        citation_chunks = (
            useful_chunks[:2] if question.question_type == "multi_hop" else useful_chunks[:1]
        )
        citations = citations_from_chunks(citation_chunks)
        answer_text = self._answer_from_chunks(citation_chunks)
        return AnswerRecord(
            question_id=question.question_id,
            question_text=question.question_text,
            answer_text=answer_text,
            retrieved_context_ids=retrieved_ids,
            citations=format_citations(citations),
            refusal_flag=False,
            confidence_label="medium" if question.question_type == "multi_hop" else "high",
            risk_level=question.risk_level,
            requires_human_review=question.requires_human_review,
            generation_mode=self.generation_mode,
        )

    def _should_refuse(self, question: QuestionRecord, useful_chunks: list[RetrievedChunk]) -> bool:
        if question.question_type in REFUSAL_TYPES:
            return True
        if question.question_type == "ambiguous":
            return True
        return not useful_chunks

    def _refusal_text(self, question: QuestionRecord) -> str:
        if question.question_type == "ambiguous":
            return "I cannot answer reliably from the corpus because the question is ambiguous and needs human review."
        return "I cannot answer from the supplied corpus evidence. The request is unsupported or requires refusal and human review."

    def _answer_from_chunks(self, chunks: list[RetrievedChunk]) -> str:
        cited_text = " ".join(chunk.text for chunk in chunks)
        return f"Based on the retrieved evidence: {cited_text}"
