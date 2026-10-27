from dataclasses import dataclass


@dataclass
class Network:
    number: int
    name: str
    year: float
    connections: float

    number_position: tuple[float, float]
    label_position: tuple[float, float]

    italic: bool = False


@dataclass
class Animal:
    name: str
    connections: float


NETWORKS = [

    Network(
        1,
        "Adaptive linear element",
        1960,
        15,
        (1952, 40),
        (1952, 40),
    ),

    Network(
        2,
        "Neocognitron",
        1980,
        250,
        (1973, 700),
        (1973, 700),
    ),

    Network(
        3,
        "GPU CNN",
        2006,
        28,
        (1999, 70),
        (1999, 70),
    ),

    Network(
        4,
        "Deep Boltzmann",
        2009,
        550,
        (2000, 1400),
        (2000, 1400),
    ),

    Network(
        5,
        "UCNN",
        2009,
        320,
        (2001, 300),
        (2001, 300),
    ),

    Network(
        6,
        "GPU MLP",
        2010,
        1200,
        (2002, 3500),
        (2002, 3500),
    ),

    Network(
        7,
        "DistBelief",
        2012,
        900,
        (2018, 3000),
        (2018, 3000),
    ),

    Network(
        8,
        "Multi-GPU CNN",
        2012,
        90,
        (2005, 130),
        (2005, 130),
    ),

    Network(
        9,
        "COTS HPC",
        2013,
        9000,
        (2013, 2500),
        (2013, 2500),
    ),

    Network(
        10,
        "GoogLeNet",
        2014,
        450,
        (2018, 400),
        (2018, 400),
    ),
]


ANIMALS = [

    Animal("Human", 9000),
    Animal("Cat", 5000),
    Animal("Mouse", 1200),
    Animal("Fruit fly", 100),
]