"""Generate PowerPoint-ready slide visuals."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.figure_utils import PALETTE, apply_style, draw_box_flow, save_all

SLIDE_DIR = ROOT / "figures/export/slides"


def generate_slide_figures() -> list[Path]:
    apply_style()
    outputs: list[Path] = []
    outputs.extend(_slide_summary())
    outputs.extend(_slide_flow())
    outputs.extend(_slide_governance())
    return outputs


def _slide_summary() -> list[Path]:
    fig, ax = plt.subplots(figsize=(13.33, 7.5))
    ax.set_axis_off()
    ax.text(
        0.05,
        0.82,
        "RAG evaluation result",
        transform=ax.transAxes,
        fontsize=28,
        fontweight="bold",
        color=PALETTE["dark"],
    )
    items = [
        ("Baseline A", "0.850 overall\n0.100 multi-hop"),
        ("Baseline E", "0.867 overall\n0.200 multi-hop"),
        ("Validation", "54 tests passed\nQuality scan passed"),
    ]
    for index, (title, value) in enumerate(items):
        x = 0.06 + index * 0.31
        ax.add_patch(
            plt.Rectangle(
                (x, 0.34),
                0.26,
                0.28,
                transform=ax.transAxes,
                facecolor=PALETTE["light"],
                edgecolor=PALETTE["blue"],
            )
        )
        ax.text(x + 0.03, 0.53, title, transform=ax.transAxes, fontsize=18, fontweight="bold")
        ax.text(x + 0.03, 0.40, value, transform=ax.transAxes, fontsize=15)
    ax.text(
        0.06,
        0.18,
        "Key message: multi-hop evidence assembly remains a limitation.",
        transform=ax.transAxes,
        fontsize=16,
        color=PALETTE["orange"],
    )
    return save_all(fig, "slide_results_summary", [SLIDE_DIR], vector=True)


def _slide_flow() -> list[Path]:
    fig, ax = plt.subplots(figsize=(13.33, 7.5))
    draw_box_flow(
        ax,
        ["Corpus", "Chunks", "Retrieval", "Answer", "Evaluation", "Review"],
        "Slide. Evaluation data flow",
    )
    return save_all(fig, "slide_evaluation_flow", [SLIDE_DIR], vector=True)


def _slide_governance() -> list[Path]:
    fig, ax = plt.subplots(figsize=(13.33, 7.5))
    draw_box_flow(
        ax,
        ["Risk level", "Support check", "Safety screen", "Human review", "Governance record"],
        "Slide. Governance flow",
    )
    return save_all(fig, "slide_governance_flow", [SLIDE_DIR], vector=True)


def main() -> None:
    outputs = generate_slide_figures()
    print("Slide figures generated.")
    print(f"files: {len(outputs)}")


if __name__ == "__main__":
    main()
