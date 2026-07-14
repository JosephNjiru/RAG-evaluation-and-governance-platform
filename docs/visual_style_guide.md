# Visual style guide

## Typography

- Font family: DejaVu Sans.
- Figure title: 13 to 15 pt, bold, sentence case.
- Axis labels: 10 pt.
- Tick labels: 9 pt.
- Captions: 9 pt, concise interpretation sentence.

## Palette

The figure palette uses colour-blind-aware blues, teal, orange, gold, purple and grey. Colour is supported with labels, markers or direct annotations where needed.

## Layout

- Use uncluttered axes and light grid lines.
- Keep legends short and close to the plotted data.
- Prefer direct labels for key comparisons.
- Use consistent figure IDs: `figure_01_...`, `figure_02_...`.

## Baseline labelling

- Baseline A: TF-IDF.
- Baseline B: weighted TF-IDF.
- Baseline C: BM25.
- Baseline D: hybrid.
- Baseline E: decomposed plus diverse.

## Limitations and annotations

Figures that show strong results must also preserve the main limitation: multi-hop evidence assembly remains weak on the original benchmark. Challenge-set figures must state that the challenge set has a different difficulty profile.

## Export guidance

- Journal: PDF, SVG and high-resolution PNG.
- Slides: 16:9 PNG and SVG.
- Web and README: PNG, with SVG where useful.
