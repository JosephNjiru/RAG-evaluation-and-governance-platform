"""API request and response schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class QuestionRequest(BaseModel):
    """Question submitted to the local RAG baseline."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    question_text: str = Field(min_length=1, max_length=4000)
    question_id: str | None = None
    question_type: str = "factual"
    risk_level: str = "medium"
    requires_human_review: bool = False


class RetrievedContextResponse(BaseModel):
    """Retrieved source-linked context returned by the API."""

    chunk_id: str
    document_id: str
    section_id: str
    rank: int
    score: float
    text: str


class AnswerResponse(BaseModel):
    """Structured answer returned by the local RAG baseline."""

    question_id: str
    question_text: str
    answer_text: str
    retrieved_contexts: list[RetrievedContextResponse]
    citations: list[str]
    refusal_flag: bool
    confidence_label: str
    risk_level: str
    requires_human_review: bool
    generation_mode: str
    evaluation_summary: dict[str, object] | None = None
    security_flags: list[str] = Field(default_factory=list)
    security_action: str = "allow"


class EvaluationRequest(BaseModel):
    """Request for evaluating or retrieving evaluation for one answer."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    question_id: str | None = None
    question_text: str | None = None


class EvaluationResponse(BaseModel):
    """Per-question evaluation response."""

    question_id: str
    question_type: str
    overall_pass: bool
    retrieval_hit: bool
    citation_precision: float
    citation_recall: float
    faithfulness_score: float
    refusal_correct: bool
    safety_flag: bool
    human_review_expected: bool
    human_review_flagged: bool
    evaluation_notes: str


class SummaryResponse(BaseModel):
    """Stage 3 summary exposed by the API."""

    questions: int
    overall_pass_rate: float
    factual_pass_rate: float
    multi_hop_pass_rate: float
    citation_precision: float
    citation_recall: float
    faithfulness_score: float
    human_review_match_rate: float
    safety_flag_rate: float


class HumanReviewQueueItem(BaseModel):
    """One record that needs human review or has failed a quality gate."""

    question_id: str
    question_type: str
    risk_level: str
    overall_pass: bool
    safety_flag: bool
    human_review_expected: bool
    human_review_flagged: bool
    evaluation_notes: str
