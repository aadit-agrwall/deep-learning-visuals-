from manim import *


class Figure216(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        # ============================================================
        # COLORS
        # ============================================================

        TEXT = BLACK
        BLUE = BLUE_D
        GREEN = GREEN_D
        RED = RED_D
        PURPLE = PURPLE_D
        ORANGE_COLOR = ORANGE

        # ============================================================
        # HELPERS
        # ============================================================

        def write(mob, runtime=0.7):
            self.play(
                Write(mob),
                run_time=runtime,
            )

        def flash(mob, color=YELLOW):
            self.play(
                Indicate(
                    mob,
                    color=color,
                    scale_factor=1.06,
                ),
                run_time=0.4,
            )

        def clear(*mobs):
            existing = [m for m in mobs if m is not None]
            if existing:
                self.play(
                    *[FadeOut(m) for m in existing],
                    run_time=0.45,
                )

        # ============================================================
        # TITLE
        # ============================================================

        title = Text(
            "Moore–Penrose Pseudoinverse",
            font_size=30,
            color=TEXT,
            weight=BOLD,
        )

        title.to_edge(UP, buff=0.45)

        write(title, 0.75)
        self.wait(0.5)

        # ============================================================
        # 1. TALL VS WIDE MATRICES
        # ============================================================

        situation = Text(
            "The shape of A determines the kind of solution",
            font_size=22,
            color=TEXT,
        )

        situation.move_to(UP * 2.05)

        write(situation, 0.6)

        # ------------------------------------------------------------
        # Tall matrix
        # ------------------------------------------------------------

        tall_matrix = MathTex(
            r"A \in \mathbb{R}^{m\times n}",
            font_size=34,
            color=BLUE,
        )

        tall_matrix.move_to(LEFT * 3.0 + UP * 0.9)

        tall_label = Text(
            "taller than wide",
            font_size=20,
            color=BLUE,
        )

        tall_label.next_to(
            tall_matrix,
            DOWN,
            buff=0.25,
        )

        tall_result = Text(
            "may have no solution",
            font_size=20,
            color=RED,
        )

        tall_result.next_to(
            tall_label,
            DOWN,
            buff=0.35,
        )

        # ------------------------------------------------------------
        # Wide matrix
        # ------------------------------------------------------------

        wide_matrix = MathTex(
            r"A \in \mathbb{R}^{m\times n}",
            font_size=34,
            color=PURPLE,
        )

        wide_matrix.move_to(RIGHT * 3.0 + UP * 0.9)

        wide_label = Text(
            "wider than tall",
            font_size=20,
            color=PURPLE,
        )

        wide_label.next_to(
            wide_matrix,
            DOWN,
            buff=0.25,
        )

        wide_result = Text(
            "may have multiple solutions",
            font_size=20,
            color=GREEN,
        )

        wide_result.next_to(
            wide_label,
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(tall_matrix),
            Write(wide_matrix),
            run_time=0.7,
        )

        self.play(
            FadeIn(tall_label),
            FadeIn(wide_label),
            run_time=0.45,
        )

        self.play(
            FadeIn(tall_result),
            FadeIn(wide_result),
            run_time=0.55,
        )

        self.wait(1)

        flash(tall_result, RED)
        flash(wide_result, GREEN)

        clear(
            situation,
            tall_matrix,
            tall_label,
            tall_result,
            wide_matrix,
            wide_label,
            wide_result,
        )

        # ============================================================
        # 2. PSEUDOINVERSE DEFINITION
        # ============================================================

        definition_title = Text(
            "The Moore–Penrose pseudoinverse",
            font_size=25,
            color=TEXT,
            weight=BOLD,
        )

        definition_title.move_to(UP * 2.25)

        write(definition_title, 0.55)

        definition_text = Text(
            "extends the idea of matrix inversion",
            font_size=21,
            color=TEXT,
        )

        definition_text.move_to(UP * 1.55)

        write(definition_text, 0.55)

        pseudo_formula = MathTex(
            r"A^{+}"
            r"="
            r"\lim_{\alpha\to0}"
            r"\left(A^{\mathsf T}A+\alpha I\right)^{-1}"
            r"A^{\mathsf T}",
            font_size=35,
            color=TEXT,
        )

        pseudo_formula.move_to(DOWN * 0.05)

        write(pseudo_formula, 0.9)

        flash(pseudo_formula, BLUE)

        definition_note = Text(
            "theoretical definition",
            font_size=19,
            color=BLUE,
        )

        definition_note.move_to(DOWN * 0.95)

        write(definition_note, 0.5)

        self.wait(1)

        clear(
            definition_title,
            definition_text,
            pseudo_formula,
            definition_note,
        )

        # ============================================================
        # 3. PRACTICAL SVD FORM
        # ============================================================

        practical_title = Text(
            "In practice, use the SVD",
            font_size=26,
            color=TEXT,
            weight=BOLD,
        )

        practical_title.move_to(UP * 2.3)

        write(practical_title, 0.55)

        svd_formula = MathTex(
            r"A^{+}=VD^{+}U^{\mathsf T}",
            font_size=42,
            color=TEXT,
        )

        svd_formula.move_to(UP * 1.2)

        write(svd_formula, 0.8)

        # ------------------------------------------------------------
        # Separate factor meanings
        # ------------------------------------------------------------

        factor_u = MathTex(
            r"U",
            font_size=34,
            color=BLUE,
        )

        factor_d = MathTex(
            r"D^{+}",
            font_size=34,
            color=GREEN,
        )

        factor_v = MathTex(
            r"V",
            font_size=34,
            color=PURPLE,
        )

        factor_u.move_to(LEFT * 3.3 + DOWN * 0.25)
        factor_d.move_to(DOWN * 0.25)
        factor_v.move_to(RIGHT * 3.3 + DOWN * 0.25)

        desc_u = Text(
            "left-singular\nvectors",
            font_size=18,
            color=BLUE,
            line_spacing=0.8,
        )

        desc_d = Text(
            "reciprocal\nsingular values",
            font_size=18,
            color=GREEN,
            line_spacing=0.8,
        )

        desc_v = Text(
            "right-singular\nvectors",
            font_size=18,
            color=PURPLE,
            line_spacing=0.8,
        )

        desc_u.next_to(factor_u, DOWN, buff=0.2)
        desc_d.next_to(factor_d, DOWN, buff=0.2)
        desc_v.next_to(factor_v, DOWN, buff=0.2)

        self.play(
            Write(factor_u),
            Write(factor_d),
            Write(factor_v),
            run_time=0.7,
        )

        self.play(
            FadeIn(desc_u),
            FadeIn(desc_d),
            FadeIn(desc_v),
            run_time=0.6,
        )

        self.wait(1)

        clear(
            practical_title,
            svd_formula,
            factor_u,
            factor_d,
            factor_v,
            desc_u,
            desc_d,
            desc_v,
        )

        # ============================================================
        # 4. WHAT D+ DOES
        # ============================================================

        d_title = Text(
            "Constructing D⁺",
            font_size=27,
            color=TEXT,
            weight=BOLD,
        )

        d_title.move_to(UP * 2.25)

        write(d_title, 0.55)

        d_original = MathTex(
            r"D=\begin{bmatrix}"
            r"\sigma_1&0&0\\"
            r"0&\sigma_2&0\\"
            r"0&0&\sigma_3"
            r"\end{bmatrix}",
            font_size=31,
            color=TEXT,
        )

        d_original.move_to(LEFT * 2.7 + UP * 0.75)

        d_arrow = Arrow(
            LEFT * 0.8,
            RIGHT * 0.8,
            color=ORANGE_COLOR,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )

        d_arrow.move_to(DOWN * 0.05)

        reciprocal = MathTex(
            r"\sigma_i\rightarrow\frac{1}{\sigma_i}",
            font_size=30,
            color=GREEN,
        )

        reciprocal.move_to(RIGHT * 2.55 + UP * 0.75)

        d_plus = MathTex(
            r"D^{+}=\begin{bmatrix}"
            r"\frac{1}{\sigma_1}&0&0\\"
            r"0&\frac{1}{\sigma_2}&0\\"
            r"0&0&\frac{1}{\sigma_3}"
            r"\end{bmatrix}",
            font_size=28,
            color=GREEN,
        )

        d_plus.move_to(RIGHT * 2.55 + DOWN * 0.55)

        self.play(
            Write(d_original),
            run_time=0.7,
        )

        self.play(
            GrowArrow(d_arrow),
            run_time=0.45,
        )

        self.play(
            Write(reciprocal),
            run_time=0.6,
        )

        self.play(
            Write(d_plus),
            run_time=0.8,
        )

        self.wait(1)

        flash(d_plus, GREEN)

        clear(
            d_title,
            d_original,
            d_arrow,
            reciprocal,
            d_plus,
        )

        # ============================================================
        # 5. MINIMUM NORM SOLUTION
        # ============================================================

        solution_title = Text(
            "When A has more columns than rows",
            font_size=25,
            color=TEXT,
            weight=BOLD,
        )

        solution_title.move_to(UP * 2.25)

        write(solution_title, 0.55)

        solution_text = Text(
            "there may be many possible solutions",
            font_size=21,
            color=TEXT,
        )

        solution_text.move_to(UP * 1.55)

        write(solution_text, 0.5)

        solution_formula = MathTex(
            r"\mathbf{x}=A^{+}\mathbf{y}",
            font_size=42,
            color=GREEN,
        )

        solution_formula.move_to(UP * 0.65)

        write(solution_formula, 0.7)

        minimum = MathTex(
            r"\text{minimum } \|\mathbf{x}\|_2",
            font_size=31,
            color=BLUE,
        )

        minimum.move_to(DOWN * 0.45)

        write(minimum, 0.65)

        minimum_note = Text(
            "among all possible solutions",
            font_size=20,
            color=TEXT,
        )

        minimum_note.move_to(DOWN * 1.25)

        write(minimum_note, 0.55)

        self.wait(1)

        flash(solution_formula, GREEN)

        clear(
            solution_title,
            solution_text,
            solution_formula,
            minimum,
            minimum_note,
        )

        # ============================================================
        # 6. LEAST-SQUARES INTERPRETATION
        # ============================================================

        least_title = Text(
            "When A has more rows than columns",
            font_size=25,
            color=TEXT,
            weight=BOLD,
        )

        least_title.move_to(UP * 2.25)

        write(least_title, 0.55)

        no_solution = Text(
            "there may be no exact solution",
            font_size=21,
            color=RED,
        )

        no_solution.move_to(UP * 1.5)

        write(no_solution, 0.55)

        least_formula = MathTex(
            r"\mathbf{x}=A^{+}\mathbf{y}",
            font_size=40,
            color=GREEN,
        )

        least_formula.move_to(UP * 0.65)

        write(least_formula, 0.7)

        error_formula = MathTex(
            r"\min_{\mathbf{x}}\|A\mathbf{x}-\mathbf{y}\|_2",
            font_size=34,
            color=BLUE,
        )

        error_formula.move_to(DOWN * 0.55)

        write(error_formula, 0.75)

        error_note = Text(
            "closest possible solution",
            font_size=20,
            color=TEXT,
        )

        error_note.move_to(DOWN * 1.4)

        write(error_note, 0.55)

        self.wait(1)

        flash(error_formula, BLUE)

        clear(
            least_title,
            no_solution,
            least_formula,
            error_formula,
            error_note,
        )

        # ============================================================
        # 7. TRACE OPERATOR
        # ============================================================

        trace_title = Text(
            "2.10  The Trace Operator",
            font_size=29,
            color=TEXT,
            weight=BOLD,
        )

        trace_title.move_to(UP * 2.3)

        write(trace_title, 0.65)

        trace_definition = Text(
            "The trace is the sum of the diagonal entries.",
            font_size=22,
            color=TEXT,
        )

        trace_definition.move_to(UP * 1.45)

        write(trace_definition, 0.55)

        trace_formula = MathTex(
            r"\operatorname{Tr}(A)=\sum_i A_{i,i}",
            font_size=40,
            color=TEXT,
        )

        trace_formula.move_to(UP * 0.45)

        write(trace_formula, 0.75)

        self.wait(0.7)

        # ------------------------------------------------------------
        # Matrix visualization
        # ------------------------------------------------------------

        matrix = MathTex(
            r"A=\begin{bmatrix}"
            r"a_{11}&a_{12}&a_{13}\\"
            r"a_{21}&a_{22}&a_{23}\\"
            r"a_{31}&a_{32}&a_{33}"
            r"\end{bmatrix}",
            font_size=30,
            color=TEXT,
        )

        matrix.move_to(LEFT * 2.6 + DOWN * 0.85)

        diag_label = Text(
            "diagonal",
            font_size=18,
            color=GREEN,
        )

        diag_label.move_to(RIGHT * 2.2 + DOWN * 0.85)

        diag_formula = MathTex(
            r"a_{11}+a_{22}+a_{33}",
            font_size=30,
            color=GREEN,
        )

        diag_formula.move_to(RIGHT * 2.55 + DOWN * 1.35)

        self.play(
            Write(matrix),
            run_time=0.7,
        )

        self.play(
            FadeIn(diag_label),
            Write(diag_formula),
            run_time=0.7,
        )

        self.wait(0.8)

        flash(diag_formula, GREEN)

        clear(
            trace_title,
            trace_definition,
            trace_formula,
            matrix,
            diag_label,
            diag_formula,
        )

        # ============================================================
        # 8. TRACE AND FROBENIUS NORM
        # ============================================================

        frob_title = Text(
            "Trace gives another form of the Frobenius norm",
            font_size=25,
            color=TEXT,
            weight=BOLD,
        )

        frob_title.move_to(UP * 2.25)

        write(frob_title, 0.6)

        frob_formula = MathTex(
            r"\|A\|_F=\sqrt{\operatorname{Tr}(AA^{\mathsf T})}",
            font_size=39,
            color=BLUE,
        )

        frob_formula.move_to(UP * 0.95)

        write(frob_formula, 0.8)

        connection = MathTex(
            r"\operatorname{Tr}(AA^{\mathsf T})"
            r"="
            r"\sum_{i,j}A_{i,j}^{\,2}",
            font_size=31,
            color=TEXT,
        )

        connection.move_to(DOWN * 0.25)

        write(connection, 0.7)

        final = Text(
            "Trace connects matrix structure to a familiar norm.",
            font_size=20,
            color=GREEN,
        )

        final.move_to(DOWN * 1.35)

        write(final, 0.6)

        self.wait(1)

        flash(frob_formula, BLUE)

        self.wait(1.5)


if __name__ == "__main__":
    Figure216().render()
