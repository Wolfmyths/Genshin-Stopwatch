from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, timedelta, date

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt, QTimer

from saveConfig import saveConfig, ConfigKeys
from constants import ONE, ZERO, TimeFormats
import notify

if TYPE_CHECKING:
    import PySide6.QtGui as qtg
    from widgets.mainWindow import window

class staticTimers(qtw.QDockWidget):
    def __init__(self, parent: window = None):
        super().__init__(parent)

        self.config = saveConfig()

        self.mw = parent

        self.setWindowTitle('Static Timers')
        self.setObjectName('staticTimersDockWidget')
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(qtw.QDockWidget.DockWidgetFeature.DockWidgetClosable)

        # Checking to see if 'STATIC_TIMERS' is a valid section in config.ini
        try:
            self.config['STATIC_TIMERS'].keys()
        except KeyError:
            self.config.add_section('STATIC_TIMERS')
            self.config.save()

        # Central Frame
        self.centralFrame: qtw.QFrame = qtw.QFrame(self)

        # Form Layout
        formlayout: qtw.QFormLayout = qtw.QFormLayout()
        self.centralFrame.setLayout(formlayout)

        # Daily reset timer
        self.dailyReset = qtw.QLabel(self, text='Loading...')
        self.dailyReset.setObjectName('dailyResetTimer')
        formlayout.addRow(qtw.QLabel(self, text='Daily Reset: '), self.dailyReset)

        # Weekly reset timer
        self.weeklyReset = qtw.QLabel(self, text='Loading...')
        self.weeklyReset.setObjectName('weeklyResetTimer')
        formlayout.addRow(qtw.QLabel(self, text='Weekly Reset: '), self.weeklyReset)

        # Server's UTC offsets
        self.serverTimezones: dict[str:int|float] = {
            'Asia' : 8,
            'EU'   : 1,
            'NA'   : -5
        }

        # Dropdown
        self.chooseServerDropDown = qtw.QComboBox(self)
        self.chooseServerDropDown.addItems(list(self.serverTimezones.keys()))
        self.chooseServerDropDown.setCurrentText(self.config.getServer())
        self.chooseServerDropDown.currentTextChanged.connect(lambda server: self.changeServer(server))
        formlayout.addRow('Server: ', self.chooseServerDropDown)

        self.setWidget(self.centralFrame)

        # Defining variables for timers

        self.dailyQTimer = QTimer(self)
        self.dailyQTimer.timeout.connect(self.dailyResetTimer)
        self.weeklyQTimer = QTimer(self)
        self.weeklyQTimer.timeout.connect(self.weeklyResetTimer)

        self.serverChange = False
        
        # Start Static Timers
        self.staticTimerStart()

    def staticTimerStart(self):

        self.serverChange = False

        # Update perferred server setting
        self.selectedServer: str = self.config.getServer()

        # Define today's date and time
        self.today = datetime.today().replace(microsecond=0)

        ### Daily Timer

        # Calculating the deadline of the daily reset with their choice of server
        self.dailyDeadline = datetime(year=self.today.year, month=self.today.month, day=self.today.day, hour=9) + timedelta(hours=self.serverTimezones[self.selectedServer])

        # If the program starts after the reset time happened, add a day to the deadline 
        if self.dailyDeadline < self.today:

            self.dailyDeadline += timedelta(days=1)
        
        self.config['STATIC_TIMERS'][ConfigKeys.dailydeadline] = datetime.strftime(self.dailyDeadline, TimeFormats.Static_Timer)

        self.difference = self.dailyDeadline - self.today

        ### Weekly Timer

        # Calculating how many days left until Monday
        # date.weekday starts at 0
        dayOfTheWeek = date.weekday(self.today)
        self.weeklyDayDifference: int = 7 - dayOfTheWeek

        # Calculating the deadline of the weekly reset with their choice of server
        # Creating datetime object, hour 9 is the time for UTC+0 for weekly reset
        self.weeklyDeadline = datetime(year=self.today.year, month=self.today.month, day=self.today.day, hour=9)

        # Adding UTC Offset depepending on server selected
        self.weeklyDeadline += timedelta(hours=self.serverTimezones[self.selectedServer])

        # Adding days left until upcoming Sunday
        self.weeklyDeadline += timedelta(days=self.weeklyDayDifference)

        self.config['STATIC_TIMERS'][ConfigKeys.weeklydeadline] = datetime.strftime(self.weeklyDeadline, TimeFormats.Static_Timer)

        self.weeklyDifference = self.weeklyDeadline - self.today
        
        self.config.save()

        self.dailyQTimer.start(1000)
        self.weeklyQTimer.start(1000)

        # Renabling server selection
        self.chooseServerDropDown.setEnabled(True)
        
    
    def dailyResetTimer(self):

        if self.difference > ZERO:

            self.difference -= ONE

            self.dailyReset.setText(str(self.difference))
        
        else:

            self.dailyDeadline += timedelta(days=1)
            self.config['STATIC_TIMERS'][ConfigKeys.dailydeadline] = datetime.strftime(self.weeklyDeadline, TimeFormats.Static_Timer)
            self.config.save()

            self.difference = self.dailyDeadline - datetime.today()

            # 2nd condition is so the daily reset doesn't also go off when the weekly reset notification does
            if self.config.getDailyReset() and not all((self.weeklyDayDifference > ZERO, self.config.getWeeklyReset())):
                notify.Notify('Daily reset', 'The daily reset has been reached!')

    def weeklyResetTimer(self):

        if self.weeklyDifference > ZERO:

            self.weeklyDifference -= ONE

            # Used formatted string because you only need to see the days since `daily reset` tells you the time
            self.weeklyReset.setText(f'{self.weeklyDifference.days} Day(s) left')
        
        else:

            self.weeklyDeadline += timedelta(days=7)
            self.config['STATIC_TIMERS'][ConfigKeys.weeklydeadline] = datetime.strftime(self.weeklyDeadline, TimeFormats.Static_Timer)
            self.config.save()

            self.weeklyDifference = self.weeklyDeadline - datetime.today()

            if self.config.getWeeklyReset():
                notify.Notify('Weekly reset', 'The weekly reset has been reached!')
    
    def changeServer(self, server: str):
        
        # Prevent the selection from being spammed which would break the timers
        self.chooseServerDropDown.setEnabled(False)

        self.config['QOL'][ConfigKeys.gameserver] = server
        self.config.save()

        self.serverChange = True

        self.dailyQTimer.stop()
        self.weeklyQTimer.stop()

        self.staticTimerStart()

    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        # Check if the parent widget is hidden

        if self.mw.isHidden():
            a0.ignore()

        else:

            self.mw.toolBar.staticButton.setChecked(False)
            
            if not self.mw.isMinimized():
                # Update the configuration setting 'settings open on startup' to 'False'
                self.config['QOL'][ConfigKeys.static_timers_open_on_startup] = 'False'
                
                # Save the updated configuration
                self.config.save()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:

        # Set the optionsButton as checked

        self.mw.toolBar.staticButton.setChecked(True)

        # Update the configuration setting 'settings open on startup' to 'True'
        if not self.mw.isMinimized():
            
            self.config['QOL'][ConfigKeys.static_timers_open_on_startup] = 'True'
            self.config.save()
        return super().showEvent(a0)