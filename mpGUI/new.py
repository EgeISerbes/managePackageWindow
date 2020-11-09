from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import  sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.show()

    def setUI(self):
        widget = QWidget()
        v_box = QVBoxLayout()
        h_box = QHBoxLayout()
        self.searchLine = QLineEdit()
        button = QPushButton("Find package from PyPI")
        #self.sonuc = QLabel()
        v_box.addLayout(h_box)

        h_box.addWidget(self.searchLine)
        h_box.addWidget(button)
        #v_box.addWidget(self.sonuc)


        widget.setLayout(v_box)
        self.setCentralWidget(widget)





"""class thread """



if __name__ == "__main__" :
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())