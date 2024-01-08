from typing import Self
from configparser import ConfigParser
from enum import StrEnum, auto
import random

from constants import CONFIG

# COLOR PALLET CREDITS:
# Dark by archer: https://lospec.com/palette-list/timeless
# Light by wcburgess: https://www.color-hex.com/color-palette/106748
# Hydro by |NOXITIVE|: https://lospec.com/palette-list/pola5
# Dendro by green guy: https://lospec.com/palette-list/slimy-05
# Pyro by NicoFerra: https://lospec.com/palette-list/spanish-sunset
# Cryo by finn: https://lospec.com/palette-list/sadness
# Anemo by Isa: https://lospec.com/palette-list/hypernova-5
# Electro by Interprete-me: https://lospec.com/palette-list/neon-moon-tarot
# Geo by namida: https://lospec.com/palette-list/koukasita

class ColorPallets(StrEnum):
    dark = auto()
    light = auto()
    original = auto()
    hydro = auto()
    dendro = auto()
    pyro = auto()
    cryo = auto()
    anemo = auto()
    electro = auto()
    geo = auto()
    random = auto()

class StyleSheets(StrEnum):
    app = auto()
    stopwatch = auto()

class StyleManager:

    def __init__(self) -> None:

        config = ConfigParser()
        config.read(CONFIG)

        # Attribute Definitions
        # Default color pallet is dark
        self.selectedColorPallet: str = config.get('OPTIONS', 'color pallet', fallback=ColorPallets.dark)

        # COLOR TYPE INDEX (These aren't strict naming conventions there are some exceptions)
        # 0 : Background
        # 1 : Frame Background
        # 2 : Foreground
        # 3 : Text
        # 4 : Alt Text

        self.colorPallets: dict[ColorPallets:tuple[str, str, str, str, str]] = {
            ColorPallets.dark     : ('#212124', '#464c54', '#5b8087', '#76add8', '#a3e7f0'),
            ColorPallets.light    : ('#fafafa', '#e4e5f1', '#d2d3db', '#9394a5', '#484b6a'),
            ColorPallets.original : ('#1A1A1B', '#333F44', '#37AA9C', '#94F3E4', '#FCB3FC'),
            ColorPallets.hydro    : ('#070810', '#18284A', '#52A5DE', '#ACD6F6', '#EBF9FF'),
            ColorPallets.dendro   : ('#0a1a2f', '#04373b', '#1a644e', '#40985e', '#d1cb95'),
            ColorPallets.pyro     : ('#5f2f45', '#a02f40', '#e56f15', '#eda94a', '#f5ddbc'),
            ColorPallets.cryo     : ('#2e364d', '#425d87', '#7d95de', '#ddc8f9', '#fbfef9'),
            ColorPallets.anemo    : ('#2e3b43', '#486970', '#5a9e89', '#9adcae', '#f9fcf1'),
            ColorPallets.electro  : ('#000000', '#5f4886', '#8767bd', '#70b9fb', '#fe0094'),
            ColorPallets.geo      : ('#111111', '#554433', '#aa6622', '#dd9933', '#88aa99'),
        }
           
        self.stopwatchColorsDict: dict[ColorPallets:str] = {
            ColorPallets.random  :'random',
            ColorPallets.cryo    :'#37AA9C',
            ColorPallets.dendro  :'#32B85C',
            ColorPallets.pyro    :'#AB413F',
            ColorPallets.hydro   :'#3F7EAB',
            ColorPallets.geo     :'#F7A936',
            ColorPallets.electro :'#8156E3',
            ColorPallets.anemo   :'#60FD75'
        }
        
        self.stopwatchBorderColor: str = self.stopwatchColorsDict[ColorPallets.anemo]

        self.appStyleSheet: str = '''

            QWidget {{
                background-color: {0};
            }}

            QMainWindow{{
                background-color: {0};
            }}

            QToolBar{{
                background-color: {1};
            }}

            QWidget#centralWidget * {{
                border: none;
            }}

            QDockWidget {{
                color: {3};
                font-size: 15px;
            }}

            QDockWidget::title {{
                background: {1};
            }}

            QToolButton, QPushButton{{
                background-color: {1};
                color: {3};
                font-size: 18px;
            }}

            QToolButton:hover, QPushButton:hover {{
                background-color: {1}
            }}

            QToolButton:pressed, QPushButton:pressed {{
                background-color: {2}
            }}

            QPushButton#applySettingsButton[unsavedChanges="true"]{{
                color: {4};
            }}

            QCheckBox {{
                color: {3};
                font-size: 18px;
            }}

            QCheckBox::indicator{{
                width: 20px;
                height: 20px;
            }}

            QLineEdit{{
                font-size: 20px;
                background-color: {1};
                color: {3};
            }}

            QComboBox {{
                background: {1};
                color: {3};
                font-size: 20px;
                selection-background-color: {0};
                border: none;
            }}

            QListView, QAbstractScrollArea {{
                background-color: {1};
                color: {3};
                border: none;
            }}

            QLabel{{
                color: {3};
                font-size: 18px;
            }}

            QScrollBar:vertical {{
                border: none;
                background-color: {0};
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 0px;
                
            }}

            QScrollBar::handle:vertical {{
                background-color: {2};
                min-height: 30px;
                border-radius: 7px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {2};
            }}

            QScrollBar::handle:vertical:pressed {{
                background-color: {3};
                min-height: 30px;
                border-radius: 7px;
            }}

            QScrollBar::sub-line:vertical {{
                border: none;
                background-color: {1};
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}

            QScrollBar::add-line:vertical {{
                border: none;
                background-color: {1};
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                background: none;
            }}

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

                '''
        self.appStyleSheet_formatted = self.formatStyleSheet(self.appStyleSheet, self.selectedColorPallet)
        
        # The background color of QFrame is changed in `main.py` in `addStopWatch()`
        self.stopwatchStyleSheet: str = '''

            QFrame {{
                border: 3px solid {5};
                border-radius: 10px;
                background-color: {1};
            }}

            QLabel#nameLabel{{
                font-size: 60px;
            }}

            QLabel#CountDownLabel{{
                font-size: 70px;
            }}

            QLabel#CountDownLabel[finished="true"]{{
                color: {4};
                font-size: 70px;
            }}

            QLabel {{
                font-size: 30px;
                color: {3};
                border: none;
                text-align: center;
            }}

            QTextEdit {{
                background-color: {0};
                color: {3};
                font-size: 24px;
                border: none;
            }}

            QPushButton {{
                font-size: 25px;
                background: {0};
            }}

            QPushButton:pressed{{
                background-color: {2};
            }}

            '''
        self.stopwatchStyleSheet_formatted = self.formatStyleSheet(self.stopwatchStyleSheet, self.selectedColorPallet)
    
    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(StyleManager, cls).__new__(cls)

        return cls.instance

    def getStyleSheet(self, styleSheet: StyleSheets) -> str:
        ''' Returns style sheet, see the enum class `StyleSheets` for available style sheets '''

        styleSheets: dict[StyleSheets:str] = {
            StyleSheets.app       : self.appStyleSheet_formatted,
            StyleSheets.stopwatch : self.stopwatchStyleSheet_formatted}

        return styleSheets[styleSheet]
    
    def getColorPallets(self) -> list[str]:
        '''Returns a list of the available color pallets'''
        return list(self.colorPallets.keys())
    
    def getStyleSheetNames(self) -> list[str]:
        '''
        Returns a list of the available color pallets.
        This function exists for naming convention and would be the same as calling `getStyleSheet()` with no parameter
        '''
        return self.getStyleSheet()
    
    def getCurrentColorPallet(self) -> str:
        '''Returns the color pallet being used'''
        return self.selectedColorPallet
    
    def getStopwatchColor(self, color: ColorPallets | str) -> str:
        '''
        Returns the hexcode version of a stopwatch border color example: {color:hexcode}

        If given a regular hexcode return the hexcode
        '''

        hexColor: str | None = self.stopwatchColorsDict.get(color.lower())

        if color == ColorPallets.random:
            return random.choice(list(self.stopwatchColorsDict.values()))
        elif hexColor is not None:
            return hexColor
        else:
            return color.upper()
    
    def getStopwatchColors(self) -> dict[str:str]:
        '''Returns a dictionary of the stopwatch border colors'''
        return self.stopwatchColorsDict
    
    def changeStopwatchBorderColor(self, color: ColorPallets) -> None:
        '''Changes the stopwatch border color'''

        self.stopwatchBorderColor = self.getStopwatchColor(color)
        
        # Reinitializing to update format changes
        self.stopwatchStyleSheet_formatted = self.formatStyleSheet(self.stopwatchStyleSheet, self.selectedColorPallet)
        
    def changeColorPallet(self, pallet: str) -> None:
        '''Updates the color pallet'''

        # Updating the selected color pallet
        self.selectedColorPallet = pallet

        # Updating formatted strings (The Style Sheets)
        self.stopwatchStyleSheet_formatted = self.formatStyleSheet(self.stopwatchStyleSheet, self.selectedColorPallet)
        self.appStyleSheet_formatted = self.formatStyleSheet(self.appStyleSheet, self.selectedColorPallet)


    def formatStyleSheet(self, styleSheet: str, colorPallet: ColorPallets) -> str:
        '''Formats a stylesheet from this class with the specified color pallet'''
        colorPalletValues = self.colorPallets[colorPallet]
        return styleSheet.format(*colorPalletValues, self.stopwatchBorderColor)
