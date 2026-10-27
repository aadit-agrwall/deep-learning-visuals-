"""
common/styles.py

Central style constants for DPVisual: font sizes, stroke widths,
spacing, and animation timing. These are GLOBAL — identical across
every chapter, per project design (only colors vary by chapter).
"""

from common.colors import get_color

# ==========================================================
# Font sizes (global)
# ==========================================================

FONT_SIZES = {
    "title": 48,
    "subtitle": 32,
    "body": 28,
    "math": 38,
    "caption": 22,
    "label": 24,
}


def font_size(name: str) -> int:
    key = name.lower()
    if key not in FONT_SIZES:
        raise KeyError(f"Unknown font size '{name}'. Available: {list(FONT_SIZES)}")
    return FONT_SIZES[key]


# ==========================================================
# Stroke / line weights (global)
# ==========================================================

STROKE_WIDTHS = {
    "thin": 1.5,
    "default": 2.5,
    "bold": 4.0,
    "heavy": 6.0,
}


def stroke_width(name: str = "default") -> float:
    key = name.lower()
    if key not in STROKE_WIDTHS:
        raise KeyError(f"Unknown stroke width '{name}'. Available: {list(STROKE_WIDTHS)}")
    return STROKE_WIDTHS[key]


# ==========================================================
# Spacing / layout constants (global)
# ==========================================================

SPACING = {
    "tight": 0.15,
    "default": 0.35,
    "loose": 0.6,
    "section": 1.0,
}


def spacing(name: str = "default") -> float:
    key = name.lower()
    if key not in SPACING:
        raise KeyError(f"Unknown spacing '{name}'. Available: {list(SPACING)}")
    return SPACING[key]


# ==========================================================
# Animation timing (global — same pacing for every chapter)
# ==========================================================

RUNTIMES = {
    "fast": 0.5,
    "default": 1.0,
    "slow": 2.0,
}


def runtime(name: str = "default") -> float:
    key = name.lower()
    if key not in RUNTIMES:
        raise KeyError(f"Unknown runtime '{name}'. Available: {list(RUNTIMES)}")
    return RUNTIMES[key]


# ==========================================================
# Composite style presets
# `chapter` controls which color palette is used; font/stroke/
# spacing/runtime values themselves never change per chapter.
# ==========================================================

def text_style(kind: str = "body", chapter: str = None, theme=None) -> dict:
    """
    kwargs dict for Manim Text/Tex, e.g.:
        Text("Hello", **text_style("title", chapter="chapter02"))
    """
    presets = {
        "title": {"font_size": font_size("title"), "color": get_color("text", chapter, theme)},
        "subtitle": {"font_size": font_size("subtitle"), "color": get_color("subtext", chapter, theme)},
        "body": {"font_size": font_size("body"), "color": get_color("text", chapter, theme)},
        "math": {"font_size": font_size("math"), "color": get_color("text", chapter, theme)},
        "caption": {"font_size": font_size("caption"), "color": get_color("subtext", chapter, theme)},
        "label": {"font_size": font_size("label"), "color": get_color("text", chapter, theme)},
    }
    key = kind.lower()
    if key not in presets:
        raise KeyError(f"Unknown text style '{kind}'. Available: {list(presets)}")
    return presets[key]


def line_style(kind: str = "default", chapter: str = None, theme=None) -> dict:
    """kwargs dict for Line/Arrow/VMobject stroke styling."""
    presets = {
        "default": {"stroke_width": stroke_width("default"), "color": get_color("primary", chapter, theme)},
        "accent": {"stroke_width": stroke_width("bold"), "color": get_color("accent", chapter, theme)},
        "subtle": {"stroke_width": stroke_width("thin"), "color": get_color("subtext", chapter, theme)},
    }
    key = kind.lower()
    if key not in presets:
        raise KeyError(f"Unknown line style '{kind}'. Available: {list(presets)}")
    return presets[key]
