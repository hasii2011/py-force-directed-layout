
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from functools import wraps

from configparser import ConfigParser

from pathlib import Path

from codeallybasic.ConfigurationLocator import ConfigurationLocator


def configurationSetter(sectionName: str):

    def decoratorConfigurationSetter(func):
        @wraps(func)
        def setWrapper(*args, **kwargs):
            """
            Wrapper function
            """
            baseConfiguration: ConfigurationProperties = args[0]
            configParser: ConfigParser = baseConfiguration.configurationParser

            configParser.set(sectionName, f'{func.__name__}', str(args[1]))
            baseConfiguration.saveConfiguration()

            value = func(*args, **kwargs)
            print(f'Do something after')
            return value

        return setWrapper
    return decoratorConfigurationSetter


def configurationGetter(sectionName: str):

    def decoratorConfigurationGetter(func):

        # noinspection PyUnusedLocal
        @wraps(func)
        def getWrapper(*args, **kwargs):
            """
            Wrapper function
            """
            baseConfiguration: ConfigurationProperties = args[0]
            configParser: ConfigParser = baseConfiguration.configurationParser

            value = configParser.get(sectionName, f'{func.__name__}')
            #  value = func(*args, **kwargs)   do not bother calling original

            return value
        return getWrapper
    return decoratorConfigurationGetter


DeSerializeFunction = Callable[[str], Any]
"""
Function that takes a string and does a custom deserialization
"""


@dataclass
class ConfigurationNameValue:

    name:                str = ''
    defaultValue:        str = ''
    deserializeFunction: DeSerializeFunction = cast(DeSerializeFunction, None)


PropertyName = NewType('PropertyName', str)
SectionName  = NewType('SectionName', str)

Section  = NewType('Section',  List[ConfigurationNameValue])
Sections = NewType('Sections', Dict[SectionName, Section])


class ConfigurationProperties:
    """

    """
    def __init__(self, moduleName: str, baseFileName, sections: Sections):

        self.logger: Logger = getLogger(__name__)

        locator: ConfigurationLocator = ConfigurationLocator()

        self._fqFileName:   Path         = locator.applicationPath(f'{moduleName}') / baseFileName
        self._configParser: ConfigParser = ConfigParser()

        self._sections: Sections = sections

        self._loadConfiguration()

    @property
    def configurationParser(self) -> ConfigParser:
        return self._configParser

    @property
    def fileName(self) -> Path:
        return self._fqFileName

    def saveConfiguration(self):
        """
        Save data to the configuration file
        """
        with self._fqFileName.open(mode='w') as fd:
            self._configParser.write(fd)

    def _loadConfiguration(self):

        self._ensureConfigurationFileExists()
        # Read data
        self._configParser.read(self._fqFileName)
        self._addMissingSections()
        self._addMissingPreferences()

    def _ensureConfigurationFileExists(self):

        fileName: Path = self._fqFileName
        if fileName.exists() is False:
            with fileName.open(mode='w') as fd:
                fd.write('')
            self.logger.warning(f'Empty Configuration file created')

    def _addMissingSections(self):

        for sectionName in self._sections:
            if self._configParser.has_section(sectionName) is False:
                self._configParser.add_section(sectionName)
                self.saveConfiguration()

    def _addMissingPreferences(self):

        for sectionName in self._sections:
            section: Section = self._sections[sectionName]
            for c in section:
                cfgNameValue: ConfigurationNameValue = cast(ConfigurationNameValue, c)
                self.logger.info(f'{cfgNameValue=}')
                if self._configParser.has_option(sectionName, cfgNameValue.name) is False:
                    self._addMissingPreference(sectionName=sectionName, preferenceName=cfgNameValue.name, value=cfgNameValue.defaultValue)

    def _addMissingPreference(self, sectionName: str, preferenceName: str, value: str):
        self._configParser.set(sectionName, preferenceName, value)
        self.saveConfiguration()
