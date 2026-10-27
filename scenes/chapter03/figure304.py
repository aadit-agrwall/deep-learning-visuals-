from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, fit_in_frame
from common.animations import build_flow_sequence, staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Figure304(Scene):

    def construct(self):

        # ============================================================
        # THEME (matches figure301/302/303)
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
        section = txt("3.2 – 3.3  Random Variables & Distributions", 28, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.45)
        show(heading, 0.75)
        show(section, 0.55)
        self.wait(1.2)
        clear_scene()

        # ============================================================
        # SCENE 2 — PROBABILITY AS EXTENSION OF LOGIC
        # ============================================================

        title = txt("Probability extends logic", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        logic_box = titled_box(
            "Logic",
            txt("true or false,\ngiven other propositions", 19, WHITE),
            chapter="chapter03", width=4.4, height=1.9,
        )
        prob_box = titled_box(
            "Probability",
            txt("likelihood of true,\ngiven other likelihoods", 19, WHITE),
            chapter="chapter03", width=4.4, height=1.9,
        )

        row = flow_row([logic_box, prob_box], buff=1.2)
        row.move_to(DOWN * 0.5)
        fit_in_frame(row, margin=1.0)

        arrow = smart_arrow(logic_box, prob_box, chapter="chapter03", color=YELLOW)
        build_flow_sequence(self, [logic_box, prob_box], [arrow], box_run_time=0.6, arrow_run_time=0.6, stagger=0.15)

        caption = txt('"extends" = handles uncertainty logic cannot', 19, MUTED)
        caption.next_to(row, DOWN, buff=0.5)
        show(caption, 0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 3 — RANDOM VARIABLES
        # ============================================================

        title = txt("What is a random variable?", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        statement = txt(
            "A description of possible states — paired with a distribution\nthat says how likely each state is.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.5)
        show(statement, 0.8)

        var_label = MathTex("x", color=CYAN, font_size=48)
        var_label.move_to(LEFT * 4.3 + DOWN * 0.6)

        state_dots = VGroup()
        state_labels = VGroup()
        positions = [DOWN * 0.6 + RIGHT * i * 1.4 for i in range(4)]
        values = ["x_1", "x_2", "x_3", "x_4"]

        for pos, val in zip(positions, values):
            dot = Dot(pos + RIGHT * 1.5, radius=0.09, color=YELLOW)
            label = MathTex(val, font_size=26, color=WHITE)
            label.next_to(dot, DOWN, buff=0.2)
            state_dots.add(dot)
            state_labels.add(label)

        arrow_to_states = Arrow(
            var_label.get_right(), state_dots[0].get_left() + LEFT * 0.3,
            buff=0.15, color=CYAN, stroke_width=3,
        )

        self.play(FadeIn(var_label), run_time=0.5)
        self.play(GrowArrow(arrow_to_states), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(d) for d in state_dots], lag_ratio=0.2),
            LaggedStart(*[FadeIn(l) for l in state_labels], lag_ratio=0.2),
            run_time=1.2,
        )

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 4 — DISCRETE vs CONTINUOUS
        # ============================================================

        title = txt("Discrete vs. Continuous", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        # --- discrete: separated dots ---
        discrete_title = txt("Discrete", 26, CYAN, BOLD)
        discrete_title.move_to(LEFT * 3.3 + UP * 1.1)

        discrete_dots = VGroup(*[
            Dot(LEFT * 3.3 + DOWN * 0.6 + RIGHT * (i - 1.5) * 0.5, radius=0.09, color=CYAN)
            for i in range(4)
        ])
        discrete_caption = txt("countable states", 18, MUTED)
        discrete_caption.next_to(discrete_dots, DOWN, buff=0.4)

        # --- continuous: a smooth line ---
        continuous_title = txt("Continuous", 26, GREEN, BOLD)
        continuous_title.move_to(RIGHT * 3.3 + UP * 1.1)

        continuous_line = Line(
            RIGHT * 3.3 + LEFT * 1.3 + DOWN * 0.6,
            RIGHT * 3.3 + RIGHT * 1.3 + DOWN * 0.6,
            color=GREEN, stroke_width=4,
        )
        continuous_caption = txt("any real value", 18, MUTED)
        continuous_caption.next_to(continuous_line, DOWN, buff=0.4)

        self.play(FadeIn(discrete_title), FadeIn(continuous_title), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(d) for d in discrete_dots], lag_ratio=0.15),
            Create(continuous_line),
            run_time=1.0,
        )
        self.play(FadeIn(discrete_caption), FadeIn(continuous_caption), run_time=0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 5 — PROBABILITY DISTRIBUTION
        # ============================================================

        title = txt("Probability distribution", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        statement = txt(
            "Describes how likely each possible state is.",
            24, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.5)
        show(statement, 0.65)

        # simple bar-style distribution over 5 discrete states
        bar_heights = [0.5, 1.3, 2.0, 1.0, 0.4]
        bars = VGroup()
        bar_labels = VGroup()
        for i, h in enumerate(bar_heights):
            bar = Rectangle(width=0.7, height=h, fill_color=CYAN, fill_opacity=0.85, stroke_width=0)
            bar.move_to(LEFT * 2.8 + RIGHT * i * 1.1 + DOWN * (1.6 - h / 2))
            label = MathTex(f"x_{i+1}", font_size=20, color=MUTED)
            label.next_to(bar, DOWN, buff=0.15)
            bars.add(bar)
            bar_labels.add(label)

        baseline = Line(
            bars[0].get_corner(DL) + LEFT * 0.3,
            bars[-1].get_corner(DR) + RIGHT * 0.3,
            color=MUTED, stroke_width=1.5,
        )

        self.play(Create(baseline), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(bar, shift=UP * 0.3) for bar in bars], lag_ratio=0.15),
            run_time=1.2,
        )
        self.play(FadeIn(bar_labels, lag_ratio=0.1), run_time=0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 6 — PROBABILITY MASS FUNCTION (PMF)
        # ============================================================

        title = txt("Probability Mass Function (PMF)", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.75)
        show(title, 0.65)

        statement = txt(
            "For discrete variables: capital  P  gives the probability of each state.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.5)
        show(statement, 0.75)

        pmf_box = titled_box(
            "PMF",
            MathTex("P(\\mathrm{x} = x_i)", font_size=32, color=WHITE),
            chapter="chapter03", width=4.5, height=1.8,
        )
        pmf_box.move_to(DOWN * 0.4)

        self.play(GrowFromCenter(pmf_box), run_time=0.8)
        emphasize_then_settle(self, pmf_box, chapter="chapter03")

        note = txt("one PMF per random variable — inferred from context", 18, MUTED)
        note.next_to(pmf_box, DOWN, buff=0.5)
        show(note, 0.6)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt("A variable describes what can happen.\nA distribution says how likely.", 32, WHITE, BOLD)
        final.move_to(ORIGIN + UP * 0.25)

        self.play(Write(final), run_time=0.9)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.45)

        self.wait(2)


if __name__ == "__main__":
    Figure304().render()
