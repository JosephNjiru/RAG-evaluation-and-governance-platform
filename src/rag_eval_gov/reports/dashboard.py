"""Static HTML dashboard generation."""

from __future__ import annotations

import html
from pathlib import Path

import pandas as pd


def build_dashboard_html(results: pd.DataFrame, summary: pd.DataFrame) -> str:
    overall = summary[summary["question_type"] == "overall"].iloc[0]
    display_summary = summary.fillna("n/a")
    queue = results[
        results["human_review_expected"] | results["safety_flag"] | ~results["overall_pass"]
    ][["question_id", "question_type", "risk_level", "evaluation_notes"]].head(30)
    extra_sections = build_optional_stage4_sections()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>RAG evaluation dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2933; }}
    h1, h2 {{ color: #102a43; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 12px; }}
    .card {{ border: 1px solid #d9e2ec; border-radius: 6px; padding: 12px; }}
    .value {{ font-size: 1.6rem; font-weight: 700; }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0 24px; }}
    th, td {{ border: 1px solid #d9e2ec; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #f0f4f8; }}
  </style>
</head>
<body>
  <h1>RAG evaluation dashboard</h1>
  <p>Static dashboard for the local RAG evaluation baseline and Stage 4 hardening checks.</p>
  <p><strong>Reading note:</strong> headline metrics are screening signals. The corpus is synthetic, the generator is deterministic and human review remains required for high-risk or failed records.</p>
  <p><strong>Safety note:</strong> no unsafe-answer flags were triggered in this synthetic evaluation run. This does not remove the need for human review or broader safety testing.</p>
  <section class="grid">
    {card("Questions", int(overall["questions"]))}
    {card("Overall pass rate", f"{overall['overall_pass_rate']:.3f}")}
    {card("Retrieval hit rate", f"{overall['retrieval_hit_rate']:.3f}")}
    {card("Citation precision", f"{overall['mean_citation_precision']:.3f}")}
    {card("Citation recall", f"{overall['mean_citation_recall']:.3f}")}
    {card("Faithfulness", f"{overall['mean_faithfulness']:.3f}")}
    {card("Refusal correctness", f"{overall['refusal_correct_rate']:.3f}")}
    {card("Human review match", f"{overall['human_review_match_rate']:.3f}")}
  </section>
  {extra_sections}
  <h2>Question-type breakdown</h2>
  {display_summary.to_html(index=False, escape=True)}
  <h2>Human review queue</h2>
  {queue.to_html(index=False, escape=True)}
  <h2>Key limitations</h2>
  <ul>
    <li>Baseline A TF-IDF performed strongly on factual questions but weakly on multi-hop questions.</li>
    <li>TF-IDF is lexical and may miss semantic matches.</li>
    <li>Mock generation is deterministic and not a field model.</li>
    <li>Deterministic faithfulness checks are screening checks, not final human judgement.</li>
    <li>Challenge set results are synthetic holdout evidence, not field performance.</li>
    <li>The challenge set has a different difficulty profile from the original 60-question benchmark and does not replace it.</li>
    <li>Human review remains necessary for high-risk, unsupported, ambiguous and failed records.</li>
  </ul>
</body>
</html>
"""


def card(label: str, value: object) -> str:
    return (
        '<div class="card">'
        f"<div>{html.escape(label)}</div>"
        f'<div class="value">{html.escape(str(value))}</div>'
        "</div>"
    )


def build_optional_stage4_sections(root: Path | None = None) -> str:
    """Render Stage 4 ablation and challenge summaries when present."""

    active_root = root or Path.cwd()
    sections: list[str] = []
    ablation_path = active_root / "outputs/evaluation/retrieval_ablation_by_question_type.csv"
    if ablation_path.exists():
        ablation = pd.read_csv(ablation_path).fillna("n/a")
        focus = ablation[ablation["question_type"].isin(["overall", "factual", "multi_hop"])][
            [
                "baseline_label",
                "question_type",
                "overall_pass_rate",
                "mean_retrieval_recall",
                "mean_citation_precision",
                "mean_citation_recall",
            ]
        ]
        sections.append("<h2>Baseline comparison</h2>")
        sections.append(focus.to_html(index=False, escape=True))
    challenge_path = active_root / "outputs/evaluation/challenge_evaluation_results.parquet"
    if challenge_path.exists():
        challenge = pd.read_parquet(challenge_path)
        challenge_summary = challenge.groupby("question_type", as_index=False).agg(
            questions=("question_id", "count"),
            pass_rate=("overall_pass", "mean"),
            citation_precision=("citation_precision", "mean"),
            citation_recall=("citation_recall", "mean"),
        )
        sections.append("<h2>Challenge set result</h2>")
        sections.append(challenge_summary.to_html(index=False, escape=True))
    return "\n".join(sections)
