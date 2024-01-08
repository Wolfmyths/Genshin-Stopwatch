from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import timedelta

from PySide6 import QtWidgets as qtw
from PySide6.QtCore import Qt

from saveConfig import saveConfig
from dataParser import dataParser, StopwatchDataKeys
from style import StyleManager
from widgets.stopwatch import Stopwatch, Property

if TYPE_CHECKING:
    from widgets.mainWindow import window

class centralWidget(qtw.QWidget):
    def __init__(self, parent: window = None):
        super().__init__(parent)
        # Create the layout for the central widget

        self.styles = StyleManager()

        self.dataParser = dataParser()

        self.config = saveConfig()

        self.setObjectName('centralWidget')
        self.scrollAreaLayout = qtw.QHBoxLayout(self)
        self.scrollAreaLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout = qtw.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        # Create the scroll area

        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setContentsMargins(0,0,0,0)
        # Create the widget to hold the scroll area contents

        self.scrollAreaWidgetContents = qtw.QWidget()
        self.scrollAreaWidgetContents.setContentsMargins(5,5,5,5)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)
        # Set the scroll area widget

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.addWidget(self.scrollArea)

    def addStopWatch(self, timeObject: str, duration: timedelta, name: str, startDuration: timedelta, color: str, notepadContents: str = '', save: bool = True) -> None:
        # Create a Stopwatch object
        stopwatch = Stopwatch(timeObject, duration, name, startDuration, color, notepadContents, central=self)

        # Add stopwatch to central widget layout
        self.verticalLayout.addWidget(stopwatch)
        
        # Connect events
        stopwatch.destroyed.connect(lambda: self.removeStopwatch(stopwatch))
        stopwatch.save.connect(self.saveData)

        # Make stopwatch visible
        stopwatch.show()

        if save:
            self.saveData()
    
    def removeStopwatch(self, stopwatch: Stopwatch) -> None:
        '''Removes stopwatch from save file'''

        self.dataParser.remove_section(stopwatch.id_)
        self.saveData()

    def saveData(self):

        stopwatch: Stopwatch
        for stopwatch in self.findChildren(Stopwatch):

            objectName: str = stopwatch.objectName()
            nameLabel: qtw.QLabel = stopwatch.findChild(qtw.QLabel, "nameLabel")
            notepad: qtw.QTextEdit = stopwatch.findChild(qtw.QTextEdit)

            stopwatchData = {
                StopwatchDataKeys.time_object            : nameLabel.text(),
                StopwatchDataKeys.time_finished          : stopwatch.property(Property.FinishedTime),
                StopwatchDataKeys.time_original_duration : stopwatch.property(Property.OriginalDuration),
                StopwatchDataKeys.border_color           : stopwatch.property(Property.BorderColor),
                StopwatchDataKeys.notes                  : notepad.toPlainText()
            }

            if not self.dataParser.has_section(objectName):
                self.dataParser.add_section(objectName)

            for key, value in stopwatchData.items():
                self.dataParser.set(objectName, key, value)

        self.dataParser.save()
