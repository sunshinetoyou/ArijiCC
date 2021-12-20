import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
from GUI_calendar import CalendarGUI

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.UI_set = QtUiTools.QUiLoader().load("../ui/main.ui")
        self.setupUI()

    def setupUI(self):

        # 달력창 띄우기
        self.UI_set.cal_btn_1.clicked.connect(self.openCalendar)
        self.UI_set.cal_btn_2.clicked.connect(self.openCalendar)
        self.UI_set.cal_btn_3.clicked.connect(self.openCalendar)

        # ui 파일 QMainWindow에 적용
        self.setCentralWidget(self.UI_set)
        self.setWindowTitle("ARIJI MAIN")
        self.setFixedSize(700, 390)
        self.show()

    def openCalendar(self):
        dialog = CalendarGUI(self)
        if dialog.exec_():
            print(dialog.getDate())
        else:
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainGUI()
    sys.exit(app.exec_())