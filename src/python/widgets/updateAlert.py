import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from saveConfig import saveConfig, ConfigKeys

from constants import ICON

from widgets.installUpdate import updateApp


class UpdateAlert(qtw.QDialog):
    def __init__(self, latestVersion: str, changelog: str) -> None:
        super().__init__()

        self.config = saveConfig()

        self.setWindowTitle('Genshin Stopwatch: Update Detected!')
        self.setWindowIcon(qtg.QIcon(ICON))

        layout = qtw.QVBoxLayout()

        self.message = qtw.QLabel(self, text=f'The latest update {latestVersion} has been released!\nWould you like to download & install?')
        layout.addWidget(self.message)

        self.checkBox = qtw.QCheckBox(self, text='Do not automatically check for updates')
        self.checkBox.clicked.connect(self.checkBoxClicked)
        layout.addWidget(self.checkBox)

        self.patchnotes = qtw.QTextBrowser(self)
        self.patchnotes.setMarkdown(changelog)
        layout.addWidget(self.patchnotes)

        self.buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.No
        self.buttonBox = qtw.QDialogButtonBox(self.buttons, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def accept(self) -> None:
        installer = updateApp()
        installer.exec()
        return super().accept()
    
    def checkBoxClicked(self) -> None:
        if self.checkBox.isChecked():
            self.config['OPTIONS'][ConfigKeys.checkversiononstartup] = 'False'
        else:
            self.config['OPTIONS'][ConfigKeys.checkversiononstartup] = 'True'
        
        self.config.save()
