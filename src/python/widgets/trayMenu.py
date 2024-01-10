from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from saveConfig import saveConfig

from constants import SYS_TRAY

if TYPE_CHECKING:
    from widgets.mainWindow import window

class trayMen(qtw.QMenu):
    def __init__(self, app: qtw.QApplication, main_window: window):
        super().__init__()

        self.config = saveConfig()
        self.app = app
        self.main_window = main_window

        self.main_window.updateTrayMenu.connect(self.openClose_Pressed)

        self.setObjectName(SYS_TRAY)
        # Determine the label for the open/close button based on a configuration option

        openOrClose = 'Close' if self.config.getStartUp() else 'Open'
        # Create the open/close button QAction and connect it to the openClose_Pressed method

        self.openCloseButton = qtg.QAction(openOrClose)
        self.openCloseButton.triggered.connect(self.openClose_Pressed)
        # Create the quit application button QAction and connect it to the shutdownApp method
        
        self.quitAppButton = qtg.QAction("Shut Down")
        self.quitAppButton.triggered.connect(self.shutdownApp)
        
        # Add the actions (buttons) to the menu
        self.addAction(self.openCloseButton)
        self.addAction(self.quitAppButton)

    def shutdownApp(self):
        # Save data before shutting down the application
        self.config.save()
        self.app.quit()

    def openClose_Pressed(self):

        if self.openCloseButton.text() == 'Close':
            # If the open/close button text is 'Close' Change the button text to 'Open'
            self.openCloseButton.setText('Open')
            # Set the main window (mw) to be invisible
            
            self.main_window.setVisible(False)
        else:
            # If the open/close button text is not 'Close' Change the button text to 'Close'
            self.openCloseButton.setText('Close')
            self.main_window.setVisible(True)
