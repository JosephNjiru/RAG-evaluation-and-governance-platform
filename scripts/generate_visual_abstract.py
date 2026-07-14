"""Generate visual abstract assets."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.figure_utils import PALETTE, apply_style, save_all

SLIDE_DIR = ROOT / "figures/export/slides"
WEB_DIR = ROOT / "figures/export/web"


def generate_visual_abstract() -> list[Path]:
    apply_style()
    outputs: list[Path] = []
    outputs.extend(
        _abstract(
            "visual_abstract_landscape",
            (13.33, 7.5),
            [SLIDE_DIR, WEB_DIR],
            "landscape",
        )
    )
    return outputs


def _abstract(stem: str, figsize: tuple[float, float], dirs: list[Path], layout: str) -> list[Path]:
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="#FBFCFE", edgecolor="none"))
    ax.add_patch(
        Rectangle((0.025, 0.035), 0.95, 0.92, fill=False, edgecolor=PALETTE["blue"], linewidth=1.8)
    )
    ax.add_patch(
        Rectangle((0.025, 0.918), 0.95, 0.037, facecolor=PALETTE["blue"], edgecolor="none")
    )

    title_size = 22 if layout == "landscape" else 18
    ax.text(
        0.06,
        0.86,
        "RAG Evaluation and Governance Platform",
        fontsize=title_size,
        fontweight="bold",
        color=PALETTE["dark"],
        ha="left",
        va="top",
    )
    subtitle_y = 0.795 if layout == "landscape" else 0.755
    subtitle = (
        "A local-first assurance project for testing retrieval quality, citation support, faithfulness, refusal behaviour and governance readiness."
        if layout == "landscape"
        else "Local RAG assurance: retrieval, citation, refusal and review are tested together."
    )
    _wrapped_text(
        ax,
        0.06,
        subtitle_y,
        subtitle,
        width=105 if layout == "landscape" else 52,
        fontsize=10.5 if layout == "landscape" else 9.4,
        colour=PALETTE["grey"],
        line_gap=0.032 if layout == "landscape" else 0.027,
    )

    if layout == "portrait":
        _portrait_content(ax)
        return save_all(fig, stem, dirs, vector=True)

    if layout == "landscape":
        panel_positions = [(0.06, 0.54), (0.285, 0.54), (0.51, 0.54), (0.735, 0.54)]
        panel_width = 0.19
        text_width = 26
        metric_y = 0.245
        caveat_y = 0.125

    panels = [
        (
            "Problem",
            "Fluent RAG answers can still be unsupported or wrongly cited.",
            PALETTE["blue"],
        ),
        (
            "Method",
            "Measure retrieval, citations, faithfulness, refusal and safety signals.",
            PALETTE["teal"],
        ),
        ("Result", "Baseline E improves overall pass rate from 0.850 to 0.867.", PALETTE["purple"]),
        (
            "Limit",
            "Multi-hop pass rate remains weak at 0.200 on the main benchmark.",
            PALETTE["orange"],
        ),
    ]
    for (x, y), (heading, text, accent) in zip(panel_positions, panels, strict=True):
        _panel(ax, x, y, panel_width, 0.175, accent)
        ax.text(
            x + 0.02,
            y + 0.127,
            heading,
            fontsize=12.5,
            fontweight="bold",
            color=accent,
            ha="left",
            va="top",
        )
        _wrapped_text(
            ax,
            x + 0.02,
            y + 0.083,
            text,
            width=text_width,
            fontsize=8.9,
            colour=PALETTE["dark"],
            line_gap=0.024,
        )

    _metric_strip(ax, 0.06, metric_y, 0.88)
    caveat_height = 0.075
    _panel(ax, 0.06, caveat_y, 0.88, caveat_height, PALETTE["orange"], face="#FFF7ED")
    _wrapped_text(
        ax,
        0.085,
        caveat_y + 0.048,
        "Interpretation: retrieval improvement is useful but modest. Challenge-set results are separate from the main 60-question benchmark.",
        width=100,
        fontsize=9.5,
        colour=PALETTE["dark"],
        line_gap=0.024,
        weight="bold",
    )
    ax.text(
        0.06,
        0.055,
        "Synthetic corpus. Deterministic generator. Human review remains necessary for high-risk outputs.",
        fontsize=8.5,
        color=PALETTE["grey"],
        ha="left",
        va="center",
    )
    return save_all(fig, stem, dirs, vector=True)


def _portrait_content(ax: Axes) -> None:
    panels = [
        ("Problem", "Fluent answers can still be unsupported or wrongly cited.", PALETTE["blue"]),
        (
            "Method",
            "Measure retrieval, citations, faithfulness, refusal and safety signals.",
            PALETTE["teal"],
        ),
        ("Result", "Baseline E improves overall pass rate from 0.850 to 0.867.", PALETTE["purple"]),
        (
            "Limit",
            "Multi-hop pass rate remains weak at 0.200 on the main benchmark.",
            PALETTE["orange"],
        ),
    ]
    y_positions = [0.570, 0.470, 0.370, 0.270]
    for y, (heading, text, accent) in zip(y_positions, panels, strict=True):
        _panel(ax, 0.08, y, 0.84, 0.075, accent)
        ax.text(
            0.105,
            y + 0.050,
            heading,
            fontsize=10.2,
            fontweight="bold",
            color=accent,
            ha="left",
            va="top",
        )
        _wrapped_text(
            ax,
            0.34,
            y + 0.052,
            text,
            width=43,
            fontsize=7.6,
            colour=PALETTE["dark"],
            line_gap=0.018,
        )

    _metric_strip(ax, 0.08, 0.120, 0.84)
    _panel(ax, 0.08, 0.045, 0.84, 0.060, PALETTE["orange"], face="#FFF7ED")
    _wrapped_text(
        ax,
        0.105,
        0.083,
        "Interpretation: improvement is useful but modest. The challenge set is separate from the main benchmark.",
        width=70,
        fontsize=7.2,
        colour=PALETTE["dark"],
        line_gap=0.017,
        weight="bold",
    )


def _panel(
    ax: Axes, x: float, y: float, width: float, height: float, accent: str, face: str = "white"
) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.01,rounding_size=0.015",
            linewidth=1.15,
            edgecolor=accent,
            facecolor=face,
        )
    )


def _wrapped_text(
    ax: Axes,
    x: float,
    y: float,
    text: str,
    width: int,
    fontsize: float,
    colour: str,
    line_gap: float,
    weight: str = "normal",
) -> float:
    lines = wrap(text, width=width, break_long_words=False)
    for offset, line in enumerate(lines):
        ax.text(
            x,
            y - offset * line_gap,
            line,
            fontsize=fontsize,
            color=colour,
            fontweight=weight,
            ha="left",
            va="top",
        )
    return y - len(lines) * line_gap


def _metric_strip(ax: Axes, x: float, y: float, width: float) -> None:
    labels = [
        ("Baseline A", "0.850", PALETTE["blue"]),
        ("Baseline E", "0.867", PALETTE["teal"]),
        ("Multi-hop E", "0.200", PALETTE["orange"]),
        ("Citation E", "0.917", PALETTE["purple"]),
    ]
    gap = 0.018
    tile_width = (width - gap * 3) / 4
    for index, (label, value, accent) in enumerate(labels):
        tile_x = x + index * (tile_width + gap)
        _panel(ax, tile_x, y, tile_width, 0.12, accent, face=PALETTE["light"])
        ax.text(
            tile_x + 0.018,
            y + 0.080,
            value,
            fontsize=15,
            fontweight="bold",
            color=accent,
            ha="left",
            va="top",
        )
        ax.text(
            tile_x + 0.018,
            y + 0.037,
            label,
            fontsize=8.8,
            color=PALETTE["dark"],
            ha="left",
            va="top",
        )


def main() -> None:
    outputs = generate_visual_abstract()
    print("Visual abstract generated.")
    print(f"files: {len(outputs)}")


if __name__ == "__main__":
    main()
