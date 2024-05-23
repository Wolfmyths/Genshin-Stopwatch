import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from widgets.mainWindow import window
from widgets.sysTrayIcon import sysTrayIcon

from saveConfig import saveConfig
from style import StyleManager, StyleSheets
from constants import VERSION, ICON, PROGRAM_NAME
import linuxApplication
import notify, os, platform

if __name__ == '__main__':
    import sys

    styles = StyleManager()

    config = saveConfig()

    # Create a QApplication instance
    app = qtw.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(styles.getStyleSheet(StyleSheets.app))

    # Create an instance of the 'window' class
    mw = window(app)

    # Initialize window
    mw.setWindowTitle(f'{PROGRAM_NAME} V{VERSION}')
    mw.setWindowIcon(qtg.QIcon(ICON))
    mw.show() if config.getStartUp() else mw.hide()

    tray = sysTrayIcon(app, mw)

    # Checking to see if any static timers and stopwatches went off while the program was shutdown
    notify.checkMissedNotify()

    # Check to see if an old version was left behind after update (windows)
    path = os.path.dirname(sys.executable)
    old = os.path.join(path, "Genshin-Stopwatch_OLD.exe")
    if os.path.exists(old):
        os.remove(old)
    
    # check application if on linux
    if platform.system() == "Linux":
        linuxApplication.setApplication()
        
    app.exec()
