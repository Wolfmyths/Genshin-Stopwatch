import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt, QPoint, QTimer

import datetime

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

            'Teapot': {
                'durations': ['12 Hours', '14 Hours', '16 Hours', '70 Hours']
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

        # Custom Duration Row (Hidden by default, see show/hide events)

        self.customDurationLabel = qtw.QLabel('Custom Duration (Amount of Hours):')
        self.customDurationLabel.setObjectName('customDurationLabel')
        self.customDurationLineEdit = qtw.QLineEdit()
        self.customDurationLineEdit.setObjectName('customDurationLineEdit')

        self.formLayout.addRow(self.customDurationLabel, self.customDurationLineEdit)

        # Name Row
        self.nameLabel = qtw.QLabel('Name (Optional):')
        self.nameLineEdit = qtw.QLineEdit()

        self.formLayout.addRow(self.nameLabel, self.nameLineEdit)

        self.colorsDict = {

            'Cryo':'#37AA9C',
            'Dendro':'#32B85C',
            'Fire':'#AB413F',
            'Water':'#3F7EAB',
            'Geo':'#F7A936',
            'Electro':'#8156E3',
            'Anemo':'#60FD75'

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
    
    def dropDownSelected(self, topic: str):
        
        selectedTopic = self.topicSelectionDict[topic]['durations']

        self.durationDropDown.clear()

        if selectedTopic != 'Custom':

            self.customDurationLabel.hide()
            self.customDurationLineEdit.hide()

            if self.durationLabel.isHidden():

                self.durationLabel.show()
                self.durationDropDown.show()

            self.durationDropDown.addItems(selectedTopic)

        else:
            
            self.durationLabel.hide()
            self.durationDropDown.hide()

            self.customDurationLabel.show()
            self.customDurationLineEdit.show()
            
    
    def startStopWatch(self):
        timeObject = self.topicDropDown.currentText()

        duration: str = self.durationDropDown.currentText() if not self.durationDropDown.isHidden() else self.customDurationLineEdit.text()

        color = self.colorsDict[self.outlineColorDropDown.currentText()]
        
        if not self.durationDropDown.isHidden():

            if duration == 'Nothing Selected':
                return
            
            duration = duration.split()

            if duration[1] == 'Days' or duration[1] == 'Day':
                duration = int(duration[0]) * 24
            else:
                duration = int(duration[0])

        else:

            if not duration.isdigit():
                return self.customDurationLineEdit.setText('Error: Whole Numbers Only')
            
            duration = int(duration)



        duration = datetime.timedelta(hours=duration)

        nameText = self.nameLineEdit.text()
        name = nameText if len(nameText) > 0 else timeObject

        centralWidget_: centralWidget = self.parent().findChild(qtw.QWidget, 'central widget')

        centralWidget_.addStopWatch(timeObject, duration, name, duration, color)
    
    
    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        
        parent: qtw.QMainWindow = self.parent()
        toolbar: qtw.QToolBar = parent.findChild(qtw.QToolBar)
        addtimerButton: qtw.QAction = toolbar.findChild(qtw.QAction, 'addTimerButton')

        addtimerButton.setChecked(False)

        return super().hideEvent(a0)
    
    def showEvent(self, a0: qtg.QShowEvent) -> None:
        
        if self.topicDropDown.currentText() != 'Custom':

            self.customDurationLabel.hide()
            self.customDurationLineEdit.hide()

        return super().showEvent(a0)
    

class toolbar(qtw.QToolBar):
    def __init__(self, parent=None | qtw.QMainWindow):
        super().__init__(parent)

        self.setFloatable(False)
        self.setMovable(False)

        self.setStyleSheet(
            '''
            QToolButton{
                font-size: 18px;
            }
            ''')

        self.addTimerButton = qtw.QAction('Add Timer', self)
        self.addTimerButton.setObjectName('addTimerButton')
        self.addTimerButton.setCheckable(True)
        self.addTimerButton.setChecked(True)
        self.addTimerButton.triggered.connect(lambda: self.addTimerButton_Clicked())
        self.addAction(self.addTimerButton)
    
    def addTimerButton_Clicked(self):

        addTimerWidget: qtw.QDockWidget = self.parent().findChild(qtw.QDockWidget, 'addTimerDockWidget')
        parent: qtw.QMainWindow = self.parent()

        if self.addTimerButton.isChecked():

            parent.addDockWidget(Qt.RightDockWidgetArea, addTimerWidget)
            addTimerWidget.show()
            
        else:

            parent.removeDockWidget(addTimerWidget)


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

        
    
    def addStopWatch(self, timeObject: str, duration: datetime.timedelta, name: str, startDuration: datetime.timedelta, color: str, notepadContents: str = '') -> None:
        
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

        if startDuration >= datetime.timedelta(hours=24): # startDuration gives the days but not in total hours, needed so that loadSaveData() can work
            
            startDurationDays = int(startDuration.__str__().split(':')[0].split()[0])
            parent.setProperty('originalDuration', f'{startDurationDays * 24}:00:00')

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
                
            except RuntimeError: # If timer is deleted, will traceback a runtime error
                return

        
        countDownTimer(self, difference)
    
    def resetTimer(self, timeObject: str, name: str, startDuration: datetime.timedelta, id: str, color: str, notes: str = ''):

        self.findChild(qtw.QFrame, id).deleteLater()

        currentTime = datetime.datetime.today()

        difference =  (currentTime + startDuration) - currentTime

        self.addStopWatch(timeObject, difference, name, startDuration, color, notepadContents=notes)

        

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


        toolBar = toolbar(self)
        self.addToolBar(toolBar)

        self.central = centralWidget(self)
        self.setCentralWidget(self.central)

        dockWidget = addTimer(self)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

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

                    originalDuration = int(originalDuration.split(':')[0])

                    originalDuration = datetime.timedelta(hours=originalDuration)
                
                elif line.startswith('Border Color:'):

                    color = line.split()[2]

                elif line.startswith('Notes: '):
                    notes = ''.join(line.split('Notes: ')[1:]).strip()

                    self.central.addStopWatch(name, finishedTime, name, originalDuration, color, notepadContents=notes)
                    
def saveData():
    
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
        
    


if __name__ == '__main__':
    import sys

    app = qtw.QApplication(sys.argv)

    mw = window()
    mw.resize(1920, 1080)
    version = '1.0'
    mw.setWindowTitle(f'Genshin Stopwatch V{version}')
    mw.setWindowIcon(qtg.QIcon('icon.ico'))
    mw.show()

    app.exec_()

    # After Program Ends
    saveData()

# Color Pallete
# Background: #1A1A1B 
# Frame Background: #333F44
# Foreground: #37AA9C
# Text: #94F3E4
# Alt Text: #FCB3FC