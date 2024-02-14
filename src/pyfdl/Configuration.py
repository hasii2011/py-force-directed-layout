
from dataclasses import dataclass


@dataclass
class Configuration:

    damping:       float = 0.5
    springLength:  int   = 100
    maxIterations: int   = 500

    minRandomX: int = 10
    maxRandomX: int = 60
    minRandomY: int = 10
    maxRandomY: int = 60
