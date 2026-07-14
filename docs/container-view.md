# Container view

The project can run directly through Python commands or through Docker Compose.

## Python package

`rag_eval_gov` contains ingestion, retrieval, generation, evaluation, judging, reporting and API modules.

## Script layer

Scripts create assets in a clear order:

1. Validate Stage 1 assets.
2. Build the TF-IDF vector index.
3. Run the deterministic RAG baseline.
4. Evaluate generated answers.
5. Build the static dashboard.
6. Run quality checks.

## Docker services

- `api`: serves the local FastAPI endpoints on port 8000.
- `dashboard`: serves the static dashboard on port 8080.

Both services use local files and do not require API keys.
