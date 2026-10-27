import numpy as np
from manim import *

from common.connectors import smart_arrow
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page_71(Scene):

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
        section = txt("3.13  Information Theory", 27, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — WHAT IS INFORMATION THEORY
        # ============================================================

        title = txt("Quantifying information in a signal", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        origin_box = titled_box(
            "Origin", txt("designing optimal codes for\nmessages over a noisy channel", 16, WHITE),
            chapter="chapter03", width=4.6, height=1.9,
        )
        ml_box = titled_box(
            "In machine learning", txt("characterize distributions &\nquantify similarity between them", 16, WHITE),
            chapter="chapter03", width=4.6, height=1.9,
        )

        row = flow_row([origin_box, ml_box], buff=0.8)
        row.move_to(DOWN * 0.4)
        fit_in_frame(row, margin=0.8)

        staggered_fade_in(self, [origin_box, ml_box], run_time=1.2, lag_ratio=0.35)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 3 — CORE INTUITION: UNLIKELY = MORE INFORMATIVE
        # ============================================================

        title = txt("Unlikely events carry more information", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        likely_box = titled_box(
            "\"The sun rose this morning\"",
            txt("P ≈ 1  →  uninformative,\nunnecessary to even send", 16, GREEN),
            chapter="chapter03", width=5.6, height=2.0,
        )
        unlikely_box = titled_box(
            "\"There was a solar eclipse\"",
            txt("P ≈ 0  →  highly informative,\nworth sending", 16, RED),
            chapter="chapter03", width=5.6, height=2.0,
        )

        col = flow_row([likely_box, unlikely_box], buff=0.6)
        col.move_to(DOWN * 0.3)
        fit_in_frame(col, margin=0.8)

        staggered_fade_in(self, [likely_box, unlikely_box], run_time=1.2, lag_ratio=0.35)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — THREE DESIRED PROPERTIES
        # ============================================================

        title = txt("Three properties we want", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        p1 = txt("1.  Likely events → low information\n     (guaranteed events → zero information)", 20, WHITE)
        p2 = txt("2.  Less likely events → higher information", 20, WHITE)
        p3 = txt("3.  Independent events → additive information", 20, WHITE)

        props = VGroup(p1, p2, p3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        props.move_to(UP * 0.2)
        fit_in_frame(props, margin=1.0)

        staggered_fade_in(self, [p1, p2, p3], run_time=1.3, lag_ratio=0.4)
        self.wait(0.6)

        coin_note = txt("two heads in a row ⇒ twice the information of one head", 18, CYAN)
        coin_note.next_to(props, DOWN, buff=0.55)
        fit_in_frame(coin_note, margin=1.0)
        show(coin_note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — SELF-INFORMATION FORMULA
        # ============================================================

        title = txt("Self-information", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(r"I(x) = -\log P(x)", font_size=38, color=YELLOW)
        formula.next_to(title, DOWN, buff=0.6)
        show(formula, 1.0)

        eq_num = txt("(3.48)", 18, MUTED)
        eq_num.next_to(formula, RIGHT, buff=1.0)
        show(eq_num, 0.4)

        axes = Axes(
            x_range=[0.02, 1, 0.2], y_range=[0, 4, 1],
            x_length=7, y_length=3.2,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
        )
        axes.next_to(formula, DOWN, buff=0.6)

        curve = axes.plot(lambda p: -np.log(p), x_range=[0.02, 1], color=CYAN, stroke_width=3.5)

        px_label = txt("P(x)", 16, MUTED)
        px_label.next_to(axes.x_axis, DOWN, buff=0.2)
        ix_label = txt("I(x)", 16, MUTED)
        ix_label.next_to(axes.y_axis, LEFT, buff=0.2)

        self.play(Create(axes), FadeIn(px_label), FadeIn(ix_label), run_time=0.7)
        self.play(Create(curve), run_time=1.1)

        note = txt("P(x) → 1 gives I(x) → 0;  P(x) → 0 gives I(x) → ∞", 17, MUTED)
        note.next_to(axes, DOWN, buff=0.35)
        fit_in_frame(note, margin=1.0)
        show(note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — UNITS: NATS VS BITS
        # ============================================================

        title = txt("Units: nats", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        nat_formula = MathTex(r"\log = \log_e", font_size=32, color=YELLOW)
        nat_formula.next_to(title, DOWN, buff=0.5)
        show(nat_formula, 0.9)

        nat_box = titled_box(
            "1 nat",
            txt("information gained from observing\nan event of probability  1/e", 16, WHITE),
            chapter="chapter03", width=7.5, height=1.9,
        )
        nat_box.next_to(nat_formula, DOWN, buff=0.6)
        fit_in_frame(nat_box, margin=0.8)

        show(nat_box, 0.9)

        bit_note = txt("(other texts use base-2 logarithms — units of bits / shannons)", 16, MUTED)
        bit_note.next_to(nat_box, DOWN, buff=0.5)
        fit_in_frame(bit_note, margin=1.0)
        show(bit_note, 0.7)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Information is the surprise of an outcome:\nrarer events carry more of it.",
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
    Page_71().render()
