"""
common/animations.py

Reusable animation patterns (transitions, emphasis, reveals) that
scenes can call instead of writing raw Manim animation calls inline.
Complements common/helpers.py (which has simpler sequence wrappers)
with more opinionated, higher-level effects.
"""

from manim import (
    Indicate, Flash, Circumscribe, Wiggle, ApplyWave,
    FadeIn, FadeOut, Transform, ReplacementTransform,
    VGroup, YELLOW,
)

from common.colors import get_color
from common.styles import runtime


def emphasize(scene, mobject, chapter: str = None, run_time: float = None):
    """Draw attention to a mobject with a color pulse (Indicate)."""
    color = get_color("accent", chapter=chapter)
    scene.play(Indicate(mobject, color=color), run_time=run_time or runtime("default"))


def flash_point(scene, point, chapter: str = None, run_time: float = None):
    """Flash effect at a specific point (e.g. to mark a highlight)."""
    color = get_color("accent", chapter=chapter)
    scene.play(Flash(point, color=color), run_time=run_time or runtime("fast"))


def circle_highlight(scene, mobject, chapter: str = None, run_time: float = None):
    """Draw a temporary circle/box around a mobject to call it out."""
    color = get_color("primary", chapter=chapter)
    scene.play(Circumscribe(mobject, color=color), run_time=run_time or runtime("default"))


def wiggle_attention(scene, mobject, run_time: float = None):
    """Wiggle a mobject to draw the eye without changing its color."""
    scene.play(Wiggle(mobject), run_time=run_time or runtime("default"))


def morph(scene, source_mobject, target_mobject, run_time: float = None, replace: bool = True):
    """
    Morph one mobject into another. Uses ReplacementTransform by
    default (source is removed from the scene); pass replace=False
    to keep both objects tracked (Transform).
    """
    anim_cls = ReplacementTransform if replace else Transform
    scene.play(anim_cls(source_mobject, target_mobject), run_time=run_time or runtime("default"))


def reveal_sequence(scene, mobjects, lag_ratio: float = 0.2, run_time: float = None):
    """Fade in a list of mobjects one after another with a stagger."""
    scene.play(
        FadeIn(VGroup(*mobjects), lag_ratio=lag_ratio),
        run_time=run_time or runtime("slow"),
    )


def dismiss_sequence(scene, mobjects, lag_ratio: float = 0.15, run_time: float = None):
    """Fade out a list of mobjects one after another with a stagger."""
    scene.play(
        FadeOut(VGroup(*mobjects), lag_ratio=lag_ratio),
        run_time=run_time or runtime("default"),
    )


def transition_scene(scene, old_mobjects, new_mobjects, run_time: float = None):
    """
    Standard scene-to-scene transition: fade out everything old,
    then fade in everything new. Useful between figure "beats".
    """
    rt = run_time or runtime("default")
    if old_mobjects:
        scene.play(FadeOut(VGroup(*old_mobjects)), run_time=rt)
    if new_mobjects:
        scene.play(FadeIn(VGroup(*new_mobjects)), run_time=rt)


# ==========================================================
# Choreographed reveal patterns
# (smoother, staggered, eased — for polished figure builds)
# ==========================================================

from manim import GrowArrow, GrowFromCenter, rate_functions, AnimationGroup


def build_flow_sequence(scene, boxes, arrows, box_run_time=0.5, arrow_run_time=0.6,
                          stagger=0.15):
    """
    Reveal a chain of boxes and connecting arrows one step at a time,
    left to right: box1 grows in -> arrow1 grows -> box2 grows in ->
    arrow2 grows -> ... This reads as a deliberate, guided sequence
    rather than everything appearing simultaneously.

    `boxes` and `arrows` must satisfy len(arrows) == len(boxes) - 1.
    """
    if len(arrows) != len(boxes) - 1:
        raise ValueError("arrows must have exactly len(boxes) - 1 items")

    scene.play(
        GrowFromCenter(boxes[0], rate_func=rate_functions.ease_out_back),
        run_time=box_run_time,
    )
    for box, arrow in zip(boxes[1:], arrows):
        scene.play(GrowArrow(arrow, rate_func=rate_functions.ease_out_cubic), run_time=arrow_run_time)
        scene.play(
            GrowFromCenter(box, rate_func=rate_functions.ease_out_back),
            run_time=box_run_time,
        )
        scene.wait(stagger)


def staggered_fade_in(scene, mobjects, run_time=1.2, lag_ratio=0.2,
                        rate_func=rate_functions.ease_out_cubic):
    """
    Fade in a list of mobjects with a gentle overlapping stagger and
    eased timing, instead of a flat simultaneous or linear reveal.
    """
    from manim import FadeIn, VGroup
    scene.play(
        FadeIn(VGroup(*mobjects), lag_ratio=lag_ratio, rate_func=rate_func),
        run_time=run_time,
    )


def emphasize_then_settle(scene, mobject, chapter=None, pulse_time=0.4, settle_time=0.3):
    """
    Slightly overshoot-scale a mobject then settle back to size —
    gives new content a sense of weight/arrival instead of popping
    in flat. Good for a key result, final answer, or headline term.
    """
    scene.play(
        mobject.animate.scale(1.12),
        rate_func=rate_functions.ease_out_back,
        run_time=pulse_time,
    )
    scene.play(
        mobject.animate.scale(1 / 1.12),
        rate_func=rate_functions.ease_in_out_sine,
        run_time=settle_time,
    )


def cross_dissolve(scene, old_mobjects, new_mobjects, run_time=1.0):
    """
    Smooth cross-fade: old content fades out WHILE new content fades
    in, rather than a hard sequential fade-out-then-fade-in (which
    can feel like a jarring blank-screen flash).
    """
    from manim import FadeOut, FadeIn, VGroup, AnimationGroup
    animations = []
    if old_mobjects:
        animations.append(FadeOut(VGroup(*old_mobjects), rate_func=rate_functions.ease_in_cubic))
    if new_mobjects:
        animations.append(FadeIn(VGroup(*new_mobjects), rate_func=rate_functions.ease_out_cubic))
    if animations:
        scene.play(AnimationGroup(*animations, lag_ratio=0.0), run_time=run_time)
