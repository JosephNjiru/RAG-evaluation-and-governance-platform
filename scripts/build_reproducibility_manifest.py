"""Build a JSON reproducibility manifest."""
# ruff: noqa: E402

from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime
from pathlib import Path

import rag_eval_gov

ROOT = Path(__file__).resolve().parents[1]

COMMAND_SEQUENCE = [
    "python -m uv run python scripts/validate_stage1_assets.py",
    "python -m uv run python scripts/build_vector_index.py",
    "python -m uv run python scripts/run_rag_batch.py",
    "python -m uv run python scripts/evaluate_rag_outputs.py",
    "python -m uv run python scripts/run_retrieval_ablation.py",
    "python -m uv run python scripts/run_improved_rag_batch.py",
    "python -m uv run python scripts/evaluate_challenge_set.py",
    "python -m uv run python scripts/build_evaluation_dashboard.py",
    "python -m uv run python scripts/build_reproducibility_manifest.py",
]


def build_reproducibility_manifest(root: Path = ROOT) -> dict[str, object]:
    manifest = {
        "package_version": getattr(rag_eval_gov, "__version__", "0.4.0"),
        "python_version": sys.version,
        "platform": platform.platform(),
        "command_sequence": COMMAND_SEQUENCE,
        "corpus_file_hashes": _hash_glob(root / "data/corpus/source_documents", "*.md"),
        "question_bank_hash": _sha256(root / "data/evaluation/question_bank.csv"),
        "reference_answer_hash": _sha256(root / "data/evaluation/reference_answers.csv"),
        "evidence_map_hash": _sha256(root / "data/evaluation/evidence_map.csv"),
        "config_hashes": _hash_glob(root / "configs", "*.yaml"),
        "retrieval_method": "Baseline A through Baseline E ablation; improved uses Baseline E",
        "evaluation_method": "rule_based_evidence_map_evaluation",
        "output_file_hashes": _hash_outputs(root),
        "timestamp": datetime.utcnow().isoformat(),
        "random_seed": None,
    }
    output_path = root / "outputs/reports/reproducibility_manifest.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def _hash_glob(directory: Path, pattern: str) -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)).replace("\\", "/"): _sha256(path)
        for path in sorted(directory.glob(pattern))
    }


def _hash_outputs(root: Path) -> dict[str, str]:
    paths = [
        root / "outputs/answers/rag_answers.parquet",
        root / "outputs/answers/improved_rag_answers.parquet",
        root / "outputs/evaluation/rag_evaluation_results.parquet",
        root / "outputs/evaluation/retrieval_ablation_results.csv",
        root / "outputs/evaluation/challenge_evaluation_results.parquet",
        root / "outputs/reports/rag_evaluation_dashboard.html",
        root / "outputs/reports/baseline_comparison_report.md",
        root / "outputs/reports/challenge_set_report.md",
    ]
    return {
        str(path.relative_to(root)).replace("\\", "/"): _sha256(path)
        for path in paths
        if path.exists()
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest = build_reproducibility_manifest()
    print("Reproducibility manifest written.")
    print(f"output_hashes: {len(manifest['output_file_hashes'])}")


if __name__ == "__main__":
    main()
