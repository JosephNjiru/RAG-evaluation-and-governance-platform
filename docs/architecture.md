# Architecture

The RAG Evaluation and Governance Platform is a local-first reference project for evaluating retrieval-augmented generation systems. It separates the corpus, RAG baseline, evaluation engine and governance artefacts so each part can be inspected and tested.

## Main components

- Corpus and evaluation design: synthetic Markdown policy documents, question bank, reference answers, evidence map, refusal questions and adversarial questions.
- RAG baseline: Markdown loader, section-aware chunker, TF-IDF vector index, retriever, deterministic mock generator and citation formatter.
- Evaluation engine: retrieval metrics, citation checks, deterministic faithfulness screening, refusal metrics, safety checks, rubric scoring and rule-based judging.
- Governance layer: risk register, human review protocol, system card, data card, model card, evaluation card and incident response playbook.
- API and dashboard: FastAPI service for local answer and evaluation access, plus a static dashboard generated from Stage 3 outputs.
- CI and release checks: validation scripts, tests, ruff, quality scan, Markdown link check and Docker Compose config check.

## Design principle

The system begins with evaluation assets rather than a chatbot interface. That keeps the quality target visible before answer generation is added. The Stage 3 result is also preserved honestly: the TF-IDF baseline works well for factual questions but performs poorly on multi-hop questions.
