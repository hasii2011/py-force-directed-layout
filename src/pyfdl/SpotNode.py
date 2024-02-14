
from logging import Logger
from logging import getLogger


from wx import BLACK_PEN
from wx import Brush
from wx import DC
from wx import Pen
from wx import WHITE_BRUSH

from pyfdl.Node import Node
from pyfdl.Point import Point
from pyfdl.Size import Size


DEFAULT_PEN:   Pen   = BLACK_PEN
DEFAULT_BRUSH: Brush = WHITE_BRUSH


class SpotNode(Node):
    """
    Provides an example implementation of the Node class. SpotNode is an 8x8 circle that is
    stroked and filled.
    """
    def __init__(self, stroke: Pen = DEFAULT_PEN, fill: Brush = DEFAULT_BRUSH):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._stroke: Pen   = stroke
        self._fill:   Brush = fill

    @property
    def size(self) -> Size:
        """
        Returns:    The size of the spot
        """
        return Size(8, 8)

    @property
    def fill(self) -> Brush:
        """
        Returns:  The Brush used to fill the spot.
        """
        return self._fill

    @fill.setter
    def fill(self, value: Brush):
        self._fill = value

    @property
    def stroke(self) -> Pen:
        """
        Returns:  The Pen used to stroke the spot.
        """
        return self._stroke

    @stroke.setter
    def stroke(self, value: Pen):
        self._stroke = value

    def drawConnector(self, dc: DC, sourcePoint: Point, destinationPoint: Point):
        """
        Draws a connector between this node and the specified child node
        The source and destination coordinates are also specified.

        Args:
            dc:                 "device context” onto which graphics and text can be drawn.
            sourcePoint:        Source coordinate
            destinationPoint:   Destination coordinate.
        """
        savePen: DC = dc.GetPen()

        dc.SetPen(self._stroke)
        dc.DrawLine(x1=sourcePoint.x, y1=sourcePoint.y, x2=destinationPoint.x, y2=destinationPoint.y)
        dc.SetPen(savePen)

    def drawNode(self, dc: DC):

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(self._stroke)
        dc.SetBrush(self._fill)

        dc.DrawEllipse(x=self.location.x, y=self.location.y, width=self.size.width, height=self.size.height)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

    def __deepcopy__(self, memoDictionary):

        newSpotNode: SpotNode = SpotNode()

        memoDictionary[id(self)] = newSpotNode

        return newSpotNode

    def __str__(self) -> str:
        return f'SpotNode {self.location}'

    def __repr(self) -> str:
        return self.__str__()
