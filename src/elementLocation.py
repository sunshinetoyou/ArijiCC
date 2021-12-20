class LoginLocation:
    def __init__(self, loginPage_btn, id_box, pw_box, login_btn):
        self.loginPage_btn = loginPage_btn
        self.id_box = id_box
        self.pw_box = pw_box
        self.login_btn = login_btn

    def getLoginPageBtn(self):
        return self.loginPage_btn

    def getIdBox(self):
        return self.id_box

    def getPwBox(self):
        return self.pw_box

    def getLoginBtn(self):
        return self.login_btn
