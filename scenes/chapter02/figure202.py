from manim import *

from components.figures.chapter02.figure202.objects import (
    ScalarVisual,
    VectorVisual,
    MatrixVisual,
    VectorPointVisual,
)

config.background_color = WHITE


class Figure202(Scene):

    def construct(self):

        title = Text(
            "Scalars, Vectors and Matrices",
            font_size=34,
            color=BLACK,
        )

        title.to_edge(UP)

        self.play(Write(title))

        # Scalar
        scalar = ScalarVisual("s")

        scalar_label = Text(
            "Scalar",
            font_size=26,
            color=BLACK,
        )

        scalar_label.next_to(scalar, DOWN, buff=0.3)

        scalar_definition = MathTex(
            r"s \in \mathbb{R}",
            font_size=32,
            color=BLACK,
        )

        scalar_definition.next_to(
            scalar_label,
            DOWN,
            buff=0.25,
        )

        scalar_group = VGroup(
            scalar,
            scalar_label,
            scalar_definition,
        )

        self.play(
            FadeIn(scalar),
            Write(scalar_label),
            Write(scalar_definition),
        )

        self.wait(1)

        self.play(FadeOut(scalar_group))

        # Vector
        vector = VectorVisual()

        vector_label = Text(
            "Vector",
            font_size=26,
            color=BLACK,
        )

        vector_label.next_to(vector, DOWN, buff=0.3)

        vector_space = MathTex(
            r"\mathbf{x} \in \mathbb{R}^{n}",
            font_size=32,
            color=BLACK,
        )

        vector_space.next_to(
            vector_label,
            DOWN,
            buff=0.25,
        )

        vector_group = VGroup(
            vector,
            vector_label,
            vector_space,
        )

        self.play(
            FadeIn(vector),
            Write(vector_label),
            Write(vector_space),
        )

        self.wait(1)

        # Vector indexing
        indexing = MathTex(
            r"\mathbf{x}="
            r"\begin{bmatrix}"
            r"x_1\\"
            r"x_2\\"
            r"\vdots\\"
            r"x_n"
            r"\end{bmatrix}",
            font_size=34,
            color=BLACK,
        )

        indexing.to_edge(RIGHT, buff=1)

        arrow = Arrow(
            vector.get_right(),
            indexing.get_left(),
            buff=0.3,
            color=BLACK,
        )

        self.play(
            GrowArrow(arrow),
            Write(indexing),
        )

        self.wait(2)

        self.play(
            FadeOut(
                vector_group,
                arrow,
                indexing,
            )
        )

        # Vector as point
        point_visual = VectorPointVisual()
        point_visual.scale(0.85)

        point_title = Text(
            "A vector can identify a point in space",
            font_size=27,
            color=BLACK,
        )

        point_title.to_edge(UP, buff=1.0)

        self.play(
            Write(point_title),
            Create(point_visual.axes),
        )

        self.play(
            GrowArrow(point_visual.vector),
            FadeIn(point_visual.point),
            Write(point_visual.coordinate),
        )

        self.wait(2)

        self.play(
            FadeOut(
                point_title,
                point_visual,
            )
        )

        # Matrix
        matrix = MatrixVisual(rows=3, cols=4)

        matrix_label = Text(
            "Matrix",
            font_size=28,
            color=BLACK,
        )

        matrix_label.next_to(matrix, DOWN, buff=0.4)

        matrix_space = MathTex(
            r"A \in \mathbb{R}^{m\times n}",
            font_size=32,
            color=BLACK,
        )

        matrix_space.next_to(
            matrix_label,
            DOWN,
            buff=0.25,
        )

        self.play(
            FadeIn(matrix),
            Write(matrix_label),
            Write(matrix_space),
        )

        self.wait(1)

        # Matrix element
        element = matrix.get_entry(0, 0)

        highlight = SurroundingRectangle(
            element,
            buff=0.08,
            stroke_width=3,
            color=BLACK,
        )

        explanation = MathTex(
            r"A_{1,1}",
            font_size=34,
            color=BLACK,
        )

        explanation.next_to(
            matrix,
            RIGHT,
            buff=0.8,
        )

        self.play(
            Create(highlight),
            Write(explanation),
        )

        self.wait(2)

        # Matrix row
        self.play(
            FadeOut(
                highlight,
                explanation,
            )
        )

        row = matrix.get_row(1)

        row_highlight = SurroundingRectangle(
            row,
            buff=0.08,
            stroke_width=3,
            color=BLACK,
        )

        row_label = MathTex(
            r"A_{2,:}",
            font_size=34,
            color=BLACK,
        )

        row_label.next_to(
            matrix,
            RIGHT,
            buff=0.8,
        )

        self.play(
            Create(row_highlight),
            Write(row_label),
        )

        self.wait(2)

        self.play(
            FadeOut(
                row_highlight,
                row_label,
                matrix,
                matrix_label,
                matrix_space,
                title,
            )
        )

        self.wait(1)
