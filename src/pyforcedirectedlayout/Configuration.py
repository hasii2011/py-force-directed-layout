
from codeallybasic.MinMax import MinMax
from codeallybasic.SingletonV3 import SingletonV3

from codeallybasic.ConfigurationProperties import ConfigurationNameValue
from codeallybasic.ConfigurationProperties import ConfigurationProperties
from codeallybasic.ConfigurationProperties import PropertyName
from codeallybasic.ConfigurationProperties import Section
from codeallybasic.ConfigurationProperties import SectionName
from codeallybasic.ConfigurationProperties import Sections
from codeallybasic.ConfigurationProperties import configurationGetter
from codeallybasic.ConfigurationProperties import configurationSetter


X_RANGE_MIN: int = -1024
X_RANGE_MAX: int = 1024
Y_RANGE_MIN: int = -1024
Y_RANGE_MAX: int = 1024

DEFAULT_MIN_X_COORDINATE: int = -50
DEFAULT_MAX_X_COORDINATE: int = 50
DEFAULT_MIN_Y_COORDINATE: int = -50
DEFAULT_MAX_Y_COORDINATE: int = 50


# these are for the arrange method
SECTION_ARRANGE: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('damping'),       defaultValue='0.5'),
        ConfigurationNameValue(name=PropertyName('springLength'),  defaultValue='100'),
        ConfigurationNameValue(name=PropertyName('maxIterations'), defaultValue='500'),
        ConfigurationNameValue(name=PropertyName('attractionForce'), defaultValue='0.1'),
        ConfigurationNameValue(name=PropertyName('repulsionForce'), defaultValue='10000'),
    ]
)

# these randomize the layout
SECTION_RANDOMIZE: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('minMaxX'), defaultValue=MinMax(minValue=DEFAULT_MIN_X_COORDINATE, maxValue=DEFAULT_MAX_X_COORDINATE).__repr__()),
        ConfigurationNameValue(name=PropertyName('minMaxY'), defaultValue=MinMax(minValue=DEFAULT_MIN_Y_COORDINATE, maxValue=DEFAULT_MAX_Y_COORDINATE).__repr__()),
    ]
)
"""
Stop execution after this many number of iterations
where the totalDisplacement is less that minimumTotalDisplacement
"""
SECTION_EARLY_EXIT: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('minimumTotalDisplacement'), defaultValue='10'),
        ConfigurationNameValue(name=PropertyName('stopCount'),                defaultValue='15'),
    ]
)

ARRANGE_SECTION_NAME:    SectionName = SectionName('Arrange')
RANDOMIZE_SECTION_NAME:  SectionName = SectionName('Randomize')
EARLY_EXIT_SECTION_NAME: SectionName = SectionName('EarlyExit')

PYFDL_SECTIONS: Sections = Sections(
    {
        ARRANGE_SECTION_NAME:    SECTION_ARRANGE,
        RANDOMIZE_SECTION_NAME:  SECTION_RANDOMIZE,
        EARLY_EXIT_SECTION_NAME: SECTION_EARLY_EXIT,
    }
)


class Configuration(ConfigurationProperties, metaclass=SingletonV3):

    def __init__(self):
        super().__init__(baseFileName='pyfdl.ini', moduleName='pydfl', sections=PYFDL_SECTIONS)

        self._loadConfiguration()

    @property
    @configurationGetter(sectionName=ARRANGE_SECTION_NAME, deserializeFunction=float)
    def damping(self) -> float:
        return 0.0

    @damping.setter
    @configurationSetter(sectionName=ARRANGE_SECTION_NAME)
    def damping(self, newValue: float):
        pass

    @property
    @configurationGetter(sectionName=ARRANGE_SECTION_NAME, deserializeFunction=int)
    def springLength(self) -> int:
        return 0

    @springLength.setter
    @configurationSetter(sectionName=ARRANGE_SECTION_NAME)
    def springLength(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=ARRANGE_SECTION_NAME, deserializeFunction=int)
    def maxIterations(self) -> int:
        return 0

    @maxIterations.setter
    @configurationSetter(sectionName=ARRANGE_SECTION_NAME)
    def maxIterations(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=ARRANGE_SECTION_NAME, deserializeFunction=float)
    def attractionForce(self) -> float:
        return 0.0

    @attractionForce.setter
    @configurationSetter(sectionName=ARRANGE_SECTION_NAME)
    def attractionForce(self, newValue: float):
        pass

    @property
    @configurationGetter(sectionName=ARRANGE_SECTION_NAME, deserializeFunction=int)
    def repulsionForce(self) -> int:
        return 0

    @repulsionForce.setter
    @configurationSetter(sectionName=ARRANGE_SECTION_NAME)
    def repulsionForce(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=RANDOMIZE_SECTION_NAME, deserializeFunction=MinMax.deSerialize)
    def minMaxX(self) -> MinMax:
        return MinMax()

    @minMaxX.setter
    @configurationSetter(sectionName=RANDOMIZE_SECTION_NAME)
    def minMaxX(self, newValue: MinMax):
        pass

    @property
    @configurationGetter(sectionName=RANDOMIZE_SECTION_NAME, deserializeFunction=MinMax.deSerialize)
    def minMaxY(self) -> MinMax:
        return MinMax()

    @minMaxY.setter
    @configurationSetter(sectionName=RANDOMIZE_SECTION_NAME)
    def minMaxY(self, newValue: MinMax):
        pass

    @property
    @configurationGetter(sectionName=EARLY_EXIT_SECTION_NAME, deserializeFunction=int)
    def minimumTotalDisplacement(self) -> int:
        return 0

    @minimumTotalDisplacement.setter
    @configurationSetter(sectionName=EARLY_EXIT_SECTION_NAME)
    def minimumTotalDisplacement(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=EARLY_EXIT_SECTION_NAME, deserializeFunction=int)
    def stopCount(self) -> int:
        return 0

    @stopCount.setter
    @configurationSetter(sectionName=EARLY_EXIT_SECTION_NAME)
    def stopCount(self, newValue: int):
        pass
