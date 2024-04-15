from typing import Self
from enum import StrEnum, auto
from datetime import datetime
import os

from configparser import ConfigParser

from constants import CONFIG, TimeFormats
from style import ColorPallets

class ConfigKeys(StrEnum):
    # OPTIONS
    show_on_startup               = 'show on startup'
    dailyresetnotify              = auto()
    weeklyresetnotify             = auto()
    checkversiononstartup         = auto()
    shutdown_app_on_close         = 'shutdown app on close'
    color_pallet                  = 'color pallet'
    desktop_notifications         = 'desktop notifications'

    # QOL
    expedition_checkbox           = auto()
    desiredstamina                = auto()
    addtimer_open_on_startup      = 'addtimer open on startup'
    settings_open_on_startup      = 'settings open on startup'
    static_timers_open_on_startup = 'static timers open on startup'
    gameserver                    = auto()

    # WINDOW SIZE
    width                         = auto()
    height                        = auto()

    # STATIC TIMERS
    dailydeadline                 = auto()
    weeklydeadline                = auto()

class saveConfig(ConfigParser):
    def __init__(self):
        super(saveConfig, self).__init__()

        # If file does not exist then create it
        if not os.path.exists(CONFIG):
            with open(CONFIG, 'w+') as f:
                pass
        
        self.read(CONFIG)

        # Checking if sections exist to prevent traceback if they don't
        for section in ('OPTIONS', 'QOL', 'STATIC_TIMERS', 'WINDOW SIZE'):
            self.__checkSection(section)

        self.save()

    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(saveConfig, cls).__new__(cls)

        return cls.instance
    
    def __checkSection(self, section: str):
        if not self.has_section(section):
            self.add_section(section)
    
    def setOption(self, section: str, option: str, value: str):
        self.__checkSection(section)

        self.set(section, option, value)

    def save(self):
        with open(CONFIG, 'w') as f:
            self.write(f)
    
    def getStartUp(self) -> bool:
        return self.getboolean('OPTIONS', ConfigKeys.show_on_startup, fallback=True)
    
    def getDailyReset(self) -> bool:
        return self.getboolean('OPTIONS', ConfigKeys.dailyresetnotify, fallback=False)
    
    def getWeeklyReset(self) -> bool:
        return self.getboolean('OPTIONS', ConfigKeys.weeklyresetnotify, fallback=False)
    
    def getCurrentPallet(self) -> ColorPallets:
        return ColorPallets(self.get('OPTIONS', ConfigKeys.color_pallet, fallback=ColorPallets.dark))
    
    def getVersionCheck(self) -> bool:
        return self.getboolean('OPTIONS', ConfigKeys.checkversiononstartup, fallback=True)
    
    def getShutdownOnClose(self) -> bool:
        return self.getboolean('OPTIONS', ConfigKeys.shutdown_app_on_close, fallback=False)

    def getDesktopNotifications(self) -> bool:
        return self.getboolean('OPTIONS', ConfigKeys.desktop_notifications, fallback=True)
    
    def getExpeditionCheckbox(self) -> bool:
        return self.getboolean('QOL', ConfigKeys.expedition_checkbox, fallback=True)
    
    def getDesiredStamina(self) -> str:
        return self.get('QOL', ConfigKeys.desiredstamina, fallback='160')
    
    def getAddtimerStartup(self) -> bool:
        return self.getboolean('QOL', ConfigKeys.addtimer_open_on_startup, fallback=True)
    
    def getSettingsStartup(self) -> bool:
        return self.getboolean('QOL', ConfigKeys.settings_open_on_startup, fallback=False)

    def getStatictimerStartup(self) -> bool:
        return self.getboolean('QOL', ConfigKeys.static_timers_open_on_startup, fallback=False)
    
    def getServer(self) -> str:
        return self.get('QOL', ConfigKeys.gameserver, fallback='NA')
    
    def getWidth(self) -> int:
        return self.getint('WINDOW SIZE', ConfigKeys.width, fallback=1300)
    
    def getHeight(self) -> int:
        return self.getint('WINDOW SIZE', ConfigKeys.height, fallback=1080)
    
    def getDailyDeadline(self) -> datetime:
        try:
            return datetime.strptime(self.get('STATIC_TIMERS', ConfigKeys.dailydeadline), TimeFormats.Static_Timer)
        except:
            return datetime(0,0,0)
    
    def getWeeklyDeadline(self) -> datetime:
        try:
            return datetime.strptime(self.get('STATIC_TIMERS', ConfigKeys.weeklydeadline), TimeFormats.Static_Timer)
        except:
            return datetime(0,0,0)
