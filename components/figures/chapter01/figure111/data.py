from dataclasses import dataclass


@dataclass
class Network:
    number: int
    name: str
    year: float
    parameters: float

    number_position: tuple[float, float]
    label_position: tuple[float, float]

    italic: bool = False


NETWORKS = [

    # --------------------------------------------------
    # Early networks
    # --------------------------------------------------

    Network(
        number=1,
        name="LeNet-5",
        year=1998,
        parameters=6e4,
        number_position=(1996.0, 1.8e5),
        label_position=(1996.0, 1.8e5),
    ),

    Network(
        number=2,
        name="AlexNet",
        year=2012,
        parameters=6e7,
        number_position=(2008.2, 1.3e8),
        label_position=(2008.2, 1.3e8),
    ),

    Network(
        number=3,
        name="ZFNet",
        year=2013,
        parameters=7e7,
        number_position=(2008.5, 8.0e7),
        label_position=(2008.5, 8.0e7),
    ),

    Network(
        number=4,
        name="VGG-16",
        year=2014,
        parameters=1.38e8,
        number_position=(2009.8, 2.8e8),
        label_position=(2009.8, 2.8e8),
    ),

    Network(
        number=5,
        name="GoogLeNet",
        year=2014,
        parameters=7e6,
        number_position=(2007.6, 2.0e7),
        label_position=(2007.6, 2.0e7),
    ),

    # --------------------------------------------------
    # Lower cluster
    # --------------------------------------------------

    Network(
        number=6,
        name="Speech MLP",
        year=1991,
        parameters=1e2,
        number_position=(1997.0, 4e4),
        label_position=(1997.0, 4e4),
    ),

    Network(
        number=7,
        name="Mean Field",
        year=1996,
        parameters=1e1,
        number_position=(2001.0, 3e4),
        label_position=(2001.0, 3e4),
    ),

    Network(
        number=8,
        name="LeNet-4",
        year=1990,
        parameters=8e1,
        number_position=(1996.0, 8e5),
        label_position=(1996.0, 8e5),
    ),

    Network(
        number=9,
        name="Echo State",
        year=2004,
        parameters=5e2,
        number_position=(2004.8, 6e4),
        label_position=(2004.8, 6e4),
    ),

    Network(
        number=10,
        name="Deep Belief",
        year=2006,
        parameters=3e3,
        number_position=(2007.2, 1.5e5),
        label_position=(2007.2, 1.5e5),
    ),

    # --------------------------------------------------
    # CNN era
    # --------------------------------------------------

    Network(
        number=11,
        name="GPU CNN",
        year=2006,
        parameters=8e5,
        number_position=(1996.0, 1.2e6),
        label_position=(1996.0, 1.2e6),
    ),

    Network(
        number=12,
        name="DBM",
        year=2009,
        parameters=6e4,
        number_position=(2008.6, 1.4e5),
        label_position=(2008.6, 1.4e5),
    ),

    Network(
        number=13,
        name="GPU DBN",
        year=2009,
        parameters=1e4,
        number_position=(2011.0, 4e5),
        label_position=(2011.0, 4e5),
    ),

    Network(
        number=14,
        name="UCNN",
        year=2009,
        parameters=1.2e6,
        number_position=(2002.2, 6e7),
        label_position=(2002.2, 6e7),
    ),

    Network(
        number=15,
        name="GPU MLP",
        year=2010,
        parameters=4e3,
        number_position=(2013.0, 1.2e5),
        label_position=(2013.0, 1.2e5),
    ),

    # --------------------------------------------------
    # Large models
    # --------------------------------------------------

    Network(
        number=16,
        name="OMP-1",
        year=2011,
        parameters=2e6,
        number_position=(1997.0, 4e8),
        label_position=(1997.0, 4e8),
    ),

    Network(
        number=17,
        name="DistBelief",
        year=2012,
        parameters=2.5e6,
        number_position=(1995.5, 1.8e9),
        label_position=(1995.5, 1.8e9),
    ),

    Network(
        number=18,
        name="Multi-GPU CNN",
        year=2012,
        parameters=1e6,
        number_position=(2011.5, 2.0e8),
        label_position=(2011.5, 2.0e8),
    ),

    Network(
        number=19,
        name="COTS HPC",
        year=2013,
        parameters=1.5e6,
        number_position=(2003.0, 8e8),
        label_position=(2003.0, 8e8),
    ),

    Network(
        number=20,
        name="GoogLeNet+",
        year=2014,
        parameters=1.8e6,
        number_position=(2008.0, 2.2e9),
        label_position=(2008.0, 2.2e9),
    ),
]