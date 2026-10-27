import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page64(Scene):

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
        section = txt("3.9.5 – 3.9.6  Empirical Distribution & Mixtures", 24, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — DIRAC DELTA AS A LIMIT OF NARROWING PEAKS
        # ============================================================

        title = txt("The delta as a limit", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Imagine a family of curves getting taller and narrower, forever.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.85)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 2.2, 1],
            x_length=7, y_length=3.4,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.next_to(statement, DOWN, buff=0.4)

        self.play(Create(axes), run_time=0.7)

        def narrow_gaussian(sigma):
            return axes.plot(
                lambda x: (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(-0.5 * (x / sigma) ** 2),
                x_range=[-3, 3], color=CYAN, stroke_width=3,
            )

        curve = narrow_gaussian(1.0)
        self.play(Create(curve), run_time=0.9)

        for sigma in [0.6, 0.35, 0.18]:
            new_curve = narrow_gaussian(sigma)
            self.play(Transform(curve, new_curve), run_time=0.8)
            self.wait(0.2)

        limit_label = MathTex(r"\sigma \to 0\ \Rightarrow\ \delta(x-\mu)", font_size=26, color=YELLOW)
        limit_label.next_to(axes, DOWN, buff=0.4)
        show(limit_label, 0.7)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 3 — EMPIRICAL DISTRIBUTION (continuous)
        # ============================================================

        title = txt("Empirical distribution: spikes at your data", 27, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(
            r"\hat{p}(x) = \frac{1}{m}\sum_{i=1}^{m}\delta(x - x^{(i)})",
            font_size=28, color=WHITE,
        )
        formula.next_to(title, DOWN, buff=0.4)
        show(formula, 1.0)

        axes2 = Axes(
            x_range=[0, 6, 1], y_range=[0, 1, 1],
            x_length=8, y_length=2.6,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes2.next_to(formula, DOWN, buff=0.4)

        sample_points = [1, 2, 2.5, 4, 5]
        spikes = VGroup()
        for x in sample_points:
            spike = Arrow(axes2.c2p(x, 0), axes2.c2p(x, 0.8), buff=0, color=CYAN, stroke_width=3.5, max_tip_length_to_length_ratio=0.2)
            spikes.add(spike)

        baseline2 = Line(axes2.c2p(0, 0), axes2.c2p(6, 0), color=MUTED, stroke_width=2)

        self.play(Create(axes2), Create(baseline2), run_time=0.7)
        self.play(LaggedStart(*[GrowArrow(s) for s in spikes], lag_ratio=0.2), run_time=1.2)

        weight_label = txt(f"each spike carries mass 1/m = 1/{len(sample_points)}", 18, MUTED)
        weight_label.next_to(axes2, DOWN, buff=0.4)
        show(weight_label, 0.6)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 4 — EMPIRICAL DISTRIBUTION (discrete case is simpler)
        # ============================================================

        title = txt("Discrete case: just count frequencies", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "No Dirac delta needed — this is a multinoulli distribution.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        show(statement, 0.75)

        categories = ["A", "B", "C", "D"]
        counts = [3, 7, 2, 5]
        total = sum(counts)
        freq_bars = VGroup()
        for cat, count in zip(categories, counts):
            h = (count / total) * 2.2
            bar = Rectangle(width=0.8, height=h, fill_color=CYAN, fill_opacity=0.85, stroke_width=0)
            label = txt(f"{cat}\n{count}/{total}", 16, WHITE)
            group = VGroup(bar, label).arrange(DOWN, buff=0.15)
            freq_bars.add(group)

        freq_row = flow_row(list(freq_bars), buff=0.6)
        freq_row.move_to(DOWN * 0.3)
        fit_in_frame(freq_row, margin=1.0)

        baseline3 = Line(freq_row.get_corner(DL) + LEFT * 0.3, freq_row.get_corner(DR) + RIGHT * 0.3, color=MUTED, stroke_width=1.5)

        self.play(Create(baseline3), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in freq_bars], lag_ratio=0.15), run_time=1.1)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — MIXTURE DISTRIBUTIONS
        # ============================================================

        title = txt("Mixture distributions", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "First pick a component (via a multinoulli), then sample from it.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.85)

        formula2 = MathTex(
            r"P(x) = \sum_i P(c{=}i)\,P(x \mid c{=}i)",
            font_size=28, color=WHITE,
        )
        formula2.next_to(statement, DOWN, buff=0.5)
        show(formula2, 1.0)

        # component selector -> one of three component distributions
        selector = titled_box("Select c", MathTex("P(c)", font_size=22, color=YELLOW), chapter="chapter03", width=2.6, height=1.3)
        selector.next_to(formula2, DOWN, buff=0.6).shift(LEFT * 3.5)

        comp1 = titled_box("c=1", MathTex("P(x|c{=}1)", font_size=18, color=CYAN), chapter="chapter03", width=2.4, height=1.2)
        comp2 = titled_box("c=2", MathTex("P(x|c{=}2)", font_size=18, color=GREEN), chapter="chapter03", width=2.4, height=1.2)
        comp3 = titled_box("c=3", MathTex("P(x|c{=}3)", font_size=18, color=RED), chapter="chapter03", width=2.4, height=1.2)

        comps = flow_column([comp1, comp2, comp3], buff=0.35)
        comps.next_to(selector, RIGHT, buff=1.3)
        fit_in_frame(VGroup(selector, comps), margin=0.8)

        arrows = VGroup(*[smart_arrow(selector, c, chapter="chapter03", color=MUTED) for c in [comp1, comp2, comp3]])

        self.play(FadeIn(selector), run_time=0.6)
        self.play(FadeIn(comps, lag_ratio=0.2), run_time=0.9)
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — EMPIRICAL DISTRIBUTION IS A MIXTURE
        # ============================================================

        title = txt("The empirical distribution is a mixture too", 27, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "One Dirac component per training example.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        show(statement, 0.75)

        mixture_box = titled_box("Mixture", MathTex(r"\sum_i P(c{=}i)P(x|c{=}i)", font_size=20, color=WHITE), chapter="chapter03", width=5.0, height=1.5)
        empirical_box = titled_box("Empirical", MathTex(r"\frac{1}{m}\sum_i \delta(x-x^{(i)})", font_size=20, color=CYAN), chapter="chapter03", width=5.0, height=1.5)

        stack = flow_column([mixture_box, empirical_box], buff=0.6)
        stack.move_to(DOWN * 0.3)
        fit_in_frame(stack, margin=0.8)

        self.play(GrowFromCenter(mixture_box), run_time=0.8)
        self.wait(0.3)
        arrow_down = smart_arrow(mixture_box, empirical_box, chapter="chapter03", color=GREEN)
        self.play(GrowArrow(arrow_down), run_time=0.5)
        self.play(GrowFromCenter(empirical_box), run_time=0.8)

        note = txt("each Dirac spike is a component, weighted equally by 1/m", 18, MUTED)
        note.next_to(stack, DOWN, buff=0.5)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Real data rarely fits one clean shape —\nmixtures let simple pieces build complex ones.",
            26, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)
        fit_in_frame(final, margin=1.0)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page64().render()
