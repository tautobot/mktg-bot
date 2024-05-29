from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, elementIsDisplayed


class UpdateNricfinPage():
    def __init__(self, driver):
        self.driver             = driver
        self.essentials_product = By.XPATH, '//*[text()="Essentials"]'
        self.nricfin            = By.XPATH, '//*[@placeholder="Enter NRIC"]' 
        self.save_button        = By.XPATH, '//*[text()="SAVE"]'
        self.error_msg          = By.XPATH, '//*[@class="error-text"]'

    def input_nricfin(self, nric):
        wait_element(self.driver,self.nricfin).send_keys(nric)

    def click_save_button(self):
        wait_element(self.driver,self.save_button).click()

    def get_error_msg(self):
        return wait_element(self.driver,self.error_msg).text

    def is_update_nric_successful(self):
        return elementIsDisplayed(self.driver, self.essentials_product)
