
from codeallybasic.SingletonV3 import SingletonV3

from codeallybasic.ConfigurationProperties import ConfigurationNameValue
from codeallybasic.ConfigurationProperties import ConfigurationProperties
from codeallybasic.ConfigurationProperties import PropertyName
from codeallybasic.ConfigurationProperties import Section
from codeallybasic.ConfigurationProperties import SectionName
from codeallybasic.ConfigurationProperties import Sections
from codeallybasic.ConfigurationProperties import configurationGetter
from codeallybasic.ConfigurationProperties import configurationSetter

from pyforcedirectedlayout.Point import Point

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
        ConfigurationNameValue(name=PropertyName('minPoint'), defaultValue=Point(x=10, y=10).__repr__()),
        ConfigurationNameValue(name=PropertyName('maxPoint'), defaultValue=Point(x=60, y=60).__repr__()),
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
        super().__init__(baseFileName='pyforcedirectedlayout.ini', moduleName='pyforcedirectedlayout', sections=PYFDL_SECTIONS)

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
    @configurationGetter(sectionName=RANDOMIZE_SECTION_NAME, deserializeFunction=Point.deSerialize)
    def minPoint(self) -> Point:
        return Point()

    @minPoint.setter
    @configurationSetter(sectionName=RANDOMIZE_SECTION_NAME)
    def minPoint(self, newValue: Point):
        pass

    @property
    @configurationGetter(sectionName=RANDOMIZE_SECTION_NAME, deserializeFunction=Point.deSerialize)
    def maxPoint(self) -> Point:
        return Point()

    @maxPoint.setter
    @configurationSetter(sectionName=RANDOMIZE_SECTION_NAME)
    def maxPoint(self, newValue: Point):
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
