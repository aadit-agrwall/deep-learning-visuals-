from __future__ import annotations

import numpy as np
from manim import *

from components.graph.axes import LogAxes
from components.graph.grids import GraphGrid

from components.figures.chapter01.figure111.points import Figure111Points
from components.figures.chapter01.figure111.labels import Figure111Labels
from components.figures.chapter01.figure111.leaders import Figure111Leaders
from components.figures.chapter01.figure111.numbers import Figure111Numbers
from components.figures.chapter01.figure111.animals import Figure111Animals
from components.figures.chapter01.figure111.trend import Figure111Trend


class Figure111Graph(VGroup):

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
            "Parameters in Artificial Neural Networks",
            font_size=28,
            color=BLACK,
        )

        self.title.move_to(
            self.border.get_top() + UP * 0.35
        )

        # ==================================================
        # Axes
        # ==================================================

        self.axes = LogAxes(
            x_range=[1995, 2025, 5],
            y_min=1e4,
            y_max=1e12,
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
                1995,
                2000,
                2005,
                2010,
                2015,
                2020,
                2025,
            ],
            y_values=[
                1e4,
                1e6,
                1e8,
                1e10,
                1e12,
            ],
            log_scale=True,
        )

        # ==================================================
        # Data Objects
        # ==================================================

        self.points = Figure111Points(self.axes)

        self.numbers = Figure111Numbers(self.axes)

        self.labels = Figure111Labels(self.axes)

        self.trend = Figure111Trend(self.axes)

        self.leaders = Figure111Leaders(
            self.axes,
            self.labels,
            self.points,
        )

        self.animals = Figure111Animals(self.axes)

        # ==================================================
        # X Tick Labels
        # ==================================================

        self.x_ticks = VGroup()

        for year in [
            1995,
            2000,
            2005,
            2010,
            2015,
            2020,
            2025,
        ]:

            label = Text(
                str(year),
                font_size=18,
                color=BLACK,
            )

            label.next_to(
                self.axes.point(year, 1e4),
                DOWN,
                buff=0.18,
            )

            self.x_ticks.add(label)

        # ==================================================
        # Y Tick Labels
        # ==================================================

        self.y_ticks = VGroup()

        for value in [
            1e4,
            1e6,
            1e8,
            1e10,
            1e12,
        ]:

            exponent = int(np.log10(value))

            label = MathTex(
                rf"10^{{{exponent}}}",
                font_size=22,
                color=BLACK,
            )

            label.next_to(
                self.axes.point(1995, value),
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
            "Parameters",
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
            self.trend,
            self.axes,
            self.points,
            self.numbers,
            self.labels,
            self.leaders,
            self.animals,
            self.x_ticks,
            self.y_ticks,
            self.x_label,
            self.y_label,
            self.title,
        )