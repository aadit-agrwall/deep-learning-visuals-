import numpy as np
from manim import *

from common.layouts import fit_in_frame


class Page70(Scene):

    def construct(self):

        # ============================================================
        # THEME — SAME AS PAGE 66 / 67 / 68 / 69
        # ============================================================

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"

        self.camera.background_color = BG

        def txt(text, size=28, color=WHITE, weight=NORMAL):
            return Text(
                text,
                font="DejaVu Sans",
                font_size=size,
                color=color,
                weight=weight
            )

        def show(obj, time=0.7):
            self.play(
                Write(obj),
                run_time=time
            )

        def clear_scene():
            if self.mobjects:
                self.play(
                    *[
                        FadeOut(obj)
                        for obj in list(self.mobjects)
                    ],
                    run_time=0.5
                )
            self.wait(0.25)

        # ============================================================
        # SCENE 1 — SECTION INTRO
        # ============================================================

        chapter = txt(
            "CHAPTER 3",
            24,
            CYAN,
            BOLD
        )

        heading = txt(
            "Probability and Information Theory",
            38,
            WHITE,
            BOLD
        )

        section = txt(
            "3.12  Transforming Continuous Variables",
            28,
            YELLOW
        )

        chapter.to_edge(
            UP,
            buff=0.65
        )

        heading.next_to(
            chapter,
            DOWN,
            buff=0.25
        )

        section.next_to(
            heading,
            DOWN,
            buff=0.35
        )

        show(chapter, 0.5)
        show(heading, 0.75)
        show(section, 0.6)

        self.wait(0.7)

        clear_scene()

        # ============================================================
        # SCENE 2 — THE PROBLEM
        # ============================================================

        title = txt(
            "Changing variables changes the space",
            31,
            WHITE,
            BOLD
        )

        title.to_edge(
            UP,
            buff=0.7
        )

        statement = txt(
            "Suppose y = g(x).",
            22,
            MUTED
        )

        statement.next_to(
            title,
            DOWN,
            buff=0.35
        )

        show(title, 0.7)
        show(statement, 0.6)

        # ------------------------------------------------------------
        # X SPACE
        # ------------------------------------------------------------

        x_axis = NumberLine(
            x_range=[0, 1, 0.25],
            length=5.0,
            include_numbers=True,
            font_size=18,
            color=MUTED
        )

        x_axis.move_to(
            LEFT * 2.7 + DOWN * 0.5
        )

        x_label = MathTex(
            "x",
            font_size=30,
            color=CYAN
        )

        x_label.next_to(
            x_axis,
            UP,
            buff=0.25
        )

        # ------------------------------------------------------------
        # Y SPACE
        # ------------------------------------------------------------

        y_axis = NumberLine(
            x_range=[0, 0.5, 0.125],
            length=2.5,
            include_numbers=True,
            font_size=18,
            color=MUTED
        )

        y_axis.move_to(
            RIGHT * 2.7 + DOWN * 0.5
        )

        y_label = MathTex(
            "y",
            font_size=30,
            color=YELLOW
        )

        y_label.next_to(
            y_axis,
            UP,
            buff=0.25
        )

        self.play(
            Create(x_axis),
            FadeIn(x_label),
            run_time=0.7
        )

        # x interval
        x_region = Line(
            x_axis.n2p(0),
            x_axis.n2p(1),
            color=CYAN,
            stroke_width=8
        )

        self.play(
            Create(x_region),
            run_time=0.5
        )

        arrow = Arrow(
            x_axis.get_right() + RIGHT * 0.25,
            y_axis.get_left() + LEFT * 0.25,
            color=YELLOW,
            stroke_width=3
        )

        transform_label = MathTex(
            r"y=\frac{x}{2}",
            font_size=28,
            color=YELLOW
        )

        transform_label.next_to(
            arrow,
            UP,
            buff=0.15
        )

        self.play(
            GrowArrow(arrow),
            Write(transform_label),
            run_time=0.7
        )

        self.play(
            Create(y_axis),
            FadeIn(y_label),
            run_time=0.6
        )

        y_region = Line(
            y_axis.n2p(0),
            y_axis.n2p(0.5),
            color=YELLOW,
            stroke_width=8
        )

        self.play(
            Create(y_region),
            run_time=0.6
        )

        distortion = txt(
            "The interval was compressed.",
            18,
            RED
        )

        distortion.to_edge(
            DOWN,
            buff=0.65
        )

        self.play(
            FadeIn(distortion, shift=UP * 0.15),
            run_time=0.5
        )

        self.wait(0.7)

        clear_scene()

        # ============================================================
        # SCENE 3 — WHY THE NAIVE DENSITY FAILS
        # ============================================================

        title = txt(
            "The density must compensate for the distortion",
            29,
            WHITE,
            BOLD
        )

        title.to_edge(
            UP,
            buff=0.7
        )

        naive = MathTex(
            r"p_y(y)=p_x(2y)",
            font_size=36,
            color=RED
        )

        naive.move_to(
            UP * 0.8
        )

        show(title, 0.7)

        self.play(
            Write(naive),
            run_time=0.9
        )

        wrong = txt(
            "This forgets that the transformation changed the size of the space.",
            18,
            MUTED
        )

        wrong.next_to(
            naive,
            DOWN,
            buff=0.35
        )

        show(wrong, 0.7)

        # ------------------------------------------------------------
        # WRONG DISTRIBUTION
        # ------------------------------------------------------------

        wrong_axes = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 2, 0.5],
            x_length=7.0,
            y_length=2.7,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": False
            },
            tips=False
        )

        wrong_axes.next_to(
            wrong,
            DOWN,
            buff=0.45
        )

        wrong_curve = wrong_axes.plot(
            lambda x: 2 if x <= 0.5 else 0,
            x_range=[0, 1],
            color=RED,
            stroke_width=4
        )

        self.play(
            Create(wrong_axes),
            run_time=0.6
        )

        self.play(
            Create(wrong_curve),
            run_time=0.9
        )

        integral = MathTex(
            r"\int p_y(y)\,dy=\frac{1}{2}\neq1",
            font_size=29,
            color=RED
        )

        integral.to_edge(
            DOWN,
            buff=0.7
        )

        self.play(
            Write(integral),
            run_time=0.8
        )

        self.wait(0.7)

        clear_scene()

        # ============================================================
        # SCENE 4 — PRESERVE PROBABILITY MASS
        # ============================================================

        title = txt(
            "Probability mass must stay the same",
            31,
            WHITE,
            BOLD
        )

        title.to_edge(
            UP,
            buff=0.7
        )

        statement = txt(
            "A tiny region may change size — but its probability cannot disappear.",
            18,
            MUTED
        )

        statement.next_to(
            title,
            DOWN,
            buff=0.35
        )

        show(title, 0.7)
        show(statement, 0.7)

        # ------------------------------------------------------------
        # SMALL X INTERVAL
        # ------------------------------------------------------------

        xline = Line(
            LEFT * 4.2,
            RIGHT * 4.2,
            color=MUTED,
            stroke_width=2
        )

        xline.move_to(
            DOWN * 0.8
        )

        x_interval = Line(
            LEFT * 1.2,
            RIGHT * 1.2,
            color=CYAN,
            stroke_width=9
        )

        x_interval.move_to(
            xline.get_center() + LEFT * 1.7
        )

        x_delta = MathTex(
            "dx",
            font_size=27,
            color=CYAN
        )

        x_delta.next_to(
            x_interval,
            UP,
            buff=0.15
        )

        self.play(
            Create(xline),
            Create(x_interval),
            FadeIn(x_delta),
            run_time=0.7
        )

        # ------------------------------------------------------------
        # Y INTERVAL
        # ------------------------------------------------------------

        y_interval = Line(
            LEFT * 0.55,
            RIGHT * 0.55,
            color=YELLOW,
            stroke_width=9
        )

        y_interval.move_to(
            xline.get_center() + RIGHT * 2.2
        )

        y_delta = MathTex(
            "dy",
            font_size=27,
            color=YELLOW
        )

        y_delta.next_to(
            y_interval,
            UP,
            buff=0.15
        )

        arrow = Arrow(
            x_interval.get_right(),
            y_interval.get_left(),
            buff=0.25,
            color=MUTED,
            stroke_width=3
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.5
        )

        self.play(
            Create(y_interval),
            FadeIn(y_delta),
            run_time=0.6
        )

        # ------------------------------------------------------------
        # MASS EQUALITY
        # ------------------------------------------------------------

        mass = MathTex(
            r"|p_y(y)\,dy|=|p_x(x)\,dx|",
            font_size=34,
            color=GREEN
        )

        mass.to_edge(
            DOWN,
            buff=0.7
        )

        self.play(
            Write(mass),
            run_time=1.0
        )

        self.play(
            Indicate(
                mass,
                color=GREEN,
                scale_factor=1.08
            ),
            run_time=0.6
        )

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 5 — THE DERIVATIVE APPEARS
        # ============================================================

        title = txt(
            "The derivative tells us how much space changed",
            29,
            WHITE,
            BOLD
        )

        title.to_edge(
            UP,
            buff=0.7
        )

        formula = MathTex(
            r"p_y(y)=p_x(g^{-1}(y))"
            r"\left|\frac{\partial x}{\partial y}\right|",
            font_size=35,
            color=YELLOW
        )

        formula.move_to(
            ORIGIN + UP * 0.5
        )

        show(title, 0.7)

        self.play(
            Write(formula),
            run_time=1.2
        )

        explanation = txt(
            "The absolute derivative corrects for stretching or compression.",
            18,
            MUTED
        )

        explanation.next_to(
            formula,
            DOWN,
            buff=0.4
        )

        show(explanation, 0.7)

        # Highlight derivative
        derivative_box = SurroundingRectangle(
            formula[-1],
            color=CYAN,
            buff=0.12,
            stroke_width=2
        )

        derivative_note = txt(
            "change in scale",
            17,
            CYAN,
            BOLD
        )

        derivative_note.next_to(
            derivative_box,
            DOWN,
            buff=0.25
        )

        self.play(
            Create(derivative_box),
            FadeIn(derivative_note),
            run_time=0.6
        )

        self.wait(0.9)

        clear_scene()

        # ============================================================
        # SCENE 6 — FROM DERIVATIVE TO JACOBIAN
        # ============================================================

        title = txt(
            "In higher dimensions, the derivative becomes a Jacobian",
            28,
            WHITE,
            BOLD
        )

        title.to_edge(
            UP,
            buff=0.7
        )

        show(title, 0.7)

        # ------------------------------------------------------------
        # LEFT — GRID IN X SPACE
        # ------------------------------------------------------------

        x_grid = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=3.6,
            y_length=3.6,
            background_line_style={
                "stroke_color": MUTED,
                "stroke_width": 1,
                "stroke_opacity": 0.35
            },
            axis_config={
                "stroke_color": MUTED,
                "stroke_width": 2
            }
        )

        x_grid.move_to(
            LEFT * 2.8 + DOWN * 0.5
        )

        x_label = MathTex(
            r"\mathbf{x}",
            font_size=28,
            color=CYAN
        )

        x_label.next_to(
            x_grid,
            DOWN,
            buff=0.25
        )

        # ------------------------------------------------------------
        # RIGHT — TRANSFORMED GRID
        # ------------------------------------------------------------

        y_grid = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4.8,
            y_length=2.7,
            background_line_style={
                "stroke_color": YELLOW,
                "stroke_width": 1,
                "stroke_opacity": 0.45
            },
            axis_config={
                "stroke_color": YELLOW,
                "stroke_width": 2
            }
        )

        y_grid.move_to(
            RIGHT * 2.8 + DOWN * 0.5
        )

        y_label2 = MathTex(
            r"\mathbf{y}",
            font_size=28,
            color=YELLOW
        )

        y_label2.next_to(
            y_grid,
            DOWN,
            buff=0.25
        )

        self.play(
            Create(x_grid),
            FadeIn(x_label),
            run_time=0.7
        )

        transform_arrow = Arrow(
            x_grid.get_right(),
            y_grid.get_left(),
            buff=0.3,
            color=CYAN,
            stroke_width=3
        )

        self.play(
            GrowArrow(transform_arrow),
            run_time=0.5
        )

        self.play(
            Create(y_grid),
            FadeIn(y_label2),
            run_time=0.8
        )

        # Jacobian formula
        jacobian = MathTex(
            r"p_x(\mathbf{x})"
            r"="
            r"p_y(g(\mathbf{x}))"
            r"\left|"
            r"\det\left("
            r"\frac{\partial g(\mathbf{x})}{\partial\mathbf{x}}"
            r"\right)"
            r"\right|",
            font_size=28,
            color=GREEN
        )

        jacobian.to_edge(
            DOWN,
            buff=0.6
        )

        fit_in_frame(
            jacobian,
            margin=0.7
        )

        self.play(
            Write(jacobian),
            run_time=1.3
        )

        self.wait(1.0)

        clear_scene()

        # ============================================================
        # SCENE 7 — FINAL TAKEAWAY
        # ============================================================

        label = txt(
            "THE KEY IDEA",
            23,
            CYAN,
            BOLD
        )

        label.to_edge(
            UP,
            buff=0.85
        )

        main = txt(
            "When variables change, probability density\n"
            "must compensate for the change in space.",
            25,
            WHITE,
            BOLD
        )

        main.move_to(
            ORIGIN + UP * 0.25
        )

        fit_in_frame(
            main,
            margin=0.8
        )

        show(label, 0.5)

        self.play(
            Write(main),
            run_time=1.3
        )

        # Main mathematical takeaway
        math_note = MathTex(
            r"\text{1D: derivative}"
            r"\qquad\longrightarrow\qquad"
            r"\text{ND: Jacobian determinant}",
            font_size=28,
            color=YELLOW
        )

        math_note.next_to(
            main,
            DOWN,
            buff=0.5
        )

        fit_in_frame(
            math_note,
            margin=0.7
        )

        self.play(
            Write(math_note),
            run_time=1.0
        )

        # Final note
        note = txt(
            "The Jacobian measures how the transformation stretches or compresses space.",
            17,
            MUTED
        )

        note.to_edge(
            DOWN,
            buff=0.65
        )

        self.play(
            FadeIn(
                note,
                shift=UP * 0.15
            ),
            run_time=0.6
        )

        underline = Underline(
            main,
            color=CYAN,
            stroke_width=3,
            buff=0.16
        )

        self.play(
            Create(underline),
            run_time=0.5
        )

        self.wait(2.0)


if __name__ == "__main__":
    Page70().render()
