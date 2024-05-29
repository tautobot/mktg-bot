from random import choice

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait, wait_element, elementIsDisplayed
from aqa.utils.generic import generate_mobile_sgd, generate_nricfin


class AddDependentPage():
    def __init__(self, driver):
        self.driver = driver

        self.success_msg                    = By.XPATH, '//*[text()="New dependent added"]'
        self.iframe_card_number             = By.XPATH, '//iframe[@title="Secure card number input frame"]'
        self.iframe_expiry_date             = By.XPATH, '//iframe[@title="Secure expiration date input frame"]'
        self.iframe_cvc                     = By.XPATH, '//iframe[@title="Secure CVC input frame"]'
        self.active_Ecard_successful_text   = By.XPATH, '//div[text()="Payment method added"]'
        self.relationship                   = By.NAME, 'relationship'
        self.gender                         = By.NAME, 'gender'
        self.full_name                      = By.NAME, 'fullName'
        self.nricfin                        = By.NAME, 'nricfin'
        self.email                          = By.NAME, 'email'
        self.mobile                         = By.NAME, 'mobile'
        self.card_name                      = By.NAME, 'cardName'
        self.card_number                    = By.NAME, 'cardNumber'
        self.exp_date                       = By.NAME, 'cardExpiry'
        self.cvc                            = By.NAME, 'cardCvc'
        self.activate_Ecard_btn             = By.XPATH, '//button[text()="ACTIVATE E-CARD"]' 
        self.got_it_btn                     = By.XPATH, '//button[text()="GOT IT"]'
        self.error_msg                      = By.XPATH, '//*[@class="error-text"]'
        self.dob                            = By.XPATH, '//*[text()="Date of birth"]/following-sibling::div[1]'
        self.save_button                    = By.XPATH, '//*[text()="Save"]'
        self.ok_btn                         = By.XPATH, '//*[text()="OK"]'
        self.add_btn                        = By.XPATH, '//button[text()="Add"]'
        
        
    def input_dependent_info(self):
        relationship_list = ['Spouse', 'Parent', 'Children', 'Sibling', 'Others']
        relation = choice(relationship_list)
        wait_element(self.driver,self.relationship).click()
        wait_element(self.driver,(By.XPATH, f'//option[text()="{relation}"]')).click()

        wait_element(self.driver,self.full_name).send_keys('test dependent')

        nric = generate_nricfin()
        wait_element(self.driver,self.nricfin).send_keys(nric)

        wait_element(self.driver,self.gender).click()
        gender_list = ['male', 'female']
        a = choice(gender_list)
        gender = wait_element(self.driver,(By.XPATH, f'//option[@value="{a}"]'))
        gender.click()

        wait_element(self.driver,self.email).send_keys(f'{nric}@gigacover.com')

        m = generate_mobile_sgd()
        wait_element(self.driver,self.mobile).send_keys(m)

        wait_element(self.driver,self.dob).click()
        wait_element(self.driver,self.ok_btn).click()

    def click_save_button(self):
        wait_element(self.driver,self.save_button).click()

    def click_add_button(self):
        wait_element(self.driver,self.add_btn).click()

    def click_got_it_button(self):
        wait_element(self.driver,self.got_it_btn).click()

    def active_Ecard(self):
        wait_element(self.driver,self.card_name).send_keys('Test aqa')

        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys(Keys.END)
        wait()
        wait_element(self.driver,self.card_number).send_keys('4444')

        wait_element(self.driver,self.exp_date).send_keys('1234')

        wait_element(self.driver,self.cvc).send_keys('123')

        wait_element(self.driver,self.activate_Ecard_btn).click()

    def is_active_Ecard_successful(self):
        return elementIsDisplayed(self.driver, self.active_Ecard_successful_text)

    def added_dependent_successful(self):
        return elementIsDisplayed(self.driver, self.success_msg)
