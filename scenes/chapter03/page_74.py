import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page_74(Scene):

    def construct(self):

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"
        BLUE = "#3E7BFA"

        self.camera.background_color = BG

        def txt(text, size=28, color=WHITE, weight=NORMAL):
            return Text(text, font="DejaVu Sans", font_size=size, color=color, weight=weight)

        def show(obj, time=0.7):
            self.play(Write(obj), run_time=time)

        def clear_scene():
            if self.mobjects:
                self.play(*[FadeOut(obj) for obj in list(self.mobjects)], run_time=0.5)
            self.wait(0.3)

        def gauss(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

        def p_bimodal(x):
            return 0.5 * gauss(x, 2, 0.6) + 0.5 * gauss(x, 6, 0.6)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 40, WHITE, BOLD)
        section = txt("Figure 3.6  &  Asymmetry of KL Divergence", 25, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — THE SETUP
        # ============================================================

        title = txt("Approximating p(x) with a single Gaussian q(x)", 27, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        setup_box = titled_box(
            "The choice",
            txt("p(x) is a mixture of two Gaussians (two modes)\nq(x) can only be a single Gaussian (one mode)",
                17, WHITE),
            chapter="chapter03", width=8.6, height=2.1,
        )
        setup_box.next_to(title, DOWN, buff=0.8)
        fit_in_frame(setup_box, margin=0.8)
        show(setup_box, 1.0)

        question = txt("minimize D_KL(p‖q)  or  D_KL(q‖p) ?", 20, CYAN)
        question.next_to(setup_box, DOWN, buff=0.55)
        fit_in_frame(question, margin=1.0)
        show(question, 0.9)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 3 — LEFT PANEL: MINIMIZE D_KL(P||Q) -> MODE COVERING
        # ============================================================

        title = txt("Minimizing D_KL(p‖q): mode-covering", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(r"q^{*} = \arg\min_{q} D_{\mathrm{KL}}(p\|q)", font_size=28, color=YELLOW)
        formula.next_to(title, DOWN, buff=0.5)
        show(formula, 0.9)

        axes = Axes(
            x_range=[0, 8, 2], y_range=[0, 0.7, 0.2],
            x_length=8, y_length=3.6,
            axis_config={"color": WHITE, "stroke_width": 2, "include_tip": False},
        )
        axes.next_to(formula, DOWN, buff=0.5)

        x_label = txt("x", 18, MUTED)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = txt("Probability Density", 14, MUTED)
        y_label.rotate(PI / 2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)

        p_curve = axes.plot(p_bimodal, x_range=[0, 8], color=BLUE, stroke_width=4)

        def q_cover(x):
            return gauss(x, 4, 1.6)

        q_curve = axes.plot(q_cover, x_range=[0, 8], color=GREEN, stroke_width=3.5)
        q_curve.set_stroke(opacity=0.9)

        legend_p = txt("p(x)", 16, BLUE)
        legend_q = txt("q*(x)", 16, GREEN)
        legend = VGroup(legend_p, legend_q).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.next_to(axes, UP, buff=-1.1).align_to(axes, RIGHT).shift(LEFT * 0.3)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.7)
        self.play(Create(p_curve), FadeIn(legend_p), run_time=1.0)
        self.play(Create(q_curve), FadeIn(legend_q), run_time=1.1)

        note = txt("q blurs across both modes to cover all high-p regions", 17, GREEN)
        note.next_to(axes, DOWN, buff=0.4)
        fit_in_frame(note, margin=1.0)
        show(note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — RIGHT PANEL: MINIMIZE D_KL(Q||P) -> MODE SEEKING
        # ============================================================

        title = txt("Minimizing D_KL(q‖p): mode-seeking", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula2 = MathTex(r"q^{*} = \arg\min_{q} D_{\mathrm{KL}}(q\|p)", font_size=28, color=YELLOW)
        formula2.next_to(title, DOWN, buff=0.5)
        show(formula2, 0.9)

        axes2 = Axes(
            x_range=[0, 8, 2], y_range=[0, 0.7, 0.2],
            x_length=8, y_length=3.6,
            axis_config={"color": WHITE, "stroke_width": 2, "include_tip": False},
        )
        axes2.next_to(formula2, DOWN, buff=0.5)

        x_label2 = txt("x", 18, MUTED)
        x_label2.next_to(axes2.x_axis, DOWN, buff=0.2)
        y_label2 = txt("Probability Density", 14, MUTED)
        y_label2.rotate(PI / 2)
        y_label2.next_to(axes2.y_axis, LEFT, buff=0.3)

        p_curve2 = axes2.plot(p_bimodal, x_range=[0, 8], color=BLUE, stroke_width=4)

        def q_seek(x):
            return gauss(x, 2, 0.45)

        q_curve2 = axes2.plot(q_seek, x_range=[0, 8], color=RED, stroke_width=3.5)

        legend_p2 = txt("p(x)", 16, BLUE)
        legend_q2 = txt("q*(x)", 16, RED)
        legend2 = VGroup(legend_p2, legend_q2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend2.next_to(axes2, UP, buff=-1.1).align_to(axes2, RIGHT).shift(LEFT * 0.3)

        self.play(Create(axes2), FadeIn(x_label2), FadeIn(y_label2), run_time=0.7)
        self.play(Create(p_curve2), FadeIn(legend_p2), run_time=1.0)
        self.play(Create(q_curve2), FadeIn(legend_q2), run_time=1.1)

        note2 = txt("q locks onto a single mode, avoiding low-p regions between modes", 17, RED)
        note2.next_to(axes2, DOWN, buff=0.4)
        fit_in_frame(note2, margin=1.0)
        show(note2, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — SIDE-BY-SIDE COMPARISON
        # ============================================================

        title = txt("Same p, two very different q's", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        cover_box = titled_box(
            "D_KL(p‖q): covering",
            txt("high p → high q\nblurs the modes together", 16, GREEN),
            chapter="chapter03", width=5.3, height=2.0,
        )
        cover_box[0].set_stroke(color=GREEN, width=3)

        seek_box = titled_box(
            "D_KL(q‖p): seeking",
            txt("low p → low q\npicks a single mode", 16, RED),
            chapter="chapter03", width=5.3, height=2.0,
        )
        seek_box[0].set_stroke(color=RED, width=3)

        row = flow_row([cover_box, seek_box], buff=0.6)
        row.move_to(DOWN * 0.2)
        fit_in_frame(row, margin=0.8)

        staggered_fade_in(self, [cover_box, seek_box], run_time=1.3, lag_ratio=0.35)

        note3 = txt("the right direction to use is problem dependent", 18, CYAN)
        note3.next_to(row, DOWN, buff=0.5)
        fit_in_frame(note3, margin=1.0)
        show(note3, 0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "KL divergence is asymmetric:\nthe direction you minimize shapes the approximation.",
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
    Page_74().render()
