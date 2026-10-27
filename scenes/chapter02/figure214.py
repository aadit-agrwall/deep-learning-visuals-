from manim import *
import numpy as np


class Figure214(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        TEXT = BLACK
        GRID = GRAY_B
        BLUE = BLUE_D
        GREEN = GREEN_D
        RED = RED_D
        # YELLOW uses Manim's built-in YELLOW

        # ============================================================
        # HELPERS
        # ============================================================

        def flash(obj):
            self.play(
                Indicate(
                    obj,
                    color=YELLOW,
                    scale_factor=1.04,
                ),
                run_time=0.45,
            )

        def section_title(text, y=3.0):
            t = Text(
                text,
                font_size=27,
                color=TEXT,
            )
            t.move_to(UP * y)
            return t

        # ============================================================
        # 1. SPECTRAL DECOMPOSITION
        # ============================================================

        heading = section_title(
            "Eigendecomposition of a symmetric matrix"
        )

        self.play(
            Write(heading),
            run_time=0.8,
        )

        # Matrix A
        A = MathTex(
            r"A",
            font_size=48,
            color=TEXT,
        )

        A.move_to(LEFT * 4.4 + UP * 1.25)

        # Symmetry
        symmetric = MathTex(
            r"A=A^{\mathsf T}",
            font_size=30,
            color=TEXT,
        )

        symmetric.next_to(
            A,
            DOWN,
            buff=0.22,
        )

        self.play(
            Write(A),
            Write(symmetric),
            run_time=0.8,
        )

        flash(symmetric)

        # Arrow
        arrow1 = Arrow(
            LEFT * 2.9 + UP * 1.25,
            LEFT * 1.7 + UP * 1.25,
            color=GRID,
            stroke_width=2,
            buff=0.1,
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.5,
        )

        # Q
        Q = MathTex(
            r"Q",
            font_size=46,
            color=BLUE,
        )

        Q.move_to(
            LEFT * 1.15 + UP * 1.25
        )

        Q_desc = Text(
            "orthogonal eigenvectors",
            font_size=18,
            color=TEXT,
        )

        Q_desc.next_to(
            Q,
            DOWN,
            buff=0.18,
        )

        self.play(
            Write(Q),
            FadeIn(Q_desc),
            run_time=0.7,
        )

        # Lambda
        Lambda = MathTex(
            r"\Lambda",
            font_size=46,
            color=GREEN,
        )

        Lambda.move_to(
            RIGHT * 0.8 + UP * 1.25
        )

        Lambda_desc = Text(
            "eigenvalues",
            font_size=18,
            color=TEXT,
        )

        Lambda_desc.next_to(
            Lambda,
            DOWN,
            buff=0.18,
        )

        # Q transpose
        QT = MathTex(
            r"Q^{\mathsf T}",
            font_size=40,
            color=BLUE,
        )

        QT.move_to(
            RIGHT * 2.5 + UP * 1.25
        )

        self.play(
            Write(Lambda),
            FadeIn(Lambda_desc),
            Write(QT),
            run_time=0.8,
        )

        # Full equation
        equation = MathTex(
            r"A=Q\Lambda Q^{\mathsf T}",
            font_size=36,
            color=TEXT,
        )

        equation.move_to(
            DOWN * 0.15
        )

        self.play(
            Write(equation),
            run_time=0.9,
        )

        flash(equation)

        # Equation number
        eq_number = MathTex(
            r"(2.41)",
            font_size=22,
            color=TEXT,
        )

        eq_number.next_to(
            equation,
            RIGHT,
            buff=0.35,
        )

        self.play(
            Write(eq_number),
            run_time=0.4,
        )

        self.wait(1)

        # ============================================================
        # 2. EIGENVALUE CLASSIFICATION
        # ============================================================

        self.play(
            FadeOut(
                heading,
                A,
                symmetric,
                arrow1,
                Q,
                Q_desc,
                Lambda,
                Lambda_desc,
                QT,
                equation,
                eq_number,
            ),
            run_time=0.6,
        )

        classification_heading = section_title(
            "Eigenvalue signs classify the matrix"
        )

        self.play(
            Write(classification_heading),
            run_time=0.7,
        )

        # ------------------------------------------------------------
        # Four categories
        # ------------------------------------------------------------

        boxes = VGroup()

        names = [
            ("Positive definite", r"\lambda_i>0", GREEN),
            ("Positive semidefinite", r"\lambda_i\geq0", GREEN_D),
            ("Negative definite", r"\lambda_i<0", RED),
            ("Negative semidefinite", r"\lambda_i\leq0", RED_D),
        ]

        positions = [
            LEFT * 3.0 + UP * 1.35,
            RIGHT * 3.0 + UP * 1.35,
            LEFT * 3.0 + DOWN * 0.55,
            RIGHT * 3.0 + DOWN * 0.55,
        ]

        for (name, condition, color), position in zip(
            names,
            positions,
        ):

            name_text = Text(
                name,
                font_size=20,
                color=TEXT,
            )

            condition_tex = MathTex(
                condition,
                font_size=27,
                color=color,
            )

            content = VGroup(
                name_text,
                condition_tex,
            )

            content.arrange(
                DOWN,
                buff=0.18,
            )

            box = RoundedRectangle(
                width=4.7,
                height=1.35,
                corner_radius=0.12,
                stroke_color=color,
                stroke_width=2,
                fill_color=WHITE,
                fill_opacity=1,
            )

            content.move_to(box.get_center())

            group = VGroup(
                box,
                content,
            )

            group.move_to(position)

            boxes.add(group)

        for box in boxes:
            self.play(
                FadeIn(box),
                run_time=0.45,
            )

        # Flash each classification
        for box in boxes:
            flash(box)

        # ============================================================
        # 3. QUADRATIC FORM
        # ============================================================

        self.play(
            FadeOut(
                classification_heading,
                boxes,
            ),
            run_time=0.6,
        )

        q_heading = section_title(
            "Eigenvalues control the quadratic form"
        )

        self.play(
            Write(q_heading),
            run_time=0.7,
        )

        quadratic = MathTex(
            r"f(\mathbf{x})=\mathbf{x}^{\mathsf T}A\mathbf{x}",
            font_size=40,
            color=TEXT,
        )

        quadratic.move_to(
            UP * 1.45
        )

        constraint = MathTex(
            r"\|\mathbf{x}\|_2=1",
            font_size=30,
            color=TEXT,
        )

        constraint.next_to(
            quadratic,
            DOWN,
            buff=0.25,
        )

        self.play(
            Write(quadratic),
            Write(constraint),
            run_time=0.9,
        )

        flash(quadratic)

        # ------------------------------------------------------------
        # Number line for eigenvalues
        # ------------------------------------------------------------

        number_line = NumberLine(
            x_range=[-3, 3, 1],
            length=8.0,
            include_numbers=True,
            font_size=16,
            color=TEXT,
        )

        number_line.move_to(
            DOWN * 0.75
        )

        self.play(
            Create(number_line),
            run_time=0.8,
        )

        zero = MathTex(
            r"0",
            font_size=23,
            color=TEXT,
        )

        zero.next_to(
            number_line.n2p(0),
            DOWN,
            buff=0.25,
        )

        negative = Text(
            "negative",
            font_size=18,
            color=RED,
        )

        negative.next_to(
            number_line.n2p(-1.5),
            DOWN,
            buff=0.48,
        )

        positive = Text(
            "positive",
            font_size=18,
            color=GREEN,
        )

        positive.next_to(
            number_line.n2p(1.5),
            DOWN,
            buff=0.48,
        )

        self.play(
            Write(zero),
            FadeIn(negative),
            FadeIn(positive),
            run_time=0.6,
        )

        # Min / max eigenvalues
        min_lambda = MathTex(
            r"\lambda_{\min}",
            font_size=27,
            color=RED,
        )

        max_lambda = MathTex(
            r"\lambda_{\max}",
            font_size=27,
            color=GREEN,
        )

        min_lambda.next_to(
            number_line.n2p(-2.0),
            UP,
            buff=0.25,
        )

        max_lambda.next_to(
            number_line.n2p(2.0),
            UP,
            buff=0.25,
        )

        self.play(
            Write(min_lambda),
            Write(max_lambda),
            run_time=0.7,
        )

        flash(min_lambda)
        flash(max_lambda)

        result = MathTex(
            r"\min f=\lambda_{\min}",
            r"\qquad",
            r"\max f=\lambda_{\max}",
            font_size=29,
            color=TEXT,
        )

        result.move_to(
            DOWN * 2.25
        )

        self.play(
            Write(result),
            run_time=0.9,
        )

        self.wait(1)

        # ============================================================
        # 4. TRANSITION TO SVD
        # ============================================================

        self.play(
            FadeOut(
                q_heading,
                quadratic,
                constraint,
                number_line,
                zero,
                negative,
                positive,
                min_lambda,
                max_lambda,
                result,
            ),
            run_time=0.7,
        )

        svd_heading = section_title(
            "2.8  Singular Value Decomposition"
        )

        self.play(
            Write(svd_heading),
            run_time=0.8,
        )

        # ============================================================
        # 5. EIGEN DECOMPOSITION VS SVD
        # ============================================================

        eigen_label = Text(
            "Eigendecomposition",
            font_size=23,
            color=TEXT,
        )

        eigen_label.move_to(
            LEFT * 3.0 + UP * 1.65
        )

        eigen_formula = MathTex(
            r"A=Q\Lambda Q^{\mathsf T}",
            font_size=32,
            color=TEXT,
        )

        eigen_formula.next_to(
            eigen_label,
            DOWN,
            buff=0.3,
        )

        self.play(
            Write(eigen_label),
            Write(eigen_formula),
            run_time=0.8,
        )

        # Arrow between
        transition_arrow = Arrow(
            LEFT * 0.8 + UP * 1.05,
            RIGHT * 0.8 + UP * 1.05,
            color=GRID,
            stroke_width=2,
            buff=0.15,
        )

        self.play(
            GrowArrow(transition_arrow),
            run_time=0.5,
        )

        svd_label = Text(
            "Singular Value Decomposition",
            font_size=22,
            color=TEXT,
        )

        svd_label.move_to(
            RIGHT * 3.0 + UP * 1.65
        )

        svd_formula = MathTex(
            r"A=U\Sigma V^{\mathsf T}",
            font_size=32,
            color=BLUE,
        )

        svd_formula.next_to(
            svd_label,
            DOWN,
            buff=0.3,
        )

        self.play(
            Write(svd_label),
            Write(svd_formula),
            run_time=0.9,
        )

        flash(svd_formula)

        # ============================================================
        # 6. SVD COMPONENTS
        # ============================================================

        components = VGroup()

        component_data = [
            (r"U", "left singular vectors"),
            (r"\Sigma", "singular values"),
            (r"V^{\mathsf T}", "right singular vectors"),
        ]

        x_positions = [
            LEFT * 3.4,
            ORIGIN,
            RIGHT * 3.4,
        ]

        for (formula, description), x in zip(
            component_data,
            x_positions,
        ):

            symbol = MathTex(
                formula,
                font_size=38,
                color=TEXT,
            )

            desc = Text(
                description,
                font_size=17,
                color=TEXT,
            )

            group = VGroup(
                symbol,
                desc,
            )

            group.arrange(
                DOWN,
                buff=0.18,
            )

            group.move_to(
                x + DOWN * 0.25
            )

            components.add(group)

        self.play(
            FadeIn(components),
            run_time=0.9,
        )

        for component in components:
            flash(component)

        # ============================================================
        # 7. FINAL MESSAGE
        # ============================================================

        final = Text(
            "SVD applies to every real matrix.",
            font_size=25,
            color=TEXT,
        )

        final.move_to(
            DOWN * 2.25
        )

        self.play(
            Write(final),
            run_time=0.8,
        )

        self.play(
            Indicate(
                svd_formula,
                color=YELLOW,
                scale_factor=1.05,
            ),
            run_time=0.6,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure214().render()
