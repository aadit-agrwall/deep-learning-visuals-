import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page_72(Scene):

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
        section = txt("3.13  Shannon Entropy & KL Divergence", 27, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — CONTINUOUS CASE, UNIT DENSITY
        # ============================================================

        title = txt("Continuous x: some properties are lost", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "An event with unit density still has zero information,\neven though it isn't guaranteed to occur.",
            20, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.6)
        fit_in_frame(statement, margin=1.0)
        show(statement, 1.0)

        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 1.5, 0.5],
            x_length=7, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.next_to(statement, DOWN, buff=0.5)

        density_line = axes.plot(lambda x: 1, x_range=[0, 4], color=CYAN, stroke_width=3.5)
        dot = Dot(axes.c2p(2, 1), color=YELLOW, radius=0.08)
        dot_label = MathTex(r"p(x)=1 \Rightarrow I(x) = -\log 1 = 0", font_size=22, color=YELLOW)
        dot_label.next_to(axes, DOWN, buff=0.35)

        self.play(Create(axes), run_time=0.6)
        self.play(Create(density_line), FadeIn(dot), run_time=0.9)
        fit_in_frame(dot_label, margin=1.0)
        show(dot_label, 0.8)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 3 — SHANNON ENTROPY DEFINITION
        # ============================================================

        title = txt("Shannon entropy", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(
            r"H(\mathrm{x}) = \mathbb{E}_{\mathrm{x}\sim P}[I(x)] = -\mathbb{E}_{\mathrm{x}\sim P}[\log P(x)]",
            font_size=30, color=YELLOW,
        )
        formula.next_to(title, DOWN, buff=0.6)
        fit_in_frame(formula, margin=0.8)
        show(formula, 1.1)

        eq_num = txt("(3.49)", 18, MUTED)
        eq_num.next_to(formula, DOWN, buff=0.25)
        show(eq_num, 0.4)

        meaning = txt(
            "expected information from an event drawn from P\n(a lower bound on average bits needed to encode P)",
            18, MUTED,
        )
        meaning.next_to(eq_num, DOWN, buff=0.5)
        fit_in_frame(meaning, margin=1.0)
        show(meaning, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — LOW ENTROPY VS HIGH ENTROPY DISTRIBUTIONS
        # ============================================================

        title = txt("Deterministic vs. uniform: low vs. high entropy", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        cats = ["A", "B", "C", "D"]

        def bar_chart(values, color, label_text):
            bars = VGroup()
            axes_b = Axes(
                x_range=[0, 4, 1], y_range=[0, 1, 0.5],
                x_length=3.2, y_length=2.4,
                axis_config={"color": MUTED, "stroke_width": 1.5, "include_tip": False},
            )
            for i, v in enumerate(values):
                bar = Rectangle(
                    width=0.5, height=v * 2.4, color=color, fill_color=color,
                    fill_opacity=0.85, stroke_width=1,
                )
                bar.move_to(axes_b.c2p(i + 0.5, 0), aligned_edge=DOWN)
                bars.add(bar)
            group = VGroup(axes_b, bars)
            lbl = txt(label_text, 17, WHITE)
            lbl.next_to(group, DOWN, buff=0.3)
            return VGroup(group, lbl)

        low_entropy = bar_chart([0.95, 0.02, 0.02, 0.01], RED, "Nearly deterministic\n→ low entropy")
        high_entropy = bar_chart([0.25, 0.25, 0.25, 0.25], GREEN, "Nearly uniform\n→ high entropy")

        row = flow_row([low_entropy, high_entropy], buff=1.2)
        row.move_to(DOWN * 0.2)
        fit_in_frame(row, margin=0.8)

        staggered_fade_in(self, [low_entropy, high_entropy], run_time=1.3, lag_ratio=0.4)

        note = txt("see Figure 3.5  ·  continuous case: differential entropy", 16, MUTED)
        note.next_to(row, DOWN, buff=0.45)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — KL DIVERGENCE DEFINITION
        # ============================================================

        title = txt("Kullback-Leibler (KL) divergence", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula2 = MathTex(
            r"D_{\mathrm{KL}}(P\|Q) = \mathbb{E}_{\mathrm{x}\sim P}\left[\log \frac{P(x)}{Q(x)}\right] "
            r"= \mathbb{E}_{\mathrm{x}\sim P}[\log P(x) - \log Q(x)]",
            font_size=26, color=YELLOW,
        )
        formula2.next_to(title, DOWN, buff=0.6)
        fit_in_frame(formula2, margin=0.7)
        show(formula2, 1.2)

        eq_num2 = txt("(3.50)", 18, MUTED)
        eq_num2.next_to(formula2, DOWN, buff=0.3)
        show(eq_num2, 0.4)

        meaning2 = txt(
            "extra information needed to send symbols from P,\nusing a code optimized for Q instead",
            18, MUTED,
        )
        meaning2.next_to(eq_num2, DOWN, buff=0.5)
        fit_in_frame(meaning2, margin=1.0)
        show(meaning2, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — PROPERTIES OF KL DIVERGENCE
        # ============================================================

        title = txt("Key properties of KL divergence", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        prop1 = titled_box(
            "Non-negative", txt("D_KL(P‖Q) ≥ 0 always", 16, WHITE),
            chapter="chapter03", width=4.6, height=1.6,
        )
        prop2 = titled_box(
            "Zero iff equal", txt("D_KL(P‖Q) = 0  ⇔  P = Q\n(a.e. if continuous)", 15, WHITE),
            chapter="chapter03", width=4.6, height=1.6,
        )
        prop3 = titled_box(
            "Not symmetric", txt("D_KL(P‖Q) ≠ D_KL(Q‖P)\nnot a true distance", 15, WHITE),
            chapter="chapter03", width=4.6, height=1.6,
        )

        row2 = flow_row([prop1, prop2, prop3], buff=0.5)
        row2.move_to(DOWN * 0.3)
        fit_in_frame(row2, margin=0.7)

        staggered_fade_in(self, [prop1, prop2, prop3], run_time=1.4, lag_ratio=0.3)

        note2 = txt("choosing D_KL(P‖Q) vs. D_KL(Q‖P) matters — see Figure 3.6", 17, CYAN)
        note2.next_to(row2, DOWN, buff=0.5)
        fit_in_frame(note2, margin=1.0)
        show(note2, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Entropy measures uncertainty in a distribution.\nKL divergence measures the gap between two.",
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
    Page_72().render()
