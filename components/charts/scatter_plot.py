"""
components/charts/scatter_plot.py

High-level scatter chart: builds axes + a ScatterPlot/NamedScatterPlot
from raw (x, y) data coordinates in a single call, converting data-space
coordinates to screen-space via the axes before handing them to
components.graph.scatter (which expects already-converted points).
"""

from manim import VGroup

from components.charts.axes import build_axes
from components.graph.scatter import ScatterPlot, NamedScatterPlot, ColoredScatterPlot
from common.colors import get_color, palette_sequence


class ChartScatterPlot(VGroup):
    """
    Example:
        chart = ChartScatterPlot(
            coordinates=[(1, 2), (3, 5), (4, 1)],
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            chapter="chapter01",
        )
    """

    def __init__(self, coordinates, x_range, y_range, chapter=None,
                 labels=None, x_length=8, y_length=5, radius=0.06, **kwargs):
        super().__init__(**kwargs)

        self.axes = build_axes(
            x_range=x_range, y_range=y_range, chapter=chapter,
            x_length=x_length, y_length=y_length,
        )
        self.add(self.axes)

        screen_points = [self.axes.c2p(x, y) for x, y in coordinates]
        color = get_color("primary", chapter=chapter)

        if labels is not None:
            self.scatter = NamedScatterPlot(
                coordinates=screen_points, labels=labels, radius=radius, color=color,
            )
        else:
            self.scatter = ScatterPlot(
                coordinates=screen_points, radius=radius, color=color,
            )
        self.add(self.scatter)

    def __iter__(self):
        return iter(self.scatter)

    def __len__(self):
        return len(self.scatter)
