"""
common/components.py

Generic, reusable visual building blocks that aren't specific to
math/ML objects or charts: titled boxes, callouts, equation frames,
bullet lists, and legends. Domain-specific components live in
components/ instead (matrix, vector, neural_network, charts, graph).
"""

from manim import (
    VGroup, Rectangle, RoundedRectangle, Text, Dot, Line,
    UP, DOWN, LEFT, RIGHT, ORIGIN,
)

from common.styles import text_style, stroke_width, spacing
from common.colors import get_color


def titled_box(title: str, content_mobject, chapter: str = None, width: float = None, height: float = None, corner_radius: float = 0.15):
    """
    Wrap a mobject in a rounded rectangle with a title above it —
    common pattern for callouts, definitions, or grouped figures.
    """
    width = width or (content_mobject.width + 1.0)
    height = height or (content_mobject.height + 1.2)
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        color=get_color("primary", chapter=chapter),
        stroke_width=stroke_width("default"),
    )
    title_text = Text(title, **text_style("subtitle", chapter=chapter))
    title_text.next_to(box, UP, buff=0.2)
    content_mobject.move_to(box.get_center())
    return VGroup(box, title_text, content_mobject)


def callout_box(text: str, chapter: str = None, width: float = 5.0):
    """Small highlighted note box, e.g. for asides or definitions."""
    body = Text(text, **text_style("body", chapter=chapter))
    body.set(width=min(body.width, width - 0.6))
    box = RoundedRectangle(
        width=body.width + 0.6,
        height=body.height + 0.6,
        corner_radius=0.12,
        color=get_color("accent", chapter=chapter),
        fill_color=get_color("background", chapter=chapter),
        fill_opacity=0.85,
        stroke_width=stroke_width("default"),
    )
    body.move_to(box.get_center())
    return VGroup(box, body)


def equation_box(equation_tex, chapter: str = None, padding: float = 0.5):
    """Frame a MathTex/Tex equation in a bordered box."""
    box = Rectangle(
        width=equation_tex.width + padding * 2,
        height=equation_tex.height + padding * 2,
        color=get_color("secondary", chapter=chapter),
        stroke_width=stroke_width("default"),
    )
    equation_tex.move_to(box.get_center())
    return VGroup(box, equation_tex)


def bullet_list(items, chapter: str = None, bullet_char: str = "•", buff: float = None):
    """Vertical list of bulleted text lines."""
    buff = buff or spacing("default")
    lines = VGroup()
    for item in items:
        line = Text(f"{bullet_char}  {item}", **text_style("body", chapter=chapter))
        lines.add(line)
    lines.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return lines


def legend(entries, chapter: str = None, dot_radius: float = 0.08, buff: float = None):
    """
    Build a simple color-key legend from a list of (label, color)
    tuples, e.g. legend([("Predicted", RED), ("Actual", BLUE)]).
    """
    buff = buff or spacing("tight")
    rows = VGroup()
    for label, color in entries:
        dot = Dot(radius=dot_radius, color=color)
        text = Text(label, **text_style("caption", chapter=chapter))
        text.next_to(dot, RIGHT, buff=0.2)
        rows.add(VGroup(dot, text))
    rows.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return rows


def divider_line(width: float = 6.0, chapter: str = None):
    """A simple horizontal divider line, e.g. between sections of a figure."""
    return Line(LEFT * width / 2, RIGHT * width / 2, color=get_color("subtext", chapter=chapter))
