# Security controls matrix

| Threat | Control | Implementation file | Test file | Output evidence | Residual risk | Human review |
| --- | --- | --- | --- | --- | --- | --- |
| Direct prompt injection | Input security flags and refusal | `src/rag_eval_gov/security/input_security.py` | `tests/test_input_security.py` | `outputs/security/security_check_results.csv` | Pattern checks can miss novel attacks. | Required for flagged requests. |
| Indirect prompt injection | Context security checks | `src/rag_eval_gov/security/context_security.py` | `tests/test_context_security.py` | `outputs/security/security_events.jsonl` | Malicious text can be subtle. | Required when context is flagged. |
| Secret leakage | Secret scanner | `src/rag_eval_gov/security/secret_scanner.py` | `tests/test_secret_scanner.py` | `outputs/reports/security_assurance_report.md` | False positives and misses remain possible. | Required for confirmed findings. |
| Unsafe output handling | Output security checks | `src/rag_eval_gov/security/output_security.py` | `tests/test_output_security.py` | `outputs/security/security_check_results.csv` | Screening is not expert judgement. | Required for high-risk outputs. |
| API misuse | Size limit, schemas and safe errors | `src/rag_eval_gov/api/main.py` | `tests/test_security_smoke.py` | `scripts/security_smoke_test.py` output | Local defaults are not full access control. | Required for unsafe requests. |
| Citation misuse | Citation validation | `src/rag_eval_gov/security/output_security.py` | `tests/test_output_security.py` | Evaluation and security reports | Retrieved context can still be incomplete. | Required for failed citations. |
| Docker runtime risk | Non-root runtime and ignored secrets | `Dockerfile`, `.dockerignore` | Docker Compose check | Docker command output | Environment-specific review remains needed. | Not applicable. |
