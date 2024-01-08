from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from widgets.trayMenu import trayMen

from constants import ICON

if TYPE_CHECKING:
    from widgets.mainWindow import window

class sysTrayIcon(qtw.QSystemTrayIcon):
    def __init__(self, parent: qtw.QApplication = None, mw: window = None) -> None:
        super().__init__(parent=parent)

        self.setIcon(qtg.QIcon(ICON))
        self.setToolTip('Genshin Stopwatch')
        self.setVisible(True)

        trayMenu = trayMen(parent, mw)

        self.setContextMenu(trayMenu)
