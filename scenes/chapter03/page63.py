import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page63(Scene):

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
        section = txt("3.9.3 – 3.9.5  Precision, Sharp Peaks & the Dirac Delta", 22, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — PRECISION MATRIX
        # ============================================================

        title = txt("Precision matrix: avoiding repeated inversion", 27, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Evaluating the PDF many times means inverting Σ every time — costly.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.9)

        cov_box = titled_box("Covariance form", MathTex(r"\Sigma", font_size=28, color=CYAN), chapter="chapter03", width=3.6, height=1.5)
        prec_box = titled_box("Precision form", MathTex(r"\beta = \Sigma^{-1}", font_size=24, color=YELLOW), chapter="chapter03", width=3.6, height=1.5)

        row = flow_row([cov_box, prec_box], buff=1.0)
        row.move_to(UP * 0.1)
        fit_in_frame(row, margin=1.0)

        arrow = smart_arrow(cov_box, prec_box, chapter="chapter03", color=GREEN)

        self.play(FadeIn(cov_box), run_time=0.5)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(prec_box), run_time=0.5)

        formula = MathTex(
            r"\mathcal{N}(x;\mu,\beta^{-1}) = \sqrt{\frac{\det(\beta)}{(2\pi)^n}}\,"
            r"\exp\!\left(-\frac{1}{2}(x-\mu)^\top\beta(x-\mu)\right)",
            font_size=22, color=WHITE,
        )
        formula.next_to(row, DOWN, buff=0.6)
        fit_in_frame(formula, margin=0.8)
        show(formula, 1.2)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — DIAGONAL AND ISOTROPIC COVARIANCE
        # ============================================================

        title = txt("Simplifying the covariance structure", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        full_box = titled_box("Full Σ", txt("every pair correlated", 16, WHITE), chapter="chapter03", width=3.2, height=1.6)
        diag_box = titled_box("Diagonal Σ", txt("only variances,\nno cross-terms", 16, WHITE), chapter="chapter03", width=3.2, height=1.6)
        iso_box = titled_box("Isotropic Σ", txt("scalar × identity,\nsame spread everywhere", 15, WHITE), chapter="chapter03", width=3.2, height=1.6)

        row = flow_row([full_box, diag_box, iso_box], buff=0.6)
        row.move_to(DOWN * 0.3)
        fit_in_frame(row, margin=1.0)

        staggered_fade_in(self, [full_box, diag_box, iso_box], run_time=1.4, lag_ratio=0.3)

        note = txt("each step trades expressiveness for computational simplicity", 18, MUTED)
        note.next_to(row, DOWN, buff=0.6)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 4 — EXPONENTIAL DISTRIBUTION
        # ============================================================

        title = txt("Exponential distribution: sharp peak at 0", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(r"p(x;\lambda) = \lambda\,\mathbb{1}_{x\ge 0}\,\exp(-\lambda x)", font_size=28, color=WHITE)
        formula.next_to(title, DOWN, buff=0.4)
        show(formula, 1.0)

        axes = Axes(
            x_range=[-2, 4, 1], y_range=[0, 1.2, 0.5],
            x_length=7, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.next_to(formula, DOWN, buff=0.4)

        lam = 1.0
        zero_line = Line(axes.c2p(-2, 0), axes.c2p(0, 0), color=RED, stroke_width=4)
        exp_curve = axes.plot(lambda x: lam * np.exp(-lam * x), x_range=[0, 4], color=CYAN, stroke_width=3.5)
        jump_marker = Dot(axes.c2p(0, lam), radius=0.06, color=CYAN)

        self.play(Create(axes), run_time=0.7)
        self.play(Create(zero_line), run_time=0.5)
        self.play(Create(exp_curve), FadeIn(jump_marker), run_time=1.0)

        note = txt("zero probability for all x < 0 — a hard cutoff", 18, RED)
        note.next_to(axes, DOWN, buff=0.4)
        show(note, 0.6)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — LAPLACE DISTRIBUTION
        # ============================================================

        title = txt("Laplace distribution: peak anywhere", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(r"\mathrm{Laplace}(x;\mu,\gamma) = \frac{1}{2\gamma}\exp\!\left(-\frac{|x-\mu|}{\gamma}\right)", font_size=26, color=WHITE)
        formula.next_to(title, DOWN, buff=0.4)
        fit_in_frame(formula, margin=1.0)
        show(formula, 1.0)

        axes2 = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.6, 0.3],
            x_length=7, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes2.next_to(formula, DOWN, buff=0.4)

        mu, gamma = 0, 1
        laplace_curve = axes2.plot(
            lambda x: (1 / (2 * gamma)) * np.exp(-abs(x - mu) / gamma),
            color=YELLOW, stroke_width=3.5,
        )
        peak_dot = Dot(axes2.c2p(mu, 1 / (2 * gamma)), radius=0.06, color=YELLOW)
        mu_label = MathTex(r"\mu", font_size=22, color=YELLOW).next_to(peak_dot, UP, buff=0.15)

        self.play(Create(axes2), run_time=0.7)
        self.play(Create(laplace_curve), FadeIn(peak_dot), FadeIn(mu_label), run_time=1.1)

        note2 = txt("a sharp, symmetric spike — unlike the smooth Gaussian peak", 18, MUTED)
        note2.next_to(axes2, DOWN, buff=0.4)
        fit_in_frame(note2, margin=1.0)
        show(note2, 0.7)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 6 — DIRAC DELTA: ALL MASS AT ONE POINT
        # ============================================================

        title = txt("The Dirac delta: infinite spike, one point", 27, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(r"p(x) = \delta(x - \mu)", font_size=30, color=WHITE)
        formula.next_to(title, DOWN, buff=0.5)
        show(formula, 0.9)

        axes3 = Axes(
            x_range=[-3, 3, 1], y_range=[0, 1, 1],
            x_length=7, y_length=2.8,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes3.next_to(formula, DOWN, buff=0.5)

        baseline3 = Line(axes3.c2p(-3, 0), axes3.c2p(3, 0), color=MUTED, stroke_width=2)
        spike = Arrow(
            axes3.c2p(0, 0), axes3.c2p(0, 2.2),
            buff=0, color=RED, stroke_width=5, max_tip_length_to_length_ratio=0.15,
        )
        spike_label = MathTex(r"\mu", font_size=22, color=RED).next_to(spike, DOWN, buff=0.15)

        self.play(Create(axes3), Create(baseline3), run_time=0.7)
        self.play(GrowArrow(spike), FadeIn(spike_label), run_time=0.8)

        properties = VGroup(
            txt("zero everywhere except x = μ", 18, MUTED),
            txt("yet integrates to exactly 1", 18, GREEN),
        ).arrange(DOWN, buff=0.25)
        properties.next_to(axes3, DOWN, buff=0.4)
        show(properties, 1.0)

        emphasize_then_settle(self, spike, chapter="chapter03")

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Different shapes for different needs:\nsmooth, sharp, or a single certain point.",
            27, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)
        fit_in_frame(final, margin=1.0)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page63().render()
