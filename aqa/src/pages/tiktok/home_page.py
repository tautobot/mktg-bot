from selenium.webdriver.common.by import By

from aqa.utils.enums import URL
from aqa.utils.webdriver_util import wait_element, wait_xpath_click


class TiktokHomePage():
    def __init__(self, driver):
        self.driver                     = driver
        self.top_login_btn              = By.XPATH, '//button[@id="header-login-button"]'
        self.login_dlg                  = By.XPATH, '//div[@id="loginContainer"]'

        self.login_with_qr_btn          = By.XPATH, '//div[@id="loginContainer"]//div[text()="Use QR code"]'
        self.login_with_qr_code         = By.XPATH, '//div[@id="loginContainer"]//div[@data-e2e="qr-code"]'

        self.login_with_phone_email_btn = By.XPATH, '//div[@id="loginContainer"]//div[text()="Use phone / email / username"]'
        self.login_with_phone_drp       = By.XPATH, '//div[@id="login-modal"]//div[@aria-controls="phone-country-code-selector-wrapper"]'
        self.login_with_phone_txt       = By.XPATH, '//div[@id="login-modal"]//input[@name="mobile"]'

        # self.buy_pml_btn      = By.XPATH, '//*[(text()="BUY PML NOW")]'
        # self.see_pricing_btn  = By.XPATH, '//*[text()="SEE PRICING"]'
        # self.purchase_now_btn = By.XPATH, '//button[text()="PURCHASE NOW"]'

    def click_on_top_login_btn(self):
        wait_element(self.driver,self.top_login_btn).click()

    def click_on_login_with_qr_btn(self):
        wait_element(self.driver,self.login_with_qr_btn).click()

    def wait_for_login_with_qr_code_display(self):
        wait_element(self.driver, self.login_with_qr_code)

    def login_w_qr(self, url):
        self.driver.get(url)
        self.click_on_top_login_btn()
        self.click_on_login_with_qr_btn()
        self.wait_for_login_with_qr_code_display()
