import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt, QPoint, QTimer

import datetime
from configparser import ConfigParser

from win10toast import ToastNotifier

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

        self.rCRateValuesDict = {k:v for (k,v) in zip(self.topicSelectionDict['Realm Currency']['durations'], (4, 8, 16, 20, 22, 24, 26, 28, 30))}

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

        self.lineEditLabel1.hide()
        self.lineEdit1.hide()

    def showRealmCurrency(self):

        self.lineEditLabel1.show()
        self.lineEdit1.show()

    def hideCustom(self):

        self.lineEditLabel1.hide()
        self.lineEdit1.hide()

        self.lineEditLabel2.hide()
        self.lineEdit2.hide()

        self.lineEditLabel3.hide()
        self.lineEdit3.hide()

    def showCustom(self):

        self.lineEditLabel1.show()
        self.lineEdit1.show()

        self.lineEditLabel2.show()
        self.lineEdit2.show()

        self.lineEditLabel3.show()
        self.lineEdit3.show()
    
    def hideNormalDurations(self):

        self.durationLabel.hide()
        self.durationDropDown.hide()
    
    def showNormalDurations(self):

        self.durationLabel.show()
        self.durationDropDown.show()
    
    def dropDownSelected(self, topic: str):
        
        selectedTopic = self.topicSelectionDict[topic]['durations']

        self.durationDropDown.clear()

        match topic:

            case 'Realm Currency':

                self.hideCustom()

                self.showNormalDurations()
                self.durationLabel.setText('Realm Status:')
                self.durationDropDown.addItems(selectedTopic)

                self.showRealmCurrency()
                self.lineEditLabel1.setText('Realm Trust Level (1-10)')
        
            case 'Realm Companionship XP':

                self.hideCustom()

                self.showNormalDurations()
                self.durationLabel.setText('Adeptal Energy:')
                self.durationDropDown.addItems(selectedTopic)
                
                self.showRealmCurrency()
                self.lineEditLabel1.setText('Realm Trust Level (1-10)')
        
            case 'Stamina':

                self.hideCustom()
                self.hideRealmCurrency()
                self.hideNormalDurations()

                self.lineEditLabel1.show()
                self.lineEditLabel1.setText('Current Stamina')
                self.lineEdit1.show()

            case 'Custom':
                
                self.hideNormalDurations()

                self.hideRealmCurrency()

                self.showCustom()
                self.lineEditLabel1.setText('Days:')
                self.lineEditLabel2.setText('Hours:')
                self.lineEditLabel3.setText('Minutes:')

            case _:

                self.hideCustom()
                self.hideRealmCurrency()

                self.durationLabel.setText('Duration:')

                if self.durationLabel.isHidden():

                    self.showNormalDurations()

                self.durationDropDown.addItems(selectedTopic)
            
    
    def startStopWatch(self):
        timeObject = self.topicDropDown.currentText()

        color = self.colorsDict[self.outlineColorDropDown.currentText()]

        days: int = 0
        hours: int = 0
        minutes: int = 0
        
        percentToMinutes: callable[[str], str] = lambda rate: round( (float(rate) / 100) * 60 )
        calculateDuration: callable[[int, int], str] = lambda maxStorage, rate: str(round(maxStorage/rate, 2)).split('.')
        
        match timeObject:
            
            case 'Realm Currency':

                try:
                    if int(self.lineEdit1.text()) not in range(1, 11):
                        raise ValueError 
                except ValueError:
                    return self.lineEdit1.setText('Error: Invalid Input')
                
                maxStorage: int = self.rCLevelValues[self.lineEdit1.text()]

                rate: str = self.durationDropDown.currentText()
                duration = self.rCRateValuesDict[rate]
                
                duration: list[str] = calculateDuration(maxStorage, duration)

                hours = int(duration[0])
                minutes = percentToMinutes(duration[1])
        
            case 'Realm Companionship XP':

                try:
                    if int(self.lineEdit1.text()) not in range(1, 11):
                        raise ValueError 
                except ValueError:
                    return self.lineEdit1.setText('Error: Invalid Input')
                
                maxStorage = int(self.lineEdit1.text()) * 50

                rate: str = self.durationDropDown.currentText()
                duration = self.rCFriendshipValuesDict[rate]

                duration = calculateDuration(maxStorage, duration)

                hours = int(duration[0])
                minutes = percentToMinutes(duration[1])

            case 'Custom':

                days: str|int = self.lineEdit1.text() if self.lineEdit1.text().isdigit() else 0
                hours: str|int = self.lineEdit2.text() if self.lineEdit2.text().isdigit() else 0
                minutes: str|int = self.lineEdit3.text() if self.lineEdit3.text().isdigit() else 0
                
                days = abs(int(days))
                hours = abs(int(hours))
                minutes = abs(int(minutes))

            case 'Stamina':

                amountOfStamina: str = self.lineEdit1.text()
                print(amountOfStamina)

                if not amountOfStamina.isdigit():
                    return self.lineEdit1.setText('Invalid Input')
                else:

                    amountOfStamina = int(amountOfStamina)
                    
                    minutes = (160 - amountOfStamina) * 8

            case _:

                duration: str = self.durationDropDown.currentText()

                if duration == 'Nothing Selected':
                    return
                
                duration = duration.split()

                if duration[1] == 'Days' or duration[1] == 'Day':
                    duration = int(duration[0]) * 24
                else:
                    duration = int(duration[0])


                hours = duration

        duration = datetime.timedelta(days=days, hours=hours, minutes=minutes)

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

                config['QOL']['addtimer open on startup'] = 'False'
                
                saveConfig()

        return super().hideEvent(a0)
    
    def showEvent(self, a0: qtg.QShowEvent) -> None:

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        addtimerButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'addTimerButton')

        addtimerButton.setChecked(True)

        self.dropDownSelected(self.topicDropDown.currentText())

        if not parent.isMinimized():

            config['QOL']['addtimer open on startup'] = 'True'
            
            saveConfig()

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

        # Checkbox
        self.appOnCloseCheckbox = qtw.QCheckBox()
        self.appOnCloseCheckbox.setChecked(config['OPTIONS'].getboolean('shutdown app on close'))
        self.appOnCloseCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.appOnCloseCheckbox.setToolTip('The app will close and not run in the background.')
        # Form Row
        self.formLayout.addRow('Shutdown app on close: ', self.appOnCloseCheckbox)

        # Checkbox
        self.showOnOpenCheckbox = qtw.QCheckBox()
        self.showOnOpenCheckbox.setChecked(config['OPTIONS'].getboolean('show on startup'))
        self.showOnOpenCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.showOnOpenCheckbox.setToolTip('Program will automatically show or hide when starting.')
        # Form Row
        self.formLayout.addRow('Show on app start: ', self.showOnOpenCheckbox)

        # Checkbox
        self.notifyCheckbox = qtw.QCheckBox()
        self.notifyCheckbox.setChecked(config['OPTIONS'].getboolean('desktop notifications'))
        self.notifyCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.notifyCheckbox.setToolTip('A windows desktop notification will appear when a stopwatch finishes.')
        # Form Row
        self.formLayout.addRow('Desktop notifications: ', self.notifyCheckbox)

        # Button
        self.applyButton = qtw.QPushButton('Apply')
        self.applyButton.clicked.connect(lambda: self.applySettings())
        self.applyButton.clicked.connect(lambda: self.settingChanged(False))
        verticalLayout.addWidget(self.applyButton, alignment=Qt.AlignTop)

        self.setWidget(self.centralFrame)
    
    def settingChanged(self, on: bool):

        if on:
            self.applyButton.setStyleSheet('color: yellow;')
            
        else:
            self.applyButton.setStyleSheet('color: #94F3E4;')
        
        self.applyButton.ensurePolished()
    
    def applySettings(self):

        updatedConfig = {
                            'shutdown app on close' : str(self.appOnCloseCheckbox.isChecked()),
                            'show on startup'       : str(self.showOnOpenCheckbox.isChecked()),
                            'desktop notifications' : str(self.notifyCheckbox.isChecked())
                        }

        config['OPTIONS'] = updatedConfig
        
        saveConfig()
        self.settingChanged(False)
    
    def hideEvent(self, a0: qtg.QHideEvent) -> None:

        if self.parent().isHidden():
            a0.ignore()
        
        else:
        
            parent: qtw.QMainWindow = self.parent()
            toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
            optionsButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'optionsButton')

            optionsButton.setChecked(False)

            config['QOL']['settings open on startup'] = 'False'
            
            saveConfig()

        return super().hideEvent(a0)
    
    def showEvent(self, a0: qtg.QShowEvent) -> None:

        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        optionsButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'optionsButton')

        optionsButton.setChecked(True)

        config['QOL']['settings open on startup'] = 'True'
        
        saveConfig()
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

    def addStopWatch(self, timeObject: str, duration: datetime.timedelta, name: str, startDuration: datetime.timedelta, color: str, notepadContents: str = '', index: int | None = None, save: bool = True) -> None:
        
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
        deleteButton.clicked.connect(lambda: self.deleteTimer(id_))
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

        # Index is only given when a timer is resetTimer() is called
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

                    if config['OPTIONS'].getboolean('desktop notifications'):

                        n.show_toast('Stopwatch Finished', f"{name} has finished!", 'icon.ico', 10, True)

                
            except RuntimeError: # If timer is deleted, will traceback a runtime error
                return

        
        countDownTimer(self, difference)

        if save:
            self.parent().saveData()
    
    def deleteTimer(self, id_: str):
        self.findChild(qtw.QFrame, id_).deleteLater()

        # There is a 1ms delay to call saveData() so that the deleteLater() method can finish, otherwise saveData() won't save anything
        QTimer.singleShot(1, lambda: self.parent().saveData())
    
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
        self.dockWidgetAddTimer.setVisible(config['QOL'].getboolean('addtimer open on startup'))

        self.dockWidgetOptions = optionsDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetOptions)
        self.dockWidgetOptions.setVisible(config['QOL'].getboolean('settings open on startup'))

        # So the resize event doesn't spam the save window resolution function (see sizeApplyTimerTimeout() )
        self.windowSizeApplyTimer = QTimer(self)
        self.windowSizeApplyTimer.setObjectName('windowSizeApplyTimer')
        self.windowSizeApplyTimer.timeout.connect(lambda: self.sizeApplyTimerTimeout())

        self.resize(config['WINDOW SIZE'].getint('width'), config['WINDOW SIZE'].getint('height'))

        self.loadSaveData()

    def loadSaveData(self):
        data = ConfigParser()
        data.read('save.txt')

        for timerID in data.sections():

            # Name
            name = data[timerID]['name']

            # Changing the timer's destination into a datetime type
            timeFinished = data[timerID]['time finished']
            timeFinished = datetime.datetime.strptime(timeFinished, '%Y-%m-%d %H:%M:%S')
            timeFinished = timeFinished - datetime.datetime.today().replace(microsecond=0)

            # The original duration (For resetting the timer) and changing into a timedelta type
            originalDuration = data[timerID]['time original duration'].split(':')
            originalDuration = datetime.timedelta(hours= int(originalDuration[0]), minutes= int(originalDuration[1]))

            # Border color (In hexcode format)
            borderColor = data[timerID]['border color']

            # Notes
            notes = data[timerID]['notes']



            # Remove old ID
            data.remove_section(timerID)

            # Create stopwatch
            self.central.addStopWatch(name, timeFinished, name, originalDuration, borderColor, notes, save=False)
        
        # Update the savefile (Old IDs are removed)
        with open('save.txt', 'w') as f:
            data.write(f)

        # Update the savefile (Saving new IDs created from for loop)
        self.saveData()

    def saveData(self):
        print('saving data')

        data = ConfigParser()

        for qtObject in self.central.findChildren(qtw.QFrame):

            objectName: str = qtObject.objectName()
            
            if len(objectName) == 13: # Length of a stopwatch's name which is their id() value

                data[objectName] = {
                    'name'                   : qtObject.findChild(qtw.QLabel, f"{objectName}nameLabel").text(),
                    'time finished'          : qtObject.property("finishedTime"),
                    'time original duration' : qtObject.property("originalDuration"),
                    'border color'           : qtObject.property("border-color"),
                    'notes'                  : qtObject.findChild(qtw.QTextEdit).toPlainText()
                }

        with open('save.txt', 'w') as f:
            data.write(f)
    
    def sizeApplyTimerTimeout(self):

        self.windowSizeApplyTimer.stop()
        
        config['WINDOW SIZE'] = {'width' : str(mw.width()), 'height' : str(mw.height())}
        
        saveConfig()


    def closeEvent(self, a0: qtg.QCloseEvent) -> None:
        
        if not config['OPTIONS'].getboolean('show on startup'):

            trayMenu.openClose_Pressed()

            a0.ignore()
        else:
            self.saveData()
            app.exit()

    
    def resizeEvent(self, a0: qtg.QResizeEvent) -> None:

        if not self.windowSizeApplyTimer.isActive():

            self.windowSizeApplyTimer.start(1000)
        
        return super().resizeEvent(a0)
    
class trayMen(qtw.QMenu):
    def __init__(self):
        super(trayMen, self).__init__()

        self.setObjectName('System Tray')

        openOrClose = 'Close' if config['OPTIONS'].getboolean('show on startup') else 'Open'

        self.openCloseButton = qtw.QAction(openOrClose)
        self.openCloseButton.triggered.connect(lambda: self.openClose_Pressed())
        self.quitAppButton = qtw.QAction("Shut Down")
        self.quitAppButton.triggered.connect(lambda: self.shutdownApp())

        self.addAction(self.openCloseButton)
        self.addAction(self.quitAppButton)
    
    def shutdownApp(self):
        mw.saveData()
        app.quit()

    def openClose_Pressed(self):

        if self.openCloseButton.text() == 'Close':
            self.openCloseButton.setText('Open')
            mw.setVisible(False)
        else:
            self.openCloseButton.setText('Close')
            mw.setVisible(True)


if __name__ == '__main__':
    import sys

    config = ConfigParser()
    config.read('config.ini')

    def saveConfig():
        with open('config.ini', 'w') as f:
            config.write(f)

    app: qtw.QApplication = qtw.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    mw = window()

    version = '1.4'
    mw.setWindowTitle(f'Genshin Stopwatch V{version}')
    mw.setWindowIcon(qtg.QIcon('icon.ico'))
    mw.show() if config['OPTIONS'].getboolean('show on startup') else mw.hide()

    tray: qtw.QSystemTrayIcon = qtw.QSystemTrayIcon()
    tray.setIcon(qtg.QIcon('icon.ico'))
    tray.setToolTip('Genshin Impact Stopwatch')
    tray.setVisible(True)

    trayMenu = trayMen()

    tray.setContextMenu(trayMenu)

    app.exec_()

# Color Pallete
# Background: #1A1A1B 
# Frame Background: #333F44
# Foreground: #37AA9C
# Text: #94F3E4
# Alt Text: #FCB3FC
