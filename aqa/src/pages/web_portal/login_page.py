from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, wait, findElements_xpath
from pyotp import *


class LoginWebPortalPage():

    def __init__(self, driver):
        self.driver                       = driver
        self.email                        = By.XPATH, '//input[@name="email"]'
        self.password                     = By.XPATH, '//input[@name="password"]'
        self.login_btn                    = By.XPATH, '//*[(text()="LOG IN")]'

        self.moe_email                    = By.ID, 'email'
        self.moe_password                 = By.ID, 'password'
        self.moe_capcha_checkbox          = By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]'
        self.passCodeInput1               = By.XPATH, '//*[@class="pass-code-input__input-container"][1]/input'
        self.passCodeInput2               = By.XPATH, '//*[@class="pass-code-input__input-container"][2]/input'
        self.passCodeInput3               = By.XPATH, '//*[@class="pass-code-input__input-container"][3]/input'
        self.passCodeInput4               = By.XPATH, '//*[@class="pass-code-input__input-container"][4]/input'
        self.passCodeInput5               = By.XPATH, '//*[@class="pass-code-input__input-container"][5]/input'
        self.passCodeInput6               = By.XPATH, '//*[@class="pass-code-input__input-container"][6]/input'
        self.moe_login_btn                = By.XPATH, '//*[text()="Login"]'
        self.moe_verify_btn               = By.XPATH, '//*[text()="Verify"]'
        self.reCAPTCHA_iframe             = By.XPATH,'//*[contains(@title,"reCAPTCHA")]'


    def login_web_portal(self, username, password, url):
        self.driver.get(url)
        wait_element(self.driver,self.email).send_keys(username)
        wait_element(self.driver,self.password).send_keys(password)
        wait_element(self.driver,self.login_btn).click()

    def login_moengage(self):
        self.driver.get('https://dashboard-04.moengage.com/v4/#/auth/')

        wait_element(self.driver,self.moe_email).send_keys('trang.truong@gigacover.com')
        wait_element(self.driver,self.moe_password).send_keys('Trang@1993')

        reCAPTCHA_iframe = wait_element(self.driver, self.reCAPTCHA_iframe)
        self.driver.switch_to.frame(reCAPTCHA_iframe)

        capcha = findElements_xpath(self.driver, '//*[@id="recaptcha-anchor"]/div[1]')
        if len(capcha) > 0:
            capcha_checkbox = wait_element(self.driver, self.moe_capcha_checkbox)
            capcha_checkbox.click()

        self.driver.switch_to.default_content()

        wait()
        wait_element(self.driver,self.moe_login_btn).click()

        # get the token from Google authenticator
        totp = TOTP("EFVW5YIVM477R4JHSAFRLQWKXEFFBA4X")
        token = totp.now()
        lst = []
        lst[:] = token

        # enter the token in the UI
        wait_element(self.driver, self.passCodeInput1).send_keys(lst[0])
        wait_element(self.driver, self.passCodeInput2).send_keys(lst[1])
        wait_element(self.driver, self.passCodeInput3).send_keys(lst[2])
        wait_element(self.driver, self.passCodeInput4).send_keys(lst[3])
        wait_element(self.driver, self.passCodeInput5).send_keys(lst[4])
        wait_element(self.driver, self.passCodeInput6).send_keys(lst[5])
        # click on the button to complete 2FA
        wait_element(self.driver,self.moe_verify_btn).click()

        wait()
        localStorage = self.driver.execute_script("return window.localStorage;")
        token = localStorage['bearer']
        return token