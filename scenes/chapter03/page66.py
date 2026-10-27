import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page66(Scene):

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
        section = txt("Figure 3.2  &  Sigmoid / Softplus", 27, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — FIGURE 3.2: GMM SAMPLES, THREE COVARIANCE TYPES
        # ============================================================

        title = txt("Figure 3.2: Samples from a Gaussian mixture", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.6)
        show(title, 0.7)

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=6.5, y_length=6.0,
            axis_config={"color": WHITE, "stroke_width": 2, "include_tip": False},
        )
        axes.move_to(DOWN * 0.3)

        x1_label = MathTex("x_1", font_size=22, color=WHITE)
        x1_label.next_to(axes.x_axis, DOWN, buff=0.25)
        x2_label = MathTex("x_2", font_size=22, color=WHITE)
        x2_label.next_to(axes.y_axis, LEFT, buff=0.25)

        border = Rectangle(width=axes.x_axis.get_length(), height=axes.y_axis.get_length(),
                            stroke_color=WHITE, stroke_width=2)
        border.move_to(axes.get_center())

        self.play(Create(border), Create(axes), FadeIn(x1_label), FadeIn(x2_label), run_time=1.0)

        rng = np.random.default_rng(42)

        # Component 1: isotropic (bottom-left), same variance both directions
        cov1 = np.array([[0.15, 0], [0, 0.15]])
        mean1 = [2, 2]
        pts1 = rng.multivariate_normal(mean1, cov1, 45)

        # Component 2: diagonal, more variance along x2 (middle)
        cov2 = np.array([[0.08, 0], [0, 0.5]])
        mean2 = [5, 5.5]
        pts2 = rng.multivariate_normal(mean2, cov2, 45)

        # Component 3: full-rank, correlated / rotated (top-right)
        cov3 = np.array([[0.25, 0.18], [0.18, 0.2]])
        mean3 = [8, 8]
        pts3 = rng.multivariate_normal(mean3, cov3, 45)

        def make_dots(points, color):
            dots = VGroup()
            for x, y in points:
                x_c = min(max(x, 0.3), 9.7)
                y_c = min(max(y, 0.3), 9.7)
                dot = Dot(axes.c2p(x_c, y_c), radius=0.045, color=color)
                dot.set_stroke(color=WHITE, width=0.5)
                dots.add(dot)
            return dots

        dots1 = make_dots(pts1, "#2E4FD8")
        dots2 = make_dots(pts2, "#2E4FD8")
        dots3 = make_dots(pts3, "#2E4FD8")

        self.play(FadeIn(dots1, lag_ratio=0.02), run_time=0.9)
        self.play(FadeIn(dots2, lag_ratio=0.02), run_time=0.9)
        self.play(FadeIn(dots3, lag_ratio=0.02), run_time=0.9)

        self.wait(1.0)
        clear_scene()

        # ============================================================
        # SCENE 3 — EXPLAIN THE THREE COVARIANCE STRUCTURES
        # ============================================================

        title = txt("Three different covariance structures", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        iso_box = titled_box(
            "Isotropic", txt("same variance\nin every direction", 16, WHITE),
            chapter="chapter03", width=3.4, height=1.7,
        )
        diag_box = titled_box(
            "Diagonal", txt("more variance along x₂\nthan x₁ (axis-aligned)", 15, WHITE),
            chapter="chapter03", width=3.4, height=1.7,
        )
        full_box = titled_box(
            "Full-rank", txt("variance along an\narbitrary rotated axis", 15, WHITE),
            chapter="chapter03", width=3.4, height=1.7,
        )

        row = flow_row([iso_box, diag_box, full_box], buff=0.5)
        row.move_to(DOWN * 0.3)
        fit_in_frame(row, margin=0.8)

        staggered_fade_in(self, [iso_box, diag_box, full_box], run_time=1.4, lag_ratio=0.3)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 4 — SIGMOID FOR THE BERNOULLI PARAMETER
        # ============================================================

        title = txt("Sigmoid produces valid φ values", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "σ(x) always lands in (0, 1) — exactly the valid range for φ.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.4)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.85)

        axes2 = Axes(
            x_range=[-8, 8, 2], y_range=[0, 1, 0.5],
            x_length=8, y_length=3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes2.next_to(statement, DOWN, buff=0.4)

        sigmoid_curve = axes2.plot(lambda x: 1 / (1 + np.exp(-x)), color=CYAN, stroke_width=3.5)

        # saturation zones shaded
        left_flat = axes2.get_area(sigmoid_curve, x_range=(-8, -4), color=RED, opacity=0.2)
        right_flat = axes2.get_area(sigmoid_curve, x_range=(4, 8), color=RED, opacity=0.2)

        self.play(Create(axes2), run_time=0.7)
        self.play(Create(sigmoid_curve), run_time=1.1)
        self.play(FadeIn(left_flat), FadeIn(right_flat), run_time=0.7)

        saturate_note = txt("saturates: flat and insensitive to small changes here", 17, RED)
        saturate_note.next_to(axes2, DOWN, buff=0.4)
        fit_in_frame(saturate_note, margin=1.0)
        show(saturate_note, 0.7)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — SOFTPLUS FUNCTION
        # ============================================================

        title = txt("Softplus: a smoothed max(0, x)", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(r"\zeta(x) = \log(1 + \exp(x))", font_size=30, color=YELLOW)
        formula.next_to(title, DOWN, buff=0.4)
        show(formula, 1.0)

        axes3 = Axes(
            x_range=[-6, 6, 2], y_range=[0, 6, 2],
            x_length=7, y_length=3.2,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes3.next_to(formula, DOWN, buff=0.4)

        relu_curve = axes3.plot(lambda x: max(0, x), x_range=[-6, 6], color=RED, stroke_width=2.5, stroke_opacity=0.7)
        softplus_curve = axes3.plot(lambda x: np.log(1 + np.exp(x)), color=CYAN, stroke_width=3.5)

        relu_label = MathTex(r"x^+ = \max(0,x)", font_size=20, color=RED)
        relu_label.next_to(axes3, RIGHT, buff=0.3).shift(UP * 0.6)

        softplus_label = MathTex(r"\zeta(x)", font_size=20, color=CYAN)
        softplus_label.next_to(axes3, RIGHT, buff=0.3).shift(DOWN * 0.3)

        self.play(Create(axes3), run_time=0.7)
        self.play(Create(relu_curve), FadeIn(relu_label), run_time=0.9)
        self.play(Create(softplus_curve), FadeIn(softplus_label), run_time=1.1)

        note = txt("range (0, ∞) — useful for parameters like β or σ", 18, MUTED)
        note.next_to(axes3, DOWN, buff=0.4)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Sigmoid bounds a value between 0 and 1.\nSoftplus keeps it smoothly positive.",
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
    Page66().render()
