import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page62(Scene):

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
        section = txt("Figure 3.1  &  Why the Gaussian?", 26, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — FIGURE 3.1: THE STANDARD NORMAL, PRECISELY
        # ============================================================

        title = txt("Figure 3.1: The normal distribution", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.6)
        show(title, 0.7)

        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[0, 0.40, 0.05],
            x_length=9,
            y_length=4.8,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
            x_axis_config={"numbers_to_include": [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]},
            y_axis_config={"numbers_to_include": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]},
            tips=False,
        )
        axes.next_to(title, DOWN, buff=0.4)

        x_axis_label = txt("x", 20, MUTED)
        x_axis_label.next_to(axes.x_axis, DOWN, buff=0.3)
        y_axis_label = txt("p(x)", 18, MUTED)
        y_axis_label.next_to(axes.y_axis, LEFT, buff=0.35).rotate(PI / 2)
        y_axis_label.move_to(axes.y_axis.get_center() + LEFT * 0.7)

        mu, sigma = 0, 1
        curve = axes.plot(
            lambda x: (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2),
            x_range=[-2, 2],
            color=CYAN, stroke_width=3.5,
        )

        self.play(Create(axes), FadeIn(x_axis_label), FadeIn(y_axis_label), run_time=1.2)
        self.play(Create(curve), run_time=1.6)
        self.wait(0.4)

        # --- Maximum at x = mu ---
        peak_x, peak_y = mu, (1 / np.sqrt(2 * np.pi * sigma ** 2))
        peak_point = axes.c2p(peak_x, peak_y)
        peak_arrow = Arrow(
            axes.c2p(peak_x, peak_y - 0.12), peak_point,
            buff=0.02, color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.25,
        )
        peak_label = Text("Maximum at x = μ", font="DejaVu Sans", font_size=18, color=WHITE)
        peak_label.next_to(peak_arrow, UP, buff=0.15).shift(RIGHT * 0.9)

        self.play(GrowArrow(peak_arrow), run_time=0.6)
        show(peak_label, 0.6)
        self.wait(0.5)

        # --- Inflection points at x = mu ± sigma ---
        infl_y = (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(-0.5)
        left_infl = axes.c2p(mu - sigma, infl_y)
        right_infl = axes.c2p(mu + sigma, infl_y)

        infl_label = Text("Inflection points at\nx = μ ± σ", font="DejaVu Sans", font_size=18, color=WHITE)
        infl_label.move_to(axes.c2p(mu, infl_y) + UP * 0.55)

        left_arrow = Arrow(infl_label.get_left() + LEFT * 0.1, left_infl, buff=0.05, color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        right_arrow = Arrow(infl_label.get_right() + RIGHT * 0.1, right_infl, buff=0.05, color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(infl_label), run_time=0.5)
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow), run_time=0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 3 — REASON 1: CENTRAL LIMIT THEOREM
        # ============================================================

        title = txt("Reason 1: the Central Limit Theorem", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Sums of many independent random variables tend toward normal.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.85)

        # visual: several ragged small distributions summing into one smooth bell
        small_dists = VGroup()
        for i in range(4):
            mini_axes = Axes(
                x_range=[-2, 2, 1], y_range=[0, 1, 1],
                x_length=1.6, y_length=1.0,
                axis_config={"stroke_width": 1, "color": MUTED, "include_tip": False},
            )
            heights = np.random.RandomState(i).uniform(0.2, 1.0, 5)
            bars = VGroup(*[
                Rectangle(width=0.25, height=h * 0.9, fill_color=YELLOW, fill_opacity=0.8, stroke_width=0)
                for h in heights
            ]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
            bars.move_to(mini_axes.get_center())
            small_dists.add(VGroup(mini_axes, bars))

        small_row = flow_row(list(small_dists), buff=0.5)
        small_row.move_to(UP * 1.3)
        fit_in_frame(small_row, margin=1.2)

        plus_signs = VGroup(*[MathTex("+", font_size=24, color=WHITE) for _ in range(3)])
        for i, plus in enumerate(plus_signs):
            plus.move_to((small_dists[i].get_right() + small_dists[i + 1].get_left()) / 2)

        self.play(FadeIn(small_row, lag_ratio=0.15), FadeIn(plus_signs), run_time=1.1)

        arrow_down = Arrow(small_row.get_bottom(), small_row.get_bottom() + DOWN * 0.8, buff=0.1, color=GREEN, stroke_width=3)
        self.play(GrowArrow(arrow_down), run_time=0.5)

        mini_bell_axes = Axes(
            x_range=[-2, 2, 1], y_range=[0, 0.4, 0.2],
            x_length=4, y_length=1.6,
            axis_config={"stroke_width": 1.5, "color": MUTED, "include_tip": False},
        )
        mini_bell_axes.next_to(arrow_down, DOWN, buff=0.3)
        mini_bell_curve = mini_bell_axes.plot(
            lambda x: (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x ** 2),
            color=GREEN, stroke_width=3,
        )

        self.play(Create(mini_bell_axes), run_time=0.5)
        self.play(Create(mini_bell_curve), run_time=0.9)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 4 — REASON 2: MAXIMUM ENTROPY
        # ============================================================

        title = txt("Reason 2: maximum uncertainty", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Among distributions with the same variance, the normal assumes the LEAST.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.9)

        least_box = titled_box(
            "Least prior knowledge",
            txt("→ Gaussian shape\n(safest default)", 18, WHITE),
            chapter="chapter03", width=4.6, height=1.9,
        )
        least_box.move_to(DOWN * 0.5)

        self.play(GrowFromCenter(least_box), run_time=0.9)
        emphasize_then_settle(self, least_box, chapter="chapter03")

        footnote = txt("full justification requires more tools (section 19.4.2)", 17, MUTED)
        footnote.next_to(least_box, DOWN, buff=0.5)
        show(footnote, 0.6)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — MULTIVARIATE NORMAL DISTRIBUTION
        # ============================================================

        title = txt("Generalizing to n dimensions", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "μ becomes a vector; σ² becomes a covariance matrix Σ.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        fit_in_frame(statement, margin=1.0)
        show(statement, 0.85)

        formula = MathTex(
            r"\mathcal{N}(\mathbf{x};\boldsymbol{\mu},\boldsymbol{\Sigma}) = "
            r"\sqrt{\frac{1}{(2\pi)^n \det(\boldsymbol{\Sigma})}}\,"
            r"\exp\!\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x}-\boldsymbol{\mu})\right)",
            font_size=24, color=WHITE,
        )
        formula.next_to(statement, DOWN, buff=0.6)
        fit_in_frame(formula, margin=0.8)
        show(formula, 1.4)

        requirement = txt("Σ must be positive definite and symmetric", 19, YELLOW)
        requirement.next_to(formula, DOWN, buff=0.6)
        show(requirement, 0.7)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "The bell curve isn't arbitrary —\nit's the least-assuming shape available.",
            28, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)
        fit_in_frame(final, margin=1.0)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page62().render()
