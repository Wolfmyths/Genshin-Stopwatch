# This requires some futher cleanup

class StyleManager:
    def __init__(self):
        self.globalStyles: list[str] = []
        self.localStyles: dict[str, list[str]] = {}

    # Appends a style to the global styles
    def appendGlobalStyle(self, style: str | list[str]) -> None:
        self.globalStyles.append(style)

    # Appends a style to local style at key
    def appendLocalStyle(self, key: str, style: str | list[str]) -> None:
        try:
            self.localStyles[key].append(style)
        except KeyError:
            self.localStyles[key] = [style]

    # Joins all global styles into a string
    def getGlobalStyleString(self) -> str:
        return '\n'.join(self.globalStyles)
    
    # Joins all local styles at key into a string
    def getLocalStyleString(self, key: str) -> str:
        return '\n'.join(self.localStyles[key])
    
    # Mixes global styles with styles at key
    def mixGlobal(self, key: str) -> str:
        return self.getGlobalStyleString() + self.getLocalStyleString(key)
    
    # Mixes local styles at each key in keys into a string
    def mixLocal(self, keys: list[str]) -> str:
        style = ""
        for key in keys:
            style += self.getLocalStyleString(key)
        return style
    
# Style Defintions

# Global Styles #
label: str = '''
    QLabel, QPushButton{
        font-size: 18px;
    }
'''

checkbox: str = '''
    QCheckBox::indictator{
        width: 40px;
        length: 40px;
    }
'''

toolButton: str = '''
    QToolButton{
        font-size: 18px;
    }
'''

# Local Styles #
window: str = '''
    QMainWindow{
        background-color: #1A1A1B;
    }

    QToolBar{
        background-color: #333F44;
    }

    QToolButton, QPushButton{
        background-color: #333F44;
        color: #94F3E4;
        font-size: 15px;
    }

    QToolButton:hover, QPushButton:hover {
        background-color: #333F44
    }

    QToolButton:pressed, QPushButton:pressed {
        background-color: #37AA9C
    }

    QLineEdit{
        font-size: 20px;
        background-color: #333F44;
        color: #94F3E4;
    }

    QComboBox{
        background: #333F44;
        color: #94F3E4;
        font-size: 20px;
    }

    QListView{
        background-color: #333F44;
        color: #94F3E4;
    }

    QComboBox QAbstractItemView {
        selection-background-color: #1A1A1B;
        border: none;
    }

    QLabel{
        color: #94F3E4;
    }
'''

centralWidget: str = '''
    QWidget{
        background-color: #1A1A1B;
        border: none;
    }

    QScrollBar:vertical {
        border: none;
        background-color: #1A1A1B;
        width: 14px;
        margin: 15px 0 15px 0;
        border-radius: 0px;
        
    }

    QScrollBar::handle:vertical {
        background-color: #37AA9C;
        min-height: 30px;
        border-radius: 7px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #37AA9C;
    }

    QScrollBar::handle:vertical:pressed {
        background-color: #94F3E4;
        min-height: 30px;
        border-radius: 7px;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background-color: #333F44;
        height: 15px;
        border-top-left-radius: 7px;
        border-top-right-radius: 7px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical {
        border: none;
        background-color: #333F44;
        height: 15px;
        border-bottom-left-radius: 7px;
        border-bottom-right-radius: 7px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
'''

stopwatch: str = '''
    QLabel {{
        font-size: 30px;
        color: #94F3E4;
        border: none;
        text-align: center;
    }}

    QLabel[finished="true"]{{
        color: #FCB3FC;
    }}

    QPushButton:pressed{{
        background-color: #37AA9C;
    }}
'''