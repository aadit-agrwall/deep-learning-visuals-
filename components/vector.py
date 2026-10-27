from manim import *
import numpy as np


class Vector2D(VGroup):
    """
    Reusable 2D Vector Component

    Example:
        vector = Vector2D([3, 2], label="v")
    """

    def __init__(
        self,
        coordinates,
        label="v",
        color=BLUE,
        show_dot=True,
        scale_factor=0.7,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.scale_factor = scale_factor
        self.original_coordinates = np.array(coordinates, dtype=float)
        self.coordinates = self.original_coordinates * self.scale_factor

        # --------------------------
        # Origin
        # --------------------------

        self.origin = ORIGIN

        # --------------------------
        # Arrow
        # --------------------------

        self.arrow = Arrow(
            self.origin,
            np.array(
                [
                    self.coordinates[0],
                    self.coordinates[1],
                    0,
                ]
            ),
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
            color=color,
        )

        # --------------------------
        # Endpoint
        # --------------------------

        self.dot = Dot(
            self.arrow.get_end(),
            color=color,
            radius=0.045,
        )

        # --------------------------
        # Label
        # --------------------------

        self.label = MathTex(label).scale(0.75)

        self.label.next_to(
            self.arrow.get_end(),
            UR,
            buff=0.15,
        )

        # --------------------------
        # Coordinate Label
        # --------------------------

        x, y = self.original_coordinates

        self.coordinate_label = MathTex(
            f"({x:g}, {y:g})"
        )

        self.coordinate_label.scale(0.45)

        self.coordinate_label.next_to(
            self.arrow.get_end(),
            DOWN,
            buff=0.15,
        )

        # --------------------------
        # Add objects
        # --------------------------

        self.add(self.arrow)

        if show_dot:
            self.add(self.dot)

        self.add(self.label)

    # -------------------------------------------------

    def create_animation(self):

        animations = [
            GrowArrow(self.arrow),
            FadeIn(self.label),
        ]

        if self.dot in self.submobjects:
            animations.append(FadeIn(self.dot))

        return AnimationGroup(*animations)

    # -------------------------------------------------

    def show_coordinates(self):

        return FadeIn(self.coordinate_label)

    # -------------------------------------------------

    def hide_coordinates(self):

        return FadeOut(self.coordinate_label)

    # -------------------------------------------------

    def highlight(self):

        return AnimationGroup(
            self.arrow.animate.set_color(YELLOW),
            self.dot.animate.set_color(YELLOW),
            self.label.animate.set_color(YELLOW),
        )

    # -------------------------------------------------

    def reset(self):

        original_color = self.arrow.get_color()

        return AnimationGroup(
            self.arrow.animate.set_color(original_color),
            self.dot.animate.set_color(original_color),
            self.label.animate.set_color(WHITE),
        )

    # -------------------------------------------------

    def transform_to(self, new_coordinates):

        self.original_coordinates = np.array(new_coordinates, dtype=float)

        scaled = self.original_coordinates * self.scale_factor

        new_arrow = Arrow(
            ORIGIN,
            np.array(
                [
                    scaled[0],
                    scaled[1],
                    0,
                ]
            ),
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
            color=self.arrow.get_color(),
        )

        new_dot = Dot(
            new_arrow.get_end(),
            color=self.arrow.get_color(),
            radius=0.045,
        )

        new_label = self.label.copy()
        new_label.next_to(
            new_arrow.get_end(),
            UR,
            buff=0.15,
        )

        x, y = self.original_coordinates

        new_coordinate = MathTex(
            f"({x:g}, {y:g})"
        ).scale(0.45)

        new_coordinate.next_to(
            new_arrow.get_end(),
            DOWN,
            buff=0.15,
        )

        animations = [
            Transform(self.arrow, new_arrow),
            Transform(self.dot, new_dot),
            Transform(self.label, new_label),
        ]

        if self.coordinate_label in self.submobjects:
            animations.append(
                Transform(
                    self.coordinate_label,
                    new_coordinate,
                )
            )

        return AnimationGroup(*animations)