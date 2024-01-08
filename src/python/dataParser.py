from configparser import ConfigParser
from typing import Self
from enum import StrEnum, auto
import os

from constants import SAVEFILE

class StopwatchDataKeys(StrEnum):
    time_object            = 'name'
    time_finished          = 'time finished'
    time_original_duration = 'time original duration'
    border_color           = 'border color'
    notes                  = auto()

class dataParser(ConfigParser):
    def __init__(self):
        super().__init__()

        # Create save file if it doesn't exist
        if not os.path.exists(SAVEFILE):
            with open(SAVEFILE, 'w+') as f:
                pass


        self.read(SAVEFILE)
    
    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(dataParser, cls).__new__(cls)

        return cls.instance

    def save(self):
        with open(SAVEFILE, 'w') as f:
            self.write(f)
