
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Button
from wx import CANCEL
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import DefaultPosition

from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_SPINCTRL
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import SL_AUTOTICKS
from wx import SL_BOTTOM
from wx import SL_HORIZONTAL

from wx import SL_VALUE_LABEL
from wx import SP_VERTICAL
from wx import Size
from wx import Slider
from wx import SpinCtrl
from wx import SpinEvent
from wx import StdDialogButtonSizer
from wx import Window

from wx.lib.agw.floatspin import EVT_FLOATSPIN
from wx.lib.agw.floatspin import FS_LEFT
from wx.lib.agw.floatspin import FloatSpin
from wx.lib.agw.floatspin import FloatSpinEvent

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallybasic.Position import Position
from codeallyadvanced.ui.widgets.PositionControl import PositionControl

from pyfdl.Configuration import Configuration
from pyfdl.Point import Point

from tests.demo.DialSelector import DialSelectorParameters
from tests.demo.DialSelector import DialSelector

NO_DIAL_SELECTOR: DialSelector = cast(DialSelector, None)
NO_BUTTON:        Button       = cast(Button, None)


class DlgConfiguration(SizedDialog):

    def __init__(self, parent: Window):

        style:   int  = DEFAULT_DIALOG_STYLE
        dlgSize: Size = Size(470, 540)

        super().__init__(parent, title='Force Directed Configuration', size=dlgSize, style=style)

        self._configuration: Configuration = Configuration()

        self.logger: Logger = getLogger(__name__)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        sizedPanel.SetSizerProps(proportion=1)

        self._damping:       DialSelector = NO_DIAL_SELECTOR
        self._springLength:  DialSelector = NO_DIAL_SELECTOR
        self._maxIterations: DialSelector = NO_DIAL_SELECTOR

        self._layoutForceParameters(parentPanel=sizedPanel)
        self._layoutRandomizeParameters(parentPanel=sizedPanel)
        self._layoutAlgorithmParameters(parentPanel=sizedPanel)
        # self._layoutStandardOkCancelButtonSizer()

        self._btnCancel: Button = NO_BUTTON
        self._btnOk:     Button = NO_BUTTON

        self._layoutCustomDialogButtons(parent=sizedPanel)

        # self.Fit()
        # self.SetMinSize(self.GetSize())

    def _layoutStandardOkCancelButtonSizer(self):
        """
        Call this last when creating controls; Will take care of
        adding callbacks for the Ok and Cancel buttons
        """
        buttSizer: StdDialogButtonSizer = self.CreateStdDialogButtonSizer(OK | CANCEL)

        self.SetButtonSizer(buttSizer)
        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

    def _layoutCustomDialogButtons(self, parent: SizedPanel):

        buttonPanel: SizedPanel = SizedPanel(parent)
        buttonPanel.SetSizerType('horizontal')
        buttonPanel.SetSizerProps(expand=False, border=(['top'], 20), halign='right')  # expand False allows aligning right

        arrangeButton: Button = Button(buttonPanel, label='&Arrange')
        resetButton:   Button = Button(buttonPanel, label='&Reset')

        self._btnCancel = Button(buttonPanel, ID_CANCEL, '&Cancel')
        self._btnOk     = Button(buttonPanel, ID_OK, '&Ok')

        self.Bind(EVT_BUTTON, self._onReset, resetButton)
        self.Bind(EVT_BUTTON, self._onArrange, arrangeButton)
        self.Bind(EVT_BUTTON, self._onOk,    self._btnOk)
        self.Bind(EVT_BUTTON, self._onClose, self._btnCancel)
        self.Bind(EVT_CLOSE,  self._onClose, self._btnCancel)

        self._btnOk.SetDefault()

    def _layoutForceParameters(self, parentPanel: SizedPanel):
        """
        Sets the protected properties:

        self._damping
        self._springLength
        self._maxIterations

        Args:
            parentPanel:  The panel that hosts these components
        """

        localPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Directed Layout Parameters')
        localPanel.SetSizerType('horizontal')
        localPanel.SetSizerProps(expand=True, proportion=2)

        dampingParameters: DialSelectorParameters = DialSelectorParameters(minValue=0.1, maxValue=1.0, dialLabel='Damping',
                                                                           formatValueCallback=self._formatDampingValue,
                                                                           valueChangedCallback=self._dampingChanged)
        damping:           DialSelector           = DialSelector(localPanel, parameters=dampingParameters)
        damping.tickFrequency = 10
        damping.tickValue     = 0.1
        damping.value         = self._configuration.damping

        springLengthParameters: DialSelectorParameters = DialSelectorParameters(minValue=100, maxValue=500, dialLabel='Spring Length',
                                                                                formatValueCallback=self._formatSpringLength,
                                                                                valueChangedCallback=self._springLengthChanged)

        springLength:           DialSelector           = DialSelector(localPanel, parameters=springLengthParameters)
        springLength.tickFrequency = 20
        springLength.tickValue     = 25
        springLength.value         = self._configuration.springLength

        maxIterationsParameters: DialSelectorParameters = DialSelectorParameters(minValue=100,
                                                                                 maxValue=1000,
                                                                                 dialLabel='Maximum Iterations',
                                                                                 formatValueCallback=self._formatMaxIterations,
                                                                                 valueChangedCallback=self._maxIterationsChanged)
        maxIterations: DialSelector = DialSelector(localPanel, parameters=maxIterationsParameters)
        maxIterations.tickFrequency = 50
        maxIterations.tickValue     = 20
        maxIterations.value         = self._configuration.maxIterations

        self._damping       = damping
        self._springLength  = springLength
        self._maxIterations = maxIterations

    def _layoutRandomizeParameters(self, parentPanel: SizedPanel):
        from codeallybasic.Position import Position

        localPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Randomize Initial Layout Parameters')
        localPanel.SetSizerType('vertical')
        localPanel.SetSizerProps(expand=True, proportion=1)

        horizontalPanel: SizedPanel = SizedPanel(localPanel)
        horizontalPanel.SetSizerType('horizontal')
        horizontalPanel.SetSizerProps(expand=True, proportion=1)

        minCoordinate: PositionControl = PositionControl(sizedPanel=horizontalPanel, displayText='Minimum X/Y',
                                                         minValue=10, maxValue=1024,
                                                         valueChangedCallback=self._onMinXY,
                                                         setControlsSize=False)
        minPoint: Point = self._configuration.minPoint
        minCoordinate.position = Position(x=minPoint.x, y=minPoint.y)

        maxCoordinate: PositionControl = PositionControl(sizedPanel=horizontalPanel, displayText='Maximum X/Y',
                                                         minValue=10, maxValue=1024,
                                                         valueChangedCallback=self._onMaxXY,
                                                         setControlsSize=False)
        maxPoint: Point = self._configuration.maxPoint
        maxCoordinate.position = Position(x=maxPoint.x, y=maxPoint.y)

    def _layoutAlgorithmParameters(self, parentPanel: SizedPanel):

        algorithmFactorsPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Algorithm Parameters')
        algorithmFactorsPanel.SetSizerType('horizontal')
        algorithmFactorsPanel.SetSizerProps(expand=True, proportion=1)

        attractionPanel: SizedStaticBox = SizedStaticBox(algorithmFactorsPanel, label='Node Attraction Force')
        attractionPanel.SetSizerType('vertical')
        attractionPanel.SetSizerProps(proportion=0)

        attractionForce: FloatSpin = FloatSpin(attractionPanel, min_val=0.1, max_val=1.0, increment=0.1, value=0.1,
                                               pos=(-1, -1), size=(75, 50), agwStyle=FS_LEFT)
        attractionForce.SetSizerProps(expand=True)
        # noinspection PyArgumentList
        attractionForce.SetDigits(2)
        # noinspection PyArgumentList
        attractionForce.SetValue(self._configuration.attractionForce)
        attractionForce.Bind(EVT_FLOATSPIN, self._attractionForceChanged)

        repulsionPanel: SizedStaticBox = SizedStaticBox(algorithmFactorsPanel, label='Node Repulsion Force')
        repulsionPanel.SetSizerType('vertical')
        repulsionPanel.SetSizerProps(proportion=0)

        repulsionForce: SpinCtrl = SpinCtrl(repulsionPanel, size=(75, 35), pos=DefaultPosition, style=SP_VERTICAL)
        repulsionForce.SetRange(500, 15000)
        repulsionForce.SetValue(self._configuration.repulsionForce)
        repulsionForce.SetIncrement(100)
        repulsionForce.Bind(EVT_SPINCTRL, self._repulsionForceChanged)

        # repulsionFactor.SetSizerProps(expand=True)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        """
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onClose(self, event: CommandEvent):
        """
        """
        self.EndModal(CANCEL)

    # noinspection PyUnusedLocal
    def _onArrange(self, event: CommandEvent):
        pass

    # noinspection PyUnusedLocal
    def _onReset(self, event: CommandEvent):
        pass

    def _onMinXY(self, position: Position):
        self._configuration.minPoint = Point(x=position.x, y=position.y)

    def _onMaxXY(self, position: Position):
        self._configuration.maxPoint = Point(x=position.x, y=position.y)

    def _layoutSlider(self, parentPanel, label: str, value: int,  minValue: int, maxValue: int) -> Slider:

        namingPanel: SizedStaticBox = SizedStaticBox(parentPanel, label=label)
        namingPanel.SetSizerType('horizontal')
        namingPanel.SetSizerProps(expand=True, proportion=1)

        style:  int    = SL_HORIZONTAL | SL_AUTOTICKS | SL_VALUE_LABEL | SL_BOTTOM
        slider: Slider = Slider(namingPanel, value=value, minValue=minValue, maxValue=maxValue, size=(250, 50), style=style)

        slider.SetSizerProps(expand=True, proportion=1)

        return slider

    def _formatDampingValue(self, valueToFormat: float):

        return f'{valueToFormat:.2f}'

    def _formatSpringLength(self, valueToFormat: int):
        return f'{valueToFormat}'

    def _formatMaxIterations(self, valueToFormat: int):
        return f'{valueToFormat}'

    def _dampingChanged(self, newValue: int):
        self._configuration.damping = newValue

    def _springLengthChanged(self, newValue: int):
        self._configuration.springLength = newValue

    def _maxIterationsChanged(self, newValue: int):
        self._configuration.maxIterations = newValue

    def _attractionForceChanged(self, event: FloatSpinEvent):

        floatSpin: FloatSpin = event.GetEventObject()

        self._configuration.attractionForce = floatSpin.GetValue()

    def _repulsionForceChanged(self, event: SpinEvent):

        spinCtrl: SpinCtrl = event.GetEventObject()

        self._configuration.repulsionForce = spinCtrl.GetValue()
