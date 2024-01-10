import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from constants import GUIDE, ICON

class Guide(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Genshin Stopwatch: Guide')
        self.setWindowIcon(qtg.QIcon(ICON))

        self.setMinimumSize(1000, 1000)

        # Vertical Box Layout
        verticalLayout = qtw.QVBoxLayout()
        self.setLayout(verticalLayout)

        self.textFile = qtw.QTextBrowser(self)
        self.textFile.setReadOnly(True)
        self.textFile.setOpenExternalLinks(True)

        # Reading html guide
        # The guide is packaged into the .exe so it is always updated
        try: 

            with open(GUIDE, 'r') as html:

                self.textFile.setHtml(html.read())

        except Exception as e:

            self.textFile.setHtml(
                f'''
                <h1>Error. Could not find Guide:</h1>
                <br><br>
                {e}
                ''')
        
        verticalLayout.addWidget(self.textFile)
