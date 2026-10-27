from __future__ import annotations

from manim import *


# ==========================================================
# Base Arrow
# ==========================================================

class BaseArrow(Arrow):
    """
    Standard arrow used throughout the project.
    """

    def __init__(
        self,
        start,
        end,
        color=BLACK,
        stroke_width=2,
        buff=0,
        tip_length=0.14,
        **kwargs,
    ):
        super().__init__(
            start,
            end,
            buff=buff,
            color=color,
            stroke_width=stroke_width,
            tip_length=tip_length,
            **kwargs,
        )


# ==========================================================
# Line Arrow
# ==========================================================

class LineArrow(Line):
    """
    Straight line without arrow tip.
    Useful for callouts.
    """

    def __init__(
        self,
        start,
        end,
        color=BLACK,
        stroke_width=2,
        **kwargs,
    ):
        super().__init__(
            start,
            end,
            color=color,
            stroke_width=stroke_width,
            **kwargs,
        )


# ==========================================================
# Curved Arrow
# ==========================================================

class CurvedGraphArrow(CurvedArrow):
    """
    Curved annotation arrow.
    """

    def __init__(
        self,
        start,
        end,
        angle=-PI / 4,
        color=BLACK,
        stroke_width=2,
        tip_length=0.14,
        **kwargs,
    ):
        super().__init__(
            start_point=start,
            end_point=end,
            angle=angle,
            color=color,
            stroke_width=stroke_width,
            tip_length=tip_length,
            **kwargs,
        )


# ==========================================================
# Dashed Arrow
# ==========================================================

class DashedGraphArrow(VGroup):
    """
    Dashed arrow.
    """

    def __init__(
        self,
        start,
        end,
        color=BLACK,
        stroke_width=2,
        num_dashes=30,
        **kwargs,
    ):
        super().__init__(**kwargs)

        line = Line(
            start,
            end,
            color=color,
            stroke_width=stroke_width,
        )

        dashed = DashedVMobject(
            line,
            num_dashes=num_dashes,
        )

        tip = ArrowTriangleFilledTip(
            color=color
        )

        tip.scale(0.7)

        direction = normalize(end - start)

        angle = angle_of_vector(direction)

        tip.rotate(angle - PI / 2)

        tip.move_to(end)

        self.add(
            dashed,
            tip,
        )


# ==========================================================
# Double Arrow
# ==========================================================

class DoubleGraphArrow(DoubleArrow):
    """
    Double-ended arrow.
    """

    def __init__(
        self,
        start,
        end,
        color=BLACK,
        stroke_width=2,
        buff=0,
        **kwargs,
    ):
        super().__init__(
            start,
            end,
            buff=buff,
            color=color,
            stroke_width=stroke_width,
            **kwargs,
        )


# ==========================================================
# Annotation Arrow
# ==========================================================

class AnnotationArrow(VGroup):
    """
    Arrow connecting a label to a target object.

    Example:
        AnnotationArrow(label, dot)
    """

    def __init__(
        self,
        source,
        target,
        color=BLACK,
        stroke_width=1.8,
        buff=0.05,
        **kwargs,
    ):
        super().__init__(**kwargs)

        arrow = Arrow(
            source.get_center(),
            target.get_center(),
            buff=buff,
            color=color,
            stroke_width=stroke_width,
            tip_length=0.12,
        )

        self.arrow = arrow

        self.add(arrow)


# ==========================================================
# Coordinate Arrow
# ==========================================================

class CoordinateArrow(BaseArrow):
    """
    Arrow using graph coordinates.

    Example:
        CoordinateArrow(
            graph,
            (1985,100),
            (2015,10000),
            log_scale=True,
        )
    """

    def __init__(
        self,
        axes,
        start_coord,
        end_coord,
        log_scale=False,
        color=BLACK,
        stroke_width=2,
        **kwargs,
    ):

        if log_scale:

            start = axes.point(*start_coord)
            end = axes.point(*end_coord)

        else:

            start = axes.c2p(*start_coord)
            end = axes.c2p(*end_coord)

        super().__init__(
            start,
            end,
            color=color,
            stroke_width=stroke_width,
            **kwargs,
        )


# ==========================================================
# Figure 1.10 Arrow
# ==========================================================

class Figure110Arrow(AnnotationArrow):
    """
    Default annotation style for Figure 1.10.
    """

    def __init__(
        self,
        source,
        target,
        **kwargs,
    ):
        super().__init__(
            source,
            target,
            color=BLACK,
            stroke_width=1.8,
            buff=0.04,
            **kwargs,
        )