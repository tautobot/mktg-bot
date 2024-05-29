import unittest
from random import choice
from datetime import date, timedelta

from testcases.lib.generic import skip_opt, read_cell_in_excel_file, generate_mobile_sgd
from aQA.webdriver.appium_weddriver import *
from aQA.android.src.app_file.util import write_to_file, generate_nricfin, read_file, \
login_pouch, wait, tutorial_welcome, tutorial_essential, wait_xpath, active_E_Card, \
    add_dependent

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver(app_name='pouch')

    def tearDown(self): self.driver.quit()

    def test_add_dependent(self):
        user = read_cell_in_excel_file(excel_file, f'F4')
        pwd = read_cell_in_excel_file(excel_file, f'E4')

        login_pouch(self.driver, user, pwd)
        wait()
        tutorial_welcome(self.driver)

        add_dependent_btn = self.driver.find_element_by_accessibility_id('dependentSectionButton, dependentSectionButton')
        add_dependent_btn.click()

        #region validate required field
        wait()

        save = wait_xpath(self.driver, '//*[@text="Save"]')
        save.click()

        wait()
        assert wait_xpath(self.driver, '//*[@text="Please enter a name"]').is_displayed() is True
        assert wait_xpath(self.driver, '//*[@text="Please enter a valid NRIC number"]').is_displayed() is True
        assert wait_xpath(self.driver, '//*[@text="Please select a gender"]').is_displayed() is True

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="NRIC"]'), wait_xpath(self.driver, "//*[@text='Add a dependent']"))

        assert wait_xpath(self.driver, '//*[@text="Please select a date of birth"]').is_displayed() is True
        #endregion validate required field

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="NRIC"]'), wait_xpath(self.driver, "//*[@text='Date of Birth']"))

        relation = wait_xpath(self.driver, '//*[@text="Relationship (optional)"]')
        relation.click()
        relation_list = ['Spouse', 'Parent', 'Children', 'Sibling', 'Others']
        a = choice(relation_list)
        wait_xpath(self.driver, f'//*[@text="{a}"]').click()

        full_name = wait_xpath(self.driver, '//*[@text="Full name"]')
        full_name.send_keys(f'Test add dependent 1')

        gender = wait_xpath(self.driver, '//*[@text="Gender"]')
        gender.click()
        gender_list = ['Male', 'Female', 'Others']
        b = choice(gender_list)
        wait_xpath(self.driver, f'//*[@text="{b}"]').click()

        write_to_file(generate_nricfin(), '/tmp/aqa/nric')
        nric = read_file('/tmp/aqa/nric')
        email = wait_xpath(self.driver, '//*[@text="Email (optional)"]')
        email.send_keys(nric + '@gigacover.com')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="NRIC"]'), wait_xpath(self.driver, "//*[@text='Add a dependent']"))

        mobile = wait_xpath(self.driver, '//*[@text="Mobile Number (optional)"]')
        mobile.send_keys(generate_mobile_sgd())

        dob = wait_xpath(self.driver, '//*[@text="Date of Birth"]')
        dob.click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()

        save = wait_xpath(self.driver, '//*[@text="Save"]')
        save.click()

        # region validate invalid nricfin
        nricfin = wait_xpath(self.driver, '//*[@text="NRIC"]/../android.widget.EditText')
        nricfin.send_keys('abc123')

        assert wait_xpath(self.driver, '//*[@text="Please input valid NRIC FIN"]').is_displayed() is True
        #endregion validate invalid nricfin

        #region validate valid nricfin
        nricfin.clear()
        nricfin.send_keys(nric)

        save = wait_xpath(self.driver, '//*[@text="Save"]')
        save.click()

        wait()
        wait_xpath(self.driver, '//*[@text="SKIP"]').click()
        #endregion validate valid nricfin

        dependent_name = wait_xpath(self.driver, f'(//android.widget.HorizontalScrollView//android.widget.TextView)[1]').text
        assert dependent_name == f'Test add dependent 1'

    def test_verify_benefit_of_dependent(self):
        nric = read_file('/tmp/aqa/nric')

        #region verify benefit of dependent
        dependent_email = f'{nric}@gigacover.com'
        skip_opt(email=dependent_email.lower())
        login_pouch(self.driver, dependent_email, nric)
        wait()
        tutorial_welcome(self.driver)
        #endregion verify benefit of dependent

        #region verify dependent can not add dependent
        self.driver.implicitly_wait(20)
        add_dependent_btn = self.driver.find_elements_by_accessibility_id('dependentSectionButton, dependentSectionButton')
        assert len(add_dependent_btn) == 0
        #endregion verify dependent can not add dependent

        #region verify if primary has not added payment card, show correct message when dependant try to open E-Card
        wait()
        wait_xpath(self.driver, '//*[@text="Doctor (GP)"]').click()
        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()
        wait()
        tutorial_essential(self.driver)

        wait()
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Consultations"]'), wait_xpath(self.driver, "//*[@text='Doctor (GP)']"))

        active_E_Card(self.driver)
        #endregion verify if primary has not added payment card, show correct message when dependant try to open E-Card

        self.driver.back()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Consultations"]'), wait_xpath(self.driver, "//*[@text='More Services']"))

        #region check info of GP
        GP = wait_xpath(self.driver, '//*[@text="Doctor (GP)"]').is_displayed()
        assert GP is True

        GP_consult_rate = wait_xpath(self.driver, '(//android.widget.TextView[@text="Consult Rate"]/../android.widget.TextView)[4]').text
        assert  GP_consult_rate == '$6.50'

        GP_subsidy_per_visit = wait_xpath(self.driver, '(//android.widget.TextView[@text="Total Subsidy per Visit"]/../android.widget.TextView)[5]').text
        assert GP_subsidy_per_visit == '-'

        GP_subsidy_remaining = wait_xpath(self.driver, '(//android.widget.TextView[@text="Subsidy Remaining"]/../android.widget.TextView)[7]').text
        assert GP_subsidy_remaining == '-'
        #endregion check info of GP

        self.driver.back()

        #region check info of TCM
        wait()
        wait_xpath(self.driver, '//*[@text="Traditional Chinese Medicine"]').click()
        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()

        TCM = wait_xpath(self.driver, '//*[@text="TCM"]').is_displayed()
        assert TCM is True

        TCM_consult = wait_xpath(self.driver, '//android.widget.TextView[@text="Consult Rate"]/../android.widget.TextView[4]').text
        TCM_consult = TCM_consult.replace('\n', '')
        assert TCM_consult == '$18 or less (Cashless)'

        TCM_Procedure_Medicine = wait_xpath(self.driver, '//android.widget.TextView[@text="Procedure & Medicine"]/../android.widget.TextView[5]').text
        TCM_Procedure_Medicine = TCM_Procedure_Medicine.replace('\n', '')
        assert TCM_Procedure_Medicine == 'Corporate rate (Cash payment)'

        TCM_subsidy_remaining = wait_xpath(self.driver, '//android.widget.TextView[@text="Subsidy Remaining"]/../android.widget.TextView[7]').text
        assert TCM_subsidy_remaining == '-'
        #endregion check info of TCM

        self.driver.back()
        wait()
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Traditional Chinese Medicine"]'), wait_xpath(self.driver, "//*[@text='Doctor (GP)']"))

        #region check info of Dental
        wait()
        wait_xpath(self.driver, '//*[@text="Dental"]').click()
        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()

        dental = wait_xpath(self.driver, '//*[@text="Dental"]').is_displayed()
        assert dental is True

        Dental_rate = wait_xpath(self.driver, '//android.widget.TextView[@text="Consult Rate"]/../android.widget.TextView[3]').text
        Dental_rate = Dental_rate.replace('\n', ' ')
        assert Dental_rate == 'Corporate rate (Cashless up to Limit)'

        Dental_subsidy_remaining = wait_xpath(self.driver, '//android.widget.TextView[@text="Subsidy Remaining"]/../android.widget.TextView[5]').text
        assert Dental_subsidy_remaining == '-'
        #endregion check info of Dental

        self.driver.back()

        wait()
        wait_xpath(self.driver, '//*[@text="Account"]').click()

        #region check personal info
        name = wait_xpath(self.driver, '(//*[@text="Personal Details"]/../../android.widget.TextView)[1]').text
        assert name == 'Test add dependent 1 '

        nricfin = wait_xpath(self.driver, '(//*[@text="Personal Details"]/../../android.widget.TextView)[2]').text
        assert nricfin == nric

        email = wait_xpath(self.driver, '(//*[@text="Personal Details"]/../../android.widget.TextView)[3]').text
        assert email == dependent_email.lower()
        #endregion check personal info

    def test_verify_limit_dependent(self):
        user = read_cell_in_excel_file(excel_file, f'F5')
        pwd = read_cell_in_excel_file(excel_file, f'E5')

        login_pouch(self.driver, user, pwd)
        wait()
        tutorial_welcome(self.driver)

        active_E_Card(self.driver, 'home screen')

        for j in range (4):
            add_dependent(self.driver)
            if j > 0: wait_xpath(self.driver, '//*[@text="OK"]').click()
            wait()

        self.driver.implicitly_wait(10)
        add_dependent_btn = self.driver.find_elements_by_accessibility_id('dependentSectionButton, dependentSectionButton')
        assert len(add_dependent_btn) == 0

    def test_verify_popup_adding_dependent(self):
        user = read_cell_in_excel_file(excel_file, f'F6')
        pwd = read_cell_in_excel_file(excel_file, f'E6')

        login_pouch(self.driver, user, pwd)
        wait()
        tutorial_welcome(self.driver)

        active_E_Card(self.driver, 'home screen')

        for i in range(2):
            add_dependent(self.driver)
            wait()

        #region verify popup
        wait()
        text1 = wait_xpath(self.driver, '//android.widget.TextView[3]').text
        assert text1 == "Please note that we require up to 3-5 working days to process and update your dependent's information with our partners."

        d = (date.today() + timedelta(days=7)).strftime('%d %b %Y')
        text2 = wait_xpath(self.driver, '//android.widget.TextView[4]').text
        assert text2 == f"Please let your dependents know they should only visit GP, TCM and Dental clinics from {d} onwards to ensure a seamless experience."

        text3 = wait_xpath(self.driver, '//android.widget.TextView[5]').text
        assert text3 == "You can contact us at hey@gigacover.com if you have any questions"
        #endregion verify popup
