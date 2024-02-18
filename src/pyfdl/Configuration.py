from pyfdl.ConfigurationProperties import ConfigurationNameValue
from pyfdl.ConfigurationProperties import ConfigurationProperties
from pyfdl.ConfigurationProperties import PropertyName
from pyfdl.ConfigurationProperties import Section
from pyfdl.ConfigurationProperties import SectionName
from pyfdl.ConfigurationProperties import Sections
from pyfdl.ConfigurationProperties import configurationGetter
from pyfdl.ConfigurationProperties import configurationSetter
from pyfdl.Point import Point

# these are for the arrange method
SECTION_ARRANGE: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('damping'),       defaultValue='0.5'),
        ConfigurationNameValue(name=PropertyName('springLength'),  defaultValue='100'),
        ConfigurationNameValue(name=PropertyName('maxIterations'), defaultValue='500'),
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
SECTION_FACTORS: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('attractionFactor'),         defaultValue='0.1'),
        ConfigurationNameValue(name=PropertyName('repulsionFactor'),          defaultValue='10000'),
        ConfigurationNameValue(name=PropertyName('minimumTotalDisplacement'), defaultValue='10'),
        ConfigurationNameValue(name=PropertyName('stopCount'),                defaultValue='15'),
    ]
)

ARRANGE_SECTION_NAME:   SectionName = SectionName('Arrange')
RANDOMIZE_SECTION_NAME: SectionName = SectionName('Randomize')
FACTORS_SECTION_NAME:   SectionName = SectionName('Factors')

PYFDL_SECTIONS: Sections = Sections(
    {
        ARRANGE_SECTION_NAME:   SECTION_ARRANGE,
        RANDOMIZE_SECTION_NAME: SECTION_RANDOMIZE,
        FACTORS_SECTION_NAME:   SECTION_FACTORS,
    }
)


class Configuration(ConfigurationProperties):

    def __init__(self):
        super().__init__(baseFileName='pyfdl.ini', moduleName='pyfdl', sections=PYFDL_SECTIONS)

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
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=float)
    def attractionFactor(self) -> float:
        return 0.0

    @attractionFactor.setter
    @configurationSetter(sectionName=FACTORS_SECTION_NAME)
    def attractionFactor(self, newValue: float):
        pass

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=int)
    def repulsionFactor(self) -> int:
        return 0

    @repulsionFactor.setter
    @configurationSetter(sectionName=FACTORS_SECTION_NAME)
    def repulsionFactor(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=int)
    def minimumTotalDisplacement(self) -> int:
        return 0

    @minimumTotalDisplacement.setter
    @configurationSetter(sectionName=FACTORS_SECTION_NAME)
    def minimumTotalDisplacement(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=int)
    def stopCount(self) -> int:
        return 0

    @stopCount.setter
    @configurationSetter(sectionName=FACTORS_SECTION_NAME)
    def stopCount(self, newValue: int):
        pass

