from selenium import webdriver

# 로그인
def ArijiLogin(driver, user_id, user_pw):
    # 홈페이지 이동
    driver.get('https://www.ariji.co.kr/')

    # ActionChain 준비
    login_act = webdriver.ActionChains(driver)

    # 로그인 페이지로 이동하는 버튼 클릭
    driver.find_element_by_xpath('//*[@id="header"]/div[1]/a[2]').click()
    
    # 버튼 위치
    id_box = driver.find_element_by_xpath('//*[@id="keyword22"]')
    pw_box = driver.find_element_by_xpath('//*[@id="keyword222"]')
    login_btn = driver.find_element_by_xpath(
        '/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[4]/a')

    # id, pw 입력 후 로그인
    login_act.send_keys_to_element(id_box, user_id).send_keys_to_element(pw_box, user_pw).click(login_btn).perform()
    driver.implicitly_wait(3)

