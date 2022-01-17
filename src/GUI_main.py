import sys
import time

from PySide2 import QtUiTools
from PySide2.QtWidgets import QApplication, QMainWindow, QComboBox, QDateEdit, QTimeEdit, QMessageBox, QGroupBox
from PySide2.QtCore import QDate, Slot
from GUI_calendar import CalendarGUI
from LOGIC_main import booking
from THREAD_logic import LOGIC_Worker
from LOGIC_logging import makeLogger

id = "ks0542"
pw = "12qwaszx."
rangeOfUpdate = 27

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.numOfGroup = 1
        self.UI_set = QtUiTools.QUiLoader().load("../ui/main.ui")
        self.groups = [self.UI_set.DataA, self.UI_set.DataB, self.UI_set.DataC]
        self.setupUI()

    def setupUI(self):
        # 기존 QDateEdit 위젯 현재 날짜로 재설정
        self.UI_set.A_dateEdit.setDate(QDate.currentDate())
        self.UI_set.B_dateEdit.setDate(QDate.currentDate())
        self.UI_set.C_dateEdit.setDate(QDate.currentDate())

        # 기존의 데이터 그룹은 1개만 활성화되어 있음
        self.UI_set.DataB.setEnabled(False)
        self.UI_set.DataC.setEnabled(False)

        # 데이터 개수에 따라 입력 가능한 그룹 변경하기
        self.UI_set.numOfData_combo.currentIndexChanged.connect(self.setDataGroup)

        # 달력 버튼 -> 달력 창 띄우기
        self.UI_set.cal_btn_1.clicked.connect(self.openACalendar)
        self.UI_set.cal_btn_2.clicked.connect(self.openBCalendar)
        self.UI_set.cal_btn_3.clicked.connect(self.openCCalendar)

        # 데이터검사/실행/종료 버튼
        self.UI_set.check_btn.clicked.connect(self.checkData)
        self.UI_set.do_btn.clicked.connect(self.startBooking)
        self.UI_set.stop_btn.clicked.connect(self.close)

        # ui 파일 QMainWindow에 적용
        self.setCentralWidget(self.UI_set)
        self.setWindowTitle("아리지("+id+")")
        self.setFixedSize(700, 390)
        self.show()

    # 그룹 활성화 변경 함수
    # 0 : enable
    # 1 : disable
    # 둘다 공통으로 색 초기화
    def setGroupEnable(self, group, status):
        if status == 0:
            # makeLogger("setGroupEnable", "info", group.objectName()+"를 enabled로 설정합니다.")
            group.setEnabled(True)
            group.findChild(QDateEdit).setDate(QDate.currentDate())
        elif status == 1:
            # makeLogger("setGroupEnable", "info", group.objectName() + "를 disabled로 설정합니다.")
            group.setEnabled(False)
        else:
            makeLogger("setGroupEnable", "error", "주어진 status가 올바르지 않습니다.")

    # 그룹 색상 변경 함수
    # 0 : enable, 주황, ready
    # 1 : enable, 초록, done
    # 2 : enable, 빨강, error
    def setGroupColor(self, widget, status):
        if status == 0:
            # makeLogger("setGroupColor", "info", widget.parent().objectName()+"를 대기상태(주황색)로 바꿉니다.")
            widget.parent().setStyleSheet("background-color: orange")
        elif status == 1:
            # makeLogger("setGroupColor", "info", widget.parent().objectName() + "를 완료상태(초록색)로 바꿉니다.")
            widget.setStyleSheet("background-color: green")
        elif status == 2:
            # makeLogger("setGroupColor", "info", widget.parent().objectName() + "를 에러상태(빨간색)로 바꿉니다.")
            widget.parent().setStyleSheet("background-color: red")
        else:
            makeLogger("setGroupColor", "error", "주어진 status가 올바르지 않습니다.")

    # 데이터 개수 적용
    def setDataGroup(self):
        print("* set group enabled")
        self.numOfGroup = int(self.UI_set.numOfData_combo.currentText()[0])
        makeLogger("setDataGroup", "info", "데이터 그룹 "+str(self.numOfGroup)+"개 활성화")
        for k in range(3):
            self.groups[k].setStyleSheet("")    # 배경색 초기화
            if k <= self.numOfGroup-1:
                self.setGroupEnable(self.groups[k], 0)
            else:
                self.setGroupEnable(self.groups[k], 1)

    # 그룹A 달력 창 띄우기
    def openACalendar(self):
        print("* open A calendar")
        makeLogger("openACalendar", "info", "그룹A 달력 창 띄우기")
        dialog_cal = CalendarGUI(self)

        if dialog_cal.exec_(): # 확인 버튼을 눌렀을 시에
            # 클릭한 값 main에 적용
            self.UI_set.A_dateEdit.setDate(dialog_cal.getDate())

    # 그룹B 달력 창 띄우기
    def openBCalendar(self):
        print("* open B calendar")
        makeLogger("openBCalendar", "info", "그룹B 달력 창 띄우기")
        dialog_cal = CalendarGUI(self)

        if dialog_cal.exec_():  # 확인 버튼을 눌렀을 시에
            # 클릭한 값 main에 적용
            self.UI_set.B_dateEdit.setDate(dialog_cal.getDate())

    # 그룹C 달력 창 띄우기
    def openCCalendar(self):
        print("* open C calendar")
        makeLogger("openCCalendar", "info", "그룹C 달력 창 띄우기")
        dialog_cal = CalendarGUI(self)

        if dialog_cal.exec_():  # 확인 버튼을 눌렀을 시에
            # 클릭한 값 main에 적용
            self.UI_set.C_dateEdit.setDate(dialog_cal.getDate())

    # 메세지 창 띄우기
    def showMessage(self, level, text):
        if level == 'warning':
            makeLogger("checkLogic", "warning", text)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            print("구현되지 않은 위험 단계입니다. 단계 조정을 warning 으로 변경해주세요.")

    # 데이터 검사 로직
    def checkLogic(self, group):
        # 날짜 데이터 검사
        dateEdit = group.findChild(QDateEdit)
        now = QDate.currentDate()
        future = dateEdit.date().addDays(-dateEdit.date().dayOfWeek() + 1 + rangeOfUpdate)

        if not now < dateEdit.date() < future:
            self.setGroupColor(dateEdit, 2)
            self.showMessage("warning", "날짜 데이터가 옳지 않습니다.")
            return False

        # 시간 데이터 검사
        stimeEdit, etimeEdit = group.findChildren(QTimeEdit)

        if stimeEdit.time() >= etimeEdit.time():
            self.setGroupColor(stimeEdit, 2)
            self.showMessage("warning", "시간 데이터가 옳지 않습니다.")
            return False

        # 코스 데이터 검사
        courses = list(map(lambda box: box.currentIndex(), group.findChildren(QComboBox)))

        # 코스 데이터의 중복 여부 판단 ( set 이용 )
        def has_duplicates(seq):
            return len(seq) != len(set(seq))

        if has_duplicates(courses):
            self.setGroupColor(group.findChild(QComboBox, "course1"), 2)
            self.showMessage("warning", "코스 데이터가 옳지 않습니다.")
            return False

        makeLogger("checkLogic", "info", group.objectName()+" 데이터 유효성 검사 통과")
        self.setGroupColor(dateEdit, 0)
        return True

    # 데이터 검사 버튼
    def checkData(self):
        print("* check data")
        makeLogger("checkData", "info", "데이터 유효성 검사 시작")
        # 각 그룹이 사용 가능한지 판단
        for group in self.groups:
            if group.isEnabled():
                self.checkLogic(group)

    # 예약
    def startBooking(self):
        print("* check data")
        for group in self.groups:
            if group.isEnabled():
                if not self.checkLogic(group):
                    makeLogger("startBooking", "error", "데이터 유효성이 올바르지 않습니다.")
                    return
        makeLogger("startBooking", "info", "예약 시작 전 데이터 유효성 검사 통과")

        print("* book data")
        makeLogger("startBooking", "info", "예약 시작")

        # 예약 데이터 가져오기
        def getGroupInfo(group):
            date = group.findChild(QDateEdit).date()
            times = list(map(lambda x: x.time(), group.findChildren(QTimeEdit)))
            courses = list(map(lambda x: x.currentText(), group.findChildren(QComboBox)))

            group.setEnabled(False)

            return date, times, courses

        # UI에 있는 각 그룹별 데이터
        groups_data = [(group, getGroupInfo(group)) for group in self.groups if group.isEnabled()]

        # 예약
        # for group_data in groups_data:
        #     booking(group_data, id, pw)

        # 쓰레드 사용해서 예약
        # 각자 쓰레드를 통해 예약을 하긴 하는데, 동시에 예약을 하면
        for group_data in groups_data:
            self.worker = LOGIC_Worker(group_data[0], group_data[1], id, pw, self)
            self.worker.start()
            time.sleep(0.5)

        self.worker.finished.connect(self.finishBooking)

    @Slot(bool, QGroupBox)
    def finishBooking(self, b, widget):
        if b:
            makeLogger("finishBooking", "info", "완료 -> 창 초록색")
            self.setGroupColor(widget, 1)
        else:
            makeLogger("finishBooking", "info", "실패 -> 창 빨간색")
            self.setGroupColor(widget, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainGUI()
    sys.exit(app.exec_())