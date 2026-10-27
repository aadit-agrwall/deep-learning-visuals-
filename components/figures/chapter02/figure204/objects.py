from __future__ import annotations

from manim import *


class MatrixVisual(VGroup):
    def __init__(self, matrix_data, font_size=34, **kwargs):
        super().__init__(**kwargs)

        self.entries = VGroup()

        rows = len(matrix_data)
        cols = len(matrix_data[0])

        for i in range(rows):
            row = VGroup()

            for j in range(cols):
                entry = MathTex(
                    matrix_data[i][j],
                    font_size=font_size,
                    color=BLACK,
                )
                row.add(entry)

            row.arrange(RIGHT, buff=0.45)
            self.entries.add(row)

        self.entries.arrange(DOWN, buff=0.3)

        left = MathTex(
            r"\left[",
            font_size=65,
            color=BLACK,
        )

        right = MathTex(
            r"\right]",
            font_size=65,
            color=BLACK,
        )

        left.stretch_to_fit_height(
            self.entries.height + 0.35
        )

        right.stretch_to_fit_height(
            self.entries.height + 0.35
        )

        left.next_to(
            self.entries,
            LEFT,
            buff=0.15,
        )

        right.next_to(
            self.entries,
            RIGHT,
            buff=0.15,
        )

        self.left_bracket = left
        self.right_bracket = right

        self.add(
            left,
            self.entries,
            right,
        )

    def get_entry(self, row, column):
        return self.entries[row][column]


class TensorVisual(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Three overlapping matrix planes
        self.planes = VGroup()

        for depth in range(3):

            plane = Rectangle(
                width=2.8,
                height=2.2,
                stroke_width=2,
                color=BLACK,
            )

            plane.shift(
                RIGHT * depth * 0.25
                + UP * depth * 0.25
            )

            self.planes.add(plane)

        self.add(self.planes)

        self.label = MathTex(
            r"A_{i,j,k}",
            font_size=36,
            color=BLACK,
        )

        self.label.next_to(
            self.planes,
            DOWN,
            buff=0.35,
        )

        self.add(self.label)


class VectorColumnVisual(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.entries = VGroup(
            MathTex("x_1", font_size=38, color=BLACK),
            MathTex("x_2", font_size=38, color=BLACK),
            MathTex("x_3", font_size=38, color=BLACK),
        )

        self.entries.arrange(
            DOWN,
            buff=0.25,
        )

        left = MathTex(
            r"\left[",
            font_size=60,
            color=BLACK,
        )

        right = MathTex(
            r"\right]",
            font_size=60,
            color=BLACK,
        )

        left.stretch_to_fit_height(
            self.entries.height + 0.3
        )

        right.stretch_to_fit_height(
            self.entries.height + 0.3
        )

        left.next_to(
            self.entries,
            LEFT,
            buff=0.12,
        )

        right.next_to(
            self.entries,
            RIGHT,
            buff=0.12,
        )

        self.add(
            left,
            self.entries,
            right,
        )


class VectorRowVisual(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.entries = VGroup(
            MathTex("x_1", font_size=38, color=BLACK),
            MathTex("x_2", font_size=38, color=BLACK),
            MathTex("x_3", font_size=38, color=BLACK),
        )

        self.entries.arrange(
            RIGHT,
            buff=0.45,
        )

        left = MathTex(
            r"\left[",
            font_size=55,
            color=BLACK,
        )

        right = MathTex(
            r"\right]",
            font_size=55,
            color=BLACK,
        )

        left.stretch_to_fit_height(
            self.entries.height + 0.2
        )

        right.stretch_to_fit_height(
            self.entries.height + 0.2
        )

        left.next_to(
            self.entries,
            LEFT,
            buff=0.12,
        )

        right.next_to(
            self.entries,
            RIGHT,
            buff=0.12,
        )

        self.add(
            left,
            self.entries,
            right,
        )
