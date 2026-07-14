FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

RUN python -m pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./
COPY configs ./configs
COPY data ./data
COPY docs ./docs
COPY governance ./governance
COPY outputs ./outputs
COPY scripts ./scripts
COPY src ./src
COPY dashboard ./dashboard

RUN python -m uv sync --frozen
RUN python -m uv run python scripts/validate_stage1_assets.py \
    && python -m uv run python scripts/build_vector_index.py \
    && python -m uv run python scripts/run_rag_batch.py \
    && python -m uv run python scripts/evaluate_rag_outputs.py \
    && python -m uv run python scripts/run_retrieval_ablation.py \
    && python -m uv run python scripts/run_improved_rag_batch.py \
    && python -m uv run python scripts/evaluate_challenge_set.py \
    && python -m uv run python scripts/build_evaluation_dashboard.py \
    && python -m uv run python dashboard/build_dashboard.py \
    && python -m uv run python scripts/build_reproducibility_manifest.py \
    && python -m uv run python scripts/run_security_checks.py \
    && python -m uv run python scripts/quality_scan.py

RUN groupadd --system appuser \
    && useradd --system --gid appuser --home-dir /app appuser \
    && chown -R appuser:appuser /app

EXPOSE 8000

USER appuser

CMD ["python", "-m", "uv", "run", "uvicorn", "rag_eval_gov.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
