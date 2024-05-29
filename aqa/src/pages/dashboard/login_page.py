from selenium.webdriver.common.by import By

from aqa.utils.enums import url
from aqa.utils.webdriver_util import wait_element


class DashboardLoginPage():
    def __init__(self, driver):
        self.driver                         = driver
        self.url_group_dashboard            = url.url_group_dashboard_release
        self.url_essentials_dashboard       = url.url_essential_dashboard_release
        self.username                       = By.XPATH, '//input[@name="email"]'
        self.password                       = By.XPATH, '//input[@name="password"]'
        self.login_btn                      = By.XPATH, '//*[(text()="LOGIN")]'
        self.log_in_btn                     = By.XPATH, '//*[(text()="LOG IN")]'

    def login_dashboard(self, email, password):
        self.driver.get(self.url_group_dashboard)
        wait_element(self.driver,self.username).send_keys(email)
        wait_element(self.driver,self.password).send_keys(password)
        wait_element(self.driver,self.login_btn).click()

    def login_essentials_dashboard(self, email, password):
        self.driver.get(self.url_essentials_dashboard)
        wait_element(self.driver,self.username).send_keys(email)
        wait_element(self.driver,self.password).send_keys(password)
        wait_element(self.driver,self.log_in_btn).click()
