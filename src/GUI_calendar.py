import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QApplication, QDialog, QGridLayout


class CalendarGUI(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.UI_set = QtUiTools.QUiLoader().load("../ui/calendar.ui")
        self.setupUI()

    def setupUI(self):
        # 이벤트 연결
        self.UI_set.ok_btn.clicked.connect(self.getDate)
        self.UI_set.no_btn.clicked.connect(self.close)

        # ui 파일 QMainWindow에 적용
        layout = QGridLayout()
        layout.addWidget(self.UI_set)
        self.setLayout(layout)

        self.setWindowTitle("ARIJI CALENDAR")
        # self.setFixedSize(430, 400)
        self.show()

    def getDate(self):
        return self.UI_set.calendarWidget.selectedDate()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = CalendarGUI()
#
#     sys.exit(app.exec_())