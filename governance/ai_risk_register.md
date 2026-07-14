# AI risk register

| Risk | Description | Detection signal | Control |
| --- | --- | --- | --- |
| Unsupported answer | Answer claims are not supported by evidence. | Faithfulness and citation checks fail. | Refuse or route to review. |
| Wrong citation | Citation points to an irrelevant section. | Citation precision below target. | Citation support gate. |
| Missed retrieval | Expected evidence is not retrieved. | Retrieval recall below target. | Improve chunking and retrieval. |
| Multi-hop retrieval failure | Required evidence spans multiple sections and is not assembled. | Multi-hop pass rate is low. | Add multi-stage retrieval or query expansion later. |
| Prompt injection | Question attempts to override evidence-only rules. | Adversarial question type or unsafe compliance. | Refuse and route to review. |
| Sensitive information exposure | Answer reveals private or secret information. | Sensitive information flag. | Stop response and review corpus controls. |
| Stale corpus | Source documents are outdated. | Version or date review fails. | Corpus update and evidence map review. |
| Judge bias | Optional judge favours style or unsupported fluency. | Calibration disagreement. | Human calibration and rubric review. |
| Human review bypass | A record needing review is not flagged. | Review match failure. | Review protocol gate. |
| Overconfidence | Answer confidence exceeds evidence support. | Low support with high confidence. | Confidence label rule. |
| Misuse of evaluation scores | Scores are treated as field performance claims. | Release review finding. | Limitations and approval checklist. |
