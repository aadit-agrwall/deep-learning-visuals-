from __future__ import annotations

from manim import *

from components.graph.scatter import ScatterPoint
from components.figures.chapter01.figure111.figure110.data import SPECIES


class Figure110Points(VGroup):
    """
    Scatter points for Figure 1.10.
    """

    def __init__(
        self,
        axes,
        radius=0.055,
        color=BLACK,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.axes = axes

        # IMPORTANT:
        # Never use self.points in a VGroup.
        self.dots = VGroup()

        for species in SPECIES:

            dot = ScatterPoint(
                axes.point(
                    species.year,
                    species.connections,
                ),
                radius=radius,
                color=color,
                stroke_color=WHITE,
                stroke_width=1.2,
            )

            self.dots.add(dot)

        self.add(self.dots)

    def __getitem__(self, index):
        return self.dots[index]

    def __len__(self):
        return len(self.dots)

    def __iter__(self):
        return iter(self.dots)