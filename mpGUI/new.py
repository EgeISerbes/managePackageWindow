from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import  sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        widget = QWidget()
        gridLayout = QGridLayout()
        



        widget.setLayout(gridLayout)




class thread



if __name__ == " main " :
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())