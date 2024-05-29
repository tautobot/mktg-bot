from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, elementIsDisplayed


class DashboardCheckoutPage():

    def __init__(self, driver):
        self.driver = driver

        self.checkout_btn                       = By.XPATH, '//button[text()="Checkout"]'
        self.next_btn                           = By.XPATH, '//button[text()="Next"]'
        self.paynow_method                      = By.XPATH, '//*[@src="/img/pay/paynow.png"]'
        self.credit_card_method                 = By.XPATH, '//*[@src="/img/pay/credit-card.png"]'

        self.success_msg                        = By.XPATH, '//*[@src="/img/smallIcon/check-green.svg"]/../div[text()="Purchase Successful!"]'
        self.back_to_overview_btn               = By.XPATH, '//button[text()="Back to Overview"]'

    def click_on_checkout_btn(self):
        wait_element(self.driver, self.checkout_btn).click()

    def click_on_next_btn(self):
        wait_element(self.driver, self.next_btn).click()

    def choose_paynow_payment_method(self):
        wait_element(self.driver, self.paynow_method).click()

    def choose_credit_card_payment_method(self):
        wait_element(self.driver, self.credit_card_method).click()

    def is_purchase_successful(self):
        return elementIsDisplayed(self.driver, self.success_msg)

    def click_on_back_to_overview_btn(self):
        wait_element(self.driver, self.back_to_overview_btn).click()

