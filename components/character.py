from manim import *


class MathCharacter(VGroup):
    def __init__(self, symbol, color=BLUE, **kwargs):
        super().__init__(**kwargs)

        body = MathTex(symbol, font_size=96, color=color)

        left_eye = Dot(radius=0.05, color=BLACK)
        right_eye = Dot(radius=0.05, color=BLACK)

        left_eye.move_to(body.get_center() + LEFT * 0.18 + UP * 0.22)
        right_eye.move_to(body.get_center() + RIGHT * 0.18 + UP * 0.22)

        smile = Arc(
            radius=0.12,
            angle=PI / 1.2,
            start_angle=-5 * PI / 6,
            color=BLACK,
            stroke_width=3,
        )
        smile.move_to(body.get_center() + DOWN * 0.08)

        # Arms
        self.left_arm = Line(
            body.get_left() + UP * 0.15,
            body.get_left() + LEFT * 0.4 + DOWN * 0.1,
            color=color,
            stroke_width=5,
        )

        self.right_arm = Line(
            body.get_right() + UP * 0.15,
            body.get_right() + RIGHT * 0.4 + DOWN * 0.1,
            color=color,
            stroke_width=5,
        )

        # Legs
        self.left_leg = Line(
            body.get_bottom() + LEFT * 0.08,
            body.get_bottom() + LEFT * 0.18 + DOWN * 0.4,
            color=color,
            stroke_width=5,
        )

        self.right_leg = Line(
            body.get_bottom() + RIGHT * 0.08,
            body.get_bottom() + RIGHT * 0.18 + DOWN * 0.4,
            color=color,
            stroke_width=5,
        )

        self.add(
            body,
            left_eye,
            right_eye,
            smile,
            self.left_arm,
            self.right_arm,
            self.left_leg,
            self.right_leg,
        )

    def wave(self, scene):
        scene.play(
            Rotate(
                self.right_arm,
                angle=35 * DEGREES,
                about_point=self.right_arm.get_start(),
            ),
            run_time=0.2,
        )

        scene.play(
            Rotate(
                self.right_arm,
                angle=-70 * DEGREES,
                about_point=self.right_arm.get_start(),
            ),
            run_time=0.2,
        )

        scene.play(
            Rotate(
                self.right_arm,
                angle=70 * DEGREES,
                about_point=self.right_arm.get_start(),
            ),
            run_time=0.2,
        )

        scene.play(
            Rotate(
                self.right_arm,
                angle=-35 * DEGREES,
                about_point=self.right_arm.get_start(),
            ),
            run_time=0.2,
        )

    def walk(self, scene, direction=RIGHT, distance=3):
        scene.play(
            self.animate.shift(direction * distance),
            run_time=2,
            rate_func=linear,
        )