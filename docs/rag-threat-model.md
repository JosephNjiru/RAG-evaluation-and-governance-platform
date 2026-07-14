# RAG threat model

## Scope

This threat model covers the local RAG evaluation platform, including user input, retrieved evidence, deterministic answer generation, evaluation outputs, API endpoints, Docker defaults and release artefacts.

## Threats covered

| Threat | Description | Main control |
| --- | --- | --- |
| Direct prompt injection | User asks the system to ignore rules or reveal hidden instructions. | Input security flags and refusal. |
| Indirect prompt injection | Retrieved text contains instructions aimed at the model. | Context security flags and prompt separation. |
| Malicious quoted instructions | User quotes unsafe instructions and asks the system to follow them. | Input and context screening. |
| Sensitive information disclosure | User asks for secrets, private identifiers or restricted information. | Input security and secret scanning. |
| Secret leakage | Secrets appear in source, outputs or logs. | Secret scanner and quality scan checks. |
| Unsupported escalation advice | User asks to bypass review or approve unsupported action. | Input and output security checks. |
| Wrong or fabricated citation | Answer cites a section not retrieved or unsupported. | Output security and citation metrics. |
| System prompt leakage | User asks for hidden prompts or instructions. | Input security refusal. |
| Vector or embedding manipulation | Corpus or query terms manipulate lexical retrieval. | Context checks, challenge tests and human review. |
| Data poisoning in corpus | Source documents contain malicious or misleading text. | Corpus review, context security and release checks. |
| Unsafe output handling | Generated answer bypasses authorisation or review. | Output security checks. |
| Unbounded input size | Large input exhausts local resources. | API request-size limit and input length checks. |
| Overconfidence | Answer overstates certainty beyond evidence. | Output confidence language checks. |

## Residual risk

The controls are deterministic and pattern-based. They can miss novel attacks, subtle data poisoning and context-dependent safety issues. Human review remains necessary for high-risk, unsupported, ambiguous and failed records.
