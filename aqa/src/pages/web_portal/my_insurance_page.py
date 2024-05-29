from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, findElements_xpath


class WebPortalMyInsurancePage():
    def __init__(self, driver):
        self.driver                 = driver
        self.list_active_product    = '//div[text()="Product"]'
        self.list_product_name      = '//div[text()="Product"]/following-sibling::div'
        self.list_coverage_status   = '//div[text()="Coverage"]/following-sibling::div'
        self.list_start_date        = '//div[text()="Start Date"]/following-sibling::div'
        self.active_tab             = By.XPATH, '(//div[text()="Active"])[1]'
        self.not_active_tab         = By.XPATH, '//div[text()="Not Active"]'

    def click_on_active_tab(self):
        wait_element(self.driver,self.active_tab).click()

    def get_list_active_product(self):
        return findElements_xpath(self.driver, self.list_active_product)

    def get_list_product_name(self):
        return findElements_xpath(self.driver, self.list_product_name)

    def get_list_coverage_status(self):
        return findElements_xpath(self.driver, self.list_coverage_status)

    def get_list_start_date(self):
        return findElements_xpath(self.driver, self.list_start_date)

