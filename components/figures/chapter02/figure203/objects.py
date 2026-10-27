from __future__ import annotations

from manim import *


class VectorIndexVisual(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.entries = VGroup(
            *[
                MathTex(
                    rf"x_{i}",
                    font_size=38,
                    color=BLACK,
                )
                for i in range(1, 7)
            ]
        )

        self.entries.arrange(
            DOWN,
            buff=0.18,
        )

        self.left_bracket = MathTex(
            r"\left[",
            font_size=55,
            color=BLACK,
        )

        self.right_bracket = MathTex(
            r"\right]",
            font_size=55,
            color=BLACK,
        )

        self.left_bracket.stretch_to_fit_height(
            self.entries.height + 0.25
        )

        self.right_bracket.stretch_to_fit_height(
            self.entries.height + 0.25
        )

        self.left_bracket.next_to(
            self.entries,
            LEFT,
            buff=0.12,
        )

        self.right_bracket.next_to(
            self.entries,
            RIGHT,
            buff=0.12,
        )

        self.add(
            self.left_bracket,
            self.entries,
            self.right_bracket,
        )


class MatrixDimensionVisual(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.matrix = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"a_{1,1}&a_{1,2}&\cdots&a_{1,n}\\"
            r"a_{2,1}&a_{2,2}&\cdots&a_{2,n}\\"
            r"\vdots&\vdots&\ddots&\vdots\\"
            r"a_{m,1}&a_{m,2}&\cdots&a_{m,n}"
            r"\end{bmatrix}",
            font_size=30,
            color=BLACK,
        )

        self.dimension = MathTex(
            r"A\in\mathbb{R}^{m\times n}",
            font_size=34,
            color=BLACK,
        )

        self.dimension.next_to(
            self.matrix,
            DOWN,
            buff=0.5,
        )

        self.add(
            self.matrix,
            self.dimension,
        )


class MatrixRowColumnVisual(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.matrix = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"a_{1,1}&a_{1,2}&a_{1,3}\\"
            r"a_{2,1}&a_{2,2}&a_{2,3}\\"
            r"a_{3,1}&a_{3,2}&a_{3,3}"
            r"\end{bmatrix}",
            font_size=38,
            color=BLACK,
        )

        self.add(self.matrix)
