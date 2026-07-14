# Project brief

RAG Evaluation and Governance Platform is a local-first reference project for evaluating retrieval-augmented generation systems. It assesses retrieval quality, answer faithfulness, citation support, refusal behaviour, safety checks, human review needs and governance readiness.

The project uses a synthetic corpus, 60-question evaluation set, TF-IDF retrieval baseline, deterministic mock generation, rule-based evaluation, governance artefacts, FastAPI endpoints, Docker support and CI checks.

The most useful Stage 3 finding is that the baseline performs well on factual questions but poorly on multi-hop evidence assembly. Stage 4 adds an ablation layer and improves multi-hop pass rate from 0.100 to 0.200, while preserving the weak original result.

The visual layer adds publication figures, slide assets, web assets, a visual abstract and a figure catalogue. These assets are generated from the same validated evidence outputs.
