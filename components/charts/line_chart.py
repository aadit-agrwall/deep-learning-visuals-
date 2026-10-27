"""
components/charts/line_chart.py

High-level LineChart: builds axes + one or more GraphCurve series from
raw (x, y) data in a single call, with chapter-aware coloring. Built on
top of components.graph.axes and components.graph.curves — does not
reimplement axis or curve drawing.
"""

from manim import VGroup

from components.charts.axes import build_axes
from components.graph.curves import GraphCurve
from common.colors import get_color, palette_sequence


class LineChart(VGroup):
    """
    Example:
        chart = LineChart(
            series={"Train loss": [(0, 2.1), (1, 1.4), (2, 0.9)],
                    "Val loss":   [(0, 2.3), (1, 1.6), (2, 1.2)]},
            x_range=[0, 2, 1],
            y_range=[0, 3, 0.5],
            chapter="chapter02",
        )
    """

    def __init__(self, series: dict, x_range, y_range, chapter=None,
                 x_length=8, y_length=5, stroke_width=2.5, show_grid=False, **kwargs):
        super().__init__(**kwargs)

        self.axes = build_axes(
            x_range=x_range, y_range=y_range, chapter=chapter,
            x_length=x_length, y_length=y_length, show_grid=show_grid,
        )
        self.add(self.axes)

        names = list(series.keys())
        colors = palette_sequence(len(names), chapter=chapter)

        self.curves = {}
        for name, color in zip(names, colors):
            curve = GraphCurve(
                axes=self.axes,
                coordinates=series[name],
                color=color,
                stroke_width=stroke_width,
            )
            self.curves[name] = curve
            self.add(curve)

    def get_curve(self, name: str):
        return self.curves[name]
