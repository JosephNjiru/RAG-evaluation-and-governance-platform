# Evaluation leakage controls

The evidence map is a ground-truth evaluation asset. It must not influence retrieval, prompt construction, generation or citation selection.

## Allowed use

- Metric calculation.
- Rule-based evaluation.
- Reports and dashboard summaries.
- Challenge and ablation scoring after answers are generated.

## Disallowed use

- Retrieval modules.
- Reranking modules.
- Generation modules.
- Prompt construction.
- Improved RAG batch generation.
- Citation selection.

## Test coverage

`tests/test_no_evaluation_leakage.py` scans retrieval and generation modules for evidence-map references and verifies that generation can run without loading `evidence_map.csv`.
