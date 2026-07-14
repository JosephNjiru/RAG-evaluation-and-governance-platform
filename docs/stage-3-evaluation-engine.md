# Stage 3 evaluation engine

Stage 3 evaluates the controlled local RAG pipeline produced in Stage 2.

The evaluation engine reads the question bank, reference answers, evidence map, answer records, retrieval results and strengthened rubrics. It produces per-question evaluation records, a summary table, a Markdown report and a static HTML dashboard.

The default judge is deterministic and rule-based. It checks retrieval against expected evidence sections, checks citations against the evidence map, screens answer faithfulness using overlap with cited evidence and reference answers, evaluates refusal behaviour, checks safety flags and applies rubric scores.

The system is designed for auditability. Each question-level result keeps the expected documents, expected sections, retrieved sections, citation labels, metric scores, rubric scores and evaluation notes.

No paid API calls are used.
