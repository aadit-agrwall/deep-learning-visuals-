from __future__ import annotations

from manim import *

from components.graph.labels import BoxLabel


class Figure111Animals(VGroup):
    """
    Biological neuron count reference labels
    shown on the right side of Figure 1.11.
    """

    def __init__(self, axes, **kwargs):
        super().__init__(**kwargs)

        self.labels = VGroup()

        animals = [
            ("Human",      1e11),
            ("Octopus",    1e8),
            ("Frog",       1e7),
            ("Bee",        3e5),
            ("Ant",        1e5),
            ("Leech",      1e3),
            ("Roundworm",  1),
            ("Sponge",     1e-2),
        ]

        x_right = axes.axes.x_range[1]

        for name, value in animals:

            box = BoxLabel(
                name,
                font_size=20,
                fill_color="#FFF176",
                stroke_color=GRAY_B,
                stroke_width=1.8,
            )

            box.next_to(
                axes.point(x_right, value),
                RIGHT,
                buff=0.55,
            )

            self.labels.add(box)

        self.add(self.labels)

    def __iter__(self):
        return iter(self.labels)

    def __getitem__(self, index):
        return self.labels[index]

    def __len__(self):
        return len(self.labels)