
from typing import cast

from logging import Logger
from logging import getLogger

from wx import EVT_SPINCTRL
from wx import EVT_SPINCTRLDOUBLE
from wx import SP_VERTICAL

from wx import Size
from wx import SpinCtrl
from wx import SpinEvent
from wx import SpinCtrlDouble
from wx import DefaultPosition
from wx import SpinDoubleEvent

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallybasic.MinMax import MinMax

from codeallyadvanced.ui.widgets.MacDialSelector import MacDialSelector
from codeallyadvanced.ui.widgets.MacDialSelector import MacDialSelectorParameters
from codeallyadvanced.ui.widgets.MacDialSelector import ValueRange
from codeallyadvanced.ui.widgets.MinMaxControl import MinMaxControl
from codeallyadvanced.ui.widgets.MinMaxControl import MinMaxParameters

from pyforcedirectedlayout.Configuration import Configuration
from pyforcedirectedlayout.Configuration import X_RANGE_MAX
from pyforcedirectedlayout.Configuration import X_RANGE_MIN
from pyforcedirectedlayout.Configuration import Y_RANGE_MAX
from pyforcedirectedlayout.Configuration import Y_RANGE_MIN


DAMPING_MIN:  float = 0.1
DAMPING_MAX:  float = 1.0
DAMPING_STEP: float = 0.1

SPRING_LENGTH_MIN:  float = 100.0
SPRING_LENGTH_MAX:  float = 500.0
SPRING_LENGTH_STEP: float = 25.0

MAX_ITERATIONS_MIN:  float = 100.0
MAX_ITERATIONS_MAX:  float = 1000.0
MAX_ITERATIONS_STEP: float = 20.0

NODE_ATTRACTION_FORCE_MIN:       float = 0.01
NODE_ATTRACTION_FORCE_MAX:       float = 1.0
NODE_ATTRACTION_FORCE_INCREMENT: float = 0.05

REPULSION_FORCE_MIN: int = 500
REPULSION_FORCE_MAX: int = 25000

NO_MAC_DIAL_SELECTOR: MacDialSelector = cast(MacDialSelector, cast(object, None))


class ConfigurationPanel:
    """
    Builds the force-directed layout configuration controls inside a parent SizedPanel.
    Assumes the parent panel is vertically oriented.

    Updates the Configuration singleton as the user changes values.
    """
    def __init__(self, sizedPanel: SizedPanel):

        self.logger: Logger = getLogger(__name__)

        self._configuration: Configuration = Configuration()

        self._damping:       MacDialSelector = NO_MAC_DIAL_SELECTOR
        self._springLength:  MacDialSelector = NO_MAC_DIAL_SELECTOR
        self._maxIterations: MacDialSelector = NO_MAC_DIAL_SELECTOR

        self._layoutForceParameters(parentPanel=sizedPanel)
        self._layoutRandomizeParameters(parentPanel=sizedPanel)
        self._layoutAlgorithmParameters(parentPanel=sizedPanel)

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

        dampingParameters: MacDialSelectorParameters = MacDialSelectorParameters(
            valueChangedCallback=self._dampingChanged,
            valueRange=ValueRange(
                minValue=DAMPING_MIN,
                maxValue=DAMPING_MAX,
                initialValue=self._configuration.damping,
                step=DAMPING_STEP
            ),
            dialLabel='Damping',
            formatValueCallback=self._formatDampingValue
        )
        damping: MacDialSelector = MacDialSelector(localPanel, parameters=dampingParameters)

        springLengthParameters: MacDialSelectorParameters = MacDialSelectorParameters(
            valueChangedCallback=self._springLengthChanged,
            valueRange=ValueRange(
                minValue=SPRING_LENGTH_MIN,
                maxValue=SPRING_LENGTH_MAX,
                initialValue=float(self._configuration.springLength),
                step=SPRING_LENGTH_STEP
            ),
            dialLabel='Spring Length',
            formatValueCallback=self._formatSpringLength
        )
        springLength: MacDialSelector = MacDialSelector(localPanel, parameters=springLengthParameters)

        maxIterationsParameters: MacDialSelectorParameters = MacDialSelectorParameters(
            valueChangedCallback=self._maxIterationsChanged,
            valueRange=ValueRange(
                minValue=MAX_ITERATIONS_MIN,
                maxValue=MAX_ITERATIONS_MAX,
                initialValue=float(self._configuration.maxIterations),
                step=MAX_ITERATIONS_STEP
            ),
            dialLabel='Maximum Iterations',
            formatValueCallback=self._formatMaxIterations
        )
        maxIterations: MacDialSelector = MacDialSelector(localPanel, parameters=maxIterationsParameters)

        self._damping       = damping
        self._springLength  = springLength
        self._maxIterations = maxIterations

    def _layoutRandomizeParameters(self, parentPanel: SizedPanel):

        localPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Randomize Initial Layout Parameters')
        localPanel.SetSizerType('vertical')
        localPanel.SetSizerProps(expand=True, proportion=1)

        horizontalPanel: SizedPanel = SizedPanel(localPanel)
        horizontalPanel.SetSizerType('horizontal')
        horizontalPanel.SetSizerProps(expand=True, proportion=1)

        minMaxXParameters: MinMaxParameters = MinMaxParameters(caption='Minimum/Maximum X Value',
                                                               minValue=X_RANGE_MIN, maxValue=X_RANGE_MAX,
                                                               valueChangedCallback=self._onMinMaxX,
                                                               proportion=1)
        minMaxX: MinMaxControl = MinMaxControl(parent=horizontalPanel, parameters=minMaxXParameters)
        minMaxX.minMax = self._configuration.minMaxX

        minMaxYParameters: MinMaxParameters = MinMaxParameters(caption='Minimum/Maximum Y Value',
                                                               minValue=Y_RANGE_MIN, maxValue=Y_RANGE_MAX,
                                                               valueChangedCallback=self._onMinMaxY,
                                                               proportion=1)
        minMaxY: MinMaxControl = MinMaxControl(parent=horizontalPanel, parameters=minMaxYParameters)
        minMaxY.minMax = self._configuration.minMaxY

    def _layoutAlgorithmParameters(self, parentPanel: SizedPanel):

        algorithmFactorsPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Algorithm Parameters')
        algorithmFactorsPanel.SetSizerType('horizontal')
        algorithmFactorsPanel.SetSizerProps(expand=True, proportion=1)

        attractionPanel: SizedStaticBox = SizedStaticBox(algorithmFactorsPanel, label='Node Attraction Force')
        attractionPanel.SetSizerType('vertical')
        attractionPanel.SetSizerProps(proportion=0)

        attractionForce: SpinCtrlDouble = SpinCtrlDouble(attractionPanel,
                                                         min=NODE_ATTRACTION_FORCE_MIN,
                                                         max=NODE_ATTRACTION_FORCE_MAX,
                                                         inc=NODE_ATTRACTION_FORCE_INCREMENT,
                                                         size=Size(75, 35))
        attractionForce.SetDigits(2)
        attractionForce.SetValue(self._configuration.attractionForce)
        attractionForce.Bind(EVT_SPINCTRLDOUBLE, self._attractionForceChanged)

        repulsionPanel: SizedStaticBox = SizedStaticBox(algorithmFactorsPanel, label='Node Repulsion Force')
        repulsionPanel.SetSizerType('vertical')
        repulsionPanel.SetSizerProps(proportion=0)

        repulsionForce: SpinCtrl = SpinCtrl(repulsionPanel, size=Size(75, 35), pos=DefaultPosition, style=SP_VERTICAL)
        repulsionForce.SetRange(REPULSION_FORCE_MIN, REPULSION_FORCE_MAX)
        repulsionForce.SetValue(self._configuration.repulsionForce)
        repulsionForce.SetIncrement(100)
        repulsionForce.Bind(EVT_SPINCTRL, self._repulsionForceChanged)

    def _formatDampingValue(self, valueToFormat: float):

        return f'{valueToFormat:.2f}'

    def _formatSpringLength(self, valueToFormat: float):
        return f'{int(valueToFormat)}'

    def _formatMaxIterations(self, valueToFormat: float):
        return f'{int(valueToFormat)}'

    def _dampingChanged(self, newValue: float):
        self._configuration.damping = newValue

    def _springLengthChanged(self, newValue: float):
        self._configuration.springLength = int(newValue)

    def _maxIterationsChanged(self, newValue: float):
        self._configuration.maxIterations = int(newValue)

    def _onMinMaxX(self, minMaxX: MinMax):
        self._configuration.minMaxX = minMaxX

    def _onMinMaxY(self, minMaxY: MinMax):
        self._configuration.minMaxY = minMaxY

    def _attractionForceChanged(self, event: SpinDoubleEvent):

        spinCtrlDouble: SpinCtrlDouble = cast(SpinCtrlDouble, event.GetEventObject())

        self._configuration.attractionForce = spinCtrlDouble.GetValue()

    def _repulsionForceChanged(self, event: SpinEvent):

        spinCtrl: SpinCtrl = cast(SpinCtrl, event.GetEventObject())

        self._configuration.repulsionForce = spinCtrl.GetValue()
