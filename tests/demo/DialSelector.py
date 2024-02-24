
from typing import List

from dataclasses import dataclass

from logging import Logger
from logging import getLogger

from wx import ALIGN_LEFT
from wx import ID_ANY
from wx import StaticText

from wx.lib.agw.knobctrl import EVT_KC_ANGLE_CHANGED
from wx.lib.agw.knobctrl import KnobCtrl
from wx.lib.agw.knobctrl import KnobCtrlEvent

from wx.lib.sized_controls import SizedStaticBox


@dataclass
class DialRange:
    minValue: int | float = 0
    maxValue: int | float = 0


OPINIONATED_TICK_FREQUENCY: int = 10
OPINIONATED_TICK_VALUE:     int = 10
KNOB_CTRL_GRANULARITY:      int = 100


class DialSelector(SizedStaticBox):
    """
    Using the Adapter pattern.  I don't care what PyBites says
    The wrapped knob control reports 100 positions; We will put
    tick marks (tags) every 10 positions and coerce the reported
    values to align on those marks
    """

    def __init__(self, parent, label: str, valueLabel: str, dialRange: DialRange):

        super().__init__(parent, label=label)
        self.logger: Logger = getLogger(__name__)

        self._valueLabel:    str         = f"{valueLabel}:"
        self._dialRange:     DialRange   = dialRange
        self._tickFrequency: int         = OPINIONATED_TICK_FREQUENCY
        self._tickValue:     int | float = OPINIONATED_TICK_VALUE
        self._value:         int | float = dialRange.minValue

        self.SetSizerType('vertical')
        # noinspection PyUnresolvedReferences
        self.SetSizerProps(expand=True, proportion=1)

        self._knobCtrl: KnobCtrl = KnobCtrl(self, size=(100, 100))

        self._knobCtrl.SetAngularRange(-45, 225)
        self._knobCtrl.SetKnobRadius(4)
        self._setTicksOnKnob()

        self._knobTracker: StaticText = StaticText(parent=self, id=ID_ANY, label=f'{valueLabel}: 0', style=ALIGN_LEFT)

        self._displayValue(value=dialRange.minValue)
        self.Bind(EVT_KC_ANGLE_CHANGED, self._onKnobChanged, self._knobCtrl)

    @property
    def tickFrequency(self) -> int | float:
        return self._tickFrequency

    @tickFrequency.setter
    def tickFrequency(self, value: int):
        """
        The underlying control has a tick granularity of 100. Set a
        value between 1 and 100

        The underlying control computes the value of each tick

        Args:
            value: Indicates how to space out the tick marks
        """
        assert 1 <= value <= 100
        self._tickFrequency = value
        self._setTicksOnKnob()

    @property
    def tickValue(self) -> int | float:
        return self._tickValue

    @tickValue.setter
    def tickValue(self, value: int | float):
        self._tickValue = value

    @property
    def valueLabel(self) -> str:
        return self._valueLabel

    @valueLabel.setter
    def valueLabel(self, label: str):
        self._valueLabel = label

    @property
    def value(self) -> int | float:
        """
        The returned value is between the min/max values specified in the
        dial range;  It is modulo the specified tick frequency.
        Returns:  The current control value
        """
        return self._value

    @value.setter
    def value(self, newValue: int | float):
        self._value = newValue

    def _onKnobChanged(self, event: KnobCtrlEvent):

        knobValue:        int = event.GetValue()
        roundedKnobValue: int = self._alignKnobToTick(knobValue=knobValue)
        self._knobCtrl.SetValue(roundedKnobValue)

        realValue = DialSelector.calculateRealValue(roundedKnobValue=roundedKnobValue,
                                                    tickValue=self._tickValue,
                                                    tickFrequency=self._tickFrequency)

        self.logger.info(f'realValue={realValue:.2f}')
        self._displayValue(value=realValue)

        self._value = realValue

        event.Skip(skip=True)

    def _alignKnobToTick(self, knobValue: int):

        # TODO: This will be moved to codeallybasic
        # Including the unit tests
        #
        def roundToNearestTick(valueToRound, boundaryValue: int) -> int:
            return int(round(valueToRound / boundaryValue)) * boundaryValue

        roundToIncrement: int = KNOB_CTRL_GRANULARITY // self._tickFrequency

        roundedKnobValue: int = roundToNearestTick(valueToRound=knobValue, boundaryValue=roundToIncrement)

        self.logger.info(f'{knobValue=} {roundedKnobValue=}')

        return roundedKnobValue

    def _setTicksOnKnob(self):
        assert self._dialRange is not None, 'Developer Error'
        assert self._tickFrequency != 0, 'Developer Error'
        assert self._knobCtrl is not None, 'Developer Error'

        integerList:   List[int] = list(range(1, self._tickFrequency + 1, 1))

        self.logger.info(f'{integerList=}')
        self._knobCtrl.SetTags(integerList)

    def _displayValue(self, value: int | float):
        self._knobTracker.SetLabel(f'{self._valueLabel} {value:.2f}')
        self._knobTracker.Refresh()

    @classmethod
    def calculateRealValue(cls, roundedKnobValue: int, tickValue: int | float, tickFrequency: int):

        tickPosition:  int = int((roundedKnobValue / KNOB_CTRL_GRANULARITY) * tickFrequency)

        realValue    = tickValue * tickPosition

        return realValue
