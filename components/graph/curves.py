from __future__ import annotations

from manim import *


# ==========================================================
# Base Curve
# ==========================================================

class BaseCurve(VMobject):
    """
    Base curve for all graph curves.
    """

    def __init__(
        self,
        color=BLACK,
        stroke_width=2,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.set_stroke(
            color=color,
            width=stroke_width,
        )


# ==========================================================
# Polyline Curve
# ==========================================================

class PolylineCurve(BaseCurve):
    """
    Connect points using straight lines.
    """

    def __init__(
        self,
        points,
        color=BLACK,
        stroke_width=2,
        **kwargs,
    ):
        super().__init__(
            color=color,
            stroke_width=stroke_width,
            **kwargs,
        )

        self.set_points_as_corners(points)


# ==========================================================
# Smooth Curve
# ==========================================================

class SmoothCurve(BaseCurve):
    """
    Smooth spline passing through points.
    """

    def __init__(
        self,
        points,
        color=BLACK,
        stroke_width=2,
        **kwargs,
    ):
        super().__init__(
            color=color,
            stroke_width=stroke_width,
            **kwargs,
        )

        self.set_points_smoothly(points)


# ==========================================================
# Graph Curve
# ==========================================================

class GraphCurve(SmoothCurve):
    """
    Takes graph coordinates and converts them automatically.

    Example:

    GraphCurve(
        graph,
        [
            (1985,20),
            (1995,100),
            (2005,600),
        ]
    )
    """

    def __init__(
        self,
        axes,
        coordinates,
        log_scale=False,
        color=BLACK,
        stroke_width=2,
        **kwargs,
    ):

        pts = []

        for x, y in coordinates:

            if log_scale:
                pts.append(axes.point(x, y))
            else:
                pts.append(axes.c2p(x, y))

        super().__init__(
            pts,
            color=color,
            stroke_width=stroke_width,
            **kwargs,
        )


# ==========================================================
# Dashed Curve
# ==========================================================

class DashedGraphCurve(VGroup):
    """
    Dashed version of GraphCurve.
    """

    def __init__(
        self,
        axes,
        coordinates,
        log_scale=False,
        color=BLACK,
        stroke_width=2,
        dash_length=0.08,
        **kwargs,
    ):
        super().__init__(**kwargs)

        curve = GraphCurve(
            axes,
            coordinates,
            log_scale=log_scale,
            color=color,
            stroke_width=stroke_width,
        )

        dashed = DashedVMobject(
            curve,
            num_dashes=60,
            dashed_ratio=0.55,
        )

        dashed.set_color(color)

        self.curve = dashed

        self.add(dashed)


# ==========================================================
# Bezier Curve
# ==========================================================

class BezierCurve(BaseCurve):
    """
    Cubic Bezier curve.

    Requires exactly four control points.
    """

    def __init__(
        self,
        control_points,
        color=BLACK,
        stroke_width=2,
        **kwargs,
    ):
        super().__init__(
            color=color,
            stroke_width=stroke_width,
            **kwargs,
        )

        self.set_points_as_corners(control_points)
        self.make_smooth()


# ==========================================================
# MultiCurve
# ==========================================================

class MultiCurve(VGroup):
    """
    Group several curves together.
    """

    def __init__(
        self,
        curves,
        **kwargs,
    ):
        super().__init__(**kwargs)

        for curve in curves:
            self.add(curve)


# ==========================================================
# Figure 1.10 Curve
# ==========================================================

class Figure110Curve(GraphCurve):
    """
    Default style used in Figure 1.10.
    """

    def __init__(
        self,
        axes,
        coordinates,
        log_scale=True,
        **kwargs,
    ):

        super().__init__(
            axes=axes,
            coordinates=coordinates,
            log_scale=log_scale,
            color=BLACK,
            stroke_width=2.2,
            **kwargs,
        )