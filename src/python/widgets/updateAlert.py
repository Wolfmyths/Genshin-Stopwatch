import webbrowser

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from saveConfig import saveConfig, ConfigKeys

from constants import ICON

class UpdateAlert(qtw.QDialog):
    def __init__(self, latestVersion: str) -> None:
        super().__init__()

        self.config = saveConfig()

        self.setWindowTitle('Genshin Stopwatch: New Version Update!')
        self.setWindowIcon(qtg.QIcon(ICON))

        layout = qtw.QVBoxLayout()

        self.message = qtw.QLabel(self, text=f'The latest update {latestVersion} has been released! Would you like to download it?')
        layout.addWidget(self.message)

        self.checkBox = qtw.QCheckBox(self, text='Do not automatically check for updates')
        self.checkBox.clicked.connect(self.checkBoxClicked)
        layout.addWidget(self.checkBox)

        self.buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.No
        self.buttonBox = qtw.QDialogButtonBox(self.buttons, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def accept(self) -> None:
        webbrowser.open_new_tab('https://github.com/Wolfmyths/Genshin-Stopwatch/releases/latest')
        return super().accept()
    
    def checkBoxClicked(self) -> None:
        if self.checkBox.isChecked():
            self.config['OPTIONS'][ConfigKeys.checkversiononstartup] = 'False'
        else:
            self.config['OPTIONS'][ConfigKeys.checkversiononstartup] = 'True'
        
        self.config.save()
