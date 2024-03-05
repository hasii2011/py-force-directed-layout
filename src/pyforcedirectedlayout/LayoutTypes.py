
from typing import Any
from typing import Callable
from typing import List
from typing import NewType
from typing import TYPE_CHECKING

from dataclasses import dataclass

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from pyforcedirectedlayout.Node import Node

Nodes = NewType('Nodes', List['Node'])


@dataclass
class LayoutStatus:
    totalDisplacement: float = 0.0
    iterations:        int   = 0
    stopCount:         int   = 0
    maxIterations:     int   = 0


LayoutStatusCallback = Callable[[LayoutStatus], None]

DrawingContext = Any
"""
Purposely set to Any to avoid tying to a particular toolkit
"""
