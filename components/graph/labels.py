from __future__ import annotations

from manim import *
import numpy as np


# ==========================================================
# Base Label
# ==========================================================

class LabelBase(VGroup):
    """
    Base class for all labels.
    """

    def __init__(self, mobject, **kwargs):
        super().__init__(**kwargs)

        self.label = mobject
        self.add(self.label)

    def move_to_point(self, point):
        self.move_to(point)
        return self

    def next_to_point(self, point, direction=UP, buff=0.15):
        self.next_to(point, direction, buff=buff)
        return self


# ==========================================================
# Axis Label
# ==========================================================

class AxisLabel(LabelBase):

    def __init__(
        self,
        text,
        direction=DOWN,
        font_size=28,
        **kwargs,
    ):

        label = Text(
            text,
            font_size=font_size,
        )

        if (
            np.allclose(direction, LEFT)

            or np.allclose(direction, RIGHT)
        ):
            label.rotate(PI / 2)
                

        super().__init__(label, **kwargs)


# ==========================================================
# Tick Label
# ==========================================================

class TickLabel(LabelBase):

    def __init__(
        self,
        text,
        font_size=24,
        **kwargs,
    ):

        super().__init__(
            Text(
                str(text),
                font_size=font_size,
            ),
            **kwargs,
        )


# ==========================================================
# Log Tick Label
# ==========================================================

class LogTickLabel(LabelBase):
    """
    Example:
        LogTickLabel(1000)

    -> 10^3
    """

    def __init__(
        self,
        value,
        font_size=26,
        **kwargs,
    ):

        exponent = int(np.log10(value))

        tex = MathTex(
            rf"10^{{{exponent}}}",
            font_size=font_size,
        )

        super().__init__(tex, **kwargs)


# ==========================================================
# Graph Title
# ==========================================================

class TitleLabel(LabelBase):

    def __init__(
        self,
        text,
        font_size=34,
        weight=BOLD,
        **kwargs,
    ):

        title = Text(
            text,
            font_size=font_size,
            weight=weight,
        )

        super().__init__(title, **kwargs)


# ==========================================================
# Species Label
# ==========================================================

class SpeciesLabel(LabelBase):

    def __init__(
        self,
        text,
        font_size=24,
        color=BLACK,
        italic=False,
        **kwargs,
    ):

        if italic:

            label = Text(
                text,
                slant=ITALIC,
                font_size=font_size,
                color=color,
            )

        else:

            label = Text(
                text,
                font_size=font_size,
                color=color,
            )

        super().__init__(label, **kwargs)


# ==========================================================
# Box Label
# ==========================================================

class BoxLabel(VGroup):

    def __init__(
        self,
        text,
        font_size=22,
        padding=0.12,
        corner_radius=0.08,
        fill_color=WHITE,
        stroke_color=BLACK,
        stroke_width=1.3,
        **kwargs,
    ):
        super().__init__(**kwargs)

        label = Text(
            str(text),
            font_size=font_size,
            color=BLACK,
        )

        box = RoundedRectangle(
            corner_radius=corner_radius,
            width=label.width + padding * 2,
            height=label.height + padding * 2,
            fill_color=fill_color,
            fill_opacity=1,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )

        label.move_to(box)

        self.box = box
        self.label = label

        self.add(
            box,
            label,
        )


# ==========================================================
# Number Badge
# ==========================================================

class NumberBadge(BoxLabel):
    """
    Figure 1.10 number boxes.

    Example:

        NumberBadge(7)
    """

    def __init__(
        self,
        number,
        radius=0.22,
        font_size=20,
        **kwargs,
    ):

        circle = Circle(
            radius=radius,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=BLACK,
            stroke_width=1.2,
        )

        label = Text(
            str(number),
            font_size=font_size,
            color=BLACK,
        )

        label.move_to(circle)

        super(VGroup, self).__init__()

        self.circle = circle
        self.label = label

        self.add(
            circle,
            label,
        )


# ==========================================================
# Annotation Label
# ==========================================================

class AnnotationLabel(LabelBase):

    def __init__(
        self,
        text,
        font_size=20,
        color=BLACK,
        **kwargs,
    ):

        super().__init__(
            Text(
                text,
                font_size=font_size,
                color=color,
            ),
            **kwargs,
        )