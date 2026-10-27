from __future__ import annotations

from manim import *


class Figure111Leaders(VGroup):

    def __init__(self, axes, labels, points, **kwargs):
        super().__init__(**kwargs)

        self.lines = VGroup()

        for label, dot in zip(labels, points):

            line = CurvedArrow(
                start_point=label.get_center(),
                end_point=dot.get_center(),
                angle=-0.25,
                stroke_width=1.2,
                tip_length=0.08,
                color=GRAY_B,
            )

            self.lines.add(line)

        self.add(self.lines)

    def __iter__(self):
        return iter(self.lines)

    def __getitem__(self, i):
        return self.lines[i]

    def __len__(self):
        return len(self.lines)