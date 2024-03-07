
from typing import TYPE_CHECKING
from typing import cast


from logging import Logger
from logging import getLogger

from abc import ABC
from abc import abstractmethod

from pyforcedirectedlayout.LayoutTypes import DrawingContext

from pyforcedirectedlayout.Point import Point
from pyforcedirectedlayout.Size import Size

if TYPE_CHECKING:
    from pyforcedirectedlayout.ForceDirectedLayout import ForceDirectedLayout

from pyforcedirectedlayout.LayoutTypes import Nodes


class Node(ABC):
    """
    I hate cyclical dependencies
    Node is the base class for a node on a diagram.
    """
    def __init__(self):

        self.nodeLogger: Logger = getLogger(__name__)

        self._layoutEngine: 'ForceDirectedLayout' = cast('ForceDirectedLayout', None)
        self._connections:  Nodes     = Nodes([])
        self._location:     Point     = Point()

    @property
    @abstractmethod
    def size(self) -> Size:
        """
        May be used when rendering

        Returns:  The node width and height
        """
        pass

    def drawConnector(self, dc: DrawingContext, sourcePoint: Point, destinationPoint: Point):
        """
        Draws a connector between this node and the specified child node
        The source and destination coordinates are also specified.

        Args:
            dc:                "Drawing Context” onto which graphics and text can be drawn.
            sourcePoint:        Source coordinate
            destinationPoint:   Destination coordinate.
        """
        dc.DrawLine(x1=sourcePoint.x, y1=sourcePoint.y, x2=destinationPoint.x, y2=destinationPoint.y)

    @abstractmethod
    def drawNode(self, dc: DrawingContext):
        """
        Draws the node
        Args:
            dc:     The drawing context to draw n
        """
        pass

    @property
    def location(self) -> Point:
        return self._location

    @location.setter
    def location(self, point: Point):
        self._location = point

    @property
    def x(self) -> int:
        return self._location.x

    @x.setter
    def x(self, x: int):
        self._location.x = x

    @property
    def y(self) -> int:
        return self._location.y

    @y.setter
    def y(self, y: int):
        self._location.y = y

    @property
    def layoutEngine(self) -> 'ForceDirectedLayout':
        return self._layoutEngine

    @layoutEngine.setter
    def layoutEngine(self, layoutEngine: 'ForceDirectedLayout'):

        if layoutEngine == self._layoutEngine:
            pass
        else:
            if layoutEngine is not None:
                self._layoutEngine = layoutEngine
                self._layoutEngine.addNode(self)

    @property
    def connections(self) -> Nodes:
        """

        Returns:  a read-only collection representing the (child) nodes that this node is connected to
        """
        return Nodes(self._connections[:])

    def addChild(self, child: 'Node') -> bool:
        """
        Connects the specified child node to this node.

        Args:
            child:  The child node to add.

        Returns:  True if the node was connected to this node
        """
        assert child is not None, 'Null child is not allowed'

        if child != self and child not in self._connections:
            child.layoutEngine = self.layoutEngine
            self._connections.append(child)
            return True
        else:
            return False

    def addParent(self, parent: 'Node') -> bool:
        """
        Connects this node to the specified parent node

        Args:
            parent:  The node to connect to this node

        Returns: True if the other node was connected to this node
        """
        assert parent is not None, 'Null parents are not allowed'

        return parent.addChild(self)

    def disConnect(self, other: 'Node') -> bool:
        """
        Removes any connection between this node and the specified node.

        Args:
            other:  The other node whose connection is to be removed.

        Returns:  True if a connection existed.

        """
        selfFailed:  bool = False
        otherFailed: bool = False
        try:
            self._connections.remove(other)
        except ValueError:
            selfFailed = True

        try:
            other.connections.remove(self)
        except ValueError:
            otherFailed = True

        if selfFailed or otherFailed:
            return False
        else:
            return True

    def __eq__(self, other) -> bool:

        ans: bool = False
        if self.x == other.x and self.y == other .y and self.location == other.location:
            ans = True

        return ans
