from __future__ import annotations

from manim import *


class Scalar(VGroup):
    def __init__(self, value="a", **kwargs):
        super().__init__(**kwargs)

        self.circle = Circle(
            radius=0.35,
            stroke_width=2,
            color=BLACK,
        )

        self.value = MathTex(
            value,
            font_size=30,
            color=BLACK,
        )

        self.value.move_to(self.circle)

        self.add(
            self.circle,
            self.value,
        )


class Vector(VGroup):
    def __init__(self, values=None, **kwargs):
        super().__init__(**kwargs)

        if values is None:
            values = ["a_1", "a_2", "a_3"]

        self.entries = VGroup(
            *[
                MathTex(
                    value,
                    font_size=28,
                    color=BLACK,
                )
                for value in values
            ]
        )

        self.entries.arrange(
            RIGHT,
            buff=0.35,
        )

        self.box = SurroundingRectangle(
            self.entries,
            buff=0.22,
            stroke_width=2,
            color=BLACK,
        )

        self.add(
            self.box,
            self.entries,
        )


class Matrix(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        values = [
            ["a_{11}", "a_{12}", "a_{13}"],
            ["a_{21}", "a_{22}", "a_{23}"],
        ]

        rows = VGroup()

        for row in values:

            row_group = VGroup(
                *[
                    MathTex(
                        value,
                        font_size=25,
                        color=BLACK,
                    )
                    for value in row
                ]
            )

            row_group.arrange(
                RIGHT,
                buff=0.3,
            )

            rows.add(row_group)

        rows.arrange(
            DOWN,
            buff=0.25,
        )

        self.box = SurroundingRectangle(
            rows,
            buff=0.25,
            stroke_width=2,
            color=BLACK,
        )

        self.add(
            self.box,
            rows,
        )


class Tensor(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layers = VGroup()

        for offset in [0, 0.18, 0.36]:

            matrix = Matrix()

            matrix.shift(
                RIGHT * offset +
                UP * offset
            )

            layers.add(matrix)

        self.add(layers)
