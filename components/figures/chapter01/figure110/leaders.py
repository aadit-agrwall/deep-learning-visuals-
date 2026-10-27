from __future__ import annotations

from manim import *


class Figure110Leaders(VGroup):
    """
    Leader lines connecting network labels to scatter points.
    """

    def __init__(
        self,
        axes,
        labels,
        points,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.lines = VGroup()

        for label, point in zip(labels, points):

            line = Line(
                start=label.get_center(),
                end=point.get_center(),
                stroke_width=1.2,
                color=BLACK,
            )

            self.lines.add(line)

        self.add(self.lines)

    def __iter__(self):
        return iter(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def __len__(self):
        return len(self.lines)