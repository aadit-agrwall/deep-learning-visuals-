"""
components/charts/bar_chart.py

High-level BarChart: builds axes + vertical bars from labeled values in
a single call. components.graph has no bar primitive, so bars are drawn
directly here as Rectangles positioned via the axes' c2p() conversion.
"""

from manim import VGroup, Rectangle, Text, UP, DOWN

from components.charts.axes import build_axes
from common.colors import get_color, palette_sequence
from common.styles import text_style


class BarChart(VGroup):
    """
    Example:
        chart = BarChart(
            data={"A": 4, "B": 7, "C": 3},
            y_max=10,
            chapter="chapter02",
        )
    """

    def __init__(self, data: dict, y_max: float, chapter=None,
                 x_length=8, y_length=5, bar_width_ratio=0.6,
                 show_value_labels=True, show_axis_labels=True, **kwargs):
        super().__init__(**kwargs)

        labels = list(data.keys())
        values = list(data.values())
        n = len(labels)

        self.axes = build_axes(
            x_range=[0, n, 1],
            y_range=[0, y_max, y_max / 5 if y_max else 1],
            chapter=chapter,
            x_length=x_length,
            y_length=y_length,
            show_border=False,
        )
        self.add(self.axes)

        colors = palette_sequence(n, chapter=chapter)
        slot_width = x_length / n
        bar_width = slot_width * bar_width_ratio

        self.bars = VGroup()
        self.value_labels = VGroup()
        self.axis_labels = VGroup()

        for i, (label, value, color) in enumerate(zip(labels, values, colors)):
            base_point = self.axes.c2p(i + 0.5, 0)
            top_point = self.axes.c2p(i + 0.5, value)
            bar_height = abs(top_point[1] - base_point[1])

            bar = Rectangle(
                width=bar_width,
                height=max(bar_height, 0.001),
                fill_color=color,
                fill_opacity=0.85,
                stroke_color=color,
                stroke_width=1.5,
            )
            bar.move_to(base_point, aligned_edge=DOWN)
            self.bars.add(bar)

            if show_value_labels:
                value_text = Text(str(value), **text_style("caption", chapter=chapter))
                value_text.next_to(bar, UP, buff=0.1)
                self.value_labels.add(value_text)

            if show_axis_labels:
                axis_text = Text(str(label), **text_style("caption", chapter=chapter))
                axis_text.next_to(base_point, DOWN, buff=0.2)
                self.axis_labels.add(axis_text)

        self.add(self.bars, self.value_labels, self.axis_labels)
