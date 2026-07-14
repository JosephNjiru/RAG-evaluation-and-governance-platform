.PHONY: install build-assets validate index build-index rag run-rag evaluate ablation improved challenge dashboard manifest security security-smoke figures smoke-api test lint format-check quality-scan all

install:
	python -m pip install uv
	python -m uv sync

build-assets:
	python -m uv run python scripts/build_stage1_assets.py

validate:
	python -m uv run python scripts/validate_stage1_assets.py

index:
	python -m uv run python scripts/build_vector_index.py

build-index:
	python -m uv run python scripts/build_vector_index.py

rag:
	python -m uv run python scripts/run_rag_batch.py

run-rag:
	python -m uv run python scripts/run_rag_batch.py

evaluate:
	python -m uv run python scripts/evaluate_rag_outputs.py

ablation:
	python -m uv run python scripts/run_retrieval_ablation.py

improved:
	python -m uv run python scripts/run_improved_rag_batch.py

challenge:
	python -m uv run python scripts/evaluate_challenge_set.py

dashboard:
	python -m uv run python scripts/build_evaluation_dashboard.py
	python -m uv run python dashboard/build_dashboard.py

manifest:
	python -m uv run python scripts/build_reproducibility_manifest.py

smoke-api:
	python -m uv run python scripts/smoke_test_api.py

security:
	python -m uv run python scripts/run_security_checks.py

security-smoke:
	python -m uv run python scripts/security_smoke_test.py

figures:
	python -m uv run python scripts/generate_publication_figures.py
	python -m uv run python scripts/generate_slide_figures.py
	python -m uv run python scripts/generate_figure_catalog.py
	python -m uv run python scripts/generate_visual_abstract.py

test:
	python -m uv run pytest

lint:
	python -m uv run ruff check .

format-check:
	python -m uv run ruff format --check .

quality-scan:
	python -m uv run python scripts/quality_scan.py

all: build-assets validate index rag evaluate ablation improved challenge dashboard manifest security quality-scan smoke-api security-smoke figures test lint format-check
