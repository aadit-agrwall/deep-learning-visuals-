"""
Figure 1.10

Estimated number of synaptic connections per neuron
across different species.

This file contains ONLY data.

No Manim objects should be created here.
"""

from dataclasses import dataclass
from typing import Tuple


# ==========================================================
# Data Structures
# ==========================================================

@dataclass(frozen=True)
class SpeciesPoint:
    """
    One point in the figure.
    """

    id: int

    species: str

    year: int

    connections: float

    label_position: Tuple[float, float]

    italic: bool = False


# ==========================================================
# Axis Configuration
# ==========================================================

X_RANGE = [1950, 2015, 10]

Y_MIN = 10
Y_MAX = 10000

YEAR_TICKS = [
    1950,
    1960,
    1970,
    1980,
    1990,
    2000,
    2010,
]

LOG_TICKS = [
    10,
    100,
    1000,
    10000,
]


# ==========================================================
# Species Data
# ==========================================================

SPECIES = [

    SpeciesPoint(
        id=1,
        species="Human",
        year=2015,
        connections=1000,
        label_position=(2008, 2500),
    ),

    SpeciesPoint(
        id=2,
        species="Cat",
        year=1995,
        connections=700,
        label_position=(1987, 1200),
    ),

    SpeciesPoint(
        id=3,
        species="Mouse",
        year=1984,
        connections=300,
        label_position=(1975, 520),
    ),

    SpeciesPoint(
        id=4,
        species="Rat",
        year=1976,
        connections=220,
        label_position=(1967, 360),
    ),

    SpeciesPoint(
        id=5,
        species="Rabbit",
        year=1972,
        connections=150,
        label_position=(1962, 220),
    ),

    SpeciesPoint(
        id=6,
        species="Frog",
        year=1967,
        connections=95,
        label_position=(1958, 135),
    ),

    SpeciesPoint(
        id=7,
        species="Fish",
        year=1964,
        connections=70,
        label_position=(1955, 95),
    ),

    SpeciesPoint(
        id=8,
        species="Insect",
        year=1960,
        connections=40,
        label_position=(1952, 58),
    ),

    SpeciesPoint(
        id=9,
        species="Fruit fly",
        year=1957,
        connections=22,
        label_position=(1951, 30),
        italic=True,
    ),

    SpeciesPoint(
        id=10,
        species="Nematode",
        year=1953,
        connections=12,
        label_position=(1950, 16),
        italic=True,
    ),

]


# ==========================================================
# Caption
# ==========================================================

CAPTION = (
    "Figure 1.10  Estimated number of synaptic connections "
    "per neuron in selected species."
)