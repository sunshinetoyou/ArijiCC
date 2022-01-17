from selenium import webdriver

def startDriver():
    # webdriver option
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")

    # webdriver start
    driver = webdriver.Chrome('../chromedriver/chromedriver.exe', options=options)
    driver.implicitly_wait(3)

    return driver
