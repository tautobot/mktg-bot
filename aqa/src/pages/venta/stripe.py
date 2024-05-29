from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element


class StripeCheckout():
    def __init__(self, driver):
        self.driver               = driver
        self.card_number          = By.ID, 'card_number'
        self.card_date            = By.ID, 'cc-exp' 
        self.card_csc             = By.ID, 'cc-csc' 
        self.pay_btn              = By.ID, 'submitButton' 
        self.pay_now_btn          = By.XPATH, '//*[text()="PAYNOW"]' 
        self.next_btn             = By.XPATH, '//*[text()="NEXT"]'
        self.pay_securely_now_btn = By.XPATH, '//*[text()="PAY SECURELY NOW"]'
        self.iframe               = 'stripe_checkout_app'


    def click_pay_btn(self):
        wait_element(self.driver, self.pay_now_btn).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()

    def click_pay_securely_btn(self):
        wait_element(self.driver,self.pay_securely_now_btn).click()

    def checkout(self):
        self.driver.switch_to.frame(self.iframe)
        amount_charge = wait_element(self.driver, self.pay_btn).text

        wait_element(self.driver, self.card_number).send_keys('4242')
        wait_element(self.driver, self.card_number).send_keys('4242')
        wait_element(self.driver, self.card_number).send_keys('4242')
        wait_element(self.driver, self.card_number).send_keys('4242')

        wait_element(self.driver, self.card_date).send_keys('11')
        wait_element(self.driver, self.card_date).send_keys('25')
        wait_element(self.driver, self.card_csc).send_keys('123')

        wait_element(self.driver, self.pay_btn).click()
        self.driver.switch_to.default_content()
        return amount_charge