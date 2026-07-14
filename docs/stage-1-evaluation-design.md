# Stage 1 evaluation design

Stage 1 begins with the evaluation dataset and rubrics rather than a chatbot because a RAG system needs a clear test target before retrieval or generation choices are meaningful.

The foundation separates five concerns:

1. What the corpus says.
2. What questions are supported by the corpus.
3. Which source sections support each answer.
4. Which questions should be refused or reviewed.
5. How answer quality and risk will be scored.

This design makes later stages auditable. Stage 2 can build retrieval and answer generation against known evidence requirements. Stage 3 can evaluate retrieval quality, answer faithfulness, citation support and refusal behaviour without relying only on whether an answer sounds plausible.
