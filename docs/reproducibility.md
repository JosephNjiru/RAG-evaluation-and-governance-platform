# Reproducibility

The project is designed to regenerate Stage 1 to Stage 3 outputs from local files.

## Environment

- Python 3.12 or higher.
- `uv` for dependency management.
- No paid API keys are required.

## Full local regeneration

```bash
python -m pip install uv
python -m uv sync
python -m uv run python scripts/validate_stage1_assets.py
python -m uv run python scripts/build_vector_index.py
python -m uv run python scripts/run_rag_batch.py
python -m uv run python scripts/evaluate_rag_outputs.py
python -m uv run python scripts/run_retrieval_ablation.py
python -m uv run python scripts/run_improved_rag_batch.py
python -m uv run python scripts/evaluate_challenge_set.py
python -m uv run python scripts/build_evaluation_dashboard.py
python -m uv run python scripts/build_reproducibility_manifest.py
python -m uv run python dashboard/build_dashboard.py
python -m uv run pytest
python -m uv run ruff check .
python -m uv run ruff format --check .
```

## Generated outputs

The main generated outputs are answer records, retrieval records, evaluation tables, Markdown reports and static HTML dashboard files. The synthetic corpus and evaluation assets are stored in source-controlled data folders.

The reproducibility manifest is written to `outputs/reports/reproducibility_manifest.json` and records file hashes, command sequence, retrieval method, evaluation method and platform details.
