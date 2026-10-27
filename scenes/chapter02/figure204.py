from manim import *

config.background_color = WHITE


class Figure204(Scene):

    def make_matrix(self, values, center, cell_w=1.05, cell_h=0.8, font_size=34):
        """
        Creates a matrix from individually positioned MathTex elements.
        Returns:
            group, entries, bracket_left, bracket_right
        """

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

                x = (c - (cols - 1) / 2) * cell_w
                y = ((rows - 1) / 2 - r) * cell_h

                entry.move_to(
                    center + RIGHT * x + UP * y
                )

                entries.add(entry)

        total_height = (rows - 1) * cell_h + 0.9
        center_y = center[1]

        left_bracket = MathTex(
            r"\left[",
            font_size=font_size * 1.5,
            color=BLACK,
        )

        right_bracket = MathTex(
            r"\right]",
            font_size=font_size * 1.5,
            color=BLACK,
        )

        left_bracket.stretch_to_fit_height(total_height)
        right_bracket.stretch_to_fit_height(total_height)

        left_bracket.move_to(
            center + LEFT * ((cols - 1) * cell_w / 2 + 0.55)
        )

        right_bracket.move_to(
            center + RIGHT * ((cols - 1) * cell_w / 2 + 0.55)
        )

        group = VGroup(
            left_bracket,
            entries,
            right_bracket,
        )

        return group, entries, left_bracket, right_bracket


    def construct(self):

        # ==========================================================
        # TITLE
        # ==========================================================

        title = Text(
            "Transpose of a Matrix",
            font_size=30,
            color=BLACK,
        )

        title.to_edge(
            UP,
            buff=0.3,
        )

        self.play(
            Write(title),
            run_time=1.0,
        )

        # ==========================================================
        # ORIGINAL MATRIX
        #
        # A =
        #
        # [ a11  a12 ]
        # [ a21  a22 ]
        # [ a31  a32 ]
        # ==========================================================

        original_values = [
            [r"a_{1,1}", r"a_{1,2}"],
            [r"a_{2,1}", r"a_{2,2}"],
            [r"a_{3,1}", r"a_{3,2}"],
        ]

        original_center = LEFT * 3.0 + DOWN * 0.45

        original, source_entries, left_bracket, right_bracket = (
            self.make_matrix(
                original_values,
                original_center,
                cell_w=1.1,
                cell_h=0.85,
                font_size=31,
            )
        )

        a_label = MathTex(
            r"A=",
            font_size=34,
            color=BLACK,
        )

        a_label.next_to(
            original,
            LEFT,
            buff=0.35,
        )

        self.play(
            FadeIn(original),
            Write(a_label),
            run_time=1.0,
        )

        # ==========================================================
        # TRANSPOSE TARGET
        #
        # [ a11  a21  a31 ]
        # [ a12  a22  a32 ]
        # ==========================================================

        target_values = [
            [r"a_{1,1}", r"a_{2,1}", r"a_{3,1}"],
            [r"a_{1,2}", r"a_{2,2}", r"a_{3,2}"],
        ]

        target_center = RIGHT * 3.0 + DOWN * 0.45

        target, target_entries, target_left, target_right = (
            self.make_matrix(
                target_values,
                target_center,
                cell_w=0.95,
                cell_h=0.85,
                font_size=31,
            )
        )

        at_label = MathTex(
            r"A^T=",
            font_size=34,
            color=BLACK,
        )

        at_label.next_to(
            target,
            LEFT,
            buff=0.35,
        )

        # Only show target brackets initially.
        self.play(
            FadeIn(target_left),
            FadeIn(target_right),
            Write(at_label),
            run_time=0.8,
        )

        # ==========================================================
        # HIDE TARGET ENTRIES
        # They will be represented by the moving source entries.
        # ==========================================================

        target_entries.set_opacity(0)

        # ==========================================================
        # TRANSPOSE MAPPING
        #
        # a11 -> a11
        # a12 -> a12
        #
        # a21 -> a21
        # a22 -> a22
        #
        # a31 -> a31
        # a32 -> a32
        #
        # The important part is that ROWS become COLUMNS.
        # ==========================================================

        source_to_target = [
            (0, 0),  # a11 -> row 1, col 1
            (1, 0),  # a12 -> row 2, col 1

            (2, 1),  # a21 -> row 1, col 2
            (3, 1),  # a22 -> row 2, col 2

            (4, 2),  # a31 -> row 1, col 3
            (5, 2),  # a32 -> row 2, col 3
        ]

        # ==========================================================
        # FLASH + MOVE EACH ELEMENT
        # ==========================================================

        for source_index, target_index in source_to_target:

            source = source_entries[source_index]
            target_position = target_entries[target_index].get_center()

            # Flash the element that is about to move.
            self.play(
                Indicate(
                    source,
                    color=YELLOW,
                    scale_factor=1.25,
                ),
                run_time=0.45,
            )

            # Actual movement.
            self.play(
                source.animate.move_to(
                    target_position
                ),
                run_time=0.9,
                rate_func=smooth,
            )

        # ==========================================================
        # FINAL TRANSPOSE EQUATION
        # ==========================================================

        equation = MathTex(
            r"(A^T)_{i,j}=A_{j,i}",
            font_size=32,
            color=BLACK,
        )

        equation.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(equation),
            run_time=1.2,
        )

        # ==========================================================
        # FINAL EMPHASIS
        # ==========================================================

        self.play(
            Indicate(
                equation,
                color=YELLOW,
                scale_factor=1.05,
            ),
            run_time=0.8,
        )

        self.wait(2)
