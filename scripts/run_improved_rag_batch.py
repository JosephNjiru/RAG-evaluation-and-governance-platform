"""Run the improved Stage 4 RAG batch without replacing Baseline A."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_retrieval_ablation import run_retrieval_ablation


def run_improved_rag_batch(root: Path = ROOT) -> dict[str, object]:
    if not (root / "outputs/evaluation/retrieval_ablation_by_question_type.csv").exists():
        run_retrieval_ablation(root)
    summary = pd.read_csv(root / "outputs/evaluation/retrieval_ablation_by_question_type.csv")
    original = _row(summary, "baseline_a_tfidf", "overall")
    improved = _row(summary, "baseline_e_decomposition_diversified", "overall")
    original_multi = _row(summary, "baseline_a_tfidf", "multi_hop")
    improved_multi = _row(summary, "baseline_e_decomposition_diversified", "multi_hop")
    report = "\n".join(
        [
            "# Stage 4 improved baseline report",
            "",
            "The original TF-IDF baseline is preserved as Baseline A.",
            "",
            f"- Baseline A overall pass rate: {original['overall_pass_rate']:.3f}",
            f"- Baseline A multi-hop pass rate: {original_multi['overall_pass_rate']:.3f}",
            f"- Improved Baseline E overall pass rate: {improved['overall_pass_rate']:.3f}",
            f"- Improved Baseline E multi-hop pass rate: {improved_multi['overall_pass_rate']:.3f}",
            "",
            "The improved method uses text-only query intent, query decomposition, hybrid lexical scoring and diversified reranking. It does not use the evidence map during retrieval or generation.",
            "",
            "The comparison remains a local synthetic-corpus result and does not remove the need for human review.",
            "",
        ]
    )
    report_path = root / "outputs/reports/stage_4_improved_baseline_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return {
        "original_overall": float(original["overall_pass_rate"]),
        "improved_overall": float(improved["overall_pass_rate"]),
        "original_multi_hop": float(original_multi["overall_pass_rate"]),
        "improved_multi_hop": float(improved_multi["overall_pass_rate"]),
    }


def _row(summary: pd.DataFrame, method: str, question_type: str) -> pd.Series:
    matches = summary[
        (summary["retrieval_method"] == method) & (summary["question_type"] == question_type)
    ]
    if matches.empty:
        raise ValueError(f"Missing summary row for {method} {question_type}")
    return matches.iloc[0]


def main() -> None:
    result = run_improved_rag_batch()
    print("Improved RAG batch complete.")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
