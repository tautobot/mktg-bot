import unittest

from testcases.lib.generic import read_cell_in_excel_file
from aQA.webdriver.appium_weddriver import *
from aQA.iOS.src.app_file.util_ios import login_pouch_ios, verify_can_claim, claim, verify_past_claim

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
excel_file = f'{app_path}/fixtures/flep_template.xlsx'


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = ios_webdriver(app_name='pouch')


    def tearDown(self): self.driver.quit()


    def test_flep_claim(self):
        email = read_cell_in_excel_file(excel_file, 'E2')
        pwd = read_cell_in_excel_file(excel_file, 'D2')
        login_pouch_ios(self.driver, email, pwd)
        claim(self.driver, 'FLEP')
        # verify_past_claim(self.driver, 'FLEP')


    def test_flep_verify_policy_in_force(self):
        email = read_cell_in_excel_file(excel_file, f'E3')
        pwd = read_cell_in_excel_file(excel_file, f'D3')
        verify_can_claim(self.driver, email, pwd, 'FLEP')


    def test_flep_verify_policy_expired_inforce(self):
        email = read_cell_in_excel_file(excel_file, f'E4')
        pwd = read_cell_in_excel_file(excel_file, f'D4')
        verify_can_claim(self.driver, email, pwd, 'FLEP')


    def test_flep_verify_policy_expired_paid(self):
        email = read_cell_in_excel_file(excel_file, f'E5')
        pwd = read_cell_in_excel_file(excel_file, f'D5')
        verify_can_claim(self.driver, email, pwd, 'FLEP')


    def test_flep_verify_policy_expired_inforce_paid(self):
        email = read_cell_in_excel_file(excel_file, f'E8')
        pwd = read_cell_in_excel_file(excel_file, f'D8')
        verify_can_claim(self.driver, email, pwd, 'FLEP')


    def test_flep_verify_policy_inforce_paid(self):
        email = read_cell_in_excel_file(excel_file, f'E11')
        pwd = read_cell_in_excel_file(excel_file, f'D11')
        verify_can_claim(self.driver, email, pwd, 'FLEP')
