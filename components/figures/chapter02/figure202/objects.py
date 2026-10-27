from __future__ import annotations

from manim import *


class ScalarVisual(VGroup):
    def __init__(self, value="s", **kwargs):
        super().__init__(**kwargs)

        self.value = MathTex(value, font_size=42, color=BLACK)

        self.box = SurroundingRectangle(
            self.value,
            buff=0.25,
            corner_radius=0.08,
            stroke_width=2,
            color=BLACK,
        )

        self.add(self.box, self.value)


class VectorVisual(VGroup):
    def __init__(self, values=None, **kwargs):
        super().__init__(**kwargs)

        if values is None:
            values = ["x_1", "x_2", "x_3", "\\vdots", "x_n"]

        self.entries = VGroup(
            *[
                MathTex(value, font_size=32, color=BLACK)
                for value in values
            ]
        )

        self.entries.arrange(DOWN, buff=0.18)

        left = MathTex("\\left[", font_size=52, color=BLACK)
        right = MathTex("\\right]", font_size=52, color=BLACK)

        left.stretch_to_fit_height(self.entries.height + 0.25)
        right.stretch_to_fit_height(self.entries.height + 0.25)

        left.next_to(self.entries, LEFT, buff=0.12)
        right.next_to(self.entries, RIGHT, buff=0.12)

        self.add(left, self.entries, right)


class MatrixVisual(VGroup):
    def __init__(self, rows=3, cols=4, **kwargs):
        super().__init__(**kwargs)

        entries = VGroup()

        for i in range(rows):
            row = VGroup(
                *[
                    MathTex(
                        f"a_{{{i + 1},{j + 1}}}",
                        font_size=27,
                        color=BLACK,
                    )
                    for j in range(cols)
                ]
            )

            row.arrange(RIGHT, buff=0.35)
            entries.add(row)

        entries.arrange(DOWN, buff=0.25)

        self.entries = entries

        left = MathTex("\\left[", font_size=60, color=BLACK)
        right = MathTex("\\right]", font_size=60, color=BLACK)

        left.stretch_to_fit_height(entries.height + 0.3)
        right.stretch_to_fit_height(entries.height + 0.3)

        left.next_to(entries, LEFT, buff=0.15)
        right.next_to(entries, RIGHT, buff=0.15)

        self.add(left, entries, right)

    def get_entry(self, row, column):
        return self.entries[row][column]

    def get_row(self, row):
        return self.entries[row]

    def get_column(self, column):
        return VGroup(
            *[
                self.entries[row][column]
                for row in range(len(self.entries))
            ]
        )


class VectorPointVisual(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=4,
            y_length=4,
            axis_config={
                "include_numbers": True,
                "font_size": 18,
                "color": BLACK,
            },
        )

        self.vector = Arrow(
            self.axes.c2p(0, 0),
            self.axes.c2p(3, 4),
            buff=0,
            stroke_width=4,
            color=BLACK,
        )

        self.point = Dot(
            self.axes.c2p(3, 4),
            radius=0.07,
            color=BLACK,
        )

        self.coordinate = MathTex(
            "(x_1,x_2)",
            font_size=28,
            color=BLACK,
        )

        self.coordinate.next_to(
            self.point,
            UR,
            buff=0.15,
        )

        self.add(
            self.axes,
            self.vector,
            self.point,
            self.coordinate,
        )
