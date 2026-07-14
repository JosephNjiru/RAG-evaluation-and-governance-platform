"""Metadata helpers for source-linked chunks."""

from __future__ import annotations

from rag_eval_gov.corpus.document_models import CorpusSection, SourceDocument


def build_section_metadata(document: SourceDocument, section: CorpusSection) -> dict[str, str]:
    """Create metadata carried by every chunk derived from a section."""

    return {
        "document_id": document.document_id,
        "title": document.title,
        "version": document.version,
        "date": document.date.isoformat(),
        "owner": document.owner,
        "risk_domain": document.risk_domain,
        "section_id": section.section_id,
        "section_heading": section.heading,
    }
