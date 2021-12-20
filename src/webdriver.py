def startDriver():
    # webdriver option
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    # webdriver start
    driver = webdriver.Chrome('C:/Users/yeonsu/Desktop/Ariji/chromedriver_win32/chromedriver.exe', options=options)
    driver.implicitly_wait(3)

    # TODO logging
    # makeLogger("ArijiDriver", 'info', 'end driver')

    return driver