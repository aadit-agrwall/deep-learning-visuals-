from manim import *

from components.figures.chapter02.figure201.objects import (
    Scalar,
    Vector,
    Matrix,
    Tensor,
)

config.background_color = WHITE


class Figure201(Scene):

    def construct(self):

        title = Text(
            "Scalars, Vectors, Matrices and Tensors",
            font_size=32,
            color=BLACK,
        )

        title.to_edge(UP)

        scalar = Scalar("a")
        vector = Vector()
        matrix = Matrix()
        tensor = Tensor()

        scalar_label = Text(
            "Scalar",
            font_size=24,
            color=BLACK,
        )

        vector_label = Text(
            "Vector",
            font_size=24,
            color=BLACK,
        )

        matrix_label = Text(
            "Matrix",
            font_size=24,
            color=BLACK,
        )

        tensor_label = Text(
            "Tensor",
            font_size=24,
            color=BLACK,
        )

        objects = VGroup(
            scalar,
            vector,
            matrix,
            tensor,
        )

        objects.arrange(
            RIGHT,
            buff=0.7,
        )

        labels = VGroup(
            scalar_label,
            vector_label,
            matrix_label,
            tensor_label,
        )

        for label, obj in zip(labels, objects):
            label.next_to(
                obj,
                DOWN,
                buff=0.3,
            )

        self.play(
            Write(title)
        )

        self.play(
            LaggedStart(
                FadeIn(scalar),
                FadeIn(vector),
                FadeIn(matrix),
                FadeIn(tensor),
                lag_ratio=0.25,
            ),
            run_time=2,
        )

        self.play(
            LaggedStart(
                FadeIn(scalar_label),
                FadeIn(vector_label),
                FadeIn(matrix_label),
                FadeIn(tensor_label),
                lag_ratio=0.15,
            )
        )

        self.wait(2)