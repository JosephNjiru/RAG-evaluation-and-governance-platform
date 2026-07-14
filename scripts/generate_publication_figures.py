"""Generate publication-grade project figures."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.figure_utils import (
    PALETTE,
    add_caption,
    annotate_bars,
    apply_style,
    clean_axes,
    draw_box_flow,
    load_ablation_summary,
    load_challenge_results,
    load_question_bank,
    save_all,
)

JOURNAL_DIR = ROOT / "figures/export/journal"
WEB_DIR = ROOT / "figures/export/web"


def generate_publication_figures(root: Path = ROOT) -> list[Path]:
    """Generate all publication and web figures."""

    apply_style()
    outputs: list[Path] = []
    outputs.extend(_figure_01_system_architecture())
    outputs.extend(_figure_02_lifecycle())
    outputs.extend(_figure_03_question_taxonomy())
    outputs.extend(_figure_04_baseline_comparison())
    outputs.extend(_figure_05_factual_vs_multihop())
    outputs.extend(_figure_06_citation_quality())
    outputs.extend(_figure_07_retrieval_performance())
    outputs.extend(_figure_08_outcome_matrix())
    outputs.extend(_figure_09_challenge_summary())
    outputs.extend(_figure_10_governance_flow())
    outputs.extend(_figure_11_risk_summary())
    outputs.extend(_figure_12_validity_summary())
    outputs.extend(_figure_13_difficulty_profile())
    outputs.extend(_figure_14_error_taxonomy())
    outputs.extend(_figure_15_claim_support())
    outputs.extend(_figure_16_source_conflict_flow())
    return outputs


def _save(fig, stem: str, caption: str) -> list[Path]:
    add_caption(fig, caption)
    return save_all(fig, stem, [JOURNAL_DIR, WEB_DIR], vector=True)


def _figure_01_system_architecture() -> list[Path]:
    fig, ax = plt.subplots(figsize=(12, 5.8))
    labels = [
        "Synthetic corpus",
        "Question bank and evidence map",
        "Chunking and retrieval",
        "Mock generation",
        "Evaluation engine",
        "Dashboard, API and governance",
    ]
    draw_box_flow(ax, labels, "Figure 1. System architecture overview")
    return _save(
        fig,
        "figure_01_system_architecture",
        "The platform links corpus design, retrieval, answer generation, evaluation and governance artefacts.",
    )


def _figure_02_lifecycle() -> list[Path]:
    fig, ax = plt.subplots(figsize=(12, 5.8))
    labels = [
        "Corpus",
        "Chunks",
        "Index",
        "Retrieved evidence",
        "Answer and citations",
        "Metrics",
        "Human review",
        "Reports",
    ]
    draw_box_flow(ax, labels, "Figure 2. Evaluation lifecycle and data flow")
    return _save(
        fig,
        "figure_02_evaluation_lifecycle",
        "A question moves from source evidence through retrieval, answer generation, scoring and review.",
    )


def _figure_03_question_taxonomy() -> list[Path]:
    questions = load_question_bank()
    counts = (
        questions["question_label"]
        .value_counts()
        .reindex(["Factual", "Multi-hop", "Ambiguous", "Refusal", "Adversarial"])
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(
        counts.index,
        counts.values,
        color=[
            PALETTE["blue"],
            PALETTE["orange"],
            PALETTE["teal"],
            PALETTE["purple"],
            PALETTE["gold"],
        ],
    )
    annotate_bars(ax, counts.values.tolist(), percent=False)
    ax.set_title("Figure 3. Question taxonomy distribution", loc="left", fontweight="bold")
    ax.set_ylabel("Question count")
    clean_axes(ax)
    return _save(
        fig,
        "figure_03_question_taxonomy",
        "The evaluation set intentionally covers answerable, ambiguous, refusal and adversarial cases.",
    )


def _figure_04_baseline_comparison() -> list[Path]:
    summary = load_ablation_summary()
    overall = summary[summary["question_type"] == "overall"]
    metrics = [
        ("overall_pass_rate", "Overall pass rate"),
        ("mean_citation_precision", "Citation precision"),
        ("mean_citation_recall", "Citation recall"),
        ("mean_retrieval_recall", "Retrieval recall"),
        ("mean_reciprocal_rank", "Mean reciprocal rank"),
    ]
    fig, axes = plt.subplots(1, len(metrics), figsize=(16, 4), sharey=True)
    for ax, (column, title) in zip(axes, metrics, strict=False):
        values = overall[column].fillna(0).tolist()
        ax.bar(overall["method_label"], values, color=PALETTE["blue"])
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=65)
        ax.set_ylim(0, 1.05)
        clean_axes(ax)
    fig.suptitle(
        "Figure 4. Baseline comparison across retrieval methods",
        x=0.02,
        ha="left",
        fontweight="bold",
    )
    return _save(
        fig,
        "figure_04_baseline_comparison",
        "Baseline E modestly improves overall and citation metrics while preserving Baseline A as the reference point.",
    )


def _figure_05_factual_vs_multihop() -> list[Path]:
    summary = load_ablation_summary()
    focus = summary[summary["question_type"].isin(["factual", "multi_hop"])]
    pivot = focus.pivot(index="method_label", columns="question_label", values="overall_pass_rate")
    fig, ax = plt.subplots(figsize=(9, 5.2))
    pivot[["Factual", "Multi-hop"]].plot(
        kind="bar", ax=ax, color=[PALETTE["teal"], PALETTE["orange"]]
    )
    ax.set_title("Figure 5. Factual versus multi-hop performance", loc="left", fontweight="bold")
    ax.set_ylabel("Pass rate")
    ax.set_xlabel("")
    ax.set_ylim(0, 1.1)
    ax.legend(title="")
    clean_axes(ax)
    return _save(
        fig,
        "figure_05_factual_vs_multihop",
        "Factual performance remains strong, while multi-hop evidence assembly remains weak despite modest improvement.",
    )


def _figure_06_citation_quality() -> list[Path]:
    summary = load_ablation_summary()
    overall = summary[summary["question_type"] == "overall"]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    x = range(len(overall))
    width = 0.38
    ax.bar(
        [item - width / 2 for item in x],
        overall["mean_citation_precision"],
        width,
        label="Precision",
        color=PALETTE["blue"],
    )
    ax.bar(
        [item + width / 2 for item in x],
        overall["mean_citation_recall"],
        width,
        label="Recall",
        color=PALETTE["gold"],
    )
    ax.set_xticks(list(x), overall["method_label"], rotation=55, ha="right")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Score")
    ax.set_title("Figure 6. Citation quality by method", loc="left", fontweight="bold")
    ax.legend()
    clean_axes(ax)
    return _save(
        fig,
        "figure_06_citation_quality",
        "Citation quality improves slightly in the improved retrieval run but remains tied to retrieved evidence quality.",
    )


def _figure_07_retrieval_performance() -> list[Path]:
    summary = load_ablation_summary()
    answerable = summary[summary["question_type"].isin(["factual", "multi_hop"])]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for ax, question_type in zip(axes, ["factual", "multi_hop"], strict=False):
        rows = answerable[answerable["question_type"] == question_type]
        ax.plot(rows["method_label"], rows["mean_retrieval_recall"], marker="o", label="Recall")
        ax.plot(rows["method_label"], rows["mean_reciprocal_rank"], marker="s", label="MRR")
        ax.set_title(QUESTION_TITLE[question_type])
        ax.tick_params(axis="x", rotation=60)
        ax.set_ylim(0, 1.05)
        clean_axes(ax)
    axes[0].set_ylabel("Score")
    axes[1].legend()
    fig.suptitle("Figure 7. Retrieval performance by method", x=0.02, ha="left", fontweight="bold")
    return _save(
        fig,
        "figure_07_retrieval_performance",
        "Retrieval recall and rank metrics separate evidence retrieval from answer-side citation results.",
    )


def _figure_08_outcome_matrix() -> list[Path]:
    results = pd.read_parquet(ROOT / "outputs/evaluation/rag_evaluation_results.parquet")
    matrix = results.groupby("question_type").agg(
        overall_pass=("overall_pass", "mean"),
        retrieval_hit=("retrieval_hit", "mean"),
        citation_precision=("citation_precision", "mean"),
        human_review_match=("human_review_match", "mean"),
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    image = ax.imshow(matrix.fillna(1.0).to_numpy(), vmin=0, vmax=1, cmap="viridis")
    ax.set_xticks(
        range(len(matrix.columns)),
        ["Overall pass", "Retrieval hit", "Citation precision", "Review match"],
        rotation=30,
        ha="right",
    )
    ax.set_yticks(
        range(len(matrix.index)), [QUESTION_TITLE.get(item, item) for item in matrix.index]
    )
    ax.set_title("Figure 8. Question-type outcome matrix", loc="left", fontweight="bold")
    fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03)
    return _save(
        fig,
        "figure_08_question_type_outcome_matrix",
        "The outcome matrix makes the multi-hop weakness visible beside otherwise strong refusal and review behaviour.",
    )


def _figure_09_challenge_summary() -> list[Path]:
    challenge = load_challenge_results()
    summary = challenge.groupby("question_type", as_index=False)["overall_pass"].mean()
    summary["label"] = summary["question_type"].map(QUESTION_TITLE)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary["label"], summary["overall_pass"], color=PALETTE["purple"])
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Pass rate")
    ax.set_title("Figure 9. Challenge set summary", loc="left", fontweight="bold")
    clean_axes(ax)
    return _save(
        fig,
        "figure_09_challenge_set_summary",
        "Challenge results are stronger than the main multi-hop benchmark and must be read as a different synthetic holdout profile.",
    )


def _figure_10_governance_flow() -> list[Path]:
    fig, ax = plt.subplots(figsize=(12, 5.8))
    labels = [
        "Question risk",
        "Support check",
        "Refusal check",
        "Safety screen",
        "Human review queue",
        "Governance artefacts",
    ]
    draw_box_flow(ax, labels, "Figure 10. Human review and governance flow")
    return _save(
        fig,
        "figure_10_human_review_governance_flow",
        "Evaluation outputs are connected to human review and governance records rather than treated as standalone scores.",
    )


def _figure_11_risk_summary() -> list[Path]:
    risks = [
        "Unsupported answer",
        "Wrong citation",
        "Missed retrieval",
        "Multi-hop failure",
        "Prompt injection",
        "Sensitive exposure",
        "Stale corpus",
        "Judge bias",
        "Review bypass",
        "Overconfidence",
        "Score misuse",
    ]
    severity = [4, 4, 3, 4, 4, 4, 3, 3, 4, 3, 3]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(risks[::-1], severity[::-1], color=PALETTE["orange"])
    ax.set_xlim(0, 5)
    ax.set_xlabel("Relative governance severity")
    ax.set_title("Figure 11. Risk register summary", loc="left", fontweight="bold")
    clean_axes(ax)
    return _save(
        fig,
        "figure_11_risk_register_summary",
        "The highest governance risks are unsupported answers, wrong citations, prompt injection and review bypass.",
    )


def _figure_12_validity_summary() -> list[Path]:
    limits = [
        "Synthetic corpus",
        "Mock generator",
        "Lexical retrieval",
        "Rule-based judge",
        "Challenge scope",
        "Human review need",
    ]
    importance = [5, 4, 5, 4, 3, 5]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(limits, importance, color=PALETTE["grey"])
    ax.set_ylim(0, 5.5)
    ax.set_ylabel("Methodological importance")
    ax.set_title("Figure 12. Threats to validity summary", loc="left", fontweight="bold")
    ax.tick_params(axis="x", rotation=30)
    clean_axes(ax)
    return _save(
        fig,
        "figure_12_threats_to_validity",
        "The main limits are synthetic data, lexical retrieval and the need for human review.",
    )


def _figure_13_difficulty_profile() -> list[Path]:
    profile = pd.read_csv(ROOT / "outputs/evaluation/question_difficulty_profile.csv")
    summary = profile.groupby("question_type", as_index=False).agg(
        evidence_rows=("expected_evidence_rows", "mean"),
        human_review=("requires_human_review", "mean"),
    )
    summary["label"] = summary["question_type"].map(QUESTION_TITLE)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(summary["evidence_rows"], summary["human_review"], s=140, color=PALETTE["teal"])
    for row in summary.itertuples(index=False):
        ax.text(row.evidence_rows + 0.03, row.human_review, row.label)
    ax.set_xlabel("Mean expected evidence rows")
    ax.set_ylabel("Human review share")
    ax.set_title("Figure 13. Question difficulty profile", loc="left", fontweight="bold")
    clean_axes(ax)
    return _save(
        fig,
        "figure_13_question_difficulty_profile",
        "Question difficulty increases where more evidence rows and human review signals are required.",
    )


def _figure_14_error_taxonomy() -> list[Path]:
    results = pd.read_parquet(ROOT / "outputs/evaluation/rag_evaluation_results.parquet")
    failed = results[~results["overall_pass"]]
    counts = failed["evaluation_notes"].value_counts().head(6)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(counts.index[::-1], counts.values[::-1], color=PALETTE["orange"])
    ax.set_xlabel("Failed records")
    ax.set_title("Figure 14. Error taxonomy distribution", loc="left", fontweight="bold")
    clean_axes(ax)
    return _save(
        fig,
        "figure_14_error_taxonomy",
        "The dominant failures are tied to incomplete expected evidence and citation support.",
    )


def _figure_15_claim_support() -> list[Path]:
    results = pd.read_parquet(ROOT / "outputs/evaluation/rag_evaluation_results.parquet")
    supported = int((~results["unsupported_claim_flag"]).sum())
    weak = int(results["unsupported_claim_flag"].sum())
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    ax.bar(
        ["Supported screen", "Weak support flag"],
        [supported, weak],
        color=[PALETTE["teal"], PALETTE["orange"]],
    )
    ax.set_ylabel("Answer count")
    ax.set_title("Figure 15. Claim-support screening summary", loc="left", fontweight="bold")
    clean_axes(ax)
    return _save(
        fig,
        "figure_15_claim_support_summary",
        "Claim-support screening flags likely weak support but is not a substitute for expert review.",
    )


def _figure_16_source_conflict_flow() -> list[Path]:
    fig, ax = plt.subplots(figsize=(12, 5.8))
    labels = [
        "Retrieved sources",
        "Check version and date",
        "Prefer specific rule",
        "Escalate tension",
        "Human review decision",
    ]
    draw_box_flow(ax, labels, "Figure 16. Source-conflict and versioning decision flow")
    return _save(
        fig,
        "figure_16_source_conflict_versioning_flow",
        "Source conflict handling prefers newer and more specific evidence, with unresolved tension routed to review.",
    )


QUESTION_TITLE = {
    "factual": "Factual",
    "multi_hop": "Multi-hop",
    "ambiguous": "Ambiguous",
    "refusal": "Refusal",
    "adversarial": "Adversarial",
}


def main() -> None:
    outputs = generate_publication_figures()
    print("Publication figures generated.")
    print(f"files: {len(outputs)}")


if __name__ == "__main__":
    main()
