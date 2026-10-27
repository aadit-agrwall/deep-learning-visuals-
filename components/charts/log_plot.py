"""
components/charts/log_plot.py

High-level logarithmic chart: builds LogAxes + a GraphCurve and/or
scatter points from real (x, y) data, handling the log-scale conversion
automatically via LogAxes.point(). Mirrors the pattern used in
components/figures/chapter01/figure110's log-scale figures.
"""

from manim import VGroup

from components.charts.axes import build_log_axes
from components.graph.curves import GraphCurve
from components.graph.scatter import ScatterPoint
from common.colors import get_color


class LogPlot(VGroup):
    """
    Example:
        chart = LogPlot(
            coordinates=[(1950, 15), (1980, 250), (2010, 9000)],
            x_range=[1950, 2015, 10],
            y_min=10,
            y_max=10000,
            chapter="chapter01",
        )
    """

    def __init__(self, coordinates, x_range, y_min, y_max, chapter=None,
                 x_length=8, y_length=5, show_curve=True, show_points=True,
                 stroke_width=2.2, point_radius=0.05, **kwargs):
        super().__init__(**kwargs)

        self.axes = build_log_axes(
            x_range=x_range, y_min=y_min, y_max=y_max, chapter=chapter,
            x_length=x_length, y_length=y_length,
        )
        self.add(self.axes)

        color = get_color("primary", chapter=chapter)

        if show_curve:
            self.curve = GraphCurve(
                axes=self.axes,
                coordinates=coordinates,
                log_scale=True,
                color=color,
                stroke_width=stroke_width,
            )
            self.add(self.curve)

        if show_points:
            # NOTE: named scatter_points, NOT "points" — VMobject.points is a
            # reserved internal attribute (the numpy array backing the mobject's
            # geometry). Overwriting it with a VGroup breaks scale(), get_anchors(),
            # and other geometric operations across the whole object tree.
            self.scatter_points = VGroup()
            for x, y in coordinates:
                point = ScatterPoint(
                    self.axes.point(x, y),
                    radius=point_radius,
                    color=color,
                )
                self.scatter_points.add(point)
            self.add(self.scatter_points)
