import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from manim import *
from tensorflow.keras.datasets import mnist

from components.mnist import MNISTDigit


class MNISTInference(Scene):

    def construct(self):

        (x_train, y_train), _ = mnist.load_data()

        image = x_train[0]
        label = y_train[0]

        title = Text(
            f"Handwritten Digit: {label}",
            font_size=36,
        ).to_edge(UP)

        digit = MNISTDigit(
            image,
            pixel_size=0.14,
        )

        self.play(Write(title))
        self.play(digit.create_animation())
        self.wait(1)

        self.play(digit.explode_animation())
        self.wait(2)