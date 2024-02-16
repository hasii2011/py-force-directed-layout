
from typing import List
from typing import NewType

from dataclasses import dataclass

from pyfdl.Node import Node
from pyfdl.Point import Point
from pyfdl.Vector import Vector


@dataclass
class NodeLayoutInformation:
    """
    Tracks the mechanical properties (velocity, future coordinates) of each node during the
    force-based simulation.
    """

    node:         Node
    """
    reference to the node in the simulation
    """
    velocity:     Vector
    """
    the node's current velocity, expressed in vector form
    """
    nextPosition: Point
    """
    the node's position after the next iteration
    """


NodeLayoutInformationList = NewType('NodeLayoutInformationList', List[NodeLayoutInformation])
