"""
common/palette.py

Locked color-to-concept mapping for Chapter 5+ (Machine Learning / Deep
Learning) animations. Import these constants everywhere instead of picking
colors ad hoc per scene, so the whole chapter reads as one consistent
visual language.

Usage:
    from common.palette import *
    # or
    from common import palette as pal
    pal.INPUT
"""

# --------------------------------------------------------------
# Base canvas
# --------------------------------------------------------------
BG = "#000000"          # background — black
TEXT = "#F5F7FA"         # primary body/heading text — near-white
TEXT_DIM = "#9AA7B5"     # secondary / caption text — muted gray-blue

# --------------------------------------------------------------
# Concept colors — meaning is fixed, reuse everywhere
# --------------------------------------------------------------
INPUT = "#4FD1FF"        # CYAN   — input / data / observed values / features
OUTPUT = "#65E572"       # GREEN  — correct output / clean / target / success
ERROR = "#FF6B6B"        # RED    — error / missing / anomaly / corrupted / loss
FORMULA = "#FFD166"      # YELLOW — key formulas / equations / highlighted terms
DISTRIBUTION = "#B388FF" # PURPLE — probability / distribution / uncertainty / density

# --------------------------------------------------------------
# Secondary / supporting accents (used sparingly, not core concepts)
# --------------------------------------------------------------
ACCENT_1 = "#FF9F6B"     # orange — secondary highlight / alternate path
ACCENT_2 = "#6BC9FF"     # light blue — secondary data stream / layer 2
ACCENT_3 = "#F06BD8"     # pink — rare/special emphasis, use very sparingly

# --------------------------------------------------------------
# Footer / chrome
# --------------------------------------------------------------
FOOTER_COLOR = OUTPUT    # "ML-xxx" footer stays green across the chapter
CHAPTER_TAG_COLOR = INPUT  # "CHAPTER 5" tag stays cyan

# --------------------------------------------------------------
# Semantic aliases (optional, improves readability at call sites)
# --------------------------------------------------------------
COLOR_DATA = INPUT
COLOR_RESULT = OUTPUT
COLOR_MISSING = ERROR
COLOR_EQUATION = FORMULA
COLOR_PROBABILITY = DISTRIBUTION

# --------------------------------------------------------------
# Quick reference (for humans editing this file)
# --------------------------------------------------------------
# INPUT        (cyan)   -> data, features, x, raw input, "what goes in"
# OUTPUT       (green)  -> correct answers, clean data, targets, success states
# ERROR        (red)    -> missing values, anomalies, corruption, loss, mistakes
# FORMULA      (yellow) -> equations, key terms worth highlighting
# DISTRIBUTION (purple) -> probability, p(x), uncertainty, density estimation
