from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import timedelta

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt, Signal

from saveConfig import saveConfig, ConfigKeys
from style import StyleManager, ColorPallets

if TYPE_CHECKING:
    from widgets.mainWindow import window
    import PySide6.QtGui as qtg

class addTimer(qtw.QDockWidget):
    createStopwatch = Signal(str, timedelta, str, timedelta, str)

    # Realm Currency Level (Hidden by default, see show/hide events)
    # {Trust Rank : Realm Currency Storage Limit}
    REALM_CURRENCY_MAX_STORAGE_VALUES = {
        '1'  : 300,
        '2'  : 300,
        '3'  : 900,
        '4'  : 1200,
        '5'  : 1400,
        '6'  : 1600,
        '7'  : 1800,
        '8'  : 2000,
        '9'  : 2200,
        '10' : 2400
    }

    # Topic data
    TOPIC_SELECTION = {

        '': {
            'durations': ('Nothing Selected', )
        },

        'Stamina': {
            'durations': 'Stamina'
        },

        'Parametric Transformer': {
            'durations': ('7 Days', )
        },

        'Respawns': {
            'durations': ('12 Hours', '1 Day', '2 Days', '3 Days')
        },

        'Expedition': {
            'durations': ('4 Hours', '8 Hours', '12 Hours', '20 Hours')
        },

        'Teapot Gardening/Construction': {
            'durations': ('12 Hours', '14 Hours', '16 Hours', '70 Hours')
        },

        'Realm Currency': {
            'durations': ('Bare-Bones', 'Humble Abode', 'Cozy', 'Queen-Size', 'Elegant', 'Exquisite', 'Extradordinary', 'Stately', 'Luxury', 'Fit for a king')
        },

        'Realm Companionship XP': {
            'durations' : ('0 - 2999 (2/hr)', '3000 - 5999 (3/hr)', '6000 - 11999 (4/hr)', '12000+ (5/hr)')
        },

        'Fishing': {
            'durations': ('1 Day', '3 Days')
        },

        'Custom': {
            'durations': 'Custom'
        }
    }

    # Values for when the player has characters that have a 25% time discount
    # {'4 Hours': 3}
    EXPEDITION_DISCOUNT = {k:v for (k,v) in zip(TOPIC_SELECTION['Expedition']['durations'], ('3 Hours', '6 Hours', '9 Hours', '15 Hours'))}

    # Dict of Realm Statuses and their corresponding income rates
    # {status:rate/hr}
    REALM_CURRENCY_RATES = {k:v for (k,v) in zip(TOPIC_SELECTION['Realm Currency']['durations'], (4, 8, 12, 16, 20, 22, 24, 26, 28, 30))}

    # Dict of Adeptal Energy thresholds and their corresponding income rates for companionship XP
    # {adeptal energy range:rate/hr}
    REALM_FRIENDSHIP_POINT_RATES = {k:v for (k,v) in zip(TOPIC_SELECTION['Realm Companionship XP']['durations'], range(2, 6)) }

    def __init__(self, parent: window):
        super().__init__(parent)

        self.config = saveConfig()
        self.styles = StyleManager()

        self.mw: window = parent

        self.setWindowTitle('Add Timer')
        self.setObjectName('addTimerDockWidget')
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(qtw.QDockWidget.DockWidgetFeature.DockWidgetClosable)

        # Central Frame
        self.centralFrame = qtw.QFrame(self)

        # Vertical Box Layout
        verticalLayout = qtw.QVBoxLayout()
        self.centralFrame.setLayout(verticalLayout)

        # Topic Frame
        self.topicFrame = qtw.QFrame(self.centralFrame)
        verticalLayout.addWidget(self.topicFrame)

        # Form Layout (For Topic Frame)
        self.formLayout = qtw.QFormLayout()
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)
        self.topicFrame.setLayout(self.formLayout)

        # Topic Selection Row
        self.topicLabel = qtw.QLabel('Timed Object:')
        self.topicDropDown = qtw.QComboBox()
        self.topicDropDown.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.topicDropDown.addItems( [x for x in self.TOPIC_SELECTION.keys()] )
        self.topicDropDown.currentTextChanged.connect(lambda topic : self.dropDownSelected(topic))

        self.formLayout.addRow(self.topicLabel, self.topicDropDown)

        # Duration Row
        self.durationLabel = qtw.QLabel('Duration:')
        self.durationDropDown = qtw.QComboBox()
        self.durationDropDown.addItem(self.TOPIC_SELECTION['']['durations'][0])
        self.durationDropDown.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.formLayout.addRow(self.durationLabel, self.durationDropDown)

        self.expeditionLabel = qtw.QLabel('Using a 25% Time Reduction Character')
        self.expeditionCheckBox = qtw.QCheckBox()
        self.expeditionCheckBox.setChecked(self.config.getExpeditionCheckbox())

        self.formLayout.addRow(self.expeditionLabel, self.expeditionCheckBox)

        # Line edit w/ label (Hidden by default, see show/hide events)

        self.lineEditLabel1 = qtw.QLabel()
        self.lineEditLabel1.setObjectName('lineEditLabel1')
        self.lineEdit1 = qtw.QLineEdit()
        self.lineEdit1.setObjectName('lineEdit1')

        self.formLayout.addRow(self.lineEditLabel1, self.lineEdit1)

        # Line edit w/ label (Hidden by default, see show/hide events)

        self.lineEditLabel2 = qtw.QLabel()
        self.lineEditLabel2.setObjectName('lineEditLabel2')
        self.lineEdit2 = qtw.QLineEdit()
        self.lineEdit2.setObjectName('lineEdit2')

        self.formLayout.addRow(self.lineEditLabel2, self.lineEdit2)

        # Line edit w/ label (Hidden by default, see show/hide events)

        self.lineEditLabel3 = qtw.QLabel()
        self.lineEditLabel3.setObjectName('lineEditLabel3')
        self.lineEdit3 = qtw.QLineEdit()
        self.lineEdit3.setObjectName('lineEdit3')

        self.formLayout.addRow(self.lineEditLabel3, self.lineEdit3)

        # Name Row
        self.nameLabel = qtw.QLabel('Name:')
        self.nameLineEdit = qtw.QLineEdit()
        self.nameLineEdit.setPlaceholderText('Optional')

        self.formLayout.addRow(self.nameLabel, self.nameLineEdit)

        self.colorsDict: list[str] = list(self.styles.getStopwatchColors().keys())

        # Color Row
        self.outlineColorLabel = qtw.QLabel('Border Color:')
        self.outlineColorDropDown = qtw.QComboBox()
        self.outlineColorDropDown.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.outlineColorDropDown.addItems([x.title() for x in self.colorsDict])

        self.formLayout.addRow(self.outlineColorLabel, self.outlineColorDropDown)

        # Button
        self.startTimerButton = qtw.QPushButton('Start Timer')
        self.startTimerButton.clicked.connect(self.startStopWatch)
        verticalLayout.addWidget(self.startTimerButton, alignment=Qt.AlignmentFlag.AlignTop)

        self.setWidget(self.centralFrame)

    def hideAll(self):
        for widget in (self.lineEdit1, 
                       self.lineEdit2, 
                       self.lineEdit3, 
                       self.lineEditLabel1, 
                       self.lineEditLabel2, 
                       self.lineEditLabel3, 
                       self.durationDropDown, 
                       self.durationLabel,
                       self.expeditionCheckBox,
                       self.expeditionLabel):

            widget.hide()

    def showRealmCurrency(self):
    # Show realm currency elements

        self.lineEditLabel1.show()
        self.lineEdit1.show()

    def showCustom(self):
    # Show custom elements

        self.lineEditLabel1.show()
        self.lineEdit1.show()

        self.lineEditLabel2.show()
        self.lineEdit2.show()

        self.lineEditLabel3.show()
        self.lineEdit3.show()

    def showNormalDurations(self):

        self.durationLabel.show()
        self.durationDropDown.show()
    
    def showExpedition(self):

        self.durationLabel.show()
        self.durationDropDown.show()

        self.expeditionLabel.show()
        self.expeditionCheckBox.show()

    def dropDownSelected(self, topic: str):
        selectedTopic = self.TOPIC_SELECTION[topic]['durations']

        self.durationDropDown.clear()

        #Hiding all elements
        self.hideAll()

        # Clearning line edits to prevent text from carrying over
        self.lineEdit1.clear(), self.lineEdit2.clear(), self.lineEdit3.clear()

        match topic:

            case 'Expedition':

                self.showExpedition()
                self.durationDropDown.addItems(selectedTopic)

            case 'Realm Currency':

                self.showNormalDurations()
                self.durationLabel.setText('Realm Status:')
                self.durationDropDown.addItems(selectedTopic)

                self.showRealmCurrency()
                self.lineEditLabel1.setText('Realm Trust Level (1-10)')

            case 'Realm Companionship XP':

                self.showNormalDurations()
                self.durationLabel.setText('Adeptal Energy:')
                self.durationDropDown.addItems(selectedTopic)

                self.showRealmCurrency()
                self.lineEditLabel1.setText('Realm Trust Level (1-10)')

            case 'Stamina':

                self.lineEditLabel1.setText('Current Stamina (Max 160)')
                self.lineEditLabel1.show()
                self.lineEdit1.show()

                self.lineEditLabel2.setText('Desired stamina (Max 160)')
                self.lineEditLabel2.show()
                self.lineEdit2.setText(self.config.getDesiredStamina())
                self.lineEdit2.show()

            case 'Custom':

                self.showCustom()
                self.lineEditLabel1.setText('Days:')
                self.lineEditLabel2.setText('Hours:')
                self.lineEditLabel3.setText('Minutes:')

            case _:

                self.durationLabel.setText('Duration:')

                if self.durationLabel.isHidden():

                    self.showNormalDurations()

                self.durationDropDown.addItems(selectedTopic)

    def calculateExpedition(self) -> timedelta:
        duration: str = self.durationDropDown.currentText()

        # If discount is checked, use the expedition discount dict instead
        hours = duration if not self.expeditionCheckBox.isChecked() else self.EXPEDITION_DISCOUNT[duration]

        hours = int(hours.split()[0])

        return timedelta(hours=hours)

    def calculateRealmCurrency(self) -> timedelta:
        # Rerieve maximum storage and rate values
        maxStorage: int = self.REALM_CURRENCY_MAX_STORAGE_VALUES[self.lineEdit1.text()]

        rate = self.durationDropDown.currentText()
        rate = self.REALM_CURRENCY_RATES[rate]

        duration = round(maxStorage / rate, 2)

        return timedelta(hours=duration)
    
    def calculateFriendShipPoints(self) -> timedelta:
        # Rerieve maximum storage and rate values

        maxStorage = int(self.lineEdit1.text()) * 50

        rate = self.durationDropDown.currentText()
        rate = self.REALM_FRIENDSHIP_POINT_RATES[rate]

        duration = round(maxStorage / rate, 2)

        return timedelta(hours=duration)

    def calculateCustom(self) -> timedelta:
        # Retrieve input values for days, hours, and minutes
        days: str|int = self.lineEdit1.text() if self.lineEdit1.text().isdigit() else 0
        hours: str|int = self.lineEdit2.text() if self.lineEdit2.text().isdigit() else 0
        minutes: str|int = self.lineEdit3.text() if self.lineEdit3.text().isdigit() else 0

        # Convert values to positive integers
        days = abs(int(days))
        hours = abs(int(hours))
        minutes = abs(int(minutes))

        return timedelta(days=days, hours=hours, minutes=minutes)

    def calculateStamina(self) -> timedelta:
        # Get inputs
        amountOfStamina: str = self.lineEdit1.text()
        desiredStamina: str = self.lineEdit2.text()

        # Program remembers how much stamina the user wants
        self.config['QOL'][ConfigKeys.desiredstamina] = desiredStamina
        self.config.save()

        # Example: (160 - 20 = 140), user needs 140 stamina until 160, stamina takes 8 minutes to regen 1 stamina
        minutes = (int(desiredStamina) - int(amountOfStamina)) * 8

        return timedelta(minutes=minutes)

    def calculateDefault(self) -> timedelta:
        duration: str = self.durationDropDown.currentText()

        duration = duration.split()

        if duration[1] == 'Days' or duration[1] == 'Day':
            duration = int(duration[0]) * 24
        else:
            duration = int(duration[0])

        hours = duration

        return timedelta(hours=hours)

    def startStopWatch(self):
        '''
        Fired when the addTimer button is pressed.
        This gathers then transforms the current data suitable for the stopwatch's 
        parameters and fires the createStopwatch event
        '''

        # Get the selected time object and outline color        
        timeObject = self.topicDropDown.currentText()

        # self.colorsDict is excluding index 0 because that would be the 'random' key value in the dict
        color: str = self.styles.getStopwatchColor(ColorPallets(self.outlineColorDropDown.currentText().lower()))

        # Create a timedelta object with the calculated duration from the matched selected time object
        match timeObject:

            case 'Expedition':
                duration = self.calculateExpedition()

            case 'Realm Currency':
                # Check if the input is in the valid range
                maxStorage = int(self.lineEdit1.text())
                if maxStorage < 1 or maxStorage > 10:
                    return self.lineEdit1.setText('Error: Invalid Input')

                duration = self.calculateRealmCurrency()

            case 'Realm Companionship XP':
                # Check if the input is in the valid range
                maxStorage = int(self.lineEdit1.text())
                if maxStorage < 1 or maxStorage > 10:
                    return self.lineEdit1.setText('Error: Invalid Input')

                duration = self.calculateFriendShipPoints()

            case 'Custom':
                duration = self.calculateCustom()

            case 'Stamina':

                # Get inputs
                amountOfStamina: str = self.lineEdit1.text()
                desiredStamina: str = self.lineEdit2.text()

                # Checking for valid inputs
                if amountOfStamina.isdigit() == False or int(amountOfStamina) > 160 or int(amountOfStamina) < 0:
                    return self.lineEdit1.setText('Error: Invalid Input')

                elif desiredStamina.isdigit() == False or int(desiredStamina) > 160 or int(desiredStamina) < 0:
                    return self.lineEdit2.setText('Error: Invalid Input')

                duration = self.calculateStamina()

            # Case: default
            case _:

                # Check if no duration is selected
                if not self.topicDropDown.currentText():
                    return

                duration = self.calculateDefault()

        duration += timedelta(days=0, hours=0, minutes=0, seconds=0, microseconds=0, milliseconds=0)

        # Get the text from the nameLineEdit and use it as the name if it is not empty, otherwise use timeObject
        nameText = self.nameLineEdit.text()
        name = nameText if len(nameText) > 0 else timeObject

        # Call the createStopWatch event with the relevant parameters
        self.createStopwatch.emit(timeObject, duration, name, duration, color)

    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        # Check if the parent widget is hidden
        
        if self.mw.isHidden():
            a0.ignore()

        else:

            # Uncheck the addtimerButton
            self.mw.toolBar.addTimerButton.setChecked(False)

            if not self.mw.isMinimized():

                self.config['QOL'][ConfigKeys.addtimer_open_on_startup] = 'False'
                self.config.save()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:

        # Check the addtimerButton
        self.mw.toolBar.addTimerButton.setChecked(True)

        self.dropDownSelected(self.topicDropDown.currentText())
        # Check if the parent widget is minimized
        if not self.mw.isMinimized():

            self.config['QOL'][ConfigKeys.addtimer_open_on_startup] = 'True'

            self.config.save()
        # Call the base class's showEvent method

        return super().showEvent(a0)
