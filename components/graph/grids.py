from __future__ import annotations

from manim import *


class BaseGrid(VGroup):
    """
    Base class for all grid systems.
    """

    def __init__(self, axes, **kwargs):
        super().__init__(**kwargs)
        self.axes = axes


# ==========================================================
# Vertical Grid
# ==========================================================

class VerticalGrid(BaseGrid):
    """
    Thin vertical guide lines.

    Example:
        VerticalGrid(graph, [1950,1985,2000,2015])
    """

    def __init__(
        self,
        axes,
        x_values,
        dashed=True,
        color=GRAY_C,
        stroke_width=0.6,
        dash_length=0.045,
        dashed_ratio=0.45,
        z_index=-10,
        **kwargs,
    ):
        super().__init__(axes, **kwargs)

        y0 = axes.axes.y_range[0]
        y1 = axes.axes.y_range[1]

        for x in x_values:

            start = axes.c2p(x, y0)
            end = axes.c2p(x, y1)

            if dashed:

                line = DashedLine(
                    start,
                    end,
                    dash_length=dash_length,
                    dashed_ratio=dashed_ratio,
                    stroke_width=stroke_width,
                    color=color,
                )

            else:

                line = Line(
                    start,
                    end,
                    stroke_width=stroke_width,
                    color=color,
                )

            line.set_z_index(z_index)

            self.add(line)


# ==========================================================
# Horizontal Grid
# ==========================================================

class HorizontalGrid(BaseGrid):
    """
    Horizontal reference lines.
    """

    def __init__(
        self,
        axes,
        y_values,
        dashed=False,
        log_scale=False,
        color=GRAY_C,
        stroke_width=0.8,
        dash_length=0.045,
        dashed_ratio=0.45,
        z_index=-10,
        **kwargs,
    ):
        super().__init__(axes, **kwargs)

        x0 = axes.axes.x_range[0]
        x1 = axes.axes.x_range[1]

        for y in y_values:

            if log_scale:
                p1 = axes.point(x0, y)
                p2 = axes.point(x1, y)
            else:
                p1 = axes.c2p(x0, y)
                p2 = axes.c2p(x1, y)

            if dashed:

                line = DashedLine(
                    p1,
                    p2,
                    dash_length=dash_length,
                    dashed_ratio=dashed_ratio,
                    stroke_width=stroke_width,
                    color=color,
                )

            else:

                line = Line(
                    p1,
                    p2,
                    stroke_width=stroke_width,
                    color=color,
                )

            line.set_z_index(z_index)

            self.add(line)


# ==========================================================
# Minor Vertical Grid
# ==========================================================

class MinorVerticalGrid(BaseGrid):
    """
    Extra thin helper lines.
    """

    def __init__(
        self,
        axes,
        x_values,
        color=GRAY_D,
        stroke_width=0.35,
        dash_length=0.03,
        dashed_ratio=0.45,
        **kwargs,
    ):
        super().__init__(axes, **kwargs)

        y0 = axes.axes.y_range[0]
        y1 = axes.axes.y_range[1]

        for x in x_values:

            self.add(
                DashedLine(
                    axes.c2p(x, y0),
                    axes.c2p(x, y1),
                    dash_length=dash_length,
                    dashed_ratio=dashed_ratio,
                    stroke_width=stroke_width,
                    color=color,
                )
            )


# ==========================================================
# Minor Horizontal Grid
# ==========================================================

class MinorHorizontalGrid(BaseGrid):
    """
    Extra thin helper lines.
    """

    def __init__(
        self,
        axes,
        y_values,
        log_scale=False,
        color=GRAY_D,
        stroke_width=0.35,
        dash_length=0.03,
        dashed_ratio=0.45,
        **kwargs,
    ):
        super().__init__(axes, **kwargs)

        x0 = axes.axes.x_range[0]
        x1 = axes.axes.x_range[1]

        for y in y_values:

            if log_scale:
                p1 = axes.point(x0, y)
                p2 = axes.point(x1, y)
            else:
                p1 = axes.c2p(x0, y)
                p2 = axes.c2p(x1, y)

            self.add(
                DashedLine(
                    p1,
                    p2,
                    dash_length=dash_length,
                    dashed_ratio=dashed_ratio,
                    stroke_width=stroke_width,
                    color=color,
                )
            )


# ==========================================================
# Combined Grid
# ==========================================================

class GraphGrid(VGroup):
    """
    Complete graph grid.

    Example
    -------
    grid = GraphGrid(
        graph,
        x_values=[1950,1985,2000,2015],
        y_values=[10,100,1000,10000],
        log_scale=True,
    )
    """

    def __init__(
        self,
        axes,
        x_values,
        y_values,
        log_scale=False,
        vertical_dashed=True,
        horizontal_dashed=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.vertical = VerticalGrid(
            axes,
            x_values=x_values,
            dashed=vertical_dashed,
        )

        self.horizontal = HorizontalGrid(
            axes,
            y_values=y_values,
            dashed=horizontal_dashed,
            log_scale=log_scale,
        )

        self.add(
            self.vertical,
            self.horizontal,
        )