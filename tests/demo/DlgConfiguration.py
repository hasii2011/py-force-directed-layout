
from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import DefaultPosition

from wx import EVT_BUTTON
from wx import EVT_CLOSE
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
from wx import StdDialogButtonSizer
from wx import Window

from wx.lib.agw.floatspin import FS_LEFT
from wx.lib.agw.floatspin import FloatSpin

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallyadvanced.ui.widgets.PositionControl import PositionControl

from tests.demo.DialSelector import DialSelectorParameters
from tests.demo.DialSelector import DialSelector


class DlgConfiguration(SizedDialog):

    def __init__(self, parent: Window):

        style:   int  = DEFAULT_DIALOG_STYLE
        dlgSize: Size = Size(470, 540)

        super().__init__(parent, title='Force Directed Configuration', size=dlgSize, style=style)

        self.logger: Logger = getLogger(__name__)

        sizedPanel:  SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        #
        sizedPanel.SetSizerProps(proportion=1)

        self._layoutForceParameters(parentPanel=sizedPanel)
        self._layoutRandomizeParameters(parentPanel=sizedPanel)
        self._layoutAlgorithmParameters(parentPanel=sizedPanel)
        self._layoutStandardOkCancelButtonSizer()

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

    def _layoutForceParameters(self, parentPanel: SizedPanel):

        localPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Directed Layout Parameters')
        localPanel.SetSizerType('horizontal')
        # noinspection PyUnresolvedReferences
        localPanel.SetSizerProps(expand=True, proportion=2)

        dampingParameters: DialSelectorParameters = DialSelectorParameters(minValue=0.1, maxValue=1.0, dialLabel='Damping', callback=self._formatDampingValue)
        damping:           DialSelector           = DialSelector(localPanel, parameters=dampingParameters)
        damping.tickFrequency = 10
        damping.tickValue     = 0.1

        springLengthParameters: DialSelectorParameters = DialSelectorParameters(minValue=100, maxValue=500, dialLabel='Spring Length', callback=self._formatSpringLength)
        springLength:           DialSelector           = DialSelector(localPanel, parameters=springLengthParameters)
        springLength.tickFrequency = 20
        springLength.tickValue     = 25
        springLength.value         = 100

        #
        # maxIterations: Slider = self._layoutSlider(parentPanel=localPanel, label='Maximum Iterations',
        #                                            value=50, minValue=10, maxValue=1000)
        #
        # maxIterations.SetTickFreq(10)

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
        minCoordinate.position = Position(10, 10)
        maxCoordinate: PositionControl = PositionControl(sizedPanel=horizontalPanel, displayText='Maximum X/Y',
                                                         minValue=10, maxValue=1024,
                                                         valueChangedCallback=self._onMinXY,
                                                         setControlsSize=False)
        maxCoordinate.position = Position(60, 60)

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

        repulsionPanel: SizedStaticBox = SizedStaticBox(algorithmFactorsPanel, label='Node Repulsion Force')
        repulsionPanel.SetSizerType('vertical')
        repulsionPanel.SetSizerProps(proportion=0)

        repulsionFactor: SpinCtrl = SpinCtrl(repulsionPanel, size=(75, 50), pos=DefaultPosition, style=SP_VERTICAL)
        repulsionFactor.SetRange(500, 15000)
        repulsionFactor.SetValue(1000)
        repulsionFactor.SetIncrement(100)

        repulsionFactor.SetSizerProps(expand=True)

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

    def _onDampingChange(self, event: CommandEvent):
        pass

    def _onMinXY(self, commandEvent, Event):
        pass

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
