from manim import *


class Figure215(Scene):

    def construct(self):

        # ============================================================
        # GLOBAL STYLE
        # ============================================================

        BG = WHITE
        TEXT = BLACK
        BLUE = BLUE_D
        GREEN = GREEN_D
        RED = RED_D
        PURPLE = PURPLE_D

        self.camera.background_color = BG

        # ============================================================
        # HELPERS
        # ============================================================

        def title(text, y=3.25):
            t = Text(
                text,
                font_size=28,
                color=TEXT,
                weight=BOLD,
            )
            t.move_to(UP * y)
            return t

        def flash(mob, color=YELLOW):
            self.play(
                Indicate(
                    mob,
                    color=color,
                    scale_factor=1.08,
                ),
                run_time=0.45,
            )

        def section_label(text, y):
            t = Text(
                text,
                font_size=22,
                color=TEXT,
                weight=BOLD,
            )
            t.move_to(UP * y)
            return t

        # ============================================================
        # TITLE
        # ============================================================

        heading = title(
            "Singular Value Decomposition",
            3.25,
        )

        self.play(Write(heading), run_time=0.8)
        self.wait(0.6)

        # ============================================================
        # PART 1 — EIGEN DECOMPOSITION
        # ============================================================

        eigen_label = section_label(
            "Eigen-decomposition",
            2.55,
        )

        eigen_formula = MathTex(
            r"A = V\,\operatorname{diag}(\lambda)\,V^{-1}",
            font_size=34,
            color=TEXT,
        )

        eigen_formula.move_to(UP * 1.85)

        self.play(
            Write(eigen_label),
            run_time=0.5,
        )

        self.play(
            Write(eigen_formula),
            run_time=0.8,
        )

        self.wait(0.8)

        # ============================================================
        # TRANSITION TO SVD
        # ============================================================

        transition = Text(
            "SVD uses three structured matrices",
            font_size=21,
            color=BLUE,
        )

        transition.move_to(UP * 1.15)

        self.play(
            FadeIn(transition, shift=UP * 0.15),
            run_time=0.6,
        )

        self.wait(0.5)

        # Remove old explanation before introducing new equation
        self.play(
            FadeOut(eigen_label),
            FadeOut(eigen_formula),
            FadeOut(transition),
            run_time=0.5,
        )

        # ============================================================
        # PART 2 — SVD EQUATION
        # ============================================================

        svd_label = section_label(
            "Singular Value Decomposition",
            2.55,
        )

        svd_formula = MathTex(
            r"A = UDV^{\mathsf T}",
            font_size=42,
            color=TEXT,
        )

        svd_formula.move_to(UP * 1.65)

        self.play(
            Write(svd_label),
            run_time=0.5,
        )

        self.play(
            Write(svd_formula),
            run_time=0.8,
        )

        self.wait(0.7)

        # ============================================================
        # HIGHLIGHT THE THREE FACTORS
        # ============================================================

        U_box = SurroundingRectangle(
            svd_formula[0][0],
            color=BLUE,
            buff=0.12,
            stroke_width=2,
        )

        D_box = SurroundingRectangle(
            svd_formula[0][2],
            color=GREEN,
            buff=0.12,
            stroke_width=2,
        )

        V_box = SurroundingRectangle(
            svd_formula[0][4:],
            color=PURPLE,
            buff=0.12,
            stroke_width=2,
        )

        self.play(
            Create(U_box),
            run_time=0.35,
        )

        U_text = Text(
            "U  — left-singular vectors",
            font_size=20,
            color=BLUE,
        )
        U_text.move_to(LEFT * 3.3 + DOWN * 0.15)

        self.play(
            FadeIn(U_text),
            run_time=0.5,
        )

        self.wait(0.3)

        self.play(
            FadeOut(U_box),
            FadeOut(U_text),
            run_time=0.25,
        )

        self.play(
            Create(D_box),
            run_time=0.35,
        )

        D_text = Text(
            "D  — singular values",
            font_size=20,
            color=GREEN,
        )
        D_text.move_to(DOWN * 0.15)

        self.play(
            FadeIn(D_text),
            run_time=0.5,
        )

        self.wait(0.3)

        self.play(
            FadeOut(D_box),
            FadeOut(D_text),
            run_time=0.25,
        )

        self.play(
            Create(V_box),
            run_time=0.35,
        )

        V_text = Text(
            "V  — right-singular vectors",
            font_size=20,
            color=PURPLE,
        )
        V_text.move_to(RIGHT * 3.2 + DOWN * 0.15)

        self.play(
            FadeIn(V_text),
            run_time=0.5,
        )

        self.wait(0.8)

        self.play(
            FadeOut(V_box),
            FadeOut(V_text),
            run_time=0.35,
        )

        # ============================================================
        # PART 3 — MATRIX DIMENSIONS
        # ============================================================

        dimensions_title = Text(
            "For A ∈ R^(m×n)",
            font_size=22,
            color=TEXT,
            weight=BOLD,
        )

        dimensions_title.move_to(DOWN * 0.65)

        self.play(
            Write(dimensions_title),
            run_time=0.5,
        )

        dimensions = VGroup(
            MathTex(
                r"U \in \mathbb{R}^{m\times m}",
                font_size=27,
                color=BLUE,
            ),
            MathTex(
                r"D \in \mathbb{R}^{m\times n}",
                font_size=27,
                color=GREEN,
            ),
            MathTex(
                r"V \in \mathbb{R}^{n\times n}",
                font_size=27,
                color=PURPLE,
            ),
        )

        dimensions.arrange(
            DOWN,
            buff=0.38,
        )

        dimensions.move_to(DOWN * 1.55)

        self.play(
            LaggedStart(
                *[Write(x) for x in dimensions],
                lag_ratio=0.18,
            ),
            run_time=1.3,
        )

        self.wait(1)

        # ============================================================
        # CLEAR EVERYTHING BEFORE NEXT CONCEPT
        # ============================================================

        self.play(
            FadeOut(svd_label),
            FadeOut(svd_formula),
            FadeOut(dimensions_title),
            FadeOut(dimensions),
            run_time=0.6,
        )

        # ============================================================
        # PART 4 — ORTHOGONAL STRUCTURE
        # ============================================================

        orth_title = section_label(
            "The structure of SVD",
            2.55,
        )

        self.play(
            Write(orth_title),
            run_time=0.5,
        )

        U_orth = MathTex(
            r"U^{\mathsf T}U = I",
            font_size=34,
            color=BLUE,
        )

        V_orth = MathTex(
            r"V^{\mathsf T}V = I",
            font_size=34,
            color=PURPLE,
        )

        U_orth.move_to(LEFT * 2.25 + UP * 1.15)
        V_orth.move_to(RIGHT * 2.25 + UP * 1.15)

        self.play(
            Write(U_orth),
            Write(V_orth),
            run_time=0.8,
        )

        self.wait(0.8)

        # ============================================================
        # SINGULAR VALUES
        # ============================================================

        singular_label = Text(
            "Diagonal entries of D are the singular values",
            font_size=21,
            color=TEXT,
        )

        singular_label.move_to(DOWN * 0.05)

        D_matrix = MathTex(
            r"D = \\begin{bmatrix}"
            r"\\sigma_1 & 0 & 0 \\\\"
            r"0 & \\sigma_2 & 0 \\\\"
            r"0 & 0 & \\sigma_3"
            r"\\end{bmatrix}",
            font_size=30,
            color=GREEN,
        )

        D_matrix.move_to(DOWN * 1.05)

        self.play(
            Write(singular_label),
            run_time=0.5,
        )

        self.play(
            Write(D_matrix),
            run_time=0.9,
        )

        self.wait(1)

        self.play(
            FadeOut(orth_title),
            FadeOut(U_orth),
            FadeOut(V_orth),
            FadeOut(singular_label),
            FadeOut(D_matrix),
            run_time=0.6,
        )

        # ============================================================
        # PART 5 — WHY SVD IS USEFUL
        # ============================================================

        useful_title = section_label(
            "Why SVD is useful",
            2.55,
        )

        self.play(
            Write(useful_title),
            run_time=0.5,
        )

        left_vec = MathTex(
            r"AA^{\mathsf T}",
            font_size=36,
            color=BLUE,
        )

        right_vec = MathTex(
            r"A^{\mathsf T}A",
            font_size=36,
            color=PURPLE,
        )

        left_desc = Text(
            "left-singular vectors",
            font_size=19,
            color=BLUE,
        )

        right_desc = Text(
            "right-singular vectors",
            font_size=19,
            color=PURPLE,
        )

        left_group = VGroup(
            left_vec,
            left_desc,
        ).arrange(
            DOWN,
            buff=0.28,
        )

        right_group = VGroup(
            right_vec,
            right_desc,
        ).arrange(
            DOWN,
            buff=0.28,
        )

        left_group.move_to(LEFT * 2.7 + UP * 0.9)
        right_group.move_to(RIGHT * 2.7 + UP * 0.9)

        self.play(
            Write(left_vec),
            FadeIn(left_desc),
            Write(right_vec),
            FadeIn(right_desc),
            run_time=0.9,
        )

        self.wait(0.8)

        singular_relation = MathTex(
            r"\sigma_i = \sqrt{\lambda_i}",
            font_size=34,
            color=GREEN,
        )

        singular_relation.move_to(DOWN * 0.35)

        self.play(
            Write(singular_relation),
            run_time=0.7,
        )

        self.wait(1)

        # ============================================================
        # PART 6 — PSEUDOINVERSE INTRODUCTION
        # ============================================================

        self.play(
            FadeOut(useful_title),
            FadeOut(left_group),
            FadeOut(right_group),
            FadeOut(singular_relation),
            run_time=0.6,
        )

        pseudo_title = section_label(
            "Moore–Penrose Pseudoinverse",
            2.55,
        )

        self.play(
            Write(pseudo_title),
            run_time=0.6,
        )

        nonsquare = Text(
            "Matrix inversion is not defined for nonsquare matrices.",
            font_size=22,
            color=TEXT,
        )

        nonsquare.move_to(UP * 1.45)

        self.play(
            Write(nonsquare),
            run_time=0.65,
        )

        self.wait(0.7)

        # ============================================================
        # LINEAR EQUATION
        # ============================================================

        equation1 = MathTex(
            r"A\mathbf{x}=\mathbf{y}",
            font_size=42,
            color=TEXT,
        )

        equation1.move_to(UP * 0.55)

        self.play(
            Write(equation1),
            run_time=0.7,
        )

        self.wait(0.6)

        flash(equation1, YELLOW)

        # ============================================================
        # LEFT MULTIPLICATION
        # ============================================================

        arrow = Arrow(
            LEFT * 0.8,
            RIGHT * 0.8,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )

        arrow.move_to(DOWN * 0.35)

        left_multiply = MathTex(
            r"\text{left-multiply by }B",
            font_size=22,
            color=RED,
        )

        left_multiply.next_to(
            arrow,
            DOWN,
            buff=0.18,
        )

        self.play(
            GrowArrow(arrow),
            FadeIn(left_multiply),
            run_time=0.6,
        )

        self.wait(0.5)

        self.play(
            FadeOut(arrow),
            FadeOut(left_multiply),
            run_time=0.35,
        )

        # ============================================================
        # RESULT
        # ============================================================

        equation2 = MathTex(
            r"\mathbf{x}=B\mathbf{y}",
            font_size=42,
            color=GREEN,
        )

        equation2.move_to(DOWN * 1.15)

        self.play(
            TransformFromCopy(
                equation1,
                equation2,
            ),
            run_time=0.9,
        )

        self.wait(0.7)

        flash(equation2, GREEN)

        # ============================================================
        # FINAL CONCEPT
        # ============================================================

        final = Text(
            "SVD provides the structure needed to generalize inversion.",
            font_size=20,
            color=BLUE,
        )

        final.move_to(DOWN * 2.15)

        self.play(
            Write(final),
            run_time=0.75,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure215().render()
