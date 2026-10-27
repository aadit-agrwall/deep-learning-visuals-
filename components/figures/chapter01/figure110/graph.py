from __future__ import annotations

import numpy as np
from manim import *

from components.graph.axes import LogAxes
from components.graph.grids import GraphGrid
from components.figures.chapter01.figure110.points import Figure110Points
from components.figures.chapter01.figure110.labels import Figure110Labels
from components.figures.chapter01.figure110.leaders import Figure110Leaders
from components.figures.chapter01.figure110.numbers import Figure110Numbers
from components.figures.chapter01.figure110.leaders import Figure110Leaders


class Figure110Graph(VGroup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ==================================================
        # Border
        # ==================================================

        self.border = Rectangle(
            width=11,
            height=6.5,
            stroke_width=2,
            color=BLACK,
        )

        # ==================================================
        # Title
        # ==================================================

        self.title = Text(
            "Connections per Neuron",
            font_size=30,
            color=BLACK,
        )

        self.title.move_to(
            self.border.get_top() + UP * 0.35
        )

        # ==================================================
        # Axes
        # ==================================================

        self.axes = LogAxes(
            x_range=[1950, 2015, 10],
            y_min=10,
            y_max=10000,
            x_length=9,
            y_length=5,
            show_border=False,
            show_grid=False,
        )

        self.axes.move_to(
            self.border.get_center() + DOWN * 0.25
        )

        # ==================================================
        # Grid
        # ==================================================

        self.grid = GraphGrid(
            self.axes,
            x_values=[
                1950, 1960, 1970, 1980,
                1990, 2000, 2010,
            ],
            y_values=[
                10,
                100,
                1000,
                10000,
            ],
            log_scale=True,
        )

        # ==================================================
        # Scatter Points
        # ==================================================
        self.points = Figure110Points(self.axes)
        self.numbers = Figure110Numbers(self.axes)
        self.labels = Figure110Labels(self.axes)
        self.leaders = Figure110Leaders(
            self.axes,
            self.labels,
            self.points,
        )

        # ==================================================
        # X Tick Labels
        # ==================================================

        self.x_ticks = VGroup()

        for year in [
            1950,
            1960,
            1970,
            1980,
            1990,
            2000,
            2010,
        ]:

            label = Text(
                str(year),
                font_size=18,
                color=BLACK,
            )

            label.next_to(
                self.axes.point(year, 10),
                DOWN,
                buff=0.18,
            )

            self.x_ticks.add(label)

        # ==================================================
        # Y Tick Labels
        # ==================================================

        self.y_ticks = VGroup()

        for value in [10, 100, 1000, 10000]:

            exponent = int(np.log10(value))

            label = MathTex(
                rf"10^{{{exponent}}}",
                font_size=22,
                color=BLACK,
            )

            label.next_to(
                self.axes.point(1950, value),
                LEFT,
                buff=0.18,
            )

            self.y_ticks.add(label)

        # ==================================================
        # Axis Labels
        # ==================================================

        self.x_label = Text(
            "Year",
            font_size=22,
            color=BLACK,
        )

        self.x_label.next_to(
            self.axes.axes.x_axis,
            DOWN,
            buff=0.75,
        )

        self.y_label = Text(
            "Connections per neuron",
            font_size=22,
            color=BLACK,
        )

        self.y_label.rotate(PI / 2)

        self.y_label.next_to(
            self.axes.axes.y_axis,
            LEFT,
            buff=0.75,
        )

        # ==================================================
        # Assemble
        # ==================================================

        self.add(
            self.border,
            self.grid,
            self.axes,

            self.leaders,

            self.points,
            self.labels,
            self.numbers,
            
            self.x_ticks,
            self.y_ticks,
            self.x_label,
            self.y_label,
            self.title,
        )