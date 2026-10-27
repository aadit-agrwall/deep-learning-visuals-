"""
common/connectors.py

Boundary-aware arrow/connector helpers. Unlike hand-placed Arrow(start,
end) calls with manually computed coordinates, these functions always
anchor to the actual edge of each mobject — so if a box, text, or curve
changes size, the connector automatically follows without overlap or
misalignment.
"""

from manim import (
    Arrow, DoubleArrow, VGroup, Text, Dot,
    LEFT, RIGHT, UP, DOWN, ORIGIN,
)

from common.colors import get_color
from common.styles import stroke_width, text_style


def _closest_edge_points(mobject_a, mobject_b):
    """
    Return (start, end) points on the facing edges of two mobjects,
    choosing horizontal or vertical connection based on their relative
    centers, so the arrow never starts/ends inside either shape.
    """
    center_a = mobject_a.get_center()
    center_b = mobject_b.get_center()
    dx = center_b[0] - center_a[0]
    dy = center_b[1] - center_a[1]

    if abs(dx) >= abs(dy):
        # horizontal relationship
        if dx >= 0:
            return mobject_a.get_right(), mobject_b.get_left()
        return mobject_a.get_left(), mobject_b.get_right()
    else:
        # vertical relationship
        if dy >= 0:
            return mobject_a.get_top(), mobject_b.get_bottom()
        return mobject_a.get_bottom(), mobject_b.get_top()


def smart_arrow(source, target, chapter=None, color=None, buff=0.15,
                stroke=None, double=False):
    """
    Draw an arrow between two mobjects that always touches their
    facing edges — no manual coordinate math, no overlap with either
    object's body, and it auto-updates if you re-call this after
    moving/resizing either mobject.
    """
    start, end = _closest_edge_points(source, target)
    color = color or get_color("primary", chapter=chapter)
    stroke_w = stroke or stroke_width("default")
    arrow_cls = DoubleArrow if double else Arrow
    return arrow_cls(start, end, color=color, buff=buff, stroke_width=stroke_w)


def labeled_connector(source, target, label: str, chapter=None, color=None,
                       buff=0.15, label_buff=0.15):
    """
    Same as smart_arrow, but with a small text label centered above
    the midpoint of the arrow (e.g. "predicts", "transforms").
    """
    arrow = smart_arrow(source, target, chapter=chapter, color=color, buff=buff)
    midpoint = arrow.get_center()
    label_text = Text(label, **text_style("caption", chapter=chapter))
    label_text.move_to(midpoint + UP * label_buff)
    return VGroup(arrow, label_text)


def connector_chain(mobjects, chapter=None, color=None, buff=0.15):
    """
    Draw arrows connecting a sequence of mobjects in order:
    mobjects[0] -> mobjects[1] -> mobjects[2] -> ...
    Each arrow is boundary-aware, so this works regardless of each
    mobject's size or exact position, as long as they're already
    arranged (e.g. via common.layouts.stack_horizontally first).
    """
    arrows = VGroup()
    for a, b in zip(mobjects[:-1], mobjects[1:]):
        arrows.add(smart_arrow(a, b, chapter=chapter, color=color, buff=buff))
    return arrows


def orbit_point(center_mobject, radius: float = 1.0, color=None, chapter=None,
                 dot_radius: float = 0.06):
    """
    Place a small dot at a fixed radius from a center mobject's edge —
    useful for "possible outcomes around a point" style diagrams
    (like figure302's uncertainty rings) without hardcoding offsets.
    """
    color = color or get_color("accent", chapter=chapter)
    center = center_mobject.get_center()
    return Dot(center + RIGHT * radius, radius=dot_radius, color=color)
