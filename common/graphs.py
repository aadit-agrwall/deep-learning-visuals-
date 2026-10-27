"""
common/graphs.py

Higher-level, reusable compositions built on top of the existing
components.graph.* classes (axes, curves, arrows, labels, scatter).
Does NOT reimplement axis/curve/scatter construction — callers build
those with components.graph.* directly, then pass the instances here
for labeling, annotation, and common combined patterns.
"""

from manim import VGroup, Text, UP, DOWN, RIGHT, LEFT

from components.graph.labels import AxisLabel, TitleLabel, AnnotationLabel
from components.graph.arrows import AnnotationArrow

from common.styles import text_style
from common.colors import get_color


def titled_graph(axes_mobject, title: str, chapter: str = None, buff: float = 0.4):
    """Attach a TitleLabel above an already-built axes instance."""
    title_label = TitleLabel(title, **text_style("subtitle", chapter=chapter))
    title_label.next_to(axes_mobject, UP, buff=buff)
    return VGroup(title_label, axes_mobject)


def axis_labels(axes_mobject, x_label: str, y_label: str, chapter: str = None):
    """
    Attach x/y AxisLabel mobjects to an already-built axes instance,
    positioned at its right and top edges respectively.
    """
    x_text = AxisLabel(x_label, **text_style("label", chapter=chapter))
    y_text = AxisLabel(y_label, **text_style("label", chapter=chapter))
    x_text.next_to(axes_mobject, RIGHT, buff=0.3)
    y_text.next_to(axes_mobject, UP, buff=0.3)
    return VGroup(axes_mobject, x_text, y_text)


def annotate_point(axes_mobject, point_coords, text: str, chapter: str = None, direction=UP):
    """
    Draw an AnnotationArrow + AnnotationLabel pointing at a specific
    data coordinate on an axes instance. `point_coords` is (x, y) in
    axes data-space; converted via axes_mobject.c2p(...).
    """
    color = get_color("accent", chapter=chapter)
    target_point = axes_mobject.c2p(*point_coords)
    label = AnnotationLabel(text, **text_style("caption", chapter=chapter))
    label.next_to(target_point, direction, buff=0.4)
    arrow = AnnotationArrow(start=label.get_bottom(), end=target_point, color=color)
    return VGroup(arrow, label)


def plot_curve(axes_mobject, curve_mobject, chapter: str = None, color=None):
    """
    Attach an already-built curve (GraphCurve/PolylineCurve/SmoothCurve/
    BezierCurve) to an axes instance, applying the chapter's primary
    color unless a color is explicitly given.
    """
    if color is None:
        color = get_color("primary", chapter=chapter)
    curve_mobject.set_color(color)
    return VGroup(axes_mobject, curve_mobject)


def plot_multiple_curves(axes_mobject, curve_mobjects, chapter: str = None):
    """
    Attach several curves to one axes instance, auto-coloring each
    with palette_sequence so they're visually distinct.
    """
    from common.colors import palette_sequence
    colors = palette_sequence(len(curve_mobjects), chapter=chapter)
    for curve, color in zip(curve_mobjects, colors):
        curve.set_color(color)
    return VGroup(axes_mobject, *curve_mobjects)


def scatter_with_labels(axes_mobject, scatter_mobject, chapter: str = None):
    """
    Combine an axes instance with an already-built ScatterPlot /
    NamedScatterPlot / ColoredScatterPlot instance into one group,
    applying the chapter's primary color to unlabeled scatter points
    if the scatter object exposes a set_color method.
    """
    if hasattr(scatter_mobject, "set_color"):
        scatter_mobject.set_color(get_color("primary", chapter=chapter))
    return VGroup(axes_mobject, scatter_mobject)


def graph_legend(entries, chapter: str = None, buff: float = 0.2):
    """
    Simple legend for graph figures: list of (label, color) tuples.
    Thin wrapper around common.components.legend for graph-specific
    call sites so imports stay intuitive (common.graphs.graph_legend).
    """
    from common.components import legend
    return legend(entries, chapter=chapter, buff=buff)
