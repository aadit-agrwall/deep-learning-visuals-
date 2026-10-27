import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page_73(Scene):

    def construct(self):

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"
        ORANGE = "#FFA94D"
        PURPLE = "#C58CFF"

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
        section = txt("Figure 3.5  &  Cross-Entropy", 27, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — FIGURE 3.5: ENTROPY OF A BINARY VARIABLE
        # ============================================================

        title = txt("Figure 3.5: Entropy of a binary random variable", 27, WHITE, BOLD)
        title.to_edge(UP, buff=0.65)
        show(title, 0.7)

        axes = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 0.7, 0.1],
            x_length=8, y_length=4.2,
            axis_config={"color": WHITE, "stroke_width": 2.2, "include_tip": False},
        )
        axes.move_to(DOWN * 0.4)

        p_label = txt("p", 20, MUTED)
        p_label.next_to(axes.x_axis, DOWN, buff=0.25)
        h_label = txt("H(x) in nats", 18, MUTED)
        h_label.rotate(PI / 2)
        h_label.next_to(axes.y_axis, LEFT, buff=0.3)

        self.play(Create(axes), FadeIn(p_label), FadeIn(h_label), run_time=0.9)

        def entropy(p):
            if p <= 1e-6 or p >= 1 - 1e-6:
                return 0
            return -(p * np.log(p) + (1 - p) * np.log(1 - p))

        curve = axes.plot(entropy, x_range=[0.001, 0.999], color=CYAN, stroke_width=4)
        self.play(Create(curve), run_time=1.3)

        peak_dot = Dot(axes.c2p(0.5, entropy(0.5)), color=YELLOW, radius=0.09)
        peak_label = MathTex(r"p=0.5 \Rightarrow \text{max entropy}", font_size=22, color=YELLOW)
        peak_label.next_to(peak_dot, UP, buff=0.3)

        left_dot = Dot(axes.c2p(0.02, entropy(0.02)), color=RED, radius=0.08)
        right_dot = Dot(axes.c2p(0.98, entropy(0.98)), color=RED, radius=0.08)
        edge_note = txt("p → 0 or 1: nearly deterministic, entropy → 0", 16, RED)
        edge_note.next_to(axes, DOWN, buff=0.35)

        self.play(FadeIn(peak_dot), Write(peak_label), run_time=0.8)
        self.play(FadeIn(left_dot), FadeIn(right_dot), run_time=0.5)
        fit_in_frame(edge_note, margin=1.0)
        show(edge_note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — ENTROPY FORMULA FOR BINARY VARIABLE
        # ============================================================

        title = txt("Closed form for the binary case", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(
            r"H(x) = (p - 1)\log(1 - p) - p \log p",
            font_size=32, color=GREEN,
        )
        formula.next_to(title, DOWN, buff=0.7)
        show(formula, 1.1)

        box1 = titled_box(
            "p near 0", txt("almost always 0\nlow entropy", 16, WHITE),
            chapter="chapter03", width=4.4, height=1.7,
        )
        box2 = titled_box(
            "p = 0.5", txt("maximally uncertain\nhighest entropy", 16, WHITE),
            chapter="chapter03", width=4.4, height=1.7,
        )
        box3 = titled_box(
            "p near 1", txt("almost always 1\nlow entropy", 16, WHITE),
            chapter="chapter03", width=4.4, height=1.7,
        )

        for b, c in zip([box1, box2, box3], [RED, YELLOW, ORANGE]):
            b[0].set_stroke(color=c, width=3)

        row = flow_row([box1, box2, box3], buff=0.4)
        row.next_to(formula, DOWN, buff=0.6)
        fit_in_frame(row, margin=0.7)

        staggered_fade_in(self, [box1, box2, box3], run_time=1.3, lag_ratio=0.3)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — CROSS-ENTROPY DEFINITION
        # ============================================================

        title = txt("Cross-entropy", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        relation = MathTex(
            r"H(P, Q) = H(P) + D_{\mathrm{KL}}(P\|Q)",
            font_size=32, color=PURPLE,
        )
        relation.next_to(title, DOWN, buff=0.7)
        show(relation, 1.0)

        formula2 = MathTex(
            r"H(P, Q) = -\mathbb{E}_{\mathrm{x}\sim P}\log Q(x)",
            font_size=30, color=YELLOW,
        )
        formula2.next_to(relation, DOWN, buff=0.5)
        show(formula2, 0.9)

        eq_num = txt("(3.51)", 18, MUTED)
        eq_num.next_to(formula2, DOWN, buff=0.25)
        show(eq_num, 0.4)

        note = txt("like KL divergence, but missing the H(P) term", 18, CYAN)
        note.next_to(eq_num, DOWN, buff=0.5)
        fit_in_frame(note, margin=1.0)
        show(note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — MINIMIZING CROSS-ENTROPY vs KL
        # ============================================================

        title = txt("Minimizing cross-entropy ≡ minimizing KL", 27, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        left_box = titled_box(
            "H(P, Q)", txt("depends on Q\nH(P) is a constant w.r.t. Q", 16, WHITE),
            chapter="chapter03", width=5.4, height=1.9,
        )
        left_box[0].set_stroke(color=GREEN, width=3)

        right_box = titled_box(
            "D_KL(P‖Q)", txt("= H(P, Q) − H(P)\nsame minimizer over Q", 16, WHITE),
            chapter="chapter03", width=5.4, height=1.9,
        )
        right_box[0].set_stroke(color=PURPLE, width=3)

        row2 = flow_row([left_box, right_box], buff=0.7)
        row2.move_to(DOWN * 0.2)
        fit_in_frame(row2, margin=0.8)

        arrow = smart_arrow(left_box, right_box, color=CYAN)

        staggered_fade_in(self, [left_box, right_box], run_time=1.2, lag_ratio=0.4)
        self.play(Create(arrow), run_time=0.6)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — CONVENTION: 0 log 0 = 0
        # ============================================================

        title = txt("A useful convention", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula3 = MathTex(r"0 \log 0", font_size=34, color=RED)
        arrow_eq = MathTex(r"\overset{\text{by convention}}{=}", font_size=24, color=MUTED)
        formula4 = MathTex(r"\lim_{x \to 0} x \log x = 0", font_size=34, color=GREEN)

        group = VGroup(formula3, arrow_eq, formula4).arrange(RIGHT, buff=0.5)
        group.next_to(title, DOWN, buff=0.8)
        fit_in_frame(group, margin=0.8)

        show(formula3, 0.8)
        show(arrow_eq, 0.6)
        show(formula4, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 7 — SECTION 3.14 INTRO: STRUCTURED PROBABILISTIC MODELS
        # ============================================================

        title = txt("3.14  Structured Probabilistic Models", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        problem_box = titled_box(
            "The problem",
            txt("a single function over ALL variables\nis inefficient — computationally\nand statistically", 16, WHITE),
            chapter="chapter03", width=8.5, height=2.3,
        )
        problem_box[0].set_stroke(color=RED, width=3)
        problem_box.next_to(title, DOWN, buff=0.7)
        fit_in_frame(problem_box, margin=0.8)
        show(problem_box, 1.0)

        insight = txt("many ML distributions involve direct interactions\nbetween only a few variables at a time", 18, CYAN)
        insight.next_to(problem_box, DOWN, buff=0.55)
        fit_in_frame(insight, margin=1.0)
        show(insight, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Entropy peaks at maximum uncertainty.\nCross-entropy and KL share the same minimizer.",
            25, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)
        fit_in_frame(final, margin=1.0)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page_73().render()
