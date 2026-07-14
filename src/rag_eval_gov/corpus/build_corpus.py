"""Parse Stage 1 Markdown corpus files."""

from __future__ import annotations

from pathlib import Path

import yaml

from rag_eval_gov.corpus.document_models import CorpusSection, SourceDocument


def _split_front_matter(text: str, path: Path) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"Missing front matter in {path}")
    _, front_matter, body = text.split("---\n", 2)
    metadata = yaml.safe_load(front_matter) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"Invalid front matter in {path}")
    return metadata, body.strip()


def _parse_sections(body: str) -> list[CorpusSection]:
    sections: list[CorpusSection] = []
    current_heading = ""
    current_lines: list[str] = []

    def flush() -> None:
        if current_heading:
            section_id = current_heading.split(" ", 1)[0].strip()
            sections.append(
                CorpusSection(
                    section_id=section_id,
                    heading=current_heading,
                    text="\n".join(current_lines).strip(),
                )
            )

    for line in body.splitlines():
        if line.startswith("## "):
            flush()
            current_heading = line.removeprefix("## ").strip()
            current_lines = []
        else:
            current_lines.append(line)
    flush()
    return sections


def load_source_document(path: Path) -> SourceDocument:
    """Load one Markdown source document."""

    text = path.read_text(encoding="utf-8")
    metadata, body = _split_front_matter(text, path)
    sections = _parse_sections(body)
    return SourceDocument(source_text=body, sections=sections, **metadata)


def load_corpus(source_dir: Path) -> list[SourceDocument]:
    """Load all Markdown source documents from a directory."""

    documents = [load_source_document(path) for path in sorted(source_dir.glob("*.md"))]
    if not documents:
        raise ValueError(f"No Markdown documents found in {source_dir}")
    return documents
