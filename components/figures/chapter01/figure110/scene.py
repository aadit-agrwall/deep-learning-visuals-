from manim import *

from components.figures.chapter01.figure110.graph import Figure110Graph


class Figure110(Scene):

    def construct(self):

        graph = Figure110Graph()

        self.play(Create(graph.border))

        self.play(Create(graph.grid))

        self.play(Create(graph.axes))

        self.play(FadeIn(graph.x_tick_labels))
        self.play(FadeIn(graph.y_tick_labels))

        self.play(Write(graph.title))

        self.play(FadeIn(graph.x_label))
        self.play(FadeIn(graph.y_label))

        self.play(FadeIn(graph.caption))

        self.wait(2)