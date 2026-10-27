import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 78 — CHAPTER 4
# NATIVE 9:16 PHONE COMPOSITION
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_78(Scene):

    def construct(self):

        # ============================================================
        # ONLY APPROVED COLORS
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

        def solid_box(
            label,
            body,
            accent,
            width=7.0,
            height=2.0,
        ):
            """
            Clean book-style box.

            No colored header bar.
            Label is plain black serif text.
            Accent color is used only for the border.
            """

            outer = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.16,
                stroke_color=accent,
                stroke_width=5,
                fill_color=WHITE,
                fill_opacity=1,
            )

            # Plain black book-style heading.
            label_obj = txt(
                label,
                23,
                BLACK,
                BOLD,
            )

            label_obj.next_to(
                outer.get_top(),
                DOWN,
                buff=0.32,
            )

            body.move_to(
                outer.get_center()
                + DOWN * 0.12
            )

            # Small white highlight on the colored border.
            # White is one of the approved colors.
            highlight = Line(
                outer.get_left()
                + RIGHT * 0.35
                + UP * 0.12,
                outer.get_right()
                + LEFT * 0.35
                + UP * 0.12,
                color=WHITE,
                stroke_width=2.5,
            )

            return VGroup(
                outer,
                label_obj,
                body,
                highlight,
            )

        def glossy_dot(point, color, radius=0.13):
            dot = Dot(
                point,
                radius=radius,
                color=color,
            )

            highlight = Dot(
                point
                + UP * radius * 0.35
                + LEFT * radius * 0.30,
                radius=radius * 0.28,
                color=WHITE,
            )

            return VGroup(
                dot,
                highlight,
            )

        # ============================================================
        # SCENE 1 — CHAPTER INTRO
        # ============================================================

        chapter = txt(
            "CHAPTER 4",
            28,
            BLUE,
            BOLD,
        )

        heading = txt(
            "Numerical Computation",
            43,
            BLACK,
            BOLD,
        )

        section = txt(
            "4.1  Overflow and Underflow",
            28,
            BLUE,
            BOLD,
        )

        chapter.to_edge(
            UP,
            buff=0.8,
        )

        heading.next_to(
            chapter,
            DOWN,
            buff=0.35,
        )

        section.next_to(
            heading,
            DOWN,
            buff=0.45,
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
        show(heading, 0.9)
        show(section, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 2 — NUMERICAL COMPUTATION
        # ============================================================

        title = txt(
            "Machine learning needs\nnumerical computation",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.6,
        )

        fit_in_frame(
            title,
            margin=0.5,
        )

        show(title, 0.8)

        # INPUT
        input_body = MathTex(
            r"\text{mathematical problem}",
            font_size=31,
            color=BLACK,
        )

        input_box = solid_box(
            "INPUT",
            input_body,
            BLUE,
            width=7.0,
            height=2.1,
        )

        input_box.next_to(
            title,
            DOWN,
            buff=0.65,
        )

        fit_in_frame(
            input_box,
            margin=0.55,
        )

        self.play(
            FadeIn(
                input_box,
                shift=UP * 0.25,
            ),
            run_time=0.9,
        )

        # ARROW
        arrow_1 = Arrow(
            input_box.get_bottom(),
            input_box.get_bottom()
            + DOWN * 0.85,
            color=BLUE,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.23,
        )

        self.play(
            GrowArrow(arrow_1),
            run_time=0.7,
        )

        # COMPUTER
        computer_body = txt(
            "iterative numerical\napproximation",
            25,
            BLACK,
            BOLD,
        )

        computer_box = solid_box(
            "COMPUTER",
            computer_body,
            BLUE,
            width=7.0,
            height=2.35,
        )

        computer_box.next_to(
            arrow_1,
            DOWN,
            buff=0.02,
        )

        fit_in_frame(
            computer_box,
            margin=0.55,
        )

        self.play(
            FadeIn(
                computer_box,
                shift=UP * 0.2,
            ),
            run_time=0.9,
        )

        # COMMON OPERATIONS
        operations_title = txt(
            "COMMON OPERATIONS",
            20,
            BLUE,
            BOLD,
        )

        operations_title.next_to(
            computer_box,
            DOWN,
            buff=0.5,
        )

        show(
            operations_title,
            0.55,
        )

        operations = [
            ("optimization", BLUE),
            ("linear systems", BLUE),
            ("function evaluation", BLUE),
        ]

        previous = None

        for label, color in operations:

            dot = glossy_dot(
                ORIGIN,
                color,
                radius=0.13,
            )

            label_obj = txt(
                label,
                22,
                BLACK,
                BOLD,
            )

            item = VGroup(
                dot,
                label_obj,
            )

            item.arrange(
                RIGHT,
                buff=0.28,
            )

            if previous is None:
                item.next_to(
                    operations_title,
                    DOWN,
                    buff=0.25,
                )
            else:
                item.next_to(
                    previous,
                    DOWN,
                    buff=0.25,
                )

            fit_in_frame(
                item,
                margin=0.5,
            )

            self.play(
                FadeIn(
                    item,
                    shift=UP * 0.12,
                ),
                run_time=0.55,
            )

            previous = item

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 3 — FINITE NUMERICAL REPRESENTATION
        # ============================================================

        title = txt(
            "A computer has finite precision",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.6,
        )

        fit_in_frame(
            title,
            margin=0.5,
        )

        show(title, 0.8)

        subtitle = txt(
            "Real numbers are continuous.\n"
            "Computer representations are finite.",
            21,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(
            subtitle,
            margin=0.5,
        )

        show(
            subtitle,
            0.75,
        )

        # Number line
        axis = NumberLine(
            x_range=[0, 10, 1],
            length=7.0,
            include_numbers=True,
            numbers_to_include=[
                0,
                2,
                4,
                6,
                8,
                10,
            ],
            font_size=18,
            color=BLACK,
            stroke_width=3,
        )

        axis.move_to(
            DOWN * 0.25
        )

        self.play(
            Create(axis),
            run_time=0.9,
        )

        # Representable points
        values = [
            1, 2, 3, 4, 5,
            6, 7, 8, 9,
        ]

        dots = VGroup(
            *[
                glossy_dot(
                    axis.n2p(value),
                    BLUE,
                    radius=0.105,
                )
                for value in values
            ]
        )

        self.play(
            *[
                FadeIn(dot)
                for dot in dots
            ],
            run_time=1.0,
        )

        representable_label = txt(
            "representable values",
            21,
            BLUE,
            BOLD,
        )

        representable_label.next_to(
            axis,
            DOWN,
            buff=0.4,
        )

        show(
            representable_label,
            0.65,
        )

        # Exact value
        exact = glossy_dot(
            axis.n2p(4.37),
            BLUE,
            radius=0.15,
        )

        exact_label = txt(
            "exact value",
            21,
            BLUE,
            BOLD,
        )

        exact_label.next_to(
            exact,
            UP,
            buff=0.28,
        )

        self.play(
            FadeIn(exact),
            run_time=0.5,
        )

        show(
            exact_label,
            0.65,
        )

        # Difference
        approximation = MathTex(
            r"\text{stored value}"
            r"\;\neq\;"
            r"\text{exact real value}",
            font_size=31,
            color=BLUE,
        )

        approximation.next_to(
            representable_label,
            DOWN,
            buff=0.65,
        )

        fit_in_frame(
            approximation,
            margin=0.5,
        )

        show(
            approximation,
            0.9,
        )

        error = txt(
            "approximation error",
            21,
            BLUE,
            BOLD,
        )

        error.next_to(
            approximation,
            DOWN,
            buff=0.3,
        )

        show(
            error,
            0.6,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — ROUNDING ERROR ACCUMULATES
        # ============================================================

        title = txt(
            "Rounding error can accumulate",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.6,
        )

        fit_in_frame(
            title,
            margin=0.5,
        )

        show(
            title,
            0.8,
        )

        subtitle = txt(
            "Each numerical operation can introduce a small error.",
            20,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.3,
        )

        fit_in_frame(
            subtitle,
            margin=0.5,
        )

        show(
            subtitle,
            0.7,
        )

        # Vertical trajectory
        p0 = np.array([0, 3.0, 0])
        p1 = np.array([-0.55, 1.65, 0])
        p2 = np.array([0.5, 0.35, 0])
        p3 = np.array([-0.45, -0.95, 0])
        p4 = np.array([0.65, -2.3, 0])

        path1 = Line(
            p0,
            p1,
            color=BLUE,
            stroke_width=6,
        )

        path2 = Line(
            p1,
            p2,
            color=BLUE,
            stroke_width=6,
        )

        path3 = Line(
            p2,
            p3,
            color=BLUE,
            stroke_width=6,
        )

        path4 = Line(
            p3,
            p4,
            color=BLUE,
            stroke_width=7,
        )

        diagram = VGroup(
            path1,
            path2,
            path3,
            path4,
        )

        diagram.move_to(
            DOWN * 0.25
        )

        self.play(
            Create(path1),
            run_time=0.45,
        )

        self.play(
            Create(path2),
            run_time=0.45,
        )

        self.play(
            Create(path3),
            run_time=0.45,
        )

        self.play(
            Create(path4),
            run_time=0.6,
        )

        # Nodes
        node0 = glossy_dot(
            p0,
            BLUE,
        )

        node1 = glossy_dot(
            p1,
            BLUE,
        )

        node2 = glossy_dot(
            p2,
            BLUE,
        )

        node3 = glossy_dot(
            p3,
            BLUE,
        )

        node4 = glossy_dot(
            p4,
            BLUE,
            radius=0.16,
        )

        self.play(
            FadeIn(node0),
            FadeIn(node1),
            run_time=0.4,
        )

        self.play(
            FadeIn(node2),
            run_time=0.35,
        )

        self.play(
            FadeIn(node3),
            run_time=0.35,
        )

        self.play(
            FadeIn(node4),
            run_time=0.45,
        )

        labels = [
            ("operation 1", BLUE, node0),
            ("operation 2", BLUE, node1),
            ("operation 3", BLUE, node2),
            ("error grows", BLUE, node4),
        ]

        for label, color, node in labels:

            label_obj = txt(
                label,
                18,
                color,
                BOLD,
            )

            if label == "operation 1":
                label_obj.next_to(
                    node,
                    RIGHT,
                    buff=0.3,
                )

            elif label == "operation 2":
                label_obj.next_to(
                    node,
                    LEFT,
                    buff=0.3,
                )

            elif label == "operation 3":
                label_obj.next_to(
                    node,
                    RIGHT,
                    buff=0.3,
                )

            else:
                label_obj.next_to(
                    node,
                    LEFT,
                    buff=0.3,
                )

            show(
                label_obj,
                0.4,
            )

        formula = MathTex(
            r"\varepsilon_1"
            r"+\varepsilon_2"
            r"+\cdots"
            r"+\varepsilon_n",
            font_size=34,
            color=BLUE,
        )

        formula.to_edge(
            DOWN,
            buff=0.85,
        )

        fit_in_frame(
            formula,
            margin=0.5,
        )

        show(
            formula,
            0.9,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 5 — UNDERFLOW
        # ============================================================

        title = txt(
            "UNDERFLOW",
            34,
            BLUE,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(
            title,
            0.75,
        )

        subtitle = txt(
            "Numbers extremely close to zero\n"
            "can be rounded down to zero.",
            23,
            BLACK,
            BOLD,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.4,
        )

        fit_in_frame(
            subtitle,
            margin=0.5,
        )

        show(
            subtitle,
            0.8,
        )

        # Horizontal number line — centered vertically.
        axis = NumberLine(
            x_range=[-1, 1, 0.25],
            length=7.0,
            include_numbers=True,
            numbers_to_include=[
                -1,
                -0.5,
                0,
                0.5,
                1,
            ],
            font_size=18,
            color=BLACK,
            stroke_width=3,
        )

        axis.move_to(
            DOWN * 0.15
        )

        self.play(
            Create(axis),
            run_time=0.9,
        )

        # Tiny values around zero.
        tiny_values = VGroup(
            *[
                glossy_dot(
                    axis.n2p(value),
                    BLUE,
                    radius=0.12,
                )
                for value in [
                    -0.10,
                    -0.05,
                    0.05,
                    0.10,
                ]
            ]
        )

        self.play(
            *[
                FadeIn(dot)
                for dot in tiny_values
            ],
            run_time=0.8,
        )

        tiny_label = txt(
            "tiny non-zero values",
            21,
            BLUE,
            BOLD,
        )

        tiny_label.next_to(
            axis,
            UP,
            buff=0.4,
        )

        show(
            tiny_label,
            0.7,
        )

        # Zero target
        zero = glossy_dot(
            axis.n2p(0),
            BLUE,
            radius=0.16,
        )

        zero_label = txt(
            "ZERO",
            21,
            BLUE,
            BOLD,
        )

        zero_label.next_to(
            zero,
            DOWN,
            buff=0.35,
        )

        self.play(
            *[
                dot.animate.move_to(
                    zero.get_center()
                )
                for dot in tiny_values
            ],
            run_time=1.15,
        )

        self.play(
            FadeIn(zero),
            run_time=0.4,
        )

        show(
            zero_label,
            0.6,
        )

        formula = MathTex(
            r"x\approx0"
            r"\quad\longrightarrow\quad"
            r"0",
            font_size=38,
            color=BLUE,
        )

        formula.to_edge(
            DOWN,
            buff=0.95,
        )

        fit_in_frame(
            formula,
            margin=0.5,
        )

        show(
            formula,
            0.9,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 6 — WHY UNDERFLOW MATTERS
        # ============================================================

        title = txt(
            "Why underflow matters",
            31,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.6,
        )

        fit_in_frame(
            title,
            margin=0.5,
        )

        show(
            title,
            0.8,
        )

        subtitle = txt(
            "A tiny number can behave very differently\n"
            "from the exact value zero.",
            21,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(
            subtitle,
            margin=0.5,
        )

        show(
            subtitle,
            0.8,
        )

        # ------------------------------------------------------------
        # TINY VALUE
        # ------------------------------------------------------------

        tiny_body = MathTex(
            r"x\approx0^+",
            font_size=36,
            color=BLUE,
        )

        tiny_box = solid_box(
            "TINY VALUE",
            tiny_body,
            BLUE,
            width=6.8,
            height=1.65,
        )

        tiny_box.move_to(
            UP * 2.4
        )

        fit_in_frame(
            tiny_box,
            margin=0.5,
        )

        self.play(
            FadeIn(
                tiny_box,
                shift=UP * 0.2,
            ),
            run_time=0.75,
        )

        # ------------------------------------------------------------
        # ARROW
        # ------------------------------------------------------------

        arrow1 = Arrow(
            tiny_box.get_bottom(),
            tiny_box.get_bottom()
            + DOWN * 0.75,
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.22,
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.6,
        )

        # ------------------------------------------------------------
        # ROUNDED TO ZERO
        # ------------------------------------------------------------

        zero_body = MathTex(
            r"x\rightarrow0",
            font_size=36,
            color=BLUE,
        )

        zero_box = solid_box(
            "ROUNDED TO ZERO",
            zero_body,
            BLUE,
            width=6.8,
            height=1.65,
        )

        zero_box.move_to(
            ORIGIN
        )

        fit_in_frame(
            zero_box,
            margin=0.5,
        )

        self.play(
            FadeIn(
                zero_box,
                shift=UP * 0.2,
            ),
            run_time=0.75,
        )

        # ------------------------------------------------------------
        # ARROW
        # ------------------------------------------------------------

        arrow2 = Arrow(
            zero_box.get_bottom(),
            zero_box.get_bottom()
            + DOWN * 0.75,
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.22,
        )

        self.play(
            GrowArrow(arrow2),
            run_time=0.6,
        )

        # ------------------------------------------------------------
        # FUNCTION
        # ------------------------------------------------------------

        function_body = MathTex(
            r"\frac{1}{x}",
            font_size=40,
            color=BLUE,
        )

        function_box = solid_box(
            "FUNCTION",
            function_body,
            BLUE,
            width=6.8,
            height=1.65,
        )

        function_box.move_to(
            DOWN * 2.35
        )

        fit_in_frame(
            function_box,
            margin=0.5,
        )

        self.play(
            FadeIn(
                function_box,
                shift=UP * 0.2,
            ),
            run_time=0.75,
        )

        consequence = MathTex(
            r"\frac{1}{x}"
            r"\quad\text{becomes}\quad"
            r"\text{unstable as }x\rightarrow0",
            font_size=27,
            color=BLUE,
        )

        consequence.to_edge(
            DOWN,
            buff=0.65,
        )

        fit_in_frame(
            consequence,
            margin=0.45,
        )

        show(
            consequence,
            0.9,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 7 — OVERFLOW
        # ============================================================

        title = txt(
            "The opposite failure:",
            29,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.6,
        )

        fit_in_frame(
            title,
            margin=0.5,
        )

        show(
            title,
            0.7,
        )

        overflow_title = txt(
            "OVERFLOW",
            35,
            BLUE,
            BOLD,
        )

        overflow_title.next_to(
            title,
            DOWN,
            buff=0.18,
        )

        show(
            overflow_title,
            0.7,
        )

        subtitle = txt(
            "Numbers can become too large to represent.",
            21,
            BLACK,
        )

        subtitle.next_to(
            overflow_title,
            DOWN,
            buff=0.3,
        )

        fit_in_frame(
            subtitle,
            margin=0.5,
        )

        show(
            subtitle,
            0.7,
        )

        # ------------------------------------------------------------
        # VERTICAL GROWTH
        # ------------------------------------------------------------

        equations = [
            (r"10^1", BLUE),
            (r"10^2", BLUE),
            (r"10^4", BLUE),
            (r"10^8", BLUE),
            (r"10^{16}", BLUE),
            (r"\infty", BLUE),
        ]

        previous = None
        arrows = []

        start_y = 2.55

        for index, (equation, color) in enumerate(
            equations
        ):

            value = MathTex(
                equation,
                font_size=36
                if index < 5
                else 45,
                color=color,
            )

            if previous is None:
                value.move_to(
                    UP * start_y
                )
            else:
                value.next_to(
                    previous,
                    DOWN,
                    buff=0.38,
                )

            fit_in_frame(
                value,
                margin=0.5,
            )

            show(
                value,
                0.45,
            )

            if previous is not None:

                arrow = Arrow(
                    previous.get_bottom(),
                    value.get_top(),
                    color=(
                        BLUE
                        if index == len(equations) - 1
                        else BLUE
                    ),
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.2,
                )

                self.play(
                    GrowArrow(arrow),
                    run_time=0.4,
                )

                arrows.append(arrow)

            previous = value

        overflow_label = txt(
            "FINITE RANGE  →  TOO LARGE  →  OVERFLOW",
            19,
            BLUE,
            BOLD,
        )

        overflow_label.to_edge(
            DOWN,
            buff=0.8,
        )

        fit_in_frame(
            overflow_label,
            margin=0.45,
        )

        show(
            overflow_label,
            0.8,
        )

        self.wait(1.7)
        clear_scene()

        # ============================================================
        # FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "Finite precision is unavoidable.\n"
            "Good numerical methods control the error.",
            26,
            BLACK,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.2
        )

        fit_in_frame(
            final,
            margin=0.6,
        )

        self.play(
            Write(final),
            run_time=1.2,
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
    Page_78().render()
