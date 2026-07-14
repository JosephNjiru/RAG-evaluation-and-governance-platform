"""Models for synthetic source documents."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class CorpusSection(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    section_id: str
    heading: str
    text: str


class SourceDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    document_id: str
    title: str
    version: str
    date: date
    owner: str
    risk_domain: str
    source_text: str
    sections: list[CorpusSection]
