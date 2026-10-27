import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 79 — CHAPTER 4
# NATIVE 9:16 PHONE FORMAT
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_79(Scene):

    def construct(self):

        # ============================================================
        # ONLY THREE VISUAL COLORS
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

        def clean_box(
            label,
            body,
            width=7.0,
            height=1.9,
            color=BLUE,
        ):
            outer = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.16,
                stroke_color=color,
                stroke_width=4,
                fill_color=WHITE,
                fill_opacity=1,
            )

            heading = txt(
                label,
                23,
                BLACK,
                BOLD,
            )

            heading.next_to(
                outer.get_top(),
                DOWN,
                buff=0.30,
            )

            body.move_to(
                outer.get_center()
                + DOWN * 0.12
            )

            return VGroup(
                outer,
                heading,
                body,
            )

        def blue_arrow(start_obj, end_obj):
            return Arrow(
                start_obj.get_bottom(),
                end_obj.get_top(),
                color=BLUE,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.22,
            )

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
            42,
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
        show(section, 0.65)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 2 — OVERFLOW
        # ============================================================

        title = txt(
            "Overflow",
            34,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.7)

        subtitle = txt(
            "Very large magnitudes can exceed\n"
            "the representable numerical range.",
            22,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(
            subtitle,
            margin=0.55,
        )

        show(subtitle, 0.8)

        # Numerical growth
        values = [
            MathTex(r"10^1", font_size=35, color=BLUE),
            MathTex(r"10^2", font_size=35, color=BLUE),
            MathTex(r"10^4", font_size=35, color=BLUE),
            MathTex(r"10^8", font_size=35, color=BLUE),
            MathTex(r"10^{16}", font_size=35, color=BLUE),
            MathTex(r"\infty", font_size=43, color=BLACK),
        ]

        group = VGroup(*values)
        group.arrange(
            DOWN,
            buff=0.35,
        )

        group.move_to(
            ORIGIN + DOWN * 0.25
        )

        fit_in_frame(
            group,
            margin=0.75,
        )

        for i, value in enumerate(values):

            show(
                value,
                0.45,
            )

            if i < len(values) - 1:

                arrow = Arrow(
                    value.get_bottom(),
                    values[i + 1].get_top(),
                    color=BLUE,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.2,
                )

                self.play(
                    GrowArrow(arrow),
                    run_time=0.4,
                )

        warning = MathTex(
            r"\text{finite range}"
            r"\quad\longrightarrow\quad"
            r"\text{overflow}",
            font_size=29,
            color=BLACK,
        )

        warning.to_edge(
            DOWN,
            buff=0.85,
        )

        fit_in_frame(
            warning,
            margin=0.5,
        )

        show(
            warning,
            0.8,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — SOFTMAX
        # ============================================================

        title = txt(
            "Softmax must remain numerically stable",
            28,
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
            "A probability transformation built from exponentials.",
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

        # Input vector
        vector_label = txt(
            "input vector",
            21,
            BLUE,
            BOLD,
        )

        vector_label.move_to(
            UP * 2.0
        )

        show(
            vector_label,
            0.55,
        )

        vector = MathTex(
            r"\mathbf{x}=[x_1,x_2,\ldots,x_n]",
            font_size=34,
            color=BLACK,
        )

        vector.next_to(
            vector_label,
            DOWN,
            buff=0.3,
        )

        fit_in_frame(
            vector,
            margin=0.55,
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
            run_time=0.6,
        )

        # Equation 4.1
        equation = MathTex(
            r"\operatorname{softmax}(\mathbf{x})_i"
            r"="
            r"\frac{\exp(x_i)}"
            r"{\sum_{j=1}^{n}\exp(x_j)}",
            font_size=34,
            color=BLUE,
        )

        equation.move_to(
            ORIGIN + DOWN * 0.15
        )

        fit_in_frame(
            equation,
            margin=0.55,
        )

        show(
            equation,
            1.0,
        )

        eq_number = txt(
            "(4.1)",
            19,
            BLACK,
        )

        eq_number.next_to(
            equation,
            DOWN,
            buff=0.22,
        )

        show(
            eq_number,
            0.45,
        )

        output = txt(
            "probabilities",
            21,
            BLUE,
            BOLD,
        )

        output.next_to(
            eq_number,
            DOWN,
            buff=0.35,
        )

        show(
            output,
            0.55,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — WHY SOFTMAX CAN FAIL
        # ============================================================

        title = txt(
            "Large magnitudes can break the calculation",
            28,
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

        # ------------------------------------------------------------
        # NEGATIVE CASE
        # ------------------------------------------------------------

        negative_box = clean_box(
            "VERY NEGATIVE INPUT",
            MathTex(
                r"c\ll0",
                font_size=35,
                color=BLUE,
            ),
            width=6.8,
            height=1.75,
        )

        negative_box.move_to(
            UP * 2.5
        )

        fit_in_frame(
            negative_box,
            margin=0.55,
        )

        self.play(
            FadeIn(
                negative_box,
                shift=UP * 0.2,
            ),
            run_time=0.75,
        )

        arrow1 = blue_arrow(
            negative_box,
            negative_box.copy().shift(DOWN * 1.4),
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.55,
        )

        negative_result = clean_box(
            "EXPONENTIAL",
            MathTex(
                r"\exp(c)\rightarrow0",
                font_size=34,
                color=BLACK,
            ),
            width=6.8,
            height=1.75,
        )

        negative_result.move_to(
            ORIGIN + DOWN * 0.15
        )

        self.play(
            FadeIn(
                negative_result,
                shift=UP * 0.2,
            ),
            run_time=0.75,
        )

        denominator = MathTex(
            r"\sum_j\exp(x_j)\rightarrow0",
            font_size=29,
            color=BLUE,
        )

        denominator.to_edge(
            DOWN,
            buff=0.95,
        )

        fit_in_frame(
            denominator,
            margin=0.5,
        )

        show(
            denominator,
            0.8,
        )

        warning = txt(
            "division by zero can appear",
            20,
            BLACK,
            BOLD,
        )

        warning.next_to(
            denominator,
            DOWN,
            buff=0.25,
        )

        show(
            warning,
            0.55,
        )

        self.wait(1.2)
        clear_scene()

        # ============================================================
        # SCENE 5 — STABILIZATION TRICK
        # ============================================================

        title = txt(
            "A simple stabilization trick",
            30,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.6,
        )

        show(
            title,
            0.8,
        )

        subtitle = txt(
            "Shift every input by the same scalar.",
            21,
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

        # Original vector
        original = MathTex(
            r"\mathbf{x}=[x_1,x_2,\ldots,x_n]",
            font_size=32,
            color=BLACK,
        )

        original.move_to(
            UP * 2.4
        )

        fit_in_frame(
            original,
            margin=0.5,
        )

        show(
            original,
            0.8,
        )

        # Max
        max_box = clean_box(
            "FIND THE MAXIMUM",
            MathTex(
                r"m=\max_i x_i",
                font_size=35,
                color=BLUE,
            ),
            width=6.8,
            height=1.7,
        )

        max_box.move_to(
            UP * 0.75
        )

        fit_in_frame(
            max_box,
            margin=0.55,
        )

        arrow1 = Arrow(
            original.get_bottom(),
            max_box.get_top(),
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.6,
        )

        self.play(
            FadeIn(
                max_box,
                shift=UP * 0.2,
            ),
            run_time=0.8,
        )

        # Stabilized vector
        stable = clean_box(
            "STABILIZED INPUT",
            MathTex(
                r"\mathbf{z}=\mathbf{x}-m",
                font_size=35,
                color=BLUE,
            ),
            width=6.8,
            height=1.7,
        )

        stable.move_to(
            DOWN * 1.25
        )

        arrow2 = Arrow(
            max_box.get_bottom(),
            stable.get_top(),
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow2),
            run_time=0.6,
        )

        self.play(
            FadeIn(
                stable,
                shift=UP * 0.2,
            ),
            run_time=0.8,
        )

        result = MathTex(
            r"\max_i z_i=0",
            font_size=34,
            color=BLACK,
        )

        result.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(
            result,
            margin=0.5,
        )

        show(
            result,
            0.8,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — WHY SUBTRACTING THE MAXIMUM WORKS
        # ============================================================

        title = txt(
            "Why subtract the maximum?",
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

        # ------------------------------------------------------------
        # NO OVERFLOW
        # ------------------------------------------------------------

        overflow = clean_box(
            "LARGEST EXPONENT",
            MathTex(
                r"\exp(x_i-m)",
                font_size=35,
                color=BLUE,
            ),
            width=6.8,
            height=1.75,
        )

        overflow.move_to(
            UP * 2.35
        )

        fit_in_frame(
            overflow,
            margin=0.55,
        )

        show(
            overflow,
            0.75,
        )

        arrow1 = Arrow(
            overflow.get_bottom(),
            overflow.get_bottom() + DOWN * 0.7,
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.55,
        )

        max_zero = MathTex(
            r"x_{\max}-m=0",
            font_size=34,
            color=BLACK,
        )

        max_zero.move_to(
            ORIGIN + UP * 0.65
        )

        fit_in_frame(
            max_zero,
            margin=0.5,
        )

        show(
            max_zero,
            0.75,
        )

        arrow2 = Arrow(
            max_zero.get_bottom(),
            max_zero.get_bottom() + DOWN * 0.75,
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow2),
            run_time=0.55,
        )

        safe = MathTex(
            r"\exp(0)=1",
            font_size=38,
            color=BLUE,
        )

        safe.move_to(
            DOWN * 0.65
        )

        show(
            safe,
            0.75,
        )

        statement = txt(
            "The largest exponential is exactly 1.",
            21,
            BLACK,
            BOLD,
        )

        statement.to_edge(
            DOWN,
            buff=0.85,
        )

        fit_in_frame(
            statement,
            margin=0.5,
        )

        show(
            statement,
            0.75,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 7 — LOG SOFTMAX
        # ============================================================

        title = txt(
            "Log-softmax needs its own stable computation",
            27,
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

        # Softmax first
        softmax_box = clean_box(
            "SOFTMAX",
            MathTex(
                r"\operatorname{softmax}(\mathbf{x})",
                font_size=31,
                color=BLUE,
            ),
            width=6.8,
            height=1.75,
        )

        softmax_box.move_to(
            UP * 2.45
        )

        fit_in_frame(
            softmax_box,
            margin=0.55,
        )

        show(
            softmax_box,
            0.75,
        )

        arrow1 = Arrow(
            softmax_box.get_bottom(),
            softmax_box.get_bottom() + DOWN * 0.7,
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.55,
        )

        log_box = clean_box(
            "LOG",
            MathTex(
                r"\log(\operatorname{softmax}(\mathbf{x}))",
                font_size=28,
                color=BLACK,
            ),
            width=6.8,
            height=1.75,
        )

        log_box.move_to(
            ORIGIN + UP * 0.65
        )

        self.play(
            FadeIn(
                log_box,
                shift=UP * 0.15,
            ),
            run_time=0.75,
        )

        warning = MathTex(
            r"0\rightarrow\log(0)=-\infty",
            font_size=32,
            color=BLUE,
        )

        warning.move_to(
            DOWN * 0.8
        )

        fit_in_frame(
            warning,
            margin=0.5,
        )

        show(
            warning,
            0.85,
        )

        stable_log = txt(
            "Compute log-softmax directly and stably.",
            21,
            BLACK,
            BOLD,
        )

        stable_log.to_edge(
            DOWN,
            buff=0.8,
        )

        fit_in_frame(
            stable_log,
            margin=0.5,
        )

        show(
            stable_log,
            0.8,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 8 — TAKEAWAY
        # ============================================================

        title = txt(
            "Numerical stability",
            32,
            BLUE,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.8,
        )

        show(
            title,
            0.8,
        )

        takeaway = txt(
            "Equivalent mathematics can behave differently\n"
            "when implemented with finite precision.",
            25,
            BLACK,
            BOLD,
        )

        takeaway.move_to(
            ORIGIN
        )

        fit_in_frame(
            takeaway,
            margin=0.65,
        )

        self.play(
            Write(takeaway),
            run_time=1.2,
        )

        self.wait(0.45)

        line = Underline(
            takeaway,
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
    Page_79().render()
