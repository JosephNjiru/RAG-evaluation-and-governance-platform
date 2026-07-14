from rag_eval_gov.security.secret_scanner import scan_text_for_secrets


def test_secret_scanner_flags_api_key_assignment() -> None:
    sample = "API" + "_KEY='sk_test_1234567890abcdef'"
    findings = scan_text_for_secrets(sample)
    assert findings
    assert findings[0].finding_type == "api_key_assignment"
