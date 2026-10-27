import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 80 — CHAPTER 4
# NATIVE 9:16 PHONE FORMAT
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_80(Scene):

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

        def clean_box(
            label,
            body,
            width=7.0,
            height=1.8,
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
                outer.get_center() + DOWN * 0.12
            )

            return VGroup(
                outer,
                heading,
                body,
            )

        # ============================================================
        # SCENE 1 — SECTION 4.2
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
            "4.2  Poor Conditioning",
            29,
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
        # SCENE 2 — CONDITIONING
        # ============================================================

        title = txt(
            "What does conditioning measure?",
            29,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.5)
        show(title, 0.8)

        subtitle = txt(
            "How strongly does a function respond\nto a small input change?",
            22,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(subtitle, margin=0.55)
        show(subtitle, 0.8)

        # Input vector
        x1 = MathTex(
            r"\mathbf{x}",
            font_size=42,
            color=BLUE,
        )

        x2 = MathTex(
            r"\mathbf{x}+\Delta\mathbf{x}",
            font_size=36,
            color=BLACK,
        )

        input_group = VGroup(
            x1,
            x2,
        )

        input_group.arrange(
            DOWN,
            buff=0.45,
        )

        input_group.move_to(
            LEFT * 2.1 + DOWN * 0.2
        )

        input_label = txt(
            "INPUT",
            20,
            BLUE,
            BOLD,
        )

        input_label.next_to(
            input_group,
            UP,
            buff=0.35,
        )

        # Output
        y1 = MathTex(
            r"f(\mathbf{x})",
            font_size=38,
            color=BLUE,
        )

        y2 = MathTex(
            r"f(\mathbf{x}+\Delta\mathbf{x})",
            font_size=31,
            color=BLACK,
        )

        output_group = VGroup(
            y1,
            y2,
        )

        output_group.arrange(
            DOWN,
            buff=0.45,
        )

        output_group.move_to(
            RIGHT * 2.1 + DOWN * 0.2
        )

        output_label = txt(
            "OUTPUT",
            20,
            BLUE,
            BOLD,
        )

        output_label.next_to(
            output_group,
            UP,
            buff=0.35,
        )

        fit_in_frame(
            VGroup(
                input_group,
                output_group,
                input_label,
                output_label,
            ),
            margin=0.65,
        )

        show(input_label, 0.4)
        show(x1, 0.45)
        show(x2, 0.45)

        arrow = Arrow(
            input_group.get_right(),
            output_group.get_left(),
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.7,
        )

        show(output_label, 0.4)
        show(y1, 0.45)
        show(y2, 0.5)

        statement = txt(
            "small input change  →  potentially large output change",
            19,
            BLUE,
            BOLD,
        )

        statement.to_edge(
            DOWN,
            buff=0.85,
        )

        fit_in_frame(statement, margin=0.45)
        show(statement, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — FUNCTION f(x) = A^-1 x
        # ============================================================

        title = txt(
            "Matrix inversion can be sensitive",
            29,
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
            r"f(\mathbf{x})=\mathbf{A}^{-1}\mathbf{x}",
            font_size=39,
            color=BLUE,
        )

        function.move_to(
            UP * 2.1
        )

        fit_in_frame(function, margin=0.5)
        show(function, 0.9)

        # Matrix diagram
        matrix_a = MathTex(
            r"\mathbf{A}^{-1}",
            font_size=42,
            color=BLACK,
        )

        vector_x = MathTex(
            r"\mathbf{x}",
            font_size=42,
            color=BLUE,
        )

        result = MathTex(
            r"f(\mathbf{x})",
            font_size=42,
            color=BLUE,
        )

        matrix_a.move_to(
            LEFT * 2.1 + DOWN * 0.25
        )

        vector_x.move_to(
            ORIGIN + DOWN * 0.25
        )

        result.move_to(
            RIGHT * 2.1 + DOWN * 0.25
        )

        left_arrow = Arrow(
            matrix_a.get_right(),
            vector_x.get_left(),
            color=BLUE,
            stroke_width=5,
        )

        right_arrow = Arrow(
            vector_x.get_right(),
            result.get_left(),
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            FadeIn(matrix_a),
            FadeIn(vector_x),
            FadeIn(result),
            run_time=0.8,
        )

        self.play(
            GrowArrow(left_arrow),
            GrowArrow(right_arrow),
            run_time=0.8,
        )

        explanation = txt(
            "If A is poorly conditioned,\n"
            "small input errors can be amplified.",
            22,
            BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.85,
        )

        fit_in_frame(explanation, margin=0.55)
        show(explanation, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — CONDITION NUMBER
        # ============================================================

        title = txt(
            "Condition number",
            32,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        show(title, 0.8)

        definition = txt(
            "For an eigenvalue decomposition:",
            21,
            BLACK,
        )

        definition.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        show(definition, 0.6)

        equation = MathTex(
            r"\kappa(\mathbf{A})=\max_{i,j}\left|\frac{\lambda_i}{\lambda_j}\right|",
            font_size=34,
            color=BLUE,
        )

        equation.next_to(
            definition,
            DOWN,
            buff=0.55,
        )

        fit_in_frame(equation, margin=0.5)
        show(equation, 1.0)

        eq_number = txt(
            "(4.2)",
            19,
            BLACK,
        )

        eq_number.next_to(
            equation,
            DOWN,
            buff=0.22,
        )

        show(eq_number, 0.45)

        # Eigenvalue spectrum
        spectrum_title = txt(
            "eigenvalue magnitudes",
            20,
            BLUE,
            BOLD,
        )

        spectrum_title.next_to(
            eq_number,
            DOWN,
            buff=0.55,
        )

        show(spectrum_title, 0.55)

        axis = NumberLine(
            x_range=[0, 10, 1],
            length=6.7,
            include_numbers=True,
            numbers_to_include=[0, 2, 4, 6, 8, 10],
            font_size=17,
            color=BLACK,
            stroke_width=3,
        )

        axis.next_to(
            spectrum_title,
            DOWN,
            buff=0.35,
        )

        self.play(
            Create(axis),
            run_time=0.8,
        )

        small_eigen = Dot(
            axis.n2p(1),
            radius=0.12,
            color=BLUE,
        )

        large_eigen = Dot(
            axis.n2p(9),
            radius=0.12,
            color=BLUE,
        )

        self.play(
            FadeIn(small_eigen),
            FadeIn(large_eigen),
            run_time=0.6,
        )

        small_label = MathTex(
            r"|\lambda_{\min}|",
            font_size=25,
            color=BLACK,
        )

        large_label = MathTex(
            r"|\lambda_{\max}|",
            font_size=25,
            color=BLACK,
        )

        small_label.next_to(
            small_eigen,
            DOWN,
            buff=0.28,
        )

        large_label.next_to(
            large_eigen,
            UP,
            buff=0.28,
        )

        show(small_label, 0.45)
        show(large_label, 0.45)

        ratio = MathTex(
            r"\text{large spread}\;\Longrightarrow\;\text{large }\kappa(\mathbf{A})",
            font_size=27,
            color=BLUE,
        )

        ratio.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(ratio, margin=0.45)
        show(ratio, 0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 5 — POORLY CONDITIONED MATRIX AMPLIFIES ERROR
        # ============================================================

        title = txt(
            "Poor conditioning amplifies error",
            29,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.5)
        show(title, 0.8)

        # Stable case
        stable = txt(
            "well conditioned",
            21,
            BLUE,
            BOLD,
        )

        stable.move_to(
            LEFT * 2.0 + UP * 2.4
        )

        show(stable, 0.5)

        stable_in = MathTex(
            r"\Delta\mathbf{x}",
            font_size=31,
            color=BLACK,
        )

        stable_out = MathTex(
            r"\Delta f(\mathbf{x})",
            font_size=31,
            color=BLUE,
        )

        stable_in.move_to(
            LEFT * 2.0 + UP * 1.25
        )

        stable_out.move_to(
            LEFT * 2.0 + DOWN * 0.15
        )

        self.play(
            FadeIn(stable_in),
            run_time=0.45,
        )

        stable_arrow = Arrow(
            stable_in.get_bottom(),
            stable_out.get_top(),
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            GrowArrow(stable_arrow),
            run_time=0.5,
        )

        self.play(
            FadeIn(stable_out),
            run_time=0.45,
        )

        stable_note = txt(
            "controlled change",
            18,
            BLACK,
        )

        stable_note.next_to(
            stable_out,
            DOWN,
            buff=0.25,
        )

        show(stable_note, 0.45)

        # Divider
        divider = Line(
            UP * 1.75,
            DOWN * 1.35,
            color=BLACK,
            stroke_width=2,
        )

        self.play(
            Create(divider),
            run_time=0.4,
        )

        # Poor case
        poor = txt(
            "poorly conditioned",
            21,
            BLUE,
            BOLD,
        )

        poor.move_to(
            RIGHT * 2.0 + UP * 2.4
        )

        show(poor, 0.5)

        poor_in = MathTex(
            r"\Delta\mathbf{x}",
            font_size=31,
            color=BLACK,
        )

        poor_out = MathTex(
            r"\Delta f(\mathbf{x})\gg\Delta\mathbf{x}",
            font_size=28,
            color=BLUE,
        )

        poor_in.move_to(
            RIGHT * 2.0 + UP * 1.25
        )

        poor_out.move_to(
            RIGHT * 2.0 + DOWN * 0.15
        )

        self.play(
            FadeIn(poor_in),
            run_time=0.45,
        )

        poor_arrow = Arrow(
            poor_in.get_bottom(),
            poor_out.get_top(),
            color=BLUE,
            stroke_width=7,
        )

        self.play(
            GrowArrow(poor_arrow),
            run_time=0.55,
        )

        self.play(
            FadeIn(poor_out),
            run_time=0.45,
        )

        poor_note = txt(
            "error is amplified",
            18,
            BLACK,
            BOLD,
        )

        poor_note.next_to(
            poor_out,
            DOWN,
            buff=0.25,
        )

        show(poor_note, 0.45)

        takeaway = txt(
            "Conditioning is a property of the problem itself.",
            20,
            BLUE,
            BOLD,
        )

        takeaway.to_edge(
            DOWN,
            buff=0.8,
        )

        fit_in_frame(takeaway, margin=0.45)
        show(takeaway, 0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 6 — SECTION 4.3
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
        # SCENE 7 — OPTIMIZATION
        # ============================================================

        title = txt(
            "Optimization changes the input to improve f(x)",
            27,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.5)
        show(title, 0.8)

        subtitle = txt(
            "Minimize a function by moving toward a lower value.",
            20,
            BLACK,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.3,
        )

        fit_in_frame(subtitle, margin=0.5)
        show(subtitle, 0.7)

        # Axes
        axes = Axes(
            x_range=[-3.2, 3.2, 1],
            y_range=[0, 7, 1],
            x_length=6.8,
            y_length=5.0,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 0.35
        )

        self.play(
            Create(axes),
            run_time=0.9,
        )

        curve = axes.plot(
            lambda x: 0.65 * x**2 + 0.7,
            x_range=[-2.8, 2.8],
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            Create(curve),
            run_time=1.0,
        )

        # Moving point
        point = Dot(
            axes.c2p(-2.1, 0.65 * (-2.1) ** 2 + 0.7),
            radius=0.12,
            color=BLUE,
        )

        self.play(
            FadeIn(point),
            run_time=0.4,
        )

        # Gradient steps
        x_positions = [
            -2.1,
            -1.45,
            -0.9,
            -0.45,
            0.0,
        ]

        for x_old, x_new in zip(
            x_positions[:-1],
            x_positions[1:],
        ):

            y_old = 0.65 * x_old**2 + 0.7
            y_new = 0.65 * x_new**2 + 0.7

            target = axes.c2p(
                x_new,
                y_new,
            )

            step_arrow = Arrow(
                point.get_center(),
                target,
                color=BLUE,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.18,
            )

            self.play(
                GrowArrow(step_arrow),
                run_time=0.35,
            )

            self.play(
                point.animate.move_to(target),
                run_time=0.45,
            )

        minimum_label = txt(
            "minimum",
            19,
            BLUE,
            BOLD,
        )

        minimum_label.next_to(
            point,
            DOWN,
            buff=0.3,
        )

        show(
            minimum_label,
            0.55,
        )

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 8 — OBJECTIVE / COST / LOSS / ERROR
        # ============================================================

        title = txt(
            "What exactly are we optimizing?",
            29,
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
            r"f(\mathbf{x})",
            font_size=43,
            color=BLUE,
        )

        function.move_to(
            UP * 2.25
        )

        show(function, 0.65)

        descriptor = txt(
            "the function we want to minimize or maximize",
            20,
            BLACK,
        )

        descriptor.next_to(
            function,
            DOWN,
            buff=0.28,
        )

        fit_in_frame(descriptor, margin=0.5)
        show(descriptor, 0.7)

        # Four terms arranged vertically
        terms = [
            ("objective function", BLUE),
            ("criterion", BLACK),
            ("cost function", BLUE),
            ("loss function", BLACK),
            ("error function", BLUE),
        ]

        y_start = 0.7

        for index, (label, color) in enumerate(terms):

            word = txt(
                label,
                24,
                color,
                BOLD,
            )

            word.move_to(
                UP * (y_start - index * 0.72)
            )

            fit_in_frame(word, margin=0.55)

            self.play(
                FadeIn(
                    word,
                    shift=UP * 0.12,
                ),
                run_time=0.5,
            )

        note = txt(
            "Different names can describe the quantity being optimized.",
            19,
            BLACK,
        )

        note.to_edge(
            DOWN,
            buff=0.8,
        )

        fit_in_frame(note, margin=0.45)
        show(note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 9 — OPTIMAL VALUE x*
        # ============================================================

        title = txt(
            "The optimum is written with a superscript *",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.65,
        )

        fit_in_frame(title, margin=0.5)
        show(title, 0.8)

        equation = MathTex(
            r"\mathbf{x}^{*}=\arg\min_{\mathbf{x}} f(\mathbf{x})",
            font_size=36,
            color=BLUE,
        )

        equation.move_to(
            UP * 1.75
        )

        fit_in_frame(equation, margin=0.5)
        show(equation, 1.0)

        # Visual minimization
        axes = Axes(
            x_range=[-2.8, 2.8, 1],
            y_range=[0, 5.5, 1],
            x_length=6.6,
            y_length=4.0,
            axis_config={
                "color": BLACK,
                "stroke_width": 2,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 0.45
        )

        self.play(
            Create(axes),
            run_time=0.8,
        )

        curve = axes.plot(
            lambda x: 0.75 * (x - 0.25) ** 2 + 0.65,
            x_range=[-2.4, 2.4],
            color=BLUE,
            stroke_width=6,
        )

        self.play(
            Create(curve),
            run_time=0.9,
        )

        optimum = axes.c2p(
            0.25,
            0.65,
        )

        point = Dot(
            optimum,
            radius=0.14,
            color=BLUE,
        )

        self.play(
            FadeIn(point),
            run_time=0.45,
        )

        star_label = MathTex(
            r"\mathbf{x}^{*}",
            font_size=34,
            color=BLUE,
        )

        star_label.next_to(
            point,
            DOWN,
            buff=0.28,
        )

        show(
            star_label,
            0.55,
        )

        explanation = txt(
            "the input value that gives the minimum f(x)",
            20,
            BLACK,
            BOLD,
        )

        explanation.to_edge(
            DOWN,
            buff=0.75,
        )

        fit_in_frame(explanation, margin=0.45)
        show(explanation, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "Poor conditioning amplifies errors.\n"
            "Optimization searches for better values of x.",
            25,
            BLACK,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.15
        )

        fit_in_frame(
            final,
            margin=0.65,
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
    Page_80().render()
