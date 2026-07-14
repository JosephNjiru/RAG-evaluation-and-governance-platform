"""Structured answer records."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Citation(BaseModel):
    """Citation to a source section and chunk."""

    model_config = ConfigDict(extra="forbid")

    document_id: str
    section_id: str
    chunk_id: str

    @property
    def label(self) -> str:
        return f"{self.document_id}:{self.section_id}"


class AnswerRecord(BaseModel):
    """Schema for one generated answer."""

    model_config = ConfigDict(extra="forbid")

    question_id: str
    question_text: str
    answer_text: str
    retrieved_context_ids: list[str]
    citations: list[str]
    refusal_flag: bool
    confidence_label: str
    risk_level: str
    requires_human_review: bool
    generation_mode: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
