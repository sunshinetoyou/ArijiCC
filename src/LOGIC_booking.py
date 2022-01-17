import selenium.common.exceptions
from PySide2.QtCore import QDate, QTime
from bs4 import BeautifulSoup

# 달력 선택
def pickCalendar(driver, date):
    # 이번 달이면 now_calendar, 다음 달이면 next_calendar으로 이동
    if date.month() == QDate.currentDate().month():
        driver.switch_to.frame("now_calendar")
    else:
        driver.switch_to.frame("next_calendar")

# 달력 페이지에서 날짜 선택
def pickDateByiframe(driver, date):
    driver.get("https://www.ariji.co.kr/membership/booking/time_calendar_form.asp")

    pickCalendar(driver, date)

    # 날짜를 인덱스로 변환
    def getDateIDX():
        parser = BeautifulSoup(driver.page_sources, 'html.parser')

        date_list = list(map(lambda x: x.text, parser.select("/html/body/table/tbody/tr[3]/td/table/tbody/tr[4]/td[6]/font")))
        idx = date_list.index(date.day())

        if idx < 7:
            return 1, idx + 1
        else:
            return 1 + idx // 7, idx % 7 + 1

    dateIDX = getDateIDX()

    # 날짜 찾아서 코스 선택 창으로 이동
    # 원리: img의 바로 윗 부모가 a 태그이면 click 가능 판단 / 아니라면 click 불가능 판단
    while True:
        try:
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr[3]/td/table/tbody/tr[' + str(dateIDX[0]) + ']/td[' + str(dateIDX[1]) + ']/a').click()
            driver.switch_to.default_content()
            break
        except selenium.common.exceptions.NoSuchElementException:
            driver.refresh()

# 홈페이지에서 날짜 선택
def pickDateByhomePage(driver, date):
    driver.get("https://www.ariji.co.kr/index.asp")
    
    parser = BeautifulSoup(driver.page_source, 'html.parser')

    # 날짜를 인덱스로 변환
    def getDateIDX():
        date_list = list(map(lambda x: int(x.text) if not "/" in x.text else int(x.text.split("/")[1]), parser.select(".calendar_new > tbody > tr > td > font")))
        
        idx = date_list.index(date.day())

        if idx < 7:
            return 1, idx + 1
        else:
            return 1 + idx // 7, idx % 7 + 1

    dateIDX = getDateIDX()

    btn = parser.select_one(
        '.calendar_new > tbody > tr:nth-child(' + str(dateIDX[0]) + ') > td:nth-child(' + str(dateIDX[1]) + ')')

    # 버튼은 언젠간 활성화가 되어야 하는 버튼이어야 함. ( 앞에서 날짜에 대한 데이터 유효성 검사를 했기 때문에 )
    # 버튼 눌러서 코스 선택 창으로 이동
    while True:
        if btn.has_attr('onclick'): # 버튼이 활성화 되어 있을 때
            driver.find_element_by_xpath(
                '//*[@class="calendar_new"]/tbody/tr[' + str(dateIDX[0]) + ']/td[' + str(dateIDX[1]) + ']').click()
            driver.implicitly_wait(1)
            break
        else:   # 버튼 비활성화
            driver.get("https://www.ariji.co.kr/index.asp") # 새로고침

# 예약 시도
def findCourse(driver, times, courses):
    for course in courses:
        parser = BeautifulSoup(driver.page_source, 'html.parser')

        courseidx = 0 if course == "햇님" else 1 if course == "달님" else 2
        # 선택한 코스에 있는 예약 할 수 있는 데이터들 ( ex, 햇님 코스의 Tee-Off 값들 )
        courses_list = parser.select('body > table.sub_mid > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr > td > table:nth-child(3) > tbody > tr:nth-child(1) > td')[courseidx].select("tr")

        for idx in range(len(courses_list)):
            if idx != 2 and courses_list[idx].has_attr('align'):    # 필요없는 값 ( 목차, 빈칸 ) 제거
                # courses[idx].select_one("td:nth-of-type(1)").text 에 들어갈 수 있는 값
                # 1. 해당하는 tee 0ff 타임이 없습니다.
                # 2. 시간 값
                if courses_list[idx].select_one("td:nth-of-type(1)").text != '해당하는 Tee-Off 타임이 없습니다.':
                    tmp_time = courses_list[idx].select_one("td:nth-of-type(1)").text
                    hour, minute = map(int, tmp_time.split(":"))
                    # 시간과 분으로 QTime 객체 생성 ( 시간 비교를 수월하게 하기 위해 )
                    time = QTime(hour, minute, 0)

                    # 시간대 판단
                    if times[0] <= time <= times[1]:
                        return clickBooking(driver, courses_list[idx].select_one("td:nth-of-type(4) > a")['href'])
                else:   # 코스 자체에 코스가 하나도 없을 경우
                    raise Exception("Tee-Off 타임이 없습니다.")

        # 코스가 존재하기는 하는데 내가 원하는 시간대의 코스가 없을 경우
        raise Exception("해당하는 Tee-Off 타임이 없습니다.")

# 예약 경고창에서 확인/취소 누르기
def clickBooking(driver, script):
    driver.execute_script(script)
    driver.implicitly_wait(1)
    alert = driver.switch_to.alert
    # alert 창 확인
    # alert.accept()
    # alert 창 취소
    alert.dismiss()

# 예약 확인
def checkBooking():
    pass

if __name__ == "__main__":
    pass