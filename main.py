import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt, QPoint, QTimer

import datetime
import json

from win10toast import ToastNotifier



class Settings:
    
    def __init__(self):
        self.settings = self.loadSettings()

    def getSettings(self) -> dict:
        return self.settings

    def loadSettings(self) -> dict:
        with open('settings.json', 'r+') as f:
            data = json.load(f)

            return data
        
    @staticmethod
    def saveSettings(updatedSettings: dict):
        with open('settings.json', 'r+') as f:
            f.seek(0)
            f.truncate()
            json.dump(updatedSettings, f, indent=4)

class addTimer(qtw.QDockWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setWindowTitle('Add Timer')
        self.setObjectName('addTimerDockWidget')
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetClosable)

        self.setStyleSheet(
            '''
            
            QLabel, QPushButton{
                font-size: 18px;
            }

            ''')

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
                'durations': ['Nothing Selected']
            }, 

            'Parametric Transformer': {
                'durations': ['7 Days']
            }, 

            'Respawns': {
                'durations': ['12 Hours', '1 Day', '2 Days', '3 Days']
            },

            'Expedition': {
                'durations': ['4 Hours', '8 Hours', '12 Hours', '20 Hours']
            },

            'Teapot Gardening/Construction': {
                'durations': ['12 Hours', '14 Hours', '16 Hours', '70 Hours']
            },

            'Realm Currency': {
                'durations': ['Bare-Bones (0, 4/hr)', 'Humble Abode (>2k, 8/hr)', 'Cozy (>3k, 12/hr)', 'Queen-Size (>4.5k, 16/hr)', 'Elegant (>6k, 20/hr)', 'Exquisite (>8k, 22/hr)', 'Extradordinary (>10k, 24/hr)', 'Stately (>12k, 26/hr)', 'Luxury (>15k, 28/hr)', 'Fit for a king (>20k, 30/hr)']
            },

            'Realm Companionship XP': {
                'durations' : ['0 - 2999 (2/hr)', '3000 - 5999 (3/hr)', '6000 - 11999 (4/hr)', '12000+ (5/hr)']
            },

            'Fishing': {
                'durations': ['1 Day', '3 Days']
            },

            'Other': {
                'durations': ['4 Hours', '8 Hours', '12 Hours', '14 Hours', '16 Hours', '20 Hours', '1 Day', '2 Days', '3 Days', '7 Days']
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

        self.rCLevelLabel = qtw.QLabel('Realm Trust Level (1-10):')
        self.rCLevelLabel.setObjectName('rCLevelLabel')
        self.rCLevelLineEdit = qtw.QLineEdit()
        self.rCLevelLineEdit.setObjectName('rCLevelLineEdit')

        self.formLayout.addRow(self.rCLevelLabel, self.rCLevelLineEdit)

        # Custom Duration Hours Row (Hidden by default, see show/hide events)

        self.customDurationLabel = qtw.QLabel('Custom Duration (Amount of Hours):')
        self.customDurationLabel.setObjectName('customDurationLabel')
        self.customDurationLineEdit = qtw.QLineEdit()
        self.customDurationLineEdit.setObjectName('customDurationLineEdit')

        self.formLayout.addRow(self.customDurationLabel, self.customDurationLineEdit)

        # Custom Duration Minutes Row (Hidden by default, see show/hide events)

        self.customDurationLabelMinutes = qtw.QLabel('Custom Duration (Amount of Minutes):')
        self.customDurationLabelMinutes.setObjectName('customDurationLabelMinutes')
        self.customDurationLineEditMinutes = qtw.QLineEdit()
        self.customDurationLineEditMinutes.setObjectName('customDurationLineEditMinutes')

        self.formLayout.addRow(self.customDurationLabelMinutes, self.customDurationLineEditMinutes)

        # Name Row
        self.nameLabel = qtw.QLabel('Name (Optional):')
        self.nameLineEdit = qtw.QLineEdit()

        self.formLayout.addRow(self.nameLabel, self.nameLineEdit)

        self.colorsDict = {

            'Cryo'   :'#37AA9C',
            'Dendro' :'#32B85C',
            'Fire'   :'#AB413F',
            'Water'  :'#3F7EAB',
            'Geo'    :'#F7A936',
            'Electro':'#8156E3',
            'Anemo'  :'#60FD75'

            }

        # Color Row
        self.outlineColorLabel = qtw.QLabel('Border Color:')
        self.outlineColorDropDown = qtw.QComboBox()
        self.outlineColorDropDown.setFocusPolicy(Qt.NoFocus)
        self.outlineColorDropDown.addItems([x for x in self.colorsDict.keys()])

        self.formLayout.addRow(self.outlineColorLabel, self.outlineColorDropDown)

        # Button
        self.startTimerButton = qtw.QPushButton('Start Timer')
        self.startTimerButton.clicked.connect(lambda: self.startStopWatch())
        verticalLayout.addWidget(self.startTimerButton, alignment=Qt.AlignTop)

        self.setWidget(self.centralFrame)
    
    def hideRealmCurrency(self):

            self.rCLevelLabel.hide()
            self.rCLevelLineEdit.hide()

    def showRealmCurrency(self):

        self.rCLevelLabel.show()
        self.rCLevelLineEdit.show()

    def hideCustom(self):

        self.customDurationLabel.hide()
        self.customDurationLineEdit.hide()

        self.customDurationLabelMinutes.hide()
        self.customDurationLineEditMinutes.hide()

    def showCustom(self):

        self.customDurationLabel.show()
        self.customDurationLineEdit.show()

        self.customDurationLabelMinutes.show()
        self.customDurationLineEditMinutes.show()
    
    def hideNormalDurations(self):

        self.durationLabel.hide()
        self.durationDropDown.hide()
    
    def showNormalDurations(self):

        self.durationLabel.show()
        self.durationDropDown.show()
    
    def dropDownSelected(self, topic: str):
        
        selectedTopic = self.topicSelectionDict[topic]['durations']

        self.durationDropDown.clear()

        if topic == 'Realm Currency':

            self.hideCustom()

            self.durationLabel.setText('Realm Status:')

            self.showRealmCurrency()
            self.durationDropDown.addItems(selectedTopic)
        
        elif topic == 'Realm Companionship XP':

            self.hideCustom()

            self.durationLabel.setText('Adeptal Energy:')
            self.durationDropDown.addItems(selectedTopic)

            self.showRealmCurrency()

        elif topic == 'Custom':
            
            self.hideNormalDurations()

            self.hideRealmCurrency()

            self.showCustom()

        else:

            self.hideCustom()
            self.hideRealmCurrency()

            self.durationLabel.setText('Duration:')

            if self.durationLabel.isHidden():

                self.showNormalDurations()

            self.durationDropDown.addItems(selectedTopic)
            
    
    def startStopWatch(self):
        timeObject = self.topicDropDown.currentText()

        color = self.colorsDict[self.outlineColorDropDown.currentText()]

        hours: int = 0
        minutes: int = 0
        
        if timeObject == 'Realm Currency':

            duration: str = self.durationDropDown.currentText()
            duration = duration.split(',')
            duration = duration[-1]

            duration: int = int(duration.split('/')[0])

            try:

                maxStorage: int = self.rCLevelValues[self.rCLevelLineEdit.text()]

            except KeyError:
                return self.rCLevelLineEdit.setText('Error: Invalid Input')
            
            duration: str = str(round(maxStorage/duration, 2)).split('.')

            hours = int(duration[0])
            minutes = round(float(f'0.{duration[1]}') * 60)
        
        elif timeObject == 'Realm Companionship XP':

            if int(self.rCLevelLineEdit.text()) not in range(1, 11):
                return self.rCLevelLineEdit.setText('Error: Invalid Input')

            duration: str = self.durationDropDown.currentText()
            duration = duration.split('/')

            duration: int = int(duration[0][-1])

            maxStorage = int(self.rCLevelLineEdit.text()) * 50

            duration: str = str(round(maxStorage/duration, 2)).split('.')

            hours = int(duration[0])
            minutes = round(float(f'0.{duration[1]}') * 60)

        elif timeObject == 'Custom':

            hours: str = self.customDurationLineEdit.text()
            minutes: str = self.customDurationLineEditMinutes.text()
            
            try:
                hours = abs(int(hours))
                minutes = abs(int(minutes))
            except ValueError:
                return self.customDurationLineEdit.setText('Error: Whole Numbers Only')

        else:

            duration: str = self.durationDropDown.currentText()

            if duration == 'Nothing Selected':
                return
            
            duration = duration.split()

            if duration[1] == 'Days' or duration[1] == 'Day':
                duration = int(duration[0]) * 24
            else:
                duration = int(duration[0])


            hours = duration

        duration = datetime.timedelta(hours=hours, minutes=minutes)

        nameText = self.nameLineEdit.text()
        name = nameText if len(nameText) > 0 else timeObject

        centralWidget_: centralWidget = self.parent().findChild(qtw.QWidget, 'central widget')

        centralWidget_.addStopWatch(timeObject, duration, name, duration, color)
    
    
    def hideEvent(self, a0: qtg.QHideEvent) -> None:

        if self.parent().isHidden():
            a0.ignore()

        else:

            parent: qtw.QMainWindow = self.parent()
            toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
            addtimerButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'addTimerButton')

            addtimerButton.setChecked(False)

            if not parent.isMinimized():

                mw.dockWidgetOptions.applySettings(Add_timer_open_on_startup=False)

        return super().hideEvent(a0)
    
    def showEvent(self, a0: qtg.QShowEvent) -> None:

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        addtimerButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'addTimerButton')

        addtimerButton.setChecked(True)

        self.dropDownSelected(self.topicDropDown.currentText())

        if not parent.isMinimized():

            mw.dockWidgetOptions.applySettings(Add_timer_open_on_startup=True)

        return super().showEvent(a0)
    
class optionsDock(qtw.QDockWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setWindowTitle('Options')
        self.setObjectName('optionsDockWidget')
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetClosable)

        self.setStyleSheet(
            '''
            
            QLabel, QPushButton{
                font-size: 18px;
            }

            QCheckBox::indictator{
                width: 40px;
                length: 40px;
            }

            ''')

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

        getSettings: dict = Settings().getSettings()

        # Checkbox
        self.appOnCloseCheckbox = qtw.QCheckBox()
        self.appOnCloseCheckbox.setChecked(getSettings['Shutdown_app_on_close'])
        self.appOnCloseCheckbox.setToolTip('The app will close and not run in the background.')
        # Form Row
        self.formLayout.addRow('Shutdown app on close: ', self.appOnCloseCheckbox)

        # Checkbox
        self.showOnOpenCheckbox = qtw.QCheckBox()
        self.showOnOpenCheckbox.setChecked(getSettings['Show_on_startup'])
        self.showOnOpenCheckbox.setToolTip('Program will automatically show or hide when starting.')
        # Form Row
        self.formLayout.addRow('Show on app start: ', self.showOnOpenCheckbox)

        # Checkbox
        self.notifyCheckbox = qtw.QCheckBox()
        self.notifyCheckbox.setChecked(getSettings['Desktop_notifications'])
        self.notifyCheckbox.setToolTip('A windows desktop notification will appear when a stopwatch finishes.')
        # Form Row
        self.formLayout.addRow('Desktop notifications: ', self.notifyCheckbox)

        # Button
        self.applyButton = qtw.QPushButton('Apply')
        self.applyButton.clicked.connect(lambda: self.applySettings(all=None))
        verticalLayout.addWidget(self.applyButton, alignment=Qt.AlignTop)

        self.setWidget(self.centralFrame)
    
    def applySettings(self, **kwargs):

        newSettings: dict = Settings().getSettings()

        for settingName, value in kwargs.items():

            if settingName == 'all':

                newSettings: dict = {
                    "Shutdown_app_on_close": self.appOnCloseCheckbox.isChecked(),
                    "Desktop_notifications": self.notifyCheckbox.isChecked(),
                    "Options_open_on_startup" : self.isHidden(),
                    "Add_timer_open_on_startup" : self.parent().findChild(qtw.QDockWidget, 'addTimerDockWidget').isHidden(),
                    "Window_size" : {'width': self.parent().width(), 'height': self.parent().height()},
                    "Show_on_startup" : self.showOnOpenCheckbox.isChecked()
                    }
                
                break

            else:

                newSettings[settingName] = value
        
        Settings.saveSettings(newSettings)
    
    def hideEvent(self, a0: qtg.QHideEvent) -> None:

        if self.parent().isHidden():
            a0.ignore()
        
        else:
        
            parent: qtw.QMainWindow = self.parent()
            toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
            optionsButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'optionsButton')

            optionsButton.setChecked(False)

            self.applySettings(Options_open_on_startup=False)

        return super().hideEvent(a0)
    
    def showEvent(self, a0: qtg.QShowEvent) -> None:

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        optionsButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'optionsButton')

        optionsButton.setChecked(True)

        self.applySettings(Options_open_on_startup=True)
        return super().showEvent(a0)


class toolbar(qtw.QToolBar):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setFloatable(False)
        self.setMovable(False)

        self.layout().setSpacing(20)

        self.setStyleSheet(
            '''
            QToolButton{
                font-size: 18px;
            }
            ''')

        setting: dict = Settings().getSettings()

        # Add Timer Button
        self.addTimerButton = qtw.QAction('Add Timer', self)
        self.addTimerButton.setObjectName('addTimerButton')
        self.addTimerButton.setCheckable(True)
        self.addTimerButton.setChecked(setting['Add_timer_open_on_startup'])
        self.addTimerButton.triggered.connect(lambda: self.button_Clicked('addTimerDockWidget', self.addTimerButton.isChecked() ) )
        self.addAction(self.addTimerButton)

        # Options Button
        self.optionsButton = qtw.QAction('Options', self)
        self.optionsButton.setObjectName('optionsButton')
        self.optionsButton.setCheckable(True)
        self.optionsButton.setChecked(setting['Options_open_on_startup'])
        self.optionsButton.triggered.connect(lambda: self.button_Clicked('optionsDockWidget', self.optionsButton.isChecked() ) )
        self.addAction(self.optionsButton)
    
    def button_Clicked(self, dockObjectName: str, buttonisChecked: bool):

        addDockWidget: qtw.QDockWidget = self.parent().findChild(qtw.QDockWidget, dockObjectName)

        if buttonisChecked:

            addDockWidget.show()
            
        else:

            addDockWidget.hide()


class centralWidget(qtw.QWidget):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setStyleSheet(
            '''
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

            ''')

        self.setObjectName('central widget')
        self.scrollAreaLayout = qtw.QHBoxLayout(self)
        self.scrollAreaLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout = qtw.QVBoxLayout()

        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setContentsMargins(0,0,0,0)

        self.scrollAreaWidgetContents = qtw.QWidget()
        self.scrollAreaWidgetContents.setContentsMargins(0,0,0,0)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.addWidget(self.scrollArea)

    def addStopWatch(self, timeObject: str, duration: datetime.timedelta, name: str, startDuration: datetime.timedelta, color: str, notepadContents: str = '', index: int | None = None) -> None:
        
        self.frame = qtw.QFrame(self.scrollAreaWidgetContents)
        self.frame.setStyleSheet('''

            QFrame {{
                border: 3px solid {0};
                border-radius: 10px;
                background-color: #333F44;
            }}

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

            

        '''.format(color))
        id_ = str(id(self.frame))
        self.frame.setObjectName(id_)
        self.frame.setMaximumHeight(500)

        parent: qtw.QFrame = self.findChild(qtw.QFrame, id_)

        parent.setProperty('border-color', color)

        startDurationDays = int(startDuration.__str__().split(':')[0].split()[0])
        startDurationMinutes = int(startDuration.__str__().split(':')[1].split(':')[0])

        if len(str(startDurationMinutes)) == 1:
            startDurationMinutes = str(startDurationMinutes) + '0'

        if startDuration >= datetime.timedelta(hours=24): # startDuration gives the days but not in total hours, needed so that loadSaveData() can work
    
            parent.setProperty('originalDuration', f'{startDurationDays * 24}:{startDurationMinutes}:00')

        else:
            parent.setProperty('originalDuration', startDuration)
    

        frameLayout = qtw.QGridLayout()
        frameLayout.setContentsMargins(20,20,20,20)

        nameLabel = qtw.QLabel(name, self.frame)
        nameLabel.setObjectName(f'{id_}nameLabel')
        nameLabel.setStyleSheet('font-size: 60px;')
        frameLayout.addWidget(nameLabel, 0, 0, alignment=Qt.AlignTop)

        deleteButton = qtw.QPushButton('X', self.frame)
        deleteButton.setMinimumSize(40,40)
        deleteButton.clicked.connect(lambda: self.findChild(qtw.QFrame, id_).deleteLater())
        frameLayout.addWidget(deleteButton, 0, 2, alignment=Qt.AlignRight)

        countDown = qtw.QLabel('00:00:00', self.frame)
        countDown.setObjectName(f'{id_}CountDownLabel')
        countDown.setStyleSheet('font-size: 70px;')
        frameLayout.addWidget(countDown, 1, 0, 1, 3, alignment=Qt.AlignCenter)

        resetButton = qtw.QPushButton('Reset Timer', self.frame)
        resetButton.setObjectName(f'{id_}resetButton')
        resetButton.setStyleSheet('font-size: 25px;')
        resetButton.setMinimumSize(120,60)
        resetButton.setMaximumSize(240,60)
        resetButton.clicked.connect(lambda: self.resetTimer(timeObject, name, startDuration, id_, color, notes=notepad.toPlainText()))
        frameLayout.addWidget(resetButton, 2,0, alignment=Qt.AlignBottom)

        finishedDate = datetime.datetime.now() + duration
        finishedDateLabel = qtw.QLabel(f'Finished on: {finishedDate.strftime("%B %d @ %I:%M %p")}')
        finishedDateLabel.setObjectName(f'{id_}finishedDateLabel')
        frameLayout.addWidget(finishedDateLabel, 2, 1, alignment=Qt.AlignCenter)

        notepad = qtw.QTextEdit(self.frame)
        notepad.setPlaceholderText('Notes go here')
        notepad.setText(notepadContents)
        notepad.setMinimumSize(300, 100)
        notepad.setMaximumSize(400, 200)
        notepad.anchorAt(QPoint(0,0))
        notepad.setStyleSheet(
            '''
            background: #1A1A1B;
            color: #94F3E4;
            font-size: 24px;
            border: none;
            ''')
        frameLayout.addWidget(notepad, 2, 2)

        self.frame.setLayout(frameLayout)

        if index:
            self.verticalLayout.insertWidget(index, self.frame)
        else:
            self.verticalLayout.addWidget(self.frame)

        self.frame.show()


        currentTime = datetime.datetime.today()

        finishedTime = currentTime + duration

        parent.setProperty('finishedTime', datetime.datetime.strftime(finishedTime, '%Y-%m-%d %H:%M:%S'))

        difference =  finishedTime - currentTime


        resetButton: qtw.QPushButton = parent.findChild(qtw.QPushButton, f'{id_}resetButton')
        countDownLabel: qtw.QLabel = parent.findChild(qtw.QLabel, f'{id_}CountDownLabel')

        zero = datetime.timedelta(days=0, hours=0, seconds=0)
        one = datetime.timedelta(seconds=1)

        QTimer_ = QTimer(parent)
        QTimer_.setObjectName(f'{id_}QTimer')

        n = ToastNotifier()

        def countDownTimer(self: qtw.QWidget, difference: datetime) -> None:

            try:

                difference -= one

                if difference > zero:
                    
                    countDownLabel.setText(str(difference))

                    QTimer_.singleShot(1000, lambda: countDownTimer(self, difference))

                else:
                    countDownLabel.setText('00:00:00')
                    countDownLabel.setProperty('finished', "true")
                    parent.style().polish(countDownLabel)

                    getsettings: dict = Settings().getSettings()
                    if getsettings['Desktop_notifications']:

                        n.show_toast('Stopwatch Finished', f"{name} has finished!", 'icon.ico', 10, True)

                
            except RuntimeError: # If timer is deleted, will traceback a runtime error
                return

        
        countDownTimer(self, difference)
            
    
    def resetTimer(self, timeObject: str, name: str, startDuration: datetime.timedelta, id: str, color: str, notes: str = ''):
        
        frame: qtw.QFrame = self.findChild(qtw.QFrame, id)

        index = self.verticalLayout.indexOf(frame)

        self.findChild(qtw.QFrame, id).deleteLater()

        currentTime = datetime.datetime.today()

        difference =  (currentTime + startDuration) - currentTime

        self.addStopWatch(timeObject, difference, name, startDuration, color, notepadContents=notes, index=index)

        

class window(qtw.QMainWindow):
    def __init__(self):
        super(window, self).__init__()

        self.setting: dict = Settings().getSettings()

        # Application Stylesheet
        self.setStyleSheet(
            '''
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
        )

        self.toolBar = toolbar(self)
        self.addToolBar(self.toolBar)

        self.central = centralWidget(self)
        self.setCentralWidget(self.central)

        self.dockWidgetAddTimer = addTimer(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetAddTimer)
        self.dockWidgetAddTimer.setVisible(self.setting['Add_timer_open_on_startup'])

        self.dockWidgetOptions = optionsDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetOptions)
        self.dockWidgetOptions.setVisible(self.setting['Options_open_on_startup'])

        # So the resize event doesn't spam the save window function (see function sizeApplyTimerTimeout)
        self.windowSizeApplyTimer = QTimer(self)
        self.windowSizeApplyTimer.setObjectName('windowSizeApplyTimer')
        self.windowSizeApplyTimer.timeout.connect(lambda: self.sizeApplyTimerTimeout())

        self.resize(self.setting["Window_size"]['width'], self.setting["Window_size"]['height'])

        self.loadSaveData()

    def loadSaveData(self):
        with open('save.txt', 'r+') as fhand:

            for line in fhand:

                if line.isspace():
                    continue

                elif line.startswith('Name:'):
            
                    name = line.split('Name: ')[1]
                    name = name.strip() # For some reason it keeps the linebreak that saveData() created, making an extra linebreak

                elif line.startswith('Time Finished: '):

                    finishedTime = line.split()[2:]

                    finishedTime = f'{finishedTime[0]} {finishedTime[1].split(".")[0]}' # The '.split(".")[0]' gets rid of the milliseconds

                    finishedTime = datetime.datetime.strptime(finishedTime, '%Y-%m-%d %H:%M:%S')

                    finishedTime = finishedTime - datetime.datetime.today().replace(microsecond=0)

                elif line.startswith('Time Original Duration: '):

                    originalDuration = ''.join(line.split()[3:])

                    originalDuration = datetime.timedelta(hours= int(originalDuration.split(':')[0]), minutes= int(originalDuration.split(':')[1]))
                
                elif line.startswith('Border Color:'):

                    color = line.split()[2]

                elif line.startswith('Notes: '):
                    notes = ''.join(line.split('Notes: ')[1:]).strip()

                    self.central.addStopWatch(name, finishedTime, name, originalDuration, color, notepadContents=notes)
                    
    def saveData(self):
        
        with open('save.txt', 'w+') as fhand:

            string = ''''''

            for qtObject in mw.central.findChildren(qtw.QFrame):
                
                if len(qtObject.objectName()) == 13: # Length of a stopwatch's name which is their id() value
                    
                    objectName: str = qtObject.objectName()

                    string += (
                    f'Name: {qtObject.findChild(qtw.QLabel, f"{objectName}nameLabel").text()}\n'
                    f'Time Finished: {qtObject.property("finishedTime")}\n'
                    f'Time Original Duration: {qtObject.property("originalDuration")}\n'
                    f'Border Color: {qtObject.property("border-color")}\n'
                    f'Notes: {qtObject.findChild(qtw.QTextEdit).toPlainText()}\n'
                    )

                    # Makes the save file easier to read in between stopwatches
                    string += '\n'

            fhand.seek(0)

            fhand.truncate()

            fhand.write(string)
    
    def sizeApplyTimerTimeout(self):

        self.windowSizeApplyTimer.stop()
        self.dockWidgetOptions.applySettings(Window_size={"width": self.width(), "height": self.height()})


    def closeEvent(self, a0: qtg.QCloseEvent) -> None:

        getsettings: dict = Settings().getSettings()
        
        if not getsettings['Shutdown_app_on_close']:

            trayMenu.openClose_Pressed()

            a0.ignore()
        else:
            app.exit()

    
    def resizeEvent(self, a0: qtg.QResizeEvent) -> None:

        if not self.windowSizeApplyTimer.isActive():

            self.windowSizeApplyTimer.start(1000)
        
        return super().resizeEvent(a0)
    
class trayMen(qtw.QMenu):
    def __init__(self):
        super(trayMen, self).__init__()

        self.setObjectName('System Tray')

        openOrClose = 'Close' if Settings().getSettings()['Show_on_startup'] else 'Open'

        self.openCloseButton = qtw.QAction(openOrClose)
        self.openCloseButton.triggered.connect(lambda: self.openClose_Pressed())
        self.quitAppButton = qtw.QAction("Shut Down")
        self.quitAppButton.triggered.connect(app.quit)

        self.addAction(self.openCloseButton)
        self.addAction(self.quitAppButton)

    def openClose_Pressed(self):

        if self.openCloseButton.text() == 'Close':
            self.openCloseButton.setText('Open')
            mw.setVisible(False)
        else:
            self.openCloseButton.setText('Close')
            mw.setVisible(True)


if __name__ == '__main__':
    import sys

    app: qtw.QApplication = qtw.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    mw = window()

    version = '1.3'
    mw.setWindowTitle(f'Genshin Stopwatch V{version}')
    mw.setWindowIcon(qtg.QIcon('icon.ico'))
    mw.show() if Settings().getSettings()['Show_on_startup'] else mw.hide()

    tray: qtw.QSystemTrayIcon = qtw.QSystemTrayIcon()
    tray.setIcon(qtg.QIcon('icon.ico'))
    tray.setToolTip('Genshin Impact Stopwatch')
    tray.setVisible(True)

    trayMenu = trayMen()

    tray.setContextMenu(trayMenu)

    app.exec_()

    # After Program Ends
    mw.saveData()

# Color Pallete
# Background: #1A1A1B 
# Frame Background: #333F44
# Foreground: #37AA9C
# Text: #94F3E4
# Alt Text: #FCB3FC
