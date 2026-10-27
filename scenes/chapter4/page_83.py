import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 83 — CHAPTER 4
# NUMERICAL COMPUTATION
# Native 9:16 composition — 1440 x 2560
# Palette: WHITE / BLACK / BLUE only
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_83(Scene):

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
        # SCENE 1 — SECTION
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
            "4.3  Gradient-Based Optimization",
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
        # SCENE 2 — FIGURE 4.3
        # APPROXIMATE MINIMIZATION
        # ============================================================

        title = txt(
            "Figure 4.3 — Approximate minimization",
            27,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.52,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.7)

        subtitle = txt(
            "Optimization may stop at a useful local minimum.",
            19,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.22,
        )

        fit_in_frame(subtitle, margin=0.45)
        show(subtitle, 0.6)

        # ------------------------------------------------------------
        # GRAPH
        # ------------------------------------------------------------

        axes = Axes(
            x_range=[-3.4, 3.4, 1],
            y_range=[-0.2, 4.4, 1],
            x_length=7.2,
            y_length=4.7,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
            x_axis_config={
                "include_ticks": False,
            },
            y_axis_config={
                "include_ticks": False,
            },
        )

        axes.move_to(
            DOWN * 0.45
        )

        border = SurroundingRectangle(
            axes,
            color=BLACK,
            stroke_width=2,
            buff=0.06,
        )

        self.play(
            Create(axes),
            Create(border),
            run_time=0.8,
        )

        # Carefully shaped landscape with several minima.
        def landscape(x):
            return (
                0.035 * x**4
                + 0.055 * x**3
                - 0.34 * x**2
                + 0.16 * x
                + 1.35
                + 0.20 * np.sin(2.0 * x)
            )

        curve = axes.plot(
            landscape,
            x_range=[-3.3, 3.3],
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            Create(curve),
            run_time=1.1,
        )

        # Approximate critical locations.
        critical_x = [
            -1.65,
            -0.15,
            1.55,
        ]

        critical_dots = VGroup()

        for x in critical_x:
            critical_dots.add(
                Dot(
                    axes.c2p(
                        x,
                        landscape(x),
                    ),
                    radius=0.09,
                    color=BLACK,
                )
            )

        self.play(
            *[
                FadeIn(dot)
                for dot in critical_dots
            ],
            run_time=0.6,
        )

        # Global minimum arrow
        global_arrow = Arrow(
            axes.c2p(
                -1.65,
                landscape(-1.65) + 0.95,
            ),
            axes.c2p(
                -1.65,
                landscape(-1.65) + 0.10,
            ),
            color=BLACK,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.20,
        )

        global_text = txt(
            "global minimum",
            17,
            BLACK,
            BOLD,
        )

        global_text.next_to(
            global_arrow.get_start(),
            UP,
            buff=0.08,
        )

        # Acceptable local minimum
        acceptable_arrow = Arrow(
            axes.c2p(
                -0.15,
                landscape(-0.15) + 1.25,
            ),
            axes.c2p(
                -0.15,
                landscape(-0.15) + 0.10,
            ),
            color=BLACK,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.20,
        )

        acceptable_text = txt(
            "acceptable stopping point",
            16,
            BLACK,
        )

        acceptable_text.next_to(
            acceptable_arrow.get_start(),
            UP,
            buff=0.08,
        )

        poor_arrow = Arrow(
            axes.c2p(
                1.55,
                landscape(1.55) + 0.75,
            ),
            axes.c2p(
                1.55,
                landscape(1.55) + 0.10,
            ),
            color=BLACK,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.20,
        )

        poor_text = txt(
            "poor local minimum",
            16,
            BLACK,
        )

        poor_text.next_to(
            poor_arrow.get_start(),
            UP,
            buff=0.08,
        )

        self.play(
            GrowArrow(global_arrow),
            run_time=0.55,
        )

        show(
            global_text,
            0.45,
        )

        self.play(
            GrowArrow(acceptable_arrow),
            run_time=0.55,
        )

        show(
            acceptable_text,
            0.5,
        )

        self.play(
            GrowArrow(poor_arrow),
            run_time=0.55,
        )

        show(
            poor_text,
            0.5,
        )

        graph_note = txt(
            "Several local minima can make exact global minimization difficult.",
            18,
            BLACK,
        )

        graph_note.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(graph_note, margin=0.45)
        show(graph_note, 0.75)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 3 — DIRECTIONAL DERIVATIVE
        # ============================================================

        title = txt(
            "Directional derivative",
            31,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.8)

        vector_u = MathTex(
            r"\mathbf{u}",
            font_size=46,
            color=BLUE,
        )

        vector_u.move_to(
            UP * 2.15
        )

        show(
            vector_u,
            0.6,
        )

        description = txt(
            "Let u be a unit vector describing a direction of travel.",
            20,
            BLACK,
        )

        description.next_to(
            vector_u,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(description, margin=0.45)
        show(description, 0.75)

        directional = MathTex(
            r"\frac{\partial}{\partial\alpha}f(\mathbf{x}+\alpha\mathbf{u})",
            font_size=32,
            color=BLUE,
        )

        directional.move_to(
            DOWN * 0.05
        )

        fit_in_frame(
            directional,
            margin=0.45,
        )

        show(
            directional,
            0.9,
        )

        at_zero = MathTex(
            r"\left.\frac{\partial}{\partial\alpha}f(\mathbf{x}+\alpha\mathbf{u})\right|_{\alpha=0}",
            font_size=29,
            color=BLACK,
        )

        at_zero.next_to(
            directional,
            DOWN,
            buff=0.45,
        )

        fit_in_frame(
            at_zero,
            margin=0.5,
        )

        show(
            at_zero,
            0.9,
        )

        chain_rule = MathTex(
            r"=\mathbf{u}^{\mathsf{T}}\nabla_{\mathbf{x}}f(\mathbf{x})",
            font_size=34,
            color=BLUE,
        )

        chain_rule.next_to(
            at_zero,
            DOWN,
            buff=0.42,
        )

        fit_in_frame(
            chain_rule,
            margin=0.45,
        )

        show(
            chain_rule,
            0.85,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — FIND THE FASTEST DECREASING DIRECTION
        # ============================================================

        title = txt(
            "Which direction decreases f fastest?",
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

        eq43 = MathTex(
            r"\min_{\mathbf{u},\,\mathbf{u}^{\mathsf{T}}\mathbf{u}=1}"
            r"\;\mathbf{u}^{\mathsf{T}}\nabla_{\mathbf{x}}f(\mathbf{x})",
            font_size=31,
            color=BLUE,
        )

        eq43.move_to(
            UP * 1.85
        )

        fit_in_frame(
            eq43,
            margin=0.5,
        )

        show(
            eq43,
            1.0,
        )

        number43 = txt(
            "(4.3)",
            17,
            BLACK,
        )

        number43.next_to(
            eq43,
            RIGHT,
            buff=0.25,
        )

        show(
            number43,
            0.4,
        )

        # Unit vectors around a central gradient
        center = Dot(
            ORIGIN + DOWN * 0.55,
            radius=0.10,
            color=BLACK,
        )

        gradient_arrow = Arrow(
            center.get_center(),
            center.get_center() + UP * 1.25 + RIGHT * 1.25,
            color=BLUE,
            stroke_width=5,
        )

        negative_arrow = Arrow(
            center.get_center(),
            center.get_center() + DOWN * 1.25 + LEFT * 1.25,
            color=BLUE,
            stroke_width=6,
        )

        grad_label = MathTex(
            r"\nabla f",
            font_size=30,
            color=BLUE,
        )

        grad_label.next_to(
            gradient_arrow.get_end(),
            UP,
            buff=0.15,
        )

        neg_label = MathTex(
            r"-\nabla f",
            font_size=30,
            color=BLUE,
        )

        neg_label.next_to(
            negative_arrow.get_end(),
            DOWN,
            buff=0.12,
        )

        self.play(
            FadeIn(center),
            GrowArrow(gradient_arrow),
            run_time=0.7,
        )

        show(
            grad_label,
            0.45,
        )

        self.play(
            GrowArrow(negative_arrow),
            run_time=0.7,
        )

        show(
            neg_label,
            0.45,
        )

        conclusion = txt(
            "The direction of steepest decrease is opposite the gradient.",
            19,
            BLACK,
            BOLD,
        )

        conclusion.to_edge(
            DOWN,
            buff=0.7,
        )

        fit_in_frame(
            conclusion,
            margin=0.45,
        )

        show(
            conclusion,
            0.8,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 5 — ANGLE FORM
        # ============================================================

        title = txt(
            "The angle makes the result clear",
            29,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.8)

        eq44 = MathTex(
            r"\min_{\mathbf{u},\,\mathbf{u}^{\mathsf{T}}\mathbf{u}=1}"
            r"\|\mathbf{u}\|_2\|\nabla_{\mathbf{x}}f(\mathbf{x})\|_2\cos\theta",
            font_size=29,
            color=BLUE,
        )

        eq44.move_to(
            UP * 1.85
        )

        fit_in_frame(
            eq44,
            margin=0.48,
        )

        show(
            eq44,
            1.0,
        )

        number44 = txt(
            "(4.4)",
            17,
            BLACK,
        )

        number44.next_to(
            eq44,
            RIGHT,
            buff=0.20,
        )

        show(
            number44,
            0.4,
        )

        # Angle visualization
        center = Dot(
            DOWN * 0.25,
            radius=0.10,
            color=BLACK,
        )

        grad = Arrow(
            center.get_center(),
            center.get_center() + RIGHT * 1.55 + UP * 0.75,
            color=BLUE,
            stroke_width=5,
        )

        direction = Arrow(
            center.get_center(),
            center.get_center() + LEFT * 1.55 + DOWN * 0.75,
            color=BLUE,
            stroke_width=5,
        )

        arc = Arc(
            radius=0.72,
            start_angle=np.pi,
            angle=-2.69,
            arc_center=center.get_center(),
            color=BLACK,
            stroke_width=3,
        )

        theta = MathTex(
            r"\theta",
            font_size=29,
            color=BLACK,
        )

        theta.move_to(
            center.get_center()
            + LEFT * 0.25
            + UP * 0.70
        )

        self.play(
            FadeIn(center),
            GrowArrow(grad),
            run_time=0.7,
        )

        self.play(
            GrowArrow(direction),
            run_time=0.7,
        )

        self.play(
            Create(arc),
            run_time=0.55,
        )

        show(
            theta,
            0.45,
        )

        key = txt(
            "To minimize cos(theta), choose theta = pi.",
            20,
            BLACK,
            BOLD,
        )

        key.to_edge(
            DOWN,
            buff=0.82,
        )

        fit_in_frame(
            key,
            margin=0.45,
        )

        show(
            key,
            0.8,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — STEEPEST DESCENT
        # ============================================================

        title = txt(
            "Steepest descent",
            31,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.8)

        gradient = MathTex(
            r"\text{steepest descent direction}=-\nabla_{\mathbf{x}}f(\mathbf{x})",
            font_size=29,
            color=BLUE,
        )

        gradient.move_to(
            UP * 1.95
        )

        fit_in_frame(
            gradient,
            margin=0.45,
        )

        show(
            gradient,
            0.95,
        )

        downhill = txt(
            "Move opposite the gradient to go downhill.",
            21,
            BLACK,
        )

        downhill.next_to(
            gradient,
            DOWN,
            buff=0.38,
        )

        fit_in_frame(
            downhill,
            margin=0.45,
        )

        show(
            downhill,
            0.7,
        )

        # Animated downhill trajectory
        axes = Axes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-0.2, 4.5, 1],
            x_length=7.0,
            y_length=4.8,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 0.8
        )

        self.play(
            Create(axes),
            run_time=0.7,
        )

        curve = axes.plot(
            lambda x: 0.13 * x**4 - 0.55 * x**2 + 1.4,
            x_range=[-2.7, 2.7],
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            Create(curve),
            run_time=0.85,
        )

        x_positions = [
            -2.1,
            -1.7,
            -1.3,
            -0.9,
            -0.55,
            -0.25,
            0.0,
        ]

        moving_dot = Dot(
            axes.c2p(
                x_positions[0],
                0.13 * x_positions[0]**4
                - 0.55 * x_positions[0]**2
                + 1.4,
            ),
            radius=0.11,
            color=BLACK,
        )

        self.play(
            FadeIn(moving_dot),
            run_time=0.35,
        )

        for x in x_positions[1:]:
            y = (
                0.13 * x**4
                - 0.55 * x**2
                + 1.4
            )

            self.play(
                moving_dot.animate.move_to(
                    axes.c2p(x, y)
                ),
                run_time=0.42,
            )

        minimum = txt(
            "downhill",
            20,
            BLUE,
            BOLD,
        )

        minimum.to_edge(
            DOWN,
            buff=0.72,
        )

        show(
            minimum,
            0.6,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 7 — UPDATE RULE (4.5)
        # ============================================================

        title = txt(
            "The gradient descent update",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(
            title,
            0.8,
        )

        intro = txt(
            "Start at x and take a small step opposite the gradient.",
            20,
            BLACK,
        )

        intro.next_to(
            title,
            DOWN,
            buff=0.30,
        )

        fit_in_frame(
            intro,
            margin=0.45,
        )

        show(
            intro,
            0.7,
        )

        equation = MathTex(
            r"\mathbf{x}'=\mathbf{x}-\epsilon\nabla_{\mathbf{x}}f(\mathbf{x})",
            font_size=39,
            color=BLUE,
        )

        equation.move_to(
            UP * 0.85
        )

        fit_in_frame(
            equation,
            margin=0.5,
        )

        show(
            equation,
            1.0,
        )

        number = txt(
            "(4.5)",
            18,
            BLACK,
        )

        number.next_to(
            equation,
            RIGHT,
            buff=0.25,
        )

        show(
            number,
            0.4,
        )

        # Step decomposition
        x_box = VGroup(
            MathTex(
                r"\mathbf{x}",
                font_size=35,
                color=BLACK,
            ),
            txt(
                "current point",
                18,
                BLACK,
            ),
        )

        x_box.arrange(
            DOWN,
            buff=0.20,
        )

        gradient_box = VGroup(
            MathTex(
                r"\nabla f(\mathbf{x})",
                font_size=32,
                color=BLUE,
            ),
            txt(
                "slope information",
                18,
                BLACK,
            ),
        )

        gradient_box.arrange(
            DOWN,
            buff=0.20,
        )

        epsilon_box = VGroup(
            MathTex(
                r"\epsilon",
                font_size=35,
                color=BLUE,
            ),
            txt(
                "step size",
                18,
                BLACK,
            ),
        )

        epsilon_box.arrange(
            DOWN,
            buff=0.20,
        )

        components = VGroup(
            x_box,
            gradient_box,
            epsilon_box,
        )

        components.arrange(
            RIGHT,
            buff=0.48,
        )

        components.move_to(
            DOWN * 1.45
        )

        fit_in_frame(
            components,
            margin=0.65,
        )

        staggered_fade_in(
            self,
            [
                x_box,
                gradient_box,
                epsilon_box,
            ],
            run_time=1.2,
            lag_ratio=0.3,
        )

        explanation = txt(
            "Repeat the update until the function reaches a sufficiently low value.",
            19,
            BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.72,
        )

        fit_in_frame(
            explanation,
            margin=0.45,
        )

        show(
            explanation,
            0.8,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "Steepest descent follows the negative gradient.\n"
            "Each step moves toward lower values of the objective.",
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
    Page_83().render()
