from manim import *


class Figure217(Scene):

    def construct(self):

        # ============================================================
        # COLORS
        # ============================================================

        BG = "#FFFFFF"
        TEXT = "#050505"
        MUTED = "#A8A8A8"

        BLUE_C = "#5DA9FF"
        GREEN_C = "#62D98B"
        YELLOW_C = "#FFD166"
        RED_C = "#FF6B6B"
        PURPLE_C = "#B794F4"

        self.camera.background_color = BG

        # ============================================================
        # HELPERS
        # ============================================================

        def flash(obj, color=YELLOW_C, scale=1.05):
            self.play(
                Indicate(
                    obj,
                    color=color,
                    scale_factor=scale,
                    rate_func=there_and_back,
                ),
                run_time=0.55,
            )

        def write(obj, runtime=0.8):
            self.play(
                Write(obj),
                run_time=runtime,
            )

        def clear_group(group):
            if len(group) > 0:
                self.play(
                    FadeOut(group),
                    run_time=0.45,
                )

        # ============================================================
        # TITLE
        # ============================================================

        title = Text(
            "Trace identities",
            font_size=34,
            color=TEXT,
        )

        title.to_edge(UP, buff=0.45)

        write(title, 0.7)
        self.wait(0.5)

        # ============================================================
        # 1. TRACE IS INVARIANT TO TRANSPOSE
        # ============================================================

        subtitle = Text(
            "Transpose does not change the trace",
            font_size=22,
            color=MUTED,
        )

        subtitle.next_to(title, DOWN, buff=0.3)

        write(subtitle, 0.55)

        formula_1 = MathTex(
            r"\operatorname{Tr}(A)"
            r"="
            r"\operatorname{Tr}(A^{\mathsf T})",
            font_size=40,
            color=TEXT,
        )

        formula_1.move_to(ORIGIN + DOWN * 0.25)

        write(formula_1, 0.9)

        flash(formula_1, BLUE_C)

        self.wait(0.8)

        # ============================================================
        # 2. CYCLIC PERMUTATION
        # ============================================================

        new_subtitle = Text(
            "Factors can move cyclically",
            font_size=22,
            color=MUTED,
        )

        new_subtitle.move_to(subtitle)

        self.play(
            Transform(subtitle, new_subtitle),
            FadeOut(formula_1),
            run_time=0.45,
        )

        formula_2 = MathTex(
            r"\operatorname{Tr}(ABC)"
            r"="
            r"\operatorname{Tr}(CAB)"
            r"="
            r"\operatorname{Tr}(BCA)",
            font_size=37,
            color=TEXT,
        )

        formula_2.move_to(ORIGIN + DOWN * 0.25)

        write(formula_2, 0.9)

        # Highlight each cyclic arrangement separately.
        parts = formula_2[0]

        flash(formula_2, GREEN_C)

        self.wait(0.5)

        # ============================================================
        # 3. GENERAL CYCLIC PERMUTATION
        # ============================================================

        general_subtitle = Text(
            "The same idea works for many factors",
            font_size=22,
            color=MUTED,
        )

        general_subtitle.move_to(subtitle)

        self.play(
            Transform(subtitle, general_subtitle),
            FadeOut(formula_2),
            run_time=0.45,
        )

        formula_3 = MathTex(
            r"\operatorname{Tr}"
            r"\left("
            r"\prod_{i=1}^{n}F^{(i)}"
            r"\right)"
            r"="
            r"\operatorname{Tr}"
            r"\left("
            r"F^{(n)}"
            r"\prod_{i=1}^{n-1}F^{(i)}"
            r"\right)",
            font_size=31,
            color=TEXT,
        )

        formula_3.move_to(ORIGIN + DOWN * 0.15)

        write(formula_3, 1.0)

        flash(formula_3, PURPLE_C)

        self.wait(0.8)

        # ============================================================
        # 4. RECTANGULAR MATRICES: Tr(AB) = Tr(BA)
        # ============================================================

        rect_subtitle = Text(
            "Even when the intermediate products have different shapes",
            font_size=20,
            color=MUTED,
        )

        rect_subtitle.move_to(subtitle)

        self.play(
            Transform(subtitle, rect_subtitle),
            FadeOut(formula_3),
            run_time=0.45,
        )

        shape_text = Text(
            "A ∈ R^(m × n)        B ∈ R^(n × m)",
            font_size=27,
            color=TEXT,
        )

        shape_text.move_to(UP * 0.55)

        write(shape_text, 0.8)

        formula_4 = MathTex(
            r"\operatorname{Tr}(AB)"
            r"="
            r"\operatorname{Tr}(BA)",
            font_size=42,
            color=TEXT,
        )

        formula_4.next_to(shape_text, DOWN, buff=0.55)

        write(formula_4, 0.8)

        dimensions = Text(
            "AB ∈ R^(m × m)        BA ∈ R^(n × n)",
            font_size=25,
            color=MUTED,
        )

        dimensions.next_to(formula_4, DOWN, buff=0.5)

        write(dimensions, 0.7)

        flash(formula_4, GREEN_C)

        self.wait(0.8)

        # ============================================================
        # 5. SCALAR IS ITS OWN TRACE
        # ============================================================

        scalar_subtitle = Text(
            "A scalar is its own trace",
            font_size=22,
            color=MUTED,
        )

        scalar_subtitle.move_to(subtitle)

        group = VGroup(
            shape_text,
            formula_4,
            dimensions,
        )

        self.play(
            Transform(subtitle, scalar_subtitle),
            FadeOut(group),
            run_time=0.45,
        )

        scalar_formula = MathTex(
            r"a=\operatorname{Tr}(a)",
            font_size=43,
            color=TEXT,
        )

        scalar_formula.move_to(ORIGIN + DOWN * 0.15)

        write(scalar_formula, 0.8)

        flash(scalar_formula, YELLOW_C)

        self.wait(0.8)

        # ============================================================
        # TRANSITION TO DETERMINANT
        # ============================================================

        self.play(
            FadeOut(scalar_formula),
            FadeOut(subtitle),
            FadeOut(title),
            run_time=0.55,
        )

        # ============================================================
        # 6. DETERMINANT
        # ============================================================

        det_title = Text(
            "2.11  The Determinant",
            font_size=34,
            color=TEXT,
        )

        det_title.to_edge(UP, buff=0.45)

        write(det_title, 0.7)

        det_intro = Text(
            "A square matrix maps to a scalar",
            font_size=23,
            color=MUTED,
        )

        det_intro.next_to(det_title, DOWN, buff=0.35)

        write(det_intro, 0.55)

        matrix = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"2&0\\"
            r"0&3"
            r"\end{bmatrix}",
            font_size=39,
            color=TEXT,
        )

        matrix.move_to(LEFT * 2.8 + DOWN * 0.35)

        write(matrix, 0.8)

        arrow = Arrow(
            matrix.get_right() + RIGHT * 0.2,
            RIGHT * 0.7 + DOWN * 0.35,
            buff=0.15,
            stroke_width=2.2,
            color=MUTED,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.55,
        )

        determinant = MathTex(
            r"\det(A)=6",
            font_size=42,
            color=GREEN_C,
        )

        determinant.move_to(RIGHT * 2.3 + DOWN * 0.35)

        write(determinant, 0.8)

        flash(determinant, GREEN_C)

        self.wait(0.7)

        # ============================================================
        # 7. DETERMINANT = PRODUCT OF EIGENVALUES
        # ============================================================

        det_relation = MathTex(
            r"\det(A)"
            r"="
            r"\prod_i\lambda_i",
            font_size=40,
            color=TEXT,
        )

        det_relation.move_to(DOWN * 1.55)

        write(det_relation, 0.8)

        flash(det_relation, BLUE_C)

        self.wait(0.8)

        # ============================================================
        # 8. GEOMETRIC MEANING
        # ============================================================

        self.play(
            FadeOut(matrix),
            FadeOut(arrow),
            FadeOut(determinant),
            FadeOut(det_relation),
            FadeOut(det_intro),
            run_time=0.5,
        )

        geometric = Text(
            "Geometric meaning",
            font_size=25,
            color=MUTED,
        )

        geometric.next_to(det_title, DOWN, buff=0.35)

        write(geometric, 0.55)

        zero_case = MathTex(
            r"\det(A)=0"
            r"\quad\Longrightarrow\quad"
            r"\text{space collapses}",
            font_size=34,
            color=RED_C,
        )

        zero_case.move_to(UP * 0.35)

        write(zero_case, 0.85)

        flash(zero_case, RED_C)

        one_case = MathTex(
            r"\det(A)=1"
            r"\quad\Longrightarrow\quad"
            r"\text{volume is preserved}",
            font_size=34,
            color=GREEN_C,
        )

        one_case.move_to(DOWN * 1.0)

        write(one_case, 0.85)

        flash(one_case, GREEN_C)

        self.wait(1.0)

        # ============================================================
        # 9. PCA TRANSITION
        # ============================================================

        self.play(
            FadeOut(zero_case),
            FadeOut(one_case),
            FadeOut(geometric),
            FadeOut(det_title),
            run_time=0.55,
        )

        pca_title = Text(
            "2.12  Principal Components Analysis",
            font_size=32,
            color=TEXT,
        )

        pca_title.to_edge(UP, buff=0.45)

        write(pca_title, 0.7)

        pca_text = Text(
            "PCA can be derived using basic linear algebra",
            font_size=24,
            color=MUTED,
        )

        pca_text.next_to(pca_title, DOWN, buff=0.45)

        write(pca_text, 0.65)

        # ============================================================
        # SIMPLE DATA CLOUD
        # ============================================================

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6.0,
            y_length=3.8,
            axis_config={
                "stroke_color": "#666666",
                "stroke_width": 1.4,
            },
            tips=False,
        )

        axes.move_to(DOWN * 0.55)

        self.play(
            Create(axes),
            run_time=0.8,
        )

        points = [
            (-2.2, -1.0),
            (-1.7, -0.7),
            (-1.2, -0.45),
            (-0.6, -0.15),
            (0.0, 0.1),
            (0.7, 0.45),
            (1.2, 0.7),
            (1.8, 1.0),
            (2.3, 1.25),
        ]

        dots = VGroup()

        for x, y in points:
            dot = Dot(
                axes.c2p(x, y),
                radius=0.055,
                color=BLUE_C,
            )
            dots.add(dot)

        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=0.6) for dot in dots],
                lag_ratio=0.08,
            ),
            run_time=1.0,
        )

        principal_axis = Line(
            axes.c2p(-2.45, -1.2),
            axes.c2p(2.45, 1.35),
            color=GREEN_C,
            stroke_width=3.0,
        )

        self.play(
            Create(principal_axis),
            run_time=0.9,
        )

        flash(principal_axis, GREEN_C)

        pca_label = MathTex(
            r"\text{principal direction}",
            font_size=29,
            color=GREEN_C,
        )

        pca_label.next_to(
            principal_axis.get_end(),
            UP,
            buff=0.2,
        )

        write(pca_label, 0.65)

        self.wait(1.5)

        # ============================================================
        # END
        # ============================================================

        self.play(
            FadeOut(
                VGroup(
                    axes,
                    dots,
                    principal_axis,
                    pca_label,
                    pca_text,
                    pca_title,
                )
            ),
            run_time=0.6,
        )

        self.wait(0.5)


if __name__ == "__main__":
    Figure217().render()
