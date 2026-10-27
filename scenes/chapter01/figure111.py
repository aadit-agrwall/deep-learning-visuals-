from manim import *

from components.figures.chapter01.figure111.graph import Figure111Graph

config.background_color = WHITE


class Figure111(Scene):

    def construct(self):

        graph = Figure111Graph()

        # Border
        self.play(Create(graph.border))

        # Grid
        self.play(Create(graph.grid), run_time=1)

        # Axes
        self.play(Create(graph.axes), run_time=1)

        # Tick labels
        self.play(
            FadeIn(graph.x_ticks),
            FadeIn(graph.y_ticks),
        )

        # Axis labels
        self.play(
            Write(graph.x_label),
            Write(graph.y_label),
        )

        # Title
        self.play(Write(graph.title))

        # Scatter points
        self.play(
            LaggedStart(
                *[GrowFromCenter(dot) for dot in graph.points],
                lag_ratio=0.05,
            )
        )

        # Number badges
        self.play(
            LaggedStart(
                *[FadeIn(badge, scale=0.5) for badge in graph.numbers],
                lag_ratio=0.05,
            )
        )

        # Labels
        self.play(
            LaggedStart(
                *[FadeIn(label) for label in graph.labels],
                lag_ratio=0.05,
            )
        )

        # Leader lines
        self.play(
            LaggedStart(
                *[Create(line) for line in graph.leaders],
                lag_ratio=0.03,
            )
        )

        # Animal labels
        self.play(FadeIn(graph.animals))

        self.wait(2)