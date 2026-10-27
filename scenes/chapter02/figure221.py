from manim import *


class Figure221(Scene):

    def construct(self):

        # ============================================================
        # CLEAN WHITE STYLE
        # ============================================================

        BG = WHITE
        TXT = BLACK
        BLUE_ACCENT = BLUE_C
        GREEN_ACCENT = GREEN_C
        ORANGE_ACCENT = ORANGE

        self.camera.background_color = BG

        # ============================================================
        # HELPERS
        # ============================================================

        def make_equation(tex, number, size=28):

            eq = MathTex(
                tex,
                font_size=size,
                color=TXT,
            )

            num = Text(
                number,
                font="Times New Roman",
                font_size=18,
                color=TXT,
            )

            num.next_to(
                eq,
                RIGHT,
                buff=0.30,
            )

            group = VGroup(eq, num)

            group.scale_to_fit_width(11.6)

            return eq, num, group

        def show(eq, num, group):

            group.move_to(
                DOWN * 0.15
            )

            self.play(
                Write(eq),
                run_time=0.65,
            )

            self.play(
                FadeIn(num),
                run_time=0.25,
            )

            self.wait(0.9)

        def clear(group):

            self.play(
                FadeOut(group),
                run_time=0.45,
            )

            self.remove(group)

            self.wait(0.15)

        # ============================================================
        # TITLE
        # ============================================================

        title = Text(
            "Expanding the PCA Objective",
            font="Times New Roman",
            font_size=30,
            color=TXT,
        )

        title.to_edge(
            UP,
            buff=0.35,
        )

        self.play(
            Write(title),
            run_time=0.65,
        )

        self.wait(0.5)

        # ============================================================
        # 2.74
        # ============================================================

        eq74, num74, g74 = make_equation(
            r"\arg\min_d"
            r"\mathrm{Tr}"
            r"\left("
            r"(X-Xdd^{T})^{T}"
            r"(X-Xdd^{T})"
            r"\right)",
            "(2.74)",
            28,
        )

        show(eq74, num74, g74)
        clear(g74)

        # ============================================================
        # 2.75
        # ============================================================

        eq75, num75, g75 = make_equation(
            r"\arg\min_d"
            r"\mathrm{Tr}"
            r"\left("
            r"X^{T}X"
            r"-X^{T}Xdd^{T}"
            r"-dd^{T}X^{T}X"
            r"+dd^{T}X^{T}Xdd^{T}"
            r"\right)",
            "(2.75)",
            25,
        )

        show(eq75, num75, g75)
        clear(g75)

        # ============================================================
        # 2.76
        # ============================================================

        eq76, num76, g76 = make_equation(
            r"\arg\min_d"
            r"\mathrm{Tr}(X^{T}X)"
            r"-\mathrm{Tr}(X^{T}Xdd^{T})"
            r"-\mathrm{Tr}(dd^{T}X^{T}X)"
            r"+\mathrm{Tr}(dd^{T}X^{T}Xdd^{T})",
            "(2.76)",
            24,
        )

        show(eq76, num76, g76)
        clear(g76)

        # ============================================================
        # 2.77
        # ============================================================

        eq77, num77, g77 = make_equation(
            r"\arg\min_d"
            r"\left("
            r"-\mathrm{Tr}(X^{T}Xdd^{T})"
            r"-\mathrm{Tr}(dd^{T}X^{T}X)"
            r"+\mathrm{Tr}(dd^{T}X^{T}Xdd^{T})"
            r"\right)",
            "(2.77)",
            25,
        )

        show(eq77, num77, g77)
        clear(g77)

        # ============================================================
        # 2.78
        # ============================================================

        eq78, num78, g78 = make_equation(
            r"\arg\min_d"
            r"\left("
            r"-2\mathrm{Tr}(X^{T}Xdd^{T})"
            r"+\mathrm{Tr}(dd^{T}X^{T}Xdd^{T})"
            r"\right)",
            "(2.78)",
            27,
        )

        show(eq78, num78, g78)
        clear(g78)

        # ============================================================
        # 2.79
        # ============================================================

        eq79, num79, g79 = make_equation(
            r"\arg\min_d"
            r"\left("
            r"-2\mathrm{Tr}(X^{T}Xdd^{T})"
            r"+\mathrm{Tr}(X^{T}Xdd^{T}dd^{T})"
            r"\right)",
            "(2.79)",
            27,
        )

        show(eq79, num79, g79)
        clear(g79)

        # ============================================================
        # CONSTRAINT INTRODUCTION
        # ============================================================

        constraint = Text(
            "Reintroduce the constraint",
            font="Times New Roman",
            font_size=25,
            color=BLUE_ACCENT,
        )

        constraint.move_to(
            DOWN * 0.15
        )

        self.play(
            Write(constraint),
            run_time=0.55,
        )

        self.wait(0.45)

        # ============================================================
        # 2.80
        # ============================================================

        eq80 = MathTex(
            r"\arg\min_d"
            r"\left("
            r"-2\mathrm{Tr}(X^{T}Xdd^{T})"
            r"+\mathrm{Tr}(X^{T}Xdd^{T}dd^{T})"
            r"\right)",
            font_size=26,
            color=TXT,
        )

        constraint80 = MathTex(
            r"d^{T}d=1",
            font_size=30,
            color=ORANGE_ACCENT,
        )

        num80 = Text(
            "(2.80)",
            font="Times New Roman",
            font_size=18,
            color=TXT,
        )

        eq80.move_to(
            UP * 0.65
        )

        constraint80.next_to(
            eq80,
            DOWN,
            buff=0.45,
        )

        num80.next_to(
            constraint80,
            RIGHT,
            buff=0.30,
        )

        g80 = VGroup(
            eq80,
            constraint80,
            num80,
        )

        g80.scale_to_fit_width(11.5)

        self.play(
            Write(eq80),
            run_time=0.65,
        )

        self.play(
            Write(constraint80),
            run_time=0.4,
        )

        self.play(
            FadeIn(num80),
            run_time=0.2,
        )

        self.wait(1.0)

        self.play(
            FadeOut(g80),
            FadeOut(constraint),
            run_time=0.45,
        )

        # ============================================================
        # 2.81
        # ============================================================

        eq81, num81, g81 = make_equation(
            r"\arg\min_d"
            r"\left("
            r"-2\mathrm{Tr}(X^{T}Xdd^{T})"
            r"+\mathrm{Tr}(X^{T}Xdd^{T})"
            r"\right)",
            "(2.81)",
            27,
        )

        show(eq81, num81, g81)
        clear(g81)

        # ============================================================
        # 2.82
        # ============================================================

        eq82, num82, g82 = make_equation(
            r"\arg\min_d"
            r"\left("
            r"-\mathrm{Tr}(X^{T}Xdd^{T})"
            r"\right)",
            "(2.82)",
            29,
        )

        show(eq82, num82, g82)
        clear(g82)

        # ============================================================
        # 2.83
        # ============================================================

        eq83 = MathTex(
            r"\arg\max_d"
            r"\mathrm{Tr}(X^{T}Xdd^{T})",
            font_size=29,
            color=TXT,
        )

        constraint83 = MathTex(
            r"d^{T}d=1",
            font_size=29,
            color=ORANGE_ACCENT,
        )

        num83 = Text(
            "(2.83)",
            font="Times New Roman",
            font_size=18,
            color=TXT,
        )

        eq83.move_to(
            UP * 0.35
        )

        constraint83.next_to(
            eq83,
            DOWN,
            buff=0.45,
        )

        num83.next_to(
            constraint83,
            RIGHT,
            buff=0.30,
        )

        g83 = VGroup(
            eq83,
            constraint83,
            num83,
        )

        g83.scale_to_fit_width(11.5)

        self.play(
            Write(eq83),
            run_time=0.6,
        )

        self.play(
            Write(constraint83),
            run_time=0.4,
        )

        self.play(
            FadeIn(num83),
            run_time=0.2,
        )

        self.wait(1.0)

        self.play(
            FadeOut(g83),
            run_time=0.45,
        )

        # ============================================================
        # 2.84
        # ============================================================

        eq84 = MathTex(
            r"\arg\max_d"
            r"\mathrm{Tr}(d^{T}X^{T}Xd)",
            font_size=31,
            color=TXT,
        )

        constraint84 = MathTex(
            r"d^{T}d=1",
            font_size=30,
            color=ORANGE_ACCENT,
        )

        num84 = Text(
            "(2.84)",
            font="Times New Roman",
            font_size=18,
            color=TXT,
        )

        eq84.move_to(
            UP * 0.45
        )

        constraint84.next_to(
            eq84,
            DOWN,
            buff=0.45,
        )

        num84.next_to(
            constraint84,
            RIGHT,
            buff=0.30,
        )

        g84 = VGroup(
            eq84,
            constraint84,
            num84,
        )

        g84.scale_to_fit_width(11.4)

        self.play(
            Write(eq84),
            run_time=0.7,
        )

        self.play(
            Write(constraint84),
            run_time=0.4,
        )

        self.play(
            FadeIn(num84),
            run_time=0.2,
        )

        self.wait(1.0)

        # Highlight X^T X
        highlight = SurroundingRectangle(
            eq84,
            buff=0.12,
            color=GREEN_ACCENT,
            stroke_width=2,
        )

        self.play(
            Create(highlight),
            run_time=0.4,
        )

        self.wait(1.0)

        # ============================================================
        # CLEAN TRANSITION
        # ============================================================

        self.play(
            FadeOut(g84),
            FadeOut(highlight),
            run_time=0.55,
        )

        self.wait(0.2)

        # ============================================================
        # EIGENDECOMPOSITION CONCLUSION
        # ============================================================

        conclusion = Text(
            "Solved using eigendecomposition",
            font="Times New Roman",
            font_size=29,
            color=TXT,
        )

        conclusion.to_edge(
            UP,
            buff=0.45,
        )

        self.play(
            Write(conclusion),
            run_time=0.65,
        )

        self.wait(0.4)

        matrix = MathTex(
            r"X^{T}X",
            font_size=42,
            color=BLUE_ACCENT,
        )

        matrix.move_to(
            LEFT * 3.3 + DOWN * 0.25
        )

        arrow = Arrow(
            start=matrix.get_right() + RIGHT * 0.25,
            end=RIGHT * 0.65 + DOWN * 0.25,
            buff=0.05,
            stroke_width=2.5,
            color=TXT,
        )

        result = MathTex(
            r"d^{*}=v_{\max}",
            font_size=38,
            color=GREEN_ACCENT,
        )

        result.move_to(
            RIGHT * 2.8 + DOWN * 0.25
        )

        self.play(
            Write(matrix),
            run_time=0.55,
        )

        self.play(
            Create(arrow),
            run_time=0.4,
        )

        self.play(
            Write(result),
            run_time=0.6,
        )

        explanation = Text(
            "d* is the eigenvector corresponding to the largest eigenvalue",
            font="Times New Roman",
            font_size=20,
            color=TXT,
        )

        explanation.next_to(
            result,
            DOWN,
            buff=0.65,
        )

        self.play(
            FadeIn(explanation),
            run_time=0.45,
        )

        self.wait(2.0)


if __name__ == "__main__":
    Figure221().render()
