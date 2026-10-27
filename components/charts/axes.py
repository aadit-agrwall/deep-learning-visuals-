"""
components/charts/axes.py

Convenience builders for chart axes. Wraps components.graph.axes.BaseAxes
and LogAxes with chapter-aware default styling, so chart classes in this
package don't each re-derive axis colors/config from scratch.
"""

from components.graph.axes import BaseAxes, LogAxes
from common.colors import get_color


def build_axes(x_range, y_range, chapter=None, x_length=8, y_length=5,
                show_border=True, show_grid=False, **kwargs):
    """
    Build a standard (linear) BaseAxes instance styled for the given
    chapter's palette. `x_range`/`y_range` follow Manim's [min, max, step]
    convention, matching BaseAxes' own signature.
    """
    axis_color = get_color("subtext") if chapter is None else get_color("text", chapter=chapter)
    axis_config = {"color": axis_color}
    return BaseAxes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        show_border=show_border,
        show_grid=show_grid,
        axis_config=axis_config,
        **kwargs,
    )


def build_log_axes(x_range, y_min, y_max, chapter=None, x_length=8, y_length=5, **kwargs):
    """
    Build a LogAxes instance (logarithmic Y-axis, real-value input via
    .point(x, y)) styled for the given chapter's palette.
    """
    axis_color = get_color("subtext") if chapter is None else get_color("text", chapter=chapter)
    axis_config = {"color": axis_color}
    return LogAxes(
        x_range=x_range,
        y_min=y_min,
        y_max=y_max,
        x_length=x_length,
        y_length=y_length,
        axis_config=axis_config,
        **kwargs,
    )
