# # logging 모듈 사용
import logging
#
# # 최고위 logger 만들기
root_logger = logging.getLogger()
#
# # 출력 형식 지정
formatter = logging.Formatter(fmt="%(levelname)s %(asctime)s - %(name)s : %(message)s")
#
# # 파일 핸들러 만들기
file_handler = logging.FileHandler('../log/file.log', encoding="utf-8")  # 파일 지정
file_handler.mode = "w"                 # 쓰기 모드
file_handler.setFormatter(formatter)    # 출력 형식 적용

root_logger.addHandler(file_handler)    # 최고위 logger에 핸들러 적용
# # 콘솔 출력 시 핸들러
# # console = logging.StreamHandler()
# # console.setFormatter(formatter)
#
# # root_logger.addHandler(console)
#
# # 이름, 단계, 메세지 적용해서 로그 생성하는 함수
def makeLogger(name, level, message):
    logger = logging.getLogger(name)# 로그 생성
    logger.setLevel(logging.INFO)   # 로그의 출력 기준 설정

    if level == "info":     # 실행 정보
        logger.info(message)
    elif level == "error":  # 에러 정보
        logger.error(message)