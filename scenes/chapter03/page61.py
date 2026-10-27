import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page61(Scene):

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
        section = txt("3.9.2 – 3.9.3  Multinoulli & the Gaussian", 25, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — MULTINOULLI PARAMETERIZATION
        # ============================================================

        title = txt("Parametrizing k states with k-1 numbers", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "The last state's probability is whatever remains.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        show(statement, 0.75)

        # 5 slots: first 4 explicit, 5th shown as "remainder"
        k = 5
        slot_boxes = VGroup()
        labels = [f"p_{i+1}" for i in range(k - 1)] + ["\\;1-\\mathbf{1}^\\top p"]
        colors = [CYAN, CYAN, CYAN, CYAN, YELLOW]
        for label, color in zip(labels, colors):
            box = Rectangle(width=1.3, height=1.0, stroke_color=color, stroke_width=2)
            tex = MathTex(label, font_size=20, color=color)
            tex.move_to(box.get_center())
            slot_boxes.add(VGroup(box, tex))

        slot_row = flow_row(list(slot_boxes), buff=0.35)
        slot_row.move_to(DOWN * 0.2)
        fit_in_frame(slot_row, margin=1.0)

        self.play(FadeIn(slot_row, lag_ratio=0.15), run_time=1.1)

        constraint = MathTex(r"\mathbf{1}^\top p \le 1", font_size=26, color=WHITE)
        constraint.next_to(slot_row, DOWN, buff=0.6)
        show(constraint, 0.8)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 3 — CATEGORIES, NOT NUMBERS
        # ============================================================

        title = txt("States are categories, not numbers", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "State 1 is not \"worth\" 1 — so E[x] and Var(x) rarely apply here.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.85)

        categories = ["🐱", "🐶", "🐦", "🐟"]
        cat_labels = ["cat", "dog", "bird", "fish"]
        cat_boxes = VGroup()
        for name in cat_labels:
            box = titled_box(name, txt("", 10, WHITE), chapter="chapter03", width=1.8, height=1.3)
            cat_boxes.add(box)

        cat_row = flow_row(list(cat_boxes), buff=0.5)
        cat_row.move_to(DOWN * 0.3)
        fit_in_frame(cat_row, margin=1.0)

        self.play(FadeIn(cat_row, lag_ratio=0.2), run_time=1.0)

        no_order = txt("no natural numeric order between them", 19, RED)
        no_order.next_to(cat_row, DOWN, buff=0.6)
        show(no_order, 0.7)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 4 — WHY BERNOULLI/MULTINOULLI SUFFICE (DISCRETE)
        # ============================================================

        title = txt("Why these two suffice for discrete cases", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Not because they're powerful — because the domain is small enough to enumerate.",
            20, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.9)

        discrete_box = titled_box(
            "Discrete",
            txt("finite states\n→ list every probability", 18, WHITE),
            chapter="chapter03", width=4.4, height=1.8,
        )
        continuous_box = titled_box(
            "Continuous",
            txt("uncountably many states\n→ must impose structure", 18, WHITE),
            chapter="chapter03", width=4.4, height=1.8,
        )

        compare_row = flow_row([discrete_box, continuous_box], buff=1.0)
        compare_row.move_to(DOWN * 0.4)
        fit_in_frame(compare_row, margin=1.0)

        staggered_fade_in(self, [discrete_box, continuous_box], run_time=1.2, lag_ratio=0.3)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — THE GAUSSIAN DISTRIBUTION
        # ============================================================

        title = txt("The Gaussian (normal) distribution", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(
            r"\mathcal{N}(x;\mu,\sigma^2) = \sqrt{\frac{1}{2\pi\sigma^2}}\,"
            r"\exp\!\left(-\frac{1}{2\sigma^2}(x-\mu)^2\right)",
            font_size=26, color=WHITE,
        )
        formula.next_to(title, DOWN, buff=0.5)
        fit_in_frame(formula, margin=1.0)
        show(formula, 1.2)

        axes = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.5, 0.25],
            x_length=7, y_length=2.6,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.next_to(formula, DOWN, buff=0.5)

        mu, sigma = 0, 1
        curve = axes.plot(
            lambda x: (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2),
            color=CYAN, stroke_width=3,
        )

        peak_point = axes.c2p(mu, (1 / np.sqrt(2 * np.pi * sigma ** 2)))
        peak_line = DashedLine(axes.c2p(mu, 0), peak_point, color=YELLOW, stroke_width=2)
        mu_label = MathTex(r"\mu", font_size=22, color=YELLOW).next_to(peak_line, DOWN, buff=0.15)

        width_left = axes.c2p(mu - sigma, 0.05)
        width_right = axes.c2p(mu + sigma, 0.05)
        width_line = DoubleArrow(width_left, width_right, buff=0, color=GREEN, stroke_width=2)
        sigma_label = MathTex(r"\sigma", font_size=20, color=GREEN).next_to(width_line, DOWN, buff=0.15)

        self.play(Create(axes), run_time=0.7)
        self.play(Create(curve), run_time=1.0)
        self.play(Create(peak_line), FadeIn(mu_label), run_time=0.6)
        self.play(Create(width_line), FadeIn(sigma_label), run_time=0.6)

        note = txt("μ = peak location = mean      σ = spread = std. deviation", 18, MUTED)
        note.next_to(axes, DOWN, buff=0.5)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — PRECISION PARAMETERIZATION
        # ============================================================

        title = txt("An alternative: precision β", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "β = 1/σ² avoids squaring and inverting σ every evaluation.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.85)

        variance_box = titled_box(
            "Variance form", MathTex(r"\mathcal{N}(x;\mu,\sigma^2)", font_size=24, color=CYAN),
            chapter="chapter03", width=4.0, height=1.4,
        )
        precision_box = titled_box(
            "Precision form", MathTex(r"\mathcal{N}(x;\mu,\beta^{-1})", font_size=24, color=YELLOW),
            chapter="chapter03", width=4.0, height=1.4,
        )

        param_row = flow_row([variance_box, precision_box], buff=1.0)
        param_row.move_to(UP * 0.2)
        fit_in_frame(param_row, margin=1.0)

        arrow = smart_arrow(variance_box, precision_box, chapter="chapter03", color=GREEN)

        self.play(FadeIn(variance_box), run_time=0.6)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(precision_box), run_time=0.6)

        formula2 = MathTex(
            r"\mathcal{N}(x;\mu,\beta^{-1}) = \sqrt{\frac{\beta}{2\pi}}\,"
            r"\exp\!\left(-\frac{1}{2}\beta(x-\mu)^2\right)",
            font_size=24, color=WHITE,
        )
        formula2.next_to(param_row, DOWN, buff=0.7)
        fit_in_frame(formula2, margin=1.0)
        show(formula2, 1.0)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Discrete domains are enumerable.\nContinuous domains need a shape like the Gaussian.",
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
    Page61().render()
