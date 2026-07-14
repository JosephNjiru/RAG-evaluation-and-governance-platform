from scripts.security_smoke_test import security_smoke_test


def test_security_smoke_test_passes() -> None:
    result = security_smoke_test()
    assert result["health"] == "ok"
    assert result["injection_action"] == "refuse"
    assert result["secret_action"] == "refuse"
