from __future__ import annotations
from typing import TYPE_CHECKING
from enum import StrEnum, auto
import webbrowser

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt, QTimer

from widgets.updateAlert import UpdateAlert
from widgets.stopwatch import Stopwatch, Property

from saveConfig import saveConfig, ConfigKeys
from style import StyleManager, StyleSheets
from checkVersion import checkUpdate

if TYPE_CHECKING:
    from widgets.mainWindow import window
    import PySide6.QtGui as qtg

class ApplyChangesProperty(StrEnum):
    unsavedChanges = auto()

class optionsDock(qtw.QDockWidget):
    def __init__(self, parent: window = None):
        super().__init__(parent)

        self.mw = parent

        self.config = saveConfig()

        self.styles = StyleManager()

        self.setWindowTitle('Options')
        self.setObjectName('optionsDockWidget')
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

        # Vertical Layout (For Topic Frame)
        self.vertLayout = qtw.QVBoxLayout()
        self.vertLayout.setSpacing(10)
        self.topicFrame.setLayout(self.vertLayout)

        # Checkbox
        self.appOnCloseCheckbox = qtw.QCheckBox()
        self.appOnCloseCheckbox.setText('Desktop Notifications')
        self.appOnCloseCheckbox.setChecked(self.config.getShutdownOnClose())
        self.appOnCloseCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.appOnCloseCheckbox.setToolTip('The app will close and not run in the background.')

        # Checkbox
        self.showOnOpenCheckbox = qtw.QCheckBox()
        self.showOnOpenCheckbox.setText('Show On App Start')
        self.showOnOpenCheckbox.setChecked(self.config.getStartUp())
        self.showOnOpenCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.showOnOpenCheckbox.setToolTip('Program will automatically show or hide when starting.')

        self.updateCheckBox = qtw.QCheckBox()
        self.updateCheckBox.setText('Check For Update On Startup')
        self.updateCheckBox.setChecked(self.config.getVersionCheck())
        self.updateCheckBox.clicked.connect(lambda: self.settingChanged(True))
        self.updateCheckBox.setToolTip('When the program starts it will go online to check and see if your client is up-to-date')

        # Checkbox
        self.notifyCheckbox = qtw.QCheckBox()
        self.notifyCheckbox.setText('Desktop Notifications')
        self.notifyCheckbox.setChecked(self.config.getDesktopNotifications())
        self.notifyCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.notifyCheckbox.setToolTip('A windows desktop notification will appear when a stopwatch finishes.')

        # Checkbox
        self.staticDailyNotifyCheckbox = qtw.QCheckBox()
        self.staticDailyNotifyCheckbox.setText('Daily Reset Notifications')
        self.staticDailyNotifyCheckbox.setChecked(self.config.getDailyReset())
        self.staticDailyNotifyCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.staticDailyNotifyCheckbox.setToolTip('Will recieve a notification when there is a daily reset.')

        # Checkbox
        self.staticWeeklyNotifyCheckbox = qtw.QCheckBox()
        self.staticWeeklyNotifyCheckbox.setText('Weekly Reset Notifications')
        self.staticWeeklyNotifyCheckbox.setChecked(self.config.getWeeklyReset())
        self.staticWeeklyNotifyCheckbox.clicked.connect(lambda: self.settingChanged(True))
        self.staticWeeklyNotifyCheckbox.setToolTip('Will recieve a notification when there is a daily reset.')
        
        # Label for color scheme dropdown
        self.colorPalletLabel = qtw.QLabel('Color Scheme:')

        # Color scheme dropdown
        self.colorPallet = qtw.QComboBox()
        self.colorPallet.addItems([x.title() for x in self.styles.getColorPallets()])
        self.colorPallet.setCurrentText(self.config.getCurrentPallet().title())
        self.colorPallet.currentTextChanged.connect(lambda: self.settingChanged(True))
        self.colorPallet.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Adding checkboxes to frame
        for widget in (self.appOnCloseCheckbox,
                       self.showOnOpenCheckbox,
                       self.updateCheckBox,
                       self.notifyCheckbox,
                       self.staticDailyNotifyCheckbox,
                       self.staticWeeklyNotifyCheckbox,
                       self.colorPalletLabel,
                       self.colorPallet):
            self.vertLayout.addWidget(widget)

        # Apply Settings Button
        self.applyButton = qtw.QPushButton('Apply', self)
        self.applyButton.setObjectName('applySettingsButton')
        self.applyButton.clicked.connect(self.applySettings)
        self.applyButton.clicked.connect(lambda: self.settingChanged(False))
        self.applyButton.setProperty(ApplyChangesProperty.unsavedChanges, 'false')
        verticalLayout.addWidget(self.applyButton, alignment=Qt.AlignmentFlag.AlignTop)

        # Check for updates button
        self.updateButton = qtw.QPushButton('Check for updates', self)
        self.updateButton.setObjectName('checkUpdateButton')
        self.updateButton.clicked.connect(self.checkUpdate)
        verticalLayout.addWidget(self.updateButton, alignment=Qt.AlignmentFlag.AlignTop)

        # Support wolfmyths
        self.supportButton = qtw.QPushButton('Support Wolfmyths on Ko-Fi', self)
        self.supportButton.setToolTip('Opens a new tab on your web browser to ko-fi.com')
        self.supportButton.clicked.connect(self.openKoFiLink)
        verticalLayout.addWidget(self.supportButton, alignment=Qt.AlignmentFlag.AlignTop)

        self.setWidget(self.centralFrame)
    
    def settingChanged(self, bool: bool):
        
        # Change the property of the applyButton to signal the user a setting's been changed
        self.applyButton.setProperty(ApplyChangesProperty.unsavedChanges, str(bool).lower())
        
        self.style().polish(self.applyButton)
    
    def openKoFiLink(self) -> None:
        webbrowser.open_new_tab('https://ko-fi.com/C0C4MJZS9')
    
    def checkUpdate(self) -> None:
        def updateFound(latestVersion: str, changelog: str) -> None:
            # Will create a dialog window if there's a version update unless specified not to

            updateNotify = UpdateAlert(latestVersion, changelog)

            updateNotify.exec()
        
        def upToDate() -> None:
            self.updateButton.setText('On latest version ^_^')
            QTimer.singleShot(3000, lambda: self.updateButton.setText('Check for updates'))
        
        self.check = checkUpdate()
        self.check.upToDate.connect(upToDate)
        self.check.updateDetected.connect(lambda x, y: updateFound(x, y))
            
    
    def applySettings(self):
        # Create a dictionary with updated configuration settings

        updatedConfig = {
                            ConfigKeys.shutdown_app_on_close : str(self.appOnCloseCheckbox.isChecked()),
                            ConfigKeys.show_on_startup       : str(self.showOnOpenCheckbox.isChecked()),
                            ConfigKeys.desktop_notifications : str(self.notifyCheckbox.isChecked()),
                            ConfigKeys.color_pallet          : self.colorPallet.currentText().lower(),
                            ConfigKeys.checkversiononstartup : str(self.updateCheckBox.isChecked()),
                            ConfigKeys.dailyresetnotify      : str(self.staticDailyNotifyCheckbox.isChecked()),
                            ConfigKeys.weeklyresetnotify     : str(self.staticWeeklyNotifyCheckbox.isChecked())
                        }
        
        # Checking to see if the user wants to change the color scheme
        if self.colorPallet.currentText().lower() != self.config.getCurrentPallet():

            self.styles.changeColorPallet(updatedConfig[ConfigKeys.color_pallet])

            stopwatch: Stopwatch
            for stopwatch in self.mw.central.findChildren(Stopwatch):

                # Updating the stylesheet again to change border color
                self.styles.changeStopwatchBorderColor(stopwatch.property(Property.BorderColor))

                # Change stopwatch stylesheet
                stopwatch.setStyleSheet(self.styles.getStyleSheet(StyleSheets.stopwatch))
                self.mw.central.style().polish(stopwatch)

            # Change global stylesheet  
            app: qtw.QApplication = qtw.QApplication.instance()      
            app.setStyleSheet(self.styles.getStyleSheet(StyleSheets.app))
            app.style().polish(app)

        self.config['OPTIONS'] = updatedConfig

        self.config.save()
        self.settingChanged(False)

    def hideEvent(self, a0: qtg.QHideEvent) -> None:
        # Check if the parent widget is hidden

        if self.mw.isHidden():
            a0.ignore()

        else:

            self.mw.toolBar.optionsButton.setChecked(False)
            
            if not self.mw.isMinimized():
                # Update the configuration setting 'settings open on startup' to 'False'
                self.config['QOL'][ConfigKeys.settings_open_on_startup] = 'False'
                
                # Save the updated configuration
                self.config.save()

        return super().hideEvent(a0)

    def showEvent(self, a0: qtg.QShowEvent) -> None:
        # Get references to the parent widget, toolbar, and optionsButton

        # Set the optionsButton as checked

        self.mw.toolBar.optionsButton.setChecked(True)

        # Update the configuration setting 'settings open on startup' to 'True'
        if not self.mw.isMinimized():
            
            self.config['QOL'][ConfigKeys.settings_open_on_startup] = 'True'
            self.config.save()
        return super().showEvent(a0)