
from logging import Logger
from logging import getLogger

from wx import App
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FRAME_FLOAT_ON_PARENT
from wx import ID_EXIT
from wx import Menu
from wx import MenuBar

from wx import NewIdRef as wxNewIdRef
from wx import Yield as wxYield

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from codeallybasic.UnitTestBase import UnitTestBase

from pyfdl.LayoutTypes import LayoutStatus
from tests.demo.DiagramFrame import DiagramFrame

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

        return True

    # noinspection PyUnusedLocal
    def onArrange(self, event: CommandEvent):
        self._diagramFrame.diagram.arrange(statusCallback=self._layoutStatusCallBack)
        self._diagramFrame.Refresh()

    def _createApplicationMenuBar(self):
        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu    = Menu()

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")

        fileMenu.Append(self._arrangeId, 'Arrange', 'Arrange the diagram')

        menuBar.Append(fileMenu, 'File')

        self._topLevelFrame.SetMenuBar(menuBar)

        self.Bind(EVT_MENU, self.onArrange, id=self._arrangeId)

    def _layoutStatusCallBack(self, status: LayoutStatus):

        statusMsg: str = (
            f'totalDisplacement: {status.totalDisplacement: .3f} '
            f'iterations: {status.iterations} '
            f'stopCount: {status.stopCount} '
        )
        self.logger.info(f'{statusMsg}')
        self._diagramFrame.Refresh()
        wxYield()


testApp: DemoLayout = DemoLayout()

testApp.MainLoop()
