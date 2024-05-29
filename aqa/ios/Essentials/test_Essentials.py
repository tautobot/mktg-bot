import unittest
from random import choice

from aQA.iOS.src.app_file.util_ios import login_pouch_ios, wait, wait_xpath, tutorial_welcome, wait_accessibility_id, tutorial_essential, active_E_Card, isDisplayed_id
from testcases.lib.generic import skip_opt, read_cell_in_excel_file, get_default_password, write_to_file, generate_nricfin, read_file, generate_mobile_sgd
from aQA.webdriver.appium_weddriver import *

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = ios_webdriver(app_name='pouch')

    def tearDown(self): self.driver.quit()

    def test_update_information(self):
        excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'
        username = read_cell_in_excel_file(excel_file, f'F2')
        pwd = get_default_password(2)

        login_pouch_ios(self.driver, username, pwd)
        wait()

        wait_accessibility_id(self.driver, 'WelcomeBtStart').click()
        wait_accessibility_id(self.driver, 'WelcomeBtADD NRIC').click()

        #region validate required field
        wait_accessibility_id(self.driver, 'WelcomeInputNric').send_keys('abc123')
        wait_xpath(self.driver, '//*[@name="Return"]').click()
        wait_accessibility_id(self.driver, 'WelcomeBtSave').click()
        assert wait_xpath(self.driver, '//*[@name="Please enter a valid NRIC number"]').is_displayed() is True
        #endregion validate required field

        wait_accessibility_id(self.driver, 'WelcomeInputNric').clear()
        nric = username.split('@')[0]

        #region input valid nricfin and save
        wait_accessibility_id(self.driver, 'WelcomeInputNric').send_keys(nric)
        wait_xpath(self.driver, '//*[@name="Return"]').click()
        wait_accessibility_id(self.driver, 'WelcomeBtSave').click()
        #endregion input valid nricfin and save

        wait()

        #check after add nricfin Pouch can go to next screen
        assert wait_accessibility_id(self.driver, 'WelcomeBtADD PAYMENT METHOD').is_displayed() is True

    def test_update_information_with_existed_nricfin(self):
        excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'
        username = read_cell_in_excel_file(excel_file, f'F3')
        pwd = get_default_password(3)

        login_pouch_ios(self.driver, username, pwd)
        wait()

        wait_accessibility_id(self.driver, 'WelcomeBtStart').click()
        wait_accessibility_id(self.driver, 'WelcomeBtADD NRIC').click()

        nric = read_cell_in_excel_file(excel_file, f'E4') # existed nricfin
        wait_accessibility_id(self.driver, 'WelcomeInputNric').send_keys(nric)

        wait_xpath(self.driver, '//*[@name="Return"]').click()
        wait_accessibility_id(self.driver, 'WelcomeBtSave').click()

        # check app_file raise error if nricfin is existed
        assert wait_xpath(self.driver, '//*[@name="You currently have your nric registered with another account. Please contact hey@gigacover.com for more details!"]').is_displayed() is True

    def test_add_dependent(self):
        username = read_cell_in_excel_file(excel_file, f'F4')
        pwd = read_cell_in_excel_file(excel_file, f'E4')

        login_pouch_ios(self.driver, username, pwd)

        tutorial_welcome(self.driver)

        add_dependent_btn = wait_accessibility_id(self.driver, 'dependentSectionButton')
        add_dependent_btn.click()

        relation = wait_xpath(self.driver, '//*[@name="Relationship (optional)"]')
        relation.click()
        relation_list = ['Spouse', 'Parent', 'Children', 'Sibling', 'Others']
        a = choice(relation_list)
        wait_xpath(self.driver, f'(//*[@name="{a}"])[1]').click()

        gender = wait_accessibility_id(self.driver, '  Gender')
        gender.click()
        gender_list = ['Male', 'Female', 'Others']
        b = choice(gender_list)
        wait_xpath(self.driver, f'(//*[@name="{b}"])[1]').click()

        full_name = wait_accessibility_id(self.driver, 'AddDependentFullname')
        full_name.send_keys(f'Test add dependent')

        write_to_file(generate_nricfin(), '/tmp/aqa/nric')
        nric = read_file('/tmp/aqa/nric')
        nricfin = wait_accessibility_id(self.driver, 'AddDependentNricfin')
        nricfin.send_keys(nric)

        email = wait_accessibility_id(self.driver, 'AddDependentEmail')
        email.send_keys(nric + '@gigacover.com')

        mobile = wait_accessibility_id(self.driver, 'AddDependentMobile')
        mobile.send_keys(generate_mobile_sgd())

        dob = self.driver.find_element_by_accessibility_id("  Date of Birth  ")
        dob.click()
        dob.click()
        wait_accessibility_id(self.driver, 'Confirm').click()

        wait_accessibility_id(self.driver, 'AddDependentSave').click()

        wait_xpath(self.driver, '//*[@name="SKIP"]').click()
        #endregion validate valid nricfin

        assert wait_accessibility_id(self.driver, 'Test add dependent dependentSectionButton').is_displayed() is True

    def test_verify_dependent_can_not_add_dependent(self):
        nric = read_file('/tmp/aqa/nric')

        #region verify benefit of dependent
        dependent_email = f'{nric}@gigacover.com'
        skip_opt(email=dependent_email.lower())
        login_pouch_ios(self.driver, dependent_email, nric)
        tutorial_welcome(self.driver)
        #endregion verify benefit of dependent

        #region verify dependent can not add dependent
        self.driver.implicitly_wait(10)
        add_dependent_btn = self.driver.find_elements_by_accessibility_id('dependentSectionButton, dependentSectionButton')
        assert len(add_dependent_btn) == 0
        #endregion verify dependent can not add dependent

    def test_verify_benefit_of_dependent(self):
        nric = read_file('/tmp/aqa/nric')

        dependent_email = f'{nric}@gigacover.com'
        skip_opt(email=dependent_email.lower())
        login_pouch_ios(self.driver, dependent_email, nric)
        wait()
        tutorial_welcome(self.driver)

        #region verify benefit of dependent
        #region verify if primary has not added payment card, show correct message when dependant try to open E-Card
        wait_accessibility_id(self.driver, 'PolicyItemgp').click()
        wait_xpath(self.driver, '//*[@name="CLOSE"]').click()
        wait()
        tutorial_essential(self.driver)

        active_E_Card(self.driver)
        # endregion verify if primary has not added payment card, show correct message when dependant try to open E-Card

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="Medical Card"]/../XCUIElementTypeOther').click()

        #region check info of GP
        GP = wait_xpath(self.driver, '//*[@name="Doctor (GP)"]').is_displayed()
        assert GP is True

        GP_consult_rate = wait_accessibility_id(self.driver, 'gpConsult Rate').text
        assert  GP_consult_rate == '$6.50'

        GP_subsidy_per_visit = wait_accessibility_id(self.driver, 'gpTotal Subsidy per Visit').text
        assert GP_subsidy_per_visit == '-'

        GP_subsidy_remaining = wait_accessibility_id(self.driver, 'gpSubsidy Remaining').text
        assert GP_subsidy_remaining == '-'
        #endregion check info of GP

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="Doctor (GP)"]/../XCUIElementTypeOther[1]').click()

        #region check info of TCM
        wait_accessibility_id(self.driver, 'PolicyItemtcm').click()
        wait_xpath(self.driver, '//*[@name="CLOSE"]').click()

        TCM = wait_xpath(self.driver, '//*[@name="TCM"]').is_displayed()
        assert TCM is True

        TCM_consult = wait_accessibility_id(self.driver, 'tcmConsult Rate').text
        TCM_consult = TCM_consult.replace('\n', '')
        assert TCM_consult == '$18 or less (Cashless)'

        TCM_Procedure_Medicine = wait_accessibility_id(self.driver, 'tcmProcedure & Medicine').text
        TCM_Procedure_Medicine = TCM_Procedure_Medicine.replace('\n', '')
        assert TCM_Procedure_Medicine == 'Corporate rate (Cash payment)'

        TCM_subsidy_remaining = wait_accessibility_id(self.driver, 'tcmSubsidy Remaining').text
        assert TCM_subsidy_remaining == '-'
        #endregion check info of TCM

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="TCM"]/../XCUIElementTypeOther[1]').click()

        #region check info of Dental
        wait_accessibility_id(self.driver, 'PolicyItemdental').click()
        wait_xpath(self.driver, '//*[@name="CLOSE"]').click()

        dental = wait_xpath(self.driver, '//*[@name="Dental"]').is_displayed()
        assert dental is True

        Dental_rate = wait_accessibility_id(self.driver, 'dentalConsult Rate').text
        Dental_rate = Dental_rate.replace('\n', ' ')
        assert Dental_rate == 'Corporate rate (Cashless up to Limit)'

        Dental_subsidy_remaining = wait_accessibility_id(self.driver, 'dentalSubsidy Remaining').text
        assert Dental_subsidy_remaining == '-'
        #endregion check info of Dental

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="Dental"]/../XCUIElementTypeOther[1]').click()

        wait_accessibility_id(self.driver, 'Account').click()

        #region check personal info
        assert isDisplayed_id(self.driver, 'Test add dependent ') is True
        assert isDisplayed_id(self.driver, nric) is True
        assert isDisplayed_id(self.driver, dependent_email.lower()) is True
        #endregion check personal info
        #endregion verify benefit of dependent

    def test_verify_benefit_of_primary(self):
        username = read_cell_in_excel_file(excel_file, f'F4')
        pwd = read_cell_in_excel_file(excel_file, f'E4')

        login_pouch_ios(self.driver, username, pwd)
        wait()
        tutorial_welcome(self.driver)

        #region verify benefit of primary
        wait_accessibility_id(self.driver, 'PolicyItemgp').click()
        wait_xpath(self.driver, '//*[@name="CLOSE"]').click()
        wait()
        tutorial_essential(self.driver)

        active_E_Card(self.driver)

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="Medical Card"]/../XCUIElementTypeOther').click()

        #region check info of GP
        GP = wait_xpath(self.driver, '//*[@name="Doctor (GP)"]').is_displayed()
        assert GP is True

        GP_consult_rate = wait_accessibility_id(self.driver, 'gpConsult Rate').text
        if read_cell_in_excel_file(excel_file, f'O4') == 'No':
            consult_rate = read_cell_in_excel_file(excel_file, f'Y4')
            assert GP_consult_rate == '$' + str(consult_rate) + '.00'
        else:
            assert  GP_consult_rate == 'Sponsored'

        GP_subsidy_per_visit = wait_accessibility_id(self.driver, 'gpTotal Subsidy per Visit').text
        if read_cell_in_excel_file(excel_file, f'P4') == 'Yes':
            assert GP_subsidy_per_visit == '$200.00'
        else:
            sponsor = '$' + str(read_cell_in_excel_file(excel_file, f'Q4')) + '.00'
            assert GP_subsidy_per_visit == sponsor

        GP_subsidy_remaining = wait_accessibility_id(self.driver, 'gpSubsidy Remaining').text
        assert GP_subsidy_remaining == '$200.00'
        #endregion check info of GP

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="Doctor (GP)"]/../XCUIElementTypeOther[1]').click()

        #region check info of TCM
        wait_accessibility_id(self.driver, 'PolicyItemtcm').click()
        wait_xpath(self.driver, '//*[@name="CLOSE"]').click()

        TCM = wait_xpath(self.driver, '//*[@name="TCM"]').is_displayed()
        assert TCM is True

        TCM_consult = wait_accessibility_id(self.driver, 'tcmConsult Rate').text
        TCM_consult = TCM_consult.replace('\n', '')
        if read_cell_in_excel_file(excel_file, f'S4') == 'Yes':
            assert TCM_consult == 'Sponsored'
        else:
            assert TCM_consult == '$18 or less (Cashless)'

        TCM_Procedure_Medicine = wait_accessibility_id(self.driver, 'tcmProcedure & Medicine').text
        TCM_Procedure_Medicine = TCM_Procedure_Medicine.replace('\n', '')
        assert TCM_Procedure_Medicine == 'Corporate rate (Cash payment)'

        TCM_subsidy_remaining = wait_accessibility_id(self.driver, 'tcmSubsidy Remaining').text
        assert TCM_subsidy_remaining == '$100.00'
        #endregion check info of TCM

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="TCM"]/../XCUIElementTypeOther[1]').click()

        #region check info of Dental
        wait_accessibility_id(self.driver, 'PolicyItemdental').click()
        wait_xpath(self.driver, '//*[@name="CLOSE"]').click()

        dental = wait_xpath(self.driver, '//*[@name="Dental"]').is_displayed()
        assert dental is True

        Dental_rate = wait_accessibility_id(self.driver, 'dentalConsult Rate').text
        Dental_rate = Dental_rate.replace('\n', ' ')
        assert Dental_rate == 'Corporate rate (Cashless up to Limit)'

        Dental_subsidy_remaining = wait_accessibility_id(self.driver, 'dentalSubsidy Remaining').text
        assert Dental_subsidy_remaining == '$100.00'
        #endregion check info of Dental

        wait_xpath(self.driver, '//XCUIElementTypeStaticText[@name="Dental"]/../XCUIElementTypeOther[1]').click()

        wait_accessibility_id(self.driver, 'Account').click()

        #region check personal info
        primary_name = read_cell_in_excel_file(excel_file, f'D4')
        assert isDisplayed_id(self.driver, f'{primary_name} ') is True

        primary_nricfin = read_cell_in_excel_file(excel_file, f'E4')
        assert isDisplayed_id(self.driver, primary_nricfin) is True

        primary_email = read_cell_in_excel_file(excel_file, f'F4')
        assert isDisplayed_id(self.driver, primary_email) is True
        #endregion check personal info
        #endregion verify benefit of primary
