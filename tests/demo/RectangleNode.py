
from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import BLACK_PEN
from wx import Brush
from wx import Colour
from wx import DC
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import FONTWEIGHT_NORMAL
from wx import Font
from wx import Pen
from wx import WHITE_BRUSH

from pyforcedirectedlayout.LayoutTypes import DrawingContext
from pyforcedirectedlayout.Node import Node
from pyforcedirectedlayout.Point import Point
from pyforcedirectedlayout.Size import Size


DEFAULT_PEN:   Pen   = BLACK_PEN
DEFAULT_BRUSH: Brush = WHITE_BRUSH
DEFAULT_FONT_SIZE = 10


class RectangleNode(Node):

    def __init__(self, name: str, stroke: Pen = DEFAULT_PEN, fill: Brush = DEFAULT_BRUSH, textColor: Colour = BLACK):
        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._name:   str = name
        self._stroke: Pen   = stroke
        self._fill:   Brush = fill

        self._textColor:   Colour = textColor
        self._defaultFont: Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self._nameFont:    Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)

    @property
    def size(self) -> Size:
        """
        Returns:    The size of the Rectangle
        """
        return Size(width=100, height=50)

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

    def drawNode(self, dc: DrawingContext):

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(self._stroke)
        dc.SetBrush(self._fill)

        x:      int = self.location.x
        y:      int = self.location.y
        width:  int = self.size.width
        height: int = self.size.height

        dc.DrawRectangle(x=x, y=y, width=width, height=height)
        (headerX, headerY, headerW, headerH) = self._drawHeader(dc=dc)
        y = headerY + headerH

        dc.DrawLine(x, y + 10, x + width, y + 10)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

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
        super().drawConnector(dc=dc, sourcePoint=sourcePoint, destinationPoint=destinationPoint)
        dc.SetPen(savePen)

    def _drawHeader(self, dc: DC):
        """
        Calculate the class header position and size and display it if
        a draw is True

        Args:
            dc:

        Returns: tuple (x, y, w, h) = position and size of the header
        """
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(self._textColor)

        x: int = self.location.x
        y: int = self.location.y

        w = self.size.width
        h = 0

        # define space between the text and line
        lth = dc.GetTextExtent("*")[1] // 2

        # from where begin the text
        h += lth

        # draw a pyutClass name
        name: str = self._name
        dc.SetFont(self._nameFont)
        nameWidth: int = self.textWidth(dc, name)

        dc.DrawText(name, x + (w - nameWidth) // 2, y + h)

        dc.SetFont(self._defaultFont)
        h += self.textHeight(dc, str(name)) // 2
        return x, y, w, h

    def textWidth(self, dc: DC, text: str):
        width = dc.GetTextExtent(text)[0]
        return width

    def textHeight(self, dc: DC, text: str):
        height = dc.GetTextExtent(text)[1]
        return height
