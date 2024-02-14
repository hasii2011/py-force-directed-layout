
from logging import Logger
from logging import getLogger
from random import randint
from typing import cast

from wx import BLACK
from wx import BLACK_BRUSH
from wx import BLUE
from wx import BLUE_BRUSH
from wx import Bitmap
from wx import Brush
from wx import Colour
from wx import DC
from wx import EVT_PAINT
from wx import GREEN_BRUSH
from wx import GREEN_PEN
from wx import LIGHT_GREY
from wx import MemoryDC
from wx import PENSTYLE_DOT
from wx import PENSTYLE_SOLID
from wx import PaintDC
from wx import PaintEvent
from wx import Pen
from wx import PenInfo
from wx import RED_BRUSH
from wx import RED_PEN
from wx import Rect
from wx import ScrolledWindow
from wx import WHITE
from wx import Window
# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from pyfdl.Diagram import Diagram
from pyfdl.LayoutTypes import Nodes
from pyfdl.Node import Node
from pyfdl.Point import Point
from pyfdl.SpotNode import SpotNode

DEFAULT_WIDTH = 3000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20

MIN_X: int = 10
MAX_X: int = 600
MIN_Y: int = 20
MAX_Y: int = 500


class DiagramFrame(ScrolledWindow):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self._diagram: Diagram = Diagram()

        self._generateRandomDiagram(diagram=self._diagram)
        # self._generateFixedDiagram(diagram=self._diagram)
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
    def diagram(self) -> Diagram:
        """
        Returns:  The diagram associated with this frame
        """
        return self._diagram

    @diagram.setter
    def diagram(self, diagram: Diagram):
        """
        Associates a new diagram with the frame
        Args:
            diagram:
        """
        self._diagram = diagram

    # noinspection PyUnusedLocal
    def onPaint(self, event: PaintEvent):

        dc: PaintDC = PaintDC(self)

        w, h = self.GetSize()

        mem: MemoryDC = self.createDC(w, h)
        mem.SetBackground(Brush(self.GetBackgroundColour()))
        mem.Clear()

        x, y = self.CalcUnscrolledPosition(0, 0)

        self._drawGrid(memDC=mem, width=w, height=h, startX=x, startY=y)

        nodes: Nodes = self._diagram.nodes
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
        # cache the bitmap, to avoid creating a new at each refresh.
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

    def _generateRandomDiagram(self, diagram: Diagram):

        bluePen:  Pen = Pen(colour=BLUE, width=1,  style=PENSTYLE_SOLID)
        blackPen: Pen = Pen(colour=BLACK, width=1, style=PENSTYLE_SOLID)

        parentNode: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode.location  = Point(x=randint(1, 600), y=randint(1, 500))

        diagram.addNode(parentNode)

        childrenCount: int = randint(1, 5)
        for x in range(childrenCount):
            childNode: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)
            childNode.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
            parentNode.addChild(childNode)
            diagram.addNode(childNode)

            grandChildrenCount: int = randint(0, 5)
            for y in range(grandChildrenCount):
                grandChildNode: SpotNode = SpotNode(stroke=GREEN_PEN, fill=GREEN_BRUSH)
                grandChildNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
                childNode.addChild(grandChildNode)
                diagram.addNode(grandChildNode)

                greatGrandChildrenCount: int = randint(0, 5)
                for z in range(greatGrandChildrenCount):
                    greatGrandChildNode: SpotNode = SpotNode(stroke=RED_PEN, fill=RED_BRUSH)
                    greatGrandChildNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
                    grandChildNode.addChild(greatGrandChildNode)
                    diagram.addNode(grandChildNode)

    def _generateFixedDiagram(self, diagram: Diagram):

        blackPen: Pen = Pen(colour=BLACK, width=1, style=PENSTYLE_SOLID)

        parentNode: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode = self._generateParentHierarchy(parentNode=parentNode, diagram=diagram)
        diagram.addNode(parentNode)

        parentNode2: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode2.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode2 = self._generateParentHierarchy(parentNode=parentNode2, diagram=diagram)
        diagram.addNode(parentNode2)

    def _generateParentHierarchy(self, diagram: Diagram, parentNode: SpotNode) -> SpotNode:

        bluePen:  Pen = Pen(colour=BLUE, width=1,  style=PENSTYLE_SOLID)
        childNode1: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)
        childNode2: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)
        childNode3: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)

        childNode1.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        childNode2.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        childNode3.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))

        diagram.addNode(childNode1)
        diagram.addNode(childNode2)
        diagram.addNode(childNode3)

        parentNode.addChild(childNode1)
        parentNode.addChild(childNode2)
        parentNode.addChild(childNode3)

        return parentNode

    def _computeShapeCenter(self, node: Node) -> Point:

        centeredPoint: Point = Point(x=node.location.x + (node.size.width // 2), y=node.location.y + (node.size.height // 2))

        return centeredPoint
