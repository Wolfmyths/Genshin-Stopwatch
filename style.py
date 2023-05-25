from configparser import ConfigParser
import os


class StyleManager:

    def __init__(self) -> None:

        config = ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
        

        # Attribute Definitions
        # Default color pallet is dark
        self.selectedColorPallet: str = config.get('OPTIONS', 'color pallet', fallback='dark')

        # COLOR TYPE INDEX (These aren't strict naming conventions there are some exceptions)
        # 0 : Background
        # 1 : Frame Background
        # 2 : Foreground
        # 3 : Text
        # 4 : Alt Text

        self.colorPallets: dict[str:list[str]] = {
            'dark' : ('#1A1A1B', '#333F44', '#37AA9C', '#94F3E4', '#FCB3FC'),
            'light': ('#FAFAFA', '#E4E5F1', '#D2D3DB', '#9394A5', '#484B6A')
        }

        self.appStyleSheet: str = '''

            QMainWindow{{
                background-color: {0};
            }}

            QToolBar{{
                background-color: {1};
            }}

            QWidget#centralWidget * {{
                background-color: {0};
                border: none;
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

            QCheckBox::indictator{{
                width: 40px;
                length: 40px;
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
                background-color: #333F44;
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
        self.appStyleSheet_formatted: str = self.appStyleSheet.format(self.colorPallets[self.selectedColorPallet][0], self.colorPallets[self.selectedColorPallet][1], self.colorPallets[self.selectedColorPallet][2], self.colorPallets[self.selectedColorPallet][3], self.colorPallets[self.selectedColorPallet][4])
        
        
        self.stopwatchColorsDict: dict[str:str] = {

            'cryo'   :'#37AA9C',
            'dendro' :'#32B85C',
            'fire'   :'#AB413F',
            'water'  :'#3F7EAB',
            'geo'    :'#F7A936',
            'electro':'#8156E3',
            'anemo'  :'#60FD75'

            }
        
        self.stopwatchBorderColor: str = self.stopwatchColorsDict['anemo']
        
        # The background color of QFrame is changed in `main.py` in `addStopWatch()`
        self.stopwatchStyleSheet: str = '''

                QFrame {{
                    border: 3px solid {5};
                    border-radius: 10px;
                    background-color: {1};
                }}

                QLabel {{
                    font-size: 30px;
                    color: {3};
                    border: none;
                    text-align: center;
                }}

                QTextEdit {{
                    background-color: {0};
                    color: #94F3E4;
                    font-size: 24px;
                    border: none;
                }}   

                QPushButton:pressed{{
                    background-color: {2};
                }}

                

            '''
        self.stopwatchStyleSheet_formatted: str = self.stopwatchStyleSheet.format(self.colorPallets[self.selectedColorPallet][0], self.colorPallets[self.selectedColorPallet][1], self.colorPallets[self.selectedColorPallet][2], self.colorPallets[self.selectedColorPallet][3], self.colorPallets[self.selectedColorPallet][4], self.stopwatchBorderColor)
    
    
    def getStyleSheet(self, styleSheet: str) -> str:
        '''Returns stylesheet specified, to see stylesheet options, run `getStyleSheetNames()`'''
        styleSheets: dict[str:str] = {'app' : self.appStyleSheet_formatted, 'stopwatch': self.stopwatchStyleSheet_formatted}
        return styleSheets[styleSheet]
    
    def getColorPallets(self) -> list[str]:
        '''Returns a list of the available color pallets'''
        return list(self.colorPallets.keys())
    
    def getStyleSheetNames(self) -> list[str]:
        '''Returns a list of stylesheet names'''
        return list(x for x in self.styleSheets.keys())
    
    def getCurrentColorPallet(self) -> str:
        '''Returns the color pallet being used'''
        return self.selectedColorPallet
    
    def getStopwatchColor(self, color: str) -> str:
        '''Returns the hexcode version of a stopwatch border color example: {color:hexcode}'''
        try:
            return self.stopwatchColorsDict[color.lower()]
        except KeyError:
            return color.upper()
    
    def getStopwatchColors(self) -> dict[str:str]:
        '''Returns a dictionary of the stopwatch border colors'''
        return self.stopwatchColorsDict
    
    def changeStopwatchBorderColor(self, color: str) -> None:
        '''Changes the stopwatch border color'''

        self.stopwatchBorderColor = self.getStopwatchColor(color)
        
        # Reinitializing to update format changes
        self.stopwatchStyleSheet_formatted = self.stopwatchStyleSheet.format(self.colorPallets[self.selectedColorPallet][0], self.colorPallets[self.selectedColorPallet][1], self.colorPallets[self.selectedColorPallet][2], self.colorPallets[self.selectedColorPallet][3], self.colorPallets[self.selectedColorPallet][4], self.stopwatchBorderColor)
        
    
    def changeColorPallet(self, pallet: str) -> None:
        '''Updates the color pallet'''
        self.selectedColorPallet = pallet

        self.stopwatchStyleSheet_formatted = self.stopwatchStyleSheet.format(self.colorPallets[self.selectedColorPallet][0], self.colorPallets[self.selectedColorPallet][1], self.colorPallets[self.selectedColorPallet][2], self.colorPallets[self.selectedColorPallet][3], self.colorPallets[self.selectedColorPallet][4], self.stopwatchBorderColor)
        self.appStyleSheet_formatted = self.appStyleSheet.format(self.colorPallets[self.selectedColorPallet][0], self.colorPallets[self.selectedColorPallet][1], self.colorPallets[self.selectedColorPallet][2], self.colorPallets[self.selectedColorPallet][3], self.colorPallets[self.selectedColorPallet][4])

