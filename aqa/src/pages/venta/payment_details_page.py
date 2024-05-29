from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from aqa.utils.webdriver_util import scroll_to_bottom, wait, wait_element, elementIsDisplayed, wait_loading_credit_iframe


class XenditPaymentDetailsPage():
    def __init__(self, driver):
        self.driver                     = driver
        self.successful_msg             = By.XPATH, '//*[text()="CONGRATULATIONS!"]'
        self.failed_msg                 = By.XPATH, '//*[text()="PAYMENT FAILED!"]'
        self.cancelled_msg              = By.XPATH, '//*[text()="PAYMENT CANCELLED"]'
        self.processing_img             = By.XPATH, '//*[contains(@src,"payment-processing")]'
        self.iframe_parent              = By.XPATH,'//*[contains(@title,"iframe")]'
        self.ewallet_option             = By.XPATH, '//*[text()="E-Wallet"]/../../button'
        self.direct_debit_option        = By.XPATH, '//*[text()="Direct Debit"]/../../button'
        self.grabpay                    = By.XPATH, '//*[contains(@src,"grabpay")]/..'
        self.gcash                      = By.XPATH, '//*[contains(@src,"gcash")]/..'
        self.maya                       = By.XPATH, '//*[contains(@src,"maya")]/..'
        self.shopeepay                  = By.XPATH, '//*[contains(@src,"shopeepay")]/..'
        self.bpi_bank                   = By.XPATH, '//*[contains(@src,"bpi")]/..'
        self.union_bank                 = By.XPATH, '//*[contains(@src,"union-bank")]/..'
        self.submit_btn                 = By.XPATH, '//*[@value="SUBMIT"]'
        self.pay_securely_btn           = By.XPATH, '//button[text()="PAY SECURELY NOW"]'
        self.confirm_btn                = By.XPATH, '//button[text()="CONFIRM"]'
        self.credit_card_cancel_button  = By.XPATH, '//*[text()="CANCEL"]'
        self.next_btn                   = By.XPATH, '//*[text()="NEXT"]'
        self.iframe_parent              = By.XPATH, '//*[contains(@title,"iframe")]'
        self.money_bank_login_btn       = By.XPATH, '//*[contains(@class,"bankSubmit")]'
        self.otp_1                      = By.XPATH, '//*[contains(@aria-label,"Digit 1")]'
        self.otp_2                      = By.XPATH, '//*[contains(@aria-label,"Digit 2")]'
        self.otp_3                      = By.XPATH, '//*[contains(@aria-label,"Digit 3")]'
        self.otp_4                      = By.XPATH, '//*[contains(@aria-label,"Digit 4")]'
        self.otp_5                      = By.XPATH, '//*[contains(@aria-label,"Digit 5")]'
        self.otp_6                      = By.XPATH, '//*[contains(@aria-label,"Digit 6")]'
        self.card_number                = By.NAME, 'card_number'
        self.expiry_date                = By.NAME, 'expiry_date'
        self.cvn_number                 = By.NAME, 'cvn_number'
        self.otp_code                   = By.NAME, 'challengeDataEntry'
        self.money_bank_client_ID       = By.NAME, 'username'
        self.money_bank_password        = By.NAME, 'password'
        self.otp                        = By.NAME, 'challengeDataEntry'
        self.proceed_button             = By.ID, 'proceed-button'
        self.ewallet_cancel_button      = By.ID, 'cancel-button'
        self.iframe                     = 'Cardinal-CCA-IFrame'

        self.pet_ewallet_option         = By.XPATH, '//*[text()="E-Wallet"]/../../../button'
        self.pet_direct_debit_option    = By.XPATH, '//*[text()="Direct Debit"]/../../../button'
        self.pet_processing_img         = By.XPATH, '//*[(@src="/img/notice/purchase-pending.png")]'
        self.pet_success_img            = By.XPATH, '//*[(@src="/img/notice/purchase-success.png")]'

    def choose_ewallet_option(self):
        scroll_to_bottom(self.driver)
        wait_element(self.driver,self.ewallet_option).click()

    def choose_ewallet_grabpay(self):
        wait_element(self.driver,self.grabpay).click()

    def choose_ewallet_gcash(self):
        wait_element(self.driver,self.gcash).click()

    def choose_ewallet_paymaya(self):
        wait_element(self.driver,self.maya).click()

    def choose_ewallet_shopeepay(self):
        wait_element(self.driver,self.shopeepay).click()

    def choose_direct_debit_option(self):
        scroll_to_bottom(self.driver)
        wait_element(self.driver,self.direct_debit_option).click()

    def choose_direct_debit_BPI_bank(self):
        wait_element(self.driver,self.bpi_bank).click()

    def choose_direct_debit_Union_bank(self):
        wait_element(self.driver,self.union_bank).click()

    def input_card_details(self):
        scroll_to_bottom(self.driver)
        wait_element(self.driver,self.card_number).send_keys('4000000000001091')
        wait_element(self.driver,self.expiry_date).send_keys('1234')
        wait_element(self.driver,self.cvn_number).send_keys('111')

    def login_direct_debit_with_valid_account(self):
        wait_element(self.driver,self.money_bank_client_ID).send_keys('91284')
        wait_element(self.driver,self.money_bank_password).send_keys('strongpassword')
        wait_element(self.driver,self.money_bank_login_btn).click()

    def login_direct_debit_with_invalid_account(self):
        wait_element(self.driver,self.money_bank_client_ID).send_keys('28284')
        wait_element(self.driver,self.money_bank_password).send_keys('badpassword')
        wait_element(self.driver,self.money_bank_login_btn).click()

    def input_valid_otp(self):
        wait_element(self.driver,self.otp_1).send_keys('2')
        wait_element(self.driver,self.otp_2).send_keys('2')
        wait_element(self.driver,self.otp_3).send_keys('2')
        wait_element(self.driver,self.otp_4).send_keys('0')
        wait_element(self.driver,self.otp_5).send_keys('0')
        wait_element(self.driver,self.otp_6).send_keys('0')
        wait_element(self.driver,self.otp_6).send_keys(Keys.ENTER)


    def input_invalid_otp(self):
        wait_element(self.driver,self.otp_1).send_keys('2')
        wait_element(self.driver,self.otp_2).send_keys('2')
        wait_element(self.driver,self.otp_3).send_keys('2')
        wait_element(self.driver,self.otp_4).send_keys('0')
        wait_element(self.driver,self.otp_5).send_keys('0')
        wait_element(self.driver,self.otp_6).send_keys('2')
        wait_element(self.driver,self.otp_6).send_keys(Keys.ENTER)


    def click_pay_securely_btn(self):
        wait_element(self.driver,self.pay_securely_btn).click()

    def click_proceed_btn(self):
        wait_element(self.driver,self.proceed_button).click()

    def ewallet_click_cancel_btn(self):
        wait_element(self.driver,self.ewallet_cancel_button).click()

    def credit_card_click_cancel_btn(self):
        wait_element(self.driver,self.credit_card_cancel_button).click()

    def input_purchase_authentication(self):
        wait_loading_credit_iframe(self.driver)
        iframe_parent = wait_element(self.driver, self.iframe_parent)
        self.driver.switch_to.frame(iframe_parent)

        wait_loading_credit_iframe(self.driver)
        self.driver.switch_to.frame(self.iframe)

        wait_loading_credit_iframe(self.driver)
        wait_element(self.driver,self.otp_code).send_keys('1234')

        wait_element(self.driver,self.otp).send_keys(Keys.ENTER)
        self.driver.switch_to.default_content()

    def click_on_next_btn(self):
        wait_element(self.driver,self.next_btn).click()

    def congratulations_text(self):
        return elementIsDisplayed(self.driver, self.successful_msg)

    def failed_text(self):
        return elementIsDisplayed(self.driver, self.failed_msg)

    def cancelled_text(self):
        return elementIsDisplayed(self.driver, self.cancelled_msg)

    def processing_image(self):
        return elementIsDisplayed(self.driver, self.processing_img)


    def pet_choose_ewallet_option(self):
        scroll_to_bottom(self.driver)
        wait_element(self.driver,self.pet_ewallet_option).click()

    def pet_choose_direct_debit_option(self):
        scroll_to_bottom(self.driver)
        wait_element(self.driver,self.pet_direct_debit_option).click()

    def pet_processing_image(self):
        return elementIsDisplayed(self.driver, self.pet_processing_img)

    def pet_success_text(self):
        return elementIsDisplayed(self.driver, self.pet_success_img)
