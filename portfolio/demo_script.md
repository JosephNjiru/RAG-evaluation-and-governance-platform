# Demo script

## 1. Build and validate assets

```bash
python -m uv run python scripts/validate_stage1_assets.py
```

## 2. Build the vector index

```bash
python -m uv run python scripts/build_vector_index.py
```

## 3. Run the RAG baseline

```bash
python -m uv run python scripts/run_rag_batch.py
```

## 4. Evaluate outputs

```bash
python -m uv run python scripts/evaluate_rag_outputs.py
```

## 5. Build and open the dashboard

```bash
python -m uv run python scripts/build_evaluation_dashboard.py
python -m uv run python dashboard/build_dashboard.py
```

Open `dashboard/index.html`.

## 6. Inspect the multi-hop weakness

Review the question-type breakdown and compare factual performance with multi-hop performance.

## 7. Inspect governance artefacts

Read `governance/evaluation_card.md`, `governance/ai_risk_register.md` and `governance/human_review_protocol.md`.
