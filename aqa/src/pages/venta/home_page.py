from selenium.webdriver.common.by import By

from aqa.utils.enums import url
from aqa.utils.webdriver_util import wait_element


class HomePage():
    def __init__(self, driver):
        self.driver           = driver
        self.buy_pml_btn      = By.XPATH, '//*[(text()="BUY PML NOW")]'
        self.see_pricing_btn  = By.XPATH, '//*[text()="SEE PRICING"]'
        self.purchase_now_btn = By.XPATH, '//button[text()="PURCHASE NOW"]'

    def open_url(self, url):
        self.driver.get(url)

    def click_on_see_pricing_btn(self):
        wait_element(self.driver,self.see_pricing_btn).click()

    def click_on_buy_pml_btn(self):
        wait_element(self.driver,self.buy_pml_btn).click()


    def click_on_purchase_now_btn(self):
        wait_element(self.driver, self.purchase_now_btn).click()


class ZeekHomePage():
    def __init__(self, driver):
        self.driver            = driver
        self.url               = url.url_zeek
        self.buy_flep_btn      = By.XPATH, '//*[text()="Freelancer Earnings Protection"]/following-sibling::button'
        self.buy_flep_now_btn  = By.XPATH, '//*[text()="BUY FLEP NOW"]'
        self.buy_pa_btn        = By.XPATH, '//*[text()="Personal Accident Protection"]/following-sibling::button'
        self.buy_pa_now_btn    = By.XPATH, '//*[text()="BUY PERSONAL ACCIDENT NOW"]'

    def open_url(self):
        self.driver.get(self.url)

    def click_on_buy_flep_btn(self):
        wait_element(self.driver,self.buy_flep_btn).click()

    def click_buy_flep_now_btn(self):
        wait_element(self.driver,self.buy_flep_now_btn).click()

    def click_on_buy_pa_btn(self):
        wait_element(self.driver,self.buy_pa_btn).click()

    def click_buy_pa_now_btn(self):
        wait_element(self.driver,self.buy_pa_now_btn).click()

