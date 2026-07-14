"""Provider-neutral generation interface."""

from __future__ import annotations

from typing import Protocol

from rag_eval_gov.config.schemas import QuestionRecord
from rag_eval_gov.generation.answer_schema import AnswerRecord
from rag_eval_gov.retrieval.vector_store import RetrievedChunk


class AnswerGenerator(Protocol):
    """Interface implemented by local and future provider-backed generators."""

    def generate(
        self,
        question: QuestionRecord,
        retrieved_chunks: list[RetrievedChunk],
    ) -> AnswerRecord:
        """Generate a structured answer record."""
