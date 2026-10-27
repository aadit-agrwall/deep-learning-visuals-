from manim import *

config.background_color = WHITE


class Figure206(Scene):

    def flash(self, mob, color=YELLOW, run_time=0.45):
        self.play(
            Indicate(
                mob,
                color=color,
                scale_factor=1.15,
            ),
            run_time=run_time,
        )

    def matrix(
        self,
        values,
        center,
        cell_w=0.9,
        cell_h=0.7,
        font_size=30,
    ):
        rows = len(values)
        cols = len(values[0])

        entries = VGroup()

        for r in range(rows):
            for c in range(cols):

                entry = MathTex(
                    values[r][c],
                    font_size=font_size,
                    color=BLACK,
                )

                entry.move_to(
                    center
                    + RIGHT * (c - (cols - 1) / 2) * cell_w
                    + UP * ((rows - 1) / 2 - r) * cell_h
                )

                entries.add(entry)

        height = (rows - 1) * cell_h + 0.7
        width = (cols - 1) * cell_w + 0.7

        left = MathTex(
            r"\left[",
            font_size=font_size * 1.6,
            color=BLACK,
        )

        right = MathTex(
            r"\right]",
            font_size=font_size * 1.6,
            color=BLACK,
        )

        left.stretch_to_fit_height(height)
        right.stretch_to_fit_height(height)

        left.move_to(
            center + LEFT * (width / 2 + 0.25)
        )

        right.move_to(
            center + RIGHT * (width / 2 + 0.25)
        )

        return VGroup(
            left,
            entries,
            right,
        ), entries

    def construct(self):

        # ==========================================================
        # TITLE
        # ==========================================================

        title = Text(
            "Identity and Inverse Matrices",
            font_size=32,
            color=BLACK,
        )

        title.to_edge(
            UP,
            buff=0.3,
        )

        self.play(
            Write(title),
            run_time=0.9,
        )

        # ==========================================================
        # 1. SYSTEM OF LINEAR EQUATIONS
        # ==========================================================

        section = Text(
            "A system of equations",
            font_size=27,
            color=BLACK,
        )

        section.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        equations = MathTex(
            r"""
            \begin{aligned}
            A_{1,1}x_1+A_{1,2}x_2+\cdots+A_{1,n}x_n &= b_1\\
            A_{2,1}x_1+A_{2,2}x_2+\cdots+A_{2,n}x_n &= b_2\\
            &\vdots\\
            A_{m,1}x_1+A_{m,2}x_2+\cdots+A_{m,n}x_n &= b_m
            \end{aligned}
            """,
            font_size=27,
            color=BLACK,
        )

        equations.move_to(
            ORIGIN + DOWN * 0.45
        )

        self.play(
            Write(section),
            Write(equations),
            run_time=1.4,
        )

        self.flash(
            equations,
            color=YELLOW,
        )

        compact = MathTex(
            r"A\mathbf{x}=\mathbf{b}",
            font_size=40,
            color=BLACK,
        )

        compact.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            TransformFromCopy(
                equations,
                compact,
            ),
            run_time=1.2,
        )

        self.wait(1)

        self.play(
            FadeOut(
                section,
                equations,
                compact,
            )
        )

        # ==========================================================
        # 2. IDENTITY MATRIX
        # ==========================================================

        section = Text(
            "The identity matrix",
            font_size=29,
            color=BLACK,
        )

        section.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(section),
            run_time=0.7,
        )

        identity, identity_entries = self.matrix(
            [
                [r"1", r"0", r"0"],
                [r"0", r"1", r"0"],
                [r"0", r"0", r"1"],
            ],
            LEFT * 2.2 + DOWN * 0.35,
            cell_w=0.8,
            cell_h=0.75,
            font_size=32,
        )

        identity_label = MathTex(
            r"I_3=",
            font_size=36,
            color=BLACK,
        )

        identity_label.next_to(
            identity,
            LEFT,
            buff=0.3,
        )

        vector, vector_entries = self.matrix(
            [
                [r"x_1"],
                [r"x_2"],
                [r"x_3"],
            ],
            RIGHT * 2.3 + DOWN * 0.35,
            cell_w=0.8,
            cell_h=0.7,
            font_size=32,
        )

        x_label = MathTex(
            r"\mathbf{x}",
            font_size=35,
            color=BLACK,
        )

        x_label.next_to(
            vector,
            LEFT,
            buff=0.3,
        )

        self.play(
            FadeIn(identity),
            Write(identity_label),
            FadeIn(vector),
            Write(x_label),
        )

        self.flash(
            identity_entries,
            color=YELLOW,
        )

        arrow = Arrow(
            identity.get_right(),
            vector.get_left(),
            color=BLACK,
            stroke_width=3,
            buff=0.2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.7,
        )

        # Flash diagonal ones individually.
        for entry in [
            identity_entries[0],
            identity_entries[4],
            identity_entries[8],
        ]:
            self.flash(
                entry,
                color=GREEN,
                run_time=0.35,
            )

        identity_rule = MathTex(
            r"I_n\mathbf{x}=\mathbf{x}",
            font_size=38,
            color=BLACK,
        )

        identity_rule.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(identity_rule),
            run_time=0.8,
        )

        self.wait(1)

        self.play(
            FadeOut(
                section,
                identity,
                identity_label,
                vector,
                x_label,
                arrow,
                identity_rule,
            )
        )

        # ==========================================================
        # 3. DIAGONAL STRUCTURE
        # ==========================================================

        section = Text(
            "Only the main diagonal contains 1s",
            font_size=28,
            color=BLACK,
        )

        section.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        I3, entries = self.matrix(
            [
                [r"1", r"0", r"0"],
                [r"0", r"1", r"0"],
                [r"0", r"0", r"1"],
            ],
            ORIGIN + DOWN * 0.35,
            cell_w=1.0,
            cell_h=0.85,
            font_size=36,
        )

        self.play(
            Write(section),
            FadeIn(I3),
        )

        diagonal = VGroup(
            entries[0],
            entries[4],
            entries[8],
        )

        off_diagonal = VGroup(
            entries[1],
            entries[2],
            entries[3],
            entries[5],
            entries[6],
            entries[7],
        )

        self.flash(
            diagonal,
            color=GREEN,
            run_time=0.7,
        )

        self.flash(
            off_diagonal,
            color=RED,
            run_time=0.7,
        )

        caption = Text(
            "All other entries are zero.",
            font_size=24,
            color=BLACK,
        )

        caption.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(caption),
            run_time=0.7,
        )

        self.wait(1)

        self.play(
            FadeOut(
                section,
                I3,
                caption,
            )
        )

        # ==========================================================
        # 4. MATRIX INVERSE
        # ==========================================================

        section = Text(
            "The matrix inverse",
            font_size=29,
            color=BLACK,
        )

        section.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        A, A_entries = self.matrix(
            [
                [r"a_{11}", r"a_{12}"],
                [r"a_{21}", r"a_{22}"],
            ],
            LEFT * 2.6 + DOWN * 0.3,
            font_size=30,
        )

        inverse, inverse_entries = self.matrix(
            [
                [r"?", r"?"],
                [r"?", r"?"],
            ],
            RIGHT * 0.2 + DOWN * 0.3,
            font_size=30,
        )

        I2, I2_entries = self.matrix(
            [
                [r"1", r"0"],
                [r"0", r"1"],
            ],
            RIGHT * 3.0 + DOWN * 0.3,
            font_size=32,
        )

        inv_label = MathTex(
            r"A^{-1}",
            font_size=34,
        )

        inv_label.next_to(
            inverse,
            LEFT,
            buff=0.3,
        )

        equals1 = MathTex(
            r"=",
            font_size=36,
        )

        equals1.move_to(
            RIGHT * 1.55 + DOWN * 0.3
        )

        self.play(
            Write(section),
            FadeIn(A),
            Write(inv_label),
            FadeIn(inverse),
            Write(equals1),
            FadeIn(I2),
        )

        self.flash(
            A,
            color=YELLOW,
        )

        self.play(
            Transform(
                inverse_entries,
                VGroup(
                    MathTex(r"p", font_size=30),
                    MathTex(r"q", font_size=30),
                    MathTex(r"r", font_size=30),
                    MathTex(r"s", font_size=30),
                ),
            ),
            run_time=0.8,
        )

        inverse_rule = MathTex(
            r"A^{-1}A=I_n",
            font_size=40,
            color=BLACK,
        )

        inverse_rule.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(inverse_rule),
            run_time=0.9,
        )

        self.wait(1)

        self.play(
            FadeOut(
                section,
                A,
                inv_label,
                inverse,
                equals1,
                I2,
                inverse_rule,
            )
        )

        # ==========================================================
        # 5. SOLVING Ax = b
        # ==========================================================

        section = Text(
            "Using the inverse to solve Ax = b",
            font_size=29,
            color=BLACK,
        )

        section.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(section),
            run_time=0.7,
        )

        eq1 = MathTex(
            r"A\mathbf{x}=\mathbf{b}",
            font_size=42,
            color=BLACK,
        )

        eq1.move_to(
            ORIGIN + UP * 1.55
        )

        self.play(
            Write(eq1),
            run_time=0.8,
        )

        self.flash(
            eq1,
            color=YELLOW,
        )

        # ==========================================================
        # STEP 1 -> STEP 2
        # ==========================================================

        eq2 = MathTex(
            r"A^{-1}A\mathbf{x}=A^{-1}\mathbf{b}",
            font_size=38,
            color=BLACK,
        )

        eq2.move_to(
            ORIGIN + UP * 0.65
        )

        self.play(
            TransformFromCopy(
                eq1,
                eq2,
            ),
            run_time=1,
        )

        # Explicitly introduce A^-1 on both sides.
        inverse_left = MathTex(
            r"A^{-1}",
            font_size=38,
            color=BLACK,
        )

        inverse_right = MathTex(
            r"A^{-1}",
            font_size=38,
            color=BLACK,
        )

        inverse_left.move_to(
            eq2.get_left() + RIGHT * 0.1
        )

        inverse_right.move_to(
            eq2.get_right() + LEFT * 0.1
        )

        self.flash(
            eq2,
            color=YELLOW,
        )

        # ==========================================================
        # STEP 2 -> STEP 3
        # ==========================================================

        eq3 = MathTex(
            r"I_n\mathbf{x}=A^{-1}\mathbf{b}",
            font_size=40,
            color=BLACK,
        )

        eq3.move_to(
            ORIGIN + DOWN * 0.25
        )

        self.flash(
            eq2,
            color=YELLOW,
        )

        self.play(
            TransformMatchingTex(
                eq2,
                eq3,
            ),
            run_time=1.1,
        )

        # Explicitly emphasize A^-1 A -> I
        identity_part = MathTex(
            r"A^{-1}A",
            font_size=40,
            color=GREEN,
        )

        identity_part.move_to(
            eq3.get_left() + RIGHT * 0.85
        )

        self.flash(
            identity_part,
            color=GREEN,
            run_time=0.6,
        )

        # ==========================================================
        # STEP 3 -> STEP 4
        # ==========================================================

        eq4 = MathTex(
            r"\mathbf{x}=A^{-1}\mathbf{b}",
            font_size=42,
            color=BLACK,
        )

        eq4.move_to(
            ORIGIN + DOWN * 1.15
        )

        self.flash(
            eq3,
            color=YELLOW,
        )

        self.play(
            TransformMatchingTex(
                eq3,
                eq4,
            ),
            run_time=1.1,
        )

        final_box = SurroundingRectangle(
            eq4,
            color=GREEN,
            buff=0.2,
            stroke_width=2.5,
        )

        self.play(
            Create(final_box),
            run_time=0.7,
        )

        final_caption = Text(
            "The solution",
            font_size=25,
            color=BLACK,
        )

        final_caption.next_to(
            final_box,
            DOWN,
            buff=0.25,
        )

        self.play(
            Write(final_caption),
            run_time=0.6,
        )

        self.wait(2)

        # ==========================================================
        # FINAL IDENTITY MATRIX FIGURE
        # ==========================================================

        self.play(
            FadeOut(
                section,
                eq1,
                eq4,
                final_box,
                final_caption,
            )
        )

        final_title = Text(
            "Example: the 3 × 3 identity matrix",
            font_size=29,
            color=BLACK,
        )

        final_title.next_to(
            title,
            DOWN,
            buff=0.4,
        )

        final_I, final_entries = self.matrix(
            [
                [r"1", r"0", r"0"],
                [r"0", r"1", r"0"],
                [r"0", r"0", r"1"],
            ],
            ORIGIN + DOWN * 0.35,
            cell_w=1.0,
            cell_h=0.85,
            font_size=38,
        )

        final_label = MathTex(
            r"I_3=",
            font_size=40,
            color=BLACK,
        )

        final_label.next_to(
            final_I,
            LEFT,
            buff=0.3,
        )

        self.play(
            Write(final_title),
            FadeIn(final_I),
            Write(final_label),
        )

        for entry in final_entries:
            self.flash(
                entry,
                color=GREEN if entry.get_tex_string() == "1" else YELLOW,
                run_time=0.25,
            )

        self.wait(2)
