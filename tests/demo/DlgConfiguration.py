
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Button
from wx import CANCEL
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import PostEvent
from wx import Size
from wx import Window

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from pyforcedirectedlayout.ui.ConfigurationPanel import ConfigurationPanel

from tests.demo.DemoTypes import ForceDirectedLayoutEvent
from tests.demo.DemoTypes import ResetDiagramEvent


NO_BUTTON: Button = cast(Button, None)


class DlgConfiguration(SizedDialog):
    """
    Demo-specific configuration dialog.  Wraps ConfigurationPanel and adds
    Arrange / Reset action buttons alongside the standard Ok / Cancel.
    """

    def __init__(self, parent: Window):

        style:   int  = DEFAULT_DIALOG_STYLE
        dlgSize: Size = Size(470, 540)

        super().__init__(parent, title='Force Directed Configuration', size=dlgSize, style=style)

        self._listeningWindow: Window = parent
        self.logger: Logger = getLogger(__name__)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        sizedPanel.SetSizerProps(proportion=1)

        self._configurationPanel: ConfigurationPanel = ConfigurationPanel(sizedPanel=sizedPanel)

        self._btnCancel: Button = NO_BUTTON
        self._btnOk:     Button = NO_BUTTON

        self._layoutCustomDialogButtons(parent=sizedPanel)

    def _layoutCustomDialogButtons(self, parent: SizedPanel):

        buttonPanel: SizedPanel = SizedPanel(parent)
        buttonPanel.SetSizerType('horizontal')
        buttonPanel.SetSizerProps(expand=False, border=(['top'], 20), halign='right')

        arrangeButton: Button = Button(buttonPanel, label='&Arrange')
        resetButton:   Button = Button(buttonPanel, label='&Reset')

        self._btnCancel = Button(buttonPanel, ID_CANCEL, '&Cancel')
        self._btnOk     = Button(buttonPanel, ID_OK, '&Ok')

        self.Bind(EVT_BUTTON, self._onReset,   resetButton)
        self.Bind(EVT_BUTTON, self._onArrange, arrangeButton)
        self.Bind(EVT_BUTTON, self._onOk,    self._btnOk)
        self.Bind(EVT_BUTTON, self._onClose, self._btnCancel)
        self.Bind(EVT_CLOSE,  self._onClose, self._btnCancel)

        self._btnOk.SetDefault()

    # noinspection PyUnusedLocal
    def _onOk(self, _event: CommandEvent):
        """
        """
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onClose(self, _event: CommandEvent):
        """
        """
        self.EndModal(CANCEL)

    # noinspection PyUnusedLocal
    def _onArrange(self, _event: CommandEvent):
        PostEvent(dest=self._listeningWindow, event=ForceDirectedLayoutEvent())

    # noinspection PyUnusedLocal
    def _onReset(self, _event: CommandEvent):
        PostEvent(dest=self._listeningWindow, event=ResetDiagramEvent())
