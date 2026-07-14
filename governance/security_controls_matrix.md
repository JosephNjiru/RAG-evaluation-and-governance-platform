# Security controls matrix

| Threat | Control | Implementation file | Test file | Output evidence | Residual risk | Human review requirement |
| --- | --- | --- | --- | --- | --- | --- |
| Prompt injection | Input and context security checks | `src/rag_eval_gov/security/input_security.py`, `context_security.py` | `tests/test_input_security.py`, `tests/test_context_security.py` | `outputs/security/security_check_results.csv` | Pattern checks are incomplete. | Yes, when flagged. |
| Sensitive information exposure | Secret scanner and output checks | `secret_scanner.py`, `output_security.py` | `tests/test_secret_scanner.py`, `tests/test_output_security.py` | `outputs/security/security_events.jsonl` | Scanning can miss unusual secrets. | Yes, for confirmed exposure. |
| Unsafe output handling | Output security checks | `output_security.py` | `tests/test_output_security.py` | `outputs/reports/security_assurance_report.md` | Human judgement is still needed. | Yes. |
| API misuse | Request-size limit and schema validation | `src/rag_eval_gov/api/main.py` | `tests/test_security_smoke.py` | API smoke test output | Local defaults are not enterprise access control. | Yes, for unsafe requests. |
| Docker runtime risk | Non-root runtime and ignored secrets | `Dockerfile`, `.dockerignore` | Compose config and runtime check | Docker command output | Host and registry controls are out of scope. | No direct review gate. |
