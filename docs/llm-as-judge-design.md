# LLM-as-judge design

Rule-based judging is the default because Stage 3 must run locally, deterministically and without paid APIs. Rule-based checks are easier to inspect and reproduce.

An optional LLM judge could be added later for cases where deterministic checks are too brittle, such as nuanced faithfulness, answer completeness or policy interpretation. The interface in `src/rag_eval_gov/judging/llm_judge_interface.py` defines input and output schemas but does not call any provider.

An LLM judge would need calibration before use. Calibration should compare judge scores with human-reviewed examples, check consistency across repeated runs, record model and prompt versions, and review disagreement cases.

Known risks include judge bias, inconsistent scoring, cost, closed-model version changes, overconfidence and hidden failure modes. LLM judge scores should not be the only approval signal for high-risk outputs.
