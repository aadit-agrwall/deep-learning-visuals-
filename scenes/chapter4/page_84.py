import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 84 — CHAPTER 4
# NUMERICAL COMPUTATION
# Native 9:16 phone composition
# Palette: WHITE / BLACK / BLUE only
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_84(Scene):

    def construct(self):

        BG = "#FFFFFF"
        BLACK = "#000000"
        BLUE = "#0047AB"

        self.camera.background_color = BG

        # ============================================================
        # HELPERS
        # ============================================================

        def txt(text, size=28, color=BLACK, weight=NORMAL):
            return Text(
                text,
                font="CMU Serif",
                font_size=size,
                color=color,
                weight=weight,
            )

        def show(obj, time=0.7):
            self.play(
                Write(obj),
                run_time=time,
            )

        def clear_scene():
            if self.mobjects:
                self.play(
                    *[
                        FadeOut(obj)
                        for obj in list(self.mobjects)
                    ],
                    run_time=0.5,
                )
            self.wait(0.3)

        # ============================================================
        # SCENE 1 — CHAPTER / SECTION
        # ============================================================

        chapter = txt(
            "CHAPTER 4",
            27,
            BLUE,
            BOLD,
        )

        heading = txt(
            "Numerical Computation",
            41,
            BLACK,
            BOLD,
        )

        section = txt(
            "4.3.1  Beyond the Gradient",
            27,
            BLUE,
            BOLD,
        )

        chapter.to_edge(
            UP,
            buff=0.72,
        )

        heading.next_to(
            chapter,
            DOWN,
            buff=0.30,
        )

        section.next_to(
            heading,
            DOWN,
            buff=0.40,
        )

        fit_in_frame(
            VGroup(
                chapter,
                heading,
                section,
            ),
            margin=0.55,
        )

        show(chapter, 0.55)
        show(heading, 0.8)
        show(section, 0.65)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — LEARNING RATE
        # ============================================================

        title = txt(
            "The learning rate controls the step size",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        equation = MathTex(
            r"\mathbf{x}'=\mathbf{x}-\epsilon\nabla_{\mathbf{x}}f(\mathbf{x})",
            font_size=37,
            color=BLUE,
        )

        equation.move_to(
            UP * 1.95
        )

        fit_in_frame(
            equation,
            margin=0.5,
        )

        show(
            equation,
            0.9,
        )

        epsilon = MathTex(
            r"\epsilon>0",
            font_size=39,
            color=BLUE,
        )

        epsilon.next_to(
            equation,
            DOWN,
            buff=0.40,
        )

        show(
            epsilon,
            0.6,
        )

        description = txt(
            "A larger ε makes a larger move.\n"
            "A smaller ε makes a smaller move.",
            21,
            BLACK,
        )

        description.next_to(
            epsilon,
            DOWN,
            buff=0.40,
        )

        fit_in_frame(
            description,
            margin=0.45,
        )

        show(
            description,
            0.8,
        )

        # Visual step-size comparison
        baseline = Line(
            LEFT * 3.0,
            RIGHT * 3.0,
            color=BLACK,
            stroke_width=3,
        )

        baseline.move_to(
            DOWN * 0.85
        )

        self.play(
            Create(baseline),
            run_time=0.5,
        )

        small_step = Arrow(
            baseline.get_center() + LEFT * 2.0,
            baseline.get_center() + LEFT * 0.65,
            color=BLUE,
            stroke_width=5,
        )

        large_step = Arrow(
            baseline.get_center() + LEFT * 1.8,
            baseline.get_center() + RIGHT * 1.65,
            color=BLUE,
            stroke_width=5,
        )

        small_label = txt(
            "small ε",
            18,
            BLACK,
        )

        small_label.next_to(
            small_step,
            DOWN,
            buff=0.20,
        )

        large_label = txt(
            "larger ε",
            18,
            BLACK,
        )

        large_label.next_to(
            large_step,
            DOWN,
            buff=0.20,
        )

        self.play(
            GrowArrow(small_step),
            run_time=0.55,
        )

        show(
            small_label,
            0.45,
        )

        self.play(
            GrowArrow(large_step),
            run_time=0.55,
        )

        show(
            large_label,
            0.45,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — LINE SEARCH
        # ============================================================

        title = txt(
            "Line search",
            32,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.8)

        intro = txt(
            "Instead of fixing one step size,\n"
            "test several candidate values of ε.",
            21,
            BLACK,
        )

        intro.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(intro, margin=0.45)
        show(intro, 0.8)

        # Candidate step sizes
        candidates = VGroup(
            MathTex(r"\epsilon_1", font_size=31, color=BLACK),
            MathTex(r"\epsilon_2", font_size=31, color=BLACK),
            MathTex(r"\epsilon_3", font_size=31, color=BLACK),
            MathTex(r"\epsilon_4", font_size=31, color=BLACK),
        )

        candidates.arrange(
            RIGHT,
            buff=0.48,
        )

        candidates.move_to(
            UP * 0.55
        )

        fit_in_frame(
            candidates,
            margin=0.65,
        )

        staggered_fade_in(
            self,
            list(candidates),
            run_time=1.1,
            lag_ratio=0.20,
        )

        arrows = VGroup()

        for item in candidates:
            arrow = Arrow(
                item.get_bottom(),
                item.get_bottom() + DOWN * 0.62,
                color=BLUE,
                stroke_width=4,
            )
            arrows.add(arrow)

        self.play(
            *[
                GrowArrow(a)
                for a in arrows
            ],
            run_time=0.8,
        )

        objective_values = VGroup(
            MathTex(r"f(\mathbf{x}_1')", font_size=27, color=BLACK),
            MathTex(r"f(\mathbf{x}_2')", font_size=27, color=BLACK),
            MathTex(r"f(\mathbf{x}_3')", font_size=27, color=BLUE),
            MathTex(r"f(\mathbf{x}_4')", font_size=27, color=BLACK),
        )

        objective_values.arrange(
            RIGHT,
            buff=0.34,
        )

        objective_values.move_to(
            DOWN * 0.45
        )

        fit_in_frame(
            objective_values,
            margin=0.55,
        )

        self.play(
            *[
                Write(item)
                for item in objective_values
            ],
            run_time=1.0,
        )

        best = txt(
            "Choose the step producing the smallest objective value.",
            20,
            BLACK,
            BOLD,
        )

        best.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(best, margin=0.45)
        show(best, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — CONVERGENCE
        # ============================================================

        title = txt(
            "When does steepest descent converge?",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        gradient = MathTex(
            r"\nabla_{\mathbf{x}}f(\mathbf{x})=\mathbf{0}",
            font_size=40,
            color=BLUE,
        )

        gradient.move_to(
            UP * 1.9
        )

        show(
            gradient,
            0.85,
        )

        meaning = txt(
            "Every component of the gradient is zero.",
            22,
            BLACK,
        )

        meaning.next_to(
            gradient,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(meaning, margin=0.45)
        show(meaning, 0.7)

        # Gradient components visually collapse to zero
        components = VGroup(
            MathTex(r"\frac{\partial f}{\partial x_1}", font_size=28, color=BLACK),
            MathTex(r"\frac{\partial f}{\partial x_2}", font_size=28, color=BLACK),
            MathTex(r"\vdots", font_size=28, color=BLACK),
            MathTex(r"\frac{\partial f}{\partial x_n}", font_size=28, color=BLACK),
        )

        components.arrange(
            DOWN,
            buff=0.22,
        )

        components.move_to(
            DOWN * 0.15
        )

        fit_in_frame(
            components,
            margin=0.65,
        )

        staggered_fade_in(
            self,
            list(components),
            run_time=1.0,
            lag_ratio=0.18,
        )

        equals_zero = MathTex(
            r"=0",
            font_size=38,
            color=BLUE,
        )

        equals_zero.next_to(
            components,
            RIGHT,
            buff=0.35,
        )

        show(
            equals_zero,
            0.6,
        )

        practical = txt(
            "In practice, convergence means the gradient is very close to zero.",
            19,
            BLACK,
        )

        practical.to_edge(
            DOWN,
            buff=0.72,
        )

        fit_in_frame(practical, margin=0.45)
        show(practical, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — HILL CLIMBING
        # ============================================================

        title = txt(
            "The same idea extends to discrete spaces",
            27,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        continuous = txt(
            "Continuous space",
            21,
            BLACK,
            BOLD,
        )

        continuous.move_to(
            UP * 1.85
        )

        show(
            continuous,
            0.55,
        )

        continuous_formula = MathTex(
            r"\mathbf{x}'=\mathbf{x}-\epsilon\nabla f(\mathbf{x})",
            font_size=29,
            color=BLUE,
        )

        continuous_formula.next_to(
            continuous,
            DOWN,
            buff=0.30,
        )

        fit_in_frame(
            continuous_formula,
            margin=0.45,
        )

        show(
            continuous_formula,
            0.75,
        )

        divider = Line(
            LEFT * 2.8,
            RIGHT * 2.8,
            color=BLACK,
            stroke_width=2,
        )

        divider.move_to(
            DOWN * 0.05
        )

        self.play(
            Create(divider),
            run_time=0.5,
        )

        discrete = txt(
            "Discrete space",
            21,
            BLACK,
            BOLD,
        )

        discrete.move_to(
            DOWN * 0.55
        )

        show(
            discrete,
            0.55,
        )

        # Hill climbing staircase
        points = [
            LEFT * 2.5 + DOWN * 1.35,
            LEFT * 1.55 + DOWN * 0.95,
            LEFT * 0.55 + DOWN * 0.55,
            RIGHT * 0.45 + DOWN * 0.15,
            RIGHT * 1.45 + UP * 0.35,
            RIGHT * 2.35 + UP * 0.85,
        ]

        dots = VGroup()

        for point in points:
            dots.add(
                Dot(
                    point,
                    radius=0.09,
                    color=BLUE,
                )
            )

        self.play(
            *[
                FadeIn(dot)
                for dot in dots
            ],
            run_time=0.8,
        )

        for start, end in zip(points[:-1], points[1:]):
            arrow = Arrow(
                start,
                end,
                color=BLUE,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.18,
            )
            self.play(
                GrowArrow(arrow),
                run_time=0.32,
            )

        hill = txt(
            "hill climbing",
            22,
            BLUE,
            BOLD,
        )

        hill.to_edge(
            DOWN,
            buff=0.72,
        )

        show(
            hill,
            0.6,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — JACOBIAN
        # ============================================================

        title = txt(
            "Beyond the gradient: the Jacobian",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        mapping = MathTex(
            r"f:\mathbb{R}^{m}\rightarrow\mathbb{R}^{n}",
            font_size=39,
            color=BLUE,
        )

        mapping.move_to(
            UP * 1.95
        )

        show(
            mapping,
            0.8,
        )

        explanation = txt(
            "When both the input and output are vectors,\n"
            "we need all partial derivatives at once.",
            20,
            BLACK,
        )

        explanation.next_to(
            mapping,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(explanation, margin=0.45)
        show(explanation, 0.8)

        jacobian = MathTex(
            r"J_{i,j}=\frac{\partial f(\mathbf{x})_i}{\partial x_j}",
            font_size=34,
            color=BLUE,
        )

        jacobian.move_to(
            DOWN * 0.05
        )

        fit_in_frame(
            jacobian,
            margin=0.45,
        )

        show(
            jacobian,
            0.9,
        )

        matrix = MathTex(
            r"J=\begin{bmatrix}"
            r"\frac{\partial f_1}{\partial x_1}&\cdots&\frac{\partial f_1}{\partial x_m}\\"
            r"\vdots&\ddots&\vdots\\"
            r"\frac{\partial f_n}{\partial x_1}&\cdots&\frac{\partial f_n}{\partial x_m}"
            r"\end{bmatrix}",
            font_size=28,
            color=BLACK,
        )

        matrix.move_to(
            DOWN * 1.65
        )

        fit_in_frame(
            matrix,
            margin=0.6,
        )

        show(
            matrix,
            1.1,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 7 — SECOND DERIVATIVE / CURVATURE
        # ============================================================

        title = txt(
            "Second derivatives measure curvature",
            29,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        second = MathTex(
            r"\frac{d^2f}{dx^2}=f''(x)",
            font_size=40,
            color=BLUE,
        )

        second.move_to(
            UP * 1.95
        )

        show(
            second,
            0.85,
        )

        description = txt(
            "The second derivative tells us how the gradient changes.",
            20,
            BLACK,
        )

        description.next_to(
            second,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(description, margin=0.45)
        show(description, 0.75)

        # Three curvature examples
        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-1.0, 2.4, 1],
            x_length=7.0,
            y_length=4.6,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 0.85
        )

        self.play(
            Create(axes),
            run_time=0.75,
        )

        flat = axes.plot(
            lambda x: 0.5,
            x_range=[-2.0, 2.0],
            color=BLACK,
            stroke_width=4,
        )

        upward = axes.plot(
            lambda x: 0.32 * x**2 + 1.0,
            x_range=[-2.0, 2.0],
            color=BLUE,
            stroke_width=5,
        )

        downward = axes.plot(
            lambda x: -0.32 * x**2 + 1.0,
            x_range=[-2.0, 2.0],
            color=BLACK,
            stroke_width=4,
        )

        self.play(
            Create(flat),
            run_time=0.55,
        )

        self.play(
            Create(upward),
            run_time=0.75,
        )

        self.play(
            Create(downward),
            run_time=0.75,
        )

        labels = VGroup(
            txt("zero curvature", 17, BLACK),
            txt("positive curvature", 17, BLUE),
            txt("negative curvature", 17, BLACK),
        )

        labels[0].move_to(
            axes.c2p(-1.25, 0.5) + DOWN * 0.30
        )

        labels[1].move_to(
            axes.c2p(1.05, 1.35) + UP * 0.30
        )

        labels[2].move_to(
            axes.c2p(1.0, 0.68) + DOWN * 0.30
        )

        for label in labels:
            fit_in_frame(label, margin=0.3)
            show(label, 0.45)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 8 — HESSIAN
        # ============================================================

        title = txt(
            "The Hessian collects second derivatives",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        hessian = MathTex(
            r"H_{i,j}=\frac{\partial^2 f}{\partial x_i\partial x_j}",
            font_size=35,
            color=BLUE,
        )

        hessian.move_to(
            UP * 1.95
        )

        fit_in_frame(hessian, margin=0.45)
        show(hessian, 0.9)

        matrix = MathTex(
            r"H=\begin{bmatrix}"
            r"\frac{\partial^2f}{\partial x_1^2}"
            r"&\cdots&"
            r"\frac{\partial^2f}{\partial x_1\partial x_n}\\"
            r"\vdots&\ddots&\vdots\\"
            r"\frac{\partial^2f}{\partial x_n\partial x_1}"
            r"&\cdots&"
            r"\frac{\partial^2f}{\partial x_n^2}"
            r"\end{bmatrix}",
            font_size=25,
            color=BLACK,
        )

        matrix.move_to(
            DOWN * 0.15
        )

        fit_in_frame(
            matrix,
            margin=0.6,
        )

        show(
            matrix,
            1.1,
        )

        curvature = txt(
            "Gradient → slope\n"
            "Hessian → curvature",
            23,
            BLACK,
            BOLD,
        )

        curvature.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(
            curvature,
            margin=0.55,
        )

        show(
            curvature,
            0.85,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "The gradient tells us where to move.\n"
            "The Hessian tells us how the landscape curves.",
            24,
            BLACK,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.1
        )

        fit_in_frame(
            final,
            margin=0.58,
        )

        self.play(
            Write(final),
            run_time=1.15,
        )

        self.wait(0.45)

        line = Underline(
            final,
            color=BLUE,
            stroke_width=5,
            buff=0.20,
        )

        self.play(
            Create(line),
            run_time=0.55,
        )

        self.wait(2.4)


if __name__ == "__main__":
    Page_84().render()
