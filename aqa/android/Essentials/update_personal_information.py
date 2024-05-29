import unittest

from testcases.lib.generic import read_cell_in_excel_file, get_default_password
from aQA.webdriver.appium_weddriver import *
from aQA.android.src.app_file.util import *

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver(app_name='pouch')

    def tearDown(self): self.driver.quit()

    def test_00_update_information(self):
        excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'
        username = read_cell_in_excel_file(excel_file, f'F2')
        pwd = get_default_password(2)

        login_pouch(self.driver, username, pwd)

        wait()

        #region validate required field
        wait_xpath(self.driver, '//*[@text="START"]').click()

        add_nric_btn = wait_xpath(self.driver, '//*[@text="ADD NRIC"]')
        add_nric_btn.click()

        nricfin = wait_xpath(self.driver, '//*[@text="NRIC"]')
        nricfin.send_keys('abc123')

        save_btn = wait_xpath(self.driver, '//*[@text="Save"]')
        save_btn.click()

        assert wait_xpath(self.driver, '//*[@text="Please enter a valid NRIC number"]').is_displayed() is True
        #endregion validate required field

        #region input valid information
        nric = username.split('@')[0]
        nricfin.clear()
        nricfin.send_keys(nric)
        save_btn.click()

        assert wait_xpath(self.driver, '//*[@text="Medical eCard"]').is_displayed() is True
        #region input valid information

    def test_00_update_information_with_existed_nricfin(self):
        excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'
        username = read_cell_in_excel_file(excel_file, f'F3')
        pwd = get_default_password(3)

        login_pouch(self.driver, username, pwd)
        wait()

        #region input existed nricfin
        wait_xpath(self.driver, '//*[@text="START"]').click()

        add_nric_btn = wait_xpath(self.driver, '//*[@text="ADD NRIC"]')
        add_nric_btn.click()

        nric = read_cell_in_excel_file(excel_file, f'E4') # existed nricfin
        nricfin = wait_xpath(self.driver, '//*[@text="NRIC"]')
        nricfin.send_keys(nric)

        save_btn = wait_xpath(self.driver, '//*[@text="Save"]')
        save_btn.click()

        #verify error msg
        wait()
        assert wait_xpath(self.driver, '//*[@text="You currently have your nric registered with another account. Please contact hey@gigacover.com for more details!"]').is_displayed() is True
        #endregion input existed nricfin

