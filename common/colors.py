"""
common/colors.py

Central color system for DPVisual.

Design rule:
  - TEXT and SUBTEXT are GLOBAL — identical across every chapter.
  - BACKGROUND is PER-CHAPTER — chapters follow an alternating
    blue / black pattern (chapter03 = blue, chapters 04-05 = black,
    chapter06 = blue, ...).
  - PRIMARY / SECONDARY / ACCENT / WARNING / MATRIX / VECTOR / NEURON /
    WEIGHT remain PER-CHAPTER as before.
"""

from manim import (
    BLUE_D, BLUE_E, GREEN_D, GREEN_E, YELLOW_D, RED_D,
    WHITE, GREY_B,
    TEAL_D, ORANGE, PURPLE_D, PURPLE_E, PINK, MAROON_D, MAROON_E,
    GOLD_D, GOLD_E, interpolate_color,
)

# ==========================================================
# GLOBAL colors — identical across every chapter.
# ==========================================================

TEXT = WHITE
SUBTEXT = GREY_B

GLOBAL_COLORS = {
    "text": TEXT,
    "subtext": SUBTEXT,
}

# ==========================================================
# Background pattern (per chapter)
# ==========================================================

BG_BLACK = "#111111"
BG_BLUE = "#04244E"   # matches existing figure301/figure302

_PALETTE_KEYS = [
    "background", "primary", "secondary", "accent", "warning",
    "matrix", "vector", "neuron", "weight",
]

# ==========================================================
# PER-CHAPTER palettes.
# ==========================================================

CHAPTER_PALETTES = {
    "chapter01": {
        "background": BG_BLACK,
        "primary": BLUE_D,
        "secondary": GREEN_D,
        "accent": YELLOW_D,
        "warning": RED_D,
        "matrix": BLUE_E,
        "vector": GREEN_E,
        "neuron": TEAL_D,
        "weight": ORANGE,
    },
    "chapter02": {
        "background": BG_BLACK,
        "primary": PURPLE_D,
        "secondary": TEAL_D,
        "accent": GOLD_D,
        "warning": RED_D,
        "matrix": PURPLE_E,
        "vector": TEAL_D,
        "neuron": GOLD_E,
        "weight": PINK,
    },
    "chapter03": {
        # Sourced from existing scenes/chapter03/figure301.py, figure302.py
        "background": BG_BLUE,
        "primary": "#55D6FF",      # CYAN
        "secondary": "#65E572",    # GREEN
        "accent": "#FFD166",       # YELLOW
        "warning": "#FF6B6B",      # RED
        "matrix": "#B9D7F2",       # BLUE_TEXT
        "vector": "#65E572",       # reuses GREEN
        "neuron": "#8FAEC9",       # SOFT
        "weight": "#FFD166",       # reuses YELLOW
    },
    "chapter04": {
        "background": BG_BLACK,
        "primary": MAROON_D,
        "secondary": BLUE_D,
        "accent": GOLD_D,
        "warning": RED_D,
        "matrix": MAROON_E,
        "vector": BLUE_E,
        "neuron": GOLD_E,
        "weight": ORANGE,
    },
    "chapter05": {
        "background": BG_BLACK,
        "primary": TEAL_D,
        "secondary": PURPLE_D,
        "accent": YELLOW_D,
        "warning": RED_D,
        "matrix": BLUE_E,
        "vector": GREEN_E,
        "neuron": PURPLE_E,
        "weight": PINK,
    },
    "chapter06": {
        "background": BG_BLUE,
        "primary": BLUE_D,
        "secondary": TEAL_D,
        "accent": GOLD_D,
        "warning": RED_D,
        "matrix": BLUE_E,
        "vector": TEAL_D,
        "neuron": GOLD_E,
        "weight": ORANGE,
    },
}

DEFAULT_PALETTE = dict(CHAPTER_PALETTES["chapter01"])


def _validate_palettes():
    for chapter, palette in CHAPTER_PALETTES.items():
        missing = set(_PALETTE_KEYS) - set(palette.keys())
        if missing:
            raise ValueError(f"CHAPTER_PALETTES['{chapter}'] is missing keys: {missing}")


_validate_palettes()


# ==========================================================
# Resolution logic
# ==========================================================

def get_color(name: str, chapter: str = None, theme=None):
    key = name.lower()

    if theme is not None:
        attr = name.upper()
        if hasattr(theme, attr):
            return getattr(theme, attr)

    if key in GLOBAL_COLORS:
        return GLOBAL_COLORS[key]

    if chapter is not None:
        chapter_key = chapter.lower()
        if chapter_key in CHAPTER_PALETTES:
            palette = CHAPTER_PALETTES[chapter_key]
            if key in palette:
                return palette[key]
            raise KeyError(f"'{name}' is not a valid palette key. Available: {_PALETTE_KEYS}")
        raise KeyError(
            f"Unknown chapter '{chapter}'. Registered chapters: {list(CHAPTER_PALETTES.keys())}"
        )

    if key in DEFAULT_PALETTE:
        return DEFAULT_PALETTE[key]

    raise KeyError(
        f"Unknown color '{name}'. Global: {list(GLOBAL_COLORS)}, Palette keys: {_PALETTE_KEYS}"
    )


def get_palette(chapter: str = None) -> dict:
    palette = dict(GLOBAL_COLORS)
    if chapter is not None:
        chapter_key = chapter.lower()
        if chapter_key not in CHAPTER_PALETTES:
            raise KeyError(
                f"Unknown chapter '{chapter}'. Registered chapters: {list(CHAPTER_PALETTES.keys())}"
            )
        palette.update(CHAPTER_PALETTES[chapter_key])
    else:
        palette.update(DEFAULT_PALETTE)
    return palette


def blend(color_a, color_b, alpha: float = 0.5):
    return interpolate_color(color_a, color_b, alpha)


def with_opacity_hint(color, level: str = "medium"):
    levels = {"faint": 0.15, "low": 0.35, "medium": 0.6, "high": 0.85, "full": 1.0}
    if level not in levels:
        raise KeyError(f"Unknown opacity level '{level}'. Available: {list(levels)}")
    return color, levels[level]


def palette_sequence(n: int, chapter: str = None, theme=None):
    order = ["primary", "secondary", "accent", "matrix", "vector", "neuron", "weight"]
    colors = [get_color(name, chapter=chapter, theme=theme) for name in order]
    if n <= len(colors):
        return colors[:n]
    return [colors[i % len(colors)] for i in range(n)]
