import unittest

from testcases.lib.generic import read_cell_in_excel_file
from aQA.webdriver.appium_weddriver import *
from aQA.android.src.app_file.util import *

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'

def setUpModule():    pass  # nothing here for now
def tearDownModule(): pass  # nothing here for now


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver(app_name='pouch')

    def tearDown(self):
        self.driver.quit()

    def test_book_healthscreen(self):
        email = read_cell_in_excel_file(excel_file, 'F4')
        pwd = read_cell_in_excel_file(excel_file, 'E4')

        login_pouch(self.driver, email, pwd)
        wait()
        tutorial_welcome(self.driver)

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Traditional Chinese Medicine"]'), wait_xpath(self.driver, "//*[@text='Doctor (GP)']"))
        wait()
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Dental"]'), wait_xpath(self.driver, "//*[@text='Traditional Chinese Medicine']"))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Dental"]'), wait_xpath(self.driver, "//*[@text='Traditional Chinese Medicine']"))

        wait()
        wait_xpath(self.driver, '//*[@text="Healthscreen"]').click()

        wait()
        wait_xpath(self.driver, '//*[@text="SKIP"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="DONE"]').click()

        wait_xpath(self.driver, '//*[@text="Book My Healthscreen"]').click()
        wait_xpath(self.driver, '//*[@text="Proceed"]').click()
        wait()

        package = self.driver.current_package
        assert package == 'com.android.chrome'
