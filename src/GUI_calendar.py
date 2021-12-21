import sys
from PySide2 import QtUiTools
from PySide2.QtWidgets import QApplication, QDialog, QGridLayout, QVBoxLayout


class CalendarGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.UI_set = QtUiTools.QUiLoader().load("../ui/calendar.ui")
        self.setupUI()

    def setupUI(self):
        # 이벤트 연결
        self.UI_set.ok_btn.clicked.connect(self.accept)
        self.UI_set.no_btn.clicked.connect(self.reject)

        # ui 파일 QMainWindow에 적용
        layout = QVBoxLayout()
        layout.addWidget(self.UI_set)
        self.setLayout(layout)

        self.setWindowTitle("ARIJI CALENDAR")
        # self.setFixedSize(430, 400)

    def getDate(self):
        return self.UI_set.calendarWidget.selectedDate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CalendarGUI()

    sys.exit(app.exec_())