
import threading
from datetime import datetime, timedelta, date
import os
from configparser import ConfigParser
import requests
import webbrowser
from random import choice as randChoice

from PyQt5.QtCore import QPoint, QTimer, Qt
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from apprise import Apprise, AppriseAsset

from style import StyleManager

class addTimer(qtw.QDockWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setWindowTitle('Add Timer')
        self.setObjectName('addTimerDockWidget')
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetClosable)

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
        self.formLayout.setRowWrapPolicy(qtw.QFormLayout.WrapAllRows)
        self.topicFrame.setLayout(self.formLayout)


        # Topic data
        self.topicSelectionDict = {

            '': {
                'durations': tuple(['Nothing Selected'])
            },

            'Stamina': {
                'durations': 'Stamina'
            },

            'Parametric Transformer': {
                'durations': tuple(['7 Days'])
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

        # Topic Selection Row
        self.topicLabel = qtw.QLabel('Timed Object:')
        self.topicDropDown = qtw.QComboBox()
        self.topicDropDown.setFocusPolicy(Qt.NoFocus)
        self.topicDropDown.addItems( [x for x in self.topicSelectionDict.keys()] )
        self.topicDropDown.currentTextChanged.connect(lambda topic : self.dropDownSelected(topic))

        self.formLayout.addRow(self.topicLabel, self.topicDropDown)

        # Duration Row
        self.durationLabel = qtw.QLabel('Duration:')
        self.durationDropDown = qtw.QComboBox()
        self.durationDropDown.addItem('Nothing Selected')
        self.durationDropDown.setFocusPolicy(Qt.NoFocus)

        self.formLayout.addRow(self.durationLabel, self.durationDropDown)

        # Values for when the player has characters that have a 25% time discount
        # {'4 Hours': 3}
        self.expeditionTwentyFivePercentOffDict = {k:v for (k,v) in zip(self.topicSelectionDict['Expedition']['durations'], ('3 Hours', '6 Hours', '9 Hours', '15 Hours'))}

        self.expeditionLabel = qtw.QLabel('Using a 25% Time Reduction Character')
        self.expeditionCheckBox = qtw.QCheckBox()
        self.expeditionCheckBox.setChecked(config['QOL'].getboolean('expedition_checkbox', fallback=True))

        self.formLayout.addRow(self.expeditionLabel, self.expeditionCheckBox)

        # Realm Currency Level (Hidden by default, see show/hide events)
        # {Trust Rank : Realm Currency Storage Limit}
        self.rCLevelValues = {
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

        # Dict of Realm Statuses and their corresponding income rates
        # {status:rate/hr}

        self.rCRateValuesDict = {k:v for (k,v) in zip(self.topicSelectionDict['Realm Currency']['durations'], (4, 8, 12, 16, 20, 22, 24, 26, 28, 30))}

        # Dict of Adeptal Energy thresholds and their corresponding income rates for companionship XP
        # {adeptal energy range:rate/hr}

        self.rCFriendshipValuesDict = {k:v for (k,v) in zip(self.topicSelectionDict['Realm Companionship XP']['durations'], range(2, 6)) }

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
        self.nameLabel = qtw.QLabel('Name (Optional):')
        self.nameLineEdit = qtw.QLineEdit()

        self.formLayout.addRow(self.nameLabel, self.nameLineEdit)

        self.colorsDict: list[str] = list(styles.getStopwatchColors().keys())

        # Color Row
        self.outlineColorLabel = qtw.QLabel('Border Color:')
        self.outlineColorDropDown = qtw.QComboBox()
        self.outlineColorDropDown.setFocusPolicy(Qt.NoFocus)
        self.outlineColorDropDown.addItems([x.title() for x in self.colorsDict])

        self.formLayout.addRow(self.outlineColorLabel, self.outlineColorDropDown)

        # Button
        self.startTimerButton = qtw.QPushButton('Start Timer')
        self.startTimerButton.clicked.connect(lambda: self.startStopWatch())
        verticalLayout.addWidget(self.startTimerButton, alignment=Qt.AlignTop)

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
        selectedTopic = self.topicSelectionDict[topic]['durations']

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
                self.lineEdit2.setText(config['QOL'].get('desiredStamina', fallback='160'))
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


    def startStopWatch(self):
        ''' Fired when the addTimer button is pressed. This gathers then transforms the current data suitable for the stopwatch's parameters and begins the stopwatch '''

        # Get the selected time object and outline color
        
        timeObject = self.topicDropDown.currentText()

        # self.colorsDict is excluding index 0 because that would be the 'random' key value in the dict
        color: str = randChoice(self.colorsDict[1:]) if self.outlineColorDropDown.currentText() == 'Random' else self.outlineColorDropDown.currentText()

        days: int = 0
        hours: int = 0
        minutes: int = 0

        percentToMinutes: callable[[str], str] = lambda rate: round( (float(rate) / 100) * 60 )
        calculateDuration: callable[[int, int], str] = lambda maxStorage, rate: str(round(maxStorage/rate, 2)).split('.')
            
        # Match the selected time object
        match timeObject:

            case 'Expedition':
                
                duration: str = self.durationDropDown.currentText()

                hours = duration if not self.expeditionCheckBox.isChecked() else self.expeditionTwentyFivePercentOffDict[duration]

                hours = int(hours.split()[0])

            case 'Realm Currency':
                
                try:
                # Check if the input is in the valid range
                    if int(self.lineEdit1.text()) not in range(1, 11):
                        raise ValueError
                except ValueError:
                    return self.lineEdit1.setText('Error: Invalid Input')
                # Rerieve maximum storage and rate values
                maxStorage: int = self.rCLevelValues[self.lineEdit1.text()]

                rate: str = self.durationDropDown.currentText()
                duration = self.rCRateValuesDict[rate]

                duration: list[str] = calculateDuration(maxStorage, duration)

                hours = int(duration[0])
                minutes = percentToMinutes(duration[1])

            case 'Realm Companionship XP':
           
                try:
                # Check if the input is in the valid range
                    if int(self.lineEdit1.text()) not in range(1, 11):
                        raise ValueError
                except ValueError:
                    return self.lineEdit1.setText('Error: Invalid Input')
                # Rerieve maximum storage and rate values
                
                maxStorage = int(self.lineEdit1.text()) * 50

                rate: str = self.durationDropDown.currentText()
                duration = self.rCFriendshipValuesDict[rate]

                duration = calculateDuration(maxStorage, duration)

                hours = int(duration[0])
                minutes = percentToMinutes(duration[1])

            case 'Custom':
            # Retrieve input values for days, hours, and minutes
                days: str|int = self.lineEdit1.text() if self.lineEdit1.text().isdigit() else 0
                hours: str|int = self.lineEdit2.text() if self.lineEdit2.text().isdigit() else 0
                minutes: str|int = self.lineEdit3.text() if self.lineEdit3.text().isdigit() else 0
                # Convert values to positive integers
                days = abs(int(days))
                hours = abs(int(hours))
                minutes = abs(int(minutes))

            case 'Stamina':
                
                # Get inputs
                amountOfStamina: str = self.lineEdit1.text()
                desiredStamina: str = self.lineEdit2.text()

                # Checking for valid inputs
                if amountOfStamina.isdigit() == False or int(amountOfStamina) > 160 or int(amountOfStamina) < 0:
                    return self.lineEdit1.setText('Error: Invalid Input')
                
                elif desiredStamina.isdigit() == False or int(desiredStamina) > 160 or int(desiredStamina) < 0:
                    return self.lineEdit2.setText('Error: Invalid Input')
                
                # Program remembers how much stamina the user wants
                config['QOL']['desiredStamina'] = desiredStamina
                saveConfig()

                # Example: (160 - 20 = 140), user needs 140 stamina until 160, stamina takes 8 minutes to regen 1 stamina
                minutes = (int(desiredStamina) - int(amountOfStamina)) * 8
                    
            # Case: default
            case _:

                duration: str = self.durationDropDown.currentText()
                    
                # Check if no duration is selected
                if duration == 'Nothing Selected':
                    return

                duration = duration.split()

                if duration[1] == 'Days' or duration[1] == 'Day':
                    duration = int(duration[0]) * 24
                else:
                    duration = int(duration[0])


                hours = duration
                
        # Create a timedelta object with the calculated duration
        duration = timedelta(days=days, hours=hours, minutes=minutes)
        
        # Get the text from the nameLineEdit and use it as the name if it is not empty, otherwise use timeObject
        nameText = self.nameLineEdit.text()
        name = nameText if len(nameText) > 0 else timeObject
        
        # Find the central widget and call the addStopWatch method with the relevant parameters
        centralWidget_: centralWidget = self.parent().findChild(qtw.QWidget, 'centralWidget')

        centralWidget_.addStopWatch(timeObject, duration, name, duration, color)


    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        # Check if the parent widget is hidden
        
        if self.parent().isHidden():
            a0.ignore()

        else:
            
            parent: qtw.QMainWindow = self.parent()
            toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
            # Uncheck the addtimerButton
            
            addtimerButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'addTimerButton')

            addtimerButton.setChecked(False)

            if not parent.isMinimized():

                config['QOL']['addtimer open on startup'] = 'False'
                saveConfig()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        addtimerButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'addTimerButton')
        # Check the addtimerButton

        addtimerButton.setChecked(True)

        self.dropDownSelected(self.topicDropDown.currentText())
        # Check if the parent widget is minimized
        if not parent.isMinimized():

            config['QOL']['addtimer open on startup'] = 'True'

            saveConfig()
        # Call the base class's showEvent method
        
        return super().showEvent(a0)

class optionsDock(qtw.QDockWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setWindowTitle('Options')
        self.setObjectName('optionsDockWidget')
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetClosable)

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
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setHorizontalSpacing(10)
        self.topicFrame.setLayout(self.formLayout)

        # Checkbox
        self.appOnCloseCheckbox = qtw.QCheckBox()
        self.appOnCloseCheckbox.setChecked(config['OPTIONS'].getboolean('shutdown app on close'))
        self.appOnCloseCheckbox.clicked.connect(lambda: self.settingChanged('true'))
        self.appOnCloseCheckbox.setToolTip('The app will close and not run in the background.')
        # Form Row
        self.formLayout.addRow('Shutdown app on close: ', self.appOnCloseCheckbox)

        # Checkbox
        self.showOnOpenCheckbox = qtw.QCheckBox()
        self.showOnOpenCheckbox.setChecked(config['OPTIONS'].getboolean('show on startup'))
        self.showOnOpenCheckbox.clicked.connect(lambda: self.settingChanged('true'))
        self.showOnOpenCheckbox.setToolTip('Program will automatically show or hide when starting.')
        # Form Row
        self.formLayout.addRow('Show on app start: ', self.showOnOpenCheckbox)

        self.updateCheckBox = qtw.QCheckBox()
        self.updateCheckBox.setChecked(config['OPTIONS'].getboolean('checkVersionOnStartup', fallback=True))
        self.updateCheckBox.clicked.connect(lambda: self.settingChanged('true'))
        self.updateCheckBox.setToolTip('When the program starts it will go online to check and see if your client is up-to-date')
        self.formLayout.addRow('Check for update on startup: ', self.updateCheckBox)

        # Checkbox
        self.notifyCheckbox = qtw.QCheckBox()
        self.notifyCheckbox.setChecked(config['OPTIONS'].getboolean('desktop notifications'))
        self.notifyCheckbox.clicked.connect(lambda: self.settingChanged('true'))
        self.notifyCheckbox.setToolTip('A windows desktop notification will appear when a stopwatch finishes.')
        # Form Row
        self.formLayout.addRow('Desktop notifications: ', self.notifyCheckbox)

        # Checkbox
        self.staticDailyNotifyCheckbox = qtw.QCheckBox()
        self.staticDailyNotifyCheckbox.setChecked(config['OPTIONS'].getboolean('dailyResetNotify', fallback=False))
        self.staticDailyNotifyCheckbox.clicked.connect(lambda: self.settingChanged('true'))
        self.staticDailyNotifyCheckbox.setToolTip('Will recieve a notification when there is a daily reset.')
        # Form Row
        self.formLayout.addRow('Daily Reset Notifications: ', self.staticDailyNotifyCheckbox)

        # Checkbox
        self.staticWeeklyNotifyCheckbox = qtw.QCheckBox()
        self.staticWeeklyNotifyCheckbox.setChecked(config['OPTIONS'].getboolean('weeklyResetNotify', fallback=False))
        self.staticWeeklyNotifyCheckbox.clicked.connect(lambda: self.settingChanged('true'))
        self.staticWeeklyNotifyCheckbox.setToolTip('Will recieve a notification when there is a daily reset.')
        # Form Row
        self.formLayout.addRow('Weekly Reset Notifications: ', self.staticWeeklyNotifyCheckbox)

        # Dropdown
        self.colorPallet = qtw.QComboBox()
        self.colorPallet.addItems([x.title() for x in styles.getColorPallets()])
        self.colorPallet.setCurrentText(config.get('OPTIONS', 'color pallet', fallback='dark').title())
        self.colorPallet.currentTextChanged.connect(lambda: self.settingChanged('true'))
        self.colorPallet.setFocusPolicy(Qt.NoFocus)
        # Form Row
        self.formLayout.addRow('Color Scheme: ', self.colorPallet)

        # Apply Settings Button
        self.applyButton = qtw.QPushButton('Apply', self)
        self.applyButton.setObjectName('applySettingsButton')
        self.applyButton.clicked.connect(lambda: self.applySettings())
        self.applyButton.clicked.connect(lambda: self.settingChanged("false"))
        self.applyButton.setProperty('unsavedChanges', "false")
        verticalLayout.addWidget(self.applyButton, alignment=Qt.AlignTop)

        # Check for updates button
        self.updateButton = qtw.QPushButton('Check for updates', self)
        self.updateButton.setObjectName('checkUpdateButton')
        self.updateButton.clicked.connect(lambda: self.checkUpdate(button=True))
        verticalLayout.addWidget(self.updateButton, alignment=Qt.AlignTop)

        self.setWidget(self.centralFrame)
    
    def settingChanged(self, boolean: str):
        
        # Change the property of the applyButton to signal the user a setting's been changed
        self.applyButton.setProperty('unsavedChanges', f"{boolean}")
        
        self.style().polish(self.applyButton)
    
    def checkUpdate(self, button: bool = False) -> None:
        
        # Will create a dialog window if there's a version update unless specified not to
        if version < version_check and config['OPTIONS'].getboolean('checkVersionOnStart', fallback=True):

            updateNotify: qtw.QDialog = UpdateAlert(self)

            updateNotify.exec()

            return
        
        # Checking if the function was started by the "check for update button"
        if button:
            self.updateButton.setText('On latest version ^_^')
            QTimer.singleShot(3000, lambda: self.updateButton.setText('Check for updates'))
    
    def applySettings(self):
        # Create a dictionary with updated configuration settings

        updatedConfig = {
                            'shutdown app on close' : str(self.appOnCloseCheckbox.isChecked()),
                            'show on startup'       : str(self.showOnOpenCheckbox.isChecked()),
                            'desktop notifications' : str(self.notifyCheckbox.isChecked()),
                            'color pallet'          : self.colorPallet.currentText().lower(),
                            'checkversiononstartup' : str(self.updateCheckBox.isChecked()),
                            'dailyResetNotify'      : str(self.staticDailyNotifyCheckbox.isChecked()),
                            'weeklyResetNotify'     : str(self.staticWeeklyNotifyCheckbox.isChecked())
                        }
        
        # Checking to see if the user wants to change the color scheme
        if self.colorPallet.currentText() != config.get('OPTIONS', 'color pallet', fallback='dark'):

            styles.changeColorPallet(updatedConfig['color pallet'])

            for stopwatch in mw.central.findChildren(qtw.QFrame):

                # Identifying a stopwatch
                if len(stopwatch.objectName()) == 13:
                    # Updating the stylesheet again to change border color
                    styles.changeStopwatchBorderColor(stopwatch.property('border-color'))

                    # Change stopwatch stylesheet
                    stopwatch.setStyleSheet(styles.getStyleSheet('stopwatch'))
                    mw.central.style().polish(stopwatch)

            # Change global stylesheet        
            app.setStyleSheet(styles.getStyleSheet('app'))
            app.style().polish(app)

        config['OPTIONS'] = updatedConfig

        saveConfig()
        self.settingChanged(False)

    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        # Check if the parent widget is hidden

        if self.parent().isHidden():
            a0.ignore()

        else:

            parent: qtw.QMainWindow = self.parent()
            toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
            optionsButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'optionsButton')

            optionsButton.setChecked(False)
            
            if not parent.isMinimized():
                # Update the configuration setting 'settings open on startup' to 'False'
                config['QOL']['settings open on startup'] = 'False'
                
                # Save the updated configuration
                saveConfig()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:
        # Get references to the parent widget, toolbar, and optionsButton

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        optionsButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'optionsButton')
        # Set the optionsButton as checked

        optionsButton.setChecked(True)

        # Update the configuration setting 'settings open on startup' to 'True'
        if not parent.isMinimized():
            
            config['QOL']['settings open on startup'] = 'True'
            saveConfig()
        return super().showEvent(a0)

class Guide(qtw.QDockWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setWindowTitle('Guide')
        self.setObjectName('guideDockWidget')
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetClosable)

        # Central Frame
        self.centralFrame: qtw.QFrame = qtw.QFrame(self)

        # Vertical Box Layout
        verticalLayout: qtw.QVBoxLayout = qtw.QVBoxLayout()
        self.centralFrame.setLayout(verticalLayout)

        self.textFile: qtw.QTextBrowser = qtw.QTextBrowser(self.centralFrame)
        self.textFile.setReadOnly(True)

        # Reading html guide
        try:
            with open(os.path.join( os.path.abspath(os.path.dirname(__file__)), 'guide.html'), 'r') as html:
                    
                    # The guide is packaged into the .exe so it is always updated
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
        
        if self.parent().isHidden():
            a0.ignore()

        else:
            
            parent: qtw.QMainWindow = self.parent()
            toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
            # Uncheck the guideButton
            
            guideButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'guideButton')

            guideButton.setChecked(False)

            if not parent.isMinimized():

                config['QOL']['guide open on startup'] = 'False'
                saveConfig()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        guideButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'guideButton')
        # Check the guideButton

        guideButton.setChecked(True)

        # Check if the parent widget is minimized
        if not parent.isMinimized():

            config['QOL']['guide open on startup'] = 'True'

            saveConfig()
        # Call the base class's showEvent method
        
        return super().showEvent(a0)


class staticTimers(qtw.QDockWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setWindowTitle('Static Timers')
        self.setObjectName('staticTimersDockWidget')
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetClosable)

        # Checking to see if 'STATIC_TIMERS' is a valid section in config.ini
        try:
            config['STATIC_TIMERS'].keys()
        except KeyError:
            config.add_section('STATIC_TIMERS')
            saveConfig()

        # Instancing the deadlines that may or may have not been reached to make room for the new deadlines
        # This is for checkNotify()
        self.oldDeadlines: dict[str:str] = {k:v for (k, v) in config['STATIC_TIMERS'].items()}

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
        self.chooseServerDropDown.setCurrentText(config['QOL'].get('gameServer', fallback='NA'))
        self.chooseServerDropDown.currentTextChanged.connect(lambda server: self.changeServer(server))
        formlayout.addRow('Server: ', self.chooseServerDropDown)

        self.setWidget(self.centralFrame)

        # Defining variables for timers

        # Set notification name for later
        self.notifyName = ' '

        self.dailyQTimer = QTimer(self)
        self.weeklyQTimer = QTimer(self)

        self.one = timedelta(seconds=1)
        self.zero = timedelta(seconds=0)

        self.serverChange = False
        
        # Start Static Timers
        self.staticTimerStart()

    def staticTimerStart(self):

        self.serverChange = False

        # Update perferred server setting
        self.selectedServer: str = config['QOL'].get('gameServer', fallback='NA')

        # Define today's date and time
        self.today = datetime.today().replace(microsecond=0)

        ### Daily Timer

        # Calculating the deadline of the daily reset with their choice of server
        self.dailyDeadline = datetime(year=self.today.year, month=self.today.month, day=self.today.day, hour=9) + timedelta(hours=self.serverTimezones[self.selectedServer])

        # If the program starts after the reset time happened, add a day to the deadline 
        if self.dailyDeadline < self.today:

            self.dailyDeadline += timedelta(days=1)
        
        config['STATIC_TIMERS']['dailydeadline'] = datetime.strftime(self.dailyDeadline, '%Y-%m-%d %I:%M:%S')

        self.difference = self.dailyDeadline - self.today

        ### Weekly Timer

        # Calculating how many days left until Monday
        # date.weekday starts at 0
        dayOfTheWeek = date.weekday(self.today) + 1
        self.weeklyDayDifference: int = 7 - dayOfTheWeek

        # Calculating the deadline of the weekly reset with their choice of server
        self.weeklyDeadline = datetime(year=self.today.year, month=self.today.month, day=(self.today.day + self.weeklyDayDifference), hour=9) + timedelta(hours=self.serverTimezones[self.selectedServer])

        config['STATIC_TIMERS']['weeklydeadline'] = datetime.strftime(self.weeklyDeadline, '%Y-%m-%d %I:%M:%S')

        self.weeklyDifference = self.weeklyDeadline - self.today
        
        saveConfig()

        self.dailyResetTimer()
        self.weeklyResetTimer()

        # Renabling server selection
        self.chooseServerDropDown.setEnabled(True)
        
    
    def dailyResetTimer(self):

        if self.difference > self.zero:

            self.difference -= self.one

            self.dailyReset.setText(str(self.difference))

            # Returns when the user changes the server to prevent timer being called multiple times
            if not self.serverChange:
                self.dailyQTimer.singleShot(1000, lambda: self.dailyResetTimer())
            else:
                return
        
        else:
            
            today = datetime.today()

            self.dailyDeadline += timedelta(days=1)
            config['STATIC_TIMERS']['dailyDeadline'] = datetime.strftime(self.weeklyDeadline, '%Y-%m-%d %I:%M:%S')
            saveConfig()

            self.difference = self.dailyDeadline - today

            self.dailyQTimer.singleShot(1000, lambda: self.dailyResetTimer())

            if config['OPTIONS'].getboolean('dailyResetNotify', fallback=False) and config['OPTIONS'].getboolean('desktop notifications', fallback=True):

                self.notifyName = 'daily reset'

                # Create thread so program doesn't freeze while notification is active
                self.notify_thread: threading.Thread = threading.Thread(target=notify.notify, kwargs={'body': f'Reset(s): {self.notifyName}', 'title':'Reset Happened'})
                self.notify_thread.start()

    def weeklyResetTimer(self):

        if self.weeklyDifference > self.zero:

            self.weeklyDifference -= self.one

            # Used formatted string because you only need to see the days since `daily reset` tells you the time
            self.weeklyReset.setText(f'{self.weeklyDifference.days} Day(s) left')

            # Returns when the user changes the server to prevent timer being called multiple times
            if not self.serverChange:
                self.weeklyQTimer.singleShot(1000, lambda: self.weeklyResetTimer())
            else:
                return
        
        else:

            today = datetime.today()

            self.weeklyDeadline += timedelta(days=7)
            config['STATIC_TIMERS']['weeklyDeadline'] = datetime.strftime(self.weeklyDeadline, '%Y-%m-%d %I:%M:%S')
            saveConfig()

            self.weeklyDifference = self.weeklyDeadline - today

            self.weeklyQTimer.singleShot(1000, lambda: self.weeklyResetTimer())

            if config['OPTIONS'].getboolean('weeklyResetNotify', fallback=False) and config['OPTIONS'].getboolean('desktop notifications', fallback=True):

                self.notifyName = 'weekly reset'
                # Create thread so program doesn't freeze while notification is active
                self.notify_thread: threading.Thread = threading.Thread(target=notify.notify, kwargs={'body': f'Reset(s): {self.notifyName}', 'title':'Reset Happened'})
                self.notify_thread.start()
    
    def changeServer(self, server: str):
        
        # Prevent the selection from being spammed which would break the timers
        self.chooseServerDropDown.setEnabled(False)
        

        config['QOL']['gameServer'] = server
        saveConfig()

        self.serverChange = True

        QTimer.singleShot(1000, lambda: self.staticTimerStart())
    
    def checkNotify(self):
        '''Checking to see if resets happened while the program was shutdown'''

        static_timers: list[str] = []

        # Getting desktop notification setting bool
        staticNotify: bool = config['OPTIONS'].getboolean('desktop notifications', fallback=True)

        for name, date in self.oldDeadlines.items():

            # Getting notification setting bool
            notification: bool = config['OPTIONS'].getboolean('{0}ResetNotify'.format(name.split('deadline')[0]), fallback=False)
            
            # Putting every notification setting in a tuple so that the if condition is easier to read below by using all()
            settingsCheck = (notification, staticNotify)

            # If date isn't valid then skip to the next iteration
            try:
                deadline: datetime = datetime.strptime(date, '%Y-%m-%d %I:%M:%S')
            except ValueError as e:
                print(e)
                continue

            # If time has passed the static timer's deadline and if the notification settings are set to true
            if deadline < self.today and all(settingsCheck):


                static_timers.append(name.split('deadline')[0].title())

        # Empty lists return false
        if not static_timers:
            return
        
        else:

            self.notify_thread: threading.Thread = threading.Thread(target=notify.notify, kwargs={'body': f'Reset(s): {self.notifyName.join(static_timers)}', 'title':'Reset Happened'})
            self.notify_thread.start()
        

    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        # Check if the parent widget is hidden

        if self.parent().isHidden():
            a0.ignore()

        else:

            parent: qtw.QMainWindow = self.parent()
            toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
            staticTimersButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'staticTimersButton')

            staticTimersButton.setChecked(False)
            
            if not parent.isMinimized():
                # Update the configuration setting 'settings open on startup' to 'False'
                config['QOL']['static timers open on startup'] = 'False'
                
                # Save the updated configuration
                saveConfig()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:
        # Get references to the parent widget, toolbar, and optionsButton

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        staticTimersButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'staticTimersButton')
        # Set the optionsButton as checked

        staticTimersButton.setChecked(True)

        # Update the configuration setting 'settings open on startup' to 'True'
        if not parent.isMinimized():
            
            config['QOL']['static timers open on startup'] = 'True'
            saveConfig()
        return super().showEvent(a0)


class toolbar(qtw.QToolBar):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)
        
        # Set floatable and movable to False
        self.setFloatable(False)
        self.setMovable(False)

        self.layout().setSpacing(20)

        # Add Timer Button
        self.addTimerButton = qtw.QAction('Add Timer', self)
        self.addTimerButton.setObjectName('addTimerButton')
        self.addTimerButton.setCheckable(True)
        self.addTimerButton.setChecked(config['QOL'].getboolean('addtimer open on startup'))
        self.addTimerButton.triggered.connect(lambda: self.button_Clicked('addTimerDockWidget', self.addTimerButton.isChecked() ) )
        self.addAction(self.addTimerButton)

        # Options Button
        self.optionsButton = qtw.QAction('Options', self)
        self.optionsButton.setObjectName('optionsButton')
        self.optionsButton.setCheckable(True)
        self.optionsButton.setChecked(config['QOL'].getboolean('settings open on startup'))
        self.optionsButton.triggered.connect(lambda: self.button_Clicked('optionsDockWidget', self.optionsButton.isChecked() ) )
        self.addAction(self.optionsButton)

        # Guide Button
        self.guideButton = qtw.QAction('Guide', self)
        self.guideButton.setObjectName('guideButton')
        self.guideButton.setCheckable(True)
        self.guideButton.setChecked(config['QOL'].getboolean('guide open on startup', fallback=False))
        self.guideButton.triggered.connect(lambda: self.button_Clicked('guideDockWidget', self.guideButton.isChecked()))
        self.addAction(self.guideButton)

        # Static Timers Button
        self.staticButton = qtw.QAction('Static Timers', self)
        self.staticButton.setObjectName('staticTimersButton')
        self.staticButton.setCheckable(True)
        self.staticButton.setChecked(config['QOL'].getboolean('static timers open on startup', fallback=False))
        self.staticButton.triggered.connect(lambda: self.button_Clicked('staticTimersDockWidget', self.staticButton.isChecked()))
        self.addAction(self.staticButton)

    def button_Clicked(self, dockObjectName: str, buttonisChecked: bool):
        # Find the QDockWidget based on the dockObjectName

        addDockWidget: qtw.QDockWidget = self.parent().findChild(qtw.QDockWidget, dockObjectName)

        if buttonisChecked:
            # If the button is checked, show the QDockWidget

            addDockWidget.show()

        else:
            # If the button is not checked, hide the QDockWidget

            addDockWidget.hide()


class centralWidget(qtw.QWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)
        # Create the layout for the central widget

        self.setObjectName('centralWidget')
        self.scrollAreaLayout = qtw.QHBoxLayout(self)
        self.scrollAreaLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout = qtw.QVBoxLayout()
        # Create the scroll area

        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setContentsMargins(0,0,0,0)
        # Create the widget to hold the scroll area contents

        self.scrollAreaWidgetContents = qtw.QWidget()
        self.scrollAreaWidgetContents.setContentsMargins(0,0,0,0)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)
        # Set the scroll area widget

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.addWidget(self.scrollArea)

    def addStopWatch(self, timeObject: str, duration: timedelta, name: str, startDuration: timedelta, color: str, notepadContents: str = '', index: int | None = None, save: bool = True) -> None:
        # Create a QFrame to hold the stopwatch
        
        styles.changeStopwatchBorderColor(color)
        color = styles.getStopwatchColor(color)

        self.frame = qtw.QFrame(self.scrollAreaWidgetContents)
        self.frame.setStyleSheet(styles.getStyleSheet('stopwatch'))
        
        # Set the object name of the frame using its ID
        id_ = str(id(self.frame))
        self.frame.setObjectName(id_)
        self.frame.setMaximumHeight(500)

        parent: qtw.QFrame = self.findChild(qtw.QFrame, id_)
        # Set the border color property of the frame

        parent.setProperty('border-color', color)
        # Extract the start duration in days and minutes

        startDurationDays = int( str(startDuration).split(':')[0].split()[0] )
        startDurationMinutes = int( str(startDuration).split(':')[1].split(':')[0] )
        # Adjust the start duration minutes to have two digits

        if len(str(startDurationMinutes)) == 1:
            startDurationMinutes = str(startDurationMinutes) + '0'
        # Set the original duration property of the frame

        if startDuration >= timedelta(hours=24): # startDuration gives the days but not in total hours, needed so that loadSaveData() can work
            parent.setProperty('originalDuration', f'{startDurationDays * 24}:{startDurationMinutes}:00')

        else:
            # Otherwise, set it directly as the startDuration
            parent.setProperty('originalDuration', startDuration)


        frameLayout = qtw.QGridLayout()
        frameLayout.setContentsMargins(20,20,20,20)
        # Create a QLabel for the name

        nameLabel = qtw.QLabel(name, self.frame)
        nameLabel.setObjectName('nameLabel')
        frameLayout.addWidget(nameLabel, 0, 0, alignment=Qt.AlignTop)
        # Create a delete button

        deleteButton = qtw.QPushButton('X', self.frame)
        deleteButton.setMinimumSize(40,40)
        deleteButton.clicked.connect(lambda: self.deleteTimer(id_))
        frameLayout.addWidget(deleteButton, 0, 2, alignment=Qt.AlignRight)
        # Create a QLabel for the countdown time

        countDown = qtw.QLabel('00:00:00', self.frame)
        countDown.setObjectName('CountDownLabel')
        frameLayout.addWidget(countDown, 1, 0, 1, 3, alignment=Qt.AlignCenter)
        # Create a reset button

        resetButton = qtw.QPushButton('Reset Timer', self.frame)
        resetButton.setObjectName('resetButton')
        resetButton.setMinimumSize(120,60)
        resetButton.setMaximumSize(240,60)
        resetButton.clicked.connect(lambda: self.resetTimer(timeObject, name, startDuration, id_, color, notes=notepad.toPlainText()))
        frameLayout.addWidget(resetButton, 2,0, alignment=Qt.AlignBottom)
        
        # Create a QLabel for the finished date
        finishedDate = datetime.now() + duration
        finishedDateLabel = qtw.QLabel(f'Finished on: {finishedDate.strftime("%B %d @ %I:%M %p")}')
        finishedDateLabel.setObjectName('finishedDateLabel')
        frameLayout.addWidget(finishedDateLabel, 2, 1, alignment=Qt.AlignCenter)
        
        # Create a QTextEdit for notes
        notepad = qtw.QTextEdit(self.frame)
        notepad.setPlaceholderText('Notes go here')
        notepad.setText(notepadContents)
        notepad.setMinimumSize(300, 100)
        notepad.setMaximumSize(400, 200)
        notepad.anchorAt(QPoint(0,0))

        frameLayout.addWidget(notepad, 2, 2)
        
        # Set the layout for the frame
        self.frame.setLayout(frameLayout)

        # Index is only given when a timer is resetTimer() is called
        if index != None:
            self.verticalLayout.insertWidget(index, self.frame)
        else:
            self.verticalLayout.addWidget(self.frame)
        
        self.frame.show()


        currentTime = datetime.today()

        finishedTime = currentTime + duration

        parent.setProperty('finishedTime', datetime.strftime(finishedTime, '%Y-%m-%d %H:%M:%S'))

        difference =  finishedTime - currentTime
    
        # Find the reset button and count down label
        resetButton: qtw.QPushButton = parent.findChild(qtw.QPushButton, 'resetButton')
        countDownLabel: qtw.QLabel = parent.findChild(qtw.QLabel, 'CountDownLabel')

        zero = timedelta(days=0, hours=0, seconds=0)
        one = timedelta(seconds=1)
        
        # Create a QTimer for updating the countdown label
        QTimer_ = QTimer(parent)
        QTimer_.setObjectName('QTimer')

        # Create thread so program doesn't freeze while notification is active
        notify_thread: threading.Thread = threading.Thread(target=notify.notify, kwargs={'body': f'{name} has finished!', 'title':'Stopwatch Finished'})

        def countDownTimer(self: qtw.QWidget, difference: datetime) -> None:

            try:

                difference -= one

                if difference > zero:
                    
                    # Update the countdown label with the new difference
                    countDownLabel.setText(str(difference))
                    
                    # Schedule the next update of the countdown timer after 1 second
                    QTimer_.singleShot(1000, lambda: countDownTimer(self, difference))

                else:
                    countDownLabel.setText('00:00:00')
                    countDownLabel.setProperty('finished', "true")
                    parent.style().polish(countDownLabel)
                    
                    # Show desktop notification if the 'desktop notifications' option is enabled
                    if config['OPTIONS'].getboolean('desktop notifications'):

                        notify_thread.start()

            # If timer is deleted, will traceback a runtime error because the function is trying to locate objects that don't exist anymore
            except RuntimeError: 
                return


        countDownTimer(self, difference)

        if save:
            self.parent().saveData()
    def deleteTimer(self, id_: str):
        self.findChild(qtw.QFrame, id_).deleteLater()

        # There is a 1ms delay to call saveData() so that the deleteLater() method can finish, otherwise saveData() won't save anything
        QTimer.singleShot(1, lambda: self.parent().saveData())

    def resetTimer(self, timeObject: str, name: str, startDuration: timedelta, id: str, color: str, notes: str = ''):
        # Find the frame associated with the given ID
        frame: qtw.QFrame = self.findChild(qtw.QFrame, id)

        index = self.verticalLayout.indexOf(frame)

        self.findChild(qtw.QFrame, id).deleteLater()

        currentTime = datetime.today()

        difference =  (currentTime + startDuration) - currentTime

        self.addStopWatch(timeObject, difference, name, startDuration, color, notepadContents=notes, index=index)



class window(qtw.QMainWindow):
    def __init__(self):
        super(window, self).__init__()

        self.toolBar = toolbar(self)
        self.addToolBar(self.toolBar)

        self.central = centralWidget(self)
        self.setCentralWidget(self.central)

        self.dockWidgetAddTimer = addTimer(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetAddTimer)
        self.dockWidgetAddTimer.setVisible(config['QOL'].getboolean('addtimer open on startup'))

        self.dockWidgetOptions = optionsDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetOptions)
        self.dockWidgetOptions.setVisible(config['QOL'].getboolean('settings open on startup'))

        self.dockWidgetGuide = Guide(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetGuide)
        self.dockWidgetGuide.setVisible(config['QOL'].getboolean('guide open on startup', fallback=False))

        self.dockWidgetStaticTimer = staticTimers(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetStaticTimer)
        self.dockWidgetStaticTimer.setVisible(config['QOL'].getboolean('static timers open on startup', fallback=False))

        # So the resize event doesn't spam the save window resolution function (see sizeApplyTimerTimeout() )
        self.windowSizeApplyTimer = QTimer(self)
        self.windowSizeApplyTimer.setObjectName('windowSizeApplyTimer')
        self.windowSizeApplyTimer.timeout.connect(lambda: self.sizeApplyTimerTimeout())

        self.resize(config['WINDOW SIZE'].getint('width'), config['WINDOW SIZE'].getint('height'))

        self.loadSaveData()

        # Checking to see if the client is the latest version
        self.dockWidgetOptions.checkUpdate()

        # Checking to see if any static timers went off while the program was shutdown
        self.dockWidgetStaticTimer.checkNotify()

    def loadSaveData(self):
        data = ConfigParser()
        data.read(saveFile_path)

        for timerID in data.sections():

            # Name
            name = data[timerID]['name']

            # Changing the timer's destination into a datetime type
            timeFinished = data[timerID]['time finished']
            timeFinished = datetime.strptime(timeFinished, '%Y-%m-%d %H:%M:%S')
            timeFinished = timeFinished - datetime.today().replace(microsecond=0)

            # The original duration (For resetting the timer) and changing into a timedelta type
            originalDuration = data[timerID]['time original duration'].split(':')
            originalDuration = timedelta(hours= int(originalDuration[0]), minutes= int(originalDuration[1]))

            # Border color (In hexcode format)
            borderColor = data[timerID]['border color']

            # Notes
            notes = data[timerID]['notes']



            # Remove old ID
            data.remove_section(timerID)

            # Create stopwatch
            self.central.addStopWatch(name, timeFinished, name, originalDuration, borderColor, notes, save=False)

        # Update the savefile (Old IDs are removed)
        with open(saveFile_path, 'w') as f:
            data.write(f)

        # Update the savefile (Saving new IDs created from for loop)
        self.saveData()

    def saveData(self):

        data = ConfigParser()

        for qtObject in self.central.findChildren(qtw.QFrame):

            objectName: str = qtObject.objectName()

            if len(objectName) == 13: # Length of a stopwatch's name which is their id() value

                data[objectName] = {
                    'name'                   : qtObject.findChild(qtw.QLabel, "nameLabel").text(),
                    'time finished'          : qtObject.property("finishedTime"),
                    'time original duration' : qtObject.property("originalDuration"),
                    'border color'           : qtObject.property("border-color"),
                    'notes'                  : qtObject.findChild(qtw.QTextEdit).toPlainText()
                }

        with open(saveFile_path, 'w') as f:
            data.write(f)

    def sizeApplyTimerTimeout(self):

        self.windowSizeApplyTimer.stop()

        config['WINDOW SIZE'] = {'width' : str(mw.width()), 'height' : str(mw.height())}

        saveConfig()


    def closeEvent(self, a0: qtg.QCloseEvent) -> None:

        if not config['OPTIONS'].getboolean('shutdown app on close'):
        # Trigger the "openClose_Pressed" function of the trayMenu (assuming trayMenu is an instance)

            trayMenu.openClose_Pressed()

            a0.ignore()
        else:
            # Save data before exiting the application
            self.saveData()
            app.exit()


    def resizeEvent(self, a0: qtg.QResizeEvent) -> None:

        if not self.windowSizeApplyTimer.isActive():
        # Start the window size apply timer if it is not active

            self.windowSizeApplyTimer.start(1000)
            
        # Call the base class's resizeEvent
        return super().resizeEvent(a0)

class trayMen(qtw.QMenu):
    def __init__(self):
        super(trayMen, self).__init__()

        self.setObjectName('System Tray')
        # Determine the label for the open/close button based on a configuration option

        openOrClose = 'Close' if config['OPTIONS'].getboolean('show on startup') else 'Open'
        # Create the open/close button QAction and connect it to the openClose_Pressed method

        self.openCloseButton = qtw.QAction(openOrClose)
        self.openCloseButton.triggered.connect(lambda: self.openClose_Pressed())
        # Create the quit application button QAction and connect it to the shutdownApp method
        
        self.quitAppButton = qtw.QAction("Shut Down")
        self.quitAppButton.triggered.connect(lambda: self.shutdownApp())
        
        # Add the actions (buttons) to the menu
        self.addAction(self.openCloseButton)
        self.addAction(self.quitAppButton)

    def shutdownApp(self):
        # Save data before shutting down the application
        mw.saveData()
        app.quit()

    def openClose_Pressed(self):

        if self.openCloseButton.text() == 'Close':
            # If the open/close button text is 'Close' Change the button text to 'Open'
            self.openCloseButton.setText('Open')
            # Set the main window (mw) to be invisible
            
            mw.setVisible(False)
        else:
            # If the open/close button text is not 'Close' Change the button text to 'Close'
            self.openCloseButton.setText('Close')
            mw.setVisible(True)


class UpdateAlert(qtw.QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setWindowTitle('Genshin Stopwatch: New Version Update!')
        self.setWindowIcon(qtg.QIcon(icon_path))

        layout = qtw.QVBoxLayout()

        self.message = qtw.QLabel(self, text=f'The latest update {version_check} has been released! Would you like to install it?')
        layout.addWidget(self.message)

        self.checkBox = qtw.QCheckBox(self, text='Do not automatically check for updates')
        self.checkBox.clicked.connect(lambda: self.checkBoxClicked())
        layout.addWidget(self.checkBox)

        self.buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.No
        self.buttonBox = qtw.QDialogButtonBox(self.buttons, self)
        self.buttonBox.accepted.connect(lambda: webbrowser.open_new_tab('https://github.com/Wolfmyths/Genshin-Stopwatch/releases/latest'))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
    
    def checkBoxClicked(self) -> None:
        if self.checkBox.isChecked():
            config['OPTIONS']['checkVersionOnStartup'] = 'False'
        else:
            config['OPTIONS']['checkVersionOnStartup'] = 'True'
        
        saveConfig()



if __name__ == '__main__':
    import sys

    ### ENVIRONMENT PATHS AND STYLEMANAGER INIT ###
    styles = StyleManager()

    # Loading paths, using `os.curdir` instead of `os.dirname(__file__)` because the file dir is in a temp dir
    config_path = os.path.join(os.path.abspath(os.curdir), 'config.ini')
    saveFile_path = os.path.join(os.path.abspath(os.curdir), 'save.txt')
    icon_path = os.path.join(os.path.abspath(os.curdir), 'icon.ico')

    config = ConfigParser()
    config.read(config_path)

    def saveConfig():
        with open(config_path, 'w') as f:
            config.write(f)

    ### INIT NOTIFICATIONS
    # Initialize notification icon
    notifyAsset: AppriseAsset = AppriseAsset(image_path_mask=icon_path, default_extension='.ico', app_id='Genshin Stopwatch', app_desc='Stopwatch has finished')

    # Initialize notification and add Notification icon
    notify: Apprise = Apprise(asset=notifyAsset)

    # Adding possible platforms notification object should use to send
    notify.add(('windows://', 'macosx://', 'gnome://', 'dbus://'))
    
    ### APPLICATION INIT ###
    # Create a QApplication instance
    app: qtw.QApplication = qtw.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(styles.getStyleSheet('app'))

    ### VERSION DEFINING###
    # Client Version
    version = '1.5.4'

    # Getting the latest version
    try:
        # Parsed to remove the "V" in the tag
        version_check: str = requests.get('https://api.github.com/repos/Wolfmyths/Genshin-Stopwatch/releases/latest').json()['tag_name'][1:]
    except Exception as e:
        print(e)

    ### WINDOW & SYSTEM TRAY INIT ###
    # Create an instance of the 'window' class
    mw = window()

    # Initialize window
    mw.setWindowTitle(f'Genshin Stopwatch V{version}')
    mw.setWindowIcon(qtg.QIcon(icon_path))
    mw.show() if config['OPTIONS'].getboolean('show on startup') else mw.hide()

    tray: qtw.QSystemTrayIcon = qtw.QSystemTrayIcon()
    tray.setIcon(qtg.QIcon(icon_path))
    tray.setToolTip('Genshin Stopwatch')
    tray.setVisible(True)

    trayMenu: qtw.QMenu = trayMen()

    tray.setContextMenu(trayMenu)

    app.exec_()
