
from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from constants import TOOLBAR
from saveConfig import saveConfig

if TYPE_CHECKING:
    from widgets.mainWindow import window

class toolbar(qtw.QToolBar):
    def __init__(self, parent: window = None):
        super().__init__(parent)

        self.setObjectName(TOOLBAR)

        self.app = qtw.QApplication.instance()
        self.mw: window = parent

        self.config = saveConfig()
        
        # Set floatable and movable to False
        self.setFloatable(False)
        self.setMovable(False)

        self.layout().setSpacing(20)

        # Add Timer Button
        self.addTimerButton = qtg.QAction('Add Timer', self)
        self.addTimerButton.setCheckable(True)
        self.addTimerButton.setChecked(self.config.getAddtimerStartup())
        self.addTimerButton.triggered.connect(lambda: self.button_Clicked(self.mw.dockWidgetAddTimer, self.addTimerButton.isChecked() ) )
        self.addAction(self.addTimerButton)

        # Options Button
        self.optionsButton = qtg.QAction('Options', self)
        self.optionsButton.setCheckable(True)
        self.optionsButton.setChecked(self.config.getSettingsStartup())
        self.optionsButton.triggered.connect(lambda: self.button_Clicked(self.mw.dockWidgetOptions, self.optionsButton.isChecked() ) )
        self.addAction(self.optionsButton)

        # Guide Button
        self.guideButton = qtg.QAction('Guide', self)
        self.guideButton.setCheckable(True)
        self.guideButton.setChecked(self.config.getGuideStartup())
        self.guideButton.triggered.connect(lambda: self.button_Clicked(self.mw.dockWidgetGuide, self.guideButton.isChecked()))
        self.addAction(self.guideButton)

        # Static Timers Button
        self.staticButton = qtg.QAction('Static Timers', self)
        self.staticButton.setCheckable(True)
        self.staticButton.setChecked(self.config.getStatictimerStartup())
        self.staticButton.triggered.connect(lambda: self.button_Clicked(self.mw.dockWidgetStaticTimer, self.staticButton.isChecked()))
        self.addAction(self.staticButton)

    def button_Clicked(self, dockObject: qtw.QDockWidget, buttonisChecked: bool):
        # Find the QDockWidget based on the dockObjectName

        if buttonisChecked:
            # If the button is checked, show the QDockWidget

            dockObject.show()

        else:
            # If the button is not checked, hide the QDockWidget

            dockObject.hide()