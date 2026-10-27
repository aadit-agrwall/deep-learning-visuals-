"""
common/math_objects.py

Higher-level, reusable compositions built on top of the existing
components.matrix.Matrix2D and components.vector.Vector2D classes.
Does NOT reimplement matrix/vector construction — only adds common
animation patterns and labeled compositions that scenes repeat.
"""

from manim import VGroup, Write, FadeIn, Text, Arrow, ORIGIN, UP, DOWN

from common.styles import text_style
from common.colors import get_color


def labeled_matrix(matrix_mobject, label: str, chapter: str = None, label_buff: float = 0.4):
    """
    Attach a text label above a Matrix2D instance.
    `matrix_mobject` is an already-constructed Matrix2D.
    """
    label_text = Text(label, **text_style("label", chapter=chapter))
    label_text.next_to(matrix_mobject, UP, buff=label_buff)
    return VGroup(label_text, matrix_mobject)


def labeled_vector(vector_mobject, label: str, chapter: str = None, label_buff: float = 0.3):
    """Attach a text label near a Vector2D instance's tip."""
    label_text = Text(label, **text_style("label", chapter=chapter))
    label_text.next_to(vector_mobject, UP, buff=label_buff)
    return VGroup(label_text, vector_mobject)


def show_matrix(scene, matrix_mobject, run_time: float = 1.0):
    """Standard reveal animation for a matrix (wraps its own create_animation)."""
    scene.play(matrix_mobject.create_animation(), run_time=run_time)


def highlight_matrix_diagonal(matrix_mobject, chapter: str = None, color=None):
    """
    Highlight the diagonal entries of a square Matrix2D using
    its existing highlight_element(row, col) method.
    """
    data = matrix_mobject.get_data()
    n = min(len(data), len(data[0]) if data else 0)
    color = color or get_color("accent", chapter=chapter)
    animations = []
    for i in range(n):
        matrix_mobject.highlight_element(i, i, color=color)
    return matrix_mobject


def matrix_transform_arrow(source_matrix, target_matrix, chapter: str = None):
    """
    Return an Arrow mobject connecting two matrices, useful for
    depicting a transformation/multiplication step (A -> B).
    """
    color = get_color("primary", chapter=chapter)
    return Arrow(
        start=source_matrix.get_right(),
        end=target_matrix.get_left(),
        color=color,
        buff=0.3,
    )


def vector_pair(vector_a, vector_b, gap: float = 1.5):
    """
    Position two Vector2D instances side by side (e.g. for showing
    addition/dot-product operands before combining them).
    """
    vector_a.move_to(ORIGIN)
    vector_b.next_to(vector_a, DOWN, buff=gap)
    return VGroup(vector_a, vector_b)


def equation_with_result(equation_tex, result_mobject, chapter: str = None, buff: float = 0.6):
    """
    Common pattern: a Tex/MathTex equation on the left, its visual
    result (matrix, vector, scalar text, etc.) on the right.
    """
    result_mobject.next_to(equation_tex, DOWN, buff=buff)
    return VGroup(equation_tex, result_mobject)
