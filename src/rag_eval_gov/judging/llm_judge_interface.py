"""Optional LLM judge interface without provider calls."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LLMJudgeInput(BaseModel):
    """Provider-neutral input for a future optional judge."""

    model_config = ConfigDict(extra="forbid")

    question_id: str
    question_text: str
    answer_text: str
    retrieved_evidence: list[str]
    citations: list[str]
    rubric_dimension: str
    rubric_guidance: str


class LLMJudgeOutput(BaseModel):
    """Structured output expected from a future optional judge."""

    model_config = ConfigDict(extra="forbid")

    dimension: str
    score: int = Field(ge=0, le=4)
    reason: str
    evidence_used: list[str]
    uncertainty_notes: str


RUBRIC_PROMPT_TEMPLATE = """Assess the answer using only the supplied question, answer, citations, evidence and rubric.

Question: {question_text}
Answer: {answer_text}
Rubric dimension: {rubric_dimension}
Rubric guidance: {rubric_guidance}
Evidence:
{retrieved_evidence}

Return structured fields: dimension, score from 0 to 4, reason, evidence_used and uncertainty_notes.
"""


class LLMJudgeAdapter:
    """Stub for future provider-backed judging."""

    def judge(self, judge_input: LLMJudgeInput) -> LLMJudgeOutput:
        raise NotImplementedError("LLM judge calls are optional and disabled by default.")
