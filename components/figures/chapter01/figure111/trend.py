from __future__ import annotations

from manim import *


class Figure111Trend(Line):
    """
    Blue trend line for Figure 1.11.
    """

    def __init__(self, axes, **kwargs):
        super().__init__(
            start=axes.point(1990, 1e2),
            end=axes.point(2022, 1e10),
            color=BLUE_D,
            stroke_width=4,
            **kwargs,
        )