from selenium.webdriver.common.by import By
from aqa.utils.webdriver_util import wait_element

class WebPortalClaimPage():
    def __init__(self, driver):
        self.driver             = driver
        self.eb_product         = By.XPATH, '//*[text()="COMPREHENSIVE HMO"]'
        self.health_product     = By.XPATH, '//*[text()="HEALTH"]'
        self.pa_product         = By.XPATH, '//div[text()="PERSONAL ACCIDENT"]'
        self.flep_product       = By.XPATH, '//div[text()="FLEP"]'
        self.cdw_product        = By.XPATH, '//div[text()="CDW"]'
        self.pml_product        = By.XPATH, '//div[text()="PML"]'
        self.termlife_product   = By.XPATH, '//div[text()="TERM LIFE"]'
        self.ip_popup           = By.XPATH, '//*[text()="IN-PATIENT"]'
        self.op_popup           = By.XPATH, '//*[text()="OUT-PATIENT"]'
        self.product_name       = By.XPATH, '//*[@alt="ClaimProductButton"]/..'
        self.hospital_type      = By.XPATH, '//*[text()="Hospital Leave"]'
        self.medical_type       = By.XPATH, '//*[text()="Medical Leave"]'
        self.covid_type         = By.XPATH, '//*[text()="COVID-19"]'
        self.ok_btn             = By.XPATH, '//*[text()="OK"]'
        self.proceed_btn        = By.XPATH, '//*[text()="PROCEED"]'
        self.yes_btn            = By.XPATH, '//*[text()="YES"]'
        self.no_btn             = By.XPATH, '//*[text()="NO"]'

        self.cdw_plus_product   = By.XPATH, '//div[text()="CDW+"]'

    def choose_eb_product(self):
        wait_element(self.driver,self.eb_product).click()

    def choose_health_product(self):
        wait_element(self.driver,self.health_product).click()

    def choose_pa_product(self):
         wait_element(self.driver,self.pa_product).click()

    def choose_flep_product(self):
         wait_element(self.driver,self.flep_product).click()

    def choose_cdw_product(self):
         wait_element(self.driver,self.cdw_product).click()

    def choose_cdw_plus_product(self):
         wait_element(self.driver,self.cdw_plus_product).click()

    def choose_pml_product(self):
         wait_element(self.driver,self.pml_product).click()

    def click_on_proceed_btn(self):
         wait_element(self.driver,self.proceed_btn).click()

    def click_on_yes_btn(self):
         wait_element(self.driver,self.yes_btn).click()

    def click_on_no_btn(self):
         wait_element(self.driver,self.no_btn).click()

    def choose_hospital_type(self):
         wait_element(self.driver,self.hospital_type).click()
         wait_element(self.driver,self.proceed_btn).click()

    def choose_medical_type(self):
         wait_element(self.driver,self.medical_type).click()
         wait_element(self.driver,self.proceed_btn).click()

    def choose_covid_type(self):
         wait_element(self.driver,self.covid_type).click()
         wait_element(self.driver,self.proceed_btn).click()

    def choose_termlife_product(self):
         wait_element(self.driver,self.termlife_product).click()

    def choose_ip_popup(self):
         wait_element(self.driver,self.ip_popup).click()

    def choose_op_popup(self):
         wait_element(self.driver,self.op_popup).click()

    def get_product_name(self):
        return wait_element(self.driver,self.product_name).text
