import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 81 — CHAPTER 4
# NATIVE 9:16 PHONE FORMAT
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_81(Scene):

    def construct(self):

        # ============================================================
        # APPROVED PALETTE ONLY
        # ============================================================

        BG = "#FFFFFF"
        WHITE = "#FFFFFF"
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

        def clean_box(label, body, width=7.0, height=1.75):
            outer = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.16,
                stroke_color=BLUE,
                stroke_width=4,
                fill_color=WHITE,
                fill_opacity=1,
            )

            heading = txt(
                label,
                22,
                BLACK,
                BOLD,
            )

            heading.next_to(
                outer.get_top(),
                DOWN,
                buff=0.28,
            )

            body.move_to(
                outer.get_center() + DOWN * 0.10
            )

            return VGroup(
                outer,
                heading,
                body,
            )

        # ============================================================
        # SCENE 1 — CHAPTER / GRADIENT-BASED OPTIMIZATION
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
            buff=0.75,
        )

        heading.next_to(
            chapter,
            DOWN,
            buff=0.30,
        )

        section.next_to(
            heading,
            DOWN,
            buff=0.42,
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
        show(heading, 0.85)
        show(section, 0.7)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 2 — FIGURE 4.1: GRADIENT DESCENT
        # ============================================================

        title = txt(
            "Figure 4.1 — Gradient descent",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.55,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.7)

        subtitle = txt(
            "Follow the derivative downhill toward a minimum.",
            19,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.25,
        )

        fit_in_frame(subtitle, margin=0.45)
        show(subtitle, 0.65)

        # ------------------------------------------------------------
        # GRAPH
        # ------------------------------------------------------------

        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-0.35, 2.25, 0.5],
            x_length=7.0,
            y_length=5.4,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 0.15
        )

        self.play(
            Create(axes),
            run_time=0.9,
        )

        # f(x) = 1/2 x^2
        function = axes.plot(
            lambda x: 0.5 * x**2,
            x_range=[-2.0, 2.0],
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            Create(function),
            run_time=1.0,
        )

        # derivative f'(x) = x
        derivative_axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=7.0,
            y_length=5.4,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        derivative_axes.move_to(
            axes.get_center()
        )

        derivative = derivative_axes.plot(
            lambda x: x,
            x_range=[-2.0, 2.0],
            color=BLACK,
            stroke_width=4,
        )

        # Instead of displaying a second set of axes,
        # show the derivative as a symbolic relationship.
        derivative_label = MathTex(
            r"f'(x)=x",
            font_size=25,
            color=BLACK,
        )

        derivative_label.to_edge(
            DOWN,
            buff=0.95,
        )

        fit_in_frame(
            derivative_label,
            margin=0.45,
        )

        self.play(
            Write(derivative_label),
            run_time=0.65,
        )

        function_label = MathTex(
            r"f(x)=\frac{1}{2}x^2",
            font_size=25,
            color=BLUE,
        )

        function_label.to_edge(
            DOWN,
            buff=0.48,
        )

        fit_in_frame(
            function_label,
            margin=0.45,
        )

        show(
            function_label,
            0.6,
        )

        # ------------------------------------------------------------
        # GRADIENT DESCENT PATH
        # ------------------------------------------------------------

        x_values = [
            -1.85,
            -1.40,
            -0.98,
            -0.63,
            -0.35,
            -0.15,
            0.0,
        ]

        point = Dot(
            axes.c2p(
                x_values[0],
                0.5 * x_values[0] ** 2,
            ),
            radius=0.13,
            color=BLUE,
        )

        self.play(
            FadeIn(point),
            run_time=0.45,
        )

        for x_old, x_new in zip(
            x_values[:-1],
            x_values[1:],
        ):

            old_y = 0.5 * x_old**2
            new_y = 0.5 * x_new**2

            target = axes.c2p(
                x_new,
                new_y,
            )

            step = Arrow(
                point.get_center(),
                target,
                color=BLUE,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.18,
            )

            self.play(
                GrowArrow(step),
                run_time=0.35,
            )

            self.play(
                point.animate.move_to(target),
                run_time=0.42,
            )

        minimum = MathTex(
            r"x=0",
            font_size=28,
            color=BLUE,
        )

        minimum.next_to(
            point,
            DOWN,
            buff=0.25,
        )

        show(
            minimum,
            0.55,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 3 — DERIVATIVE = SLOPE
        # ============================================================

        title = txt(
            "The derivative tells us the slope",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.5)
        show(title, 0.8)

        function = MathTex(
            r"y=f(x)",
            font_size=40,
            color=BLUE,
        )

        function.move_to(
            UP * 2.25
        )

        show(
            function,
            0.65,
        )

        derivative = MathTex(
            r"f'(x)=\frac{dy}{dx}",
            font_size=38,
            color=BLACK,
        )

        derivative.next_to(
            function,
            DOWN,
            buff=0.42,
        )

        fit_in_frame(
            derivative,
            margin=0.5,
        )

        show(
            derivative,
            0.8,
        )

        # Local tangent visualization
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-0.5, 5.5, 1],
            x_length=6.8,
            y_length=4.6,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 0.7
        )

        self.play(
            Create(axes),
            run_time=0.8,
        )

        curve = axes.plot(
            lambda x: 0.55 * x**2 + 1.0,
            x_range=[-2.2, 2.2],
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            Create(curve),
            run_time=0.8,
        )

        x0 = 1.1
        y0 = 0.55 * x0**2 + 1.0

        point = Dot(
            axes.c2p(x0, y0),
            radius=0.12,
            color=BLUE,
        )

        tangent = axes.plot(
            lambda x: (2 * 0.55 * x0) * (x - x0) + y0,
            x_range=[-0.3, 2.3],
            color=BLACK,
            stroke_width=3,
        )

        self.play(
            FadeIn(point),
            run_time=0.4,
        )

        self.play(
            Create(tangent),
            run_time=0.8,
        )

        slope = MathTex(
            r"\text{slope}=f'(x)",
            font_size=25,
            color=BLUE,
        )

        slope.to_edge(
            DOWN,
            buff=0.65,
        )

        fit_in_frame(slope, margin=0.45)
        show(slope, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — LOCAL LINEAR APPROXIMATION
        # ============================================================

        title = txt(
            "A small input change gives a predictable output change",
            25,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.6,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        formula = MathTex(
            r"f(x+\epsilon)\approx f(x)+\epsilon f'(x)",
            font_size=34,
            color=BLUE,
        )

        formula.move_to(
            UP * 1.75
        )

        fit_in_frame(formula, margin=0.45)
        show(formula, 1.0)

        # Three-step visual
        input_box = clean_box(
            "INPUT",
            MathTex(
                r"x\rightarrow x+\epsilon",
                font_size=30,
                color=BLUE,
            ),
            width=6.8,
            height=1.65,
        )

        output_box = clean_box(
            "OUTPUT",
            MathTex(
                r"f(x)\rightarrow f(x)+\epsilon f'(x)",
                font_size=27,
                color=BLACK,
            ),
            width=6.8,
            height=1.65,
        )

        input_box.move_to(
            UP * 0.25
        )

        output_box.move_to(
            DOWN * 1.85
        )

        self.play(
            FadeIn(
                input_box,
                shift=UP * 0.15,
            ),
            run_time=0.7,
        )

        arrow = Arrow(
            input_box.get_bottom(),
            output_box.get_top(),
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.6,
        )

        self.play(
            FadeIn(
                output_box,
                shift=UP * 0.15,
            ),
            run_time=0.7,
        )

        note = txt(
            "The derivative converts a small input step into an output step.",
            19,
            BLACK,
        )

        note.to_edge(
            DOWN,
            buff=0.72,
        )

        fit_in_frame(note, margin=0.4)
        show(note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — MOVE OPPOSITE THE DERIVATIVE
        # ============================================================

        title = txt(
            "Gradient descent moves opposite the derivative",
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

        # Negative derivative
        left_box = clean_box(
            "IF  f'(x) < 0",
            MathTex(
                r"x\;\text{should increase}",
                font_size=31,
                color=BLUE,
            ),
            width=6.8,
            height=1.7,
        )

        left_box.move_to(
            UP * 1.9
        )

        show(
            left_box,
            0.8,
        )

        arrow_up = Arrow(
            left_box.get_bottom(),
            left_box.get_bottom() + DOWN * 0.7,
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow_up),
            run_time=0.55,
        )

        right_box = clean_box(
            "IF  f'(x) > 0",
            MathTex(
                r"x\;\text{should decrease}",
                font_size=31,
                color=BLACK,
            ),
            width=6.8,
            height=1.7,
        )

        right_box.move_to(
            DOWN * 0.65
        )

        self.play(
            FadeIn(
                right_box,
                shift=UP * 0.15,
            ),
            run_time=0.75,
        )

        rule = MathTex(
            r"x_{\text{new}}=x-\epsilon\,f'(x)",
            font_size=34,
            color=BLUE,
        )

        rule.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(rule, margin=0.45)
        show(rule, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — CRITICAL POINTS
        # ============================================================

        title = txt(
            "Critical points",
            32,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.8)

        equation = MathTex(
            r"f'(x)=0",
            font_size=42,
            color=BLUE,
        )

        equation.move_to(
            UP * 2.0
        )

        show(
            equation,
            0.75,
        )

        description = txt(
            "At a critical point, the derivative gives\n"
            "no preferred direction for an infinitesimal step.",
            21,
            BLACK,
        )

        description.next_to(
            equation,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(description, margin=0.5)
        show(description, 0.85)

        # Three points: minimum, stationary, maximum
        axes = Axes(
            x_range=[-3.0, 3.0, 1],
            y_range=[-1.5, 3.5, 1],
            x_length=6.8,
            y_length=4.3,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 1.25
        )

        self.play(
            Create(axes),
            run_time=0.8,
        )

        curve = axes.plot(
            lambda x: 0.18 * x**4 - 0.8 * x**2 + 1.4,
            x_range=[-2.6, 2.6],
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            Create(curve),
            run_time=0.9,
        )

        # Stationary points for the quartic
        for x in [-1.49, 0.0, 1.49]:
            y = 0.18 * x**4 - 0.8 * x**2 + 1.4
            dot = Dot(
                axes.c2p(x, y),
                radius=0.11,
                color=BLUE,
            )
            self.play(
                FadeIn(dot),
                run_time=0.3,
            )

        labels = VGroup(
            txt("local minimum", 17, BLACK),
            txt("local maximum", 17, BLACK),
            txt("local minimum", 17, BLACK),
        )

        labels[0].next_to(
            axes.c2p(-1.49, 0.18 * (-1.49)**4 - 0.8 * (-1.49)**2 + 1.4),
            DOWN,
            buff=0.2,
        )

        labels[1].next_to(
            axes.c2p(0, 1.4),
            UP,
            buff=0.2,
        )

        labels[2].next_to(
            axes.c2p(1.49, 0.18 * (1.49)**4 - 0.8 * (1.49)**2 + 1.4),
            DOWN,
            buff=0.2,
        )

        for label in labels:
            fit_in_frame(label, margin=0.3)
            show(label, 0.4)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 7 — LOCAL MINIMUM / MAXIMUM
        # ============================================================

        title = txt(
            "Minimum versus maximum",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.8)

        minimum = clean_box(
            "LOCAL MINIMUM",
            MathTex(
                r"f(x)\leq f(x+\delta)",
                font_size=31,
                color=BLUE,
            ),
            width=6.8,
            height=1.75,
        )

        minimum.move_to(
            UP * 1.65
        )

        show(
            minimum,
            0.8,
        )

        maximum = clean_box(
            "LOCAL MAXIMUM",
            MathTex(
                r"f(x)\geq f(x+\delta)",
                font_size=31,
                color=BLACK,
            ),
            width=6.8,
            height=1.75,
        )

        maximum.move_to(
            DOWN * 0.7
        )

        self.play(
            FadeIn(
                maximum,
                shift=UP * 0.15,
            ),
            run_time=0.8,
        )

        stationary = MathTex(
            r"f'(x)=0",
            font_size=38,
            color=BLUE,
        )

        stationary.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(stationary, margin=0.45)
        show(stationary, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 8 — FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "The derivative gives the direction.\n"
            "Gradient descent uses it to search for a minimum.",
            25,
            BLACK,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.1
        )

        fit_in_frame(
            final,
            margin=0.6,
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
            buff=0.2,
        )

        self.play(
            Create(line),
            run_time=0.55,
        )

        self.wait(2.4)


if __name__ == "__main__":
    Page_81().render()
