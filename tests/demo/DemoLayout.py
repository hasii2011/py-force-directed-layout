from enum import Enum
from typing import cast

from logging import Logger
from logging import getLogger

from wx import App
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FRAME_FLOAT_ON_PARENT
from wx import ID_EXIT
from wx import ID_PREFERENCES
from wx import Menu
from wx import MenuBar

from wx import NewIdRef as wxNewIdRef
from wx import OK
from wx import PD_APP_MODAL
from wx import PD_ELAPSED_TIME
from wx import ProgressDialog
from wx import Yield as wxYield

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from codeallybasic.UnitTestBase import UnitTestBase

from pyforcedirectedlayout.LayoutEngine import LayoutEngine
from pyforcedirectedlayout.LayoutTypes import LayoutStatus

from tests.demo.DemoTypes import EVT_FORCED_DIRECTED_LAYOUT
from tests.demo.DemoTypes import EVT_RESET_DIAGRAM
from tests.demo.DemoTypes import ForceDirectedLayoutEvent
from tests.demo.DemoTypes import ResetDiagramEvent

from tests.demo.DiagramFrame import DiagramFrame
from tests.demo.DiagramGenerator import DiagramGenerator
from tests.demo.DlgConfiguration import DlgConfiguration

FRAME_WIDTH:  int = 1280
FRAME_HEIGHT: int = 800

NO_PROGRESS_DIALOG:  ProgressDialog = cast(ProgressDialog, None)


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
        self._diagramType:  DiagramType  = DiagramType.RANDOM_RECTANGLE_NODES

        # noinspection PyUnresolvedReferences
        self._diagramFrame.SetSizerProps(expand=True, proportion=1)
        self._diagramFrame.layoutEngine = LayoutEngine()

        self._diagramGenerator: DiagramGenerator = DiagramGenerator()

        # Matches how we set diagramType
        self._diagramGenerator.generateRandomDiagramRectangleNodes(layoutEngine=self._diagramFrame.layoutEngine)

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
                self._diagramGenerator.generateRandomDiagramSpotNodes(layoutEngine=self._diagramFrame.layoutEngine)
            case DiagramType.RANDOM_RECTANGLE_NODES:
                self._diagramGenerator.generateRandomDiagramRectangleNodes(layoutEngine=self._diagramFrame.layoutEngine)
            case DiagramType.FIXED_SPOT_NODES:
                self._diagramGenerator.generateFixedDiagramSpotNodes(layoutEngine=self._diagramFrame.layoutEngine)
            case DiagramType.FIXED_RECTANGLE_NODES:
                self._diagramGenerator.generateFixedDiagramRectangleNodes(layoutEngine=self._diagramFrame.layoutEngine)
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


testApp: DemoLayout = DemoLayout()

testApp.MainLoop()
