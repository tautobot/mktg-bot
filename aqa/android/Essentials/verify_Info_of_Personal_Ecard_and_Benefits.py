import unittest

from testcases.lib.generic import read_cell_in_excel_file
from aQA.webdriver.appium_weddriver import *
from aQA.android.src.app_file.util import *

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver(app_name='pouch')

    def tearDown(self): self.driver.quit()

    def test_verify_Ecard_and_Benefits(self):
        email = read_cell_in_excel_file(excel_file, f'F4')
        pwd = read_cell_in_excel_file(excel_file, f'E4')

        login_pouch(self.driver, email, pwd)
        wait()
        tutorial_welcome(self.driver)

        wait()
        wait_xpath(self.driver, '//*[@text="Doctor (GP)"]').click()
        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()

        wait()
        tutorial_essential(self.driver)
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Consultations"]'), wait_xpath(self.driver, "//*[@text='Doctor (GP)']"))

        wait()
        active_E_Card(self.driver)

        self.driver.back()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Consultations"]'), wait_xpath(self.driver, "//*[@text='More Services']"))

        #region check info of GP
        GP = wait_xpath(self.driver, '//*[@text="Doctor (GP)"]').is_displayed()
        assert GP is True

        GP_consult_rate = wait_xpath(self.driver, '//android.widget.TextView[@text="Consult Rate"]/../android.widget.TextView[4]').text
        if read_cell_in_excel_file(excel_file, f'O4') == 'No':
            consult_rate =  read_cell_in_excel_file(excel_file, f'Y4')
            assert GP_consult_rate == '$' + str(consult_rate) + '.00'
        else:
            assert  GP_consult_rate == 'Sponsored'

        GP_subsidy_per_visit = wait_xpath(self.driver, '//android.widget.TextView[@text="Total Subsidy per Visit"]/../android.widget.TextView[5]').text
        if read_cell_in_excel_file(excel_file, f'P4') == 'Yes':
            assert GP_subsidy_per_visit == '$200.00'
        else:
            sponsor = '$' + str(read_cell_in_excel_file(excel_file, f'Q4')) + '.00'
            assert GP_subsidy_per_visit == sponsor

        GP_subsidy_remaining = wait_xpath(self.driver, '//android.widget.TextView[@text="Subsidy Remaining"]/../android.widget.TextView[7]').text
        assert GP_subsidy_remaining == '$200.00'
        #endregion

        self.driver.back()

        #region check info of TCM
        wait()
        wait_xpath(self.driver, '//*[@text="Traditional Chinese Medicine"]').click()
        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()

        TCM = wait_xpath(self.driver, '//*[@text="TCM"]').is_displayed()
        assert TCM is True

        TCM_consult = wait_xpath(self.driver, '//android.widget.TextView[@text="Consult Rate"]/../android.widget.TextView[4]').text
        TCM_consult = TCM_consult.replace('\n', '')
        if read_cell_in_excel_file(excel_file, f'S4') == 'Yes':
            assert TCM_consult == 'Sponsored'
        else:
            assert TCM_consult == '$18 or less (Cashless)'

        TCM_Procedure_Medicine = wait_xpath(self.driver, '//android.widget.TextView[@text="Procedure & Medicine"]/../android.widget.TextView[5]').text
        TCM_Procedure_Medicine = TCM_Procedure_Medicine.replace('\n', '')
        assert TCM_Procedure_Medicine == 'Corporate rate (Cash payment)'

        TCM_subsidy_remaining = wait_xpath(self.driver, '//android.widget.TextView[@text="Subsidy Remaining"]/../android.widget.TextView[7]').text
        assert TCM_subsidy_remaining == '$100.00'
        #endregion

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
        assert Dental_subsidy_remaining == '$100.00'
        #endregion

        self.driver.back()

        wait()
        wait_xpath(self.driver, '//*[@text="Account"]').click()

        #region check personal info
        primary_name = read_cell_in_excel_file(excel_file, f'D4')
        name = wait_xpath(self.driver, '(//*[@text="Personal Details"]/../../android.widget.TextView)[1]').text
        assert name == f'{primary_name} '

        primary_nricfin = read_cell_in_excel_file(excel_file, f'E4')
        nricfin = wait_xpath(self.driver, '(//*[@text="Personal Details"]/../../android.widget.TextView)[2]').text
        assert nricfin == primary_nricfin

        primary_email = read_cell_in_excel_file(excel_file, f'F4')
        email = wait_xpath(self.driver, '(//*[@text="Personal Details"]/../../android.widget.TextView)[3]').text
        assert email == primary_email
        #endregion

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Balance"]'), wait_xpath(self.driver, "//*[@text='Personal Details']"))

        wait_xpath(self.driver, '//*[@text="Logout"]').click()
