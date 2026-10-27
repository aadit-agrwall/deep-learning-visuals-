from manim import *

from components.figures.chapter02.figure203.objects import (
    VectorIndexVisual,
    MatrixDimensionVisual,
    MatrixRowColumnVisual,
)

config.background_color = WHITE


class Figure203(Scene):

    def construct(self):

        # ==================================================
        # TITLE
        # ==================================================

        title = Text(
            "Indexing Vectors and Matrices",
            font_size=34,
            color=BLACK,
        )

        title.to_edge(UP)

        self.play(Write(title))

        # ==================================================
        # VECTOR INDEXING
        # ==================================================

        vector_visual = VectorIndexVisual()

        vector_visual.move_to(
            LEFT * 3
        )

        vector_title = Text(
            "Vector indexing",
            font_size=28,
            color=BLACK,
        )

        vector_title.next_to(
            vector_visual,
            UP,
            buff=0.4,
        )

        self.play(
            Write(vector_title),
            FadeIn(vector_visual),
        )

        # S = {1,3,6}

        set_text = MathTex(
            r"S=\{1,3,6\}",
            font_size=34,
            color=BLACK,
        )

        set_text.next_to(
            vector_visual,
            RIGHT,
            buff=1.0,
        )

        x_s = MathTex(
            r"\mathbf{x}_S",
            font_size=38,
            color=BLACK,
        )

        x_s.next_to(
            set_text,
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(set_text),
            Write(x_s),
        )

        self.wait(1)

        # Highlight selected entries individually
        highlights = VGroup()

        for index in [0, 2, 5]:
            entry = vector_visual.entries[index]

            box = SurroundingRectangle(
                entry,
                buff=0.06,
                stroke_width=2.5,
                color=BLACK,
            )

            highlights.add(box)

        self.play(
            LaggedStart(
                *[
                    Create(box)
                    for box in highlights
                ],
                lag_ratio=0.2,
            )
        )

        self.wait(1)


        result = MathTex(
            r"\mathbf{x}_S="
            r"\begin{bmatrix}"
            r"x_1\\"
            r"x_3\\"
            r"x_6"
            r"\end{bmatrix}",
            font_size=36,
            color=BLACK,
        )

        result.next_to(
            x_s,
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(result)
        )

        self.wait(2)

        # ==================================================
        # COMPLEMENT
        # ==================================================

        self.play(
            FadeOut(
                vector_visual,
                vector_title,
                set_text,
                x_s,
                result,
                highlights,
            )
        )

        complement_title = Text(
            "Complement indexing",
            font_size=28,
            color=BLACK,
        )

        complement_title.next_to(
            title,
            DOWN,
            buff=0.6,
        )

        complement = MathTex(
            r"\mathbf{x}_{-1}",
            font_size=42,
            color=BLACK,
        )

        explanation = Text(
            "all elements except x₁",
            font_size=26,
            color=BLACK,
        )

        explanation.next_to(
            complement,
            DOWN,
            buff=0.35,
        )

        complement_group = VGroup(
            complement,
            explanation,
        )

        complement_group.move_to(
            ORIGIN
        )

        self.play(
            Write(complement_title),
            Write(complement),
            FadeIn(explanation),
        )

        self.wait(2)

        # ==================================================
        # MATRIX DIMENSIONS
        # ==================================================

        self.play(
            FadeOut(
                complement_title,
                complement_group,
                title,
            )
        )

        matrix_dimension = MatrixDimensionVisual()

        matrix_dimension.move_to(
            ORIGIN
        )

        matrix_title = Text(
            "Matrix dimensions",
            font_size=30,
            color=BLACK,
        )

        matrix_title.to_edge(
            UP,
            buff=0.8,
        )

        self.play(
            Write(matrix_title),
            FadeIn(matrix_dimension),
        )

        self.wait(2)

        # ==================================================
        # ROW / COLUMN
        # ==================================================

        self.play(
            FadeOut(
                matrix_dimension,
                matrix_title,
            )
        )

        row_column = MatrixRowColumnVisual()

        row_column.move_to(
            ORIGIN
        )

        rc_title = Text(
            "Rows and columns",
            font_size=30,
            color=BLACK,
        )

        rc_title.to_edge(
            UP,
            buff=0.8,
        )

        self.play(
            Write(rc_title),
            FadeIn(row_column),
        )

        self.wait(1)

        # Highlight second row
        row_box = SurroundingRectangle(
            row_column.matrix,
            buff=0.15,
            stroke_width=3,
            color=BLACK,
        )

        row_label = MathTex(
            r"A_{2,:}",
            font_size=38,
            color=BLACK,
        )

        row_label.next_to(
            row_box,
            RIGHT,
            buff=0.5,
        )

        self.play(
            Create(row_box),
            Write(row_label),
        )

        self.wait(2)

        self.play(
            FadeOut(
                row_box,
                row_label,
            )
        )

        # Highlight second column
        column_box = SurroundingRectangle(
            row_column.matrix,
            buff=0.15,
            stroke_width=3,
            color=BLACK,
        )

        column_label = MathTex(
            r"A_{:,2}",
            font_size=38,
            color=BLACK,
        )

        column_label.next_to(
            column_box,
            DOWN,
            buff=0.5,
        )

        self.play(
            Create(column_box),
            Write(column_label),
        )

        self.wait(2)

        self.play(
            FadeOut(
                column_box,
                column_label,
                row_column,
                rc_title,
            )
        )

        self.wait(1)
