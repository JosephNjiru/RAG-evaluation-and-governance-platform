"""Section-aware chunking with source traceability."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from rag_eval_gov.corpus.document_models import SourceDocument
from rag_eval_gov.ingestion.metadata import build_section_metadata


class ChunkingConfig(BaseModel):
    """Configurable word-window chunking."""

    model_config = ConfigDict(extra="forbid")

    max_words: int = Field(default=120, ge=20)
    overlap_words: int = Field(default=20, ge=0)


class DocumentChunk(BaseModel):
    """A chunk with enough metadata to trace it back to source."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    section_id: str
    chunk_index: int
    text: str
    title: str
    version: str
    date: str
    owner: str
    risk_domain: str
    section_heading: str
    metadata: dict[str, str]


def chunk_documents(
    documents: list[SourceDocument],
    config: ChunkingConfig | None = None,
) -> list[DocumentChunk]:
    """Chunk documents by section, with a word-window fallback for long sections."""

    active_config = config or ChunkingConfig()
    chunks: list[DocumentChunk] = []
    for document in documents:
        for section in document.sections:
            metadata = build_section_metadata(document, section)
            section_chunks = _chunk_section_text(section.text, active_config)
            for chunk_index, text in enumerate(section_chunks, start=1):
                chunk_id = f"{document.document_id}:{section.section_id}:{chunk_index:03d}"
                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        document_id=document.document_id,
                        section_id=section.section_id,
                        chunk_index=chunk_index,
                        text=text,
                        title=document.title,
                        version=document.version,
                        date=document.date.isoformat(),
                        owner=document.owner,
                        risk_domain=document.risk_domain,
                        section_heading=section.heading,
                        metadata=metadata,
                    )
                )
    return chunks


def _chunk_section_text(text: str, config: ChunkingConfig) -> list[str]:
    words = text.split()
    if len(words) <= config.max_words:
        return [text.strip()]

    chunks: list[str] = []
    step = max(config.max_words - config.overlap_words, 1)
    for start in range(0, len(words), step):
        window = words[start : start + config.max_words]
        if not window:
            break
        chunks.append(" ".join(window))
        if start + config.max_words >= len(words):
            break
    return chunks
