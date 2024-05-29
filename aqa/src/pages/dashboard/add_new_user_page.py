from random import choice

from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, findElements_xpath
from aqa.utils.generic import generate_mobile_phl, generate_nricfin, generate_mobile_sgd


class DashboardAddNewUserPage():

    def __init__(self, driver):
        self.driver                                = driver
        self.inputFile                             = '//input[@type="file"]'
        self.error_msg                             = '//*[@role="rowgroup"]//*[contains(@class, "text-red-600")]/div'
        self.individual_onboarding_btn             = By.XPATH, '//*[text()="Individual Onboarding"]'
        self.bulk_onboarding_btn                   = By.XPATH, '//*[text()="Bulk Onboarding"]'
        self.dependent_success_msg                 = By.XPATH, '//*[@class="DependentDetail"]'
        self.first_name                            = By.ID, 'firstName'
        self.last_name                             = By.ID, 'lastName'
        self.employeeEmail                         = By.ID, 'email'
        self.mobile                                = By.ID, 'mobile'
        self.dob                                   = By.XPATH, '//*[text()="Date of Birth"]/following-sibling::div'
        self.okBtn                                 = By.XPATH, '//*[text()="OK"]'
        self.employeeRank                          = By.XPATH, '//*[text()="Employee Rank"]/following-sibling::div'
        self.effectiveDate                         = By.XPATH, '//*[text()="Effective Date"]/following-sibling::div'
        self.next_btn                              = By.XPATH, '//*[text()="Next"]'
        self.back_btn                              = By.XPATH, '//*[text()="Back"]'
        self.uploadCsvBtn                          = By.XPATH, '//*[text()="UPLOAD CSV. FILE"]'
        self.enrollBtnPopup                        = By.XPATH, '//*[@class="btText " and text()="ENROLL"]'
        self.success_msg                           = By.XPATH, '//img[@src="/img/icon/check-green.svg"]/../div[1]'
        self.dependent_fname                       = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="First Name"]/following-sibling::div/input'
        self.dependent_lname                       = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="Last Name"]/following-sibling::div/input'
        self.dependent_dob                         = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="Date of Birth"]/following-sibling::div'
        self.dependent_gender                      = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="Gender"]/following-sibling::div'
        self.dependent_IdTypeDropdown              = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="ID Type (Passport / UMID / etc)"]/following-sibling::div'
        self.dependent_OtherIdType                 = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="ID Type Name"]/following-sibling::div/input'
        self.dependent_IdName                      = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="ID Name"]/following-sibling::div/input'
        self.dependent_IdNumber                    = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="ID Number"]/following-sibling::div/input'
        self.dependent_email                       = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="Email Address"]/following-sibling::div/input'
        self.dependent_effectiveDate               = By.XPATH, '//*[@class="EnrollDependentForm"]//div[text()="Effective Date"]/following-sibling::div'

        #essentials
        self.employee_name                         = By.NAME, 'employee_name'
        self.email                                 = By.NAME, 'email'
        self.mobile                                = By.NAME, 'mobile'
        self.identification_no                     = By.NAME, 'identification_no'
        self.employee_no                           = By.NAME, 'employee_no'
        self.dependents_allowed                    = By.XPATH, '//*[@name="dependents_allowed"]/../div'
        self.gender                                = By.XPATH, '//*[@name="gender"]/../div'
        self.start_date_of_coverage                = By.XPATH, '(//*[@id="date-picker-dialog"])[1]/..'
        self.dob                                   = By.XPATH, '(//*[@id="date-picker-dialog"])[2]/..'
        self.submit_btn                            = By.XPATH, '//*[text()="Submit"]'
        self.enrol_success_msg                     = By.XPATH, '//*[@id="approve-success"]//p'

    def click_on_individual_onboarding_btn(self):
        wait_element(self.driver, self.individual_onboarding_btn).click()

    def click_on_bulk_onboarding_btn(self):
        wait_element(self.driver, self.bulk_onboarding_btn).click()

    def individual_onboarding_employee(self):
        wait_element(self.driver, self.individual_onboarding_btn).click()

        wait_element(self.driver,self.first_name).send_keys('eb')
        wait_element(self.driver,self.last_name).send_keys('aqa')
        wait_element(self.driver,self.dob).click()
        wait_element(self.driver,self.okBtn).click()

        email = f'{generate_nricfin()}@gigacover.com'
        wait_element(self.driver,self.employeeEmail).send_keys(email)

        mobile_number = generate_mobile_phl()
        wait_element(self.driver,self.mobile).send_keys(mobile_number)

        rank_option_list = ['Manager', 'BOD', 'Senior Manager', 'Staff', 'Management', 'Middle Management']
        rank = choice(rank_option_list)
        wait_element(self.driver,self.employeeRank).click()
        wait_element(self.driver,(By.XPATH, f'//option[text()="{rank}"]')).click()

        wait_element(self.driver,self.effectiveDate).click()

        wait_element(self.driver,self.okBtn).click()

        wait_element(self.driver, self.next_btn).click()

    def click_back_btn(self):
        wait_element(self.driver,self.back_btn).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()

    def add_employee_successful_msg(self):
        return wait_element(self.driver,self.success_msg).text

    def validation_error_msg(self):
        errors_msg = findElements_xpath(self.driver, self.error_msg)
        return errors_msg

    def enroll_by_excel(self, file):
        upload_file = findElements_xpath(self.driver, self.inputFile)[0]
        upload_file.send_keys(file)

    def essential_input_employee_info(self, name):
        wait_element(self.driver, self.employee_name).send_keys(name)
        wait_element(self.driver, self.email).send_keys(f'{name}@gigacover.com')

        wait_element(self.driver, self.dependents_allowed).click()
        yes_no_option = choice(['Yes', 'No'])
        wait_element(self.driver, (By.XPATH, f'//li[text()="{yes_no_option}"]')).click()

        wait_element(self.driver, self.mobile).send_keys(generate_mobile_sgd())
        wait_element(self.driver, self.identification_no).send_keys(name)

        wait_element(self.driver, self.start_date_of_coverage).click()
        wait_element(self.driver, self.okBtn).click()

        wait_element(self.driver, self.employee_no).send_keys(name)

        wait_element(self.driver, self.dob).click()
        wait_element(self.driver, self.okBtn).click()

        wait_element(self.driver, self.gender).click()
        gender_option = choice(['Male', 'Female'])
        wait_element(self.driver, (By.XPATH, f'//li[text()="{gender_option}"]')).click()

        wait_element(self.driver, self.submit_btn).click()

    def get_essentials_enrol_success_msg(self):
        return wait_element(self.driver, self.enrol_success_msg).text
