# Figure generation notes

## Data sources

- `outputs/evaluation/rag_evaluation_summary.csv`
- `outputs/evaluation/retrieval_ablation_results.csv`
- `outputs/evaluation/retrieval_ablation_by_question_type.csv`
- `outputs/evaluation/challenge_evaluation_results.parquet`
- `outputs/evaluation/question_difficulty_profile.csv`
- `outputs/reports/baseline_comparison_report.md`
- `outputs/security/security_check_results.csv`
- `governance/ai_risk_register.md`
- `docs/threats-to-validity.md`

## Manual assumptions

Risk severity values in Figure 11 are visual summaries for communication, not newly measured empirical probabilities.

## Build order

```bash
python -m uv run python scripts/generate_publication_figures.py
python -m uv run python scripts/generate_slide_figures.py
python -m uv run python scripts/generate_figure_catalog.py
python -m uv run python scripts/generate_visual_abstract.py
```

## Known limitations

The figures communicate validated project outputs, but they do not add new empirical evidence. They should be regenerated after any change to metrics or challenge-set results.
