from pathlib import Path

from rag_eval_gov.governance.risk_taxonomy import load_risk_taxonomy

ROOT = Path(__file__).resolve().parents[1]


def test_required_risks_are_present() -> None:
    config = load_risk_taxonomy(ROOT / "configs/risk_taxonomy.yaml")
    names = {risk.risk_name for risk in config.risks}
    assert "prompt injection susceptibility" in names
    assert "human review bypass" in names
    assert "unsupported answer" in names
