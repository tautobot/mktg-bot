import calendar
import datetime
from random import choice

from selenium.webdriver.common.by import By

from aqa.utils.enums import path
from aqa.utils.webdriver_util import scroll_to_bottom, wait_element, findElements_xpath, wait
from aqa.utils.generic import generate_nricfin, write_to_file, generate_mobile_sgd, generate_mobile_phl, cal_year


class FlepPersonalInfoPage():
    def __init__(self, driver):
        self.driver                = driver
        self.first_name            = By.NAME, 'first_name'
        self.last_name             = By.NAME, 'last_name'
        self.nricfin               = By.NAME, 'nricfin'
        self.mobile                = By.NAME, 'mobile'
        self.postalcode            = By.NAME, 'postalcode'
        self.email                 = By.NAME, 'email'
        self.address               = By.NAME, 'address1'
        self.next_btn              = By.XPATH, '//*[text()="NEXT"]'
        self.checkbox_confirm      = By.XPATH, '//*[contains(text(),"Yes, I confirm")]/../../div[1]'
        self.checkbox_understand   = By.XPATH, '//*[contains(text(),"I understand")]/../../div[1]'  



    def input_personal_info(self, nricfin=None):
        wait_element(self.driver,self.first_name).send_keys('flep')
        wait_element(self.driver,self.last_name).send_keys('aqa')

        nric = generate_nricfin() if nricfin == None else nricfin
        wait_element(self.driver,self.nricfin).send_keys(nric)

        mobile_number = generate_mobile_sgd()
        wait_element(self.driver,self.mobile).send_keys(mobile_number)
        wait_element(self.driver,self.email).send_keys(f'{nric}@gigacover.com')

        gender_list = ['Male', 'Female']
        g = choice(gender_list)
        gender = wait_element(self.driver, (By.XPATH, f'//*[text()="{g}"]'))
        gender.click()

        wait_element(self.driver,self.address).send_keys('some address')
        wait_element(self.driver,self.postalcode).send_keys('123456')

    def click_all_checkbox(self):
        wait_element(self.driver,self.checkbox_confirm).click()
        wait_element(self.driver,self.checkbox_understand).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()


class PaPersonalInfoPage():
    def __init__(self, driver):
        self.driver                 = driver
        self.first_name             = By.NAME, 'first_name'
        self.last_name              = By.NAME, 'last_name'
        self.nricfin                = By.NAME, 'nricfin'
        self.mobile                 = By.NAME, 'mobile'
        self.postalcode             = By.NAME, 'postalcode'
        self.email                  = By.NAME, 'email'
        self.address                = By.NAME, 'address1'
        self.dob                    = By.XPATH, '//*[text()="Date of Birth"]/following-sibling::div'
        self.date_picker_year       = By.XPATH, '//*[contains(@class, "MuiPickersToolbarButton-toolbarBtn")][1]'
        self.ok_btn                 = By.XPATH, '//*[text()="OK"]'
        self.next_btn               = By.XPATH, '//*[text()="NEXT"]'
        self.checkbox_confirm       = By.XPATH, '//*[contains(text(),"Yes, I confirm")]/../../div[1]'
        self.checkbox_understand    = By.XPATH, '//*[contains(text(),"I understand")]/../../div[1]'
        self.year_1990              = By.XPATH, '//*[text()="1990"]'


    def input_personal_info(self, nricfin=None):
        wait_element(self.driver,self.first_name).send_keys('pa')
        wait_element(self.driver,self.last_name).send_keys('aqa')

        nric = generate_nricfin() if nricfin == None else nricfin
        wait_element(self.driver,self.nricfin).send_keys(nric)

        mobile_number = generate_mobile_sgd()
        wait_element(self.driver,self.mobile).send_keys(mobile_number)
        wait_element(self.driver,self.email).send_keys(f'{nric}@gigacover.com')
        wait_element(self.driver,self.dob).click()
        wait_element(self.driver,self.date_picker_year).click()
        wait_element(self.driver,self.year_1990).click()
        wait_element(self.driver,self.ok_btn).click()

        gender_list = ['Male', 'Female']
        g = choice(gender_list)
        gender = wait_element(self.driver,(By.XPATH, f'//*[text()="{g}"]'))
        gender.click()

        wait_element(self.driver,self.address).send_keys('some address')
        wait_element(self.driver,self.postalcode).send_keys('123456')

    def click_all_checkbox(self):
        wait_element(self.driver,self.checkbox_confirm).click()
        wait_element(self.driver,self.checkbox_understand).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()


class CdwPersonalInfoPage():
    def __init__(self, driver):
        self.driver                              = driver
        self.first_name                          = By.NAME, 'first_name'
        self.last_name                           = By.NAME, 'last_name'
        self.dob                                 = By.XPATH, '//*[text()="Date of Birth"]/following-sibling::div'
        self.date_picker_year                    = By.XPATH, '//*[contains(@class, "MuiPickersToolbarButton-toolbarBtn")][1]'
        self.ok_btn                              = By.XPATH, '//*[text()="OK"]'
        self.cdwy_ok_btn                         = By.XPATH, '//*[text()="Ok"]'
        self.year_1990                           = By.XPATH, '//*[text()="1990"]'
        self.nricfin                             = By.NAME, 'nricfin'
        self.mobile                              = By.NAME, 'mobile'
        self.postalcode                          = By.NAME, 'postalcode'
        self.email                               = By.NAME, 'email'
        self.address                             = By.NAME, 'address1'
        self.cdwy_address                        = By.NAME, 'address'
        self.vehicle_reg                         = By.NAME, 'vehicle_reg'
        self.next_btn                            = By.XPATH, '//*[text()="NEXT"]'
        self.checkbox_reviewed                   = By.XPATH, '//*[contains(text(),"I have reviewed the")]/../../div[1]'
        self.checkbox_understand                 = By.XPATH, '//*[contains(text(),"I understand")]/../../div[1]'
        self.cdwy_checkbox_reviewed              = By.XPATH, '//*[contains(text(),"I have reviewed the")]/../..'
        self.cdwy_checkbox_providing_information = By.XPATH, '//*[contains(text(),"By providing the information")]/../..'


    def input_personal_info(self, nricfin=None, is_cdwy=False):
        wait_element(self.driver,self.first_name).send_keys('cdw')
        wait_element(self.driver,self.last_name).send_keys('aqa')

        nric = generate_nricfin() if nricfin == None else nricfin
        wait_element(self.driver,self.nricfin).send_keys(nric)

        mobile_number = generate_mobile_sgd()
        wait_element(self.driver,self.mobile).send_keys(mobile_number)
        wait_element(self.driver,self.email).send_keys(f'{nric}@gigacover.com')
        wait_element(self.driver,self.dob).click()

        if is_cdwy:
            wait()
            today = datetime.date.today().day
            wait_element(self.driver, (By.XPATH, f'//button[text()="{today}"]')).click()
        else:
            wait_element(self.driver,self.date_picker_year).click()
            wait_element(self.driver,self.year_1990).click()
            wait_element(self.driver,self.ok_btn).click()

        wait_element(self.driver,self.cdwy_address).send_keys('some address') if is_cdwy else wait_element(self.driver,self.address).send_keys('some address')

        gender_list = ['Male', 'Female']
        g = choice(gender_list)
        gender = wait_element(self.driver,(By.XPATH, f'//*[text()="{g}"]'))
        gender.click()

        wait_element(self.driver,self.postalcode).send_keys('123456')
        if not is_cdwy:
            wait_element(self.driver,self.vehicle_reg).send_keys(f'{nric}')

    def click_all_checkbox(self):
        wait_element(self.driver,self.checkbox_reviewed).click()
        wait_element(self.driver,self.checkbox_understand).click()

    def cdwy_click_all_checkbox(self):
        wait_element(self.driver,self.cdwy_checkbox_reviewed).click()
        wait_element(self.driver,self.cdwy_checkbox_providing_information).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()


class PmlYourInformationPage():
    def __init__(self, driver):
        self.driver                = driver
        self.check_box             = '//*[@type="checkbox"]'
        self.success_msg           = By.XPATH, '//*[text()="Congratulations"]'
        self.fname                 = By.NAME, 'first_name'
        self.lname                 = By.NAME, 'last_name'
        self.gender                = By.NAME, 'gender'
        self.nricfin               = By.NAME, 'nricfin'
        self.mobile                = By.NAME, 'mobile'
        self.email                 = By.NAME, 'email'
        self.address1              = By.NAME, 'address1'
        self.postalcode            = By.NAME, 'postalcode'
        self.vehicle_reg           = By.NAME, 'vehicle_reg'
        self.dob                   = By.XPATH, '//*[text()="Birthday"]/..//div[@class="datePickContainer"]'
        self.plan                  = By.XPATH, '//*[@name="plan"]'
        self.ok_btn                = By.XPATH, '//*[text()="ok"]'
        self.daily_benefit_80      = By.XPATH, '//option[text()="$80 daily benefit"]'
        self.start_date            = By.XPATH, '//*[text()="Policy start date"]/..//div[@class="datePickContainer"]'
        self.checkout_btn          = By.XPATH, '//*[text()="CHECKOUT"]'
        self.cash_benefit          = By.XPATH, '//*[text()="Cash Benefit"]/../following-sibling::div'
        self.pay_securely_now_btn  = By.XPATH, '//*[text()="PAY SECURELY NOW"]'
        self.iframe                = 'stripe_checkout_app'


    def input_information(self):
        wait_element(self.driver,self.fname).send_keys('pml')
        wait_element(self.driver,self.lname).send_keys('aqa')
        wait_element(self.driver,self.dob).click()
        wait_element(self.driver,self.ok_btn).click()

        gender_list = ['Male', 'Female']
        a = choice(gender_list)
        wait_element(self.driver,self.gender).click()
        gender = wait_element(self.driver,(By.XPATH, f'//option[text()="{a}"]'))
        gender.click()

        nric = generate_nricfin()
        write_to_file(nric, '/tmp/aqa/pml_nricfin')
        wait_element(self.driver,self.nricfin).send_keys(nric)
        wait_element(self.driver,self.mobile).send_keys(generate_mobile_sgd())
        wait_element(self.driver,self.email).send_keys(f'{nric}@gigacover.com')
        wait_element(self.driver,self.address1).send_keys('some address')
        wait_element(self.driver,self.postalcode).send_keys('123456')
        wait_element(self.driver,self.start_date).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.vehicle_reg).send_keys(f'SH{nric}')

        scroll_to_bottom(self.driver)

    def click_policy_checkbox(self):
        check_boxs = findElements_xpath(self.driver,self.check_box)
        for i in check_boxs:  # click all check box
            i.click()

    def click_checkout_btn(self):
        wait_element(self.driver,self.checkout_btn).click()


class ZeekYourInformationPage():
    def __init__(self, driver):
        self.driver                = driver
        self.fname                 = By.NAME, 'first_name'
        self.lname                 = By.NAME, 'last_name'
        self.gender                = By.NAME, 'gender'
        self.nricfin               = By.NAME, 'nricfin'
        self.mobile                = By.NAME, 'mobile'
        self.email                 = By.NAME, 'email'
        self.address1              = By.NAME, 'address1'
        self.postalcode            = By.NAME, 'postalcode'
        self.ok_btn                = By.XPATH, '//*[text()="ok"]'
        self.start_date            = By.XPATH, '//*[text()="Policy start date"]/following-sibling::div[1]'
        self.checkbox_confirm      = By.XPATH, '//*[contains(text(),"Yes, I confirm")]/../button'
        self.checkbox_understand   = By.XPATH, '//*[contains(text(),"I understand")]/../button'
        self.checkout_now_btn      = By.XPATH, '//*[text()="CHECKOUT NOW"]'
        self.success_msg           = By.XPATH,'//*[text()="Congratulations"]'
        self.iframe                = 'stripe_checkout_app'

    def input_information(self, nricfin=None):
        wait_element(self.driver,self.fname).send_keys('aqa')
        wait_element(self.driver,self.lname).send_keys('zeek venta')

        gender_list = ['Male', 'Female']
        a = choice(gender_list)
        wait_element(self.driver,self.gender).click()
        gender = wait_element(self.driver,(By.XPATH, f'//option[text()="{a}"]'))
        gender.click()

        nric = generate_nricfin() if nricfin == None else nricfin
        wait_element(self.driver,self.nricfin).send_keys(nric)
        wait_element(self.driver,self.mobile).send_keys(generate_mobile_sgd())
        wait_element(self.driver,self.email).send_keys(f'{nric}@gigacover.com')
        wait_element(self.driver,self.address1).send_keys('some address')
        wait_element(self.driver,self.postalcode).send_keys('123456')
        wait_element(self.driver,self.start_date).click()
        wait_element(self.driver,self.ok_btn).click()

        scroll_to_bottom(self.driver)

    def click_policy_checkbox(self):
        wait_element(self.driver,self.checkbox_confirm).click()
        wait_element(self.driver,self.checkbox_understand).click()

    def click_checkout_now_btn(self):
        wait_element(self.driver,self.checkout_now_btn).click()


class HealthYourInformationPage():
    def __init__(self, driver):
        self.driver                       = driver
        self.fname                        = By.NAME, 'first_name'
        self.lname                        = By.NAME, 'last_name'
        self.mname                        = By.NAME, 'middle_name'
        self.mobile                       = By.NAME, 'mobile'
        self.email                        = By.NAME, 'email'
        self.suffix                       = By.NAME, 'suffix'
        self.marital_status               = By.NAME, 'marital_status'

        self.dependent_first_name         = By.NAME, 'd_first_name_0'
        self.dependent_last_name          = By.NAME, 'd_last_name_0'
        self.dependent_middle_name        = By.NAME, 'd_middle_name_0'
        self.dependent_relationship       = By.NAME, 'd_relationship_0'
        self.dependent_gender             = By.NAME, 'd_gender_0'
        self.dependent_marital_status     = By.NAME, 'd_marital_status_0'

        self.dependent_two_first_name     = By.NAME, 'd_first_name_1'
        self.dependent_two_middle_name    = By.NAME, 'd_middle_name_1'
        self.dependent_two_last_name      = By.NAME, 'd_last_name_1'
        self.dependent_two_relationship   = By.NAME, 'd_relationship_1'
        self.dependent_two_gender         = By.NAME, 'd_gender_1'
        self.dependent_two_marital_status = By.NAME, 'd_marital_status_1'

        self.next_btn                     = By.XPATH, '//*[text()="NEXT"]'
        self.primary_dob                  = By.XPATH, '(//*[text()="Date of Birth"]/following-sibling::div//button)[1]'
        self.dependent_dob                = By.XPATH, '(//*[text()="Date of Birth"]/following-sibling::div//button)[2]'
        self.choose_year                  = By.XPATH, '//*[text()="Select Month"]'
        self.ok_btn                       = By.XPATH, '//*[text()="OK"]'


    def input_dob(self):
        wait_element(self.driver,self.primary_dob).click()
        currentMonth = datetime.datetime.now().strftime('%B')

        #choose year
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - 1994"]')).click()
        wait_element(self.driver, self.choose_year).click()
        random_year = choice(list(range(1989, 1997)))
        wait_element(self.driver, f'//*[text()="{random_year}"]').click()

        #choose month
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - 1994"]')).click()
        random_month = choice(list(range(1, 13)))
        month = calendar.month_name[random_month]
        wait_element(self.driver, f'//*[text()="{month}"]').click()

        #choose date
        random_date = choice(list(range(1, 28)))
        wait_element(self.driver, f'//button[text()="{random_date}"]').click()

    def input_primary_information(self):
        wait_element(self.driver,self.fname).send_keys('aqa')
        wait_element(self.driver,self.mname).send_keys('health')
        wait_element(self.driver,self.lname).send_keys('primary')

        nric = generate_nricfin()
        wait_element(self.driver,self.mobile).send_keys(generate_mobile_phl())
        wait_element(self.driver,self.email).send_keys(f'{nric.lower()}@gigacover.com')
        wait_element(self.driver,self.suffix).send_keys('suffix')
        wait_element(self.driver,self.marital_status).click()

        #choose random dob from calendar
        wait_element(self.driver,self.primary_dob).click()
        currentMonth = datetime.datetime.now().strftime('%B')

        #choose year
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - 1994"]')).click()
        wait_element(self.driver, self.choose_year).click()
        random_year = choice(list(range(1990, 1997)))
        wait_element(self.driver, (By.XPATH, f'//*[text()="{random_year}"]')).click()

        #choose month
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - {random_year}"]')).click()
        random_month = choice(list(range(1, 13)))
        month = calendar.month_name[random_month]
        wait_element(self.driver, (By.XPATH, f'//*[text()="{month}"]')).click()

        #choose date
        random_date = choice(list(range(1, 28)))
        wait_element(self.driver, (By.XPATH, f'//button[text()="{random_date}"]')).click()

        marital_status_list = ['Single', 'Married', 'Divorced', 'Separated', 'Widowed']
        marital_status = choice(marital_status_list)
        wait_element(self.driver, (By.XPATH, f'//*[@value="{marital_status}"]')).click()

    def input_dependent_information(self):
        wait_element(self.driver,self.dependent_first_name).send_keys('aqa')
        wait_element(self.driver,self.dependent_middle_name).send_keys('exo')
        wait_element(self.driver,self.dependent_last_name).send_keys('dependent')

        relationship_list = ['Spouse', 'Parent', 'Children', 'Sibling', 'Others']
        relationship = choice(relationship_list)
        wait_element(self.driver,self.dependent_relationship).click()
        wait_element(self.driver,(By.XPATH, f'(//option[text()="{relationship}"])[1]')).click()

        gender_list = ['Male', 'Female']
        gender = choice(gender_list)
        wait_element(self.driver, self.dependent_gender).click()
        wait_element(self.driver, (By.XPATH, f'(//option[text()="{gender}"])[last()]')).click()

        #choose random dob from calendar
        wait_element(self.driver,self.dependent_dob).click()
        currentMonth = datetime.datetime.now().strftime('%B')

        #choose year
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - 1994"]')).click()
        wait_element(self.driver, self.choose_year).click()
        random_year = choice(list(range(1990, 1997)))
        wait_element(self.driver, (By.XPATH, f'//*[text()="{random_year}"]')).click()

        #choose month
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - {random_year}"]')).click()
        random_month = choice(list(range(1, 13)))
        month = calendar.month_name[random_month]
        wait_element(self.driver, (By.XPATH, f'//*[text()="{month}"]')).click()

        #choose date
        random_date = choice(list(range(1, 28)))
        wait_element(self.driver, (By.XPATH, f'//button[text()="{random_date}"]')).click()

        wait_element(self.driver,self.dependent_marital_status).click()
        marital_status_list = ['Single', 'Married', 'Divorced', 'Separated', 'Widowed']
        marital_status = choice(marital_status_list)
        wait_element(self.driver, (By.XPATH, f'(//*[@value="{marital_status}"])[last()]')).click()

    def input_dependent_two_information(self):
        wait_element(self.driver,self.dependent_two_first_name).send_keys('aqa')
        wait_element(self.driver,self.dependent_two_middle_name).send_keys('exo')
        wait_element(self.driver,self.dependent_two_last_name).send_keys('dependent two')

        relationship_list = ['Spouse', 'Parent', 'Children', 'Sibling', 'Others']
        relationship = choice(relationship_list)
        wait_element(self.driver,self.dependent_two_relationship).click()
        wait_element(self.driver,(By.XPATH, f'(//option[text()="{relationship}"])[2]')).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()


class PetYourInformationPage():
    def __init__(self, driver):
        self.driver                      = driver
        self.fname                       = By.NAME, 'first_name'
        self.lname                       = By.NAME, 'last_name'
        self.gender                      = By.NAME, 'gender'
        self.civil_status_dropdown       = By.NAME, 'civilStatus'
        self.address                     = By.NAME, 'address'
        self.occupation                  = By.NAME, 'occupation'
        self.mobile                      = By.NAME, 'mobile'
        self.email                       = By.NAME, 'email'
        self.beneficiary_name            = By.NAME, 'beneficiaryName'
        self.relationship_with_pet_owner = By.NAME, 'relationshipWithPetOwner'
        self.beneficiary_address         = By.NAME, 'beneficiaryAddress'

        self.dob                         = By.XPATH, '(//*[text()="Birthdate"]/following-sibling::div//button)[1]'
        self.same_address_btn            = By.XPATH, '//*[contains(text(), "Same as to my Complete Home Address ")]/../button'

        self.origin_dropdown             = By.NAME, 'origin'
        self.clinic                      = By.NAME, 'clinic'

        self.certificate                 = '//*[@name="certificate"]'
        self.ok_btn                      = By.XPATH, '//*[text()="Ok"]'
        self.next_btn                    = By.XPATH, '//button[text()="NEXT"]'
        self.primary_dob                 = By.XPATH, '(//*[text()="Date of Birth"]/following-sibling::div//button)[1]'
        self.dependent_dob               = By.XPATH, '(//*[text()="Date of Birth"]/following-sibling::div//button)[2]'
        self.choose_year                 = By.XPATH, '//*[text()="Select Month"]'
        self.year_left_btn               = By.XPATH, '//*[text()="Select Year"]/../button[1]'


    def input_personal_information(self):
        # personal info
        wait_element(self.driver, self.fname).send_keys('aqa')
        wait_element(self.driver, self.lname).send_keys('pet')

        #choose random dob from calendar
        wait_element(self.driver,self.dob).click()
        currentMonth = datetime.datetime.now().strftime('%B')
        currentYear = datetime.datetime.now().strftime('%Y')
        currentYear_2digit = datetime.datetime.now().strftime('%y')

        #choose year
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - {currentYear}"]')).click()
        wait_element(self.driver, self.choose_year).click()

        wait_element(self.driver, self.year_left_btn).click()
        wait_element(self.driver, self.year_left_btn).click()
        wait_element(self.driver, self.year_left_btn).click()

        random_year = choice(list(range(int(currentYear) - 30, int(currentYear) - int(currentYear_2digit))))
        wait_element(self.driver, (By.XPATH, f'//*[text()="{random_year}"]')).click()

        #choose month
        wait_element(self.driver,(By.XPATH, f'//*[text()="{currentMonth} - {random_year}"]')).click()
        random_month = choice(list(range(1, 13)))
        month = calendar.month_name[random_month]
        wait_element(self.driver, (By.XPATH, f'//*[text()="{month}"]')).click()

        #choose date
        random_date = choice(list(range(1, 28)))
        wait_element(self.driver, (By.XPATH, f'//button[text()="{random_date}"]')).click()

        gender_list = ['Male', 'Female']
        a = choice(gender_list)
        wait_element(self.driver,self.gender).click()
        gender = wait_element(self.driver,(By.XPATH, f'//option[text()="{a}"]'))
        gender.click()

        wait_element(self.driver, self.civil_status_dropdown).click()
        civil_status_list = ['Single', 'Married', 'Divorced', 'Separated', 'Widowed']
        civil_status = choice(civil_status_list)
        wait_element(self.driver, (By.XPATH, f'//option[@value="{civil_status}"]')).click()

        wait_element(self.driver, self.address).send_keys('address')
        wait_element(self.driver, self.occupation).send_keys('occupation')

        # contact info
        wait_element(self.driver,self.mobile).send_keys(generate_mobile_phl())
        wait_element(self.driver,self.email).send_keys(f'{generate_nricfin()}@gigacover.com')

        # beneficiary info
        wait_element(self.driver,self.beneficiary_name).send_keys('beneficiary name')

        relationship_list = ['Spouse', 'Parent', 'Child', 'Sibling']
        relationship = choice(relationship_list)
        wait_element(self.driver,self.relationship_with_pet_owner).click()
        wait_element(self.driver,(By.XPATH, f'(//option[text()="{relationship}"])[1]')).click()

        wait_element(self.driver,self.beneficiary_address).send_keys('beneficiary address')

        wait_element(self.driver, self.next_btn).click()

    def input_pet_information(self):
        # choose random dob from calendar
        wait_element(self.driver, self.dob).click()
        currentMonth = datetime.datetime.now().strftime('%B')
        currentYear = datetime.datetime.now().strftime('%Y')

        # choose year
        wait_element(self.driver, (By.XPATH, f'//*[text()="{currentMonth} - {currentYear}"]')).click()
        wait_element(self.driver, self.choose_year).click()

        random_year = int(currentYear) - 1
        wait_element(self.driver, (By.XPATH, f'//*[text()="{random_year}"]')).click()

        # choose month
        wait_element(self.driver, (By.XPATH, f'//*[text()="{currentMonth} - {random_year}"]')).click()
        random_month = choice(list(range(1, 13)))
        month = calendar.month_name[random_month]
        wait_element(self.driver, (By.XPATH, f'//*[text()="{month}"]')).click()

        # choose date
        random_date = choice(list(range(1, 28)))
        wait_element(self.driver, (By.XPATH, f'//button[text()="{random_date}"]')).click()

        gender_list = ['Male', 'Female']
        a = choice(gender_list)
        wait_element(self.driver,self.gender).click()
        gender = wait_element(self.driver,(By.XPATH, f'//option[text()="{a}"]'))
        gender.click()

        wait_element(self.driver, self.clinic).send_keys('Vet Clinics / Grooming Clinics Visited')

        certificate = findElements_xpath(self.driver, self.certificate)
        certificate[0].send_keys(f'{path.fixture_dir}/1.jpg')
        wait_element(self.driver, self.next_btn).click()
