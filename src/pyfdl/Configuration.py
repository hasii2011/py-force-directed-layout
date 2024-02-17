
from dataclasses import dataclass


@dataclass
class Configuration:

    # these are for the arrange method
    damping:       float = 0.5
    springLength:  int   = 100
    maxIterations: int   = 500

    # these randomize the layout
    minRandomX: int = 10
    maxRandomX: int = 60
    minRandomY: int = 10
    maxRandomY: int = 60

    #
    attractionFactor: float = 0.1
    repulsionFactor:  float = 10000

    minimumTotalDisplacement: int = 10
    stopCount:                int = 15
    """
    Stop execution after this many number of iterations
    where the totalDisplacement is less that minimumTotalDisplacement
    """
