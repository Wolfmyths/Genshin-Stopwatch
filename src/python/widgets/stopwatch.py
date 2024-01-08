from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import timedelta, datetime
from enum import StrEnum

from PySide6 import QtWidgets as qtw
from PySide6.QtCore import QTimer, Signal

from constants import ZERO, ONE, TimeFormats
from style import StyleSheets
import notify

if TYPE_CHECKING:
    from widgets.central import centralWidget

class Property(StrEnum):
    '''Property Names for Stopwatch QObject'''
    BorderColor = 'border-color'
    OriginalDuration = 'originalDuration'
    FinishedTime = 'finishedTime'

class Stopwatch(qtw.QFrame):

    save = Signal()

    def __init__(self, timeObject: str, duration: timedelta, name: str, startDuration: timedelta, color: str, notepadContents: str = '', central: centralWidget = None) -> None:
        super().__init__()

        self.timeObject = timeObject
        self.duration = duration
        self.name = name
        self.startDuration = startDuration
        self.color = color
        self.notepadContents = notepadContents

        self.central = central
        self.setParent(self.central.scrollAreaWidgetContents)

        # Set the object name of the frame using its ID
        self.id_ = str(id(self))

        self.central.styles.changeStopwatchBorderColor(color)
        color = self.central.styles.getStopwatchColor(color)

        self.setStyleSheet(self.central.styles.getStyleSheet(StyleSheets.stopwatch))

        self.setObjectName(self.id_)
        #self.setMaximumHeight(500)

        frameLayout = qtw.QVBoxLayout()
        frameLayout.setContentsMargins(15,15,15,15)
        frameLayout.setSpacing(10)
        # Create a QLabel for the name

        nameLabel = qtw.QLabel(name, self)
        nameLabel.setObjectName('nameLabel')

        # Create a delete button

        deleteButton = qtw.QPushButton('Delete', self)
        deleteButton.setMinimumHeight(60)
        deleteButton.clicked.connect(self.deleteLater)
        # Create a QLabel for the countdown time

        self.countDown = qtw.QLabel('00:00:00', self)
        self.countDown.setObjectName('CountDownLabel')
        # Create a reset button

        resetButton = qtw.QPushButton('Reset', self)
        resetButton.setObjectName('resetButton')
        resetButton.setMinimumHeight(60)
        resetButton.clicked.connect(self.restartTimer)
        
        # Create a QLabel for the finished date
        finishedDate = datetime.now() + duration
        self.finishedDateLabel = qtw.QLabel(f'{finishedDate.strftime(TimeFormats.Finished_Date)}')
        self.finishedDateLabel.setObjectName('finishedDateLabel')
        
        # Create a QTextEdit for notes
        notepad = qtw.QTextEdit(self)
        notepad.setPlaceholderText('Notes:')
        notepad.setMaximumHeight(200)
        notepad.setText(notepadContents)

        # Add widgets to layout
        for widget in (nameLabel,
                       self.countDown,
                       self.finishedDateLabel,
                       notepad,
                       resetButton,
                       deleteButton):
            frameLayout.addWidget(widget)
        
        # Set the layout for the frame
        self.setLayout(frameLayout)

        # Finished/Difference time calculations
        currentTime = datetime.today()

        finishedTime = currentTime + duration

        # Calculate the days, hours, minutes from time delta object for original duration property
        startDurationTotalSeconds = startDuration.total_seconds()
        startDurationHours, remainder = divmod(startDurationTotalSeconds, 3600)
        startDurationMinutes, seconds = divmod(remainder, 60)

        # Setting properties for save manager
        # Original duration property of the frame
        self.setProperty(Property.OriginalDuration, '{:02}:{:02}:{:02}'.format(int(startDurationHours), int(startDurationMinutes), int(seconds)))
        # Time until the stopwatch is finished
        self.setProperty(Property.FinishedTime, datetime.strftime(finishedTime, TimeFormats.Saved_Date))
        # Set the border color property
        self.setProperty(Property.BorderColor, color)

        self.difference = finishedTime - currentTime

        self.QTimer = QTimer()
        self.QTimer.timeout.connect(self.countDownTimer)

        # Setting the text to the difference so when a timer starts its not starting at 00:00:00 unless that's actually the case
        if self.difference > ZERO:
            self.countDown.setText(str(self.difference))

            # Begin timer
            self.QTimer.start(1000)
    
    def restartTimer(self) -> None:
        self.QTimer.stop()

        today = datetime.today()
        finishedTime = today + self.startDuration
        self.difference =  finishedTime - today

        self.countDown.setText(str(self.difference))
        self.finishedDateLabel.setText(f'{finishedTime.strftime(TimeFormats.Finished_Date)}')

        self.setProperty(Property.FinishedTime, datetime.strftime(finishedTime, TimeFormats.Saved_Date))

        self.QTimer.start(1000)

    def countDownTimer(self) -> None:

        self.difference -= ONE

        if self.difference > ZERO:
            
            # Update the countdown label with the new difference
            self.countDown.setText(str(self.difference))

        else:
            self.QTimer.stop()
            self.countDown.setText('00:00:00')
            self.countDown.setProperty('finished', "true")
            self.style().polish(self.countDown)
                
            notify.Notify('Stopwatch finished', f'{self.timeObject} has finished!')
