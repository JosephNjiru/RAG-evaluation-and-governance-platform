# Data flow

The data path is designed for auditability.

1. Synthetic Markdown source documents are stored in `data/corpus/source_documents`.
2. The document loader extracts document metadata and sections.
3. The chunker creates section-linked chunks with document and section identifiers.
4. The TF-IDF vector index stores local lexical retrieval features.
5. The retriever returns top-k chunks with document, section, rank and score metadata.
6. The mock generator creates structured answer records and citations from retrieved chunks.
7. The evaluation engine compares retrieval and citation behaviour against the evidence map.
8. Reports, dashboard output and governance artefacts summarise quality, risk and review needs.

This path keeps source traceability intact from corpus text to final evaluation records.
