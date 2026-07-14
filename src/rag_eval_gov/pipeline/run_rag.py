"""Run the local Stage 2 RAG pipeline for one question."""

from __future__ import annotations

from rag_eval_gov.config.schemas import QuestionRecord
from rag_eval_gov.generation.answer_schema import AnswerRecord
from rag_eval_gov.generation.mock_generator import MockAnswerGenerator
from rag_eval_gov.generation.prompt_builder import build_prompt
from rag_eval_gov.retrieval.retriever import Retriever


def run_rag_question(
    question: QuestionRecord,
    retriever: Retriever,
    generator: MockAnswerGenerator | None = None,
) -> AnswerRecord:
    """Retrieve evidence and generate one structured answer record."""

    active_generator = generator or MockAnswerGenerator()
    retrieved_chunks = retriever.retrieve(question.question_id, question.question_text)
    build_prompt(question, retrieved_chunks)
    return active_generator.generate(question, retrieved_chunks)
