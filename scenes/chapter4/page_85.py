import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 85 — CHAPTER 4: NUMERICAL COMPUTATION
# Native 9:16 phone composition
# Background: white
# Palette: black + rgb(0,71,171) blue only
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_85(Scene):

    def construct(self):

        BG = "#FFFFFF"
        BLACK = "#000000"
        BLUE = "#0047AB"

        self.camera.background_color = BG

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------

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
            40,
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
            buff=0.68,
        )

        heading.next_to(
            chapter,
            DOWN,
            buff=0.28,
        )

        section.next_to(
            heading,
            DOWN,
            buff=0.34,
        )

        fit_in_frame(
            VGroup(
                chapter,
                heading,
                section,
            ),
            margin=0.55,
        )

        show(chapter, 0.5)
        show(heading, 0.75)
        show(section, 0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — FIGURE 4.4
        # NEGATIVE / ZERO / POSITIVE CURVATURE
        # ============================================================

        title = txt(
            "Second derivative determines curvature",
            27,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.58,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.75)

        subtitle = txt(
            "Three local shapes of a function",
            20,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.25,
        )

        show(subtitle, 0.55)

        # ------------------------------------------------------------
        # Three actual mini-panels, matching Figure 4.4 structure.
        # ------------------------------------------------------------

        panel_w = 2.15
        panel_h = 3.05

        panels = VGroup(
            Rectangle(
                width=panel_w,
                height=panel_h,
                color=BLACK,
                stroke_width=2.5,
            ),
            Rectangle(
                width=panel_w,
                height=panel_h,
                color=BLACK,
                stroke_width=2.5,
            ),
            Rectangle(
                width=panel_w,
                height=panel_h,
                color=BLACK,
                stroke_width=2.5,
            ),
        )

        panels.arrange(
            RIGHT,
            buff=0.24,
        )

        panels.move_to(
            DOWN * 0.65
        )

        fit_in_frame(
            panels,
            margin=0.55,
        )

        # Titles
        labels = VGroup(
            txt("Negative curvature", 18, BLACK),
            txt("No curvature", 18, BLACK),
            txt("Positive curvature", 18, BLACK),
        )

        for label, panel in zip(labels, panels):
            label.next_to(
                panel,
                UP,
                buff=0.16,
            )

        fit_in_frame(labels, margin=0.45)

        staggered_fade_in(
            self,
            list(labels),
            run_time=0.9,
            lag_ratio=0.18,
        )

        self.play(
            *[
                Create(panel)
                for panel in panels
            ],
            run_time=0.9,
        )

        # ------------------------------------------------------------
        # Panel 1: negative curvature — downward parabola
        # ------------------------------------------------------------

        ax1 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=1.85,
            y_length=2.45,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
            },
            tips=False,
        )

        ax1.move_to(
            panels[0].get_center()
        )

        curve1 = ax1.plot(
            lambda x: -0.43 * x**2 + 0.35,
            x_range=[-1.85, 1.85],
            color=BLUE,
            stroke_width=4.5,
        )

        tangent1 = DashedLine(
            ax1.c2p(0.45, 0.35),
            ax1.c2p(1.65, -0.08),
            color=BLUE,
            stroke_width=3,
            dash_length=0.12,
        )

        # ------------------------------------------------------------
        # Panel 2: zero curvature — straight line
        # ------------------------------------------------------------

        ax2 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=1.85,
            y_length=2.45,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
            },
            tips=False,
        )

        ax2.move_to(
            panels[1].get_center()
        )

        curve2 = ax2.plot(
            lambda x: -0.42 * x,
            x_range=[-1.85, 1.85],
            color=BLUE,
            stroke_width=4.5,
        )

        tangent2 = DashedLine(
            ax2.c2p(0.25, -0.105),
            ax2.c2p(1.55, -0.65),
            color=BLUE,
            stroke_width=3,
            dash_length=0.12,
        )

        # ------------------------------------------------------------
        # Panel 3: positive curvature — upward parabola
        # ------------------------------------------------------------

        ax3 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=1.85,
            y_length=2.45,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
            },
            tips=False,
        )

        ax3.move_to(
            panels[2].get_center()
        )

        curve3 = ax3.plot(
            lambda x: 0.43 * x**2 - 0.45,
            x_range=[-1.85, 1.85],
            color=BLUE,
            stroke_width=4.5,
        )

        tangent3 = DashedLine(
            ax3.c2p(0.35, -0.397),
            ax3.c2p(1.65, -0.08),
            color=BLUE,
            stroke_width=3,
            dash_length=0.12,
        )

        self.play(
            Create(curve1),
            Create(curve2),
            Create(curve3),
            run_time=1.15,
        )

        self.play(
            Create(tangent1),
            Create(tangent2),
            Create(tangent3),
            run_time=0.9,
        )

        # x and f(x) labels
        axis_labels = VGroup(
            MathTex(r"x", font_size=20, color=BLACK),
            MathTex(r"f(x)", font_size=20, color=BLACK),
            MathTex(r"x", font_size=20, color=BLACK),
            MathTex(r"f(x)", font_size=20, color=BLACK),
            MathTex(r"x", font_size=20, color=BLACK),
            MathTex(r"f(x)", font_size=20, color=BLACK),
        )

        axis_labels[0].next_to(
            panels[0],
            DOWN,
            buff=0.18,
        )

        axis_labels[1].next_to(
            panels[0],
            LEFT,
            buff=0.08,
        )

        axis_labels[2].next_to(
            panels[1],
            DOWN,
            buff=0.18,
        )

        axis_labels[3].next_to(
            panels[1],
            LEFT,
            buff=0.08,
        )

        axis_labels[4].next_to(
            panels[2],
            DOWN,
            buff=0.18,
        )

        axis_labels[5].next_to(
            panels[2],
            LEFT,
            buff=0.08,
        )

        self.play(
            *[
                FadeIn(item)
                for item in axis_labels
            ],
            run_time=0.65,
        )

        explanation = txt(
            "The dashed line shows what the gradient alone would predict.",
            18,
            BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.62,
        )

        fit_in_frame(
            explanation,
            margin=0.45,
        )

        show(
            explanation,
            0.75,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 3 — HESSIAN DEFINITION
        # ============================================================

        title = txt(
            "The Hessian matrix",
            31,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.75)

        intro = txt(
            "With many input dimensions, there are many second derivatives.",
            20,
            BLACK,
        )

        intro.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(intro, margin=0.45)
        show(intro, 0.75)

        equation = MathTex(
            r"H(f)(\mathbf{x})_{i,j}"
            r"="
            r"\frac{\partial^2}{\partial x_i\partial x_j}"
            r"f(\mathbf{x})",
            font_size=36,
            color=BLUE,
        )

        equation.move_to(
            UP * 0.75
        )

        fit_in_frame(
            equation,
            margin=0.5,
        )

        show(
            equation,
            1.0,
        )

        eqnum = txt(
            "(4.6)",
            19,
            BLACK,
        )

        eqnum.next_to(
            equation,
            RIGHT,
            buff=0.25,
        )

        show(eqnum, 0.4)

        meaning = txt(
            "Each entry of H stores one second partial derivative.",
            21,
            BLACK,
        )

        meaning.next_to(
            equation,
            DOWN,
            buff=0.55,
        )

        fit_in_frame(
            meaning,
            margin=0.45,
        )

        show(
            meaning,
            0.8,
        )

        # Matrix visual
        matrix = MathTex(
            r"H="
            r"\begin{bmatrix}"
            r"H_{11}&H_{12}&\cdots&H_{1n}\\"
            r"H_{21}&H_{22}&\cdots&H_{2n}\\"
            r"\vdots&\vdots&\ddots&\vdots\\"
            r"H_{n1}&H_{n2}&\cdots&H_{nn}"
            r"\end{bmatrix}",
            font_size=29,
            color=BLACK,
        )

        matrix.move_to(
            DOWN * 1.65
        )

        fit_in_frame(
            matrix,
            margin=0.55,
        )

        show(
            matrix,
            1.0,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — HESSIAN IS JACOBIAN OF GRADIENT
        # ============================================================

        title = txt(
            "A useful viewpoint",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.75)

        gradient = MathTex(
            r"\nabla_{\mathbf{x}}f(\mathbf{x})",
            font_size=40,
            color=BLUE,
        )

        gradient.move_to(
            UP * 1.75
        )

        show(
            gradient,
            0.8,
        )

        arrow = Arrow(
            UP * 1.1,
            DOWN * 0.15,
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            Create(arrow),
            run_time=0.6,
        )

        jacobian_text = txt(
            "Jacobian of the gradient",
            21,
            BLACK,
            BOLD,
        )

        jacobian_text.next_to(
            arrow,
            RIGHT,
            buff=0.30,
        )

        show(
            jacobian_text,
            0.65,
        )

        hessian = MathTex(
            r"H(f)(\mathbf{x})",
            font_size=44,
            color=BLUE,
        )

        hessian.move_to(
            DOWN * 0.95
        )

        show(
            hessian,
            0.8,
        )

        equivalence = MathTex(
            r"H(f)(\mathbf{x})"
            r"="
            r"J\!\left(\nabla_{\mathbf{x}}f(\mathbf{x})\right)",
            font_size=30,
            color=BLACK,
        )

        equivalence.to_edge(
            DOWN,
            buff=0.9,
        )

        fit_in_frame(
            equivalence,
            margin=0.5,
        )

        show(
            equivalence,
            0.8,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 5 — MIXED PARTIALS COMMUTE
        # ============================================================

        title = txt(
            "Mixed partial derivatives can be swapped",
            27,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        condition = txt(
            "When the second partial derivatives are continuous:",
            20,
            BLACK,
        )

        condition.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(condition, margin=0.45)
        show(condition, 0.75)

        left_eq = MathTex(
            r"\frac{\partial^2}{\partial x_i\partial x_j}f(\mathbf{x})",
            font_size=33,
            color=BLUE,
        )

        right_eq = MathTex(
            r"\frac{\partial^2}{\partial x_j\partial x_i}f(\mathbf{x})",
            font_size=33,
            color=BLUE,
        )

        equals = MathTex(
            r"=",
            font_size=38,
            color=BLACK,
        )

        equation_group = VGroup(
            left_eq,
            equals,
            right_eq,
        )

        equation_group.arrange(
            RIGHT,
            buff=0.32,
        )

        equation_group.move_to(
            UP * 0.75
        )

        fit_in_frame(
            equation_group,
            margin=0.48,
        )

        self.play(
            Write(left_eq),
            run_time=0.8,
        )

        self.play(
            Write(equals),
            run_time=0.45,
        )

        self.play(
            Write(right_eq),
            run_time=0.8,
        )

        eqnum = txt(
            "(4.7)",
            19,
            BLACK,
        )

        eqnum.next_to(
            equation_group,
            RIGHT,
            buff=0.22,
        )

        show(
            eqnum,
            0.4,
        )

        consequence = MathTex(
            r"H_{i,j}=H_{j,i}",
            font_size=40,
            color=BLUE,
        )

        consequence.move_to(
            DOWN * 0.65
        )

        show(
            consequence,
            0.8,
        )

        symmetric = txt(
            "Therefore the Hessian is symmetric.",
            23,
            BLACK,
            BOLD,
        )

        symmetric.next_to(
            consequence,
            DOWN,
            buff=0.40,
        )

        fit_in_frame(
            symmetric,
            margin=0.45,
        )

        show(
            symmetric,
            0.75,
        )

        # Symmetric matrix visual
        sym_matrix = MathTex(
            r"\begin{bmatrix}"
            r"a&b&c\\"
            r"b&d&e\\"
            r"c&e&f"
            r"\end{bmatrix}",
            font_size=39,
            color=BLACK,
        )

        sym_matrix.to_edge(
            DOWN,
            buff=0.65,
        )

        show(
            sym_matrix,
            0.8,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 6 — EIGENVALUES / ORTHOGONAL BASIS
        # ============================================================

        title = txt(
            "A symmetric Hessian has useful structure",
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

        hessian = MathTex(
            r"H=H^{\mathsf T}",
            font_size=43,
            color=BLUE,
        )

        hessian.move_to(
            UP * 1.85
        )

        show(
            hessian,
            0.75,
        )

        arrow = Arrow(
            UP * 1.25,
            UP * 0.45,
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            Create(arrow),
            run_time=0.55,
        )

        eigen = txt(
            "real eigenvalues",
            23,
            BLACK,
            BOLD,
        )

        eigen.next_to(
            arrow,
            RIGHT,
            buff=0.25,
        )

        show(
            eigen,
            0.65,
        )

        basis = txt(
            "orthogonal eigenvector basis",
            23,
            BLACK,
            BOLD,
        )

        basis.move_to(
            DOWN * 0.45
        )

        show(
            basis,
            0.7,
        )

        # Eigenvalue visualization
        number_line = NumberLine(
            x_range=[-3, 3, 1],
            length=6.6,
            include_numbers=True,
            font_size=18,
            color=BLACK,
        )

        number_line.move_to(
            DOWN * 1.45
        )

        self.play(
            Create(number_line),
            run_time=0.7,
        )

        eigenvalues = [-2.1, 0.8, 2.2]

        dots = VGroup()

        for value in eigenvalues:
            dots.add(
                Dot(
                    number_line.n2p(value),
                    radius=0.11,
                    color=BLUE,
                )
            )

        self.play(
            *[
                FadeIn(dot, scale=0.5)
                for dot in dots
            ],
            run_time=0.8,
        )

        eigen_label = MathTex(
            r"\lambda_1,\lambda_2,\ldots,\lambda_n\in\mathbb{R}",
            font_size=29,
            color=BLUE,
        )

        eigen_label.to_edge(
            DOWN,
            buff=0.65,
        )

        fit_in_frame(
            eigen_label,
            margin=0.45,
        )

        show(
            eigen_label,
            0.75,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "The Hessian captures curvature\n"
            "through second-order derivatives.",
            27,
            BLACK,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.10
        )

        fit_in_frame(
            final,
            margin=0.60,
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
    Page_85().render()
