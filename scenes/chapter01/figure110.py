from manim import *

from components.figures.chapter01.figure110.graph import Figure110Graph

config.background_color = WHITE


class Figure110(Scene):

    def construct(self):

        graph = Figure110Graph()
        print("graph.points =", graph.points)
        print("number of dots =", len(graph.points))

        # Border
        self.play(Create(graph.border))

        # Grid
        self.play(Create(graph.grid), run_time=1.2)

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
        self.play(
            Write(graph.title)
        )

        # Scatter points
        self.play(
            LaggedStart(
                *[
                    GrowFromCenter(dot)
                    for dot in graph.points
                ],
                lag_ratio=0.08,
            )
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(number, scale=0.6)
                    for number in graph.numbers
                ],
                lag_ratio=0.05,
            ),
            run_time=1,
        )



        #Label animation  
        self.play(
            LaggedStart(
                *[
                    FadeIn(label)
                    for label in graph.labels
                ],
                lag_ratio=0.08,
            )
        )

        self.play(
            LaggedStart(
                *[
                    Create(line)
                    for line in graph.leaders
                ],
                lag_ratio=0.05,
                run_time=1.5,
            )
        )

        self.play(
            LaggedStart(
                *[
                    Create(line)
                    for line in graph.leaders
                ],
                lag_ratio=0.05,
            ),
            run_time=1.5,
        )

        self.wait(2)