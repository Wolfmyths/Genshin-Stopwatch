from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

from saveConfig import saveConfig, ConfigKeys
from constants import GUIDE

if TYPE_CHECKING:
    from widgets.mainWindow import window
    import PySide6.QtGui as qtg

class Guide(qtw.QDockWidget):
    def __init__(self, parent: window = None):
        super().__init__(parent)

        self.app = qtw.QApplication.instance()

        self.mw: window = parent

        self.config = saveConfig()

        self.setWindowTitle('Guide')
        self.setObjectName('guideDockWidget')
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(qtw.QDockWidget.DockWidgetFeature.DockWidgetClosable)

        # Central Frame
        self.centralFrame: qtw.QFrame = qtw.QFrame(self)

        # Vertical Box Layout
        verticalLayout: qtw.QVBoxLayout = qtw.QVBoxLayout()
        self.centralFrame.setLayout(verticalLayout)

        self.textFile: qtw.QTextBrowser = qtw.QTextBrowser(self.centralFrame)
        self.textFile.setReadOnly(True)
        self.textFile.setOpenExternalLinks(True)

        # Reading html guide
        # The guide is packaged into the .exe so it is always updated
        try: 

            with open(GUIDE, 'r') as html:

                self.textFile.setHtml(html.read())

        except Exception as e:
            print(e)

            self.textFile.setHtml(
                f'''
                <h1>Error. Could not find Guide:</h1>
                <br><br>
                {e}
                ''')
        
        verticalLayout.addWidget(self.textFile)

        self.setWidget(self.centralFrame)
    
    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        # Check if the parent widget is hidden
        
        if self.mw.isHidden():
            a0.ignore()

        else:
            
            # Uncheck the guideButton

            self.mw.toolBar.guideButton.setChecked(False)

            if not self.mw.isMinimized():

                self.config['QOL'][ConfigKeys.guide_open_on_startup] = 'False'
                self.config.save()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:

        # Check the guideButton

        self.mw.toolBar.guideButton.setChecked(True)

        # Check if the parent widget is minimized
        if not self.mw.isMinimized():

            self.config['QOL'][ConfigKeys.guide_open_on_startup] = 'True'

            self.config.save()
        # Call the base class's showEvent method
        
        return super().showEvent(a0)