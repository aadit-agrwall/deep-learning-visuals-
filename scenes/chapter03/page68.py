import numpy as np
from manim import *

from common.layouts import fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle


class Page68(Scene):

    def construct(self):

        # ============================================================
        # THEME — SAME AS PAGE 66 / 67
        # ============================================================

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"

        self.camera.background_color = BG

        def txt(text, size=28, color=WHITE, weight=NORMAL):
            return Text(
                text,
                font="DejaVu Sans",
                font_size=size,
                color=color,
                weight=weight
            )

        def show(obj, time=0.7):
            self.play(Write(obj), run_time=time)

        def clear_scene():
            if self.mobjects:
                self.play(
                    *[FadeOut(obj) for obj in list(self.mobjects)],
                    run_time=0.5
                )
            self.wait(0.25)

        # ============================================================
        # SCENE 1 — SECTION INTRO
        # ============================================================

        chapter = txt(
            "CHAPTER 3",
            24,
            CYAN,
            BOLD
        )

        heading = txt(
            "Probability and Information Theory",
            38,
            WHITE,
            BOLD
        )

        section = txt(
            "3.11  Bayes' Rule",
            31,
            YELLOW
        )

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.75)
        show(section, 0.6)

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 2 — THE PROBLEM
        # ============================================================

        title = txt(
            "What if we know P(y | x)...",
            32,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.75)

        known = MathTex(
            r"P(y\mid x)",
            font_size=43,
            color=CYAN
        )

        known.move_to(LEFT * 2.5 + UP * 0.8)

        arrow = Arrow(
            known.get_right(),
            RIGHT * 0.2 + UP * 0.8,
            buff=0.25,
            color=MUTED,
            stroke_width=3
        )

        question = MathTex(
            r"P(x\mid y)\;?",
            font_size=43,
            color=RED
        )

        question.move_to(RIGHT * 2.0 + UP * 0.8)

        explain = txt(
            "We know the probability of the evidence given the cause.\n"
            "But often, we need the probability of the cause given the evidence.",
            18,
            MUTED
        )

        explain.next_to(known, DOWN, buff=0.7)
        fit_in_frame(explain, margin=0.8)

        show(title, 0.7)

        self.play(
            FadeIn(known, shift=LEFT * 0.3),
            run_time=0.7
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.5
        )

        self.play(
            FadeIn(question, shift=RIGHT * 0.3),
            run_time=0.7
        )

        show(explain, 0.9)

        # Emphasize the question
        self.play(
            Indicate(
                question,
                color=RED,
                scale_factor=1.15
            ),
            run_time=0.8
        )

        self.wait(0.7)

        clear_scene()

        # ============================================================
        # SCENE 3 — BAYES RULE APPEARS
        # ============================================================

        title = txt(
            "Bayes' rule reverses the direction",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        formula = MathTex(
            r"P(x\mid y)=\frac{P(x)P(y\mid x)}{P(y)}",
            font_size=42,
            color=YELLOW
        )

        formula.move_to(ORIGIN + UP * 0.8)

        show(title, 0.7)
        self.play(
            Write(formula),
            run_time=1.3
        )

        # ============================================================
        # BREAK THE EQUATION INTO THREE CONCEPTS
        # ============================================================

        prior = MathTex(
            r"P(x)",
            font_size=30,
            color=CYAN
        )

        likelihood = MathTex(
            r"P(y\mid x)",
            font_size=30,
            color=CYAN
        )

        evidence = MathTex(
            r"P(y)",
            font_size=30,
            color=MUTED
        )

        prior_label = txt(
            "prior",
            17,
            WHITE
        )

        likelihood_label = txt(
            "likelihood",
            17,
            WHITE
        )

        evidence_label = txt(
            "evidence",
            17,
            WHITE
        )

        prior_group = VGroup(prior, prior_label)
        likelihood_group = VGroup(likelihood, likelihood_label)
        evidence_group = VGroup(evidence, evidence_label)

        prior_label.next_to(prior, DOWN, buff=0.15)
        likelihood_label.next_to(likelihood, DOWN, buff=0.15)
        evidence_label.next_to(evidence, DOWN, buff=0.15)

        prior_group.move_to(LEFT * 3.3 + DOWN * 1.1)
        likelihood_group.move_to(ORIGIN + DOWN * 1.1)
        evidence_group.move_to(RIGHT * 3.3 + DOWN * 1.1)

        self.play(
            FadeIn(prior_group, shift=UP * 0.2),
            FadeIn(likelihood_group, shift=UP * 0.2),
            FadeIn(evidence_group, shift=UP * 0.2),
            run_time=0.9
        )

        self.wait(1.0)

        # Highlight numerator
        numerator_box = SurroundingRectangle(
            VGroup(prior, likelihood),
            color=CYAN,
            buff=0.15,
            stroke_width=2
        )

        self.play(
            Create(numerator_box),
            run_time=0.5
        )

        numerator_note = txt(
            "prior × likelihood",
            18,
            CYAN,
            BOLD
        )

        numerator_note.next_to(
            numerator_box,
            UP,
            buff=0.18
        )

        self.play(
            FadeIn(numerator_note),
            run_time=0.5
        )

        self.wait(0.6)

        clear_scene()

        # ============================================================
        # SCENE 4 — BAYES AS AN UPDATE
        # ============================================================

        title = txt(
            "Think of Bayes' rule as an update",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        prior_title = txt(
            "Prior belief",
            22,
            CYAN,
            BOLD
        )

        prior_formula = MathTex(
            r"P(x)",
            font_size=36,
            color=CYAN
        )

        prior_title.next_to(
            prior_formula,
            UP,
            buff=0.25
        )

        prior_group = VGroup(
            prior_title,
            prior_formula
        )

        prior_group.move_to(
            LEFT * 3.4 + DOWN * 0.3
        )

        evidence_title = txt(
            "New evidence",
            22,
            YELLOW,
            BOLD
        )

        evidence_formula = MathTex(
            r"P(y\mid x)",
            font_size=36,
            color=YELLOW
        )

        evidence_title.next_to(
            evidence_formula,
            UP,
            buff=0.25
        )

        evidence_group = VGroup(
            evidence_title,
            evidence_formula
        )

        evidence_group.move_to(
            ORIGIN + DOWN * 0.3
        )

        posterior_title = txt(
            "Updated belief",
            22,
            GREEN,
            BOLD
        )

        posterior_formula = MathTex(
            r"P(x\mid y)",
            font_size=36,
            color=GREEN
        )

        posterior_title.next_to(
            posterior_formula,
            UP,
            buff=0.25
        )

        posterior_group = VGroup(
            posterior_title,
            posterior_formula
        )

        posterior_group.move_to(
            RIGHT * 3.4 + DOWN * 0.3
        )

        show(title, 0.7)

        self.play(
            FadeIn(prior_group, shift=LEFT * 0.3),
            run_time=0.6
        )

        arrow1 = Arrow(
            prior_group.get_right(),
            evidence_group.get_left(),
            buff=0.3,
            color=MUTED,
            stroke_width=3
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.5
        )

        self.play(
            FadeIn(evidence_group, shift=UP * 0.25),
            run_time=0.7
        )

        arrow2 = Arrow(
            evidence_group.get_right(),
            posterior_group.get_left(),
            buff=0.3,
            color=MUTED,
            stroke_width=3
        )

        self.play(
            GrowArrow(arrow2),
            run_time=0.5
        )

        self.play(
            FadeIn(posterior_group, shift=RIGHT * 0.3),
            run_time=0.7
        )

        update_note = txt(
            "Evidence changes what we believe.",
            21,
            WHITE,
            BOLD
        )

        update_note.to_edge(DOWN, buff=0.7)

        self.play(
            FadeIn(update_note, shift=UP * 0.15),
            run_time=0.6
        )

        self.play(
            Indicate(
                posterior_formula,
                color=GREEN,
                scale_factor=1.15
            ),
            run_time=0.7
        )

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 5 — WHY P(y) IS THERE
        # ============================================================

        title = txt(
            "But what about P(y)?",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        statement = txt(
            "It normalizes the result so the probabilities remain valid.",
            20,
            MUTED
        )

        statement.next_to(title, DOWN, buff=0.35)

        show(title, 0.7)
        show(statement, 0.7)

        denominator = MathTex(
            r"P(y)=\sum_x P(y\mid x)P(x)",
            font_size=34,
            color=YELLOW
        )

        denominator.next_to(
            statement,
            DOWN,
            buff=0.6
        )

        self.play(
            Write(denominator),
            run_time=1.1
        )

        # Visual normalization concept
        bar1 = Rectangle(
            width=2.4,
            height=0.55,
            stroke_color=MUTED,
            stroke_width=2
        )

        bar2 = Rectangle(
            width=2.4,
            height=0.55,
            stroke_color=MUTED,
            stroke_width=2
        )

        bar3 = Rectangle(
            width=2.4,
            height=0.55,
            stroke_color=MUTED,
            stroke_width=2
        )

        bars = VGroup(bar1, bar2, bar3).arrange(
            DOWN,
            buff=0.28
        )

        bars.next_to(
            denominator,
            DOWN,
            buff=0.65
        )

        self.play(
            FadeIn(bars, shift=UP * 0.2),
            run_time=0.6
        )

        # Fill portions
        fill1 = Rectangle(
            width=1.5,
            height=0.55,
            fill_opacity=0.7,
            fill_color=CYAN,
            stroke_opacity=0
        )

        fill2 = Rectangle(
            width=0.9,
            height=0.55,
            fill_opacity=0.7,
            fill_color=CYAN,
            stroke_opacity=0
        )

        fill3 = Rectangle(
            width=1.8,
            height=0.55,
            fill_opacity=0.7,
            fill_color=CYAN,
            stroke_opacity=0
        )

        fill1.move_to(bar1.get_left() + RIGHT * 0.75)
        fill2.move_to(bar2.get_left() + RIGHT * 0.45)
        fill3.move_to(bar3.get_left() + RIGHT * 0.9)

        self.play(
            FadeIn(fill1),
            FadeIn(fill2),
            FadeIn(fill3),
            run_time=0.7
        )

        normalize_note = txt(
            "P(y) collects all ways the evidence can occur.",
            18,
            GREEN
        )

        normalize_note.to_edge(DOWN, buff=0.65)

        self.play(
            FadeIn(normalize_note, shift=UP * 0.15),
            run_time=0.6
        )

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 6 — FINAL TAKEAWAY
        # ============================================================

        label = txt(
            "THE KEY IDEA",
            23,
            CYAN,
            BOLD
        )

        label.to_edge(UP, buff=0.85)

        formula = MathTex(
            r"P(x\mid y)=\frac{P(x)P(y\mid x)}{P(y)}",
            font_size=42,
            color=YELLOW
        )

        formula.move_to(
            ORIGIN + UP * 0.7
        )

        main = txt(
            "Bayes' rule lets us reason backward:\n"
            "from evidence to the belief that produced it.",
            25,
            WHITE,
            BOLD
        )

        main.next_to(
            formula,
            DOWN,
            buff=0.55
        )

        fit_in_frame(main, margin=0.8)

        show(label, 0.5)

        self.play(
            Write(formula),
            run_time=1.2
        )

        self.play(
            Write(main),
            run_time=1.2
        )

        note = txt(
            "Prior belief + evidence → updated belief",
            19,
            MUTED
        )

        note.to_edge(
            DOWN,
            buff=0.7
        )

        self.play(
            FadeIn(note, shift=UP * 0.15),
            run_time=0.6
        )

        underline = Underline(
            main,
            color=CYAN,
            stroke_width=3,
            buff=0.15
        )

        self.play(
            Create(underline),
            run_time=0.5
        )

        self.wait(2.0)


if __name__ == "__main__":
    Page68().render()
