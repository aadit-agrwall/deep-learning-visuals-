from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page59(Scene):

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
        section = txt("3.8  Expectation, Variance, Covariance", 26, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — NOTATION SHORTHAND (stacked, never side by side)
        # ============================================================

        title = txt("Expectation notation, simplified", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        full = MathTex(r"\mathbb{E}_{\mathrm{x}\sim P}[f(x)]", font_size=32, color=WHITE)
        step1 = MathTex(r"\mathbb{E}_{\mathrm{x}}[f(x)]", font_size=32, color=CYAN)
        step2 = MathTex(r"\mathbb{E}[f(x)]", font_size=32, color=YELLOW)
        step3 = MathTex(r"\mathbb{E}[f(x)]\ \text{(brackets omitted when clear)}", font_size=26, color=GREEN)

        captions = [
            txt("full form", 16, MUTED),
            txt("distribution is clear from context", 16, MUTED),
            txt("random variable is clear from context", 16, MUTED),
            txt("assume: averages over ALL variables inside", 16, MUTED),
        ]

        rows = VGroup(*[
            VGroup(eq, cap).arrange(RIGHT, buff=0.6)
            for eq, cap in zip([full, step1, step2, step3], captions)
        ])
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        fit_in_frame(rows, margin=1.0)
        rows.move_to(DOWN * 0.3)

        for row in rows:
            self.play(FadeIn(row, shift=UP * 0.15), run_time=0.7)
            self.wait(0.3)

        self.wait(1.2)
        clear_scene()

        # ============================================================
        # SCENE 3 — LINEARITY OF EXPECTATION
        # ============================================================

        title = txt("Expectation is linear", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Splitting a sum inside E[·] splits the expectation too.",
            22, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        show(statement, 0.75)

        formula = MathTex(
            r"\mathbb{E}_{\mathrm{x}}[\alpha f(x) + \beta g(x)] = "
            r"\alpha\,\mathbb{E}_{\mathrm{x}}[f(x)] + \beta\,\mathbb{E}_{\mathrm{x}}[g(x)]",
            font_size=28, color=WHITE,
        )
        formula.next_to(statement, DOWN, buff=0.7)
        fit_in_frame(formula, margin=1.2)
        show(formula, 1.2)

        condition = txt("valid when α and β do not depend on x", 19, GREEN)
        condition.next_to(formula, DOWN, buff=0.6)
        show(condition, 0.6)

        emphasize_then_settle(self, formula, chapter="chapter03")

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 4 — VARIANCE
        # ============================================================

        title = txt("Variance: how spread out?", 34, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula_v = MathTex(
            r"\mathrm{Var}(f(x)) = \mathbb{E}\left[(f(x) - \mathbb{E}[f(x)])^2\right]",
            font_size=28, color=WHITE,
        )
        formula_v.move_to(UP * 0.9)
        fit_in_frame(formula_v, margin=1.2)
        show(formula_v, 1.1)

        # low variance vs high variance dot clouds, clearly separated columns
        low_title = txt("low variance", 20, CYAN, BOLD)
        high_title = txt("high variance", 20, RED, BOLD)

        low_center = LEFT * 3.0 + DOWN * 1.6
        high_center = RIGHT * 3.0 + DOWN * 1.6

        low_dots = VGroup(*[
            Dot(low_center + np.array([dx, dy, 0]), radius=0.06, color=CYAN)
            for dx, dy in [(-0.15, 0.1), (0.1, -0.1), (0.0, 0.15), (-0.1, -0.05), (0.15, 0.05)]
        ])
        high_dots = VGroup(*[
            Dot(high_center + np.array([dx, dy, 0]), radius=0.06, color=RED)
            for dx, dy in [(-0.8, 0.5), (0.7, -0.6), (0.0, 0.75), (-0.6, -0.5), (0.75, 0.4)]
        ])

        low_title.next_to(low_dots, UP, buff=0.35)
        high_title.next_to(high_dots, UP, buff=0.35)

        self.play(FadeIn(low_title), FadeIn(high_title), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(d) for d in low_dots], lag_ratio=0.1),
            LaggedStart(*[FadeIn(d) for d in high_dots], lag_ratio=0.1),
            run_time=1.0,
        )

        std_note = txt("standard deviation = √variance", 19, MUTED)
        std_note.next_to(VGroup(low_dots, high_dots), DOWN, buff=0.6)
        show(std_note, 0.6)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 5 — COVARIANCE
        # ============================================================

        title = txt("Covariance: do they move together?", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula_c = MathTex(
            r"\mathrm{Cov}(f(x), g(y)) = \mathbb{E}\left[(f(x)-\mathbb{E}[f(x)])(g(y)-\mathbb{E}[g(y)])\right]",
            font_size=22, color=WHITE,
        )
        formula_c.move_to(UP * 1.1)
        fit_in_frame(formula_c, margin=1.0)
        show(formula_c, 1.2)

        pos_title = txt("positive", 20, GREEN, BOLD)
        neg_title = txt("negative", 20, RED, BOLD)

        pos_axes = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=2.6, y_length=2.0,
                         axis_config={"color": MUTED, "stroke_width": 1.5, "include_tip": False})
        neg_axes = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=2.6, y_length=2.0,
                         axis_config={"color": MUTED, "stroke_width": 1.5, "include_tip": False})

        pos_dots = VGroup(*[
            Dot(pos_axes.c2p(x, x + 0.05 * (i % 3 - 1)), radius=0.05, color=GREEN)
            for i, x in enumerate([-0.7, -0.4, 0.0, 0.4, 0.7])
        ])
        neg_dots = VGroup(*[
            Dot(neg_axes.c2p(x, -x + 0.05 * (i % 3 - 1)), radius=0.05, color=RED)
            for i, x in enumerate([-0.7, -0.4, 0.0, 0.4, 0.7])
        ])

        pos_group = VGroup(pos_axes, pos_dots)
        neg_group = VGroup(neg_axes, neg_dots)

        pos_col = VGroup(pos_title, pos_group).arrange(DOWN, buff=0.3)
        neg_col = VGroup(neg_title, neg_group).arrange(DOWN, buff=0.3)

        cov_row = flow_row([pos_col, neg_col], buff=1.5)
        cov_row.next_to(formula_c, DOWN, buff=0.6)
        fit_in_frame(cov_row, margin=1.0)

        self.play(FadeIn(pos_col), FadeIn(neg_col), run_time=1.0)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 6 — COVARIANCE vs INDEPENDENCE
        # ============================================================

        title = txt("Covariance vs. independence", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Related, but not the same — independence is the stronger claim.",
            21, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.45)
        show(statement, 0.8)

        outer_box = titled_box(
            "Independent  ⇒  zero covariance",
            txt("zero linear AND nonlinear relationship", 16, WHITE),
            chapter="chapter03", width=7.0, height=1.6,
        )
        inner_box = titled_box(
            "Zero covariance only",
            txt("no linear relationship\n(nonlinear dependence still possible)", 16, WHITE),
            chapter="chapter03", width=5.0, height=1.6,
        )

        stack = flow_column([outer_box, inner_box], buff=0.6)
        stack.move_to(DOWN * 0.3)
        fit_in_frame(stack, margin=0.8)

        self.play(GrowFromCenter(outer_box), run_time=0.8)
        self.wait(0.3)
        self.play(GrowFromCenter(inner_box), run_time=0.8)

        note = txt("dependent variables CAN still have zero covariance", 18, YELLOW)
        note.next_to(stack, DOWN, buff=0.5)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Variance measures spread.\nCovariance measures shared movement.",
            30, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)

        self.play(Write(final), run_time=1.0)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page59().render()
