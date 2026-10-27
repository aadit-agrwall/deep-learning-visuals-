import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 82 — CHAPTER 4
# NATIVE 9:16 PHONE FORMAT
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_82(Scene):

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

        def box_label(text_value, position):
            label = txt(
                text_value,
                20,
                BLACK,
                BOLD,
            )
            label.move_to(position)
            return label

        # ============================================================
        # SCENE 1 — SECTION CONTINUATION
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
        # SCENE 2 — FIGURE 4.2: THREE TYPES OF CRITICAL POINTS
        # ============================================================

        title = txt(
            "Figure 4.2 — Types of critical points",
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
            "A critical point has zero slope.",
            20,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.25,
        )

        show(subtitle, 0.6)

        # ------------------------------------------------------------
        # THREE ACTUAL MINI-PLOTS
        # ------------------------------------------------------------

        def mini_axes():
            return Axes(
                x_range=[-2.2, 2.2, 1],
                y_range=[-1.0, 2.2, 1],
                x_length=2.05,
                y_length=1.65,
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

        minimum_axes = mini_axes()
        maximum_axes = mini_axes()
        saddle_axes = mini_axes()

        plots = VGroup(
            minimum_axes,
            maximum_axes,
            saddle_axes,
        )

        plots.arrange(
            RIGHT,
            buff=0.38,
        )

        plots.move_to(
            UP * 0.95
        )

        fit_in_frame(
            plots,
            margin=0.65,
        )

        # Minimum
        minimum_curve = minimum_axes.plot(
            lambda x: 0.55 * x**2 - 0.35,
            x_range=[-2.0, 2.0],
            color=BLUE,
            stroke_width=5,
        )

        minimum_dot = Dot(
            minimum_axes.c2p(
                0,
                -0.35,
            ),
            radius=0.09,
            color=BLACK,
        )

        # Maximum
        maximum_curve = maximum_axes.plot(
            lambda x: -0.55 * x**2 + 1.25,
            x_range=[-2.0, 2.0],
            color=BLUE,
            stroke_width=5,
        )

        maximum_dot = Dot(
            maximum_axes.c2p(
                0,
                1.25,
            ),
            radius=0.09,
            color=BLACK,
        )

        # Saddle / inflection-style point
        saddle_curve = saddle_axes.plot(
            lambda x: 0.25 * x**3,
            x_range=[-2.0, 2.0],
            color=BLUE,
            stroke_width=5,
        )

        saddle_dot = Dot(
            saddle_axes.c2p(
                0,
                0,
            ),
            radius=0.09,
            color=BLACK,
        )

        labels = VGroup(
            box_label(
                "Minimum",
                minimum_axes.get_top() + UP * 0.25,
            ),
            box_label(
                "Maximum",
                maximum_axes.get_top() + UP * 0.25,
            ),
            box_label(
                "Saddle point",
                saddle_axes.get_top() + UP * 0.25,
            ),
        )

        fit_in_frame(
            VGroup(
                plots,
                labels,
            ),
            margin=0.55,
        )

        # Plot borders
        borders = VGroup(
            SurroundingRectangle(
                minimum_axes,
                color=BLACK,
                stroke_width=2,
                buff=0.08,
            ),
            SurroundingRectangle(
                maximum_axes,
                color=BLACK,
                stroke_width=2,
                buff=0.08,
            ),
            SurroundingRectangle(
                saddle_axes,
                color=BLACK,
                stroke_width=2,
                buff=0.08,
            ),
        )

        self.play(
            Create(borders),
            run_time=0.7,
        )

        self.play(
            Create(minimum_curve),
            run_time=0.65,
        )

        self.play(
            FadeIn(minimum_dot),
            run_time=0.3,
        )

        self.play(
            Create(maximum_curve),
            run_time=0.65,
        )

        self.play(
            FadeIn(maximum_dot),
            run_time=0.3,
        )

        self.play(
            Create(saddle_curve),
            run_time=0.65,
        )

        self.play(
            FadeIn(saddle_dot),
            run_time=0.3,
        )

        for label in labels:
            show(label, 0.4)

        # Explanation cards
        minimum_text = txt(
            "lower than nearby points",
            18,
            BLACK,
        )

        maximum_text = txt(
            "higher than nearby points",
            18,
            BLACK,
        )

        saddle_text = txt(
            "neighbors can be higher and lower",
            18,
            BLACK,
        )

        descriptions = VGroup(
            minimum_text,
            maximum_text,
            saddle_text,
        )

        descriptions.arrange(
            DOWN,
            buff=0.28,
        )

        descriptions.move_to(
            DOWN * 1.55
        )

        fit_in_frame(
            descriptions,
            margin=0.55,
        )

        show(minimum_text, 0.45)
        show(maximum_text, 0.45)
        show(saddle_text, 0.55)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 3 — CRITICAL POINTS ARE NOT ALWAYS OPTIMA
        # ============================================================

        title = txt(
            "A critical point is not necessarily an optimum",
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
            0.7,
        )

        center = MathTex(
            r"\Downarrow",
            font_size=38,
            color=BLUE,
        )

        center.next_to(
            equation,
            DOWN,
            buff=0.25,
        )

        show(
            center,
            0.45,
        )

        three = VGroup(
            MathTex(
                r"\text{local minimum}",
                font_size=28,
                color=BLACK,
            ),
            MathTex(
                r"\text{local maximum}",
                font_size=28,
                color=BLACK,
            ),
            MathTex(
                r"\text{saddle point}",
                font_size=28,
                color=BLACK,
            ),
        )

        three.arrange(
            DOWN,
            buff=0.55,
        )

        three.move_to(
            DOWN * 0.55
        )

        fit_in_frame(
            three,
            margin=0.6,
        )

        for item in three:
            show(item, 0.5)

        note = txt(
            "Zero slope tells us that the first derivative alone\n"
            "does not determine the final type of point.",
            19,
            BLACK,
        )

        note.to_edge(
            DOWN,
            buff=0.72,
        )

        fit_in_frame(note, margin=0.45)
        show(note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — GLOBAL MINIMUM VS LOCAL MINIMA
        # ============================================================

        title = txt(
            "Global minimum versus local minima",
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

        # Multi-well function
        axes = Axes(
            x_range=[-3.4, 3.4, 1],
            y_range=[-1.3, 4.2, 1],
            x_length=7.0,
            y_length=5.1,
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
            run_time=0.8,
        )

        curve = axes.plot(
            lambda x: 0.09 * x**4 - 0.65 * x**2 + 1.2,
            x_range=[-3.0, 3.0],
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            Create(curve),
            run_time=1.0,
        )

        # Approximate minima and maximum
        points = [
            (-1.9, 0.09 * (-1.9)**4 - 0.65 * (-1.9)**2 + 1.2),
            (0.0, 1.2),
            (1.9, 0.09 * (1.9)**4 - 0.65 * (1.9)**2 + 1.2),
        ]

        dots = VGroup()

        for x, y in points:
            dot = Dot(
                axes.c2p(x, y),
                radius=0.11,
                color=BLACK,
            )
            dots.add(dot)

        self.play(
            *[
                FadeIn(dot)
                for dot in dots
            ],
            run_time=0.7,
        )

        local_label = txt(
            "local minima",
            19,
            BLACK,
            BOLD,
        )

        local_label.next_to(
            dots[0],
            DOWN,
            buff=0.25,
        )

        show(
            local_label,
            0.55,
        )

        global_label = txt(
            "global minimum",
            20,
            BLUE,
            BOLD,
        )

        global_label.next_to(
            dots[2],
            DOWN,
            buff=0.25,
        )

        show(
            global_label,
            0.65,
        )

        explanation = txt(
            "A global minimum has the lowest value over the entire domain.",
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
        # SCENE 5 — WHY DEEP LEARNING OPTIMIZATION IS HARD
        # ============================================================

        title = txt(
            "Why optimization becomes difficult",
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

        landscape = Axes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-1.0, 4.8, 1],
            x_length=7.0,
            y_length=5.2,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        landscape.move_to(
            DOWN * 0.35
        )

        self.play(
            Create(landscape),
            run_time=0.8,
        )

        terrain = landscape.plot(
            lambda x: (
                0.10 * x**4
                - 0.55 * x**2
                + 0.22 * x
                + 1.2
            ),
            x_range=[-2.8, 2.8],
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            Create(terrain),
            run_time=1.0,
        )

        local_a = Dot(
            landscape.c2p(
                -1.5,
                0.10 * (-1.5)**4 - 0.55 * (-1.5)**2 + 0.22 * (-1.5) + 1.2,
            ),
            radius=0.11,
            color=BLACK,
        )

        local_b = Dot(
            landscape.c2p(
                1.35,
                0.10 * (1.35)**4 - 0.55 * (1.35)**2 + 0.22 * 1.35 + 1.2,
            ),
            radius=0.11,
            color=BLACK,
        )

        self.play(
            FadeIn(local_a),
            FadeIn(local_b),
            run_time=0.5,
        )

        labels = VGroup(
            txt("local minimum", 18, BLACK),
            txt("saddle / flat region", 18, BLACK),
        )

        labels[0].next_to(
            local_a,
            DOWN,
            buff=0.25,
        )

        labels[1].next_to(
            local_b,
            UP,
            buff=0.25,
        )

        show(labels[0], 0.45)
        show(labels[1], 0.45)

        problems = txt(
            "many local minima\n"
            "many saddle points\n"
            "flat regions\n"
            "high-dimensional input",
            21,
            BLACK,
        )

        problems.to_edge(
            DOWN,
            buff=0.68,
        )

        fit_in_frame(
            problems,
            margin=0.5,
        )

        show(
            problems,
            0.9,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 6 — MULTIPLE INPUTS
        # ============================================================

        title = txt(
            "From one input to many inputs",
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

        function = MathTex(
            r"f:\mathbb{R}^{n}\rightarrow\mathbb{R}",
            font_size=40,
            color=BLUE,
        )

        function.move_to(
            UP * 1.9
        )

        fit_in_frame(
            function,
            margin=0.45,
        )

        show(
            function,
            0.85,
        )

        # Input vector
        vector = MathTex(
            r"\mathbf{x}=[x_1,x_2,\ldots,x_n]",
            font_size=31,
            color=BLACK,
        )

        vector.next_to(
            function,
            DOWN,
            buff=0.45,
        )

        fit_in_frame(
            vector,
            margin=0.45,
        )

        show(
            vector,
            0.8,
        )

        arrow = Arrow(
            vector.get_bottom(),
            vector.get_bottom() + DOWN * 0.8,
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.55,
        )

        scalar = MathTex(
            r"f(\mathbf{x})\in\mathbb{R}",
            font_size=36,
            color=BLUE,
        )

        scalar.next_to(
            arrow,
            DOWN,
            buff=0.25,
        )

        show(
            scalar,
            0.75,
        )

        explanation = txt(
            "Many inputs are mapped to one scalar output.",
            20,
            BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(
            explanation,
            margin=0.45,
        )

        show(
            explanation,
            0.75,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 7 — PARTIAL DERIVATIVES
        # ============================================================

        title = txt(
            "Partial derivatives",
            31,
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

        formula = MathTex(
            r"\frac{\partial}{\partial x_i}f(\mathbf{x})",
            font_size=39,
            color=BLUE,
        )

        formula.move_to(
            UP * 1.95
        )

        fit_in_frame(
            formula,
            margin=0.45,
        )

        show(
            formula,
            0.9,
        )

        explanation = txt(
            "Change only one variable xᵢ\n"
            "while keeping the other variables fixed.",
            21,
            BLACK,
        )

        explanation.next_to(
            formula,
            DOWN,
            buff=0.42,
        )

        fit_in_frame(
            explanation,
            margin=0.5,
        )

        show(
            explanation,
            0.85,
        )

        # Coordinate visualization
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-1, 3, 1],
            x_length=5.2,
            y_length=4.2,
            z_length=3.8,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
        )

        axes.scale(0.72)
        axes.move_to(
            DOWN * 1.45
        )

        surface = Surface(
            lambda u, v: axes.c2p(
                u,
                v,
                0.25 * u**2 + 0.18 * v**2,
            ),
            u_range=[-1.8, 1.8],
            v_range=[-1.8, 1.8],
            resolution=(14, 14),
            fill_opacity=0.12,
            checkerboard_colors=[
                BLUE,
                BLUE,
            ],
            stroke_color=BLUE,
            stroke_width=1.2,
        )

        self.play(
            Create(axes),
            run_time=0.8,
        )

        self.play(
            Create(surface),
            run_time=1.0,
        )

        direction = Arrow3D(
            start=axes.c2p(
                -1.0,
                0,
                0.25,
            ),
            end=axes.c2p(
                1.0,
                0,
                0.75,
            ),
            color=BLUE,
            thickness=0.035,
        )

        self.play(
            Create(direction),
            run_time=0.7,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 8 — GRADIENT VECTOR
        # ============================================================

        title = txt(
            "The gradient collects all partial derivatives",
            27,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(
            title,
            margin=0.45,
        )

        show(
            title,
            0.8,
        )

        gradient = MathTex(
            r"\nabla_{\mathbf{x}}f(\mathbf{x})",
            font_size=43,
            color=BLUE,
        )

        gradient.move_to(
            UP * 1.95
        )

        show(
            gradient,
            0.8,
        )

        components = MathTex(
            r"\nabla_{\mathbf{x}}f(\mathbf{x})=\begin{bmatrix}\frac{\partial f}{\partial x_1}\\\frac{\partial f}{\partial x_2}\\\vdots\\\frac{\partial f}{\partial x_n}\end{bmatrix}",
            font_size=31,
            color=BLACK,
        )

        components.move_to(
            DOWN * 0.05
        )

        fit_in_frame(
            components,
            margin=0.6,
        )

        show(
            components,
            1.1,
        )

        arrow = MathTex(
            r"\Downarrow",
            font_size=38,
            color=BLUE,
        )

        arrow.next_to(
            components,
            DOWN,
            buff=0.25,
        )

        show(
            arrow,
            0.45,
        )

        meaning = txt(
            "one vector describing how f changes\n"
            "along every input direction",
            21,
            BLACK,
        )

        meaning.next_to(
            arrow,
            DOWN,
            buff=0.25,
        )

        fit_in_frame(
            meaning,
            margin=0.5,
        )

        show(
            meaning,
            0.85,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "Critical points reveal where the slope vanishes.\n"
            "The gradient extends this idea to many dimensions.",
            24,
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
    Page_82().render()
