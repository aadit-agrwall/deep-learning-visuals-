import numpy as np
from manim import *

from common.layouts import fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle


class Page67(Scene):

    def construct(self):

        # ============================================================
        # THEME — SAME AS PAGE 66
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
            self.play(Write(obj), run_time=time)

        def clear_scene():
            if self.mobjects:
                self.play(
                    *[FadeOut(obj) for obj in list(self.mobjects)],
                    run_time=0.5
                )
            self.wait(0.25)

        # ============================================================
        # SCENE 1 — PAGE INTRO
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 38, WHITE, BOLD)
        subheading = txt("Sigmoid and Softplus", 30, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        subheading.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.75)
        show(subheading, 0.6)

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 2 — SIGMOID INTRODUCTION
        # ============================================================

        title = txt(
            "The logistic sigmoid function",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.65)

        formula = MathTex(
            r"\sigma(x)=\frac{1}{1+e^{-x}}",
            font_size=36,
            color=YELLOW
        )
        formula.next_to(title, DOWN, buff=0.35)

        statement = txt(
            "It transforms any real number into a value between 0 and 1.",
            19,
            MUTED
        )
        statement.next_to(formula, DOWN, buff=0.25)

        show(title, 0.7)
        show(formula, 0.9)
        show(statement, 0.7)

        # ============================================================
        # SIGMOID GRAPH
        # ============================================================

        axes = Axes(
            x_range=[-10, 10, 5],
            y_range=[0, 1, 0.2],
            x_length=8.2,
            y_length=3.8,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": False,
            },
            tips=False,
        )

        axes.next_to(statement, DOWN, buff=0.35)

        x_label = MathTex("x", font_size=21, color=MUTED)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.15)

        y_label = MathTex(r"\sigma(x)", font_size=21, color=MUTED)
        y_label.next_to(axes.y_axis, UP, buff=0.15)

        sigmoid = axes.plot(
            lambda x: 1 / (1 + np.exp(-x)),
            x_range=[-10, 10],
            color=CYAN,
            stroke_width=4,
        )

        # Horizontal guide lines for 0 and 1
        lower_line = DashedLine(
            axes.c2p(-10, 0),
            axes.c2p(10, 0),
            color=MUTED,
            stroke_opacity=0.35,
            dash_length=0.08
        )

        upper_line = DashedLine(
            axes.c2p(-10, 1),
            axes.c2p(10, 1),
            color=MUTED,
            stroke_opacity=0.35,
            dash_length=0.08
        )

        self.play(
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=0.8
        )

        self.play(
            Create(lower_line),
            Create(upper_line),
            run_time=0.4
        )

        self.play(
            Create(sigmoid),
            run_time=1.7,
            rate_func=smooth
        )

        # ============================================================
        # SIGMOID — HIGHLIGHT VALID RANGE
        # ============================================================

        range_note = txt(
            "0 < σ(x) < 1",
            23,
            GREEN,
            BOLD
        )
        range_note.next_to(axes, DOWN, buff=0.3)

        show(range_note, 0.6)

        # Highlight center
        center_dot = Dot(
            axes.c2p(0, 0.5),
            radius=0.07,
            color=YELLOW
        )

        center_line = DashedLine(
            axes.c2p(0, 0),
            axes.c2p(0, 0.5),
            color=YELLOW,
            stroke_width=2,
            dash_length=0.08
        )

        self.play(
            Create(center_line),
            FadeIn(center_dot),
            run_time=0.6
        )

        center_note = txt(
            "At x = 0,  σ(x) = 0.5",
            17,
            YELLOW
        )
        center_note.next_to(center_dot, RIGHT, buff=0.25)

        show(center_note, 0.5)

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 3 — SOFTPLUS INTRODUCTION
        # ============================================================

        title = txt(
            "The softplus function",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.65)

        formula = MathTex(
            r"\zeta(x)=\log(1+e^x)",
            font_size=36,
            color=YELLOW
        )
        formula.next_to(title, DOWN, buff=0.35)

        statement = txt(
            "A smooth version of max(0, x).",
            21,
            MUTED
        )
        statement.next_to(formula, DOWN, buff=0.25)

        show(title, 0.7)
        show(formula, 0.9)
        show(statement, 0.7)

        # ============================================================
        # SOFTPLUS GRAPH
        # ============================================================

        axes2 = Axes(
            x_range=[-10, 10, 5],
            y_range=[0, 10, 2],
            x_length=8.2,
            y_length=4.0,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": False,
            },
            tips=False,
        )

        axes2.next_to(statement, DOWN, buff=0.35)

        x_label2 = MathTex("x", font_size=21, color=MUTED)
        x_label2.next_to(axes2.x_axis, RIGHT, buff=0.15)

        y_label2 = MathTex(r"\zeta(x)", font_size=21, color=MUTED)
        y_label2.next_to(axes2.y_axis, UP, buff=0.15)

        # Softplus
        def softplus(x):
            # Numerically stable softplus
            return np.logaddexp(0, x)

        softplus_curve = axes2.plot(
            softplus,
            x_range=[-10, 10],
            color=CYAN,
            stroke_width=4,
        )

        # ReLU comparison
        relu_curve = axes2.plot(
            lambda x: max(0, x),
            x_range=[-10, 10],
            color=RED,
            stroke_width=2.5,
            stroke_opacity=0.65,
        )

        self.play(
            Create(axes2),
            FadeIn(x_label2),
            FadeIn(y_label2),
            run_time=0.8
        )

        # First reveal ReLU as the simple idea
        self.play(
            Create(relu_curve),
            run_time=1.1
        )

        relu_label = MathTex(
            r"\max(0,x)",
            font_size=22,
            color=RED
        )
        relu_label.next_to(
            axes2.c2p(5, 5),
            UP,
            buff=0.15
        )

        self.play(
            FadeIn(relu_label),
            run_time=0.4
        )

        self.wait(0.4)

        # Softplus appears over it
        self.play(
            Create(softplus_curve),
            run_time=1.7,
            rate_func=smooth
        )

        softplus_label = MathTex(
            r"\zeta(x)",
            font_size=24,
            color=CYAN
        )
        softplus_label.next_to(
            axes2.c2p(6.5, softplus(6.5)),
            UP,
            buff=0.15
        )

        self.play(
            FadeIn(softplus_label),
            run_time=0.5
        )

        # ============================================================
        # HIGHLIGHT SMOOTHNESS
        # ============================================================

        smooth_note = txt(
            "Same idea — but smooth and differentiable.",
            18,
            GREEN
        )
        smooth_note.next_to(axes2, DOWN, buff=0.3)

        show(smooth_note, 0.6)

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 4 — SIGMOID vs SOFTPLUS
        # ============================================================

        title = txt(
            "Two functions, two different jobs",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        # ------------------------------------------------------------
        # LEFT — SIGMOID
        # ------------------------------------------------------------

        sigmoid_box = RoundedRectangle(
            width=4.5,
            height=3.7,
            corner_radius=0.15,
            stroke_color=CYAN,
            stroke_width=2
        )

        sigmoid_box.shift(LEFT * 2.45 + DOWN * 0.15)

        sigmoid_title = txt(
            "SIGMOID",
            23,
            CYAN,
            BOLD
        )
        sigmoid_title.move_to(
            sigmoid_box.get_top() + DOWN * 0.4
        )

        sigmoid_formula = MathTex(
            r"\sigma(x)\in(0,1)",
            font_size=30,
            color=YELLOW
        )
        sigmoid_formula.next_to(
            sigmoid_title,
            DOWN,
            buff=0.4
        )

        sigmoid_desc = txt(
            "Useful when a value\nmust behave like a probability.",
            17,
            WHITE
        )
        sigmoid_desc.next_to(
            sigmoid_formula,
            DOWN,
            buff=0.35
        )

        # ------------------------------------------------------------
        # RIGHT — SOFTPLUS
        # ------------------------------------------------------------

        softplus_box = RoundedRectangle(
            width=4.5,
            height=3.7,
            corner_radius=0.15,
            stroke_color=CYAN,
            stroke_width=2
        )

        softplus_box.shift(RIGHT * 2.45 + DOWN * 0.15)

        softplus_title2 = txt(
            "SOFTPLUS",
            23,
            CYAN,
            BOLD
        )
        softplus_title2.move_to(
            softplus_box.get_top() + DOWN * 0.4
        )

        softplus_formula2 = MathTex(
            r"\zeta(x)>0",
            font_size=30,
            color=YELLOW
        )
        softplus_formula2.next_to(
            softplus_title2,
            DOWN,
            buff=0.4
        )

        softplus_desc2 = txt(
            "Useful when a parameter\nmust stay smoothly positive.",
            17,
            WHITE
        )
        softplus_desc2.next_to(
            softplus_formula2,
            DOWN,
            buff=0.35
        )

        # ------------------------------------------------------------
        # ANIMATE CARDS
        # ------------------------------------------------------------

        self.play(
            FadeIn(sigmoid_box, shift=LEFT * 0.3),
            FadeIn(softplus_box, shift=RIGHT * 0.3),
            run_time=0.8
        )

        self.play(
            FadeIn(sigmoid_title),
            FadeIn(sigmoid_formula),
            FadeIn(sigmoid_desc),
            run_time=0.8
        )

        self.play(
            FadeIn(softplus_title2),
            FadeIn(softplus_formula2),
            FadeIn(softplus_desc2),
            run_time=0.8
        )

        # ============================================================
        # CENTER CONNECTOR
        # ============================================================

        arrow = Arrow(
            sigmoid_box.get_right(),
            softplus_box.get_left(),
            buff=0.15,
            color=MUTED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.12
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.5
        )

        self.wait(1.0)

        clear_scene()

        # ============================================================
        # SCENE 5 — FINAL TAKEAWAY
        # ============================================================

        label = txt(
            "THE KEY IDEA",
            23,
            CYAN,
            BOLD
        )
        label.to_edge(UP, buff=0.85)

        main = txt(
            "Sigmoid gives us a bounded probability-like value.\n"
            "Softplus gives us a smooth positive value.",
            27,
            WHITE,
            BOLD
        )

        main.move_to(ORIGIN + UP * 0.15)
        fit_in_frame(main, margin=0.9)

        show(label, 0.5)
        self.play(
            Write(main),
            run_time=1.3
        )

        # Small mathematical anchors
        left_math = MathTex(
            r"0<\sigma(x)<1",
            font_size=28,
            color=YELLOW
        )

        right_math = MathTex(
            r"\zeta(x)>0",
            font_size=28,
            color=GREEN
        )

        left_math.next_to(main, DOWN, buff=0.45)
        right_math.next_to(left_math, RIGHT, buff=1.0)

        self.play(
            FadeIn(left_math, shift=UP * 0.15),
            FadeIn(right_math, shift=UP * 0.15),
            run_time=0.7
        )

        # Final note
        note = txt(
            "Choose the transformation that matches the constraint.",
            18,
            MUTED
        )
        note.to_edge(DOWN, buff=0.65)

        self.play(
            FadeIn(note, shift=UP * 0.15),
            run_time=0.6
        )

        # Final emphasis
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
    Page67().render()
