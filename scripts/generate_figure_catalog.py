"""Generate the figure catalogue documentation."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


FIGURES = [
    (
        "Figure 1",
        "System architecture overview",
        "Show the end-to-end platform structure.",
        "figure_01_system_architecture",
        "The platform links corpus, retrieval, evaluation and governance.",
    ),
    (
        "Figure 2",
        "Evaluation lifecycle and data flow",
        "Show question movement through the system.",
        "figure_02_evaluation_lifecycle",
        "A question moves through retrieval, answers, metrics and review.",
    ),
    (
        "Figure 3",
        "Question taxonomy distribution",
        "Show evaluation set design.",
        "figure_03_question_taxonomy",
        "The question set covers supported and unsupported behaviours.",
    ),
    (
        "Figure 4",
        "Baseline comparison",
        "Show ablation results.",
        "figure_04_baseline_comparison",
        "Baseline E modestly improves overall results.",
    ),
    (
        "Figure 5",
        "Factual versus multi-hop performance",
        "Show the key result.",
        "figure_05_factual_vs_multihop",
        "Multi-hop evidence assembly remains weak.",
    ),
    (
        "Figure 6",
        "Citation quality by method",
        "Show citation support.",
        "figure_06_citation_quality",
        "Citation quality follows retrieval quality.",
    ),
    (
        "Figure 7",
        "Retrieval performance by method",
        "Separate retrieval evidence from answer quality.",
        "figure_07_retrieval_performance",
        "Retrieval metrics expose evidence coverage.",
    ),
    (
        "Figure 8",
        "Question-type outcome matrix",
        "Show outcome variation.",
        "figure_08_question_type_outcome_matrix",
        "Question type changes risk and performance.",
    ),
    (
        "Figure 9",
        "Challenge set summary",
        "Show holdout results.",
        "figure_09_challenge_set_summary",
        "Challenge results have a different difficulty profile.",
    ),
    (
        "Figure 10",
        "Human review and governance flow",
        "Show governance connection.",
        "figure_10_human_review_governance_flow",
        "Evaluation feeds human review.",
    ),
    (
        "Figure 11",
        "Risk register summary",
        "Summarise governance risks.",
        "figure_11_risk_register_summary",
        "Key risks require review controls.",
    ),
    (
        "Figure 12",
        "Threats to validity summary",
        "Show method limits.",
        "figure_12_threats_to_validity",
        "Synthetic and lexical limits remain.",
    ),
    (
        "Figure 13",
        "Question difficulty profile",
        "Show challenge difficulty features.",
        "figure_13_question_difficulty_profile",
        "Evidence rows and review needs affect difficulty.",
    ),
    (
        "Figure 14",
        "Error taxonomy distribution",
        "Show failure patterns.",
        "figure_14_error_taxonomy",
        "Failures cluster around evidence and citation support.",
    ),
    (
        "Figure 15",
        "Claim-support screening summary",
        "Show claim support flags.",
        "figure_15_claim_support_summary",
        "Claim checks are screening tools.",
    ),
    (
        "Figure 16",
        "Source-conflict and versioning flow",
        "Show source preference rules.",
        "figure_16_source_conflict_versioning_flow",
        "Source conflict still needs review.",
    ),
]


def generate_figure_catalog(root: Path = ROOT) -> Path:
    rows = [
        "# Figure catalogue",
        "",
        "| ID | Title | Purpose | Audience | Input data | Script | Output files | Interpretation | Use |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for figure_id, title, purpose, stem, interpretation in FIGURES:
        outputs = f"`figures/export/journal/{stem}.pdf`, `{stem}.svg`, `{stem}.png`"
        rows.append(
            f"| {figure_id} | {title} | {purpose} | Technical reviewers, researchers, presentations | Project evidence outputs | `scripts/generate_publication_figures.py` | {outputs} | {interpretation} | journal, slides, README |"
        )
    rows.extend(
        [
            "| Asset 1 | Visual abstract | Communicate problem, method, result and governance contribution. | Technical readers and seminar audiences | Metrics and project design | `scripts/generate_visual_abstract.py` | `figures/export/web/visual_abstract_landscape.png`, `.svg`, `.pdf` | Improvement is modest and limits remain visible. | slides, README, web |",
        ]
    )
    path = root / "docs/figure_catalog.md"
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def main() -> None:
    path = generate_figure_catalog()
    print(f"Figure catalogue written: {path}")


if __name__ == "__main__":
    main()
