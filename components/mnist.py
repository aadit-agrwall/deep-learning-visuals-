from manim import *
import numpy as np


class MNISTDigit(VGroup):
    """
    Reusable MNIST Digit Component.

    Displays a 28x28 grayscale image using small squares.
    """

    def __init__(
        self,
        image,
        pixel_size=0.12,
        border=True,
        **kwargs,
    ):
        super().__init__(**kwargs)

        image = np.array(image, dtype=float)

        if image.shape != (28, 28):
            raise ValueError("MNIST image must have shape (28, 28).")

        self.image = image
        self.pixel_size = pixel_size

        # -----------------------------------------
        # Create Pixels
        # -----------------------------------------

        self.pixel_group = VGroup()

        for r in range(28):
            for c in range(28):

                value = image[r, c] / 255.0

                pixel = Square(
                    side_length=pixel_size,
                    stroke_width=0,
                )

                pixel.set_fill(
                    WHITE,
                    opacity=value,
                )

                pixel.move_to(
                    RIGHT * c * pixel_size +
                    DOWN * r * pixel_size
                )

                self.pixel_group.add(pixel)

        self.pixel_group.move_to(ORIGIN)

        self.add(self.pixel_group)

        # -----------------------------------------
        # Border
        # -----------------------------------------

        if border:

            self.frame = SurroundingRectangle(
                self.pixel_group,
                color=WHITE,
                buff=0.03,
                stroke_width=2,
            )

            self.add(self.frame)

    # -------------------------------------------------------
    # Accessors
    # -------------------------------------------------------

    def get_pixels(self):
        return self.pixel_group

    # -------------------------------------------------------
    # Create Animation
    # -------------------------------------------------------

    def create_animation(self):

        return LaggedStart(
            *[
                FadeIn(pixel, scale=0.5)
                for pixel in self.pixel_group
            ],
            lag_ratio=0.001,
            run_time=2,
        )

    # -------------------------------------------------------
    # Explode
    # -------------------------------------------------------

    def explode_animation(
        self,
        distance=0.5,
        run_time=2,
    ):

        center = self.pixel_group.get_center()

        animations = []

        for pixel in self.pixel_group:

            direction = pixel.get_center() - center

            norm = np.linalg.norm(direction)

            if norm != 0:
                direction = direction / norm

            animations.append(
                pixel.animate.shift(
                    direction * distance
                )
            )

        return AnimationGroup(
            *animations,
            lag_ratio=0,
            run_time=run_time,
        )

    # -------------------------------------------------------
    # Collapse
    # -------------------------------------------------------

    def collapse_animation(
        self,
        run_time=2,
    ):

        target = self.pixel_group.copy()

        target.move_to(ORIGIN)

        animations = []

        for old_pixel, new_pixel in zip(
            self.pixel_group,
            target,
        ):

            animations.append(
                old_pixel.animate.move_to(
                    new_pixel.get_center()
                )
            )

        return AnimationGroup(
            *animations,
            lag_ratio=0,
            run_time=run_time,
        )

    # -------------------------------------------------------
    # Highlight Pixel
    # -------------------------------------------------------

    def highlight_pixel(
        self,
        row,
        col,
        color=YELLOW,
    ):

        index = row * 28 + col

        return self.pixel_group[index].animate.set_fill(
            color=color,
            opacity=1,
        )

    # -------------------------------------------------------
    # Reset Colors
    # -------------------------------------------------------

    def reset_colors(self):

        animations = []

        for pixel, value in zip(
            self.pixel_group,
            self.image.flatten(),
        ):

            animations.append(
                pixel.animate.set_fill(
                    WHITE,
                    opacity=value / 255,
                )
            )

        return AnimationGroup(*animations)

    # -------------------------------------------------------
    # Fade Out
    # -------------------------------------------------------

    def fade_pixels(self):

        return FadeOut(self.pixel_group)

    # -------------------------------------------------------
    # Fade In
    # -------------------------------------------------------

    def fade_pixels_in(self):

        return FadeIn(self.pixel_group)