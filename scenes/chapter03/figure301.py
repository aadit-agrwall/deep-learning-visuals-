from manim import *
import numpy as np


class Figure301(Scene):

    def construct(self):

        # ============================================================
        # CHAPTER 3 STYLE
        # ============================================================

        BG = "#04244E"
        WHITE_TEXT = "#F5F7FA"
        BLUE_TEXT = "#B9D7F2"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        SOFT = "#8FAEC9"

        self.camera.background_color = BG

        # ============================================================
        # HELPERS
        # ============================================================

        def fade_out_all(group, runtime=0.45):
            self.play(
                FadeOut(group),
                run_time=runtime,
            )
            self.remove(group)
            self.wait(0.15)

        # ============================================================
        # CHAPTER TITLE
        # ============================================================

        chapter = Text(
            "CHAPTER 3",
            font="Times New Roman",
            font_size=25,
            color=CYAN,
        )

        chapter.to_edge(
            UP,
            buff=0.35,
        )

        title = Text(
            "Probability and Information Theory",
            font="Times New Roman",
            font_size=39,
            color=WHITE_TEXT,
        )

        title.move_to(
            UP * 1.55
        )

        self.play(
            Write(chapter),
            run_time=0.5,
        )

        self.play(
            Write(title),
            run_time=0.8,
        )

        self.wait(1.2)

        # ============================================================
        # UNCERTAINTY
        # ============================================================

        self.play(
            FadeOut(chapter),
            FadeOut(title),
            run_time=0.45,
        )

        uncertainty_title = Text(
            "Uncertainty",
            font="Times New Roman",
            font_size=34,
            color=WHITE_TEXT,
        )

        uncertainty_title.move_to(
            UP * 2.15
        )

        self.play(
            Write(uncertainty_title),
            run_time=0.55,
        )

        # Three possible outcomes
        labels = [
            ("A", -3.1),
            ("B", 0),
            ("C", 3.1),
        ]

        circles = VGroup()

        for label, x in labels:

            circle = Circle(
                radius=0.62,
                stroke_width=2,
                color=SOFT,
            )

            circle.move_to(
                RIGHT * x + DOWN * 0.15
            )

            txt = Text(
                label,
                font="Times New Roman",
                font_size=30,
                color=WHITE_TEXT,
            )

            txt.move_to(
                circle.get_center()
            )

            circles.add(
                VGroup(circle, txt)
            )

        self.play(
            LaggedStart(
                *[
                    FadeIn(c)
                    for c in circles
                ],
                lag_ratio=0.18,
            ),
            run_time=0.9,
        )

        question = Text(
            "Which outcome will occur?",
            font="Times New Roman",
            font_size=24,
            color=BLUE_TEXT,
        )

        question.move_to(
            DOWN * 1.35
        )

        self.play(
            Write(question),
            run_time=0.55,
        )

        self.wait(1.2)

        # ============================================================
        # PROBABILITY
        # ============================================================

        group_uncertainty = VGroup(
            uncertainty_title,
            circles,
            question,
        )

        fade_out_all(group_uncertainty)

        probability_title = Text(
            "Probability",
            font="Times New Roman",
            font_size=34,
            color=WHITE_TEXT,
        )

        probability_title.move_to(
            UP * 2.25
        )

        self.play(
            Write(probability_title),
            run_time=0.55,
        )

        # Axes
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=7.5,
            y_length=3.6,
            axis_config={
                "color": SOFT,
                "stroke_width": 1.5,
            },
            tips=False,
        )

        axes.move_to(
            DOWN * 0.25
        )

        self.play(
            Create(axes),
            run_time=0.7,
        )

        # Probability distribution
        bars = VGroup()

        probabilities = [
            0.25,
            0.55,
            0.85,
            0.40,
        ]

        for i, value in enumerate(probabilities):

            x = i + 0.5

            bar = Rectangle(
                width=0.75,
                height=value * 2.8,
                fill_opacity=0.75,
                stroke_width=1.5,
                stroke_color=CYAN,
                fill_color=CYAN,
            )

            bar.move_to(
                axes.c2p(x, value / 2)
            )

            bars.add(bar)

        self.play(
            LaggedStart(
                *[
                    GrowFromEdge(
                        bar,
                        DOWN,
                    )
                    for bar in bars
                ],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )

        distribution_label = Text(
            "A probability distribution assigns weight to possible outcomes.",
            font="Times New Roman",
            font_size=20,
            color=BLUE_TEXT,
        )

        distribution_label.move_to(
            DOWN * 2.35
        )

        self.play(
            Write(distribution_label),
            run_time=0.65,
        )

        self.wait(1.4)

        # ============================================================
        # REASONING UNDER UNCERTAINTY
        # ============================================================

        group_probability = VGroup(
            probability_title,
            axes,
            bars,
            distribution_label,
        )

        fade_out_all(group_probability)

        reasoning_title = Text(
            "Reasoning under uncertainty",
            font="Times New Roman",
            font_size=33,
            color=WHITE_TEXT,
        )

        reasoning_title.move_to(
            UP * 2.25
        )

        self.play(
            Write(reasoning_title),
            run_time=0.6,
        )

        # Probability box
        probability_box = RoundedRectangle(
            width=2.5,
            height=1.25,
            corner_radius=0.15,
            stroke_width=2,
            color=CYAN,
        )

        probability_box.move_to(
            LEFT * 3.2 + DOWN * 0.1
        )

        probability_text = Text(
            "Probability",
            font="Times New Roman",
            font_size=27,
            color=CYAN,
        )

        probability_text.move_to(
            probability_box.get_center()
        )

        # AI reasoning box
        ai_box = RoundedRectangle(
            width=2.5,
            height=1.25,
            corner_radius=0.15,
            stroke_width=2,
            color=YELLOW,
        )

        ai_box.move_to(
            RIGHT * 3.2 + DOWN * 0.1
        )

        ai_text = Text(
            "AI reasoning",
            font="Times New Roman",
            font_size=27,
            color=YELLOW,
        )

        ai_text.move_to(
            ai_box.get_center()
        )

        arrow = Arrow(
            start=probability_box.get_right() + RIGHT * 0.25,
            end=ai_box.get_left() + LEFT * 0.25,
            buff=0.05,
            stroke_width=2.5,
            color=WHITE_TEXT,
        )

        explanation = Text(
            "Probability theory provides rules for reasoning with uncertainty.",
            font="Times New Roman",
            font_size=21,
            color=BLUE_TEXT,
        )

        explanation.move_to(
            DOWN * 1.65
        )

        self.play(
            Create(probability_box),
            Write(probability_text),
            run_time=0.65,
        )

        self.play(
            Create(arrow),
            run_time=0.45,
        )

        self.play(
            Create(ai_box),
            Write(ai_text),
            run_time=0.65,
        )

        self.play(
            Write(explanation),
            run_time=0.6,
        )

        self.wait(1.4)

        # ============================================================
        # INFORMATION THEORY
        # ============================================================

        group_reasoning = VGroup(
            reasoning_title,
            probability_box,
            probability_text,
            arrow,
            ai_box,
            ai_text,
            explanation,
        )

        fade_out_all(group_reasoning)

        information_title = Text(
            "Information Theory",
            font="Times New Roman",
            font_size=34,
            color=WHITE_TEXT,
        )

        information_title.move_to(
            UP * 2.25
        )

        self.play(
            Write(information_title),
            run_time=0.6,
        )

        # Uncertainty meter
        meter = Line(
            LEFT * 3.8 + DOWN * 0.15,
            RIGHT * 3.8 + DOWN * 0.15,
            color=SOFT,
            stroke_width=4,
        )

        low = Text(
            "low uncertainty",
            font="Times New Roman",
            font_size=20,
            color=BLUE_TEXT,
        )

        high = Text(
            "high uncertainty",
            font="Times New Roman",
            font_size=20,
            color=BLUE_TEXT,
        )

        low.next_to(
            meter.get_left(),
            DOWN,
            buff=0.35,
        )

        high.next_to(
            meter.get_right(),
            DOWN,
            buff=0.35,
        )

        marker = Dot(
            point=meter.get_center(),
            radius=0.11,
            color=YELLOW,
        )

        entropy = MathTex(
            r"H(X)",
            font_size=42,
            color=YELLOW,
        )

        entropy.move_to(
            UP * 0.75
        )

        entropy_label = Text(
            "Entropy measures uncertainty in a distribution.",
            font="Times New Roman",
            font_size=22,
            color=WHITE_TEXT,
        )

        entropy_label.move_to(
            DOWN * 1.35
        )

        self.play(
            Create(meter),
            FadeIn(low),
            FadeIn(high),
            run_time=0.7,
        )

        self.play(
            FadeIn(marker),
            Write(entropy),
            run_time=0.65,
        )

        self.play(
            Write(entropy_label),
            run_time=0.55,
        )

        # Move marker to demonstrate changing uncertainty
        self.play(
            marker.animate.move_to(
                meter.get_left() + RIGHT * 1.25
            ),
            run_time=0.8,
        )

        self.play(
            marker.animate.move_to(
                meter.get_right() + LEFT * 1.25
            ),
            run_time=0.8,
        )

        self.wait(1.2)

        # ============================================================
        # FINAL CHAPTER MAP
        # ============================================================

        group_information = VGroup(
            information_title,
            meter,
            low,
            high,
            marker,
            entropy,
            entropy_label,
        )

        fade_out_all(group_information)

        final_title = Text(
            "Chapter 3",
            font="Times New Roman",
            font_size=29,
            color=CYAN,
        )

        final_title.move_to(
            UP * 2.2
        )

        self.play(
            Write(final_title),
            run_time=0.5,
        )

        # Four concepts
        concepts = [
            ("Uncertainty", -3.9),
            ("Probability", -1.3),
            ("Reasoning", 1.3),
            ("Information", 3.9),
        ]

        concept_group = VGroup()

        for text, x in concepts:

            box = RoundedRectangle(
                width=2.15,
                height=1.05,
                corner_radius=0.12,
                stroke_width=2,
                color=CYAN,
            )

            box.move_to(
                RIGHT * x + DOWN * 0.15
            )

            label = Text(
                text,
                font="Times New Roman",
                font_size=21,
                color=WHITE_TEXT,
            )

            label.move_to(
                box.get_center()
            )

            concept_group.add(
                VGroup(box, label)
            )

        self.play(
            LaggedStart(
                *[
                    FadeIn(c)
                    for c in concept_group
                ],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )

        # Connecting line underneath, not through the boxes
        connection = Line(
            LEFT * 3.9 + DOWN * 1.15,
            RIGHT * 3.9 + DOWN * 1.15,
            color=SOFT,
            stroke_width=2,
        )

        self.play(
            Create(connection),
            run_time=0.6,
        )

        closing = Text(
            "A mathematical framework for reasoning about uncertainty.",
            font="Times New Roman",
            font_size=22,
            color=BLUE_TEXT,
        )

        closing.move_to(
            DOWN * 1.75
        )

        self.play(
            Write(closing),
            run_time=0.65,
        )

        self.wait(2.5)


if __name__ == "__main__":
    Figure301().render()
