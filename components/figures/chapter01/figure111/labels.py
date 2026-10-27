from __future__ import annotations

from manim import *

from components.graph.labels import SpeciesLabel
from components.figures.chapter01.figure111.data import NETWORKS


class Figure111Labels(VGroup):
    """
    Species labels for Figure 1.10.
    """

    def __init__(self, axes, **kwargs):
        super().__init__(**kwargs)

        self.labels = VGroup()

        for network in NETWORKS:

            label = SpeciesLabel(
                network.name,
                italic=network.italic,
                font_size=20,
                color=BLACK,
            )

            label.move_to(
                axes.point(
                    network.label_position[0],
                    network.label_position[1],
                )
            )

            self.labels.add(label)

        self.add(self.labels)

    def __getitem__(self, index):
        return self.labels[index]

    def __len__(self):
        return len(self.labels)

    def __iter__(self):
        return iter(self.labels)