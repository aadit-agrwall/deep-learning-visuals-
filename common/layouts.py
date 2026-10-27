"""
common/layouts.py

Reusable layout helpers and presets for positioning mobjects on
screen. Presets cover the most common figure/scene structures;
low-level helpers let scenes compose custom arrangements when a
preset doesn't fit.
"""

from manim import (
    VGroup, UP, DOWN, LEFT, RIGHT, ORIGIN,
    config,
)

FRAME_WIDTH = config.frame_width
FRAME_HEIGHT = config.frame_height


def stack_vertically(mobjects, buff: float = 0.35, center: bool = True):
    """Arrange mobjects top-to-bottom with even spacing."""
    group = VGroup(*mobjects).arrange(DOWN, buff=buff)
    if center:
        group.move_to(ORIGIN)
    return group


def stack_horizontally(mobjects, buff: float = 0.35, center: bool = True):
    """Arrange mobjects left-to-right with even spacing."""
    group = VGroup(*mobjects).arrange(RIGHT, buff=buff)
    if center:
        group.move_to(ORIGIN)
    return group


def align_to_grid(mobjects, rows: int, cols: int, h_buff: float = 0.5, v_buff: float = 0.5):
    """Arrange mobjects into a rows x cols grid."""
    group = VGroup(*mobjects).arrange_in_grid(rows=rows, cols=cols, buff=(h_buff, v_buff))
    group.move_to(ORIGIN)
    return group


def anchor_region(width_frac: float, height_frac: float, position=ORIGIN):
    """Return (width, height) of a screen region as a fraction of the full frame."""
    return FRAME_WIDTH * width_frac, FRAME_HEIGHT * height_frac


def title_top_content_center(title_mobject, content_mobject, title_buff: float = 0.6):
    """Title pinned near the top, content centered below it."""
    title_mobject.to_edge(UP, buff=0.5)
    content_mobject.next_to(title_mobject, DOWN, buff=title_buff)
    content_mobject.move_to([0, content_mobject.get_y(), 0])
    return VGroup(title_mobject, content_mobject)


def split_left_right(left_mobject, right_mobject, buff: float = 1.0, ratio: float = 0.5):
    """Two mobjects side by side (e.g. equation vs. diagram)."""
    left_mobject.move_to(LEFT * (FRAME_WIDTH * ratio / 2))
    right_mobject.next_to(left_mobject, RIGHT, buff=buff)
    return VGroup(left_mobject, right_mobject)


def grid_layout(mobjects, rows: int = None, cols: int = None, buff: float = 0.5):
    """Arrange N mobjects into an auto-sized grid if rows/cols aren't given."""
    n = len(mobjects)
    if rows is None and cols is None:
        cols = max(1, round(n ** 0.5))
        rows = -(-n // cols)
    elif rows is None:
        rows = -(-n // cols)
    elif cols is None:
        cols = -(-n // rows)
    return align_to_grid(mobjects, rows=rows, cols=cols, h_buff=buff, v_buff=buff)


def title_top_split_bottom(title_mobject, left_mobject, right_mobject, title_buff: float = 0.6, split_buff: float = 1.0):
    """Title at top, two panels split left/right below it."""
    title_mobject.to_edge(UP, buff=0.5)
    row = split_left_right(left_mobject, right_mobject, buff=split_buff)
    row.next_to(title_mobject, DOWN, buff=title_buff)
    row.move_to([0, row.get_y(), 0])
    return VGroup(title_mobject, row)


# ==========================================================
# Overlap-safe arrangement helpers
# ==========================================================

def flow_row(mobjects, buff: float = 0.6, center: bool = True):
    """
    Arrange mobjects left-to-right using each object's ACTUAL width,
    guaranteeing no overlap regardless of content size (unlike manual
    move_to(LEFT * N) placement, which breaks if content size changes).
    """
    group = VGroup(*mobjects).arrange(RIGHT, buff=buff, aligned_edge=UP)
    if center:
        group.move_to(ORIGIN)
    return group


def flow_column(mobjects, buff: float = 0.5, center: bool = True):
    """
    Arrange mobjects top-to-bottom using each object's ACTUAL height,
    guaranteeing no overlap regardless of content size.
    """
    group = VGroup(*mobjects).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    if center:
        group.move_to(ORIGIN)
    return group


def fit_in_frame(mobject, margin: float = 0.5):
    """
    Scale a mobject down (never up) if it would exceed the visible
    frame minus a safety margin, preventing content from running off
    screen. Returns the (possibly rescaled) mobject.
    """
    max_width = FRAME_WIDTH - margin * 2
    max_height = FRAME_HEIGHT - margin * 2
    scale_factor = min(max_width / mobject.width, max_height / mobject.height, 1.0)
    if scale_factor < 1.0:
        mobject.scale(scale_factor)
    return mobject


def no_overlap_offset(mobject_a, mobject_b, min_gap: float = 0.2):
    """
    Check whether two mobjects' bounding boxes overlap (or are closer
    than min_gap) and, if so, return the horizontal shift needed to
    separate them cleanly. Returns 0.0 if no adjustment is needed.
    """
    a_right = mobject_a.get_right()[0]
    b_left = mobject_b.get_left()[0]
    gap = b_left - a_right
    if gap >= min_gap:
        return 0.0
    return min_gap - gap
