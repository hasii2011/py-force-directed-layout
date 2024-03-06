from enum import Enum
from typing import cast

from logging import Logger
from logging import getLogger

from random import randint

from wx import App
from wx import BLACK
from wx import BLACK_BRUSH
from wx import BLACK_PEN
from wx import BLUE
from wx import BLUE_BRUSH
from wx import Brush
from wx import Colour
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FRAME_FLOAT_ON_PARENT
from wx import GREEN_BRUSH
from wx import GREEN_PEN
from wx import ID_EXIT
from wx import ID_PREFERENCES
from wx import Menu
from wx import MenuBar

from wx import NewIdRef as wxNewIdRef
from wx import OK
from wx import PD_APP_MODAL
from wx import PD_ELAPSED_TIME
from wx import PENSTYLE_SOLID
from wx import Pen
from wx import ProgressDialog
from wx import RED_BRUSH
from wx import RED_PEN
from wx import WHITE
from wx import Yield as wxYield

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from codeallybasic.UnitTestBase import UnitTestBase

from pyforcedirectedlayout.LayoutEngine import LayoutEngine
from pyforcedirectedlayout.LayoutTypes import LayoutStatus
from pyforcedirectedlayout.Point import Point
from tests.demo.DemoColorEnum import DemoColorEnum

from tests.demo.DemoTypes import EVT_FORCED_DIRECTED_LAYOUT
from tests.demo.DemoTypes import EVT_RESET_DIAGRAM
from tests.demo.DemoTypes import ForceDirectedLayoutEvent
from tests.demo.DemoTypes import ResetDiagramEvent

from tests.demo.DiagramFrame import DiagramFrame
from tests.demo.DlgConfiguration import DlgConfiguration
from tests.demo.RectangleNode import RectangleNode
from tests.demo.SpotNode import SpotNode

FRAME_WIDTH:  int = 1280
FRAME_HEIGHT: int = 800

NO_PROGRESS_DIALOG:  ProgressDialog = cast(ProgressDialog, None)

MIN_X: int = 10
MAX_X: int = 800
MIN_Y: int = 20
MAX_Y: int = 600


MAX_CHILD_COUNT: int = 5


class DiagramType(Enum):
    RANDOM_SPOT_NODES      = 1
    RANDOM_RECTANGLE_NODES = 2
    FIXED_SPOT_NODES       = 3
    FIXED_RECTANGLE_NODES  = 4


class DemoLayout(App):

    def __init__(self):

        UnitTestBase.setUpLogging()

        self.logger: Logger = getLogger(__name__)

        super().__init__(redirect=False)

    # noinspection PyAttributeOutsideInit
    def OnInit(self):

        self._topLevelFrame: SizedFrame = SizedFrame(parent=None, title="Demo Force Directed Layout",
                                                     size=(FRAME_WIDTH, FRAME_HEIGHT),
                                                     style=DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT)
        self._topLevelFrame.CreateStatusBar()  # should always do this when there's a resize border

        sizedPanel: SizedPanel = self._topLevelFrame.GetContentsPane()

        self._diagramFrame: DiagramFrame = DiagramFrame(parent=sizedPanel)
        self._diagramType:  DiagramType  = DiagramType.FIXED_RECTANGLE_NODES

        # noinspection PyUnresolvedReferences
        self._diagramFrame.SetSizerProps(expand=True, proportion=1)
        self._diagramFrame.layoutEngine = LayoutEngine()
        # self._generateRandomDiagram(layoutEngine=self._diagramFrame.layoutEngine)
        # self._generateRandomFixedDiagramRectangleNodes(layoutEngine=self._diagramFrame.layoutEngine)
        self._generateRandomDiagramRectangleNodes(layoutEngine=self._diagramFrame.layoutEngine)

        self._arrangeId:              int = wxNewIdRef()
        self._randomSpotNodesId:      int = wxNewIdRef()
        self._randomRectangleNodesId: int = wxNewIdRef()
        self._fixedSpotNodesId:       int = wxNewIdRef()
        self._fixedRectangleNodesId:  int = wxNewIdRef()

        self._createApplicationMenuBar()

        self.SetTopWindow(self._topLevelFrame)

        self._topLevelFrame.SetAutoLayout(True)
        self._topLevelFrame.Show(True)

        self._layoutProgressDialog: ProgressDialog = NO_PROGRESS_DIALOG

        self._topLevelFrame.Bind(EVT_FORCED_DIRECTED_LAYOUT, self._onExternalArrange)
        self._topLevelFrame.Bind(EVT_RESET_DIAGRAM,          self._onResetDiagram)

        return True

    def _createApplicationMenuBar(self):
        menuBar:     MenuBar = MenuBar()
        fileMenu:    Menu    = Menu()
        diagramMenu: Menu = Menu()

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_PREFERENCES, "&Configuration\tCtrl-C", "Force Directed Configuration")

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")

        fileMenu.Append(id=self._arrangeId, item='&Arrange\tCtrl-A', helpString='Arrange the diagram')

        diagramMenu.Append(id=self._randomSpotNodesId,      item='Random &Spot Nodes\tCtrl-S',      helpString='')
        diagramMenu.Append(id=self._randomRectangleNodesId, item='Random &Rectangle Nodes\tCtrl-R', helpString='')
        diagramMenu.Append(id=self._fixedSpotNodesId,       item='&Fixed Spot Nodes\tCtrl-F',       helpString='')
        diagramMenu.Append(id=self._fixedRectangleNodesId,  item='Fixed Rectangle &Nodes\tCtrl-N',  helpString='')

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(diagramMenu, 'Diagram Type')

        # entryArrange1: AcceleratorEntry = AcceleratorEntry(flags=ACCEL_ALT, keyCode=ord('a'), cmd=self._arrangeId)
        # entryArrange2: AcceleratorEntry = AcceleratorEntry(flags=ACCEL_ALT, keyCode=ord('A'), cmd=self._arrangeId)
        #
        # acceleratorTable: AcceleratorTable = AcceleratorTable([entryArrange1, entryArrange2])
        #
        # self.logger.info(f'{acceleratorTable.IsOk()=}')
        # self._topLevelFrame.SetAcceleratorTable(acceleratorTable)

        self._topLevelFrame.SetMenuBar(menuBar)

        self._topLevelFrame.Bind(EVT_MENU, self._onArrange,         id=self._arrangeId)
        self._topLevelFrame.Bind(EVT_MENU, self._onConfiguration,   id=ID_PREFERENCES)
        self._topLevelFrame.Bind(EVT_MENU, self._changeDiagramType, id=self._randomSpotNodesId)
        self._topLevelFrame.Bind(EVT_MENU, self._changeDiagramType, id=self._randomRectangleNodesId)
        self._topLevelFrame.Bind(EVT_MENU, self._changeDiagramType, id=self._fixedSpotNodesId)
        self._topLevelFrame.Bind(EVT_MENU, self._changeDiagramType, id=self._fixedRectangleNodesId)

    # noinspection PyUnusedLocal
    def _onArrange(self, event: CommandEvent):
        self._diagramFrame.layoutEngine.arrange(statusCallback=self._layoutStatusCallBack)
        self._diagramFrame.Refresh()

        self._layoutProgressDialog.Destroy()

    # noinspection PyUnusedLocal
    def _onExternalArrange(self, event: ForceDirectedLayoutEvent):
        self._layoutProgressDialog = NO_PROGRESS_DIALOG
        self._diagramFrame.layoutEngine.arrange(statusCallback=self._layoutStatusCallBack)
        self._diagramFrame.Refresh()

        self._layoutProgressDialog.Destroy()

    # noinspection PyUnusedLocal
    def _onConfiguration(self, event: CommandEvent):

        with DlgConfiguration(parent=self._topLevelFrame) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.info(f'Pressed Ok')

    # noinspection PyUnusedLocal
    def _onResetDiagram(self, event: ResetDiagramEvent):

        self.logger.info(f'Old node count: {len(self._diagramFrame.layoutEngine.nodes)}')
        self._diagramFrame.layoutEngine = LayoutEngine()
        match self._diagramType:
            case DiagramType.RANDOM_SPOT_NODES:
                self._generateRandomDiagramSpotNodes(layoutEngine=self._diagramFrame.layoutEngine)
            case DiagramType.RANDOM_RECTANGLE_NODES:
                self._generateRandomDiagramRectangleNodes(layoutEngine=self._diagramFrame.layoutEngine)
            case DiagramType.FIXED_SPOT_NODES:
                self._generateFixedDiagramSpotNodes(layoutEngine=self._diagramFrame.layoutEngine)
            case DiagramType.FIXED_RECTANGLE_NODES:
                self._generateFixedDiagramRectangleNodes(layoutEngine=self._diagramFrame.layoutEngine)
            case _:
                self.logger.error(f'Unknown diagram type: {self._diagramType}')

        self.logger.info(f'New node count: {len(self._diagramFrame.layoutEngine.nodes)}')
        self._diagramFrame.Refresh()

    def _layoutStatusCallBack(self, status: LayoutStatus):

        if self._layoutProgressDialog is None:
            self._layoutProgressDialog = ProgressDialog('Arranging', 'Starting', parent=None, style=PD_APP_MODAL | PD_ELAPSED_TIME)
            self._layoutProgressDialog.SetRange(status.maxIterations)

        statusMsg: str = (
            f'totalDisplacement: {status.totalDisplacement: .3f}\n'
            f'iterations: {status.iterations}\n'
            f'stopCount: {status.stopCount}\n'
        )
        # self.logger.info(f'{statusMsg}')
        self._layoutProgressDialog.Update(status.iterations, statusMsg)

        self._diagramFrame.Refresh()
        wxYield()

    def _changeDiagramType(self, event: CommandEvent):

        diagramTypeId: int = event.GetId()
        print(f'{diagramTypeId=}')
        match diagramTypeId:
            case self._randomSpotNodesId:
                self._diagramType = DiagramType.RANDOM_SPOT_NODES
            case self._randomRectangleNodesId:
                self._diagramType = DiagramType.RANDOM_RECTANGLE_NODES
            case self._fixedSpotNodesId:
                self._diagramType = DiagramType.FIXED_SPOT_NODES
            case self._fixedRectangleNodesId:
                self._diagramType = DiagramType.FIXED_RECTANGLE_NODES
            case _:
                self.logger.error(f'Unknown diagram type')

        self._onResetDiagram(None)

    def _generateRandomDiagramSpotNodes(self, layoutEngine: LayoutEngine):

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

    def _generateRandomDiagramRectangleNodes(self, layoutEngine: LayoutEngine):

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

    def _generateFixedDiagramRectangleNodes(self, layoutEngine: LayoutEngine):

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

    def _generateFixedDiagramSpotNodes(self, layoutEngine: LayoutEngine):

        blackPen: Pen = Pen(colour=BLACK, width=1, style=PENSTYLE_SOLID)

        parentNode: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode = self._generateParentHierarchy(parentNode=parentNode, layoutEngine=layoutEngine)
        layoutEngine.addNode(parentNode)

        parentNode2: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode2.location  = Point(x=randint(MIN_X, MAX_X), y=randint(MIN_Y, MAX_Y))
        parentNode2 = self._generateParentHierarchy(parentNode=parentNode2, layoutEngine=layoutEngine)
        layoutEngine.addNode(parentNode2)

    def _generateParentHierarchy(self, layoutEngine: LayoutEngine, parentNode: SpotNode) -> SpotNode:

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


testApp: DemoLayout = DemoLayout()

testApp.MainLoop()
