from LOGIC_webdriver import startDriver
from LOGIC_login import ArijiLogin
from LOGIC_booking import pickDateByiframe, pickDateByhomePage, findCourse
from LOGIC_logging import makeLogger
from Check_Chromedriver import Check_Chromedriver

def booking(group_data, _id, _pw):
    # driver 버전 확인
    Check_Chromedriver.main()

    # driver 실행
    makeLogger("startDriver", "info", "driver 실행")
    driver = startDriver()

    # 로그인 실행 (무조건 로그인 된다고 생각 <- id, pw 하드코딩 )
    makeLogger("ArijiLogin", "info", "아리지cc 로그인")
    ArijiLogin(driver, _id, _pw)

    # 달력창으로 이동 & 날짜 선택
    makeLogger("pickDateByhomePage", "info", "달력창으로 이동 & 날짜 선택( 홈페이지의 달력 )")
    pickDateByhomePage(driver, group_data[0])
    # makeLogger("pickDateByiframe", "info", "달력창으로 이동 & 날짜 선택( 달력창 페이지 )")
    # pickDateByiframe(driver, group_data[0])
    
    # 코스 선택 & 예약 버튼 누르기
    makeLogger("findCourse", "info", "코스 선택 & 예약 버튼 누르기")
    findCourse(driver, group_data[1], group_data[2])

if __name__ == "__main__":
    pass