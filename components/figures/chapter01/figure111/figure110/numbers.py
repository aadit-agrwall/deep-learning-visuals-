from __future__ import annotations

from manim import *

from components.graph.labels import NumberBadge
from components.figures.chapter01.figure111.figure110.data import SPECIES


class Figure110Numbers(VGroup):
    """
    Number badges placed on top of scatter points.
    """

    def __init__(self, axes, **kwargs):
        super().__init__(**kwargs)

        self.badges = VGroup()

        for species in SPECIES:

            badge = NumberBadge(
                species.id,
                radius=0.12,
                font_size=14,
            )

            badge.move_to(
                axes.point(
                    species.year,
                    species.connections,
                )
            )

            self.badges.add(badge)

        self.add(self.badges)

    def __iter__(self):
        return iter(self.badges)

    def __getitem__(self, index):
        return self.badges[index]

    def __len__(self):
        return len(self.badges)