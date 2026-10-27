import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page60(Scene):

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
        section = txt("3.8 – 3.9  Covariance Matrix & Common Distributions", 23, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — DEPENDENT BUT ZERO COVARIANCE (the x,s,y example)
        # ============================================================

        title = txt("Dependent, yet zero covariance", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "x is uniform on [-1, 1].  s is +1 or -1, each with probability ½.  y = s·x.",
            20, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.9)
        self.wait(0.4)

        # visualize: x on a number line, then two mirrored branches for s=+1 / s=-1
        x_line = NumberLine(x_range=[-1, 1, 1], length=5, color=MUTED, include_numbers=False)
        x_line.move_to(UP * 0.7)
        x_dot = Dot(x_line.n2p(0.6), radius=0.08, color=CYAN)
        x_label = MathTex("x", font_size=22, color=CYAN).next_to(x_dot, UP, buff=0.15)

        self.play(Create(x_line), FadeIn(x_dot), FadeIn(x_label), run_time=0.8)

        s_pos_box = titled_box("s = +1  (prob ½)", MathTex("y = x", font_size=22, color=GREEN), chapter="chapter03", width=3.2, height=1.3)
        s_neg_box = titled_box("s = -1  (prob ½)", MathTex("y = -x", font_size=22, color=RED), chapter="chapter03", width=3.2, height=1.3)

        branches = flow_row([s_pos_box, s_neg_box], buff=1.0)
        branches.next_to(x_line, DOWN, buff=0.8)
        fit_in_frame(branches, margin=1.0)

        arrow_pos = smart_arrow(x_dot, s_pos_box, chapter="chapter03", color=GREEN)
        arrow_neg = smart_arrow(x_dot, s_neg_box, chapter="chapter03", color=RED)

        self.play(FadeIn(branches, lag_ratio=0.2), run_time=0.9)
        self.play(GrowArrow(arrow_pos), GrowArrow(arrow_neg), run_time=0.7)

        conclusion = VGroup(
            txt("x determines |y|  →  dependent", 18, YELLOW),
            MathTex(r"\mathrm{Cov}(x, y) = 0", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.3)
        conclusion.next_to(branches, DOWN, buff=0.6)
        show(conclusion, 1.0)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — COVARIANCE MATRIX
        # ============================================================

        title = txt("The covariance matrix", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "For a random vector, every pair of components gets a covariance entry.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.8)

        formula = MathTex(r"\mathrm{Cov}(\mathbf{x})_{i,j} = \mathrm{Cov}(x_i, x_j)", font_size=28, color=WHITE)
        formula.next_to(statement, DOWN, buff=0.6)
        show(formula, 0.9)

        # 3x3 symbolic matrix, diagonal highlighted
        n = 3
        cell_size = 0.9
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                cell = Square(side_length=cell_size, stroke_color=MUTED, stroke_width=1.5)
                if i == j:
                    label = MathTex(f"\\mathrm{{Var}}(x_{i+1})", font_size=16, color=YELLOW)
                else:
                    label = MathTex(f"\\mathrm{{Cov}}(x_{i+1},x_{j+1})", font_size=13, color=WHITE)
                label.move_to(cell.get_center())
                cells.add(VGroup(cell, label))

        matrix = VGroup(*cells).arrange_in_grid(rows=n, cols=n, buff=0)
        matrix.next_to(formula, DOWN, buff=0.6)
        fit_in_frame(matrix, margin=1.0)

        self.play(FadeIn(matrix, lag_ratio=0.05), run_time=1.1)

        diagonal_note = MathTex(r"\mathrm{Cov}(x_i,x_i) = \mathrm{Var}(x_i)", font_size=22, color=YELLOW)
        diagonal_note.next_to(matrix, DOWN, buff=0.5)
        show(diagonal_note, 0.8)

        emphasize_then_settle(self, diagonal_note, chapter="chapter03")

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — BERNOULLI DISTRIBUTION
        # ============================================================

        title = txt("Bernoulli distribution", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "A single binary variable, controlled by one parameter φ.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        show(statement, 0.8)

        # two bars: P(x=1)=phi, P(x=0)=1-phi
        phi = 0.7
        bar1 = Rectangle(width=0.9, height=phi * 2.2, fill_color=CYAN, fill_opacity=0.85, stroke_width=0)
        bar0 = Rectangle(width=0.9, height=(1 - phi) * 2.2, fill_color=MUTED, fill_opacity=0.85, stroke_width=0)

        bar1_label = txt("x = 1", 18, WHITE)
        bar0_label = txt("x = 0", 18, WHITE)

        bars_row = VGroup(
            VGroup(bar1, bar1_label).arrange(DOWN, buff=0.2),
            VGroup(bar0, bar0_label).arrange(DOWN, buff=0.2),
        )
        bars_row.arrange(RIGHT, buff=1.0, aligned_edge=DOWN)
        bars_row.move_to(DOWN * 0.3)

        baseline = Line(
            bars_row.get_corner(DL) + LEFT * 0.3,
            bars_row.get_corner(DR) + RIGHT * 0.3,
            color=MUTED, stroke_width=1.5,
        )

        self.play(Create(baseline), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in [VGroup(bar1, bar1_label), VGroup(bar0, bar0_label)]], lag_ratio=0.2),
            run_time=1.0,
        )

        formulas = VGroup(
            MathTex(r"P(x{=}1)=\varphi", font_size=22, color=CYAN),
            MathTex(r"P(x{=}0)=1-\varphi", font_size=22, color=MUTED),
            MathTex(r"P(x{=}x)=\varphi^x(1-\varphi)^{1-x}", font_size=22, color=WHITE),
            MathTex(r"\mathbb{E}_x[x]=\varphi", font_size=22, color=YELLOW),
            MathTex(r"\mathrm{Var}_x(x)=\varphi(1-\varphi)", font_size=22, color=GREEN),
        )
        formulas.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        formulas.next_to(bars_row, RIGHT, buff=1.2).align_to(bars_row, UP)
        fit_in_frame(VGroup(bars_row, formulas), margin=0.8)

        self.play(FadeIn(formulas, lag_ratio=0.2), run_time=1.2)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — MULTINOULLI / CATEGORICAL DISTRIBUTION
        # ============================================================

        title = txt("Multinoulli (categorical) distribution", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "One discrete variable, k possible states — the multi-outcome version of Bernoulli.",
            20, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.9)

        k = 5
        cat_bars = VGroup()
        heights = [0.6, 1.2, 1.9, 0.9, 1.4]
        for i, h in enumerate(heights):
            bar = Rectangle(width=0.7, height=h, fill_color=CYAN, fill_opacity=0.85, stroke_width=0)
            label = MathTex(f"x_{i+1}", font_size=18, color=MUTED)
            group = VGroup(bar, label).arrange(DOWN, buff=0.15)
            cat_bars.add(group)
        cat_bars.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        cat_bars.move_to(DOWN * 0.4)
        fit_in_frame(cat_bars, margin=1.0)

        cat_baseline = Line(
            cat_bars.get_corner(DL) + LEFT * 0.3,
            cat_bars.get_corner(DR) + RIGHT * 0.3,
            color=MUTED, stroke_width=1.5,
        )

        self.play(Create(cat_baseline), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in cat_bars], lag_ratio=0.15), run_time=1.2)

        note = txt("special case of the multinomial distribution (n = 1 draw)", 18, YELLOW)
        note.next_to(cat_bars, DOWN, buff=0.6)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Zero covariance is not proof of independence.\nBernoulli and Multinoulli model simple choices.",
            27, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)
        fit_in_frame(final, margin=1.0)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page60().render()
