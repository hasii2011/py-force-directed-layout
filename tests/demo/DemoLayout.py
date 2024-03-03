
from typing import cast

from logging import Logger
from logging import getLogger

from random import randint

from wx import App
from wx import BLACK
from wx import BLACK_BRUSH
from wx import BLUE
from wx import BLUE_BRUSH
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
from wx import Yield as wxYield

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from codeallybasic.UnitTestBase import UnitTestBase

from pyfdl.LayoutEngine import LayoutEngine
from pyfdl.LayoutTypes import LayoutStatus
from pyfdl.Point import Point

from tests.demo.DemoTypes import EVT_FORCED_DIRECTED_LAYOUT
from tests.demo.DemoTypes import EVT_RESET_DIAGRAM
from tests.demo.DemoTypes import ForceDirectedLayoutEvent
from tests.demo.DemoTypes import ResetDiagramEvent

from tests.demo.DiagramFrame import DiagramFrame
from tests.demo.DlgConfiguration import DlgConfiguration
from tests.demo.SpotNode import SpotNode

FRAME_WIDTH:  int = 1280
FRAME_HEIGHT: int = 800

NO_PROGRESS_DIALOG:  ProgressDialog = cast(ProgressDialog, None)

MIN_X: int = 10
MAX_X: int = 800
MIN_Y: int = 20
MAX_Y: int = 600


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

        # noinspection PyUnresolvedReferences
        self._diagramFrame.SetSizerProps(expand=True, proportion=1)
        self._diagramFrame.layoutEngine = LayoutEngine()
        self._generateRandomDiagram(layoutEngine=self._diagramFrame.layoutEngine)

        self._arrangeId = wxNewIdRef()
        self._createApplicationMenuBar()

        self.SetTopWindow(self._topLevelFrame)

        self._topLevelFrame.SetAutoLayout(True)
        self._topLevelFrame.Show(True)

        self._layoutProgressDialog: ProgressDialog = NO_PROGRESS_DIALOG

        self._topLevelFrame.Bind(EVT_FORCED_DIRECTED_LAYOUT, self._onExternalArrange)
        self._topLevelFrame.Bind(EVT_RESET_DIAGRAM,          self._onResetDiagram)

        return True

    def _createApplicationMenuBar(self):
        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu    = Menu()

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_PREFERENCES, "&Configuration\tCtrl-C", "Force Directed Configuration")

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")

        fileMenu.Append(id=self._arrangeId, item='&Arrange\tCtrl-A', helpString='Arrange the diagram')

        menuBar.Append(fileMenu, 'File')

        # entryArrange1: AcceleratorEntry = AcceleratorEntry(flags=ACCEL_ALT, keyCode=ord('a'), cmd=self._arrangeId)
        # entryArrange2: AcceleratorEntry = AcceleratorEntry(flags=ACCEL_ALT, keyCode=ord('A'), cmd=self._arrangeId)
        #
        # acceleratorTable: AcceleratorTable = AcceleratorTable([entryArrange1, entryArrange2])
        #
        # self.logger.info(f'{acceleratorTable.IsOk()=}')
        # self._topLevelFrame.SetAcceleratorTable(acceleratorTable)

        self._topLevelFrame.SetMenuBar(menuBar)

        self._topLevelFrame.Bind(EVT_MENU, self._onArrange,       id=self._arrangeId)
        self._topLevelFrame.Bind(EVT_MENU, self._onConfiguration, id=ID_PREFERENCES)

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
        self._generateRandomDiagram(layoutEngine=self._diagramFrame.layoutEngine)
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

    def _generateRandomDiagram(self, layoutEngine: LayoutEngine):

        bluePen:  Pen = Pen(colour=BLUE, width=1,  style=PENSTYLE_SOLID)
        blackPen: Pen = Pen(colour=BLACK, width=1, style=PENSTYLE_SOLID)

        parentNode: SpotNode = SpotNode(stroke=blackPen, fill=BLACK_BRUSH)
        parentNode.location  = Point(x=randint(1, 600), y=randint(1, 500))

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

    def _generateFixedDiagram(self, layoutEngine: LayoutEngine):

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
