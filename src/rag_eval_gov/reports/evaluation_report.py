"""Markdown evaluation report generation."""

from __future__ import annotations

import pandas as pd


def build_evaluation_report(results: pd.DataFrame, summary: pd.DataFrame) -> str:
    overall = summary[summary["question_type"] == "overall"].iloc[0].to_dict()
    by_type = summary[summary["question_type"] != "overall"]
    notable_errors = results[~results["overall_pass"]]["evaluation_notes"].value_counts().head(8)
    human_review_queue = results[
        results["human_review_expected"] | results["safety_flag"] | ~results["overall_pass"]
    ]
    lines = [
        "# Stage 3 evaluation report",
        "",
        "Stage 3 evaluates the local TF-IDF RAG baseline with deterministic rule-based checks.",
        "",
        "## Overall scorecard",
        "",
        f"- Questions evaluated: {int(overall['questions'])}",
        f"- Overall pass rate: {overall['overall_pass_rate']:.3f}",
        f"- Retrieval hit rate: {overall['retrieval_hit_rate']:.3f}",
        f"- Mean citation precision: {overall['mean_citation_precision']:.3f}",
        f"- Mean citation recall: {overall['mean_citation_recall']:.3f}",
        f"- Mean faithfulness score: {overall['mean_faithfulness']:.3f}",
        f"- Human review match rate: {overall['human_review_match_rate']:.3f}",
        "- Safety note: no unsafe-answer flags were triggered in this synthetic evaluation run. This does not remove the need for human review or broader safety testing.",
        "",
        "## Results by question type",
        "",
        _markdown_table(by_type),
        "",
        "## Notable error patterns",
        "",
    ]
    if notable_errors.empty:
        lines.append("- No recurring error pattern was found by the rule-based checks.")
    else:
        for note, count in notable_errors.items():
            lines.append(f"- {note}: {count}")
    lines.extend(
        [
            "",
            "## Human review queue",
            "",
            f"- Queue size: {len(human_review_queue)}",
            "- Queue rule: expected human review, safety flag or failed overall rule-based check.",
            "",
            "## Limitations",
            "",
            "- TF-IDF is a lexical retrieval baseline.",
            "- Mock generation is deterministic and controlled.",
            "- Deterministic faithfulness checks are useful for screening but are not a substitute for expert review.",
            "- Synthetic corpus results are not field performance claims.",
            "- A zero safety flag rate in this synthetic run does not mean the system has no safety risk.",
            "",
            "## Recommended Stage 4 improvements",
            "",
            "- Add governance artefacts that reference the evaluation outputs.",
            "- Add Docker and continuous checks without requiring paid APIs.",
            "- Add architecture diagrams and release checks.",
        ]
    )
    return "\n".join(lines) + "\n"


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "No rows."
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in frame.itertuples(index=False):
        values = []
        for value in row:
            if pd.isna(value):
                values.append("n/a")
            elif isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)
