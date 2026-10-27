from manim import *


class Figure222(Scene):

    def construct(self):

        # ============================================================
        # STYLE
        # ============================================================

        self.camera.background_color = WHITE

        BLACK_CLEAN = BLACK
        BLUE_ACCENT = BLUE_C
        GREEN_ACCENT = GREEN_C
        ORANGE_ACCENT = ORANGE

        # ============================================================
        # SAFE HELPERS
        # ============================================================

        def write(obj, runtime=0.6):
            self.play(
                Write(obj),
                run_time=runtime,
            )

        def remove_group(group):
            self.play(
                FadeOut(group),
                run_time=0.45,
            )
            self.remove(group)
            self.wait(0.2)

        # ============================================================
        # SECTION 1
        # ============================================================

        heading1 = Text(
            "Principal Components",
            font="Times New Roman",
            font_size=30,
            color=BLACK_CLEAN,
        )

        heading1.to_edge(
            UP,
            buff=0.30,
        )

        # Everything below this line is deliberately kept low.
        l_text = MathTex(
            r"l>1",
            font_size=34,
            color=BLUE_ACCENT,
        )

        l_text.move_to(
            UP * 1.25
        )

        statement = Text(
            "For multiple principal components,",
            font="Times New Roman",
            font_size=24,
            color=BLACK_CLEAN,
        )

        statement.move_to(
            UP * 0.65
        )

        d_matrix = MathTex(
            r"D="
            r"\left["
            r"d^{(1)}\;"
            r"d^{(2)}\;"
            r"\cdots\;"
            r"d^{(l)}"
            r"\right]",
            font_size=34,
            color=GREEN_ACCENT,
        )

        d_matrix.move_to(
            DOWN * 0.05
        )

        eigen1 = Text(
            "The columns of D are eigenvectors",
            font="Times New Roman",
            font_size=22,
            color=BLACK_CLEAN,
        )

        eigen1.move_to(
            DOWN * 0.75
        )

        eigen2 = Text(
            "corresponding to the largest eigenvalues.",
            font="Times New Roman",
            font_size=22,
            color=ORANGE_ACCENT,
        )

        eigen2.move_to(
            DOWN * 1.20
        )

        section1 = VGroup(
            heading1,
            l_text,
            statement,
            d_matrix,
            eigen1,
            eigen2,
        )

        write(heading1, 0.55)
        write(l_text, 0.4)
        write(statement, 0.5)
        write(d_matrix, 0.6)
        write(eigen1, 0.5)
        write(eigen2, 0.5)

        self.wait(1.1)

        remove_group(section1)

        # ============================================================
        # SECTION 2
        # ============================================================

        heading2 = Text(
            "Proof",
            font="Times New Roman",
            font_size=30,
            color=BLACK_CLEAN,
        )

        heading2.to_edge(
            UP,
            buff=0.30,
        )

        induction = MathTex(
            r"\text{Proof by induction}",
            font_size=32,
            color=BLUE_ACCENT,
        )

        induction.move_to(
            UP * 0.75
        )

        exercise = Text(
            "The complete proof can be derived as an exercise.",
            font="Times New Roman",
            font_size=22,
            color=BLACK_CLEAN,
        )

        exercise.move_to(
            DOWN * 0.05
        )

        section2 = VGroup(
            heading2,
            induction,
            exercise,
        )

        write(heading2, 0.5)
        write(induction, 0.55)
        write(exercise, 0.55)

        self.wait(1.1)

        remove_group(section2)

        # ============================================================
        # SECTION 3
        # ============================================================

        heading3 = Text(
            "Chapter 2 — Linear Algebra",
            font="Times New Roman",
            font_size=30,
            color=BLACK_CLEAN,
        )

        heading3.to_edge(
            UP,
            buff=0.30,
        )

        line1 = Text(
            "Linear algebra is a fundamental mathematical discipline",
            font="Times New Roman",
            font_size=22,
            color=BLACK_CLEAN,
        )

        line1.move_to(
            UP * 0.55
        )

        line2 = Text(
            "for understanding deep learning.",
            font="Times New Roman",
            font_size=22,
            color=BLACK_CLEAN,
        )

        line2.move_to(
            DOWN * 0.05
        )

        section3 = VGroup(
            heading3,
            line1,
            line2,
        )

        write(heading3, 0.55)
        write(line1, 0.55)
        write(line2, 0.5)

        self.wait(1.1)

        remove_group(section3)

        # ============================================================
        # SECTION 4 — NEXT CHAPTER
        # ============================================================

        heading4 = Text(
            "Next",
            font="Times New Roman",
            font_size=28,
            color=BLACK_CLEAN,
        )

        heading4.to_edge(
            UP,
            buff=0.30,
        )

        probability = Text(
            "Probability Theory",
            font="Times New Roman",
            font_size=40,
            color=GREEN_ACCENT,
        )

        probability.move_to(
            UP * 0.35
        )

        subtitle = Text(
            "Another key area of mathematics in machine learning",
            font="Times New Roman",
            font_size=21,
            color=BLACK_CLEAN,
        )

        subtitle.move_to(
            DOWN * 0.50
        )

        section4 = VGroup(
            heading4,
            probability,
            subtitle,
        )

        write(heading4, 0.5)
        write(probability, 0.7)
        write(subtitle, 0.5)

        self.wait(1.5)

        underline = Line(
            probability.get_left() + DOWN * 0.25,
            probability.get_right() + DOWN * 0.25,
            color=GREEN_ACCENT,
            stroke_width=2.5,
        )

        self.play(
            Create(underline),
            run_time=0.45,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure222().render()
