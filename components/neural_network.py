import numpy as np
from manim import *


class NeuralNetwork(VGroup):
    """
    Reusable neural network visualization.

    Example:
        nn = NeuralNetwork([2, 4, 3, 1])
    """

    def __init__(
        self,
        layers,
        neuron_radius=0.15,
        layer_spacing=2.2,
        neuron_spacing=0.8,
        neuron_color=BLUE,
        edge_color=GREY_B,
        stroke_width=2,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.layers_config = layers
        self.layer_spacing = layer_spacing
        self.neuron_spacing = neuron_spacing

        self.layers = VGroup()
        self.edges = VGroup()

        # -------------------------
        # Create neurons
        # -------------------------
        for i, num_neurons in enumerate(layers):

            layer = VGroup()

            for j in range(num_neurons):

                neuron = Circle(
                    radius=neuron_radius,
                    color=neuron_color,
                    stroke_width=2,
                    fill_color=BLACK,
                    fill_opacity=1,
                )

                neuron.move_to(
                    RIGHT * i * layer_spacing
                    + UP * ((num_neurons - 1) / 2 - j) * neuron_spacing
                )

                layer.add(neuron)

            self.layers.add(layer)

        # -------------------------
        # Create edges
        # -------------------------
        for i in range(len(self.layers) - 1):

            current_layer = self.layers[i]
            next_layer = self.layers[i + 1]

            for n1 in current_layer:
                for n2 in next_layer:

                    edge = Line(
                        n1.get_center(),
                        n2.get_center(),
                        color=edge_color,
                        stroke_width=stroke_width,
                    )

                    self.edges.add(edge)

        self.add(self.edges)
        self.add(self.layers)

        self.move_to(ORIGIN)

    # ------------------------------------------------
    # Animation Methods
    # ------------------------------------------------

    def create_animation(self):
        return AnimationGroup(
            Create(self.edges),
            LaggedStart(
                *[Create(layer) for layer in self.layers],
                lag_ratio=0.2,
            ),
            lag_ratio=0.3,
        )

    def highlight_layer(self, index, color=YELLOW):

        animations = []

        for neuron in self.layers[index]:
            animations.append(
                neuron.animate.set_stroke(color, width=4)
            )

        return AnimationGroup(*animations)

    def reset_colors(self, color=BLUE):

        animations = []

        for layer in self.layers:
            for neuron in layer:
                animations.append(
                    neuron.animate.set_stroke(color, width=2)
                )

        return AnimationGroup(*animations)

    def forward_pass(self, signal_color=YELLOW):

        animations = []

        for edge in self.edges:

            animations.append(
                edge.animate.set_color(signal_color)
            )

        return LaggedStart(
            *animations,
            lag_ratio=0.02,
        )

    def get_layer(self, index):
        return self.layers[index]

    def activate_layer(
        self,
        index,
        color=YELLOW,
    ):
        animations = []

        for neuron in self.layers[index]:
            animations.append(
                neuron.animate.set_fill(
                  color,
                  opacity=1,
                )
            )

        return AnimationGroup(*animations)


    def deactivate_layer(
        self,
        index,
    ):
        animations = []

        for neuron in self.layers[index]:
            animations.append(
                neuron.animate.set_fill(
                    BLACK,
                    opacity=1,
                )
            )

        return AnimationGroup(*animations)



    def animate_connections(
        self,
        layer_index,
        color=YELLOW,
    ):
        animations = []

        start = self.layers[layer_index]
        end = self.layers[layer_index + 1]

        for edge in self.edges:

            s = edge.get_start()
            e = edge.get_end()

            for n1 in start:
                for n2 in end:

                    if (
                        np.allclose(
                            s,
                            n1.get_center(),
                        )
                    and
                    np.allclose(
                        e,
                        n2.get_center(),
                    )
                ):
                        animations.append(
                           edge.animate.set_color(color)
                    )

        return LaggedStart(
            *animations,
            lag_ratio=0.02,
        )




    def forward_pass(self):

        animations = []

        for i in range(len(self.layers)):

            animations.append(
                self.activate_layer(i)
            )

            if i < len(self.layers) - 1:

                animations.append(
                    self.animate_connections(i)
                )

        return Succession(*animations)



    # ------------------------------------------------
    # Output Labels
    # ------------------------------------------------

    def add_output_labels(
        self,
        labels=None,
        font_size=22,
    ):
        

        if labels is None:
            labels = [str(i) for i in range(len(self.layers[-1]))]

        self.output_labels = VGroup()

        output_layer = self.layers[-1]

        for neuron, label in zip(output_layer, labels):

            text = Text(
                str(label),
                font_size=font_size,
            )

            text.next_to(
                neuron,
                RIGHT,
                buff=0.45,
            )

            self.output_labels.add(text)

        self.add(self.output_labels)

        return self.output_labels




# ------------------------------------------------
# Highlight Output
# ------------------------------------------------

    def highlight_output(
        self,
        index,
        color=GREEN,
    ):

        neuron = self.layers[-1][index]

        animations = [
            neuron.animate.set_fill(
                color,
                opacity=1,
            ),
            neuron.animate.set_stroke(
                color,
                width=5,
            ),
        ]

        if hasattr(self, "output_labels"):

            animations.append(
                self.output_labels[index].animate.set_color(color)
            )

        return AnimationGroup(*animations)