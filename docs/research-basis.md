# Research basis

RAG evaluation needs to assess retrieval and generation together. A system can retrieve weak evidence and still generate a fluent answer, or retrieve strong evidence and misuse it. This project therefore treats retrieval quality, answer faithfulness, citation support, refusal behaviour, safety risk and human review need as separate but connected signals.

RAGAS is relevant because it frames evaluation around context quality and response quality. Its documented metric set includes context precision, context recall, faithfulness, answer relevancy, context entity recall and noise sensitivity.

ARES is relevant because it treats automated RAG evaluation as a measurement problem. It evaluates context relevance, answer faithfulness and answer relevance, and uses synthetic training data with a small set of human annotations through prediction-powered inference.

NIST AI RMF is relevant because it frames AI risk management around trustworthy design, development, use and evaluation. The NIST Generative AI Profile adds generative AI risks such as content provenance, testing, information integrity and incident handling.

OWASP guidance is relevant because RAG systems can fail through prompt injection, sensitive information disclosure, data and model poisoning, excessive agency, system prompt leakage, vector and embedding weaknesses, misinformation and unbounded consumption.

LLM-as-judge methods such as G-Eval and Prometheus support rubric-based scalable evaluation, but they need calibration, consistency checks, bias controls and clear limits. Stage 1 therefore defines rubrics before any optional judge is added.

## References

- Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2023). RAGAS: Automated evaluation of retrieval augmented generation. arXiv. https://arxiv.org/abs/2309.15217
- RAGAS documentation. Metrics for RAG evaluation. https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
- Saad-Falcon, J., Khattab, O., Potts, C., & Zaharia, M. (2024). ARES: An automated evaluation framework for retrieval-augmented generation systems. NAACL. https://aclanthology.org/2024.naacl-long.20/
- National Institute of Standards and Technology. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). https://www.nist.gov/itl/ai-risk-management-framework
- National Institute of Standards and Technology. (2024). Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Foundation. (2025). OWASP Top 10 for Large Language Model Applications. https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., & Zhu, C. (2023). G-Eval: NLG evaluation using GPT-4 with better human alignment. arXiv. https://arxiv.org/abs/2303.16634
- Kim, S., Shin, J., Cho, Y., Jang, J., Longpre, S., et al. (2023). Prometheus: Inducing fine-grained evaluation capability in language models. arXiv. https://arxiv.org/abs/2310.08491

## References to verify before publication

Before public release, verify final venue details and author ordering for arXiv papers and any survey literature added in later stages. Keep this section until Stage 4 release review is complete.
