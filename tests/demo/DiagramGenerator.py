
from logging import Logger
from logging import getLogger

from random import randint

from wx import BLACK
from wx import BLACK_BRUSH
from wx import BLACK_PEN
from wx import BLUE
from wx import BLUE_BRUSH
from wx import Brush
from wx import Colour
from wx import GREEN_BRUSH
from wx import PENSTYLE_SOLID
from wx import Pen
from wx import RED_BRUSH
from wx import RED_PEN
from wx import WHITE

from pyforcedirectedlayout.LayoutEngine import LayoutEngine
from pyforcedirectedlayout.Point import Point

from tests.demo.DemoColorEnum import DemoColorEnum
from tests.demo.RectangleNode import RectangleNode
from tests.demo.SpotNode import SpotNode


MIN_X: int = 10
MAX_X: int = 800
MIN_Y: int = 20
MAX_Y: int = 600


MAX_CHILD_COUNT: int = 5


class DiagramGenerator:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def generateRandomDiagramSpotNodes(self, layoutEngine: LayoutEngine):

        bluePen:  Pen = Pen(colour=BLUE, width=1,  style=PENSTYLE_SOLID)
        blackPen: Pen = Pen(colour=BLACK, width=1, style=PENSTYLE_SOLID)

        parentNode: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode.location  = Point(x=randint(1, MAX_X), y=randint(1, MAX_Y))

        layoutEngine.addNode(parentNode)

        childrenCount: int = randint(1, 5)
        for x in range(childrenCount):
            childNode: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)
            childNode.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
            parentNode.addChild(childNode)
            layoutEngine.addNode(childNode)

            grandChildrenCount: int = randint(0, 5)
            for y in range(grandChildrenCount):
                from wx import GREEN_PEN
                grandChildNode: SpotNode = SpotNode(stroke=GREEN_PEN, fill=GREEN_BRUSH)
                grandChildNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
                childNode.addChild(grandChildNode)
                layoutEngine.addNode(grandChildNode)

                greatGrandChildrenCount: int = randint(0, 5)
                for z in range(greatGrandChildrenCount):
                    greatGrandChildNode: SpotNode = SpotNode(stroke=RED_PEN, fill=RED_BRUSH)
                    greatGrandChildNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
                    grandChildNode.addChild(greatGrandChildNode)
                    layoutEngine.addNode(grandChildNode)

    def generateRandomDiagramRectangleNodes(self, layoutEngine: LayoutEngine):

        fillColor: Colour = DemoColorEnum.toWxColor(DemoColorEnum.LIGHT_YELLOW)
        brush:     Brush  = Brush(colour=fillColor)

        parentNode: RectangleNode = RectangleNode(name='The Parent', fill=brush)
        parentNode.location  = Point(x=randint(1, MAX_X), y=randint(1, MAX_Y))

        layoutEngine.addNode(parentNode)

        childPen:             Pen   = Pen(colour=DemoColorEnum.toWxColor(DemoColorEnum.LIGHT_STEEL_BLUE), width=1,  style=PENSTYLE_SOLID)
        childBrush:           Brush = Brush(colour=DemoColorEnum.toWxColor(DemoColorEnum.LIGHT_GREY))
        grandChildBrush:      Brush = Brush(colour=DemoColorEnum.toWxColor(DemoColorEnum.ALICE_BLUE))
        greatGrandChildBrush: Brush = Brush(colour=DemoColorEnum.toWxColor(DemoColorEnum.LIGHT_BLUE))

        childrenCount: int = randint(1, MAX_CHILD_COUNT)

        for x in range(childrenCount):
            name: str = f'Child{x}'
            childNode: RectangleNode = RectangleNode(name=name, stroke=childPen, fill=childBrush, textColor=WHITE)
            childNode.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
            parentNode.addChild(childNode)
            layoutEngine.addNode(childNode)

            grandChildrenCount: int = randint(0, MAX_CHILD_COUNT)
            for y in range(grandChildrenCount):
                grandChildName: str = f'GrandChild{y}'
                grandChildNode: RectangleNode = RectangleNode(name=grandChildName, stroke=BLACK_PEN, fill=grandChildBrush)
                grandChildNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
                childNode.addChild(grandChildNode)
                layoutEngine.addNode(grandChildNode)

                greatGrandChildrenCount: int = randint(0, MAX_CHILD_COUNT)
                for z in range(greatGrandChildrenCount):
                    greatGrandChildName: str = f'GreatGrandChild{z}'
                    greatGrandChildNode: RectangleNode = RectangleNode(name=greatGrandChildName, stroke=RED_PEN, fill=greatGrandChildBrush)
                    greatGrandChildNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
                    grandChildNode.addChild(greatGrandChildNode)
                    layoutEngine.addNode(grandChildNode)

    def generateFixedDiagramRectangleNodes(self, layoutEngine: LayoutEngine):

        fillColor: Colour = DemoColorEnum.toWxColor(DemoColorEnum.LIGHT_YELLOW)
        brush:     Brush  = Brush(colour=fillColor)

        parentNode: RectangleNode = RectangleNode(name='Parent Node 1', fill=brush)
        parentNode.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode = self._generateRectangleHierarchy(parentNode=parentNode, layoutEngine=layoutEngine)
        layoutEngine.addNode(parentNode)

        parentNode2: RectangleNode = RectangleNode(name='Parent Node 2', fill=brush)
        parentNode2.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode2 = self._generateRectangleHierarchy(parentNode=parentNode2, layoutEngine=layoutEngine)
        layoutEngine.addNode(parentNode2)

    def generateFixedDiagramSpotNodes(self, layoutEngine: LayoutEngine):

        blackPen: Pen = Pen(colour=BLACK, width=1, style=PENSTYLE_SOLID)

        parentNode: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode = self._generateSpotHierarchy(parentNode=parentNode, layoutEngine=layoutEngine)
        layoutEngine.addNode(parentNode)

        parentNode2: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode2.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode2 = self._generateSpotHierarchy(parentNode=parentNode2, layoutEngine=layoutEngine)
        layoutEngine.addNode(parentNode2)

    def _generateRectangleHierarchy(self, layoutEngine: LayoutEngine, parentNode: RectangleNode) -> RectangleNode:

        bluePen: Pen   = Pen(colour=BLUE, width=1,  style=PENSTYLE_SOLID)
        brush:   Brush = Brush(colour=DemoColorEnum.toWxColor(DemoColorEnum.LIGHT_STEEL_BLUE))

        childNode1: RectangleNode = RectangleNode(name='ChildNode1', stroke=bluePen, fill=brush)
        childNode2: RectangleNode = RectangleNode(name='ChildNode2', stroke=bluePen, fill=brush)
        childNode3: RectangleNode = RectangleNode(name='ChildNode2', stroke=bluePen, fill=brush)

        childNode1.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        childNode2.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        childNode3.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))

        layoutEngine.addNode(childNode1)
        layoutEngine.addNode(childNode2)
        layoutEngine.addNode(childNode3)

        parentNode.addChild(childNode1)
        parentNode.addChild(childNode2)
        parentNode.addChild(childNode3)

        return parentNode

    def _generateSpotHierarchy(self, layoutEngine: LayoutEngine, parentNode: SpotNode) -> SpotNode:

        bluePen:  Pen = Pen(colour=BLUE, width=1,  style=PENSTYLE_SOLID)
        childNode1: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)
        childNode2: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)
        childNode3: SpotNode = SpotNode(stroke=bluePen, fill=BLUE_BRUSH)

        childNode1.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        childNode2.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        childNode3.location = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))

        layoutEngine.addNode(childNode1)
        layoutEngine.addNode(childNode2)
        layoutEngine.addNode(childNode3)

        parentNode.addChild(childNode1)
        parentNode.addChild(childNode2)
        parentNode.addChild(childNode3)

        return parentNode
