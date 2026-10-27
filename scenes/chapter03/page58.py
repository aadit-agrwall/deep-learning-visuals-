import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page58(Scene):

    def construct(self):

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"

        self.camera.background_color = BG

        def txt(text, size=28, color=WHITE, weight=NORMAL):
            return Text(text, font="DejaVu Sans", font_size=size, color=color, weight=weight)

        def show(obj, time=0.7):
            self.play(Write(obj), run_time=time)

        def clear_scene():
            if self.mobjects:
                self.play(*[FadeOut(obj) for obj in list(self.mobjects)], run_time=0.5)
            self.wait(0.3)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 40, WHITE, BOLD)
        section = txt("3.7 – 3.8  Independence & Expectation", 26, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — CHAIN RULE APPLIED TWICE (three variables)
        # ============================================================

        title = txt("Chain rule, applied twice", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Break a 3-variable joint into conditionals, one step at a time.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.75)
        self.wait(0.3)

        line1 = MathTex(r"P(a,b,c) = P(a \mid b,c)\,P(b,c)", font_size=28, color=WHITE)
        line2 = MathTex(r"P(b,c) = P(b \mid c)\,P(c)", font_size=28, color=YELLOW)
        line3 = MathTex(r"P(a,b,c) = P(a \mid b,c)\,P(b \mid c)\,P(c)", font_size=30, color=GREEN)

        lines = VGroup(line1, line2, line3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        lines.move_to(DOWN * 0.2)

        self.play(Write(line1), run_time=1.0)
        self.wait(0.5)
        self.play(Write(line2), run_time=1.0)
        self.wait(0.5)

        substitute_note = txt("substitute line 2 into line 1", 18, MUTED)
        substitute_note.next_to(line2, DOWN, buff=0.3)
        show(substitute_note, 0.5)
        self.wait(0.4)
        self.play(FadeOut(substitute_note), run_time=0.3)

        self.play(Write(line3), run_time=1.2)
        emphasize_then_settle(self, line3, chapter="chapter03")

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 3 — INDEPENDENCE
        # ============================================================

        title = txt("Independence", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "The joint splits cleanly into two separate factors.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.7)

        joint_box = titled_box("Joint", MathTex("p(x, y)", font_size=26, color=WHITE), chapter="chapter03", width=3.0, height=1.4)
        joint_box.move_to(UP * 0.1)

        equals = MathTex("=", font_size=32, color=WHITE)
        equals.next_to(joint_box, DOWN, buff=0.35)

        x_box = titled_box("x alone", MathTex("p(x)", font_size=24, color=CYAN), chapter="chapter03", width=2.6, height=1.3)
        y_box = titled_box("y alone", MathTex("p(y)", font_size=24, color=YELLOW), chapter="chapter03", width=2.6, height=1.3)

        factor_row = flow_row([x_box, y_box], buff=0.6)
        factor_row.next_to(equals, DOWN, buff=0.35)

        self.play(GrowFromCenter(joint_box), run_time=0.7)
        self.play(FadeIn(equals), run_time=0.3)
        self.play(FadeIn(factor_row, lag_ratio=0.25), run_time=0.9)

        notation = MathTex(r"\mathrm{x} \perp \mathrm{y}", font_size=30, color=GREEN)
        notation.next_to(factor_row, DOWN, buff=0.5)
        show(notation, 0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 4 — CONDITIONAL INDEPENDENCE
        # ============================================================

        title = txt("Conditional independence", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Independent once you already know z.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.7)

        z_box = titled_box("Given z", MathTex("z = z", font_size=22, color=WHITE), chapter="chapter03", width=2.6, height=1.2)
        z_box.to_edge(UP, buff=2.2)

        joint_given = titled_box(
            "Joint | z", MathTex("p(x, y \\mid z)", font_size=24, color=WHITE),
            chapter="chapter03", width=3.4, height=1.3,
        )
        joint_given.move_to(DOWN * 0.2)

        x_given = titled_box("x | z", MathTex("p(x \\mid z)", font_size=22, color=CYAN), chapter="chapter03", width=2.6, height=1.2)
        y_given = titled_box("y | z", MathTex("p(y \\mid z)", font_size=22, color=YELLOW), chapter="chapter03", width=2.6, height=1.2)

        given_row = flow_row([x_given, y_given], buff=0.6)
        given_row.next_to(joint_given, DOWN, buff=0.6)

        arrow_z1 = smart_arrow(z_box, joint_given, chapter="chapter03", color=WHITE)

        self.play(FadeIn(z_box), run_time=0.5)
        self.play(GrowArrow(arrow_z1), run_time=0.4)
        self.play(GrowFromCenter(joint_given), run_time=0.6)
        self.play(FadeIn(given_row, lag_ratio=0.25), run_time=0.9)

        notation2 = MathTex(r"\mathrm{x} \perp \mathrm{y} \mid \mathrm{z}", font_size=28, color=GREEN)
        notation2.next_to(given_row, DOWN, buff=0.5)
        show(notation2, 0.6)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — EXPECTATION (discrete)
        # ============================================================

        title = txt("Expectation: the average outcome", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Weight each outcome of f(x) by how likely it is.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.7)

        # weighted bars converging to one averaged value
        bar_data = [(0.5, 0.2), (1.4, 0.4), (0.9, 0.3), (1.8, 0.1)]  # (f(x), P(x))
        bars = VGroup()
        for i, (fx, px) in enumerate(bar_data):
            bar = Rectangle(width=0.6, height=fx, fill_color=CYAN, fill_opacity=px + 0.3, stroke_width=0)
            bar.move_to(LEFT * 3.0 + RIGHT * i * 1.0 + DOWN * (1.8 - fx / 2))
            weight_label = Text(f"P={px}", font="DejaVu Sans", font_size=14, color=MUTED)
            weight_label.next_to(bar, DOWN, buff=0.1)
            bars.add(VGroup(bar, weight_label))
        bars.move_to(DOWN * 1.4 + LEFT * 1.5)

        baseline = Line(
            bars[0].get_corner(DL) + LEFT * 0.3,
            bars[-1].get_corner(DR) + RIGHT * 0.3,
            color=MUTED, stroke_width=1.5,
        )

        self.play(Create(baseline), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.15), run_time=1.1)

        expected_val = sum(fx * px for fx, px in bar_data)
        expected_line = DashedLine(
            [bars.get_left()[0] - 0.3, baseline.get_y() + expected_val, 0],
            [bars.get_right()[0] + 0.3, baseline.get_y() + expected_val, 0],
            color=GREEN, stroke_width=2.5,
        )
        expected_tag = Text(f"E[f(x)] ≈ {expected_val:.2f}", font="DejaVu Sans", font_size=18, color=GREEN)
        expected_tag.next_to(expected_line, RIGHT, buff=0.2)

        self.play(Create(expected_line), FadeIn(expected_tag), run_time=0.8)

        formula_d = MathTex(r"\mathbb{E}_{\mathrm{x}\sim P}[f(x)] = \sum_x P(x)f(x)", font_size=24, color=WHITE)
        formula_d.next_to(bars, RIGHT, buff=1.4).align_to(bars, UP)
        show(formula_d, 0.8)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 6 — EXPECTATION (continuous)
        # ============================================================

        title = txt("The continuous case: integrate", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.2, 0.5],
            x_length=7, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.move_to(DOWN * 0.6)

        curve = axes.plot(lambda x: 0.9 * np.exp(-((x - 3) ** 2) / 2), color=CYAN, stroke_width=3)
        area = axes.get_area(curve, x_range=(0, 6), color=YELLOW, opacity=0.3)

        self.play(Create(axes), run_time=0.7)
        self.play(Create(curve), run_time=0.9)
        self.play(FadeIn(area), run_time=0.7)

        formula_c = MathTex(r"\mathbb{E}_{\mathrm{x}\sim p}[f(x)] = \int p(x)f(x)\,dx", font_size=28, color=GREEN)
        formula_c.next_to(axes, DOWN, buff=0.5)
        show(formula_c, 0.9)

        emphasize_then_settle(self, formula_c, chapter="chapter03")

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Independence splits the joint apart.\nExpectation averages what's left.",
            30, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)

        self.play(Write(final), run_time=1.0)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page58().render()
