from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from aqa.utils.webdriver_util import wait_element, wait, findElements_xpath


class WebPortalHomePage():
    def __init__(self, driver):
        self.driver = driver
        self.product_list                   = '//*[text()="Your Coverage"]/following-sibling::div/button'
        self.pa_product                     = By.XPATH, '//*[text()="Personal Accident"]'
        self.flep_product                   = By.XPATH, '//*[text()="Freelancer Earnings Protection"]'
        self.cdw_product                    = By.XPATH, '//*[text()="Collision Damage Waiver"]'
        self.termlife_product               = By.XPATH, '//*[text()="Term Life"]'
        self.essentials_product             = By.XPATH, '//*[text()="Essentials"]'
        self.eb_product                     = By.XPATH, '//*[text()="Comprehensive HMO"]'
        self.health_product                 = By.XPATH, '//*[text()="Health"]'
        self.claim_icon                     = By.XPATH, '//*[text()="Claims"]'
        self.my_insurance                   = By.XPATH, '//*[text()="My Insurance"]'
        self.add_dependent_btn              = By.XPATH, '//*[text()="+ Add Dependent"]'
        self.add_credit_card_btn            = By.XPATH, '//button[text()="+ADD CREDIT CARD"]'
        self.activate_Ecard_btn             = By.XPATH, '//button[text()="ACTIVATE E-CARD"]'
        self.got_it_btn                     = By.XPATH, '//button[text()="GOT IT"]'
        self.iframe_card_number             = By.XPATH, '//iframe[@title="Secure card number input frame"]'
        self.iframe_expiry_date             = By.XPATH, '//iframe[@title="Secure expiration date input frame"]'
        self.iframe_cvc                     = By.XPATH, '//iframe[@title="Secure CVC input frame"]'
        self.card_name                      = By.NAME, 'cardName'
        self.card_number                    = By.NAME, 'cardNumber'
        self.exp_date                       = By.NAME, 'cardExpiry'
        self.cvc                            = By.NAME, 'cardCvc'

        self.cdw_plus_product               = By.XPATH, '//*[text()="Collision Damage Waiver Extension"]'

    def go_to_claim_page(self):
        wait_element(self.driver,self.claim_icon).click()

    def go_to_my_insurance_page(self):
        wait_element(self.driver,self.my_insurance).click()

    def get_product_list(self):
        return findElements_xpath(self.driver, self.product_list)

    def click_on_pa_product(self):
        wait_element(self.driver,self.pa_product).click()

    def click_on_flep_product(self):
        wait_element(self.driver,self.flep_product).click()

    def click_on_cdw_product(self):
        wait_element(self.driver,self.cdw_product).click()

    def click_on_cdw_plus_product(self):
        wait_element(self.driver,self.cdw_plus_product).click()

    def click_on_termlife_product(self):
        wait_element(self.driver,self.termlife_product).click()

    def click_on_essentials_product(self):
        wait_element(self.driver,self.essentials_product).click()

    def click_on_eb_product(self):
        wait_element(self.driver,self.eb_product).click()

    def click_on_health_product(self):
        wait_element(self.driver,self.health_product).click()

    def click_on_add_dependent_btn(self):
        wait_element(self.driver,self.add_dependent_btn).click()

    def active_Ecard(self):
        wait_element(self.driver,self.add_credit_card_btn).click()
        wait_element(self.driver,self.card_name).send_keys('Test aqa')

        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys(Keys.END)
        wait_element(self.driver,self.card_number).send_keys('4444')

        wait_element(self.driver,self.exp_date).send_keys('1234')
        wait_element(self.driver,self.cvc).send_keys('123')

        wait_element(self.driver,self.activate_Ecard_btn).click()

    def click_on_got_it_btn(self):
        wait_element(self.driver, self.got_it_btn).click()
