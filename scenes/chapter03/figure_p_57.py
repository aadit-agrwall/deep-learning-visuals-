import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class FigureP56(Scene):

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
        section = txt("3.4 – 3.6  Marginal, Conditional & Chain Rule", 24, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — WHERE "MARGINAL" COMES FROM
        # ============================================================

        title = txt('Why "marginal"?', 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Sum across a row, then write the result in the margin of the page.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.8)
        self.wait(0.4)

        rows, cols = 3, 3
        cell_size = 0.85
        cell_values = [[0.05, 0.10, 0.05], [0.08, 0.20, 0.07], [0.10, 0.25, 0.10]]

        grid_cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                cell = Square(side_length=cell_size, stroke_color=MUTED, stroke_width=1.5)
                val_text = Text(f"{cell_values[r][c]:.2f}", font="DejaVu Sans", font_size=15, color=WHITE)
                val_text.move_to(cell.get_center())
                grid_cells.add(VGroup(cell, val_text))

        grid = VGroup(*grid_cells).arrange_in_grid(rows=rows, cols=cols, buff=0)
        grid.move_to(LEFT * 1.8 + DOWN * 0.2)

        x_label = txt("x  →", 20, CYAN)
        x_label.next_to(grid, DOWN, buff=0.25)
        y_label = txt("y ↓", 20, YELLOW)
        y_label.next_to(grid, LEFT, buff=0.25)

        self.play(FadeIn(grid, lag_ratio=0.05), FadeIn(x_label), FadeIn(y_label), run_time=1.0)
        self.wait(0.4)

        # sum row by row, "writing" each result into the margin on the right
        margin_x = grid.get_right()[0] + 1.6
        margin_values = []
        for r in range(rows):
            row_cells = VGroup(*[grid_cells[r * cols + c][0] for c in range(cols)])
            highlight = row_cells.copy().set_stroke(color=YELLOW, width=3)
            self.play(Create(highlight), run_time=0.35)

            row_sum = sum(cell_values[r])
            margin_values.append(row_sum)

            margin_text = Text(f"{row_sum:.2f}", font="DejaVu Sans", font_size=20, color=GREEN)
            margin_text.move_to([margin_x, row_cells.get_center()[1], 0])

            self.play(
                TransformFromCopy(highlight, margin_text),
                run_time=0.6,
            )
            self.remove(highlight)
            self.wait(0.15)

        margin_bracket = Line(
            [margin_x - 0.5, grid.get_top()[1], 0],
            [margin_x - 0.5, grid.get_bottom()[1], 0],
            color=GREEN, stroke_width=2,
        )
        self.play(Create(margin_bracket), run_time=0.5)

        margin_label = MathTex("P(\\mathrm{y})", font_size=24, color=GREEN)
        margin_label.next_to(margin_bracket, RIGHT, buff=0.3).move_to([margin_x + 0.9, grid.get_center()[1], 0])
        show(margin_label, 0.5)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 3 — CONTINUOUS VERSION: INTEGRATION
        # ============================================================

        title = txt("For continuous variables: integrate", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(r"p(x) = \int p(x, y)\, dy", font_size=36, color=CYAN)
        formula.move_to(UP * 0.3)
        show(formula, 1.0)

        subtext = txt("same idea as summing — just over a continuum", 20, MUTED)
        subtext.next_to(formula, DOWN, buff=0.6)
        show(subtext, 0.6)

        emphasize_then_settle(self, formula, chapter="chapter03")

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 4 — CONDITIONAL PROBABILITY
        # ============================================================

        title = txt("Conditional probability", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "The probability of one event, GIVEN another has happened.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.75)

        circle_x = Circle(radius=1.3, stroke_color=CYAN, stroke_width=2.5)
        circle_x.move_to(LEFT * 1.0 + DOWN * 0.5)
        circle_y = Circle(radius=1.3, stroke_color=YELLOW, stroke_width=2.5)
        circle_y.move_to(RIGHT * 1.0 + DOWN * 0.5)

        label_x = MathTex("\\mathrm{x}=x", font_size=24, color=CYAN)
        label_x.move_to(circle_x.get_center() + LEFT * 0.7)
        label_y = MathTex("\\mathrm{y}=y", font_size=24, color=YELLOW)
        label_y.move_to(circle_y.get_center() + RIGHT * 0.7)

        overlap_label = txt("both\ntrue", 16, WHITE)
        overlap_label.move_to((circle_x.get_center() + circle_y.get_center()) / 2)

        self.play(Create(circle_x), Create(circle_y), run_time=0.9)
        self.play(FadeIn(label_x), FadeIn(label_y), FadeIn(overlap_label), run_time=0.6)

        formula2 = MathTex(
            r"P(\mathrm{y}=y \mid \mathrm{x}=x) = \frac{P(\mathrm{y}=y,\ \mathrm{x}=x)}{P(\mathrm{x}=x)}",
            font_size=28, color=WHITE,
        )
        formula2.next_to(VGroup(circle_x, circle_y), DOWN, buff=0.7)
        show(formula2, 1.0)

        caveat = txt("defined only when P(x = x) > 0", 18, RED)
        caveat.next_to(formula2, DOWN, buff=0.35)
        show(caveat, 0.6)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — CONDITIONAL ≠ INTERVENTION (the Germany example)
        # ============================================================

        title = txt("Conditioning is not intervening", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        # LEFT: observing (conditional)
        observe_title = txt("Observe", 24, CYAN, BOLD)
        observe_title.move_to(LEFT * 3.2 + UP * 1.2)

        speaker = txt("speaks German", 18, WHITE)
        origin = txt("likely from Germany", 18, GREEN)
        speaker.move_to(LEFT * 3.2 + UP * 0.3)
        origin.move_to(LEFT * 3.2 + DOWN * 0.5)
        observe_arrow = smart_arrow(speaker, origin, chapter="chapter03", color=CYAN)

        # RIGHT: intervening (teaching)
        intervene_title = txt("Intervene", 24, RED, BOLD)
        intervene_title.move_to(RIGHT * 3.2 + UP * 1.2)

        taught = txt("taught German", 18, WHITE)
        unchanged = txt("origin unchanged", 18, RED)
        taught.move_to(RIGHT * 3.2 + UP * 0.3)
        unchanged.move_to(RIGHT * 3.2 + DOWN * 0.5)
        intervene_arrow = smart_arrow(taught, unchanged, chapter="chapter03", color=RED)

        self.play(FadeIn(observe_title), FadeIn(intervene_title), run_time=0.6)
        self.play(FadeIn(speaker), FadeIn(taught), run_time=0.6)
        self.play(GrowArrow(observe_arrow), GrowArrow(intervene_arrow), run_time=0.7)
        self.play(FadeIn(origin), FadeIn(unchanged), run_time=0.6)

        note = txt('changing the action does not rewrite the past ("causal modeling")', 17, MUTED)
        note.next_to(VGroup(observe_title, intervene_title), DOWN, buff=2.6)
        show(note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — CHAIN RULE
        # ============================================================

        title = txt("The chain rule of probability", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Any joint distribution decomposes into a chain of conditionals.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        show(statement, 0.75)

        joint = MathTex(
            r"P(x^{(1)}, \ldots, x^{(n)})", font_size=30, color=WHITE
        )
        joint.move_to(UP * 0.4)
        show(joint, 0.8)

        equals = MathTex("=", font_size=30, color=WHITE)
        equals.next_to(joint, DOWN, buff=0.4)
        self.play(FadeIn(equals), run_time=0.3)

        chain = MathTex(
            r"P(x^{(1)})\, P(x^{(2)} \mid x^{(1)})\, P(x^{(3)} \mid x^{(1)}, x^{(2)}) \cdots",
            font_size=26, color=YELLOW,
        )
        chain.next_to(equals, DOWN, buff=0.4)
        self.play(Write(chain), run_time=1.4)

        # visual chain of boxes to reinforce the sequential dependency
        step_labels = ["x⁽¹⁾", "x⁽²⁾|x⁽¹⁾", "x⁽³⁾|x⁽¹⁾,x⁽²⁾"]
        steps = VGroup(*[
            titled_box(f"step {i+1}", txt(label, 16, WHITE), chapter="chapter03", width=2.6, height=1.2)
            for i, label in enumerate(step_labels)
        ])
        row = flow_row(list(steps), buff=0.7)
        row.next_to(chain, DOWN, buff=0.7)
        fit_in_frame(row, margin=1.0)

        arrows = VGroup(*[
            smart_arrow(steps[i], steps[i + 1], chapter="chapter03", color=GREEN)
            for i in range(len(steps) - 1)
        ])

        self.play(FadeIn(row, lag_ratio=0.2), run_time=1.0)
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Marginal sums away what you ignore.\nConditional narrows to what you know.",
            30, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)

        self.play(Write(final), run_time=1.0)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    FigureP56().render()
