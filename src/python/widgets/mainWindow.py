from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import timedelta, datetime

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QTimer, Qt, Signal

from widgets.addTimer import addTimer
from widgets.options import optionsDock
from widgets.toolbar import toolbar
from widgets.guide import Guide
from widgets.staticTimers import staticTimers
from widgets.central import centralWidget
from constants import MAIN_WINDOW, TimeFormats
from saveConfig import saveConfig, ConfigKeys
from dataParser import dataParser, StopwatchDataKeys

if TYPE_CHECKING:
    import PySide6.QtGui as qtg

class window(qtw.QMainWindow):

    updateTrayMenu = Signal()

    def __init__(self, app: qtw.QApplication):
        super().__init__()

        self.config = saveConfig()

        self.dataParser = dataParser()

        self.app = app

        self.setObjectName(MAIN_WINDOW)

        self.toolBar = toolbar(parent=self)
        self.addToolBar(self.toolBar)

        self.central = centralWidget(self)
        self.setCentralWidget(self.central)

        self.dockWidgetAddTimer = addTimer(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetAddTimer)
        self.dockWidgetAddTimer.setVisible(self.config.getAddtimerStartup())

        self.dockWidgetOptions = optionsDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetOptions)
        self.dockWidgetOptions.setVisible(self.config.getSettingsStartup())

        self.dockWidgetGuide = Guide(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetGuide)
        self.dockWidgetGuide.setVisible(self.config.getGuideStartup())

        self.dockWidgetStaticTimer = staticTimers(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetStaticTimer)
        self.dockWidgetStaticTimer.setVisible(self.config.getStatictimerStartup())

        # So the resize event doesn't spam the save window resolution function (see sizeApplyTimerTimeout() )
        self.windowSizeApplyTimer = QTimer(self)
        self.windowSizeApplyTimer.setObjectName('windowSizeApplyTimer')
        self.windowSizeApplyTimer.timeout.connect(self.sizeApplyTimerTimeout)

        self.resize(self.config.getWidth(), self.config.getHeight())

        self.loadSaveData()

        # Checking to see if the client is the latest version
        self.dockWidgetOptions.checkUpdate()

        self.dockWidgetAddTimer.createStopwatch.connect(lambda a, b, c, d, e: self.central.addStopWatch(a, b, c, d, e))

    def loadSaveData(self):

        for timerID in self.dataParser.sections():

            # Name
            name = self.dataParser[timerID][StopwatchDataKeys.time_object]

            # Changing the timer's destination into a datetime type
            timeFinished = self.dataParser[timerID][StopwatchDataKeys.time_finished]
            timeFinished = datetime.strptime(timeFinished, TimeFormats.Saved_Date)
            timeFinished = timeFinished - datetime.today().replace(microsecond=0)

            # The original duration (For resetting the timer) and changing into a timedelta type
            originalDuration = self.dataParser[timerID][StopwatchDataKeys.time_original_duration].split(':')
            originalDuration = timedelta(hours= int(originalDuration[0]), minutes= int(originalDuration[1]))

            # Border color (In hexcode format)
            borderColor = self.dataParser[timerID][StopwatchDataKeys.border_color]

            # Notes
            notes = self.dataParser[timerID][StopwatchDataKeys.notes]

            # Remove old ID
            self.dataParser.remove_section(timerID)

            # Create stopwatch by calling the central widget's function
            self.central.addStopWatch(name, timeFinished, name, originalDuration, borderColor, notes, save=False)

        # Update the savefile (Old IDs are removed)
        self.dataParser.save()

        # Update the savefile (Saving new IDs created from for loop)
        self.central.saveData()

    def sizeApplyTimerTimeout(self):

        self.windowSizeApplyTimer.stop()

        self.config['WINDOW SIZE'] = {ConfigKeys.width : str(self.width()), ConfigKeys.height : str(self.height())}

        self.config.save()


    def closeEvent(self, a0: qtg.QCloseEvent) -> None:

        if not self.config.getShutdownOnClose():
        # Trigger the "openClose_Pressed" function of the trayMenu (assuming trayMenu is an instance)

            self.updateTrayMenu.emit()

            a0.ignore()
        else:
            # Save data before exiting the application
            self.central.saveData()
            self.app.exit()


    def resizeEvent(self, a0: qtg.QResizeEvent) -> None:

        # Start the window size apply timer if it is not active
        if not self.windowSizeApplyTimer.isActive():
            self.windowSizeApplyTimer.start(1000)
            
        # Call the base class's resizeEvent
        return super().resizeEvent(a0)
