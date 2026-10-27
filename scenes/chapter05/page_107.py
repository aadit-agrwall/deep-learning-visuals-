from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.ml_shapes import dataset_table, matrix_grid


class Page_107(Chapter5Scene):

    PAGE_NO = "107"
    RNG_SEED = 73

    def construct(self):
        self.init_page()

        # ============================================================
        # SCENE 1 — FROM THE OBJECTIVE TO THE GRADIENT CONDITION
        # ============================================================

        title1 = self.txt(
            "Solving the linear regression objective",
            27, pal.TEXT, BOLD
        )
        title1.to_edge(UP, buff=0.6)
        self.type_in(title1, run_time=1.0)

        formula1 = self.formula(
            r"\frac{1}{m}\nabla_{\mathbf w}"
            r"\left\|\mathbf X^{(\mathrm{train})}\mathbf w"
            r"-\mathbf y^{(\mathrm{train})}\right\|_2^2 = 0",
            27, pal.FORMULA
        )
        formula1.next_to(title1, DOWN, buff=0.7)

        self.play(Write(formula1), run_time=1.4)

        eq1 = self.txt("(5.8)", 14, pal.TEXT_DIM)
        eq1.next_to(formula1, RIGHT, buff=0.35)
        self.type_in(eq1, run_time=0.4)

        note1 = self.txt(
            "at the minimum, the gradient vanishes",
            16, pal.TEXT
        )
        note1.next_to(formula1, DOWN, buff=0.55)
        self.type_in(note1, run_time=0.9)

        self.wait(1.1)
        self.dust_wipe([title1, formula1, eq1, note1])

        # ============================================================
        # SCENE 2 — EQUATION 5.9
        # ============================================================

        title2 = self.txt(
            "Write the error in matrix form",
            27, pal.TEXT, BOLD
        )
        title2.to_edge(UP, buff=0.6)
        self.type_in(title2, run_time=1.0)

        formula2 = self.formula(
            r"\nabla_{\mathbf w}"
            r"\left(\mathbf X^{(\mathrm{train})}\mathbf w"
            r"-\mathbf y^{(\mathrm{train})}\right)^{\mathsf T}"
            r"\left(\mathbf X^{(\mathrm{train})}\mathbf w"
            r"-\mathbf y^{(\mathrm{train})}\right)=0",
            25, pal.FORMULA
        )
        self.fit_width(formula2, 8.5)
        formula2.next_to(title2, DOWN, buff=0.8)

        self.play(Write(formula2), run_time=1.5)

        eq2 = self.txt("(5.9)", 14, pal.TEXT_DIM)
        eq2.next_to(formula2, RIGHT, buff=0.25)
        self.type_in(eq2, run_time=0.4)

        note2 = self.txt(
            "the squared error is a quadratic function of w",
            16, pal.TEXT
        )
        note2.next_to(formula2, DOWN, buff=0.55)
        self.type_in(note2, run_time=0.9)

        self.wait(1.0)
        self.dust_wipe([title2, formula2, eq2, note2])

        # ============================================================
        # SCENE 3 — EXPAND THE QUADRATIC
        # ============================================================

        title3 = self.txt(
            "Expand the quadratic",
            27, pal.TEXT, BOLD
        )
        title3.to_edge(UP, buff=0.6)
        self.type_in(title3, run_time=1.0)

        formula3 = self.formula(
            r"\nabla_{\mathbf w}\left("
            r"\mathbf w^{\mathsf T}\mathbf X^{(\mathrm{train})\mathsf T}"
            r"\mathbf X^{(\mathrm{train})}\mathbf w"
            r"-2\mathbf w^{\mathsf T}\mathbf X^{(\mathrm{train})\mathsf T}"
            r"\mathbf y^{(\mathrm{train})}"
            r"+\mathbf y^{(\mathrm{train})\mathsf T}"
            r"\mathbf y^{(\mathrm{train})}\right)=0",
            24, pal.FORMULA
        )
        self.fit_width(formula3, 8.7)
        formula3.next_to(title3, DOWN, buff=0.8)

        self.play(Write(formula3), run_time=1.6)

        eq3 = self.txt("(5.10)", 14, pal.TEXT_DIM)
        eq3.next_to(formula3, RIGHT, buff=0.25)
        self.type_in(eq3, run_time=0.4)

        note3 = self.txt(
            "only the terms containing w affect the gradient",
            16, pal.TEXT
        )
        note3.next_to(formula3, DOWN, buff=0.55)
        self.type_in(note3, run_time=0.9)

        self.wait(1.0)
        self.dust_wipe([title3, formula3, eq3, note3])

        # ============================================================
        # SCENE 4 — DIFFERENTIATE
        # ============================================================

        title4 = self.txt(
            "Differentiate with respect to w",
            27, pal.TEXT, BOLD
        )
        title4.to_edge(UP, buff=0.6)
        self.type_in(title4, run_time=1.0)

        formula4 = self.formula(
            r"2\mathbf X^{(\mathrm{train})\mathsf T}"
            r"\mathbf X^{(\mathrm{train})}\mathbf w"
            r"-2\mathbf X^{(\mathrm{train})\mathsf T}"
            r"\mathbf y^{(\mathrm{train})}=0",
            29, pal.FORMULA
        )
        formula4.next_to(title4, DOWN, buff=0.9)

        self.play(Write(formula4), run_time=1.3)

        eq4 = self.txt("(5.11)", 14, pal.TEXT_DIM)
        eq4.next_to(formula4, RIGHT, buff=0.3)
        self.type_in(eq4, run_time=0.4)

        note4 = self.txt(
            "set the resulting gradient equal to zero",
            16, pal.TEXT
        )
        note4.next_to(formula4, DOWN, buff=0.55)
        self.type_in(note4, run_time=0.9)

        self.wait(1.0)
        self.dust_wipe([title4, formula4, eq4, note4])

        # ============================================================
        # SCENE 5 — NORMAL EQUATIONS
        # ============================================================

        title5 = self.txt(
            "The normal equations",
            29, pal.TEXT, BOLD
        )
        title5.to_edge(UP, buff=0.6)
        self.type_in(title5, run_time=1.0)

        formula5 = self.formula(
            r"\mathbf w"
            r"=\left(\mathbf X^{(\mathrm{train})\mathsf T}"
            r"\mathbf X^{(\mathrm{train})}\right)^{-1}"
            r"\mathbf X^{(\mathrm{train})\mathsf T}"
            r"\mathbf y^{(\mathrm{train})}",
            30, pal.FORMULA
        )
        self.fit_width(formula5, 8.4)
        formula5.next_to(title5, DOWN, buff=0.85)

        self.play(Write(formula5), run_time=1.5)

        eq5 = self.txt("(5.12)", 14, pal.TEXT_DIM)
        eq5.next_to(formula5, RIGHT, buff=0.25)
        self.type_in(eq5, run_time=0.4)

        normal_box = SurroundingRectangle(
            formula5,
            color=pal.INPUT,
            buff=0.22,
            stroke_width=2.5
        )
        self.play(Create(normal_box), run_time=0.7)

        note5 = self.txt(
            "this closed-form solution is called the normal equations",
            16, pal.TEXT
        )
        note5.next_to(formula5, DOWN, buff=0.6)
        self.type_in(note5, run_time=1.0)

        self.wait(1.2)
        self.dust_wipe([
            title5, formula5, eq5, normal_box, note5
        ])

        # ============================================================
        # SCENE 6 — WHY THIS IS A LEARNING ALGORITHM
        # ============================================================

        title6 = self.txt(
            "A simple learning algorithm",
            28, pal.TEXT, BOLD
        )
        title6.to_edge(UP, buff=0.6)
        self.type_in(title6, run_time=1.0)

        step1 = self.txt(
            "1. collect the training data",
            18, pal.INPUT
        )
        step1.next_to(title6, DOWN, buff=0.8)

        step2 = self.txt(
            "2. build X and y",
            18, pal.FORMULA
        )
        step2.next_to(step1, DOWN, buff=0.4)

        step3 = self.txt(
            "3. evaluate the normal equation",
            18, pal.OUTPUT
        )
        step3.next_to(step2, DOWN, buff=0.4)

        step4 = self.txt(
            "4. obtain the optimal weight vector w",
            18, pal.TEXT
        )
        step4.next_to(step3, DOWN, buff=0.4)

        self.type_in(step1, run_time=0.7)
        self.type_in(step2, run_time=0.7)
        self.type_in(step3, run_time=0.8)
        self.type_in(step4, run_time=0.9)

        self.wait(1.2)
        self.dust_wipe([
            title6, step1, step2, step3, step4
        ])

        # ============================================================
        # SCENE 7 — INTRODUCE THE INTERCEPT
        # ============================================================

        title7 = self.txt(
            "Linear regression with an intercept",
            27, pal.TEXT, BOLD
        )
        title7.to_edge(UP, buff=0.6)
        self.type_in(title7, run_time=1.0)

        statement7 = self.txt(
            "A slightly richer model adds one parameter:",
            17, pal.TEXT
        )
        statement7.next_to(title7, DOWN, buff=0.6)
        self.type_in(statement7, run_time=0.9)

        b_label = self.formula(
            r"b\quad\text{(intercept)}",
            24, pal.OUTPUT
        )
        b_label.next_to(statement7, DOWN, buff=0.55)
        self.play(Write(b_label), run_time=0.8)

        formula7 = self.formula(
            r"\hat y = \mathbf w^{\mathsf T}\mathbf x + b",
            32, pal.FORMULA
        )
        formula7.next_to(b_label, DOWN, buff=0.65)
        self.play(Write(formula7), run_time=1.1)

        eq7 = self.txt("(5.13)", 14, pal.TEXT_DIM)
        eq7.next_to(formula7, RIGHT, buff=0.35)
        self.type_in(eq7, run_time=0.4)

        note7 = self.txt(
            "parameters → predictions: still linear\n"
            "features → predictions: now affine",
            16, pal.TEXT
        )
        note7.next_to(formula7, DOWN, buff=0.6)
        self.type_in(note7, run_time=1.1)

        self.wait(1.2)
        self.dust_wipe([
            title7, statement7, b_label,
            formula7, eq7, note7
        ])

        # ============================================================
        # SCENE 8 — FIGURE 5.1: LINEAR REGRESSION EXAMPLE
        # ============================================================

        title8 = self.txt(
            "Figure 5.1 — linear regression in action",
            26, pal.TEXT, BOLD
        )
        title8.to_edge(UP, buff=0.5)
        self.type_in(title8, run_time=1.0)

        # ------------------------------------------------------------
        # LEFT PLOT — DATA + FITTED LINE
        # ------------------------------------------------------------

        axes_left = Axes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-3, 3, 1],
            x_length=4.0,
            y_length=3.4,
            axis_config={
                "color": pal.TEXT_DIM,
                "stroke_width": 1.8,
            },
            tips=False,
        )

        axes_left.move_to(LEFT * 2.55 + DOWN * 0.65)

        x_label = axes_left.get_x_axis_label(
            MathTex("x_1", font_size=18),
            edge=RIGHT,
            direction=DOWN,
            buff=0.15
        )

        y_label = axes_left.get_y_axis_label(
            MathTex("y", font_size=18),
            edge=UP,
            direction=LEFT,
            buff=0.15
        )

        left_title = self.txt(
            "Linear regression example",
            15, pal.TEXT
        )
        left_title.next_to(axes_left, UP, buff=0.18)

        self.play(Create(axes_left), run_time=0.9)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.4)
        self.type_in(left_title, run_time=0.7)

        # Ten training points, matching the visual character of the book.
        points = np.array([
            [-0.55, -0.25],
            [-0.48,  0.05],
            [-0.35, -1.25],
            [-0.32, -1.35],
            [-0.18,  0.02],
            [ 0.10, -0.10],
            [ 0.10,  0.58],
            [ 0.30,  0.42],
            [ 0.45,  0.55],
            [ 0.65,  1.20],
        ])

        dots = VGroup(*[
            Dot(
                axes_left.c2p(x, y),
                radius=0.065,
                color=pal.FORMULA
            )
            for x, y in points
        ])

        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=0.5) for dot in dots],
                lag_ratio=0.08
            ),
            run_time=1.0
        )

        fit_line = axes_left.plot(
            lambda x: 1.55 * x - 0.15,
            x_range=[-1.2, 1.2],
            color=pal.INPUT,
            stroke_width=3.2
        )

        self.play(Create(fit_line), run_time=1.1)

        # ------------------------------------------------------------
        # RIGHT PLOT — OPTIMIZATION OF w
        # ------------------------------------------------------------

        axes_right = Axes(
            x_range=[0, 2.0, 0.5],
            y_range=[0.20, 0.55, 0.05],
            x_length=3.8,
            y_length=3.4,
            axis_config={
                "color": pal.TEXT_DIM,
                "stroke_width": 1.8,
            },
            tips=False,
        )

        axes_right.move_to(RIGHT * 2.45 + DOWN * 0.65)

        right_title = self.txt(
            "Optimization of w",
            15, pal.TEXT
        )
        right_title.next_to(axes_right, UP, buff=0.18)

        rx = axes_right.get_x_axis_label(
            MathTex("w_1", font_size=18),
            edge=RIGHT,
            direction=DOWN,
            buff=0.15
        )

        ry = axes_right.get_y_axis_label(
            MathTex(r"\mathrm{MSE}^{(\mathrm{train})}", font_size=15),
            edge=UP,
            direction=LEFT,
            buff=0.15
        )

        self.play(Create(axes_right), run_time=0.9)
        self.play(FadeIn(rx), FadeIn(ry), run_time=0.4)
        self.type_in(right_title, run_time=0.7)

        loss_curve = axes_right.plot(
            lambda w: 0.245 + 0.09 * (w - 1.5) ** 2,
            x_range=[0, 2.0],
            color=pal.INPUT,
            stroke_width=3.0
        )

        self.play(Create(loss_curve), run_time=1.1)

        optimum = Dot(
            axes_right.c2p(1.5, 0.245),
            radius=0.075,
            color=pal.FORMULA
        )

        optimum_label = self.formula(
            r"w_1^\star \approx 1.5",
            17, pal.FORMULA
        )
        optimum_label.next_to(optimum, UP, buff=0.22)

        self.play(FadeIn(optimum, scale=0.5), run_time=0.6)
        self.type_in(optimum_label, run_time=0.8)

        # ------------------------------------------------------------
        # CONNECT BOTH PLOTS
        # ------------------------------------------------------------

        connector = DashedLine(
            axes_left.get_right() + RIGHT * 0.15,
            axes_right.get_left() + LEFT * 0.15,
            color=pal.TEXT_DIM,
            stroke_width=1.5,
            dash_length=0.08,
        )

        self.play(Create(connector), run_time=0.5)

        caption = self.txt(
            "the normal equations choose the w that minimizes training MSE",
            15, pal.TEXT
        )
        caption.to_edge(DOWN, buff=0.35)
        self.type_in(caption, run_time=1.1)

        self.wait(1.5)

        self.dust_wipe([
            title8,
            axes_left, x_label, y_label, left_title,
            dots, fit_line,
            axes_right, right_title, rx, ry,
            loss_curve, optimum, optimum_label,
            connector, caption
        ])

        # ============================================================
        # SCENE 9 — FINAL TAKEAWAY
        # ============================================================

        final = self.txt(
            "The normal equations turn linear regression\n"
            "into a closed-form optimization problem.",
            22, pal.TEXT, BOLD
        )
        self.fit_width(final, 7.4)
        final.move_to(ORIGIN)

        self.type_in(final, run_time=1.5)

        line = Underline(
            final,
            color=pal.INPUT,
            stroke_width=3,
            buff=0.18
        )
        self.play(Create(line), run_time=0.5)

        self.zoom_pulse(
            final,
            zoom_scale=0.93,
            run_time_in=0.8,
            hold=0.3,
            run_time_out=0.01
        )

        self.wait(1.5)


if __name__ == "__main__":
    Page_107().render()
