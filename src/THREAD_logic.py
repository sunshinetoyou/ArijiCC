from PySide2.QtCore import *
from PySide2.QtWidgets import QGroupBox
from LOGIC_main import booking


class LOGIC_Worker(QThread):
    finished = Signal(bool, QGroupBox)

    def __init__(self, widget, group_data, _id, _pw, parent=None):
        super().__init__(parent)
        self.widget = widget
        self.groupInfo = group_data
        self.id = _id
        self.pw = _pw

    def run(self):
        print("* book data by thread")
        try:
            # 예약
            booking(self.groupInfo, self.id, self.pw)
            self.finished.emit(True, self.widget)
        except:
            self.finished.emit(False, self.widget)
            print("error")