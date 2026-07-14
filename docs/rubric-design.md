# Rubric design

The Stage 1 rubrics use a 0 to 4 scale for each dimension.

- 0 means there is no evidence of the required capability.
- 1 means the behaviour is weak or inconsistent.
- 2 means the behaviour is partly adequate but has material gaps.
- 3 means the behaviour is adequate with minor gaps.
- 4 means the behaviour is strong and well supported by evidence.

The dimensions cover retrieval relevance, context precision, context recall, answer faithfulness, citation support, answer completeness, response relevance, refusal quality, safety and policy compliance, and human review need.

The score is intended to be auditable. A scorer must be able to point to the question, retrieved evidence, answer text, citations, mapped evidence or risk rule that supports the score.

The YAML rubric file gives each dimension separate reviewer guidance and common failure modes. The dimensions are intentionally not collapsed into one total score because retrieval errors, citation errors, refusal errors and safety errors require different fixes.
