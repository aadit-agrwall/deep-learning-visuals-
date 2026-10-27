from manim import *
import numpy as np


class Figure213(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        BLACK_TEXT = BLACK
        BLUE_CURVE = BLUE_D
        GRID_COLOR = GRAY_B
        HIGHLIGHT = YELLOW

        # ============================================================
        # TITLE
        # ============================================================

        title = Text(
            "Effect of eigenvectors and eigenvalues",
            font_size=26,
            color=BLACK_TEXT,
        )

        title.to_edge(UP, buff=0.45)

        self.play(
            Write(title),
            run_time=0.8,
        )

        # ============================================================
        # TWO GRAPH PANELS
        # ============================================================

        left_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.5,
            y_length=4.2,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
                "include_ticks": True,
                "include_numbers": True,
                "font_size": 15,
            },
            tips=False,
        )

        right_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.5,
            y_length=4.2,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
                "include_ticks": True,
                "include_numbers": True,
                "font_size": 15,
            },
            tips=False,
        )

        left_axes.move_to(
            LEFT * 2.45 + DOWN * 0.45
        )

        right_axes.move_to(
            RIGHT * 2.45 + DOWN * 0.45
        )

        self.play(
            Create(left_axes),
            Create(right_axes),
            run_time=1.0,
        )

        # ============================================================
        # LIGHT GRID
        # ============================================================

        def make_grid(ax):

            lines = VGroup()

            for x in range(-2, 3):
                line = Line(
                    ax.c2p(x, -3),
                    ax.c2p(x, 3),
                    color=GRID_COLOR,
                    stroke_width=0.7,
                    stroke_opacity=0.35,
                )
                lines.add(line)

            for y in range(-2, 3):
                line = Line(
                    ax.c2p(-3, y),
                    ax.c2p(3, y),
                    color=GRID_COLOR,
                    stroke_width=0.7,
                    stroke_opacity=0.35,
                )
                lines.add(line)

            return lines

        left_grid = make_grid(left_axes)
        right_grid = make_grid(right_axes)

        self.play(
            FadeIn(left_grid),
            FadeIn(right_grid),
            run_time=0.5,
        )

        # ============================================================
        # PANEL TITLES
        # ============================================================

        before = Text(
            "Before multiplication",
            font_size=22,
            color=BLACK_TEXT,
        )

        after = Text(
            "After multiplication",
            font_size=22,
            color=BLACK_TEXT,
        )

        before.next_to(
            left_axes,
            UP,
            buff=0.12,
        )

        after.next_to(
            right_axes,
            UP,
            buff=0.12,
        )

        self.play(
            Write(before),
            Write(after),
            run_time=0.7,
        )

        # ============================================================
        # AXIS LABELS
        # ============================================================

        lx = MathTex(
            r"x_0",
            font_size=20,
            color=BLACK_TEXT,
        )

        ly = MathTex(
            r"x_1",
            font_size=20,
            color=BLACK_TEXT,
        )

        rx = MathTex(
            r"x'_0",
            font_size=20,
            color=BLACK_TEXT,
        )

        ry = MathTex(
            r"x'_1",
            font_size=20,
            color=BLACK_TEXT,
        )

        lx.next_to(left_axes.x_axis, DOWN, buff=0.12)
        ly.next_to(left_axes.y_axis, LEFT, buff=0.12)

        rx.next_to(right_axes.x_axis, DOWN, buff=0.12)
        ry.next_to(right_axes.y_axis, LEFT, buff=0.12)

        self.play(
            Write(lx),
            Write(ly),
            Write(rx),
            Write(ry),
            run_time=0.6,
        )

        # ============================================================
        # UNIT CIRCLE
        # ============================================================

        def circle_point(t):
            return left_axes.c2p(
                np.cos(t),
                np.sin(t),
            )

        circle = ParametricFunction(
            circle_point,
            t_range=[0, TAU],
            color=BLUE_CURVE,
            stroke_width=3,
        )

        self.play(
            Create(circle),
            run_time=1.1,
        )

        # ============================================================
        # EIGENVECTORS
        # ============================================================

        v1_direction = np.array([0.78, 0.62])
        v2_direction = np.array([0.78, -0.62])

        v1_end = left_axes.c2p(
            v1_direction[0],
            v1_direction[1],
        )

        v2_end = left_axes.c2p(
            v2_direction[0],
            v2_direction[1],
        )

        origin_left = left_axes.c2p(0, 0)

        v1 = Arrow(
            origin_left,
            v1_end,
            buff=0,
            color=BLACK,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.15,
        )

        v2 = Arrow(
            origin_left,
            v2_end,
            buff=0,
            color=BLACK,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.15,
        )

        v1_label = MathTex(
            r"\mathbf{v}^{(1)}",
            font_size=20,
            color=BLACK_TEXT,
        )

        v2_label = MathTex(
            r"\mathbf{v}^{(2)}",
            font_size=20,
            color=BLACK_TEXT,
        )

        v1_label.next_to(
            v1.get_end(),
            RIGHT,
            buff=0.08,
        )

        v2_label.next_to(
            v2.get_end(),
            RIGHT,
            buff=0.08,
        )

        self.play(
            GrowArrow(v1),
            GrowArrow(v2),
            Write(v1_label),
            Write(v2_label),
            run_time=0.9,
        )

        # ============================================================
        # FLASH EIGENVECTORS BEFORE TRANSFORMATION
        # ============================================================

        self.play(
            Indicate(
                v1,
                color=HIGHLIGHT,
                scale_factor=1.08,
            ),
            run_time=0.55,
        )

        self.play(
            Indicate(
                v2,
                color=HIGHLIGHT,
                scale_factor=1.08,
            ),
            run_time=0.55,
        )

        # ============================================================
        # TRANSFORMATION MATRIX
        #
        # Choose eigen-directions:
        # v1 -> scale 2.6
        # v2 -> scale 0.75
        # ============================================================

        lambda_1 = 2.6
        lambda_2 = 0.75

        # Construct orthonormal basis
        e1 = v1_direction / np.linalg.norm(v1_direction)
        e2 = v2_direction / np.linalg.norm(v2_direction)

        # Ellipse using the two eigen-directions
        def transformed_point(t):

            u = np.array([
                np.cos(t),
                np.sin(t),
            ])

            # Express u approximately in orthonormal basis
            # using a clean rotation basis.
            theta = np.arctan2(
                v1_direction[1],
                v1_direction[0],
            )

            c = np.cos(theta)
            s = np.sin(theta)

            # Rotated coordinates
            r1 = c * u[0] + s * u[1]
            r2 = -s * u[0] + c * u[1]

            result = (
                lambda_1 * r1 * np.array([c, s])
                +
                lambda_2 * r2 * np.array([-s, c])
            )

            return right_axes.c2p(
                result[0],
                result[1],
            )

        ellipse = ParametricFunction(
            transformed_point,
            t_range=[0, TAU],
            color=BLUE_CURVE,
            stroke_width=3,
        )

        # ============================================================
        # TRANSFORMED EIGENVECTORS
        # ============================================================

        right_origin = right_axes.c2p(0, 0)

        rv1_end = right_axes.c2p(
            v1_direction[0] * lambda_1,
            v1_direction[1] * lambda_1,
        )

        rv2_end = right_axes.c2p(
            v2_direction[0] * lambda_2,
            v2_direction[1] * lambda_2,
        )

        rv1 = Arrow(
            right_origin,
            rv1_end,
            buff=0,
            color=BLACK,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.10,
        )

        rv2 = Arrow(
            right_origin,
            rv2_end,
            buff=0,
            color=BLACK,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.16,
        )

        rv1_label = MathTex(
            r"\lambda_1\mathbf{v}^{(1)}",
            font_size=18,
            color=BLACK_TEXT,
        )

        rv2_label = MathTex(
            r"\lambda_2\mathbf{v}^{(2)}",
            font_size=18,
            color=BLACK_TEXT,
        )

        rv1_label.next_to(
            rv1.get_end(),
            RIGHT,
            buff=0.05,
        )

        rv2_label.next_to(
            rv2.get_end(),
            RIGHT,
            buff=0.08,
        )

        # ============================================================
        # ACTUAL MORPH
        # ============================================================

        self.play(
            Indicate(
                circle,
                color=HIGHLIGHT,
                scale_factor=1.02,
            ),
            run_time=0.45,
        )

        # Circle physically moves across to right panel
        moving_circle = circle.copy()

        self.add(moving_circle)

        # Move circle center from left origin to right origin
        shift_vector = right_axes.c2p(0, 0) - left_axes.c2p(0, 0)

        self.play(
            moving_circle.animate.shift(shift_vector),
            run_time=0.7,
        )

        # Then transform it into ellipse
        self.play(
            Transform(
                moving_circle,
                ellipse,
            ),
            run_time=2.0,
        )

        self.remove(moving_circle)
        self.add(ellipse)

        # ============================================================
        # MOVE EIGENVECTORS EXPLICITLY
        # ============================================================

        v1_target = rv1.copy()
        v2_target = rv2.copy()

        self.play(
            Transform(
                v1,
                v1_target,
            ),
            Transform(
                v2,
                v2_target,
            ),
            Transform(
                v1_label,
                MathTex(
                    r"\lambda_1\mathbf{v}^{(1)}",
                    font_size=18,
                    color=BLACK_TEXT,
                ).move_to(rv1_label),
            ),
            Transform(
                v2_label,
                MathTex(
                    r"\lambda_2\mathbf{v}^{(2)}",
                    font_size=18,
                    color=BLACK_TEXT,
                ).move_to(rv2_label),
            ),
            run_time=1.5,
        )

        # ============================================================
        # FINAL HIGHLIGHT
        # ============================================================

        self.play(
            Indicate(
                ellipse,
                color=HIGHLIGHT,
                scale_factor=1.015,
            ),
            run_time=0.7,
        )

        # ============================================================
        # EIGENDECOMPOSITION EQUATION
        # ============================================================

        equation = MathTex(
            r"A = V\,\operatorname{diag}(\lambda)\,V^{-1}",
            font_size=31,
            color=BLACK_TEXT,
        )

        equation.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(equation),
            run_time=0.9,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure213().render()
