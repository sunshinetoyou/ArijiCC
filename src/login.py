import webdriver

# ariji_elements = LoginLocation('//*[@id="header"]/div[1]/a[2]', '//*[@id="keyword22"]', '//*[@id="keyword222"]', '/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[4]/a')
# print(ariji_elements.id_box)
# 아이디 / 비번 입력
def getID():
    pass

def getPassword():
    pass

# 사이트 입력
def getSite():
    pass

# 로그인
# url : 'https://www.ariji.co.kr/'
# login_elements = [loginPage_btn, id_box, pw_box, login_btn]
# //*[@id="header"]/div[1]/a[2], //*[@id="keyword22"], //*[@id="keyword222"], /html/body/table[2]/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[4]/a
def login(driver, url, login_elements, user_id, user_pw):
    # 홈페이지 이동
    driver.get(url)

    # ActionChain 준비
    login_act = webdriver.ActionChains(driver)

    # 로그인 페이지로 이동하는 버튼 클릭
    driver.find_element_by_xpath(login_elements.getLoginPageBtn).click()

    login_act.send_keys_to_element(login_elements.getIdBox, user_id).send_keys_to_element(login_elements.getPwBox, user_pw).click(login_elements.getLoginBtn).perform()
    driver.implicitly_wait(3)
