from manim import *

import numpy as np

from tensorflow.keras.datasets import mnist

from components.mnist import MNISTDigit


class TestMNIST(Scene):

    def construct(self):

        # Load dataset
        (x_train, y_train), _ = mnist.load_data()

        # Select one handwritten digit
        image = x_train[0]
        label = y_train[0]

        digit = MNISTDigit(
            image,
            pixel_size=0.16
        )

        title = Text(
            f"Handwritten Digit : {label}",
            font_size=34
        )

        title.to_edge(UP)

        self.play(Write(title))

        self.play(digit.create_animation())

        self.wait(2)