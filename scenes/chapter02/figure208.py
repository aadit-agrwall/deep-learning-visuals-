from manim import *

config.background_color = WHITE


class Figure208(Scene):

    # ==========================================================
    # HELPERS
    # ==========================================================

    def make_title(self, text):
        return Text(
            text,
            font_size=30,
            color=BLACK,
        ).to_edge(
            UP,
            buff=0.35,
        )

    def clear_scene(self, *groups, run_time=0.45):
        objects = []

        for group in groups:
            if group is not None:
                objects.extend(list(group))

        if objects:
            self.play(
                *[FadeOut(obj) for obj in objects],
                run_time=run_time,
            )

    def flash(self, mob, color=YELLOW, run_time=0.35):
        self.play(
            Indicate(
                mob,
                color=color,
                scale_factor=1.12,
            ),
            run_time=run_time,
        )

    def subtle_plane(self):
        """
        Subtle 2D grid.
        Visible enough to give spatial reference without
        overpowering the mathematical objects.
        """
        return NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5.2,
            background_line_style={
                "stroke_color": GRAY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.28,
            },
            axis_config={
                "color": GRAY_D,
                "stroke_width": 1.5,
            },
        )

    # ==========================================================
    # SCENE
    # ==========================================================

    def construct(self):

        # ======================================================
        # PHASE 1
        # COLUMN SPACE
        # ======================================================

        g1 = VGroup()

        title = self.make_title(
            "The column space of A"
        )

        self.play(
            Write(title),
            run_time=0.7,
        )

        matrix_A = MathTex(
            r"A",
            font_size=52,
            color=BLACK,
        )

        matrix_A.move_to(
            LEFT * 3.4
        )

        columns = MathTex(
            r"A_{:,1}",
            r"\quad",
            r"A_{:,2}",
            font_size=34,
            color=BLACK,
        )

        columns.next_to(
            matrix_A,
            RIGHT,
            buff=0.5,
        )

        equation = MathTex(
            r"A\mathbf{x}=\mathbf{b}",
            font_size=42,
            color=BLACK,
        )

        equation.move_to(
            DOWN * 0.4
        )

        explanation = Text(
            "Changing x moves b through combinations of the columns of A.",
            font_size=23,
            color=BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(matrix_A),
            run_time=0.5,
        )

        self.play(
            Write(columns),
            run_time=0.7,
        )

        self.flash(
            columns[0],
            color=YELLOW,
        )

        self.flash(
            columns[2],
            color=YELLOW,
        )

        self.play(
            Write(equation),
            Write(explanation),
            run_time=0.8,
        )

        g1.add(
            title,
            matrix_A,
            columns,
            equation,
            explanation,
        )

        self.wait(1)

        self.clear_scene(
            g1,
        )

        # ======================================================
        # PHASE 2
        # 3 x 2 MATRIX → 2D PLANE IN R3
        # ======================================================

        g2 = VGroup()

        title = self.make_title(
            "A 3×2 matrix spans at most a plane in R³"
        )

        self.play(
            Write(title),
            run_time=0.7,
        )

        # 3D coordinate system
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=5.8,
            y_length=5.8,
            z_length=4.8,
            axis_config={
                "color": GRAY_D,
                "stroke_width": 1.4,
            },
        )

        axes.shift(
            DOWN * 0.2
        )

        self.play(
            Create(axes),
            run_time=0.8,
        )

        # Semi-transparent plane
        plane = Surface(
            lambda u, v: axes.c2p(
                u,
                v,
                0.5 * u + 0.25 * v,
            ),
            u_range=[-2.4, 2.4],
            v_range=[-2.2, 2.2],
            resolution=(10, 10),
            fill_opacity=0.16,
            checkerboard_colors=[
                BLUE,
                BLUE,
            ],
            stroke_color=BLUE_E,
            stroke_opacity=0.35,
        )

        self.play(
            Create(plane),
            run_time=1.0,
        )

        plane_label = MathTex(
            r"\operatorname{Col}(A)",
            font_size=31,
            color=BLUE_E,
        )

        plane_label.move_to(
            axes.c2p(
                -1.8,
                -1.2,
                1.0,
            )
        )

        self.play(
            Write(plane_label),
            run_time=0.6,
        )

        dimension_text = MathTex(
            r"A\in\mathbb{R}^{3\times2}",
            font_size=30,
            color=BLACK,
        )

        dimension_text.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(dimension_text),
            run_time=0.7,
        )

        self.flash(
            plane,
            color=BLUE,
            run_time=0.45,
        )

        g2.add(
            title,
            axes,
            plane,
            plane_label,
            dimension_text,
        )

        self.wait(1)

        self.clear_scene(
            g2,
        )

        # ======================================================
        # PHASE 3
        # b ON / OFF THE PLANE
        # ======================================================

        g3 = VGroup()

        title = self.make_title(
            "A solution exists exactly when b lies in the column space"
        )

        self.play(
            Write(title),
            run_time=0.8,
        )

        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=5,
            axis_config={
                "color": GRAY_D,
                "stroke_width": 1.4,
            },
        )

        axes.shift(
            DOWN * 0.15
        )

        plane = Surface(
            lambda u, v: axes.c2p(
                u,
                v,
                0.5 * u + 0.25 * v,
            ),
            u_range=[-2.4, 2.4],
            v_range=[-2.2, 2.2],
            resolution=(10, 10),
            fill_opacity=0.13,
            checkerboard_colors=[
                BLUE,
                BLUE,
            ],
            stroke_color=BLUE_E,
            stroke_opacity=0.3,
        )

        self.play(
            Create(axes),
            Create(plane),
            run_time=0.9,
        )

        # Point on plane
        b_on_pos = axes.c2p(
            1.0,
            0.5,
            0.625,
        )

        b_on = Dot(
            b_on_pos,
            radius=0.11,
            color=GREEN,
        )

        b_on_label = MathTex(
            r"\mathbf{b}",
            font_size=31,
            color=GREEN_E,
        )

        b_on_label.next_to(
            b_on,
            RIGHT,
            buff=0.15,
        )

        on_text = Text(
            "b is reachable",
            font_size=24,
            color=GREEN_E,
        )

        on_text.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            FadeIn(b_on),
            Write(b_on_label),
            run_time=0.6,
        )

        self.flash(
            b_on,
            color=GREEN,
        )

        self.play(
            Write(on_text),
            run_time=0.6,
        )

        self.wait(0.8)

        # Move b away from plane explicitly.
        b_off_pos = axes.c2p(
            1.0,
            0.5,
            2.2,
        )

        off_text = Text(
            "b is outside the column space → no solution",
            font_size=24,
            color=RED_E,
        )

        off_text.to_edge(
            DOWN,
            buff=0.45,
        )

        self.flash(
            b_on,
            color=YELLOW,
        )

        self.play(
            b_on.animate.move_to(b_off_pos),
            Transform(
                b_on_label,
                MathTex(
                    r"\mathbf{b}",
                    font_size=31,
                    color=RED_E,
                ).move_to(
                    b_off_pos + RIGHT * 0.25
                ),
            ),
            run_time=1.0,
        )

        self.play(
            Transform(
                on_text,
                off_text,
            ),
            run_time=0.5,
        )

        self.flash(
            b_on,
            color=RED,
        )

        g3.add(
            title,
            axes,
            plane,
            b_on,
            b_on_label,
            on_text,
        )

        self.wait(1)

        self.clear_scene(
            g3,
        )

        # ======================================================
        # PHASE 4
        # n >= m IS NECESSARY
        # ======================================================

        g4 = VGroup()

        title = self.make_title(
            "To reach every point in Rᵐ, A needs at least m columns"
        )

        self.play(
            Write(title),
            run_time=0.8,
        )

        matrix_shape = MathTex(
            r"A\in\mathbb{R}^{m\times n}",
            font_size=42,
            color=BLACK,
        )

        matrix_shape.move_to(
            UP * 1.2
        )

        condition = MathTex(
            r"n\ge m",
            font_size=48,
            color=BLUE_E,
        )

        condition.move_to(
            DOWN * 0.05
        )

        explanation = Text(
            "Otherwise the column space cannot fill all of Rᵐ.",
            font_size=24,
            color=BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(matrix_shape),
            run_time=0.7,
        )

        self.play(
            Write(condition),
            run_time=0.7,
        )

        self.flash(
            condition,
            color=YELLOW,
        )

        self.play(
            Write(explanation),
            run_time=0.7,
        )

        g4.add(
            title,
            matrix_shape,
            condition,
            explanation,
        )

        self.wait(1)

        self.clear_scene(
            g4,
        )

        # ======================================================
        # PHASE 5
        # REDUNDANT COLUMNS
        # ======================================================

        g5 = VGroup()

        title = self.make_title(
            "But n ≥ m is not sufficient"
        )

        self.play(
            Write(title),
            run_time=0.7,
        )

        subtitle = Text(
            "Two identical columns add no new direction.",
            font_size=24,
            color=BLACK,
        )

        subtitle.move_to(
            UP * 1.35
        )

        self.play(
            Write(subtitle),
            run_time=0.6,
        )

        # Visible 2D grid
        grid = self.subtle_plane()

        grid.move_to(
            DOWN * 0.3
        )

        self.play(
            Create(grid),
            run_time=0.7,
        )

        origin = grid.c2p(
            0,
            0,
        )

        direction = grid.c2p(
            2.6,
            1.4,
        )

        line = Line(
            origin,
            direction,
            color=BLUE_E,
            stroke_width=4,
        )

        v1 = Arrow(
            origin,
            direction,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        v2 = Arrow(
            origin,
            direction,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        label1 = MathTex(
            r"A_{:,1}",
            font_size=28,
        ).next_to(
            direction,
            UP,
            buff=0.15,
        )

        label2 = MathTex(
            r"A_{:,2}",
            font_size=28,
        ).next_to(
            direction,
            DOWN,
            buff=0.15,
        )

        self.play(
            GrowArrow(v1),
            Write(label1),
            run_time=0.7,
        )

        self.flash(
            v1,
            color=YELLOW,
        )

        self.play(
            GrowArrow(v2),
            Write(label2),
            run_time=0.7,
        )

        self.flash(
            v2,
            color=RED,
        )

        redundant = MathTex(
            r"A_{:,2}=A_{:,1}",
            font_size=32,
            color=RED_E,
        )

        redundant.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(redundant),
            run_time=0.7,
        )

        g5.add(
            title,
            subtitle,
            grid,
            line,
            v1,
            v2,
            label1,
            label2,
            redundant,
        )

        self.wait(1)

        self.clear_scene(
            g5,
        )

        # ======================================================
        # PHASE 6
        # LINEAR INDEPENDENCE
        # ======================================================

        g6 = VGroup()

        title = self.make_title(
            "Linear independence means no redundant direction"
        )

        self.play(
            Write(title),
            run_time=0.8,
        )

        grid = self.subtle_plane()

        grid.move_to(
            DOWN * 0.3
        )

        self.play(
            Create(grid),
            run_time=0.6,
        )

        origin = grid.c2p(
            0,
            0,
        )

        end1 = grid.c2p(
            2.2,
            0.7,
        )

        end2 = grid.c2p(
            0.6,
            2.1,
        )

        v1 = Arrow(
            origin,
            end1,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        v2 = Arrow(
            origin,
            end2,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        label1 = MathTex(
            r"\mathbf{v}^{(1)}",
            font_size=29,
        ).next_to(
            end1,
            RIGHT,
            buff=0.15,
        )

        label2 = MathTex(
            r"\mathbf{v}^{(2)}",
            font_size=29,
        ).next_to(
            end2,
            UP,
            buff=0.15,
        )

        self.play(
            GrowArrow(v1),
            Write(label1),
            run_time=0.7,
        )

        self.flash(
            v1,
            color=YELLOW,
        )

        self.play(
            GrowArrow(v2),
            Write(label2),
            run_time=0.7,
        )

        self.flash(
            v2,
            color=YELLOW,
        )

        independent = Text(
            "v₂ is not a multiple of v₁",
            font_size=28,
            color=GREEN_E,
        )
        independent.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(independent),
            run_time=0.7,
        )

        self.flash(
            VGroup(v1, v2),
            color=GREEN,
        )

        g6.add(
            title,
            grid,
            v1,
            v2,
            label1,
            label2,
            independent,
        )

        self.wait(1)

        self.clear_scene(
            g6,
        )

        # ======================================================
        # PHASE 7
        # INVERSE CONDITIONS
        # ======================================================

        g7 = VGroup()

        title = self.make_title(
            "For A⁻¹ to exist, the matrix must be square and independent"
        )

        self.play(
            Write(title),
            run_time=0.8,
        )

        square = MathTex(
            r"m=n",
            font_size=48,
            color=BLUE_E,
        )

        independent = MathTex(
            r"\text{columns are linearly independent}",
            font_size=34,
            color=GREEN_E,
        )

        square.move_to(
            UP * 0.75
        )

        independent.move_to(
            DOWN * 0.25
        )

        self.play(
            Write(square),
            run_time=0.6,
        )

        self.flash(
            square,
            color=YELLOW,
        )

        self.play(
            Write(independent),
            run_time=0.8,
        )

        self.flash(
            independent,
            color=YELLOW,
        )

        result = MathTex(
            r"\boxed{A^{-1}\text{ exists}}",
            font_size=38,
            color=BLACK,
        )

        result.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(result),
            run_time=0.8,
        )

        g7.add(
            title,
            square,
            independent,
            result,
        )

        self.wait(1)

        self.clear_scene(
            g7,
        )

        # ======================================================
        # PHASE 8
        # SINGULAR VS INVERTIBLE
        # ======================================================

        g8 = VGroup()

        title = self.make_title(
            "Singular vs. invertible"
        )

        self.play(
            Write(title),
            run_time=0.7,
        )

        # Left: singular
        singular_matrix = MathTex(
            r"A_s="
            r"\begin{bmatrix}"
            r"1&2\\"
            r"2&4"
            r"\end{bmatrix}",
            font_size=36,
            color=BLACK,
        )

        singular_matrix.move_to(
            LEFT * 2.7
            + UP * 0.4
        )

        singular_label = Text(
            "Singular",
            font_size=25,
            color=RED_E,
        )

        singular_label.next_to(
            singular_matrix,
            DOWN,
            buff=0.35,
        )

        singular_reason = MathTex(
            r"A_{:,2}=2A_{:,1}",
            font_size=27,
            color=RED_E,
        )

        singular_reason.next_to(
            singular_label,
            DOWN,
            buff=0.25,
        )

        # Right: invertible
        invertible_matrix = MathTex(
            r"A_i="
            r"\begin{bmatrix}"
            r"1&0\\"
            r"0&1"
            r"\end{bmatrix}",
            font_size=36,
            color=BLACK,
        )

        invertible_matrix.move_to(
            RIGHT * 2.7
            + UP * 0.4
        )

        invertible_label = Text(
            "Invertible",
            font_size=25,
            color=GREEN_E,
        )

        invertible_label.next_to(
            invertible_matrix,
            DOWN,
            buff=0.35,
        )

        invertible_reason = MathTex(
            r"\text{independent columns}",
            font_size=27,
            color=GREEN_E,
        )

        invertible_reason.next_to(
            invertible_label,
            DOWN,
            buff=0.25,
        )

        self.play(
            Write(singular_matrix),
            run_time=0.7,
        )

        self.flash(
            singular_matrix,
            color=RED,
        )

        self.play(
            Write(singular_label),
            Write(singular_reason),
            run_time=0.6,
        )

        self.play(
            Write(invertible_matrix),
            run_time=0.7,
        )

        self.flash(
            invertible_matrix,
            color=GREEN,
        )

        self.play(
            Write(invertible_label),
            Write(invertible_reason),
            run_time=0.6,
        )

        g8.add(
            title,
            singular_matrix,
            singular_label,
            singular_reason,
            invertible_matrix,
            invertible_label,
            invertible_reason,
        )

        self.wait(1)

        self.clear_scene(
            g8,
        )

        # ======================================================
        # FINAL SUMMARY
        # ======================================================

        final = VGroup()

        title = self.make_title(
            "Conditions for a matrix inverse"
        )

        self.play(
            Write(title),
            run_time=0.7,
        )

        condition1 = MathTex(
            r"m=n",
            font_size=38,
            color=BLACK,
        )

        condition2 = MathTex(
            r"\text{columns are linearly independent}",
            font_size=32,
            color=BLACK,
        )

        condition3 = MathTex(
            r"\Longrightarrow",
            font_size=36,
            color=BLACK,
        )

        inverse = MathTex(
            r"A^{-1}\text{ exists}",
            font_size=40,
            color=GREEN_E,
        )

        condition1.move_to(
            LEFT * 3.3
            + UP * 0.5
        )

        condition2.move_to(
            LEFT * 2.0
            + DOWN * 0.55
        )

        condition3.move_to(
            RIGHT * 0.7
        )

        inverse.move_to(
            RIGHT * 2.5
        )

        self.play(
            Write(condition1),
            run_time=0.6,
        )

        self.flash(
            condition1,
            color=YELLOW,
        )

        self.play(
            Write(condition2),
            run_time=0.7,
        )

        self.flash(
            condition2,
            color=YELLOW,
        )

        self.play(
            Write(condition3),
            run_time=0.5,
        )

        self.play(
            Write(inverse),
            run_time=0.8,
        )

        self.flash(
            inverse,
            color=GREEN,
        )

        warning = Text(
            "If A is non-square or singular, matrix inversion cannot be used.",
            font_size=23,
            color=BLACK,
        )

        warning.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(warning),
            run_time=0.8,
        )

        final.add(
            title,
            condition1,
            condition2,
            condition3,
            inverse,
            warning,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure208().render()
