"""
common/utils.py

Project-wide, non-Manim utility functions.
"""

import re


def format_number(value: float, decimals: int = 2, thousands_sep: bool = True) -> str:
    """Format a number for on-screen display, e.g. format_number(15342.5) -> '15,342.50'."""
    fmt = f"{{:,.{decimals}f}}" if thousands_sep else f"{{:.{decimals}f}}"
    return fmt.format(value)


def slugify(text: str) -> str:
    """Convert a title/label into a filesystem- and id-safe slug."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def validate_chapter_name(chapter: str) -> str:
    """Normalize a chapter identifier like 'chapter01', 'Chapter 1', or 'ch1' into 'chapterNN'."""
    match = re.search(r"(\d+)", chapter)
    if not match:
        raise ValueError(f"Could not parse a chapter number from '{chapter}'")
    number = int(match.group(1))
    return f"chapter{number:02d}"


def is_valid_figure_id(figure_id: str) -> bool:
    """Check whether a figure id matches the project's NNN convention (e.g. '110', '217')."""
    return bool(re.fullmatch(r"\d{3}", figure_id))
