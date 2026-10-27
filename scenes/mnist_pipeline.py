import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from manim import *
from tensorflow.keras.datasets import mnist

from components.mnist import MNISTDigit
from components.neural_network import NeuralNetwork


class MNISTPipeline(Scene):

    def construct(self):

        # ---------------------------------------
        # Load MNIST
        # ---------------------------------------

        (x_train, y_train), _ = mnist.load_data()

        image = x_train[0]
        label = y_train[0]

        # ---------------------------------------
        # MNIST Digit
        # ---------------------------------------

        digit = MNISTDigit(
            image,
            pixel_size=0.08,
        )

        digit.shift(LEFT * 4)

        # ---------------------------------------
        # Neural Network
        # ---------------------------------------

        network = NeuralNetwork(
            [12, 8, 8, 10],
            neuron_radius=0.12,
            layer_spacing=1.8,
            neuron_spacing=0.45,
        )

        network.shift(RIGHT * 0.5)

        # Add labels 0-9 beside output neurons
        network.add_output_labels()

        # ---------------------------------------
        # Animation
        # ---------------------------------------

        self.play(digit.create_animation())
        self.wait(0.5)

        self.play(Create(network))
        self.wait(0.5)

        self.play(network.forward_pass())
        self.wait(0.5)

        # Highlight predicted output neuron
        self.play(
            network.highlight_output(label)
        )

        self.wait(0.5)

        # Prediction text
        prediction = Text(
            f"Prediction = {label}",
            font_size=32,
            color=GREEN,
        )

        prediction.next_to(
            network,
            RIGHT,
            buff=0.6,
        )

        self.play(FadeIn(prediction))

        self.wait(2)