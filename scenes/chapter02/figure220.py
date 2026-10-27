from manim import *


class Figure220(Scene):

    def construct(self):

        # ------------------------------------------------------------
        # CLEAN SCENE TRANSITION
        # Every conceptual block must be cleared before the next one.
        # ------------------------------------------------------------
        def clear_scene(*objects, run_time=0.55):
            visible = [obj for obj in objects if obj is not None]
            if visible:
                self.play(
                    *[FadeOut(obj) for obj in visible],
                    run_time=run_time,
                )
                self.remove(*visible)


        # ============================================================
        # CLEAN PAGE STYLE
        # ============================================================
        BG = WHITE

        self.camera.background_color = BG

        # ------------------------------------------------------------
        # HELPERS
        # ------------------------------------------------------------
        def write(obj, t=0.7):
            self.play(Write(obj), run_time=t)

        def flash(obj, color=BLUE_C):
            self.play(
                Indicate(
                    obj,
                    color=color,
                    scale_factor=1.04,
                    rate_func=there_and_back,
                ),
                run_time=0.45,
            )

        def remove(obj):
            self.play(FadeOut(obj), run_time=0.35)

        def section_pause(t=0.7):
            self.wait(t)

        # ============================================================
        # HEADER
        # ============================================================

        header = Text(
            "CHAPTER 2.  LINEAR ALGEBRA",
            font="Times New Roman",
            font_size=25,
            color=BLACK,
        )

        header.to_edge(UP, buff=0.25)

        line = Line(
            LEFT * 6.0 + UP * 0.05,
            RIGHT * 6.0 + UP * 0.05,
            color=BLACK,
            stroke_width=1.2,
        )

        line.next_to(header, DOWN, buff=0.08)

        write(header, 0.55)
        self.play(Create(line), run_time=0.35)

        # ============================================================
        # INTRODUCTION
        # ============================================================

        intro = Text(
            "Next, we need to choose the encoding matrix D.",
            font="Times New Roman",
            font_size=23,
            color=BLACK,
        )

        intro.move_to(UP * 2.75)

        write(intro, 0.6)
        section_pause(0.5)

        intro2 = Text(
            "We minimize the Frobenius norm of the reconstruction errors",
            font="Times New Roman",
            font_size=21,
            color=BLACK,
        )

        intro2.next_to(intro, DOWN, buff=0.22)

        write(intro2, 0.6)
        section_pause(0.7)

        # ============================================================
        # EQUATION 2.68
        # ============================================================

        eq68 = MathTex(
            r"D^{*}=\arg\min_{D}",
            font_size=29,
            color=BLACK,
        )

        eq68_detail = MathTex(
            r"\sqrt{\sum_{i,j}(x_j^{(i)}-r(x^{(i)})_j)^2}",
            font_size=27,
            color=BLACK,
        )

        eq68_constraint = MathTex(
            r"D^{T}D=I_l",
            font_size=27,
            color=BLACK,
        )

        eq68_group = VGroup(
            eq68,
            eq68_detail,
            eq68_constraint,
        ).arrange(
            RIGHT,
            buff=0.28,
        )

        eq68_group.scale_to_fit_width(10.5)
        eq68_group.move_to(UP * 1.55)

        num68 = Text(
            "(2.68)",
            font="Times New Roman",
            font_size=18,
            color=BLACK,
        )

        num68.next_to(
            eq68_group,
            RIGHT,
            buff=0.25,
        )

        self.play(
            Write(eq68),
            run_time=0.55,
        )

        self.play(
            Write(eq68_detail),
            run_time=0.65,
        )

        self.play(
            Write(eq68_constraint),
            run_time=0.45,
        )

        self.play(
            FadeIn(num68),
            run_time=0.25,
        )

        self.play(
            Indicate(
                eq68_group,
                scale_factor=1.03,
                color=BLUE_C,
            ),
            run_time=0.45,
        )

        self.wait(0.8)

        # ============================================================
        # TRANSITION TO l = 1
        # ============================================================

        text69 = Text(
            "For l = 1, D becomes a single vector d.",
            font="Times New Roman",
            font_size=21,
            color=BLACK,
        )

        text69.move_to(UP * 0.75)

        write(text69, 0.6)

        # ============================================================
        # EQUATION 2.69
        # ============================================================

        eq69 = MathTex(
            r"d^{*}=\arg\min_{d}"
            r"\sum_i"
            r"\left\|x^{(i)}-d d^{T}x^{(i)}\right\|_2^2"
            r"\quad"
            r"\|d\|_2=1.",
            font_size=25,
            color=BLACK,
        )

        eq69.move_to(UP * 0.05)

        num69 = Text(
            "(2.69)",
            font="Times New Roman",
            font_size=19,
            color=BLACK,
        )

        num69.next_to(eq69, RIGHT, buff=0.30)

        write(eq69, 0.8)
        self.play(FadeIn(num69), run_time=0.3)
        flash(eq69)

        section_pause(0.8)

        # ============================================================
        # COSMETIC REARRANGEMENT
        # ============================================================

        note70 = Text(
            "Rearranging the scalar gives the standard form:",
            font="Times New Roman",
            font_size=20,
            color=BLACK,
        )

        note70.move_to(DOWN * 0.65)

        write(note70, 0.55)

        eq70 = MathTex(
            r"d^{*}=\arg\min_{d}"
            r"\sum_i"
            r"\left\|x^{(i)}-d^{T}x^{(i)}d\right\|_2^2"
            r"\quad"
            r"\|d\|_2=1,",
            font_size=24,
            color=BLACK,
        )

        eq70.move_to(DOWN * 1.25)

        num70 = Text(
            "(2.70)",
            font="Times New Roman",
            font_size=19,
            color=BLACK,
        )

        num70.next_to(eq70, RIGHT, buff=0.30)

        write(eq70, 0.8)
        self.play(FadeIn(num70), run_time=0.3)
        flash(eq70)

        section_pause(0.7)

        # ============================================================
        # EQUATION 2.71
        # ============================================================

        eq71 = MathTex(
            r"d^{*}=\arg\min_{d}"
            r"\sum_i"
            r"\left\|x^{(i)}-x^{(i)T}dd\right\|_2^2"
            r"\quad"
            r"\|d\|_2=1.",
            font_size=24,
            color=BLACK,
        )

        eq71.move_to(DOWN * 2.00)

        num71 = Text(
            "(2.71)",
            font="Times New Roman",
            font_size=19,
            color=BLACK,
        )

        num71.next_to(eq71, RIGHT, buff=0.30)

        write(eq71, 0.8)
        self.play(FadeIn(num71), run_time=0.3)
        flash(eq71)

        section_pause(0.8)

        # ============================================================
        # DESIGN MATRIX X
        # ============================================================

        xtext = Text(
            "Now stack all example vectors into one design matrix X.",
            font="Times New Roman",
            font_size=20,
            color=BLACK,
        )

        xtext.move_to(DOWN * 2.72)

        write(xtext, 0.6)

        # ============================================================
        # --------------------------------------------------------
        # TRANSITION: remove the complete previous mathematical block
        # before introducing equation 2.72.
        # --------------------------------------------------------
        previous_objects = [
            obj for obj in self.mobjects
            if obj is not self.camera
        ]

        if previous_objects:
            self.play(
                *[FadeOut(obj) for obj in previous_objects],
                run_time=0.60,
            )

        self.clear()

        # EQUATION 2.72
        # ============================================================

        # EQUATION 2.72
        # Split into separate MathTex objects to avoid LaTeX issues.

        eq72_main = MathTex(
            r"d^{*}=\arg\min_{d}",
            font_size=28,
            color=BLACK,
        )

        eq72_norm = MathTex(
            r"\left\|X-Xdd^{T}\right\|_F^2",
            font_size=28,
            color=BLACK,
        )

        eq72_constraint = MathTex(
            r"d^{T}d=1",
            font_size=28,
            color=BLACK,
        )

        eq72 = VGroup(
            eq72_main,
            eq72_norm,
            eq72_constraint,
        ).arrange(
            RIGHT,
            buff=0.30,
        )

        eq72.scale_to_fit_width(10.2)
        eq72.move_to(ORIGIN)

        self.play(
            Write(eq72_main),
            run_time=0.45,
        )

        self.play(
            Write(eq72_norm),
            run_time=0.60,
        )

        self.play(
            Write(eq72_constraint),
            run_time=0.40,
        )

        self.play(
            Indicate(
                eq72,
                scale_factor=1.03,
                color=BLUE_C,
            ),
            run_time=0.45,
        )

        self.wait(0.8)

        # Keep safely inside frame
        if eq72.get_bottom()[1] < -3.55:
            eq72.shift(UP * 0.35)

        num72 = Text(
            "(2.72)",
            font="Times New Roman",
            font_size=19,
            color=BLACK,
        )

        num72.next_to(eq72, RIGHT, buff=0.30)

        write(eq72, 0.8)
        self.play(FadeIn(num72), run_time=0.3)
        flash(eq72)

        section_pause(0.8)

        # ============================================================
        # EQUATION 2.73
        # ============================================================

        # Move previous material upward slightly as the final equation
        # gets introduced, rather than allowing overlap.

        self.play(
            VGroup(
                intro,
                intro2,
                eq68,
                num68,
                text69,
                eq69,
                num69,
                note70,
                eq70,
                num70,
                eq71,
                num71,
                xtext,
                eq72,
                num72,
            ).animate.shift(UP * 0.15),
            run_time=0.35,
        )

        final_note = Text(
            "Ignoring the constraint for the moment,",
            font="Times New Roman",
            font_size=20,
            color=BLACK,
        )

        final_note.to_edge(DOWN, buff=0.72)

        write(final_note, 0.55)

        eq73 = MathTex(
            r"\arg\min_{d}"
            r"\left\|X-Xdd^{T}\right\|_F^2",
            font_size=28,
            color=BLACK,
        )

        eq73.next_to(final_note, DOWN, buff=0.28)

        num73 = Text(
            "(2.73)",
            font="Times New Roman",
            font_size=19,
            color=BLACK,
        )

        num73.next_to(eq73, RIGHT, buff=0.35)

        write(eq73, 0.75)
        self.play(FadeIn(num73), run_time=0.3)

        flash(eq73)

        section_pause(1.8)


if __name__ == "__main__":
    Figure220().render()
