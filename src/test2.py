import sys
from PySide2 import QtUiTools
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Signal, Slot



class MainView(QMainWindow):
    btn_signal
    def __init__(self):
        super().__init__()
        self.num = 0
        self.UI_set = QtUiTools.QUiLoader().load("../ui/testPalette.ui")
        self.setupUI()

    def setupUI(self):
        self.UI_set.pushButton.clicked.connect(self.test2)

        self.UI_set.pushButton.emit()
        self.setCentralWidget(self.UI_set)
        self.setWindowTitle("UI TEST")
        self.resize(400, 380)
        self.show()

    @Slot(int)
    def test2(self, n):
        print(n)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainView()
    sys.exit(app.exec_())