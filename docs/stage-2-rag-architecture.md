# Stage 2 RAG architecture

Stage 2 implements a local-first RAG pipeline for controlled evaluation.

The pipeline has five steps:

1. Load the synthetic Markdown corpus and preserve document metadata.
2. Chunk documents by section, with a word-window fallback for longer sections.
3. Build a local TF-IDF vector index.
4. Retrieve top-k source-linked chunks for each question.
5. Generate deterministic structured answer records with citations or refusal.

The default generation mode is a deterministic mock generator. It is not intended to simulate a full LLM. Its purpose is to create stable outputs for evaluation, testing and governance checks.

No paid API calls are used in Stage 2.
