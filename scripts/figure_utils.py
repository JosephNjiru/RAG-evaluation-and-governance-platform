"""Shared visual utilities for project figures."""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
PALETTE = {
    "blue": "#2F5D8C",
    "teal": "#2A9D8F",
    "orange": "#E76F51",
    "gold": "#E9C46A",
    "purple": "#7B6DAD",
    "grey": "#6B7280",
    "light": "#F3F6FA",
    "dark": "#1F2937",
}
BASELINE_LABELS = {
    "baseline_a_tfidf": "A: TF-IDF",
    "baseline_b_metadata_weighted_tfidf": "B: weighted TF-IDF",
    "baseline_c_bm25": "C: BM25",
    "baseline_d_hybrid": "D: hybrid",
    "baseline_e_decomposition_diversified": "E: decomposed + diverse",
}
QUESTION_LABELS = {
    "factual": "Factual",
    "multi_hop": "Multi-hop",
    "ambiguous": "Ambiguous",
    "refusal": "Refusal",
    "adversarial": "Adversarial",
}


def apply_style() -> None:
    """Apply a consistent project style."""

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "axes.linewidth": 0.8,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "figure.titlesize": 15,
            "savefig.dpi": 220,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def save_all(fig: Figure, stem: str, target_dirs: list[Path], vector: bool = True) -> list[Path]:
    """Save a figure as PNG and, where appropriate, vector formats."""

    outputs: list[Path] = []
    for directory in target_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        png_path = directory / f"{stem}.png"
        fig.savefig(png_path, bbox_inches="tight", facecolor="white")
        outputs.append(png_path)
        if vector:
            for suffix in ["svg", "pdf"]:
                output_path = directory / f"{stem}.{suffix}"
                fig.savefig(output_path, bbox_inches="tight", facecolor="white")
                outputs.append(output_path)
    plt.close(fig)
    return outputs


def load_ablation_summary(root: Path = ROOT) -> pd.DataFrame:
    path = root / "outputs/evaluation/retrieval_ablation_by_question_type.csv"
    frame = pd.read_csv(path)
    frame["method_label"] = frame["retrieval_method"].map(BASELINE_LABELS)
    frame["question_label"] = (
        frame["question_type"].map(QUESTION_LABELS).fillna(frame["question_type"])
    )
    return frame


def load_question_bank(root: Path = ROOT) -> pd.DataFrame:
    frame = pd.read_csv(root / "data/evaluation/question_bank.csv")
    frame["question_label"] = frame["question_type"].map(QUESTION_LABELS)
    return frame


def load_challenge_results(root: Path = ROOT) -> pd.DataFrame:
    return pd.read_parquet(root / "outputs/evaluation/challenge_evaluation_results.parquet")


def annotate_bars(ax: Axes, values: list[float], percent: bool = True) -> None:
    for index, value in enumerate(values):
        label = f"{value:.3f}" if percent else str(value)
        ax.text(index, value + 0.02, label, ha="center", va="bottom", fontsize=9)


def add_caption(fig: Figure, text: str) -> None:
    fig.text(0.02, 0.01, text, ha="left", va="bottom", fontsize=9, color=PALETTE["dark"])


def draw_box_flow(ax: Axes, labels: list[str], title: str) -> None:
    ax.set_axis_off()
    ax.set_title(title, loc="left", fontweight="bold")
    count = len(labels)
    width = 0.82 / count
    y = 0.48
    for index, label in enumerate(labels):
        x = 0.05 + index * (width + 0.025)
        rect = Rectangle(
            (x, y),
            width,
            0.22,
            facecolor=PALETTE["light"],
            edgecolor=PALETTE["blue"],
            linewidth=1.2,
        )
        ax.add_patch(rect)
        ax.text(
            x + width / 2,
            y + 0.11,
            "\n".join(wrap(label, 14)),
            ha="center",
            va="center",
            fontsize=9,
        )
        if index < count - 1:
            arrow = FancyArrowPatch(
                (x + width, y + 0.11),
                (x + width + 0.025, y + 0.11),
                arrowstyle="->",
                mutation_scale=12,
                color=PALETTE["grey"],
            )
            ax.add_patch(arrow)


def clean_axes(ax: Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#D8DEE9", linewidth=0.6, alpha=0.8)
