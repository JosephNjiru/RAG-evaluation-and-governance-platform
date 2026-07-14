import json
from pathlib import Path


def test_reproducibility_manifest_schema_when_present() -> None:
    path = Path("outputs/reports/reproducibility_manifest.json")
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert "package_version" in manifest
    assert "corpus_file_hashes" in manifest
    assert "output_file_hashes" in manifest
    assert manifest["evaluation_method"] == "rule_based_evidence_map_evaluation"
