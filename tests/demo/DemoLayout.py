
from logging import Logger
from logging import getLogger
from typing import cast

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

from pyfdl.LayoutTypes import LayoutStatus
from tests.demo.DiagramFrame import DiagramFrame
from tests.demo.DlgConfiguration import DlgConfiguration

FRAME_WIDTH:  int = 1280
FRAME_HEIGHT: int = 800


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

        self._arrangeId = wxNewIdRef()

        self._createApplicationMenuBar()

        self.SetTopWindow(self._topLevelFrame)

        self._topLevelFrame.SetAutoLayout(True)
        self._topLevelFrame.Show(True)

        self._layoutProgressDialog: ProgressDialog = cast(ProgressDialog, None)

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

        self.Bind(EVT_MENU, self._onArrange, id=self._arrangeId)
        self.Bind(EVT_MENU, self._onConfiguration, id=ID_PREFERENCES)

    # noinspection PyUnusedLocal
    def _onArrange(self, event: CommandEvent):
        self._diagramFrame.layoutEngine.arrange(statusCallback=self._layoutStatusCallBack)
        self._diagramFrame.Refresh()

        self._layoutProgressDialog.Destroy()

    # noinspection PyUnusedLocal
    def _onConfiguration(self, event: CommandEvent):

        with DlgConfiguration(parent=self._topLevelFrame) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.info(f'Pressed Ok')

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


testApp: DemoLayout = DemoLayout()

testApp.MainLoop()
