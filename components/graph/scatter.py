from __future__ import annotations

from manim import *


# ==========================================================
# Scatter Point
# ==========================================================

class ScatterPoint(Dot):
    """
    Reusable scatter point.

    Example:
        ScatterPoint(graph.point(2010, 1200))
    """

    def __init__(
        self,
        point,
        radius=0.05,
        color=BLACK,
        stroke_color=WHITE,
        stroke_width=1.5,
        **kwargs,
    ):
        super().__init__(
            point=point,
            radius=radius,
            color=color,
            **kwargs,
        )

        self.set_stroke(
            stroke_color,
            width=stroke_width,
        )


# ==========================================================
# Scatter Plot
# ==========================================================

class ScatterPlot(VGroup):
    """
    Generic scatter plot.
    """

    def __init__(
        self,
        coordinates,
        radius=0.05,
        color=BLACK,
        stroke_color=WHITE,
        stroke_width=1,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.dots = VGroup()

        for coordinate in coordinates:

            dot = ScatterPoint(
                coordinate,
                radius=radius,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )

            self.dots.add(dot)

        self.add(self.dots)

    def __iter__(self):
        return iter(self.dots)

    def __getitem__(self, index):
        return self.dots[index]

    def __len__(self):
        return len(self.dots)


# ==========================================================
# Named Scatter Plot
# ==========================================================

class NamedScatterPlot(VGroup):
    """
    Scatter points with labels.
    """

    def __init__(
        self,
        coordinates,
        labels,
        radius=0.05,
        color=BLACK,
        label_direction=UR,
        label_buff=0.12,
        font_size=18,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.dots = VGroup()
        self.labels = VGroup()

        for coordinate, text in zip(coordinates, labels):

            dot = ScatterPoint(
                coordinate,
                radius=radius,
                color=color,
            )

            label = Text(
                str(text),
                font_size=font_size,
            )

            label.next_to(
                dot,
                label_direction,
                buff=label_buff,
            )

            self.dots.add(dot)
            self.labels.add(label)

        self.add(
            self.dots,
            self.labels,
        )


# ==========================================================
# Colored Scatter Plot
# ==========================================================

class ColoredScatterPlot(VGroup):
    """
    Scatter plot where every point has its own color.
    """

    def __init__(
        self,
        coordinates,
        colors,
        radius=0.05,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.dots = VGroup()

        for coordinate, color in zip(coordinates, colors):

            self.dots.add(
                ScatterPoint(
                    coordinate,
                    radius=radius,
                    color=color,
                )
            )

        self.add(self.dots)


# ==========================================================
# Highlight Point
# ==========================================================

class HighlightPoint(VGroup):
    """
    Point with glow.
    """

    def __init__(
        self,
        point,
        radius=0.06,
        glow_radius=0.14,
        color=YELLOW,
        **kwargs,
    ):
        super().__init__(**kwargs)

        glow = Circle(
            radius=glow_radius,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.18,
        )

        glow.move_to(point)

        dot = ScatterPoint(
            point,
            radius=radius,
            color=color,
        )

        self.glow = glow
        self.dot = dot

        self.add(
            glow,
            dot,
        )


# ==========================================================
# Figure 1.10 Scatter
# ==========================================================

class Figure110Scatter(ScatterPlot):
    """
    Default scatter style used in Figure 1.10.
    """

    def __init__(
        self,
        coordinates,
        **kwargs,
    ):
        super().__init__(
            coordinates,
            radius=0.055,
            color=BLACK,
            stroke_color=WHITE,
            stroke_width=1,
            **kwargs,
        )