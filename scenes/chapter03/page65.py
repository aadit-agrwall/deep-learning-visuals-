import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page65(Scene):

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
        section = txt("3.9.6 – 3.10  Latent Variables & GMMs", 25, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — LATENT VARIABLES
        # ============================================================

        title = txt("Latent variables: hidden causes", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "A latent variable shapes what you see, but you never observe it directly.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.9)

        c_box = titled_box("Latent: c", MathTex("P(c)", font_size=22, color=YELLOW), chapter="chapter03", width=3.0, height=1.4)
        x_box = titled_box("Observed: x", MathTex("P(x \\mid c)", font_size=22, color=CYAN), chapter="chapter03", width=3.0, height=1.4)

        row = flow_row([c_box, x_box], buff=1.2)
        row.move_to(UP * 0.1)
        fit_in_frame(row, margin=1.0)

        # dashed border on c_box to signal "hidden"
        hidden_marker = c_box[0].copy().set_stroke(color=RED, width=2)
        hidden_marker.set_fill(opacity=0)

        arrow = smart_arrow(c_box, x_box, chapter="chapter03", color=GREEN)

        self.play(FadeIn(c_box), run_time=0.6)
        eye_slash = txt("(never seen)", 15, RED)
        eye_slash.next_to(c_box, DOWN, buff=0.15)
        self.play(FadeIn(eye_slash), run_time=0.4)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(x_box), run_time=0.6)

        formula = MathTex(r"P(x, c) = P(x \mid c)\,P(c)", font_size=26, color=WHITE)
        formula.next_to(row, DOWN, buff=0.7)
        show(formula, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — GAUSSIAN MIXTURE MODEL (the visual centerpiece)
        # ============================================================

        title = txt("Gaussian mixture model", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.6)
        show(title, 0.7)

        statement = txt(
            "Each component is its own Gaussian, weighted and summed.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.35)
        show(statement, 0.8)

        axes = Axes(
            x_range=[-6, 8, 2], y_range=[0, 0.5, 0.25],
            x_length=8.5, y_length=3.2,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.next_to(statement, DOWN, buff=0.35)

        components = [
            {"mu": -3, "sigma": 1.0, "alpha": 0.3, "color": CYAN},
            {"mu": 1, "sigma": 1.5, "alpha": 0.5, "color": YELLOW},
            {"mu": 5, "sigma": 0.8, "alpha": 0.2, "color": GREEN},
        ]

        def gaussian(x, mu, sigma):
            return (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        self.play(Create(axes), run_time=0.8)

        component_curves = VGroup()
        for comp in components:
            curve = axes.plot(
                lambda x, m=comp["mu"], s=comp["sigma"]: gaussian(x, m, s) * comp["alpha"] if False else gaussian(x, m, s),
                x_range=[comp["mu"] - 3 * comp["sigma"], comp["mu"] + 3 * comp["sigma"]],
                color=comp["color"], stroke_width=2, stroke_opacity=0.7,
            )
            component_curves.add(curve)

        self.play(LaggedStart(*[Create(c) for c in component_curves], lag_ratio=0.3), run_time=1.5)
        self.wait(0.4)

        def mixture(x):
            return sum(comp["alpha"] * gaussian(x, comp["mu"], comp["sigma"]) for comp in components)

        mixture_curve = axes.plot(mixture, x_range=[-6, 8], color=WHITE, stroke_width=4)

        sum_label = MathTex(r"P(x) = \sum_i \alpha_i\,\mathcal{N}(x;\mu^{(i)},\Sigma^{(i)})", font_size=22, color=WHITE)
        sum_label.next_to(axes, DOWN, buff=0.35)

        self.play(Create(mixture_curve), run_time=1.4)
        show(sum_label, 0.9)

        emphasize_then_settle(self, mixture_curve, chapter="chapter03")

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — SHARED CONSTRAINTS
        # ============================================================

        title = txt("Optional constraints on the mixture", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        free_box = titled_box("Fully free", MathTex(r"\Sigma^{(i)} \text{ per component}", font_size=18, color=CYAN), chapter="chapter03", width=3.6, height=1.5)
        shared_box = titled_box("Shared Σ", MathTex(r"\Sigma^{(i)} = \Sigma\ \forall i", font_size=18, color=YELLOW), chapter="chapter03", width=3.6, height=1.5)
        diag_box = titled_box("Diagonal / isotropic", txt("simpler per-component\ncovariance", 15, WHITE), chapter="chapter03", width=3.6, height=1.5)

        row = flow_row([free_box, shared_box, diag_box], buff=0.5)
        row.move_to(DOWN * 0.3)
        fit_in_frame(row, margin=0.8)

        staggered_fade_in(self, [free_box, shared_box, diag_box], run_time=1.4, lag_ratio=0.3)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — PRIOR vs POSTERIOR
        # ============================================================

        title = txt("Prior vs. posterior belief about c", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        prior_box = titled_box("Prior", MathTex(r"\alpha_i = P(c{=}i)", font_size=22, color=CYAN), chapter="chapter03", width=4.2, height=1.6)
        posterior_box = titled_box("Posterior", MathTex(r"P(c \mid x)", font_size=22, color=GREEN), chapter="chapter03", width=4.2, height=1.6)

        row = flow_row([prior_box, posterior_box], buff=1.0)
        row.move_to(UP * 0.1)
        fit_in_frame(row, margin=1.0)

        arrow = smart_arrow(prior_box, posterior_box, chapter="chapter03", color=YELLOW)
        arrow_label = txt("after observing x", 16, MUTED)
        arrow_label.next_to(arrow, UP, buff=0.15)

        self.play(FadeIn(prior_box), run_time=0.6)
        self.play(GrowArrow(arrow), FadeIn(arrow_label), run_time=0.6)
        self.play(FadeIn(posterior_box), run_time=0.6)

        note = txt("prior = belief BEFORE data      posterior = belief AFTER data", 18, MUTED)
        note.next_to(row, DOWN, buff=0.6)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — UNIVERSAL APPROXIMATOR + SIGMOID INTRO
        # ============================================================

        title = txt("GMMs approximate any smooth density", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Enough components, any error tolerance — a universal approximator.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.9)
        self.wait(0.5)
        clear_scene()

        title2 = txt("3.10  A new useful function: the sigmoid", 30, WHITE, BOLD)
        title2.to_edge(UP, buff=0.7)
        show(title2, 0.8)

        formula2 = MathTex(r"\sigma(x) = \frac{1}{1+\exp(-x)}", font_size=32, color=YELLOW)
        formula2.next_to(title2, DOWN, buff=0.5)
        show(formula2, 1.0)

        axes2 = Axes(
            x_range=[-6, 6, 2], y_range=[0, 1, 0.5],
            x_length=7, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes2.next_to(formula2, DOWN, buff=0.4)

        sigmoid_curve = axes2.plot(lambda x: 1 / (1 + np.exp(-x)), color=CYAN, stroke_width=3.5)

        self.play(Create(axes2), run_time=0.7)
        self.play(Create(sigmoid_curve), run_time=1.2)

        note2 = txt("squashes any real number into (0, 1)", 18, MUTED)
        note2.next_to(axes2, DOWN, buff=0.4)
        show(note2, 0.6)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Hidden variables can shape what we see.\nSimple pieces, summed, approximate anything.",
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
    Page65().render()
