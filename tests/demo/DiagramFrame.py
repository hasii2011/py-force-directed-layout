
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Bitmap
from wx import Brush
from wx import Colour
from wx import DC
from wx import EVT_PAINT
from wx import LIGHT_GREY
from wx import MemoryDC
from wx import PENSTYLE_DOT
from wx import PaintDC
from wx import PaintEvent
from wx import Pen
from wx import PenInfo
from wx import Rect
from wx import ScrolledWindow
from wx import WHITE
from wx import Window
# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from pyforcedirectedlayout.ForceDirectedLayout import ForceDirectedLayout
from pyforcedirectedlayout.LayoutTypes import Nodes
from pyforcedirectedlayout.Node import Node
from pyforcedirectedlayout.Point import Point

DEFAULT_WIDTH = 3000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20

NO_LAYOUT_ENGINE: ForceDirectedLayout = cast(ForceDirectedLayout, None)


class DiagramFrame(ScrolledWindow):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self._layoutEngine: ForceDirectedLayout = NO_LAYOUT_ENGINE

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(PIXELS_PER_UNIT_X, PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

        # paint related
        w, h = self.GetSize()
        self._workingBitmap    = Bitmap(w, h)   # double buffering
        self._backgroundBitmap = Bitmap(w, h)

        self.SetBackgroundColour(WHITE)

        self.Bind(EVT_PAINT, self.onPaint)

    # noinspection PyUnusedLocal
    def Refresh(self, eraseBackground: bool = True, rect: Rect = None):
        self.onPaint(cast(PaintEvent, None))

    @property
    def layoutEngine(self) -> ForceDirectedLayout:
        """
        Returns:  The diagram associated with this frame
        """
        return self._layoutEngine

    @layoutEngine.setter
    def layoutEngine(self, layoutEngine: ForceDirectedLayout):
        """
        Associates a new layout engine with the frame
        Args:
            layoutEngine:
        """
        self._layoutEngine = layoutEngine

    # noinspection PyUnusedLocal
    def onPaint(self, event: PaintEvent):

        dc: PaintDC = PaintDC(self)

        w, h = self.GetSize()

        mem: MemoryDC = self.createDC(w, h)
        mem.SetBackground(Brush(self.GetBackgroundColour()))
        mem.Clear()

        x, y = self.CalcUnscrolledPosition(0, 0)

        self._drawGrid(memDC=mem, width=w, height=h, startX=x, startY=y)

        nodes: Nodes = self._layoutEngine.nodes
        for n in nodes:
            parentNode: Node = cast(Node, n)
            parentNode.drawNode(mem)
            centerParentPoint: Point = self._computeShapeCenter(node=parentNode)

            for c in parentNode.connections:
                childNode: Node = cast(Node, c)
                childNode.drawNode(mem)
                centerChildPoint: Point = self._computeShapeCenter(node=childNode)
                childNode.drawConnector(dc=mem, sourcePoint=centerParentPoint, destinationPoint=centerChildPoint)

                for g in childNode.connections:
                    grandChildNode: Node = cast(Node, g)
                    grandChildNode.drawNode(dc=mem)
                    centerGrandChildPoint: Point = self._computeShapeCenter(node=grandChildNode)
                    grandChildNode.drawConnector(dc=mem, sourcePoint=centerChildPoint, destinationPoint=centerGrandChildPoint)

                    for gg in grandChildNode.connections:
                        greatGrandChildNode: Node = cast(Node, gg)
                        greatGrandChildNode.drawNode(dc=mem)
                        centerGreatGrandChildPoint: Point = self._computeShapeCenter(node=greatGrandChildNode)
                        greatGrandChildNode.drawConnector(dc=mem, sourcePoint=centerGrandChildPoint, destinationPoint=centerGreatGrandChildPoint)

        dc.Blit(0, 0, w, h, mem, x, y)

    def createDC(self, w: int, h: int) -> MemoryDC:
        """
        Create a DC,
        Args:
            w:  frame width
            h:  frame height

        Returns: A device context
        """
        dc: MemoryDC = MemoryDC()

        bm = self._workingBitmap
        # cache the bitmap, to avoid creating a new one at each refresh.
        # only recreate it if the size of the window has changed
        if (bm.GetWidth(), bm.GetHeight()) != (w, h):
            bm = self._workingBitmap = Bitmap(w, h)
        dc.SelectObject(bm)

        dc.SetBackground(Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.PrepareDC(dc)

        return dc

    def _drawGrid(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        # self.clsLogger.info(f'{width=} {height=} {startX=} {startY=}')
        savePen = memDC.GetPen()

        newPen: Pen = self._getGridPen()
        memDC.SetPen(newPen)

        self._drawHorizontalLines(memDC=memDC, width=width, height=height, startX=startX, startY=startY)
        self._drawVerticalLines(memDC=memDC,   width=width, height=height, startX=startX, startY=startY)
        memDC.SetPen(savePen)

    def _drawHorizontalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        x1:   int = 0
        x2:   int = startX + width
        stop: int = height + startY
        step: int = 25
        for movingY in range(startY, stop, step):
            memDC.DrawLine(x1, movingY, x2, movingY)

    def _drawVerticalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        y1:   int = 0
        y2:   int = startY + height
        stop: int = width + startX
        step: int = 25

        for movingX in range(startX, stop, step):
            memDC.DrawLine(movingX, y1, movingX, y2)

    def _getGridPen(self) -> Pen:

        gridLineColor: Colour   = LIGHT_GREY
        gridLineStyle: PenStyle = PENSTYLE_DOT

        pen:           Pen    = Pen(PenInfo(gridLineColor).Style(gridLineStyle).Width(1))

        return pen

    def _computeShapeCenter(self, node: Node) -> Point:

        centeredPoint: Point = Point(x=node.location.x + (node.size.width // 2), y=node.location.y + (node.size.height // 2))

        return centeredPoint
