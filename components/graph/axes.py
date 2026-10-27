from __future__ import annotations

from abc import ABC
import numpy as np
from manim import *


class BaseAxes(VGroup, ABC):
    """
    Base wrapper around Manim Axes.

    Every graph in this project should inherit from this class.
    """

    def __init__(
        self,
        x_range,
        y_range,
        x_length=8,
        y_length=5,
        show_border=True,
        show_grid=False,
        axis_config=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        default_axis_config = {
            "include_ticks": True,
            "include_numbers": False,
            "include_tip": False,
            "stroke_width": 2,
            "color": BLACK,
        }

        if axis_config:
            default_axis_config.update(axis_config)

        self.axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config=default_axis_config,
        )

        self.add(self.axes)

        self.border = None

        if show_border:
            self.border = Rectangle(
                width=x_length,
                height=y_length,
                stroke_width=2,
                color=BLACK,
            )
            self.border.move_to(self.axes)
            self.add(self.border)

        self.grid = VGroup()

        if show_grid:
            self.create_grid()

    # --------------------------------------------------

    def create_grid(self):
        """
        Override in subclasses.
        """
        pass

    # --------------------------------------------------

    def c2p(self, *coords):
        return self.axes.c2p(*coords)

    def p2c(self, point):
        return self.axes.p2c(point)

    # --------------------------------------------------

    @property
    def width(self):
        return self.axes.x_length

    @property
    def height(self):
        return self.axes.y_length


# ======================================================================


class LogAxes(BaseAxes):
    """
    Logarithmic Y-axis.

    User provides REAL values.

    Example

    graph.point(2012,1200)

    automatically converts

    log10(1200)
    """

    def __init__(
        self,
        x_range,
        y_min,
        y_max,
        x_length=8,
        y_length=5,
        **kwargs,
    ):

        self.y_min = y_min
        self.y_max = y_max

        super().__init__(
            x_range=x_range,
            y_range=[
                np.log10(y_min),
                np.log10(y_max),
                1,
            ],
            x_length=x_length,
            y_length=y_length,
            **kwargs,
        )

    # --------------------------------------------------

    def point(self, x, y):
        """
        Convert real value to graph coordinate.

        point(2010,1000)
        """

        return self.axes.c2p(
            x,
            np.log10(y),
        )

    # --------------------------------------------------

    def add_log_labels(
        self,
        values,
        font_size=26,
        left_buff=0.2,
    ):
        """
        values = [10,100,1000]
        """

        labels = VGroup()

        for value in values:

            exponent = int(np.log10(value))

            tex = MathTex(
                rf"10^{{{exponent}}}",
                font_size=font_size,
            )

            tex.next_to(
                self.point(
                    self.axes.x_range[0],
                    value,
                ),
                LEFT,
                buff=left_buff,
            )

            labels.add(tex)

        self.add(labels)

        return labels

    # --------------------------------------------------

    def create_vertical_grid(
        self,
        xs,
        color=GRAY,
        stroke_width=1,
        dash_length=0.08,
    ):

        grid = VGroup()

        y0 = self.axes.y_range[0]
        y1 = self.axes.y_range[1]

        for x in xs:

            line = DashedLine(
                self.axes.c2p(x, y0),
                self.axes.c2p(x, y1),
                dash_length=dash_length,
                color=color,
                stroke_width=stroke_width,
            )

            grid.add(line)

        self.add(grid)

        return grid

    # --------------------------------------------------

    def create_horizontal_grid(
        self,
        values,
        color=GRAY,
        stroke_width=1,
    ):

        grid = VGroup()

        for value in values:

            y = np.log10(value)

            line = Line(
                self.axes.c2p(self.axes.x_range[0], y),
                self.axes.c2p(self.axes.x_range[1], y),
                stroke_width=stroke_width,
                color=color,
            )

            grid.add(line)

        self.add(grid)

        return grid