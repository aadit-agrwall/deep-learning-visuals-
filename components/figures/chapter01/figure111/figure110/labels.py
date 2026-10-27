from __future__ import annotations

from manim import *

from components.graph.labels import SpeciesLabel
from components.figures.chapter01.figure111.figure110.data import SPECIES


class Figure110Labels(VGroup):
    """
    Species labels for Figure 1.10.
    """

    def __init__(self, axes, **kwargs):
        super().__init__(**kwargs)

        self.labels = VGroup()

        for species in SPECIES:

            label = SpeciesLabel(
                species.species,
                italic=species.italic,
                font_size=20,
                color=BLACK,
            )

            label.move_to(
                axes.point(
                    species.label_position[0],
                    species.label_position[1],
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