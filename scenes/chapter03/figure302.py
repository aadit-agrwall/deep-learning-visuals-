from manim import *


class Figure302(Scene):

    def construct(self):

        # ============================================================
        # THEME
        # ============================================================

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"

        self.camera.background_color = BG

        # ============================================================
        # HELPERS
        # ============================================================

        def txt(text, size=28, color=WHITE, weight=NORMAL):
            return Text(
                text,
                font="DejaVu Sans",
                font_size=size,
                color=color,
                weight=weight,
            )

        def show(obj, time=0.7):
            self.play(
                Write(obj),
                run_time=time,
            )

        def clear_scene():
            """
            Completely clear the current scene.
            This prevents objects from previous scenes
            from remaining underneath the next scene.
            """
            if self.mobjects:
                self.play(
                    *[
                        FadeOut(obj)
                        for obj in list(self.mobjects)
                    ],
                    run_time=0.5,
                )

            self.wait(0.25)

        # ============================================================
        # SCENE 1
        # CHAPTER TITLE
        # ============================================================

        chapter = txt(
            "CHAPTER 3",
            24,
            CYAN,
            BOLD,
        )

        heading = txt(
            "Probability and Information Theory",
            40,
            WHITE,
            BOLD,
        )

        section = txt(
            "3.1  Why Probability?",
            30,
            YELLOW,
        )

        chapter.to_edge(UP, buff=0.65)

        heading.next_to(
            chapter,
            DOWN,
            buff=0.25,
        )

        section.next_to(
            heading,
            DOWN,
            buff=0.35,
        )

        show(chapter, 0.45)
        show(heading, 0.75)
        show(section, 0.55)

        self.wait(1.2)

        clear_scene()

        # ============================================================
        # SCENE 2
        # WHY PROBABILITY?
        # ============================================================

        question = txt(
            "Why does machine learning need probability?",
            32,
            WHITE,
            BOLD,
        )

        question.to_edge(
            UP,
            buff=0.65,
        )

        show(question, 0.7)

        # ------------------------------------------------------------
        # LEFT — DETERMINISTIC WORLD
        # ------------------------------------------------------------

        deterministic_title = txt(
            "Deterministic world",
            27,
            CYAN,
            BOLD,
        )

        deterministic_title.move_to(
            LEFT * 3.25 + UP * 0.45
        )

        deterministic = txt(
            "instruction",
            24,
            MUTED,
        )

        deterministic.move_to(
            LEFT * 4.0 + DOWN * 0.35
        )

        deterministic_result = txt(
            "result",
            25,
            WHITE,
            BOLD,
        )

        deterministic_result.move_to(
            LEFT * 2.35 + DOWN * 0.35
        )

        deterministic_arrow = Arrow(
            deterministic.get_right(),
            deterministic_result.get_left(),
            buff=0.18,
            color=CYAN,
            stroke_width=3,
        )

        show(deterministic_title, 0.5)

        self.play(
            FadeIn(deterministic),
            GrowArrow(deterministic_arrow),
            FadeIn(deterministic_result),
            run_time=0.8,
        )

        # ------------------------------------------------------------
        # RIGHT — MACHINE LEARNING
        # ------------------------------------------------------------

        ml_title = txt(
            "Machine learning",
            27,
            YELLOW,
            BOLD,
        )

        ml_title.move_to(
            RIGHT * 3.25 + UP * 0.45
        )

        data = txt(
            "data",
            24,
            MUTED,
        )

        data.move_to(
            RIGHT * 2.35 + DOWN * 0.35
        )

        prediction = txt(
            "prediction",
            25,
            WHITE,
            BOLD,
        )

        prediction.move_to(
            RIGHT * 4.0 + DOWN * 0.35
        )

        ml_arrow = Arrow(
            data.get_right(),
            prediction.get_left(),
            buff=0.18,
            color=YELLOW,
            stroke_width=3,
        )

        show(ml_title, 0.5)

        self.play(
            FadeIn(data),
            GrowArrow(ml_arrow),
            FadeIn(prediction),
            run_time=0.8,
        )

        # ------------------------------------------------------------
        # CENTER — UNCERTAINTY
        # ------------------------------------------------------------

        uncertainty = txt(
            "uncertainty",
            27,
            RED,
            BOLD,
        )

        uncertainty.move_to(
            DOWN * 1.35
        )

        self.play(
            FadeIn(uncertainty),
            run_time=0.5,
        )

        self.wait(1.5)

        clear_scene()

        # ============================================================
        # SCENE 3
        # UNCERTAINTY
        # ============================================================

        title = txt(
            "Uncertainty is unavoidable",
            36,
            WHITE,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.75,
        )

        show(title, 0.65)

        statement = txt(
            "Many real-world quantities cannot be known with certainty.",
            25,
            MUTED,
        )

        statement.move_to(
            UP * 1.15
        )

        show(statement, 0.7)

        center = Dot(
            DOWN * 0.35,
            radius=0.10,
            color=YELLOW,
        )

        ring1 = Circle(
            radius=0.75,
            stroke_color=CYAN,
            stroke_width=2,
        )

        ring2 = Circle(
            radius=1.35,
            stroke_color=CYAN,
            stroke_width=2,
            stroke_opacity=0.55,
        )

        ring1.move_to(center)
        ring2.move_to(center)

        labels = txt(
            "possible outcomes",
            25,
            WHITE,
            BOLD,
        )

        labels.next_to(
            ring2,
            DOWN,
            buff=0.35,
        )

        self.play(
            FadeIn(center),
            Create(ring1),
            Create(ring2),
            run_time=0.8,
        )

        show(labels, 0.55)

        self.wait(1.2)

        clear_scene()

        # ============================================================
        # SCENE 4
        # SOURCE 1
        # ============================================================

        title = txt(
            "Source 1",
            25,
            CYAN,
            BOLD,
        )

        main = txt(
            "Inherent stochasticity",
            38,
            WHITE,
            BOLD,
        )

        description = txt(
            "Randomness exists inside the system itself.",
            27,
            MUTED,
        )

        title.to_edge(
            UP,
            buff=0.75,
        )

        main.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        description.next_to(
            main,
            DOWN,
            buff=0.35,
        )

        show(title, 0.45)
        show(main, 0.7)
        show(description, 0.65)

        dots = VGroup()

        positions = [
            LEFT * 2.5 + DOWN * 1.0,
            LEFT * 1.0 + DOWN * 0.3,
            RIGHT * 0.7 + DOWN * 1.1,
            RIGHT * 2.5 + DOWN * 0.1,
            LEFT * 1.8 + DOWN * 1.8,
            RIGHT * 1.5 + DOWN * 1.9,
        ]

        for position in positions:
            dots.add(
                Dot(
                    position,
                    radius=0.09,
                    color=CYAN,
                )
            )

        self.play(
            LaggedStart(
                *[
                    FadeIn(dot)
                    for dot in dots
                ],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )

        self.wait(1.1)

        clear_scene()

        # ============================================================
        # SCENE 5
        # SOURCE 2
        # ============================================================

        title = txt(
            "Source 2",
            25,
            YELLOW,
            BOLD,
        )

        main = txt(
            "Incomplete observability",
            38,
            WHITE,
            BOLD,
        )

        description = txt(
            "A deterministic system can appear random when information is hidden.",
            24,
            MUTED,
        )

        title.to_edge(
            UP,
            buff=0.75,
        )

        main.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        description.next_to(
            main,
            DOWN,
            buff=0.35,
        )

        show(title, 0.45)
        show(main, 0.7)
        show(description, 0.7)

        # ------------------------------------------------------------
        # THREE DOORS
        # ------------------------------------------------------------

        doors = VGroup()

        for i in range(3):

            door = Rectangle(
                width=1.55,
                height=2.5,
                stroke_color=WHITE,
                stroke_width=2,
            )

            number = txt(
                str(i + 1),
                27,
                WHITE,
                BOLD,
            )

            number.move_to(
                door.get_center()
            )

            doors.add(
                VGroup(
                    door,
                    number,
                )
            )

        doors.arrange(
            RIGHT,
            buff=0.7,
        )

        doors.move_to(
            DOWN * 1.15
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(door)
                    for door in doors
                ],
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )

        hidden = txt(
            "?",
            42,
            RED,
            BOLD,
        )

        hidden.move_to(
            doors[1].get_center()
        )

        self.play(
            FadeIn(hidden),
            run_time=0.45,
        )

        self.wait(1.2)

        clear_scene()

        # ============================================================
        # SCENE 6
        # SOURCE 3
        # ============================================================

        title = txt(
            "Source 3",
            25,
            GREEN,
            BOLD,
        )

        main = txt(
            "Incomplete modeling",
            38,
            WHITE,
            BOLD,
        )

        description = txt(
            "A model may discard information, creating uncertainty.",
            27,
            MUTED,
        )

        title.to_edge(
            UP,
            buff=0.75,
        )

        main.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        description.next_to(
            main,
            DOWN,
            buff=0.35,
        )

        show(title, 0.45)
        show(main, 0.7)
        show(description, 0.7)

        # ------------------------------------------------------------
        # INFORMATION → MODEL → PREDICTION
        # ------------------------------------------------------------

        information = RoundedRectangle(
            width=2.4,
            height=1.25,
            corner_radius=0.15,
            stroke_color=GREEN,
            stroke_width=2,
        )

        information_label = txt(
            "observed data",
            22,
            WHITE,
        )

        information_label.move_to(
            information.get_center()
        )

        information_group = VGroup(
            information,
            information_label,
        )

        information_group.move_to(
            LEFT * 3.5 + DOWN * 1.2
        )

        model = RoundedRectangle(
            width=2.4,
            height=1.25,
            corner_radius=0.15,
            stroke_color=CYAN,
            stroke_width=2,
        )

        model_label = txt(
            "simplified model",
            21,
            WHITE,
        )

        model_label.move_to(
            model.get_center()
        )

        model_group = VGroup(
            model,
            model_label,
        )

        model_group.move_to(
            DOWN * 1.2
        )

        prediction_box = RoundedRectangle(
            width=2.4,
            height=1.25,
            corner_radius=0.15,
            stroke_color=YELLOW,
            stroke_width=2,
        )

        prediction_label = txt(
            "prediction",
            22,
            WHITE,
            BOLD,
        )

        prediction_label.move_to(
            prediction_box.get_center()
        )

        prediction_group = VGroup(
            prediction_box,
            prediction_label,
        )

        prediction_group.move_to(
            RIGHT * 3.5 + DOWN * 1.2
        )

        arrow1 = Arrow(
            information_group.get_right(),
            model_group.get_left(),
            buff=0.15,
            color=WHITE,
        )

        arrow2 = Arrow(
            model_group.get_right(),
            prediction_group.get_left(),
            buff=0.15,
            color=WHITE,
        )

        self.play(
            FadeIn(information_group),
            GrowArrow(arrow1),
            FadeIn(model_group),
            GrowArrow(arrow2),
            FadeIn(prediction_group),
            run_time=1.2,
        )

        self.wait(1.3)

        clear_scene()

        # ============================================================
        # SCENE 7
        # FINAL SUMMARY
        # ============================================================

        final_title = txt(
            "Three sources of uncertainty",
            35,
            WHITE,
            BOLD,
        )

        final_title.to_edge(
            UP,
            buff=0.8,
        )

        show(final_title, 0.65)

        source1 = txt(
            "01   Inherent stochasticity",
            27,
            CYAN,
            BOLD,
        )

        source2 = txt(
            "02   Incomplete observability",
            27,
            YELLOW,
            BOLD,
        )

        source3 = txt(
            "03   Incomplete modeling",
            27,
            GREEN,
            BOLD,
        )

        summary = VGroup(
            source1,
            source2,
            source3,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.45,
        )

        summary.move_to(
            DOWN * 0.25
        )

        self.play(
            Write(source1),
            run_time=0.5,
        )

        self.play(
            Write(source2),
            run_time=0.5,
        )

        self.play(
            Write(source3),
            run_time=0.5,
        )

        self.wait(1.5)

        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Probability gives us a language\n"
            "for reasoning about uncertainty.",
            35,
            WHITE,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.25
        )

        self.play(
            Write(final),
            run_time=0.9,
        )

        self.wait(0.4)

        # Underline is generated AFTER the text is positioned.
        # This keeps it safely below both lines.
        line = Underline(
            final,
            color=CYAN,
            stroke_width=3,
            buff=0.18,
        )

        self.play(
            Create(line),
            run_time=0.45,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure302().render()
