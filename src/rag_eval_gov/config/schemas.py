"""Pydantic schemas for Stage 1 configuration and evaluation assets."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

APPROVED_RISK_LEVELS = {"low", "medium", "high", "critical"}
APPROVED_QUESTION_TYPES = {"factual", "multi_hop", "ambiguous", "refusal", "adversarial"}
ANSWERABLE_QUESTION_TYPES = {"factual", "multi_hop"}


class StrictBaseModel(BaseModel):
    """Base model with strict extra-field handling."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ProjectConfig(StrictBaseModel):
    project_title: str
    package_name: str
    stage: int
    approved_risk_levels: list[str]
    approved_question_types: list[str]
    answerable_question_types: list[str]

    @field_validator("project_title", "package_name")
    @classmethod
    def non_empty_text(cls, value: str) -> str:
        if not value:
            raise ValueError("value must not be empty")
        return value


class CorpusConfig(StrictBaseModel):
    source_path: str
    required_metadata_fields: list[str]
    allowed_risk_domains: list[str]
    expected_document_count_min: int = Field(ge=1)
    expected_document_count_max: int = Field(ge=1)

    @model_validator(mode="after")
    def check_count_range(self) -> CorpusConfig:
        if self.expected_document_count_max < self.expected_document_count_min:
            raise ValueError("max document count must be at least the min count")
        return self


class ScoreLabel(StrictBaseModel):
    score: int
    label: str


class RubricDimension(StrictBaseModel):
    REQUIRED_DIMENSIONS: ClassVar[set[str]] = {
        "retrieval relevance",
        "context precision",
        "context recall",
        "answer faithfulness",
        "citation support",
        "answer completeness",
        "response relevance",
        "refusal quality",
        "safety and policy compliance",
        "human review need",
    }

    dimension: str
    score_min: int = Field(ge=0)
    score_max: int = Field(gt=0)
    score_labels: list[ScoreLabel]
    scoring_guidance: str
    common_failure_modes: list[str]

    @model_validator(mode="after")
    def check_score_bounds(self) -> RubricDimension:
        if self.score_max <= self.score_min:
            raise ValueError("score_max must be greater than score_min")
        label_scores = {item.score for item in self.score_labels}
        expected_scores = set(range(self.score_min, self.score_max + 1))
        if label_scores != expected_scores:
            raise ValueError("score_labels must cover every score from min to max")
        return self


class RubricConfig(StrictBaseModel):
    rubrics: list[RubricDimension]

    @model_validator(mode="after")
    def check_required_dimensions(self) -> RubricConfig:
        found = {item.dimension for item in self.rubrics}
        missing = RubricDimension.REQUIRED_DIMENSIONS - found
        if missing:
            raise ValueError(f"missing rubric dimensions: {sorted(missing)}")
        return self


class RiskItem(StrictBaseModel):
    risk_id: str
    risk_name: str
    description: str
    severity: str
    detection_signals: list[str]
    mitigation_controls: list[str]

    @field_validator("severity")
    @classmethod
    def severity_is_approved(cls, value: str) -> str:
        if value not in APPROVED_RISK_LEVELS:
            raise ValueError(f"invalid severity: {value}")
        return value


class RiskTaxonomyConfig(StrictBaseModel):
    risks: list[RiskItem]

    @model_validator(mode="after")
    def check_required_risks(self) -> RiskTaxonomyConfig:
        required = {
            "unsupported answer",
            "missed retrieval",
            "wrong citation",
            "citation overclaiming",
            "failure to refuse",
            "unsafe answer",
            "prompt injection susceptibility",
            "sensitive information disclosure",
            "stale information",
            "answer overconfidence",
            "ambiguous question mishandling",
            "human review bypass",
        }
        found = {item.risk_name for item in self.risks}
        missing = required - found
        if missing:
            raise ValueError(f"missing risk taxonomy items: {sorted(missing)}")
        return self


class QuestionRecord(StrictBaseModel):
    question_id: str
    question_text: str
    question_type: str
    risk_level: str
    expected_answer_type: str
    requires_human_review: bool
    expected_source_documents: str
    notes: str

    @field_validator("question_type")
    @classmethod
    def valid_question_type(cls, value: str) -> str:
        if value not in APPROVED_QUESTION_TYPES:
            raise ValueError(f"invalid question_type: {value}")
        return value

    @field_validator("risk_level")
    @classmethod
    def valid_risk_level(cls, value: str) -> str:
        if value not in APPROVED_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {value}")
        return value


class ReferenceAnswerRecord(StrictBaseModel):
    question_id: str
    reference_answer: str
    expected_citations: str
    answer_scope_notes: str


class EvidenceMapRecord(StrictBaseModel):
    question_id: str
    document_id: str
    section_id: str
    evidence_text: str
    evidence_relevance: str
    required_for_full_credit: bool


def validate_records(model: type[BaseModel], records: list[dict[str, Any]]) -> list[BaseModel]:
    """Validate records against a Pydantic model."""

    return [model.model_validate(record) for record in records]
