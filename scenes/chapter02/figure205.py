from manim import *

config.background_color = WHITE


class Figure205(Scene):

    # ==========================================================
    # HELPERS
    # ==========================================================

    def flash(self, mob, color=YELLOW):
        self.play(
            Indicate(
                mob,
                color=color,
                scale_factor=1.18,
            ),
            run_time=0.45,
        )

    def write(self, mob, run_time=0.8):
        self.play(
            Write(mob),
            run_time=run_time,
        )

    def matrix_entries(
        self,
        values,
        center,
        cell_w=0.8,
        cell_h=0.65,
        font_size=30,
    ):
        entries = VGroup()

        rows = len(values)
        cols = len(values[0])

        for r in range(rows):
            for c in range(cols):

                entry = MathTex(
                    values[r][c],
                    font_size=font_size,
                    color=BLACK,
                )

                x = (c - (cols - 1) / 2) * cell_w
                y = ((rows - 1) / 2 - r) * cell_h

                entry.move_to(
                    center
                    + RIGHT * x
                    + UP * y
                )

                entries.add(entry)

        return entries

    def matrix_brackets(
        self,
        center,
        rows,
        cols,
        cell_w=0.8,
        cell_h=0.65,
        font_size=30,
    ):

        height = (rows - 1) * cell_h + 0.65
        width = (cols - 1) * cell_w + 0.65

        left = MathTex(
            r"\left[",
            font_size=font_size * 1.7,
            color=BLACK,
        )

        right = MathTex(
            r"\right]",
            font_size=font_size * 1.7,
            color=BLACK,
        )

        left.stretch_to_fit_height(height)
        right.stretch_to_fit_height(height)

        left.move_to(
            center + LEFT * (width / 2 + 0.25)
        )

        right.move_to(
            center + RIGHT * (width / 2 + 0.25)
        )

        return left, right

    def make_matrix(
        self,
        values,
        center,
        cell_w=0.8,
        cell_h=0.65,
        font_size=30,
    ):

        entries = self.matrix_entries(
            values,
            center,
            cell_w,
            cell_h,
            font_size,
        )

        left, right = self.matrix_brackets(
            center,
            len(values),
            len(values[0]),
            cell_w,
            cell_h,
            font_size,
        )

        return VGroup(
            left,
            entries,
            right,
        ), entries

    def section_title(self, text):

        title = Text(
            text,
            font_size=30,
            color=BLACK,
        )

        title.to_edge(
            UP,
            buff=0.28,
        )

        return title

    # ==========================================================
    # SCENE
    # ==========================================================

    def construct(self):

        # ======================================================
        # TITLE
        # ======================================================

        title = self.section_title(
            "Linear Algebra — Operations with Matrices and Vectors"
        )

        self.write(title)

        self.wait(0.5)

        # ======================================================
        # 1. ROW VECTOR -> COLUMN VECTOR
        # ======================================================

        row_title = Text(
            "A vector can be written as a row, then transposed",
            font_size=25,
            color=BLACK,
        )

        row_title.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        row = MathTex(
            r"\mathbf{x}="
            r"\begin{bmatrix}"
            r"x_1&x_2&x_3"
            r"\end{bmatrix}",
            font_size=40,
            color=BLACK,
        )

        row.move_to(
            LEFT * 2.7 + DOWN * 0.4
        )

        transpose_symbol = MathTex(
            r"^T",
            font_size=34,
            color=BLACK,
        )

        transpose_symbol.next_to(
            row,
            UP,
            buff=0.15,
        )

        arrow = Arrow(
            LEFT * 0.65,
            RIGHT * 0.65,
            color=BLACK,
            stroke_width=3,
            buff=0,
        )

        arrow.move_to(
            ORIGIN + DOWN * 0.4
        )

        column = MathTex(
            r"\mathbf{x}^T="
            r"\begin{bmatrix}"
            r"x_1\\"
            r"x_2\\"
            r"x_3"
            r"\end{bmatrix}",
            font_size=40,
            color=BLACK,
        )

        column.move_to(
            RIGHT * 2.7 + DOWN * 0.4
        )

        self.play(
            Write(row_title),
            Write(row),
        )

        self.flash(row)

        self.play(
            GrowArrow(arrow),
            run_time=0.7,
        )

        # Explicit transformation:
        # each entry moves from horizontal positions
        # into vertical positions.

        row_entries = [
            MathTex(r"x_1", font_size=40, color=BLACK),
            MathTex(r"x_2", font_size=40, color=BLACK),
            MathTex(r"x_3", font_size=40, color=BLACK),
        ]

        for i, entry in enumerate(row_entries):
            entry.move_to(
                row.get_center()
                + RIGHT * (i - 1) * 0.65
            )

        # Replace visual row with individual entries
        self.play(
            FadeOut(row),
            run_time=0.4,
        )

        self.add(*row_entries)

        target_positions = [
            column.get_center() + UP * 0.65,
            column.get_center(),
            column.get_center() + DOWN * 0.65,
        ]

        for entry, target in zip(
            row_entries,
            target_positions,
        ):

            self.flash(entry)

            self.play(
                entry.animate.move_to(target),
                run_time=0.8,
                rate_func=smooth,
            )

        final_column = column.copy()

        self.play(
            FadeIn(final_column),
            run_time=0.5,
        )

        self.play(
            FadeOut(
                row_title,
                *row_entries,
                final_column,
                arrow,
            )
        )

        # ======================================================
        # 2. SCALAR TRANSPOSE
        # ======================================================

        scalar_title = Text(
            "A scalar is its own transpose",
            font_size=28,
            color=BLACK,
        )

        scalar_title.next_to(
            title,
            DOWN,
            buff=0.4,
        )

        scalar = MathTex(
            r"a",
            font_size=52,
            color=BLACK,
        )

        scalar_T = MathTex(
            r"a^T",
            font_size=52,
            color=BLACK,
        )

        scalar.move_to(LEFT * 2)
        scalar_T.move_to(RIGHT * 2)

        scalar_arrow = Arrow(
            LEFT * 0.65,
            RIGHT * 0.65,
            color=BLACK,
            stroke_width=3,
            buff=0,
        )

        self.write(scalar_title)
        self.write(scalar)

        self.flash(scalar)

        self.play(
            GrowArrow(scalar_arrow),
            run_time=0.6,
        )

        self.play(
            TransformFromCopy(
                scalar,
                scalar_T,
            ),
            run_time=1,
        )

        scalar_rule = MathTex(
            r"a^T=a",
            font_size=38,
            color=BLACK,
        )

        scalar_rule.to_edge(
            DOWN,
            buff=0.4,
        )

        self.write(scalar_rule)

        self.wait(1)

        self.play(
            FadeOut(
                scalar_title,
                scalar,
                scalar_T,
                scalar_arrow,
                scalar_rule,
            )
        )

        # ======================================================
        # 3. MATRIX ADDITION
        # ======================================================

        add_title = Text(
            "Matrix addition: corresponding elements are added",
            font_size=27,
            color=BLACK,
        )

        add_title.next_to(
            title,
            DOWN,
            buff=0.4,
        )

        A, A_entries = self.make_matrix(
            [
                [r"a_{11}", r"a_{12}"],
                [r"a_{21}", r"a_{22}"],
            ],
            LEFT * 3.0 + DOWN * 0.35,
            font_size=28,
        )

        B, B_entries = self.make_matrix(
            [
                [r"b_{11}", r"b_{12}"],
                [r"b_{21}", r"b_{22}"],
            ],
            LEFT * 0.3 + DOWN * 0.35,
            font_size=28,
        )

        C, C_entries = self.make_matrix(
            [
                [r"a_{11}+b_{11}", r"a_{12}+b_{12}"],
                [r"a_{21}+b_{21}", r"a_{22}+b_{22}"],
            ],
            RIGHT * 3.0 + DOWN * 0.35,
            font_size=25,
        )

        plus1 = MathTex(
            r"+",
            font_size=35,
        ).move_to(
            LEFT * 1.65 + DOWN * 0.35
        )

        equals1 = MathTex(
            r"=",
            font_size=35,
        ).move_to(
            RIGHT * 1.35 + DOWN * 0.35
        )

        self.write(add_title)

        self.play(
            FadeIn(A),
            FadeIn(B),
            Write(plus1),
            Write(equals1),
        )

        # Flash corresponding elements before their transformation.
        for a_entry, b_entry, c_entry in zip(
            A_entries,
            B_entries,
            C_entries,
        ):

            self.flash(a_entry)
            self.flash(b_entry)

            self.play(
                Indicate(
                    c_entry,
                    color=GREEN,
                    scale_factor=1.1,
                ),
                run_time=0.35,
            )

        self.play(
            FadeIn(C),
            run_time=0.8,
        )

        addition_rule = MathTex(
            r"C_{i,j}=A_{i,j}+B_{i,j}",
            font_size=32,
            color=BLACK,
        )

        addition_rule.to_edge(
            DOWN,
            buff=0.4,
        )

        self.write(addition_rule)

        self.wait(1)

        self.play(
            FadeOut(
                add_title,
                A,
                B,
                C,
                plus1,
                equals1,
                addition_rule,
            )
        )

        # ======================================================
        # 4. SCALAR OPERATION
        # ======================================================

        scalar_matrix_title = Text(
            "Scalar multiplication and addition",
            font_size=28,
            color=BLACK,
        )

        scalar_matrix_title.next_to(
            title,
            DOWN,
            buff=0.4,
        )

        B2, B2_entries = self.make_matrix(
            [
                [r"b_{11}", r"b_{12}"],
                [r"b_{21}", r"b_{22}"],
            ],
            LEFT * 2.6 + DOWN * 0.35,
            font_size=28,
        )

        expression = MathTex(
            r"a\cdot B+c",
            font_size=34,
            color=BLACK,
        )

        expression.move_to(
            ORIGIN + DOWN * 0.35
        )

        result = MathTex(
            r"D",
            font_size=40,
            color=BLACK,
        )

        result.move_to(
            RIGHT * 2.8 + DOWN * 0.35
        )

        self.write(scalar_matrix_title)
        self.play(
            FadeIn(B2),
            Write(expression),
            Write(result),
        )

        self.flash(B2)

        scalar_rule2 = MathTex(
            r"D_{i,j}=a\cdot B_{i,j}+c",
            font_size=32,
            color=BLACK,
        )

        scalar_rule2.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(scalar_rule2)
        )

        self.wait(1)

        self.play(
            FadeOut(
                scalar_matrix_title,
                B2,
                expression,
                result,
                scalar_rule2,
            )
        )

        # ======================================================
        # 5. BROADCASTING
        # ======================================================

        broadcast_title = Text(
            "Broadcasting: one vector is added to every row",
            font_size=28,
            color=BLACK,
        )

        broadcast_title.next_to(
            title,
            DOWN,
            buff=0.4,
        )

        matrix_center = LEFT * 2.4 + DOWN * 0.25

        big_A, big_entries = self.make_matrix(
            [
                [r"a_{11}", r"a_{12}", r"a_{13}"],
                [r"a_{21}", r"a_{22}", r"a_{23}"],
                [r"a_{31}", r"a_{32}", r"a_{33}"],
            ],
            matrix_center,
            cell_w=0.75,
            cell_h=0.65,
            font_size=25,
        )

        vector = MathTex(
            r"\mathbf b="
            r"\begin{bmatrix}"
            r"b_1&b_2&b_3"
            r"\end{bmatrix}",
            font_size=28,
            color=BLACK,
        )

        vector.move_to(
            RIGHT * 2.8 + UP * 0.9
        )

        broadcast_arrow = Arrow(
            vector.get_bottom(),
            matrix_center + RIGHT * 0.4,
            color=BLACK,
            stroke_width=3,
            buff=0.15,
        )

        self.write(broadcast_title)
        self.play(
            FadeIn(big_A),
            Write(vector),
        )

        self.flash(vector)

        self.play(
            GrowArrow(broadcast_arrow),
            run_time=0.8,
        )

        # Explicitly show copies of b moving toward each row.
        copies = VGroup()

        for row_y in [
            matrix_center[1] + 0.65,
            matrix_center[1],
            matrix_center[1] - 0.65,
        ]:

            copy = vector.copy()

            copy.scale(0.75)

            copy.move_to(
                RIGHT * 3.0 + row_y * UP
            )

            copies.add(copy)

        self.play(
            LaggedStart(
                *[
                    TransformFromCopy(
                        vector,
                        copy,
                    )
                    for copy in copies
                ],
                lag_ratio=0.25,
                run_time=1.8,
            )
        )

        self.wait(0.5)

        broadcast_formula = MathTex(
            r"C=A+\mathbf b",
            font_size=34,
            color=BLACK,
        )

        broadcast_formula.to_edge(
            DOWN,
            buff=0.4,
        )

        self.write(broadcast_formula)

        self.wait(1)

        self.play(
            FadeOut(
                broadcast_title,
                big_A,
                vector,
                broadcast_arrow,
                copies,
                broadcast_formula,
            )
        )

        # ======================================================
        # 6. MATRIX MULTIPLICATION
        # ======================================================

        multiplication_title = Text(
            "Matrix multiplication",
            font_size=30,
            color=BLACK,
        )

        multiplication_title.next_to(
            title,
            DOWN,
            buff=0.4,
        )

        A3, A3_entries = self.make_matrix(
            [
                [r"a_{11}", r"a_{12}", r"a_{13}"],
                [r"a_{21}", r"a_{22}", r"a_{23}"],
            ],
            LEFT * 3.5 + DOWN * 0.3,
            cell_w=0.7,
            font_size=24,
        )

        B3, B3_entries = self.make_matrix(
            [
                [r"b_{11}", r"b_{12}"],
                [r"b_{21}", r"b_{22}"],
                [r"b_{31}", r"b_{32}"],
            ],
            ORIGIN + DOWN * 0.3,
            cell_w=0.7,
            font_size=24,
        )

        C3, C3_entries = self.make_matrix(
            [
                [r"c_{11}", r"c_{12}"],
                [r"c_{21}", r"c_{22}"],
            ],
            RIGHT * 3.5 + DOWN * 0.3,
            cell_w=0.7,
            font_size=24,
        )

        multiplication = MathTex(
            r"AB=C",
            font_size=32,
        )

        multiplication.to_edge(
            DOWN,
            buff=0.4,
        )

        self.write(multiplication_title)

        self.play(
            FadeIn(A3),
            FadeIn(B3),
            FadeIn(C3),
        )

        self.flash(A3)
        self.flash(B3)

        dimensions = MathTex(
            r"(m\times n)(n\times p)=(m\times p)",
            font_size=30,
            color=BLACK,
        )

        dimensions.next_to(
            multiplication_title,
            DOWN,
            buff=0.35,
        )

        self.write(dimensions)

        self.wait(1)

        # ======================================================
        # 7. EXPLICIT DOT PRODUCT FOR C_11
        # ======================================================

        self.play(
            FadeOut(
                dimensions,
                A3,
                B3,
                C3,
                multiplication,
                multiplication_title,
            )
        )

        dot_title = Text(
            "Each output element is a dot product",
            font_size=29,
            color=BLACK,
        )

        dot_title.to_edge(
            UP,
            buff=0.7,
        )

        row = MathTex(
            r"\\begin{bmatrix}a_{11}&a_{12}&a_{13}\\end{bmatrix}",
            font_size=35,
            color=BLACK,
        )

        column = MathTex(
            r"\\begin{bmatrix}b_{11}\\\\b_{21}\\\\b_{31}\\end{bmatrix}",
            font_size=35,
            color=BLACK,
        )

        row.move_to(
            LEFT * 2.5
        )

        column.move_to(
            RIGHT * 0.5
        )

        dot_arrow = Arrow(
            LEFT * 0.7,
            RIGHT * 0.7,
            color=BLACK,
            stroke_width=3,
            buff=0,
        )

        dot_arrow.move_to(
            LEFT * 1.0
        )

        result_c11 = MathTex(
            r"C_{1,1}",
            font_size=38,
            color=BLACK,
        )

        result_c11.move_to(
            RIGHT * 3.0
        )

        self.write(dot_title)
        self.play(
            Write(row),
            Write(column),
        )

        self.flash(row)
        self.flash(column)

        self.play(
            GrowArrow(dot_arrow),
            run_time=0.7,
        )

        calculation = MathTex(
            r"C_{1,1}"
            r"="
            r"a_{11}b_{11}"
            r"+"
            r"a_{12}b_{21}"
            r"+"
            r"a_{13}b_{31}",
            font_size=30,
            color=BLACK,
        )

        calculation.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(result_c11),
            Write(calculation),
        )

        self.wait(2)

        self.play(
            FadeOut(
                dot_title,
                row,
                column,
                dot_arrow,
                result_c11,
                calculation,
            )
        )

        # ======================================================
        # 8. HADAMARD PRODUCT
        # ======================================================

        hadamard_title = Text(
            "Element-wise multiplication: Hadamard product",
            font_size=27,
            color=BLACK,
        )

        hadamard_title.to_edge(
            UP,
            buff=0.7,
        )

        H1, H1_entries = self.make_matrix(
            [
                [r"a_{11}", r"a_{12}"],
                [r"a_{21}", r"a_{22}"],
            ],
            LEFT * 2.5,
            font_size=28,
        )

        H2, H2_entries = self.make_matrix(
            [
                [r"b_{11}", r"b_{12}"],
                [r"b_{21}", r"b_{22}"],
            ],
            ORIGIN,
            font_size=28,
        )

        H3, H3_entries = self.make_matrix(
            [
                [r"a_{11}b_{11}", r"a_{12}b_{12}"],
                [r"a_{21}b_{21}", r"a_{22}b_{22}"],
            ],
            RIGHT * 2.8,
            font_size=25,
        )

        hadamard_symbol = MathTex(
            r"\odot",
            font_size=34,
        ).move_to(
            LEFT * 1.25
        )

        hadamard_equals = MathTex(
            r"=",
            font_size=34,
        ).move_to(
            RIGHT * 1.3
        )

        hadamard_formula = MathTex(
            r"A\odot B",
            font_size=35,
        )

        hadamard_formula.to_edge(
            DOWN,
            buff=0.4,
        )

        self.write(hadamard_title)

        self.play(
            FadeIn(H1),
            FadeIn(H2),
            FadeIn(H3),
            Write(hadamard_symbol),
            Write(hadamard_equals),
        )

        for a_entry, b_entry in zip(
            H1_entries,
            H2_entries,
        ):
            self.flash(a_entry)
            self.flash(b_entry)

        self.play(
            Indicate(
                H3_entries,
                color=GREEN,
                scale_factor=1.08,
            ),
            run_time=0.8,
        )

        self.write(hadamard_formula)

        self.wait(2)

        self.play(
            FadeOut(
                hadamard_title,
                H1,
                H2,
                H3,
                hadamard_symbol,
                hadamard_equals,
                hadamard_formula,
            )
        )

        # ======================================================
        # 9. VECTOR DOT PRODUCT
        # ======================================================

        dot_product_title = Text(
            "Vector dot product",
            font_size=30,
            color=BLACK,
        )

        dot_product_title.to_edge(
            UP,
            buff=0.7,
        )

        x = MathTex(
            r"\mathbf{x}^T="
            r"\begin{bmatrix}"
            r"x_1&x_2&x_3"
            r"\end{bmatrix}",
            font_size=34,
        )

        y = MathTex(
            r"\mathbf{y}="
            r"\begin{bmatrix}"
            r"y_1\\"
            r"y_2\\"
            r"y_3"
            r"\end{bmatrix}",
            font_size=34,
        )

        x.move_to(
            LEFT * 2.4
        )

        y.move_to(
            ORIGIN
        )

        dot_symbol = MathTex(
            r"\cdot",
            font_size=35,
        ).move_to(
            LEFT * 1.0
        )

        result = MathTex(
            r"\mathbf{x}^T\mathbf{y}",
            font_size=36,
        )

        result.move_to(
            RIGHT * 2.6
        )

        self.write(dot_product_title)

        self.play(
            Write(x),
            Write(y),
        )

        self.flash(x)
        self.flash(y)

        self.play(
            Write(dot_symbol),
            run_time=0.5,
        )

        self.play(
            TransformFromCopy(
                x,
                result,
            ),
            run_time=1,
        )

        dot_formula = MathTex(
            r"\mathbf{x}^T\mathbf{y}"
            r"="
            r"x_1y_1+x_2y_2+x_3y_3",
            font_size=31,
            color=BLACK,
        )

        dot_formula.to_edge(
            DOWN,
            buff=0.4,
        )

        self.write(dot_formula)

        self.wait(2)

        # ======================================================
        # FINAL SUMMARY
        # ======================================================

        self.play(
            FadeOut(
                dot_product_title,
                x,
                y,
                dot_symbol,
                result,
                dot_formula,
            )
        )

        summary_title = Text(
            "The key idea",
            font_size=32,
            color=BLACK,
        )

        summary_title.to_edge(
            UP,
            buff=0.8,
        )

        summary = VGroup(
            MathTex(
                r"C=A+B",
                font_size=34,
            ),
            MathTex(
                r"D=aB+c",
                font_size=34,
            ),
            MathTex(
                r"C=A+\mathbf b",
                font_size=34,
            ),
            MathTex(
                r"C=AB",
                font_size=34,
            ),
            MathTex(
                r"\mathbf{x}^T\mathbf{y}",
                font_size=34,
            ),
        )

        summary.arrange(
            DOWN,
            buff=0.35,
        )

        summary.move_to(
            DOWN * 0.25
        )

        self.write(summary_title)

        for item in summary:

            self.flash(
                item,
                color=YELLOW,
            )

            self.play(
                Write(item),
                run_time=0.5,
            )

        self.wait(3)
