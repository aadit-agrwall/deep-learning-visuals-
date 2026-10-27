from __future__ import annotations

from manim import *

from components.figures.chapter01.figure111.figure110.data import SPECIES


class Figure110Leaders(VGroup):
    """
    Leader lines joining labels to scatter points.
    """

    def __init__(self, axes, labels, points, **kwargs):
        super().__init__(**kwargs)

        self.lines = VGroup()

        for label, dot in zip(labels, points):

            line = Line(
                label.get_center(),
                dot.get_center(),
                stroke_width=1.1,
                color=GRAY_B,
            )

            self.lines.add(line)

        self.add(self.lines)

    def __iter__(self):
        return iter(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def __len__(self):
        return len(self.lines)