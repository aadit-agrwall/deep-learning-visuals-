from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, fit_in_frame
from common.animations import build_flow_sequence, staggered_fade_in, emphasize_then_settle, cross_dissolve
from common.components import titled_box


class Figure303(Scene):

    def construct(self):

        # ============================================================
        # THEME (matches figure301/302 exactly)
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
            return Text(text, font="DejaVu Sans", font_size=size, color=color, weight=weight)

        def show(obj, time=0.7):
            self.play(Write(obj), run_time=time)

        def clear_scene():
            if self.mobjects:
                self.play(*[FadeOut(obj) for obj in list(self.mobjects)], run_time=0.5)
            self.wait(0.25)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 40, WHITE, BOLD)
        section = txt("3.2  Why Do We Need Probability?", 30, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.45)
        show(heading, 0.75)
        show(section, 0.55)
        self.wait(1.2)
        clear_scene()

        # ============================================================
        # SCENE 2 — DISCRETIZATION CREATES UNCERTAINTY
        # ============================================================

        title = txt("Discretization creates uncertainty", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        statement = txt(
            "A discrete cell hides exactly where inside it an object sits.",
            24, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.5)
        show(statement, 0.65)

        # grid of cells, one cell highlighted, a dot with a fuzzy "could be anywhere" halo
        grid = VGroup(*[
            Square(side_length=0.9, stroke_color=MUTED, stroke_width=1.5)
            for _ in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0.08)
        grid.move_to(DOWN * 0.6)

        target_cell = grid[4]
        highlight = target_cell.copy().set_stroke(color=YELLOW, width=3)

        uncertainty_dot = Dot(target_cell.get_center(), radius=0.08, color=RED)
        halo = Circle(radius=0.35, stroke_color=RED, stroke_width=1.5, stroke_opacity=0.5)
        halo.move_to(target_cell.get_center())

        self.play(FadeIn(grid, lag_ratio=0.08), run_time=1.0)
        self.play(Create(highlight), run_time=0.5)
        self.play(FadeIn(uncertainty_dot), Create(halo), run_time=0.6)

        caption = txt("observed cell  →  true position unknown", 20, MUTED)
        caption.next_to(grid, DOWN, buff=0.4)
        show(caption, 0.6)

        self.wait(1.2)
        clear_scene()

        # ============================================================
        # SCENE 3 — SIMPLE RULE vs EXHAUSTIVE RULE (flow-built)
        # ============================================================

        title = txt("A modeling trade-off", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        statement = txt(
            "A simple, uncertain rule often beats a complex, certain one.",
            24, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.5)
        show(statement, 0.65)

        simple_box = titled_box(
            "Simple rule",
            txt('"Most birds fly"', 20, WHITE),
            chapter="chapter03", width=4.2, height=1.8,
        )
        complex_box = titled_box(
            "Exhaustive rule",
            txt("list every exception:\nyoung, injured, ostrich...", 17, WHITE),
            chapter="chapter03", width=4.6, height=1.8,
        )

        row = flow_row([simple_box, complex_box], buff=1.0)
        row.move_to(DOWN * 0.5)
        fit_in_frame(row, margin=1.0)

        arrow = smart_arrow(simple_box, complex_box, chapter="chapter03", color=YELLOW)

        build_flow_sequence(self, [simple_box, complex_box], [arrow], box_run_time=0.6, arrow_run_time=0.5, stagger=0.1)

        verdict = txt("cheap + broadly useful   >   expensive + still brittle", 19, GREEN)
        verdict.next_to(row, DOWN, buff=0.5)
        show(verdict, 0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 4 — FREQUENTIST vs BAYESIAN (side-by-side, staggered)
        # ============================================================

        title = txt("Two ways to interpret probability", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.6)

        freq_box = titled_box(
            "Frequentist",
            txt("drawing a poker hand,\nrepeated infinitely often", 18, WHITE),
            chapter="chapter03", width=4.4, height=1.9,
        )
        bayes_box = titled_box(
            "Bayesian",
            txt("40% chance a patient\nhas the flu — one-off belief", 18, WHITE),
            chapter="chapter03", width=4.4, height=1.9,
        )

        pair = flow_row([freq_box, bayes_box], buff=1.2)
        pair.move_to(DOWN * 0.6)
        fit_in_frame(pair, margin=1.0)

        staggered_fade_in(self, [freq_box, bayes_box], run_time=1.2, lag_ratio=0.35)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 5 — SAME FORMULAS, DIFFERENT MEANING
        # ============================================================

        title = txt("Same formulas, different meaning", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.8)
        show(title, 0.6)

        poker = titled_box("Poker odds", txt("P(win | cards)", 20, WHITE), chapter="chapter03", width=3.6, height=1.4)
        formula = titled_box("Shared math", txt("same probability rules", 18, WHITE), chapter="chapter03", width=3.6, height=1.4)
        diagnosis = titled_box("Diagnosis", txt("P(flu | symptoms)", 20, WHITE), chapter="chapter03", width=3.6, height=1.4)

        row = flow_row([poker, formula, diagnosis], buff=0.8)
        row.move_to(DOWN * 0.5)
        fit_in_frame(row, margin=0.8)

        arrows = connector_chain([poker, formula, diagnosis], chapter="chapter03", color=GREEN)
        build_flow_sequence(self, [poker, formula, diagnosis], list(arrows), box_run_time=0.5, arrow_run_time=0.45, stagger=0.1)

        emphasize_then_settle(self, formula, chapter="chapter03")

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt("Uncertainty needs a language.\nProbability is that language.", 34, WHITE, BOLD)
        final.move_to(ORIGIN + UP * 0.25)

        self.play(Write(final), run_time=0.9)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.45)

        self.wait(2)


if __name__ == "__main__":
    Figure303().render()
