# Retrieval improvement design

## Why TF-IDF was kept first

The initial baseline used TF-IDF because it is local, transparent and repeatable. It gave a clean first measurement of retrieval behaviour without paid APIs, model downloads or provider drift.

## Why multi-hop questions were difficult

Multi-hop questions often require evidence from more than one section or document. A simple top-k lexical retriever can retrieve one relevant section while missing the second evidence point. The original result showed this clearly: factual questions passed at 1.000, while multi-hop questions passed at 0.100.

## Added retrieval methods

- Baseline B: metadata-weighted TF-IDF repeats title, section heading and risk-domain text during indexing while leaving cited evidence unchanged.
- Baseline C: BM25-style retrieval adds length-normalised lexical scoring.
- Baseline D: hybrid lexical retrieval fuses metadata-weighted TF-IDF and BM25 scores.
- Baseline E: text-only query decomposition plus diversified reranking splits likely multi-evidence questions and avoids duplicate sections.

## No paid APIs

All methods are deterministic and local. They do not call external LLMs or require embedding model downloads.
