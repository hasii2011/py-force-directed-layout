
from logging import Logger
from logging import getLogger

from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections

from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions
from codeallybasic.MinMax import MinMax

from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.SingletonV3 import SingletonV3

X_RANGE_MIN: int = -1024
X_RANGE_MAX: int = 1024
Y_RANGE_MIN: int = -1024
Y_RANGE_MAX: int = 1024

arrangeProperties: ValueDescriptions = ValueDescriptions(
    {
        KeyName('damping'):         ValueDescription(defaultValue='0.5',   deserializer=SecureConversions.secureFloat),
        KeyName('springLength'):    ValueDescription(defaultValue='100',   deserializer=SecureConversions.secureInteger),
        KeyName('maxIterations'):   ValueDescription(defaultValue='500',   deserializer=SecureConversions.secureInteger),
        KeyName('attractionForce'): ValueDescription(defaultValue='0.1',   deserializer=SecureConversions.secureFloat),
        KeyName('repulsionForce'):  ValueDescription(defaultValue='10000', deserializer=SecureConversions.secureInteger),
    }
)

DEFAULT_MIN_X_COORDINATE: int = -50
DEFAULT_MAX_X_COORDINATE: int = 50
DEFAULT_MIN_Y_COORDINATE: int = -50
DEFAULT_MAX_Y_COORDINATE: int = 50

DEFAULT_MIN_MAX_X: str = MinMax(minValue=DEFAULT_MIN_X_COORDINATE, maxValue=DEFAULT_MAX_X_COORDINATE).__repr__()
DEFAULT_MIN_MAX_Y: str = MinMax(minValue=DEFAULT_MIN_Y_COORDINATE, maxValue=DEFAULT_MAX_Y_COORDINATE).__repr__()

randomizeProperties: ValueDescriptions = ValueDescriptions(
    {
        KeyName('minMaxX'): ValueDescription(defaultValue=DEFAULT_MIN_MAX_X, deserializer=MinMax.deSerialize),
        KeyName('minMaxY'): ValueDescription(defaultValue=DEFAULT_MIN_MAX_Y, deserializer=MinMax.deSerialize),
    }
)
"""
Stop execution after this many number of iterations
where the totalDisplacement is less that minimumTotalDisplacement
"""
earlyExitProperties: ValueDescriptions = ValueDescriptions(
    {
        KeyName('minimumTotalDisplacement'): ValueDescription(defaultValue='10', deserializer=SecureConversions.secureInteger),
        KeyName('stopCount'):                ValueDescription(defaultValue='15', deserializer=SecureConversions.secureInteger),
    }
)
PYFDL_SECTIONS: Sections = Sections(
    {
        SectionName('Arrange'):   arrangeProperties,
        SectionName('Randomize'): randomizeProperties,
        SectionName('EarlyExit'): earlyExitProperties,
    }
)


class Configuration(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):

        self._logger: Logger = getLogger(__name__)

        super().__init__(baseFileName='pyfdl.ini', moduleName='pydfl', sections=PYFDL_SECTIONS)
