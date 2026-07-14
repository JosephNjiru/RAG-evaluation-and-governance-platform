# Traceability matrix

| Research question | Project component | Data artefact | Metric | Output file | Governance artefact |
| --- | --- | --- | --- | --- | --- |
| Does retrieval find expected evidence? | Retrieval metrics | Evidence map | Recall at k, hit rate, MRR | `outputs/evaluation/rag_evaluation_results.parquet` | AI risk register |
| Are citations supported? | Citation metrics | Evidence map | Citation precision and recall | `outputs/evaluation/rag_evaluation_results.parquet` | Evaluation card |
| Does improved retrieval reduce multi-hop weakness? | Retrieval ablation | Question bank and evidence map | Multi-hop pass rate | `outputs/evaluation/retrieval_ablation_by_question_type.csv` | Baseline comparison report |
| Does the system refuse unsupported requests? | Refusal metrics | Refusal questions | Correct refusal rate | `outputs/reports/stage_3_evaluation_report.md` | Human review protocol |
| Are high-risk records routed to review? | Rule-based judge | Question bank | Human review match | `outputs/evaluation/rag_evaluation_summary.csv` | Human review protocol |
| Are challenge questions handled after improvement? | Challenge evaluation | Challenge set | Overall and type-level pass rates | `outputs/reports/challenge_set_report.md` | Incident response playbook |
