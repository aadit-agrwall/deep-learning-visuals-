"""
common/helpers.py

Small, general-purpose helper functions used across scenes and
components.
"""

from manim import VGroup, FadeIn, FadeOut, Write, Create


def fade_in_sequence(mobjects, lag_ratio: float = 0.15, run_time: float = 1.0):
    """Return a single animation that fades in a list of mobjects in sequence."""
    return FadeIn(VGroup(*mobjects), lag_ratio=lag_ratio, run_time=run_time)


def fade_out_all(scene, run_time: float = 1.0):
    """Fade out every mobject currently on scene.mobjects."""
    if scene.mobjects:
        scene.play(FadeOut(VGroup(*scene.mobjects)), run_time=run_time)


def write_sequence(mobjects, lag_ratio: float = 0.2, run_time: float = 1.5):
    """Return a single animation that writes text/tex mobjects in sequence."""
    return Write(VGroup(*mobjects), lag_ratio=lag_ratio, run_time=run_time)


def create_sequence(mobjects, lag_ratio: float = 0.2, run_time: float = 1.5):
    """Return a single animation that draws (Create) mobjects in sequence."""
    return Create(VGroup(*mobjects), lag_ratio=lag_ratio, run_time=run_time)


def safe_get(dictionary: dict, key, default=None):
    """Dict lookup that never raises, for optional config values."""
    return dictionary.get(key, default)


def clamp(value: float, low: float, high: float) -> float:
    """Clamp a numeric value into [low, high]."""
    return max(low, min(high, value))


def chunk(iterable, size: int):
    """Split an iterable into chunks of at most `size` items."""
    items = list(iterable)
    return [items[i:i + size] for i in range(0, len(items), size)]
