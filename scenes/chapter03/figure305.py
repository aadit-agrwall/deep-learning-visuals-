from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, fit_in_frame
from common.animations import build_flow_sequence, staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Figure305(Scene):

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
            self.wait(0.25)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 40, WHITE, BOLD)
        section = txt("3.3.1  PMF Notation & Axioms", 28, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.45)
        show(heading, 0.75)
        show(section, 0.55)
        self.wait(1.2)
        clear_scene()

        # ============================================================
        # SCENE 2 — READING PMF NOTATION
        # ============================================================

        title = txt("Reading PMF notation", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        notations = VGroup(
            MathTex(r"P(x)", font_size=34, color=CYAN),
            MathTex(r"P(\mathrm{x} = x)", font_size=34, color=YELLOW),
            MathTex(r"\mathrm{x} \sim P(\mathrm{x})", font_size=34, color=GREEN),
        )
        captions = VGroup(
            txt("shorthand", 18, MUTED),
            txt("explicit: which PMF?", 18, MUTED),
            txt('"x follows distribution P"', 18, MUTED),
        )

        pairs = VGroup(*[VGroup(n, c).arrange(DOWN, buff=0.25) for n, c in zip(notations, captions)])
        pairs.arrange(RIGHT, buff=1.1)
        pairs.move_to(DOWN * 0.4)
        fit_in_frame(pairs, margin=1.0)

        staggered_fade_in(self, list(pairs), run_time=1.3, lag_ratio=0.3)

        certainty_note = txt("P = 1  →  certain      P = 0  →  impossible", 20, WHITE)
        certainty_note.next_to(pairs, DOWN, buff=0.6)
        show(certainty_note, 0.7)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 3 — JOINT PROBABILITY DISTRIBUTION
        # ============================================================

        title = txt("Joint probability distribution", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        statement = txt(
            "A PMF can act on several variables at once.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.5)
        show(statement, 0.65)

        x_dot = Dot(LEFT * 3.0 + DOWN * 0.5, radius=0.09, color=CYAN)
        x_label = MathTex("\\mathrm{x}=x", font_size=26, color=CYAN)
        x_label.next_to(x_dot, DOWN, buff=0.25)

        y_dot = Dot(RIGHT * 3.0 + DOWN * 0.5, radius=0.09, color=YELLOW)
        y_label = MathTex("\\mathrm{y}=y", font_size=26, color=YELLOW)
        y_label.next_to(y_dot, DOWN, buff=0.25)

        joint_box = titled_box(
            "Joint",
            MathTex("P(x, y)", font_size=30, color=WHITE),
            chapter="chapter03", width=3.0, height=1.5,
        )
        joint_box.move_to(UP * 0.2)

        arrow_x = smart_arrow(x_dot, joint_box, chapter="chapter03", color=CYAN)
        arrow_y = smart_arrow(y_dot, joint_box, chapter="chapter03", color=YELLOW)

        self.play(FadeIn(x_dot), FadeIn(x_label), FadeIn(y_dot), FadeIn(y_label), run_time=0.7)
        self.play(GrowFromCenter(joint_box), run_time=0.6)
        self.play(GrowArrow(arrow_x), GrowArrow(arrow_y), run_time=0.7)

        full_notation = MathTex(
            "P(\\mathrm{x}=x,\\ \\mathrm{y}=y)", font_size=24, color=GREEN
        )
        full_notation.next_to(joint_box, DOWN, buff=0.6)
        show(full_notation, 0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 4 — THREE PMF AXIOMS
        # ============================================================

        title = txt("Three rules every PMF must obey", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        rule1 = titled_box(
            "1. Domain",
            txt("covers every possible\nstate of x", 17, WHITE),
            chapter="chapter03", width=3.6, height=1.7,
        )
        rule2 = titled_box(
            "2. Bounded",
            MathTex("0 \\le P(x) \\le 1", font_size=24, color=WHITE),
            chapter="chapter03", width=3.6, height=1.7,
        )
        rule3 = titled_box(
            "3. Normalized",
            MathTex(r"\sum_{x} P(x) = 1", font_size=24, color=WHITE),
            chapter="chapter03", width=3.6, height=1.7,
        )

        rules = flow_row([rule1, rule2, rule3], buff=0.6)
        rules.move_to(DOWN * 0.4)
        fit_in_frame(rules, margin=0.7)

        staggered_fade_in(self, [rule1, rule2, rule3], run_time=1.4, lag_ratio=0.3)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — UNIFORM DISTRIBUTION EXAMPLE
        # ============================================================

        title = txt("Example: the uniform distribution", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        statement = txt(
            "k states, each equally likely.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.5)
        show(statement, 0.6)

        formula = MathTex(
            r"P(\mathrm{x} = x_i) = \frac{1}{k}", font_size=36, color=YELLOW
        )
        formula.next_to(statement, DOWN, buff=0.5)
        show(formula, 0.8)

        # equal-height bars showing uniformity
        k = 5
        bars = VGroup()
        for i in range(k):
            bar = Rectangle(width=0.7, height=1.0, fill_color=CYAN, fill_opacity=0.85, stroke_width=0)
            bar.move_to(LEFT * 2.8 + RIGHT * i * 1.4 + DOWN * 1.8)
            bars.add(bar)
        bars.move_to(DOWN * 1.6)

        baseline = Line(
            bars[0].get_corner(DL) + LEFT * 0.3,
            bars[-1].get_corner(DR) + RIGHT * 0.3,
            color=MUTED, stroke_width=1.5,
        )

        self.play(Create(baseline), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(bar, shift=UP * 0.3) for bar in bars], lag_ratio=0.12),
            run_time=1.1,
        )

        check = MathTex(
            r"\sum_i \frac{1}{k} = \frac{k}{k} = 1", font_size=26, color=GREEN
        )
        check.next_to(bars, DOWN, buff=0.5)
        show(check, 0.7)

        emphasize_then_settle(self, check, chapter="chapter03")

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt("Every state gets a share.\nThe shares always add to one.", 32, WHITE, BOLD)
        final.move_to(ORIGIN + UP * 0.25)

        self.play(Write(final), run_time=0.9)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.45)

        self.wait(2)


if __name__ == "__main__":
    Figure305().render()
