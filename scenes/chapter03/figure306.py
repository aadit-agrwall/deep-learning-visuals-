from manim import *
import numpy as np
from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Figure306(Scene):

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
        section = txt("3.3.2 – 3.4  Densities & Marginal Probability", 26, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — PDF: A CURVE, NOT A DIRECT PROBABILITY
        # ============================================================

        title = txt("Continuous variables need a density", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "p(x) is a curve — height is not itself a probability.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.7)
        self.wait(0.4)

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.2, 0.5],
            x_length=7, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.move_to(DOWN * 0.6)

        curve = axes.plot(lambda x: 0.9 * np.exp(-((x - 3) ** 2) / 2), color=CYAN, stroke_width=3)

        self.play(Create(axes), run_time=0.9)
        self.play(Create(curve), run_time=1.1)
        self.wait(0.5)

        p_label = MathTex("p(x)", font_size=28, color=CYAN)
        p_label.next_to(curve.get_point_from_function(0.15), UP, buff=0.2)
        show(p_label, 0.5)

        self.wait(1.2)
        clear_scene()

        # ============================================================
        # SCENE 3 — INTEGRATING TO GET REAL PROBABILITY
        # ============================================================

        title = txt("Area under the curve = probability", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        axes2 = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.2, 0.5],
            x_length=7, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes2.move_to(DOWN * 0.5)

        curve2 = axes2.plot(lambda x: 0.9 * np.exp(-((x - 3) ** 2) / 2), color=CYAN, stroke_width=3)

        a_val, b_val = 2, 4
        shaded = axes2.get_area(curve2, x_range=(a_val, b_val), color=YELLOW, opacity=0.45)

        a_line = DashedLine(axes2.c2p(a_val, 0), axes2.c2p(a_val, 1.0), color=MUTED, stroke_width=1.5)
        b_line = DashedLine(axes2.c2p(b_val, 0), axes2.c2p(b_val, 1.0), color=MUTED, stroke_width=1.5)
        a_label = MathTex("a", font_size=22, color=MUTED).next_to(a_line, DOWN, buff=0.15)
        b_label = MathTex("b", font_size=22, color=MUTED).next_to(b_line, DOWN, buff=0.15)

        self.play(Create(axes2), Create(curve2), run_time=1.0)
        self.play(Create(a_line), Create(b_line), FadeIn(a_label), FadeIn(b_label), run_time=0.7)
        self.play(FadeIn(shaded), run_time=1.0)

        integral_label = MathTex(r"\int_{[a,b]} p(x)\,dx", font_size=30, color=YELLOW)
        integral_label.next_to(axes2, DOWN, buff=0.5)
        show(integral_label, 0.8)

        emphasize_then_settle(self, integral_label, chapter="chapter03")

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 4 — CONTINUOUS UNIFORM DISTRIBUTION
        # ============================================================

        title = txt("Example: continuous uniform", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Equal density everywhere inside [a, b], zero outside.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.7)

        number_line = NumberLine(x_range=[0, 6, 1], length=8, color=MUTED, include_numbers=False)
        number_line.move_to(DOWN * 0.3)

        a_pt = number_line.n2p(1.5)
        b_pt = number_line.n2p(4.5)

        flat_region = Line(a_pt, b_pt, color=CYAN, stroke_width=6)
        flat_region.shift(UP * 0.7)

        zero_left = Line(number_line.n2p(0), a_pt, color=RED, stroke_width=3)
        zero_right = Line(b_pt, number_line.n2p(6), color=RED, stroke_width=3)
        zero_left.shift(UP * 0.02)
        zero_right.shift(UP * 0.02)

        a_tick = DashedLine(a_pt, a_pt + UP * 0.7, color=MUTED, stroke_width=1.5)
        b_tick = DashedLine(b_pt, b_pt + UP * 0.7, color=MUTED, stroke_width=1.5)
        a_label2 = MathTex("a", font_size=24, color=MUTED).next_to(a_pt, DOWN, buff=0.2)
        b_label2 = MathTex("b", font_size=24, color=MUTED).next_to(b_pt, DOWN, buff=0.2)

        self.play(Create(number_line), run_time=0.8)
        self.play(Create(a_tick), Create(b_tick), FadeIn(a_label2), FadeIn(b_label2), run_time=0.6)
        self.play(Create(zero_left), Create(zero_right), run_time=0.6)
        self.play(Create(flat_region), run_time=0.9)

        formula = MathTex(r"u(x;a,b) = \frac{1}{b-a}", font_size=30, color=CYAN)
        formula.next_to(number_line, DOWN, buff=0.9)
        show(formula, 0.8)

        notation = MathTex(r"\mathrm{x} \sim U(a,b)", font_size=26, color=GREEN)
        notation.next_to(formula, DOWN, buff=0.4)
        show(notation, 0.6)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — MARGINAL PROBABILITY (the visual centerpiece)
        # ============================================================

        title = txt("Marginal probability: the sum rule", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Know P(x, y). Want P(x) alone? Sum out y.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.7)
        self.wait(0.4)

        # build a 3x3 joint-probability grid
        rows, cols = 3, 3
        cell_size = 0.9
        grid_cells = VGroup()
        cell_values = [[0.05, 0.10, 0.05], [0.08, 0.20, 0.07], [0.10, 0.25, 0.10]]

        for r in range(rows):
            for c in range(cols):
                cell = Square(side_length=cell_size, stroke_color=MUTED, stroke_width=1.5)
                val_text = Text(f"{cell_values[r][c]:.2f}", font="DejaVu Sans", font_size=16, color=WHITE)
                val_text.move_to(cell.get_center())
                grid_cells.add(VGroup(cell, val_text))

        grid = VGroup(*grid_cells).arrange_in_grid(rows=rows, cols=cols, buff=0)
        grid.move_to(LEFT * 2.3 + DOWN * 0.3)

        y_axis_label = txt("y", 22, YELLOW)
        y_axis_label.next_to(grid, LEFT, buff=0.4)
        x_axis_label = txt("x", 22, CYAN)
        x_axis_label.next_to(grid, DOWN, buff=0.3)

        self.play(FadeIn(grid, lag_ratio=0.05), FadeIn(y_axis_label), FadeIn(x_axis_label), run_time=1.1)
        self.wait(0.5)

        joint_label = MathTex("P(\\mathrm{x}, \\mathrm{y})", font_size=26, color=WHITE)
        joint_label.next_to(grid, UP, buff=0.3)
        show(joint_label, 0.6)
        self.wait(0.6)

        # highlight each column, then collapse it into a marginal bar
        col_sums = [sum(cell_values[r][c] for r in range(rows)) for c in range(cols)]
        marginal_bars = VGroup()

        for c in range(cols):
            column_cells = VGroup(*[grid_cells[r * cols + c] for r in range(rows)])
            highlight_rects = VGroup(*[
                grid_cells[r * cols + c][0].copy().set_stroke(color=YELLOW, width=3)
                for r in range(rows)
            ])
            self.play(Create(highlight_rects), run_time=0.4)

            bar = Rectangle(
                width=cell_size * 0.8, height=col_sums[c] * 3.0,
                fill_color=GREEN, fill_opacity=0.85, stroke_width=0,
            )
            bar_x = grid_cells[c].get_center()[0]
            bar.move_to([bar_x, grid.get_bottom()[1] - 0.6 - col_sums[c] * 1.5, 0], aligned_edge=DOWN)

            self.play(
                *[Transform(hr, bar.copy()) for hr in highlight_rects],
                run_time=0.6,
            )
            self.remove(*highlight_rects)
            self.add(bar)
            marginal_bars.add(bar)
            self.wait(0.2)

        marginal_label = MathTex("P(\\mathrm{x})", font_size=26, color=GREEN)
        marginal_label.next_to(marginal_bars, DOWN, buff=0.3)
        show(marginal_label, 0.6)

        sum_formula = MathTex(
            r"P(\mathrm{x}=x) = \sum_{y} P(\mathrm{x}=x,\ \mathrm{y}=y)",
            font_size=26, color=WHITE,
        )
        sum_formula.next_to(grid, RIGHT, buff=1.2).align_to(grid, UP)
        show(sum_formula, 1.0)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt("Sum out what you don't need.\nWhat remains is the marginal.", 32, WHITE, BOLD)
        final.move_to(ORIGIN + UP * 0.25)

        self.play(Write(final), run_time=1.0)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Figure306().render()
